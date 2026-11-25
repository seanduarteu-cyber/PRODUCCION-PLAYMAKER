"""Propuesta comercial 2027 para Los Leones de Quilpué en Excel, con el formato de la valorización FEVOCHI.

Uso:
    python3 propuestas/leones-quilpue/generar_propuesta_excel.py

Lee la solicitud del club (Solicitud_indumentaria_CDC_Los_Leones_2027_v2.xlsx, hojas LNB y LNF, prendas por talla)
y los precios de lista del simulador interno (Canje_Leones_Quilpue_2027.xlsx, hoja Precios), y crea
Propuesta_Comercial_Los_Leones_2027.xlsm:
  - RESUMEN: por equipo y sección, valor del canje (a precio público general) y valor a precio club de lo que se
    paga (neto e IVA); valor por producto. Vínculo GENERAR PDF PARA EL CLUB (macro): exporta a PDF todas las hojas
    visibles menos COSTOS.
  - PRECIOS: por producto, precio público general, descuento y precio club (con IVA). El precio club es el de lo
    que el club compre fuera del canje y el de las series formativas.
  - LNB 2027 y LNF 2027: lo solicitado por el club, por sección y prenda: tallas, unidades, precios, canje
    (SÍ: 100% de descuento; viene marcado en todo lo solicitado por los primeros equipos y su cuerpo técnico) y
    valor a pagar.
  - FORMATIVAS 2027: lista de productos a precio club para las series formativas; unidades por completar con la
    proyección de compra del club.
  - COSTOS (uso interno): costo unitario y código de inventario por producto, costo del canje y de lo vendido,
    venta neta y resultado. No va en el PDF.
Si la planilla ya existe, se conservan los precios, descuentos, unidades, canje y costos cargados en ella.
"""

import sys
from pathlib import Path

import openpyxl
from openpyxl.drawing.image import Image as XLImage
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.hyperlink import Hyperlink

DIR = Path(__file__).parent
sys.path.insert(0, str(DIR))
sys.path.insert(0, str(DIR.parent))
from generar_propuesta import PRENDAS, PRODUCTOS, SECCIONES, clave  # noqa: E402
from vba_proyecto import agregar_vba  # noqa: E402

SOLICITUD = DIR / "Solicitud_indumentaria_CDC_Los_Leones_2027_v2.xlsx"
SIMULADOR = DIR / "Canje_Leones_Quilpue_2027.xlsx"
SALIDA = DIR / "Propuesta_Comercial_Los_Leones_2027.xlsm"
LOGO = DIR.parent / "_recursos" / "playmaker_logo_horizontal_navy.png"
IVA = 0.19
DESCUENTO = 0.10  # descuento general sobre el precio público (precio club y formativas)
HOJA_INTERNA = "COSTOS"
EQUIPOS = [("LNB", "LNB 2027", "Primer equipo masculino, Liga Nacional de Básquetbol"),
           ("LNF", "LNF 2027", "Primer equipo femenino, Liga Nacional Femenina")]
LINEAS = ["Juego", "Entrenamiento", "Presentación y viaje", "Socios e hinchas"]

MACRO_PDF = """' Genera el PDF de la propuesta para el club: todas las hojas visibles menos COSTOS (uso interno).
Sub GenerarPDFClub()
    Dim hojas() As Variant, n As Integer, ws As Worksheet, ruta As String, activa As Worksheet
    Set activa = ActiveSheet
    For Each ws In ThisWorkbook.Worksheets
        If ws.Name <> "COSTOS" And ws.Visible = xlSheetVisible Then
            n = n + 1
            ReDim Preserve hojas(1 To n)
            hojas(n) = ws.Name
        End If
    Next ws
    ruta = ThisWorkbook.Path & Application.PathSeparator & "Propuesta_Comercial_Los_Leones_2027.pdf"
    ThisWorkbook.Worksheets(hojas).Select
    ActiveSheet.ExportAsFixedFormat Type:=xlTypePDF, Filename:=ruta, Quality:=xlQualityStandard, _
        IncludeDocProperties:=True, IgnorePrintAreas:=False, OpenAfterPublish:=True
    activa.Select
    MsgBox "PDF guardado en: " & ruta, vbInformation, "PDF para el club"
End Sub
"""
EVENTO_VINCULO = """' El vinculo GENERAR PDF de la hoja RESUMEN (su texto de ayuda dice PDF) corre la macro.
Private Sub Workbook_SheetFollowHyperlink(ByVal Sh As Object, ByVal Target As Hyperlink)
    If InStr(1, Target.ScreenTip, "PDF", vbTextCompare) > 0 Then GenerarPDFClub
End Sub
"""


