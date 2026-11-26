"""Propuesta comercial 2027 para Los Leones de Quilpué en Excel, con el formato de la valorización FEVOCHI.

Uso:
    python3 propuestas/leones-quilpue/generar_propuesta_excel.py

Lee la solicitud del club (Solicitud_indumentaria_CDC_Los_Leones_2027_v2.xlsx, hojas LNB y LNF, prendas por talla)
y los precios de lista del simulador interno (Canje_Leones_Quilpue_2027.xlsx, hoja Precios), y crea
Propuesta_Comercial_Los_Leones_2027.xlsm:
  - RESUMEN: por equipo y sección, canje (a precio público) y compras (a precio primer equipo o formativas) del 1°
    y del 2° semestre, total del convenio con neto e IVA, y valor por producto. Vínculo GENERAR PDF PARA EL CLUB (macro): exporta a PDF todas las hojas
    visibles menos COSTOS.
  - PRECIOS: tres precios por producto (con IVA): público (hinchas y tienda oficial), primer equipo (lo que LNB y
    LNF compren fuera del canje) y formativas. Los dos últimos salen del público con su descuento, terminados en 900.
  - LNB 2027 y LNF 2027: lo solicitado por el club (jugadores y cuerpo técnico), todo en canje, por sección y
    prenda: tallas, unidades, CANJE EN (1° o 2° semestre, a elegir por prenda) y valor del canje a precio público
    en cada semestre. La indumentaria de juego azul y negra viene en el 2° semestre.
  - FORMATIVAS 2027: compra de las series formativas a precio formativas, por rama (varones y damas) y categoría
    (Sub-11 a Sub-20): jugadores, producto (a elegir de la lista de precios) y unidades por jugador, con el mismo
    formato que la valorización FEVOCHI. Canje NO por defecto. La camiseta y el short de juego de las formativas
    son productos propios (con su precio), distintos de los del primer equipo.
  - COSTOS (uso interno): costo unitario y código de inventario por producto, costo del canje y de lo vendido,
    venta neta y resultado. No va en el PDF.
Si la planilla ya existe, se conservan los precios, descuentos, unidades, canje y costos cargados en ella.
"""

import sys
from pathlib import Path

import openpyxl
import openpyxl.utils
from openpyxl.drawing.image import Image as XLImage
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.hyperlink import Hyperlink

DIR = Path(__file__).parent
sys.path.insert(0, str(DIR))
sys.path.insert(0, str(DIR.parent))
from generar_propuesta import PRENDAS, SECCIONES, clave  # noqa: E402
from generar_propuesta import PRODUCTOS as PRODUCTOS_BASE  # noqa: E402
from vba_proyecto import agregar_vba  # noqa: E402

SOLICITUD = DIR / "Solicitud_indumentaria_CDC_Los_Leones_2027_v2.xlsx"
SIMULADOR = DIR / "Canje_Leones_Quilpue_2027.xlsx"
SALIDA = DIR / "Propuesta_Comercial_Los_Leones_2027.xlsm"
LOGO = DIR.parent / "_recursos" / "playmaker_logo_horizontal_navy.png"
IVA = 0.19
DESCUENTOS = {"primer": 0.20, "formativas": 0.10}  # descuento general sobre el precio público, por tipo de precio
HOJA_INTERNA = "COSTOS"
EQUIPOS = [("LNB", "LNB 2027", "Primer equipo masculino, Liga Nacional de Básquetbol"),
           ("LNF", "LNF 2027", "Primer equipo femenino, Liga Nacional Femenina")]
LINEAS = ["Juego", "Entrenamiento", "Presentación y viaje", "Socios e hinchas"]
RAMAS = ["Varones", "Damas"]
CATEGORIAS = ["Sub-11", "Sub-13", "Sub-14", "Sub-16", "Sub-18", "Sub-20"]
# prendas que trae cada categoría formativa (se pueden cambiar en la planilla) y filas libres para agregar otras
PRENDAS_FORMATIVAS = ["camiseta_juego_formativas", "short_juego_formativas", "calcetas", "polera_calentamiento", "poleron_buzo",
                      "pantalon_buzo"]
FILAS_LIBRES = 1

# La indumentaria de juego de las formativas es otro producto, con su propio precio: la del primer equipo se
# distingue en el nombre. Los nombres anteriores se traspasan al leer una planilla ya cargada.
NOMBRES_PRIMER_EQUIPO = {"camiseta_juego": "Camiseta de juego primer equipo",
                         "short_juego": "Short de juego primer equipo"}
JUEGO_FORMATIVAS = {  # clave: (nombre, línea, precio público por defecto, adicional, referencia)
    "camiseta_juego_formativas": ("Camiseta de juego formativas", "Juego", 20900, True,
                                  "Versión para series formativas, con su propio precio"),
    "short_juego_formativas": ("Short de juego formativas", "Juego", 18900, True,
                               "Versión para series formativas, con su propio precio"),
}
PRODUCTOS = {}
for _k, _v in PRODUCTOS_BASE.items():
    PRODUCTOS[_k] = (NOMBRES_PRIMER_EQUIPO.get(_k, _v[0]),) + tuple(_v[1:])
    if _k == "short_juego":
        PRODUCTOS.update(JUEGO_FORMATIVAS)
ALIAS = {PRODUCTOS_BASE[k][0]: n for k, n in NOMBRES_PRIMER_EQUIPO.items()}  # nombre anterior -> nombre nuevo
ALIAS_FORMATIVAS = {PRODUCTOS_BASE[k][0]: JUEGO_FORMATIVAS[k + "_formativas"][0] for k in NOMBRES_PRIMER_EQUIPO}
ETAPA_1, ETAPA_2 = "1° SEMESTRE", "2° SEMESTRE"
COLORES_2_SEMESTRE = ("azul", "negr")  # indumentaria de juego de estos colores: 2° semestre

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
        nombres = {v[0]: k for k, v in PRODUCTOS_BASE.items()}
        for r in range(5, pr.max_row + 1):
            n = texto(pr.cell(r, 1).value).replace(" (nueva)", "")
            if n in nombres and isinstance(pr.cell(r, 3).value, (int, float)):
                precios[nombres[n]] = pr.cell(r, 3).value
    return precios