def texto(v):
    return " ".join(str(v or "").split())


def nombre_producto(k):
    return PRODUCTOS[k][0]


def leer_solicitud():
    """Por equipo: [(sección, [(prenda, producto, tallas, unidades)])], una fila por producto (la camiseta
    reversible con short se separa en camiseta y short)."""
    wb = openpyxl.load_workbook(SOLICITUD)
    equipos = {}
    for hoja, _, _ in EQUIPOS:
        ws = wb[hoja]
        secciones, seccion, tallas_cab = {}, None, {}
        for f in range(1, ws.max_row + 1):
            a, b = ws.cell(f, 1).value, ws.cell(f, 2).value
            fila = {c: ws.cell(f, c).value for c in range(4, 13)}
            if any(isinstance(v, str) and v.strip().upper() in ("XS", "S", "M") for v in fila.values()):
                tallas_cab = {c: texto(v) for c, v in fila.items() if isinstance(v, str)}
                continue
            if a and clave(a) in SECCIONES:
                seccion = SECCIONES[clave(a)]
            if not b or clave(b) not in PRENDAS:
                continue
            cant = {tallas_cab.get(c, "?"): int(v) for c, v in fila.items() if isinstance(v, (int, float)) and v}
            n = sum(cant.values())
            if not n:
                continue
            nombre, productos = PRENDAS[clave(b)]
            t = ", ".join(f"{k} {v}" for k, v in cant.items())
            for p in productos:
                prenda = nombre if len(productos) == 1 else f"{nombre}: {nombre_producto(p).lower()}"
                secciones.setdefault(seccion, []).append((prenda, p, t, n))
        equipos[hoja] = [(s, secciones[s]) for s in SECCIONES.values() if s in secciones]
    return equipos


def precios_lista():
    """Precio de lista por producto: el del simulador interno si existe, si no el de PRODUCTOS."""
    precios = {k: v[2] for k, v in PRODUCTOS.items()}
    if SIMULADOR.exists():
        pr = openpyxl.load_workbook(SIMULADOR)["Precios"]
        nombres = {v[0]: k for k, v in PRODUCTOS.items()}
        for r in range(5, pr.max_row + 1):
            n = texto(pr.cell(r, 1).value).replace(" (nueva)", "")
            if n in nombres and isinstance(pr.cell(r, 3).value, (int, float)):
                precios[nombres[n]] = pr.cell(r, 3).value
    return precios


def leer_previo():
    if not SALIDA.exists():
        return None
    wb = openpyxl.load_workbook(SALIDA)
    azul = lambda c: c.font is not None and c.font.color is not None and c.font.color.rgb == "FF0000FF"  # noqa: E731
    previo = {"precios": {}, "costos": {}, "celdas": {}}
    pr = wb["PRECIOS"]
    previo["iva"], previo["descuento"] = pr["C4"].value, pr["C5"].value
    for r in range(8, pr.max_row + 1):
        if pr.cell(r, 2).value and azul(pr.cell(r, 3)):
            previo["precios"][texto(pr.cell(r, 2).value)] = (pr.cell(r, 3).value, pr.cell(r, 4).value, pr.cell(r, 7).value)
    if HOJA_INTERNA in wb.sheetnames:
        co = wb[HOJA_INTERNA]
        for r in range(1, co.max_row + 1):
            if co.cell(r, 2).value and azul(co.cell(r, 4)):
                previo["costos"][texto(co.cell(r, 2).value)] = (co.cell(r, 3).value, co.cell(r, 4).value)
    for hoja in [h for _, h, _ in EQUIPOS] + ["FORMATIVAS 2027"]:
        if hoja in wb.sheetnames:
            for row in wb[hoja].iter_rows():
                for c in row:
                    if azul(c) and c.value is not None:
                        previo["celdas"][(hoja, c.coordinate)] = c.value
    return previo


def main():
    equipos = leer_solicitud()
    lista = precios_lista()
    previo = leer_previo()

    NAVY = "002060"
    f_tit = Font(name="Calibri", size=14, bold=True, color=NAVY)
    f_sec = Font(name="Calibri", size=12, bold=True, color=NAVY)
    f_sub = Font(name="Calibri", size=10, bold=True, color="B1A542")
    f_cab = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    f_norm = Font(name="Calibri", size=11)
    f_gris = Font(name="Calibri", size=10, color="595959")
    f_input = Font(name="Calibri", size=11, color="0000FF")
    f_tot = Font(name="Calibri", size=11, bold=True)
    f_gran = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    f_nota = Font(name="Calibri", size=10, italic=True, color="595959")
    r_cab = PatternFill("solid", fgColor=NAVY)
    r_input = PatternFill("solid", fgColor="FFF2CC")
    r_sub = PatternFill("solid", fgColor="D9E1F2")
    r_gran = PatternFill("solid", fgColor=NAVY)
    fino = Side(style="thin", color="A6A6A6")
    caja = Border(left=fino, right=fino, top=fino, bottom=fino)
    PESOS = '"$"#,##0;-"$"#,##0;"-"'
    NUM = '#,##0;-#,##0;"-"'
    PCT = '0.0%;-0.0%;"-"'
    centro = Alignment(horizontal="center", vertical="center", wrap_text=True)
    izq = Alignment(horizontal="left", vertical="center", wrap_text=True)

    wb = openpyxl.Workbook()

    def celda(ws, ref, valor, fuente=f_norm, formato=None, relleno=None, alinear=centro, borde=True):
        c = ws[ref]
        c.value, c.font, c.alignment = valor, fuente, alinear
        if formato:
            c.number_format = formato
        if relleno:
            c.fill = relleno
        if borde:
            c.border = caja
        return c

    def entrada(ws, ref, valor, formato=None, alinear=centro):
        v = previo["celdas"].get((ws.title, ref), valor) if previo else valor
        return celda(ws, ref, v, f_input, formato, r_input, alinear)

    def cabecera(ws, fila, col0, textos, alto=34):
        for k, t in enumerate(textos):
            celda(ws, ws.cell(fila, col0 + k).coordinate, t, f_cab, relleno=r_cab)
        ws.row_dimensions[fila].height = alto

    def encabezado(ws, titulo, bajada):
        if LOGO.exists():
            im = XLImage(str(LOGO))
            im.height, im.width = 20, int(20 * im.width / im.height)
            ws.add_image(im, "B1")
        celda(ws, "B2", titulo, f_tit, alinear=Alignment(vertical="center"), borde=False)
        celda(ws, "B3", bajada, f_nota, alinear=Alignment(vertical="center"), borde=False)
        ws.row_dimensions[1].height = 20
        ws.column_dimensions["A"].width = 3

    # ---------------------------------------------------------------- PRECIOS
    pr = wb.active
    pr.title = "PRECIOS"
    encabezado(pr, "PRECIOS POR PRODUCTO", "Precio público general (con IVA) y descuento: el precio club se calcula "
                                           "solo, terminado en 900, y aplica a lo que el club compre fuera del canje y "
                                           "a las series formativas.")
    celda(pr, "B4", "IVA", f_tot, alinear=izq)
    celda(pr, "C4", previo["iva"] if previo and previo.get("iva") is not None else IVA, f_input, "0%", r_input)
    celda(pr, "B5", "Descuento general para el club", f_tot, alinear=izq)
    celda(pr, "C5", previo["descuento"] if previo and previo.get("descuento") is not None else DESCUENTO, f_input,
          "0%", r_input)
    celda(pr, "D5", "Se aplica a los productos que no tienen un descuento propio en la columna DESCUENTO.", f_nota,
          alinear=Alignment(vertical="center"), borde=False)
    cabecera(pr, 7, 2, ["PRODUCTO", "PRECIO PÚBLICO GENERAL (CON IVA)", "DESCUENTO CLUB", "PRECIO CLUB (CON IVA)",
                        "PRECIO CLUB NETO", "OBSERVACIONES"], alto=36)
    fila_precio, r = {}, 8
    for linea in LINEAS:
        celda(pr, f"B{r}", linea.upper(), Font(name="Calibri", size=10, bold=True, color=NAVY), relleno=r_sub,
              alinear=izq)
        for col in "CDEFG":
            celda(pr, f"{col}{r}", None, relleno=r_sub)
        r += 1
        for k, (nombre, l, _p, _a, _ref) in PRODUCTOS.items():
            if l != linea:
                continue
            fila_precio[k] = r
            publico, desc, obs = (previo["precios"].get(nombre, (None, None, None)) if previo else (None, None, None))
            celda(pr, f"B{r}", nombre, alinear=izq)
            celda(pr, f"C{r}", publico if publico is not None else lista[k], f_input, PESOS, r_input)
            celda(pr, f"D{r}", desc, f_input, "0%", r_input)
            # precio con descuento llevado al valor terminado en 900 más cercano (como los precios de lista)
            celda(pr, f"E{r}", f'=IF(N(C{r})=0,0,ROUND((N(C{r})*(1-IF(D{r}="",$C$5,D{r}))-900)/1000,0)*1000+900)',
                  f_tot, PESOS)
            celda(pr, f"F{r}", f"=ROUND(E{r}/(1+$C$4),0)", formato=PESOS)
            celda(pr, f"G{r}", obs, f_input, relleno=r_input, alinear=izq)
            r += 1
    ultima_precio = r - 1
    for col, ancho in zip("BCDEFG", (38, 18, 13, 16, 15, 40)):
        pr.column_dimensions[col].width = ancho
    dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                        errorTitle="Precio", error="Ingresa un precio en pesos (0 o más).")
    pr.add_data_validation(dv)
    dv.add(f"C8:C{ultima_precio}")
    dvp = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True,
                         errorTitle="Descuento", error="Ingresa un porcentaje entre 0% y 100%.")
    pr.add_data_validation(dvp)
    dvp.add("C5")
    dvp.add(f"D8:D{ultima_precio}")

    def precio_de(k, col="E"):  # E: precio club; C: precio público
        return f"PRECIOS!${col}${fila_precio[k]}"

    # ---------------------------------------------------------------- LNB 2027 y LNF 2027
    detalle = {}  # hoja -> (secciones [(sección, primera fila, fila subtotal)], fila total)
    for equipo, hoja, descripcion in EQUIPOS:
        ws = wb.create_sheet(hoja)
        encabezado(ws, f"{hoja}: INDUMENTARIA SOLICITADA POR EL CLUB",
                   f"{descripcion}, jugadores y cuerpo técnico. CANJE SÍ = 100% de descuento en esa prenda. Celdas "
                   "amarillas editables.")
        cabecera(ws, 5, 2, ["PRENDA SOLICITADA", "PRODUCTO PLAYMAKER", "TALLAS", "UNIDADES", "PRECIO PÚBLICO",
                            "PRECIO CLUB", "CANJE", "VALOR A PAGAR"])
        dv_canje = DataValidation(type="list", formula1='"SÍ,NO"', allow_blank=True, errorTitle="Canje",
                                  error="Elige SÍ (canje, 100% de descuento) o NO.")
        dv_u = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                              errorTitle="Unidades", error="Ingresa un número entero (0 o más).")
        r, secs = 6, []
        for seccion, filas in equipos[equipo]:
            celda(ws, f"B{r}", seccion.upper(), f_sub, alinear=izq, borde=False)
            r += 1
            f0 = r
            for prenda, k, tallas, n in filas:
                celda(ws, f"B{r}", prenda, alinear=izq)
                celda(ws, f"C{r}", nombre_producto(k), f_gris, alinear=izq)
                celda(ws, f"D{r}", tallas, f_gris, alinear=izq)
                entrada(ws, f"E{r}", n, NUM)
                celda(ws, f"F{r}", "=" + precio_de(k, "C"), f_gris, PESOS)
                celda(ws, f"G{r}", "=" + precio_de(k), formato=PESOS)
                entrada(ws, f"H{r}", "SÍ")
                celda(ws, f"I{r}", f'=IF(H{r}="SÍ",0,E{r}*G{r})', f_tot, PESOS)
                r += 1
            dv_canje.add(f"H{f0}:H{r - 1}")
            dv_u.add(f"E{f0}:E{r - 1}")
            celda(ws, f"B{r}", f"Total {seccion.split(': ')[-1]}", f_tot, relleno=r_sub, alinear=izq)
            for col in "CDFGH":
                celda(ws, f"{col}{r}", None, relleno=r_sub)
            celda(ws, f"E{r}", f"=SUM(E{f0}:E{r - 1})", f_tot, NUM, r_sub)
            celda(ws, f"I{r}", f"=SUM(I{f0}:I{r - 1})", f_tot, PESOS, r_sub)
            secs.append((seccion, f0, r))
            r += 2
        celda(ws, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
        for col in "CDEFGHI":
            celda(ws, f"{col}{r}", None, f_gran, relleno=r_gran)
        celda(ws, f"E{r}", "=" + "+".join(f"E{s}" for _, _, s in secs), f_gran, NUM, r_gran)
        celda(ws, f"I{r}", "=" + "+".join(f"I{s}" for _, _, s in secs), f_gran, PESOS, r_gran)
        ws.row_dimensions[r].height = 20
        ws.add_data_validation(dv_canje)
        ws.add_data_validation(dv_u)
        for col, ancho in zip("BCDEFGHI", (40, 30, 30, 11, 13, 13, 9, 15)):
            ws.column_dimensions[col].width = ancho
        ws.freeze_panes = "B6"
        detalle[hoja] = (secs, r)

    # ---------------------------------------------------------------- FORMATIVAS 2027
    fo = wb.create_sheet("FORMATIVAS 2027")
    encabezado(fo, "SERIES FORMATIVAS: PRECIO CLUB POR PRODUCTO",
               "Las series formativas compran a precio club. Unidades por completar con la proyección de compra del "
               "club (celdas amarillas).")
    cabecera(fo, 5, 2, ["PRODUCTO", "LÍNEA", "PRECIO PÚBLICO", "PRECIO CLUB", "UNIDADES", "VALOR A PAGAR"])
    r = 6
    fo0 = r
    for k, (nombre, l, _p, _a, _ref) in PRODUCTOS.items():
        celda(fo, f"B{r}", nombre, alinear=izq)
        celda(fo, f"C{r}", l, f_gris, alinear=izq)
        celda(fo, f"D{r}", "=" + precio_de(k, "C"), f_gris, PESOS)
        celda(fo, f"E{r}", "=" + precio_de(k), f_tot, PESOS)
        entrada(fo, f"F{r}", None, NUM)
        celda(fo, f"G{r}", f"=N(F{r})*E{r}", f_tot, PESOS)
        r += 1
    celda(fo, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    for col in "CDEFG":
        celda(fo, f"{col}{r}", None, f_gran, relleno=r_gran)
    celda(fo, f"F{r}", f"=SUM(F{fo0}:F{r - 1})", f_gran, NUM, r_gran)
    celda(fo, f"G{r}", f"=SUM(G{fo0}:G{r - 1})", f_gran, PESOS, r_gran)
    fo_tot = r
    dv_f = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                          errorTitle="Unidades", error="Ingresa un número entero (0 o más).")
    fo.add_data_validation(dv_f)
    dv_f.add(f"F{fo0}:F{fo_tot - 1}")
    for col, ancho in zip("BCDEFG", (38, 20, 14, 14, 12, 16)):
        fo.column_dimensions[col].width = ancho

    # ---------------------------------------------------------------- RESUMEN
    rs = wb.create_sheet("RESUMEN", 0)
    encabezado(rs, "PROPUESTA COMERCIAL 2027: CLUB DEPORTIVO COLEGIO LOS LEONES DE QUILPUÉ",
               "Valores con IVA. El canje (100% de descuento) se valoriza a precio público general; el resto, a precio "
               "club.")
    cabecera(rs, 5, 2, ["EQUIPO", "SECCIÓN", "UNIDADES", "VALOR TOTAL DEL CANJE (PRECIO PÚBLICO)",
                        "VALOR PRECIO CLUB", "NETO", "IVA"], alto=36)
    r, filas_total = 6, []

    def fila_resumen(r, equipo, seccion, unid, canje, pagar, fuente=f_norm, relleno=None):
        celda(rs, f"B{r}", equipo, fuente, relleno=relleno, alinear=izq)
        celda(rs, f"C{r}", seccion, fuente, relleno=relleno, alinear=izq)
        celda(rs, f"D{r}", unid, fuente, NUM, relleno)
        celda(rs, f"E{r}", canje, fuente, PESOS, relleno)
        celda(rs, f"F{r}", pagar, fuente if relleno else f_tot, PESOS, relleno)
        celda(rs, f"G{r}", f"=ROUND(F{r}/(1+PRECIOS!$C$4),0)", fuente, PESOS, relleno)
        celda(rs, f"H{r}", f"=F{r}-G{r}", fuente, PESOS, relleno)

    for equipo, hoja, descripcion in EQUIPOS:
        secs, _tot = detalle[hoja]
        H = f"'{hoja}'"
        r0 = r
        for k, (seccion, f0, s) in enumerate(secs):
            e, fpub, h = (f"{H}!{c}{f0}:{c}{s - 1}" for c in "EFH")
            fila_resumen(r, f"{equipo} (primer equipo)" if k == 0 else None, seccion, f"={H}!E{s}",
                         f'=SUMPRODUCT(({h}="SÍ")*{e}*{fpub})', f"={H}!I{s}")
            r += 1
        fila_resumen(r, f"Total {equipo}", None, *[f"=SUM({c}{r0}:{c}{r - 1})" for c in "DEF"], f_tot, r_sub)
        filas_total.append(r)
        r += 1
    F = "'FORMATIVAS 2027'"
    fila_resumen(r, "Series formativas", "Compras a precio club", f"={F}!F{fo_tot}", 0, f"={F}!G{fo_tot}", f_tot, r_sub)
    filas_total.append(r)
    r += 1
    fila_resumen(r, "TOTAL GENERAL", None, *["=" + "+".join(f"{c}{x}" for x in filas_total) for c in "DEF"],
                 f_gran, r_gran)
    rs.row_dimensions[r].height = 22
    total_general = r

    r += 4
    celda(rs, f"B{r}", "VALOR POR PRODUCTO", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    cabecera(rs, r, 2, ["PRODUCTO", "PRECIO PÚBLICO", "DESCUENTO", "PRECIO CLUB", "TOTAL UNIDADES",
                        "VALOR TOTAL DEL CANJE (PRECIO PÚBLICO)", "VALOR PRECIO CLUB"], alto=36)
    r += 1
    p0 = r
    hojas_det = [f"'{h}'" for _, h, _ in EQUIPOS]
    fila_producto = {}
    for k, (nombre, *_x) in PRODUCTOS.items():
        fp = fila_precio[k]
        fila_producto[k] = r
        celda(rs, f"B{r}", nombre, alinear=izq)
        celda(rs, f"C{r}", f"=PRECIOS!C{fp}", f_gris, PESOS)
        celda(rs, f"D{r}", f"=IF(N(C{r})=0,0,1-E{r}/C{r})", formato=PCT)
        celda(rs, f"E{r}", f"=PRECIOS!E{fp}", formato=PESOS)
        unid = "+".join(f'SUMIF({h}!$C:$C,"{nombre}",{h}!$E:$E)' for h in hojas_det)
        celda(rs, f"F{r}", f'={unid}+SUMIF({F}!$B:$B,"{nombre}",{F}!$F:$F)', formato=NUM)
        canje = "+".join(f'SUMIFS({h}!$E:$E,{h}!$C:$C,"{nombre}",{h}!$H:$H,"SÍ")' for h in hojas_det)
        celda(rs, f"G{r}", f"=({canje})*C{r}", formato=PESOS)
        pagar = "+".join(f'SUMIF({h}!$C:$C,"{nombre}",{h}!$I:$I)' for h in hojas_det)
        celda(rs, f"H{r}", f'={pagar}+SUMIF({F}!$B:$B,"{nombre}",{F}!$G:$G)', f_tot, PESOS)
        r += 1
    celda(rs, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    for col in "CDE":
        celda(rs, f"{col}{r}", None, f_gran, relleno=r_gran)
    for col, fmt in (("F", NUM), ("G", PESOS), ("H", PESOS)):
        celda(rs, f"{col}{r}", f"=SUM({col}{p0}:{col}{r - 1})", f_gran, fmt, r_gran)
    celda(rs, f"B{r + 1}", f'=IF(AND(G{r}=E{total_general},H{r}=F{total_general}),"Control: la suma por producto '
                           f'coincide con el total general.","Revisar: la suma por producto no coincide con el total '
                           f'general.")', f_nota, alinear=Alignment(vertical="center"), borde=False)
    for col, ancho in zip("BCDEFGH", (38, 36, 14, 18, 17, 15, 14)):
        rs.column_dimensions[col].width = ancho
    rs.print_area = f"A1:H{r + 1}"

    # vínculo que genera el PDF para el club (macro GenerarPDFClub vía Workbook_SheetFollowHyperlink)
    celda(rs, "J2", "GENERAR PDF PARA EL CLUB", Font(name="Calibri", size=11, bold=True, color="FFFFFF",
                                                       underline="single"), relleno=r_gran)
    for col in "JKL":
        for fila in (2, 3):
            rs[f"{col}{fila}"].fill = r_gran
    rs.merge_cells("J2:L3")
    rs["J2"].hyperlink = Hyperlink(ref="J2", location="RESUMEN!J2",
                                   tooltip="Generar PDF para el club (todas las hojas menos COSTOS)")
    celda(rs, "J4", "Exporta todas las hojas menos COSTOS a un PDF en la misma carpeta de esta planilla.", f_nota,
          alinear=Alignment(vertical="top", wrap_text=True), borde=False)
    rs.merge_cells("J4:L5")
    celda(rs, "J6", "Requiere habilitar macros. Si no funciona: Archivo, Exportar, PDF, con todas las hojas menos "
                    "COSTOS seleccionadas.", f_nota, alinear=Alignment(vertical="top", wrap_text=True), borde=False)
    rs.merge_cells("J6:L9")
    for col in "JKL":
        rs.column_dimensions[col].width = 14

    # ---------------------------------------------------------------- COSTOS (uso interno)
    co = wb.create_sheet(HOJA_INTERNA)
    co.sheet_properties.tabColor = "C00000"
    encabezado(co, "COSTOS DE LA PROPUESTA (USO INTERNO, NO VA EN EL PDF)",
               "Celdas amarillas: código de inventario y costo unitario neto (sin IVA) por producto. Unidades y ventas "
               "vienen de las demás hojas.")
    cabecera(co, 5, 2, ["PRODUCTO", "CÓDIGO INVENTARIO", "COSTO UNITARIO NETO", "UNIDADES EN CANJE",
                        "UNIDADES VENDIDAS", "TOTAL UNIDADES", "COSTO DEL CANJE", "COSTO DE LO VENDIDO",
                        "COSTO TOTAL (INVENTARIO)", "VENTA NETA", "MARGEN DE LA VENTA", "MARGEN %"], alto=40)
    r = 6
    c0 = r
    for k, (nombre, *_x) in PRODUCTOS.items():
        fr = fila_producto[k]
        codigo, costo = previo["costos"].get(nombre, (None, None)) if previo else (None, None)
        celda(co, f"B{r}", nombre, alinear=izq)
        celda(co, f"C{r}", codigo, f_input, relleno=r_input, alinear=izq)
        celda(co, f"D{r}", costo, f_input, PESOS, r_input)
        canje = "+".join(f'SUMIFS({h}!$E:$E,{h}!$C:$C,"{nombre}",{h}!$H:$H,"SÍ")' for h in hojas_det)
        celda(co, f"E{r}", f"={canje}", formato=NUM)
        celda(co, f"F{r}", f"=G{r}-E{r}", formato=NUM)
        celda(co, f"G{r}", f"=RESUMEN!F{fr}", formato=NUM)
        celda(co, f"H{r}", f"=E{r}*N(D{r})", formato=PESOS)
        celda(co, f"I{r}", f"=F{r}*N(D{r})", formato=PESOS)
        celda(co, f"J{r}", f"=H{r}+I{r}", f_tot, PESOS)
        celda(co, f"K{r}", f"=ROUND(RESUMEN!H{fr}/(1+PRECIOS!$C$4),0)", formato=PESOS)
        celda(co, f"L{r}", f"=K{r}-I{r}", f_tot, PESOS)
        celda(co, f"M{r}", f'=IF(OR(K{r}=0,N(D{r})=0),"",L{r}/K{r})', formato=PCT)
        r += 1
    celda(co, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    for col in "CD":
        celda(co, f"{col}{r}", None, f_gran, relleno=r_gran)
    for col in "EFGHIJKL":
        celda(co, f"{col}{r}", f"=SUM({col}{c0}:{col}{r - 1})", f_gran, NUM if col in "EFG" else PESOS, r_gran)
    celda(co, f"M{r}", f'=IF(OR(K{r}=0,COUNT(D{c0}:D{r - 1})<ROWS(D{c0}:D{r - 1})),"",L{r}/K{r})', f_gran, PCT,
          r_gran)
    tc = r
    r += 3
    celda(co, f"B{r}", "RESULTADO DE LA PROPUESTA", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    for txt, f, fuente in [
        ("Valor del canje para el club (precio público, con IVA)", f"=RESUMEN!E{total_general}", f_norm),
        ("Costo real del canje para Playmaker (neto)", f"=H{tc}", f_norm),
        ("Venta al club y a formativas (neto, sin IVA)", f"=K{tc}", f_norm),
        ("Costo de lo vendido (neto)", f"=I{tc}", f_norm),
        ("Margen de la venta", f"=L{tc}", f_tot),
        ("Resultado (margen de la venta menos costo del canje)", f"=L{tc}-H{tc}", f_tot),
        ("Costo total de inventario a producir (canje y venta)", f"=J{tc}", f_tot),
    ]:
        celda(co, f"B{r}", txt, fuente, alinear=izq)
        for col in "CDEF":
            celda(co, f"{col}{r}", None)
        co.merge_cells(f"B{r}:F{r}")
        celda(co, f"G{r}", f, fuente, PESOS, r_sub if fuente is f_tot else None)
        r += 1
    co.conditional_formatting.add(f"G{r - 2}", CellIsRule(operator="lessThan", formula=["0"],
                                                          fill=PatternFill("solid", fgColor="F6D5D0")))
    celda(co, f"B{r + 1}", "Si falta el costo de un producto, sus costos quedan en cero: completa la columna COSTO "
                           "UNITARIO NETO para que el resultado sea real.", f_nota,
          alinear=Alignment(vertical="center"), borde=False)
    dvc = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                         errorTitle="Costo", error="Ingresa un costo en pesos (0 o más).")
    co.add_data_validation(dvc)
    dvc.add(f"D{c0}:D{tc - 1}")
    for col, ancho in zip("BCDEFGHIJKLM", (36, 15, 13, 12, 12, 12, 15, 15, 16, 15, 15, 10)):
        co.column_dimensions[col].width = ancho

    for k, ws in enumerate(wb.worksheets, start=1):
        ws.sheet_view.showGridLines = False
        ws.page_setup.orientation = "landscape"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
        ws.sheet_properties.codeName = f"Sheet{k}"  # nombres VBA de las hojas (como los asigna Excel)
    agregar_vba(wb, MACRO_PDF, EVENTO_VINCULO)
    wb.save(SALIDA)
    n = sum(f[3] for eq in equipos.values() for _, filas in eq for f in filas)
    print(f"OK  {SALIDA.name}  ({n} unidades solicitadas en {sum(len(f) for eq in equipos.values() for _, f in eq)} filas)")


if __name__ == "__main__":
    main()