def leer_previo():
    if not SALIDA.exists():
        return None
    wb = openpyxl.load_workbook(SALIDA)
    azul = lambda c: c.font is not None and c.font.color is not None and str(c.font.color.rgb)[-6:] == "0000FF"  # noqa: E731
    previo = {"precios": {}, "costos": {}, "celdas": {}}
    pr = wb["PRECIOS"]
    previo["iva"], previo["descuentos"] = pr["C4"].value, {}
    for r in range(5, 8):
        etq = texto(pr.cell(r, 2).value).lower()
        if "primer equipo" in etq:
            previo["descuentos"]["primer"] = pr.cell(r, 3).value
        elif "formativas" in etq or "club" in etq:  # el formato anterior tenía un solo descuento club
            previo["descuentos"]["formativas"] = pr.cell(r, 3).value
    cab = next(r for r in range(1, 15) if texto(pr.cell(r, 2).value) == "PRODUCTO")
    cols = {texto(pr.cell(cab, c).value).upper(): c for c in range(2, pr.max_column + 1)}
    col = lambda *claves: next((c for t, c in cols.items() if all(k in t for k in claves)), None)  # noqa: E731
    c_pub, c_obs = col("PRECIO PÚBLICO"), col("OBSERVACIONES")
    c_dpe, c_dfo = col("DESCUENTO", "PRIMER"), col("DESCUENTO", "FORMATIVAS") or col("DESCUENTO CLUB")
    for r in range(cab + 1, pr.max_row + 1):
        if pr.cell(r, 2).value and azul(pr.cell(r, c_pub)):
            v = lambda c: pr.cell(r, c).value if c else None  # noqa: E731
            n = texto(pr.cell(r, 2).value)
            previo["precios"][ALIAS.get(n, n)] = (v(c_pub), v(c_dpe), v(c_dfo), v(c_obs))
    if HOJA_INTERNA in wb.sheetnames:
        co = wb[HOJA_INTERNA]
        for r in range(1, co.max_row + 1):
            if co.cell(r, 2).value and azul(co.cell(r, 4)):
                n = texto(co.cell(r, 2).value)
                previo["costos"][ALIAS.get(n, n)] = (co.cell(r, 3).value, co.cell(r, 4).value)
    for hoja in [h for _, h, _ in EQUIPOS] + ["FORMATIVAS 2027"]:
        if hoja not in wb.sheetnames:
            continue
        ws = wb[hoja]
        cab = next((r for r in range(1, 15) if texto(ws.cell(r, 2).value) in ("PRENDA SOLICITADA", "CATEGORÍA")), None)
        if cab is None:
            continue
        nombres = {c: texto(ws.cell(cab, c).value) for c in range(2, ws.max_column + 1)}
        for row in ws.iter_rows(min_row=cab + 1):
            for c in row:
                if azul(c) and c.value is not None and nombres.get(c.column):
                    v = c.value
                    if nombres[c.column] == "ETAPA":  # nombre anterior de la columna CANJE EN
                        nombres[c.column] = "CANJE EN"
                    if nombres[c.column] == "PRODUCTO PLAYMAKER" and isinstance(v, str):
                        # en formativas, la indumentaria de juego pasa a su versión formativa
                        v = ALIAS_FORMATIVAS.get(v, v) if hoja == "FORMATIVAS 2027" else ALIAS.get(v, v)
                    previo["celdas"][(hoja, c.row, nombres[c.column])] = v
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

    cabeceras = {}  # hoja -> {columna: texto de la cabecera de su tabla}

    def entrada(ws, ref, valor, formato=None, alinear=centro):
        c = ws[ref]
        nombre = cabeceras.get(ws.title, {}).get(c.column_letter)
        v = previo["celdas"].get((ws.title, c.row, nombre), valor) if previo and nombre else valor
        return celda(ws, ref, v, f_input, formato, r_input, alinear)

    def cabecera(ws, fila, col0, textos, alto=34):
        cabeceras.setdefault(ws.title, {k: v for k, v in
                                        ((openpyxl.utils.get_column_letter(col0 + i), t) for i, t in enumerate(textos))})
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
    encabezado(pr, "PRECIOS POR PRODUCTO 2027", "Tres precios con IVA: público (hinchas y tienda oficial), primer equipo "
                                                "(compras de LNB y LNF fuera del canje) y formativas. Los dos últimos se "
                                                "calculan con su descuento y terminan en 900.")
    celda(pr, "B4", "IVA", f_tot, alinear=izq)
    celda(pr, "C4", previo["iva"] if previo and previo.get("iva") is not None else IVA, f_input, "0%", r_input)
    prev_d = previo.get("descuentos", {}) if previo else {}
    for fila, clave_d, txt in ((5, "primer", "Descuento general primer equipo"),
                               (6, "formativas", "Descuento general formativas")):
        celda(pr, f"B{fila}", txt, f_tot, alinear=izq)
        v = prev_d.get(clave_d)
        celda(pr, f"C{fila}", v if v is not None else DESCUENTOS[clave_d], f_input, "0%", r_input)
    celda(pr, "D5", "Se aplica a los productos que no tienen un descuento propio en su columna de descuento.", f_nota,
          alinear=Alignment(vertical="center"), borde=False)
    cabecera(pr, 8, 2, ["PRODUCTO", "PRECIO PÚBLICO (HINCHAS Y TIENDA)", "DESCUENTO PRIMER EQUIPO",
                        "PRECIO PRIMER EQUIPO", "DESCUENTO FORMATIVAS", "PRECIO FORMATIVAS", "OBSERVACIONES"], alto=40)
    PRIMERA_PRECIO = 9
    fila_precio, r = {}, PRIMERA_PRECIO

    def con_descuento(fila, col_desc, celda_general):
        # precio con descuento, llevado al valor terminado en 900 más cercano (como los precios de lista); con un
        # descuento de 100% (o un precio que quede bajo $500) el precio es 0, nunca negativo
        neto = f'N(C{fila})*(1-IF({col_desc}{fila}="",{celda_general},{col_desc}{fila}))'
        return f"=IF({neto}<=0,0,MAX(0,ROUND(({neto}-900)/1000,0)*1000+900))"

    for linea in LINEAS:
        celda(pr, f"B{r}", linea.upper(), Font(name="Calibri", size=10, bold=True, color=NAVY), relleno=r_sub,
              alinear=izq)
        for col in "CDEFGH":
            celda(pr, f"{col}{r}", None, relleno=r_sub)
        r += 1
        for k, (nombre, l, _p, _a, _ref) in PRODUCTOS.items():
            if l != linea:
                continue
            fila_precio[k] = r
            publico, d_pe, d_fo, obs = (previo["precios"].get(nombre, (None,) * 4) if previo else (None,) * 4)
            celda(pr, f"B{r}", nombre, alinear=izq)
            celda(pr, f"C{r}", publico if publico is not None else lista[k], f_input, PESOS, r_input)
            celda(pr, f"D{r}", d_pe, f_input, "0%", r_input)
            celda(pr, f"E{r}", con_descuento(r, "D", "$C$5"), f_tot, PESOS)
            celda(pr, f"F{r}", d_fo, f_input, "0%", r_input)
            celda(pr, f"G{r}", con_descuento(r, "F", "$C$6"), f_tot, PESOS)
            if obs is None and k in JUEGO_FORMATIVAS:
                obs = JUEGO_FORMATIVAS[k][4]
            celda(pr, f"H{r}", obs, f_input, relleno=r_input, alinear=izq)
            r += 1
    ultima_precio = r - 1
    for col, ancho in zip("BCDEFGH", (38, 17, 13, 14, 13, 14, 36)):
        pr.column_dimensions[col].width = ancho
    dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                        errorTitle="Precio", error="Ingresa un precio en pesos (0 o más).")
    pr.add_data_validation(dv)
    dv.add(f"C{PRIMERA_PRECIO}:C{ultima_precio}")
    dvp = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True,
                         errorTitle="Descuento", error="Ingresa un porcentaje entre 0% y 100%.")
    pr.add_data_validation(dvp)
    dvp.add("C5:C6")
    dvp.add(f"D{PRIMERA_PRECIO}:D{ultima_precio}")
    dvp.add(f"F{PRIMERA_PRECIO}:F{ultima_precio}")

    def precio_de(k, col="E"):  # C: público; E: primer equipo; G: formativas
        return f"PRECIOS!${col}${fila_precio[k]}"

    # ---------------------------------------------------------------- LNB 2027 y LNF 2027
    detalle = {}  # hoja -> (secciones [(sección, primera fila, fila subtotal)], fila total)
    for equipo, hoja, descripcion in EQUIPOS:
        ws = wb.create_sheet(hoja)
        encabezado(ws, f"{hoja}: INDUMENTARIA SOLICITADA POR EL CLUB (CANJE)",
                   f"{descripcion}, jugadores y cuerpo técnico. Todo va en canje (100% de descuento). En CANJE EN se "
                   "elige el semestre de cada prenda. Celdas amarillas editables.")
        cabecera(ws, 5, 2, ["PRENDA SOLICITADA", "PRODUCTO PLAYMAKER", "TALLAS", "UNIDADES", "CANJE EN",
                            "PRECIO PÚBLICO", "VALOR CANJE 1° SEMESTRE", "VALOR CANJE 2° SEMESTRE"])
        dv_etapa = DataValidation(type="list", formula1=f'"{ETAPA_1},{ETAPA_2}"', allow_blank=False,
                                  errorTitle="Canje en", error=f"Elige {ETAPA_1} o {ETAPA_2}.")
        dv_u = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                              errorTitle="Unidades", error="Ingresa un número entero (0 o más).")
        r, secs = 6, []
        for seccion, filas in equipos[equipo]:
            celda(ws, f"B{r}", seccion.upper(), f_sub, alinear=izq, borde=False)
            r += 1
            f0 = r
            for prenda, k, tallas, n in filas:
                de_juego = "juego" in seccion.lower()
                etapa = ETAPA_2 if de_juego and any(c in prenda.lower() for c in COLORES_2_SEMESTRE) else ETAPA_1
                celda(ws, f"B{r}", prenda, alinear=izq)
                celda(ws, f"C{r}", nombre_producto(k), f_gris, alinear=izq)
                celda(ws, f"D{r}", tallas, f_gris, alinear=izq)
                entrada(ws, f"E{r}", n, NUM)
                entrada(ws, f"F{r}", etapa)
                celda(ws, f"G{r}", "=" + precio_de(k, "C"), f_gris, PESOS)
                celda(ws, f"H{r}", f'=IF(F{r}="{ETAPA_2}",0,E{r}*G{r})', f_tot, PESOS)
                celda(ws, f"I{r}", f'=IF(F{r}="{ETAPA_2}",E{r}*G{r},0)', f_tot, PESOS)
                r += 1
            dv_etapa.add(f"F{f0}:F{r - 1}")
            dv_u.add(f"E{f0}:E{r - 1}")
            ws.conditional_formatting.add(f"F{f0}:F{r - 1}", FormulaRule(
                formula=[f'$F{f0}="{ETAPA_2}"'], font=Font(color="7030A0", bold=True),
                fill=PatternFill("solid", fgColor="E4DFEC")))
            fe, ee = f"F{f0}:F{r - 1}", f"E{f0}:E{r - 1}"
            celda(ws, f"B{r}", f"Total {seccion.split(': ')[-1]}", f_tot, relleno=r_sub, alinear=izq)
            for col in "CFG":
                celda(ws, f"{col}{r}", None, relleno=r_sub)
            celda(ws, f"D{r}", f'=IF(COUNTIF({fe},"{ETAPA_2}")=0,"",SUMIF({fe},"<>{ETAPA_2}",{ee})&" en 1° semestre y "'
                               f'&SUMIF({fe},"{ETAPA_2}",{ee})&" en 2° semestre")', f_gris, relleno=r_sub, alinear=izq)
            celda(ws, f"E{r}", f"=SUM({ee})", f_tot, NUM, r_sub)
            celda(ws, f"H{r}", f"=SUM(H{f0}:H{r - 1})", f_tot, PESOS, r_sub)
            celda(ws, f"I{r}", f"=SUM(I{f0}:I{r - 1})", f_tot, PESOS, r_sub)
            secs.append((seccion, f0, r))
            r += 2
        celda(ws, f"B{r}", "TOTAL CANJE", f_gran, relleno=r_gran, alinear=izq)
        for col in "CDEFGHI":
            celda(ws, f"{col}{r}", None, f_gran, relleno=r_gran)
        for col, fmt in (("E", NUM), ("H", PESOS), ("I", PESOS)):
            celda(ws, f"{col}{r}", "=" + "+".join(f"{col}{s_}" for _, _, s_ in secs), f_gran, fmt, r_gran)
        primero = "+".join(f'SUMIF(F{f0}:F{s_ - 1},"<>{ETAPA_2}",E{f0}:E{s_ - 1})' for _, f0, s_ in secs)
        segundo = "+".join(f'SUMIF(F{f0}:F{s_ - 1},"{ETAPA_2}",E{f0}:E{s_ - 1})' for _, f0, s_ in secs)
        celda(ws, f"D{r}", f'=({primero})&" en 1° semestre y "&({segundo})&" en 2° semestre"',
              Font(name="Calibri", size=10, color="FFFFFF"), relleno=r_gran, alinear=izq)
        ws.row_dimensions[r].height = 20
        ws.add_data_validation(dv_etapa)
        ws.add_data_validation(dv_u)
        for col, ancho in zip("BCDEFGHI", (42, 30, 30, 11, 14, 14, 16, 16)):
            ws.column_dimensions[col].width = ancho
        ws.freeze_panes = "B6"
        detalle[hoja] = (secs, r)

    # ---------------------------------------------------------------- FORMATIVAS 2027
    fo = wb.create_sheet("FORMATIVAS 2027")
    encabezado(fo, "SERIES FORMATIVAS 2027: COMPRA A PRECIO FORMATIVAS POR CATEGORÍA",
               "Celdas amarillas: jugadores, producto (lista desplegable) y unidades por jugador. El precio viene de la "
               "hoja PRECIOS. CANJE SÍ = 100% de descuento en esa prenda.")
    cabecera(fo, 5, 2, ["CATEGORÍA", "PRODUCTO PLAYMAKER", "JUGADORES", "UNIDADES POR JUGADOR", "TOTAL UNIDADES",
                        "PRECIO PÚBLICO", "PRECIO FORMATIVAS", "CANJE", "VALOR A PAGAR"])
    rango_nombres = f"PRECIOS!$B${PRIMERA_PRECIO}:$B${ultima_precio}"
    dv_prod = DataValidation(type="list", formula1=f"={rango_nombres}", allow_blank=True, errorTitle="Producto",
                             error="Elige un producto de la hoja PRECIOS.")
    dv_canje_f = DataValidation(type="list", formula1='"SÍ,NO"', allow_blank=True, errorTitle="Canje",
                                error="Elige SÍ (canje, 100% de descuento) o NO.")
    dv_f = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                          errorTitle="Cantidad", error="Ingresa un número entero (0 o más).")

    def precio_por_nombre(ref, col):
        return (f"IFERROR(N(INDEX(PRECIOS!${col}${PRIMERA_PRECIO}:${col}${ultima_precio},"
                f"MATCH({ref},{rango_nombres},0))),0)")

    r = 6
    formativas = []  # (rama, [(categoría, primera fila, fila subtotal)], fila total rama)
    for rama in RAMAS:
        celda(fo, f"B{r}", f"FORMATIVAS {rama.upper()}", f_sec, alinear=Alignment(vertical="center"), borde=False)
        fo.row_dimensions[r].height = 20
        r += 1
        cats = []
        for cat in CATEGORIAS:
            f0 = r
            productos = [nombre_producto(k) for k in PRENDAS_FORMATIVAS] + [None] * FILAS_LIBRES
            for k, prod in enumerate(productos):
                if k == 0:
                    celda(fo, f"B{r}", cat, f_tot)
                    entrada(fo, f"D{r}", None, NUM)
                else:
                    celda(fo, f"B{r}", None)
                    celda(fo, f"D{r}", f"=N(D{f0})", f_gris, NUM)
                entrada(fo, f"C{r}", prod, alinear=izq)
                entrada(fo, f"E{r}", 1 if prod else None, NUM)
                celda(fo, f"F{r}", f"=N(D{r})*N(E{r})", formato=NUM)
                celda(fo, f"G{r}", "=" + precio_por_nombre(f"C{r}", "C"), f_gris, PESOS)
                celda(fo, f"H{r}", "=" + precio_por_nombre(f"C{r}", "G"), formato=PESOS)
                entrada(fo, f"I{r}", "NO")
                celda(fo, f"J{r}", f'=IF(I{r}="SÍ",0,F{r}*H{r})', f_tot, PESOS)
                r += 1
            dv_prod.add(f"C{f0}:C{r - 1}")
            dv_canje_f.add(f"I{f0}:I{r - 1}")
            dv_f.add(f"D{f0}")
            dv_f.add(f"E{f0}:E{r - 1}")
            celda(fo, f"B{r}", f"Total {cat}", f_tot, relleno=r_sub, alinear=izq)
            for col in "CEGHI":
                celda(fo, f"{col}{r}", None, relleno=r_sub)
            celda(fo, f"D{r}", f"=N(D{f0})", f_tot, NUM, r_sub)
            celda(fo, f"F{r}", f"=SUM(F{f0}:F{r - 1})", f_tot, NUM, r_sub)
            celda(fo, f"J{r}", f"=SUM(J{f0}:J{r - 1})", f_tot, PESOS, r_sub)
            cats.append((cat, f0, r))
            r += 1
        celda(fo, f"B{r}", f"TOTAL {rama.upper()}", f_gran, relleno=r_gran, alinear=izq)
        for col in "CDEFGHIJ":
            celda(fo, f"{col}{r}", None, f_gran, relleno=r_gran)
        for col, fmt in (("D", NUM), ("F", NUM), ("J", PESOS)):
            celda(fo, f"{col}{r}", "=" + "+".join(f"{col}{s_}" for _, _, s_ in cats), f_gran, fmt, r_gran)
        fo.row_dimensions[r].height = 20
        formativas.append((rama, cats, r))
        r += 3
    for dv_ in (dv_prod, dv_canje_f, dv_f):
        fo.add_data_validation(dv_)
    for col, ancho in zip("BCDEFGHIJ", (16, 36, 12, 13, 12, 13, 13, 9, 15)):
        fo.column_dimensions[col].width = ancho
    fo.freeze_panes = "B6"

    # ---------------------------------------------------------------- RESUMEN
    rs = wb.create_sheet("RESUMEN", 0)
    encabezado(rs, "PROPUESTA COMERCIAL 2027: CLUB DEPORTIVO COLEGIO LOS LEONES DE QUILPUÉ",
               "Valores con IVA. LNB, LNF y cuerpo técnico: todo en canje, valorizado a precio público, en el semestre "
               "elegido. Formativas: compras a precio formativas.")
    rs.merge_cells("D4:F4")
    rs.merge_cells("G4:I4")
    rs.merge_cells("J4:M4")
    for c0, c1, txt, fondo in (("D", "F", "1° SEMESTRE", "2F5597"), ("G", "I", "2° SEMESTRE", "7030A0"),
                               ("J", "M", "TOTAL CONVENIO", NAVY)):
        celda(rs, f"{c0}4", txt, Font(name="Calibri", size=10, bold=True, color="FFFFFF"),
              relleno=PatternFill("solid", fgColor=fondo))
    cabecera(rs, 5, 2, ["EQUIPO", "SECCIÓN", "UNIDADES", "CANJE (PRECIO PÚBLICO)", "COMPRAS", "UNIDADES",
                        "CANJE (PRECIO PÚBLICO)", "COMPRAS", "CANJE TOTAL", "COMPRAS TOTAL", "NETO COMPRAS",
                        "IVA COMPRAS"], alto=36)
    r, filas_total = 6, []

    def fila_resumen(r, equipo, seccion, u1, c1, p1, u2=0, c2=0, p2=0, fuente=f_norm, relleno=None):
        celda(rs, f"B{r}", equipo, fuente, relleno=relleno, alinear=izq)
        celda(rs, f"C{r}", seccion, fuente, relleno=relleno, alinear=izq)
        for col, v, fmt in (("D", u1, NUM), ("E", c1, PESOS), ("F", p1, PESOS), ("G", u2, NUM), ("H", c2, PESOS),
                            ("I", p2, PESOS)):
            celda(rs, f"{col}{r}", v, fuente, fmt, relleno)
        celda(rs, f"J{r}", f"=E{r}+H{r}", fuente if relleno else f_tot, PESOS, relleno)
        celda(rs, f"K{r}", f"=F{r}+I{r}", fuente if relleno else f_tot, PESOS, relleno)
        celda(rs, f"L{r}", f"=ROUND(K{r}/(1+PRECIOS!$C$4),0)", fuente, PESOS, relleno)
        celda(rs, f"M{r}", f"=K{r}-L{r}", fuente, PESOS, relleno)

    for equipo, hoja, descripcion in EQUIPOS:
        secs, _tot = detalle[hoja]
        H = f"'{hoja}'"
        r0 = r
        for k, (seccion, f0, s) in enumerate(secs):
            e, et = (f"{H}!{c}{f0}:{c}{s - 1}" for c in "EF")
            fila_resumen(r, f"{equipo} (primer equipo)" if k == 0 else None, seccion,
                         f'=SUMIF({et},"<>{ETAPA_2}",{e})', f"={H}!H{s}", 0,
                         f'=SUMIF({et},"{ETAPA_2}",{e})', f"={H}!I{s}", 0)
            r += 1
        fila_resumen(r, f"Total {equipo}", None, *[f"=SUM({c}{r0}:{c}{r - 1})" for c in "DEFGHI"], fuente=f_tot,
                     relleno=r_sub)
        filas_total.append(r)
        r += 1
    F = "'FORMATIVAS 2027'"
    for rama, cats, ft in formativas:
        r0 = r
        for k, (cat, f0, s_) in enumerate(cats):
            fu, gp, ic = (f"{F}!{c}{f0}:{c}{s_ - 1}" for c in "FGI")
            fila_resumen(r, f"Formativas {rama.lower()}" if k == 0 else None, cat, f"={F}!F{s_}",
                         f'=SUMPRODUCT(({ic}="SÍ")*{fu}*{gp})', f"={F}!J{s_}")
            r += 1
        fila_resumen(r, f"Total formativas {rama.lower()}", None, *[f"=SUM({c}{r0}:{c}{r - 1})" for c in "DEFGHI"],
                     fuente=f_tot, relleno=r_sub)
        filas_total.append(r)
        r += 1
    fila_resumen(r, "TOTAL CONVENIO", None, *["=" + "+".join(f"{c}{x}" for x in filas_total) for c in "DEFGHI"],
                 fuente=f_gran, relleno=r_gran)
    rs.row_dimensions[r].height = 22
    total_general = r
    celda(rs, f"B{r + 1}", "Las formativas se cuentan en el 1° semestre.", f_nota, alinear=Alignment(vertical="center"),
          borde=False)

    r += 4
    celda(rs, f"B{r}", "VALOR POR PRODUCTO (TOTAL CONVENIO)", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    cabecera(rs, r, 2, ["PRODUCTO", "PRECIO PÚBLICO (HINCHAS)", "PRECIO PRIMER EQUIPO", "PRECIO FORMATIVAS",
                        "TOTAL UNIDADES", "CANJE 1° SEMESTRE", "CANJE 2° SEMESTRE", "CANJE TOTAL",
                        "COMPRAS TOTAL"], alto=40)
    r += 1
    p0 = r
    hojas_det = [f"'{h}'" for _, h, _ in EQUIPOS]
    fila_producto = {}
    for k, (nombre, *_x) in PRODUCTOS.items():
        fp = fila_precio[k]
        fila_producto[k] = r
        celda(rs, f"B{r}", nombre, alinear=izq)
        celda(rs, f"C{r}", f"=PRECIOS!C{fp}", f_gris, PESOS)
        celda(rs, f"D{r}", f"=PRECIOS!E{fp}", formato=PESOS)
        celda(rs, f"E{r}", f"=PRECIOS!G{fp}", formato=PESOS)
        unid = "+".join(f'SUMIF({h}!$C:$C,"{nombre}",{h}!$E:$E)' for h in hojas_det)
        celda(rs, f"F{r}", f'={unid}+SUMIF({F}!$C:$C,"{nombre}",{F}!$F:$F)', formato=NUM)
        c1 = "+".join(f'SUMIFS({h}!$E:$E,{h}!$C:$C,"{nombre}",{h}!$F:$F,"<>{ETAPA_2}")' for h in hojas_det)
        celda(rs, f"G{r}", f'=({c1}+SUMIFS({F}!$F:$F,{F}!$C:$C,"{nombre}",{F}!$I:$I,"SÍ"))*C{r}', formato=PESOS)
        c2 = "+".join(f'SUMIFS({h}!$E:$E,{h}!$C:$C,"{nombre}",{h}!$F:$F,"{ETAPA_2}")' for h in hojas_det)
        celda(rs, f"H{r}", f"=({c2})*C{r}", formato=PESOS)
        celda(rs, f"I{r}", f"=G{r}+H{r}", f_tot, PESOS)
        celda(rs, f"J{r}", f'=SUMIF({F}!$C:$C,"{nombre}",{F}!$J:$J)', f_tot, PESOS)  # compras: formativas
        r += 1
    celda(rs, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    for col in "CDE":
        celda(rs, f"{col}{r}", None, f_gran, relleno=r_gran)
    for col, fmt in (("F", NUM), ("G", PESOS), ("H", PESOS), ("I", PESOS), ("J", PESOS)):
        celda(rs, f"{col}{r}", f"=SUM({col}{p0}:{col}{r - 1})", f_gran, fmt, r_gran)
    tg = total_general
    celda(rs, f"B{r + 1}", f'=IF(AND(G{r}=E{tg},H{r}=H{tg},J{r}=K{tg},F{r}=D{tg}+G{tg}),"Control: la suma por '
                           f'producto coincide con el total del convenio.","Revisar: la suma por producto no coincide '
                           f'con el total del convenio.")', f_nota, alinear=Alignment(vertical="center"), borde=False)
    for col, ancho in zip("BCDEFGHIJKLM", (30, 34, 11, 15, 14, 11, 15, 14, 15, 15, 14, 13)):
        rs.column_dimensions[col].width = ancho
    rs.print_area = f"A1:M{r + 1}"

    # vínculo que genera el PDF para el club (macro GenerarPDFClub vía Workbook_SheetFollowHyperlink)
    celda(rs, "O2", "GENERAR PDF PARA EL CLUB", Font(name="Calibri", size=11, bold=True, color="FFFFFF",
                                                       underline="single"), relleno=r_gran)
    for col in "OPQ":
        for fila in (2, 3):
            rs[f"{col}{fila}"].fill = r_gran
    rs.merge_cells("O2:Q3")
    rs["O2"].hyperlink = Hyperlink(ref="O2", location="RESUMEN!O2",
                                   tooltip="Generar PDF para el club (todas las hojas menos COSTOS)")
    celda(rs, "O4", "Exporta todas las hojas menos COSTOS a un PDF en la misma carpeta de esta planilla.", f_nota,
          alinear=Alignment(vertical="top", wrap_text=True), borde=False)
    rs.merge_cells("O4:Q5")
    celda(rs, "O6", "Requiere habilitar macros. Si no funciona: Archivo, Exportar, PDF, con todas las hojas menos "
                    "COSTOS seleccionadas.", f_nota, alinear=Alignment(vertical="top", wrap_text=True), borde=False)
    rs.merge_cells("O6:Q9")
    for col in "OPQ":
        rs.column_dimensions[col].width = 14

    # ---------------------------------------------------------------- COSTOS (uso interno)
    co = wb.create_sheet(HOJA_INTERNA)
    co.sheet_properties.tabColor = "C00000"
    encabezado(co, "COSTOS DEL CONVENIO, 1° Y 2° SEMESTRE (USO INTERNO, NO VA EN EL PDF)",
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
        canje = "+".join(f'SUMIF({h}!$C:$C,"{nombre}",{h}!$E:$E)' for h in hojas_det)  # LNB y LNF: todo canje
        celda(co, f"E{r}", f'={canje}+SUMIFS({F}!$F:$F,{F}!$C:$C,"{nombre}",{F}!$I:$I,"SÍ")', formato=NUM)
        celda(co, f"F{r}", f"=G{r}-E{r}", formato=NUM)
        celda(co, f"G{r}", f"=RESUMEN!F{fr}", formato=NUM)
        celda(co, f"H{r}", f"=E{r}*N(D{r})", formato=PESOS)
        celda(co, f"I{r}", f"=F{r}*N(D{r})", formato=PESOS)
        celda(co, f"J{r}", f"=H{r}+I{r}", f_tot, PESOS)
        celda(co, f"K{r}", f"=ROUND(RESUMEN!J{fr}/(1+PRECIOS!$C$4),0)", formato=PESOS)
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
        ("Valor del canje del convenio para el club (precio público, con IVA)", f"=RESUMEN!J{total_general}", f_norm),
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
