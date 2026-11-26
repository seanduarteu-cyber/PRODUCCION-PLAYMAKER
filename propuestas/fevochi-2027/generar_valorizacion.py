"""Valorización de la ropa de las selecciones de vóleibol (FEVOCHI) 2027, a partir de la proyección del cliente.

Uso:
    python3 propuestas/fevochi-2027/generar_valorizacion.py

Lee Proyeccion_Ropa_Selecciones_FEVOCHI_2027_original.xlsx (hojas SELECCIONES ROPA 2027 y CUERPO TÉCNICO 2027:
jugadores por categoría y prendas por jugador, con colores escritos junto a la cantidad, p. ej. "2 roja-azul")
y crea Valorizacion_Ropa_Selecciones_FEVOCHI_2027.xlsm (con macros):
  - RESUMEN: por selección y categoría, valor total del canje (a precio público general) y valor a precio
    federación de lo que se paga (con neto e IVA), y lo mismo por prenda.
  - SELECCIONES ROPA 2027 y CUERPO TÉCNICO 2027: una fila por categoría y prenda: unidades por jugador, total de
    unidades, precio público (valoriza el canje), precio federación, canje (SÍ: 100% de descuento en esa prenda; viene
    marcado en los equipos adultos de todas las selecciones) y valor a pagar.
  - PRECIOS: por prenda, precio público general, descuento y precio federación (todos con IVA). El descuento
    general se aplica a las prendas sin descuento propio.
  - RESUMEN NEGOCIO (uso interno): por selección y cuerpo técnico, venta neta, costo de lo vendido y margen, canje
    (a precio público y a costo) y margen total del negocio, con un supuesto de otros costos (% de la venta) y el
    punto de equilibrio. No va en el PDF de la federación.
  - COSTOS (uso interno): costo unitario y código de inventario por prenda, costo del canje y de lo vendido, venta
    neta y resultado del convenio. No va en el PDF de la federación.
En RESUMEN, el vínculo GENERAR PDF PARA LA FEDERACIÓN corre la macro GenerarPDFFederacion: exporta a PDF todas las
hojas visibles menos COSTOS y RESUMEN NEGOCIO, en la misma carpeta de la planilla (requiere habilitar macros).
Si la planilla de valorización ya existe, se conservan los precios, costos, jugadores y unidades que tenga cargados,
y las celdas que el usuario haya agregado debajo o a la derecha de las tablas.
"""

import re
import sys
from pathlib import Path

import openpyxl
from openpyxl.drawing.image import Image as XLImage
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.hyperlink import Hyperlink

sys.path.insert(0, str(Path(__file__).parent.parent))
from vba_proyecto import agregar_vba  # noqa: E402

DIR = Path(__file__).parent
ORIGEN = DIR / "Proyeccion_Ropa_Selecciones_FEVOCHI_2027_original.xlsx"
SALIDA = DIR / "Valorizacion_Ropa_Selecciones_FEVOCHI_2027.xlsm"
ANTERIOR = DIR / "Valorizacion_Ropa_Selecciones_FEVOCHI_2027.xlsx"  # versión sin macros, solo para traspasar valores
HOJA_INTERNA = "COSTOS"
HOJA_NEGOCIO = "RESUMEN NEGOCIO"  # uso interno, no va en el PDF
MACRO_PDF = """' Genera el PDF para la federacion: todas las hojas visibles menos las internas (COSTOS y
' RESUMEN NEGOCIO).
Sub GenerarPDFFederacion()
    Dim hojas() As Variant, n As Integer, ws As Worksheet, ruta As String, activa As Worksheet
    Set activa = ActiveSheet
    For Each ws In ThisWorkbook.Worksheets
        If ws.Name <> "COSTOS" And InStr(1, ws.Name, "NEGOCIO", vbTextCompare) = 0 And ws.Visible = xlSheetVisible Then
            n = n + 1
            ReDim Preserve hojas(1 To n)
            hojas(n) = ws.Name
        End If
    Next ws
    ruta = ThisWorkbook.Path & Application.PathSeparator & "Valorizacion_FEVOCHI_2027_Federacion.pdf"
    ThisWorkbook.Worksheets(hojas).Select
    ActiveSheet.ExportAsFixedFormat Type:=xlTypePDF, Filename:=ruta, Quality:=xlQualityStandard, _
        IncludeDocProperties:=True, IgnorePrintAreas:=False, OpenAfterPublish:=True
    activa.Select
    MsgBox "PDF guardado en: " & ruta, vbInformation, "PDF para la federacion"
End Sub
"""
EVENTO_VINCULO = """' El vinculo GENERAR PDF de la hoja RESUMEN (su texto de ayuda dice PDF) corre la macro.
Private Sub Workbook_SheetFollowHyperlink(ByVal Sh As Object, ByVal Target As Hyperlink)
    If InStr(1, Target.ScreenTip, "PDF", vbTextCompare) > 0 Then GenerarPDFFederacion
End Sub
"""
IVA = 0.19

# prendas con precio propio, por grupo (el nombre es la llave entre hojas: no cambiarlo en una sola parte)
PRENDAS = [
    ("LÍNEA DE JUEGO PISO", ["Camiseta de juego piso", "Short de juego piso", "Calza de juego piso"]),
    ("LÍNEA DE JUEGO PLAYA", ["Camiseta de juego playa", "Short de juego playa", "Bikini de juego playa"]),
    ("ENTRENAMIENTO Y PRESENTACIÓN", ["Buzo completo (polerón y pantalón)", "Polera de entrenamiento",
                                      "Polera de presentación", "Short de presentación",
                                      "Short o calza de presentación"]),
]
# columna de la proyección del cliente -> prenda, según el encabezado y el tipo de selección
def prenda_de(encabezado, playa):
    e = encabezado.upper()
    if "CAMISETA" in e:
        return "Camiseta de juego playa" if playa else "Camiseta de juego piso"
    if "CALZA" in e and "SHORT" in e:
        return "Short o calza de presentación"
    if "CALZA" in e:
        return "Calza de juego piso"
    if "BIKINI" in e:
        return "Bikini de juego playa"
    if "SHORT" in e and "PRESENTACI" in e:
        return "Short de presentación"
    if "SHORT" in e:
        return "Short de juego playa" if playa else "Short de juego piso"
    if "BUZO" in e:
        return "Buzo completo (polerón y pantalón)"
    if "ENTRENAMIENTO" in e:
        return "Polera de entrenamiento"
    if "PRESENTACI" in e:
        return "Polera de presentación"
    raise SystemExit(f"Prenda sin precio definido: {encabezado}")


def unidades_y_colores(valor):
    """'2 roja-azul' -> (2, 'Rojo y azul'); '2 azul-1 rojo' -> (3, '2 azul y 1 rojo'); 2 -> (2, '')."""
    if isinstance(valor, (int, float)):
        return int(valor), ""
    partes = [p.strip() for p in str(valor).split("-") if p.strip()]
    con_numero = [re.match(r"(\d+)\s*(.*)", p) for p in partes]
    genero = {"roja": "rojo", "blanca": "blanco", "negra": "negro"}
    if sum(1 for m in con_numero if m) > 1:  # cantidades por color
        items = [(int(m.group(1)), genero.get(m.group(2).lower(), m.group(2).lower())) for m in con_numero if m]
        return sum(n for n, _ in items), lista([f"{n} {c}" for n, c in items])
    m = con_numero[0]
    if not m:
        raise SystemExit(f"Cantidad sin número: {valor}")
    colores = [m.group(2)] + partes[1:]
    colores = [genero.get(c.lower(), c.lower()) for c in colores if c]
    if colores and len(colores) != int(m.group(1)):
        raise SystemExit(f"La cantidad no calza con los colores: {valor}")
    return int(m.group(1)), lista(colores).capitalize()


def lista(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " y " + xs[-1]


def texto(v):
    return " ".join(str(v or "").split())


def leer_proyeccion():
    wb = openpyxl.load_workbook(ORIGEN)
    selecciones = []  # (título, [(categoría, jugadores, [(prenda, unidades, colores)])])
    ws = wb["SELECCIONES ROPA 2027"]
    r = 1
    while r <= ws.max_row:
        b = texto(ws.cell(r, 2).value)
        if b.upper().startswith("SELECCIÓN"):
            playa = "PLAYA" in b.upper()
            cab = [texto(ws.cell(r + 1, c).value) for c in range(4, 9)]
            prendas = [prenda_de(h, playa) for h in cab]
            cats, f = [], r + 2
            while f <= ws.max_row and ws.cell(f, 2).value:
                items = [(p, *unidades_y_colores(ws.cell(f, 4 + k).value)) for k, p in enumerate(prendas)]
                cats.append((texto(ws.cell(f, 2).value), ws.cell(f, 3).value, items))
                f += 1
            selecciones.append((b, cats))
            r = f
        r += 1
    tecnicos = []  # (título, personas, [(prenda, unidades)])
    ws = wb["CUERPO TÉCNICO 2027"]
    for r in range(1, ws.max_row + 1):
        b = texto(ws.cell(r, 2).value)
        m = re.match(r"(CUERPO TÉCNICO.*?)\s*\(\s*(\d+)\s*PERSONAS\s*\)", b.upper())
        if m:
            titulo = re.sub(r"\s*\(.*", "", b).strip()
            items, f = [], r + 2
            while f <= ws.max_row and ws.cell(f, 2).value:
                items.append((prenda_de(texto(ws.cell(f, 2).value), "PLAYA" in b.upper()), int(ws.cell(f, 3).value)))
                f += 1
            tecnicos.append((titulo, int(m.group(2)), items))
    return selecciones, tecnicos


def leer_previo():
    """Valores ya cargados en la valorización (precios, jugadores, unidades), para no perderlos."""
    origen = SALIDA if SALIDA.exists() else ANTERIOR
    if not origen.exists():
        return None
    wb = openpyxl.load_workbook(origen)
    previo = {"precios": {}, "iva": None, "descuento": None, "celdas": {}, "costos": {}, "supuestos": {}, "extras": {}}
    if HOJA_INTERNA in wb.sheetnames:
        co = wb[HOJA_INTERNA]
        for r in range(1, co.max_row + 1):
            if co.cell(r, 2).value and co.cell(r, 4).font.color is not None and str(co.cell(r, 4).font.color.rgb)[-6:] == "0000FF":
                previo["costos"][texto(co.cell(r, 2).value)] = (co.cell(r, 3).value, co.cell(r, 4).value)
    pr = wb["PRECIOS"]
    for r in range(8, pr.max_row + 1):
        if pr.cell(r, 2).value:  # público, descuento propio, observaciones
            previo["precios"][texto(pr.cell(r, 2).value)] = (pr.cell(r, 3).value, pr.cell(r, 4).value,
                                                             pr.cell(r, 7).value)
    previo["iva"], previo["descuento"] = pr["C4"].value, pr["C5"].value
    if HOJA_NEGOCIO in wb.sheetnames:
        sn = wb[HOJA_NEGOCIO]
        for r in range(4, 8):
            c = sn.cell(r, 3)
            if sn.cell(r, 2).value and c.font.color is not None and str(c.font.color.rgb)[-6:] == "0000FF":
                previo["supuestos"][texto(sn.cell(r, 2).value)] = c.value
    for hoja in ("RESUMEN", "PRECIOS", "SELECCIONES ROPA 2027", "CUERPO TÉCNICO 2027"):
        if hoja in wb.sheetnames:
            previo["extras"][hoja] = [(c.row, c.column, c.value, c.number_format, bool(c.font and c.font.b))
                                      for row in wb[hoja].iter_rows() for c in row if c.value is not None]
    for hoja in ("SELECCIONES ROPA 2027", "CUERPO TÉCNICO 2027"):
        ws = wb[hoja]
        for row in ws.iter_rows():
            for c in row:
                if c.font and c.font.color is not None and str(c.font.color.rgb)[-6:] == "0000FF" and c.value is not None:
                    previo["celdas"][(hoja, c.coordinate)] = c.value
    return previo


def main():
    selecciones, tecnicos = leer_proyeccion()
    previo = leer_previo()

    NAVY = "002060"
    f_tit = Font(name="Calibri", size=14, bold=True, color=NAVY)
    f_sec = Font(name="Calibri", size=12, bold=True, color=NAVY)
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

    def logo(ws, archivo):
        ruta = DIR / archivo
        if ruta.exists():
            im = XLImage(str(ruta))
            im.width, im.height = 72, 64
            ws.add_image(im, "A1")

    def encabezado(ws, titulo, bajada):
        celda(ws, "C2", titulo, f_tit, alinear=Alignment(vertical="center"), borde=False)
        celda(ws, "C3", bajada, f_nota, alinear=Alignment(vertical="center"), borde=False)
        ws.row_dimensions[1].height = 22
        ws.column_dimensions["A"].width = 11

    # ---------------------------------------------------------------- PRECIOS
    pr = wb.active
    pr.title = "PRECIOS"
    logo(pr, "logo_fevochi.png")
    encabezado(pr, "PRECIOS POR PRENDA", "Celdas amarillas: precio público general (con IVA) y descuento. El precio "
                                         "federación se calcula solo y se aplica a todas las categorías.")
    celda(pr, "B4", "IVA", f_tot, alinear=izq)
    celda(pr, "C4", previo["iva"] if previo and previo["iva"] is not None else IVA, f_input, "0%", r_input)
    celda(pr, "B5", "Descuento general para la federación", f_tot, alinear=izq)
    celda(pr, "C5", previo["descuento"] if previo and previo["descuento"] is not None else 0, f_input, "0%", r_input)
    celda(pr, "D5", "Se aplica a las prendas que no tienen un descuento propio en la columna DESCUENTO.", f_nota,
          alinear=Alignment(vertical="center"), borde=False)
    cabecera(pr, 7, 2, ["PRENDA", "PRECIO PÚBLICO GENERAL (CON IVA)", "DESCUENTO FEDERACIÓN",
                        "PRECIO FEDERACIÓN (CON IVA)", "PRECIO FEDERACIÓN NETO", "OBSERVACIONES"], alto=36)
    fila_precio = {}
    r = 8
    for grupo, prendas in PRENDAS:
        celda(pr, f"B{r}", grupo, Font(name="Calibri", size=10, bold=True, color=NAVY), relleno=r_sub, alinear=izq)
        for col in "CDEFG":
            celda(pr, f"{col}{r}", None, relleno=r_sub)
        r += 1
        for p in prendas:
            fila_precio[p] = r
            publico, desc, obs = previo["precios"].get(p, (None, None, None)) if previo else (None, None, None)
            celda(pr, f"B{r}", p, alinear=izq)
            celda(pr, f"C{r}", publico, f_input, PESOS, r_input)
            celda(pr, f"D{r}", desc, f_input, "0%", r_input)
            celda(pr, f"E{r}", f'=ROUND(N(C{r})*(1-IF(D{r}="",$C$5,D{r})),0)', f_tot, PESOS)
            celda(pr, f"F{r}", f"=ROUND(E{r}/(1+$C$4),0)", formato=PESOS)
            celda(pr, f"G{r}", obs, f_input, relleno=r_input, alinear=izq)
            r += 1
    ultima_precio = r - 1
    for col, ancho in zip("BCDEFG", (40, 18, 14, 18, 16, 40)):
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

    def precio_de(prenda, col="E"):  # E: precio federación; C: precio público
        return (f"N(INDEX(PRECIOS!${col}$8:${col}${ultima_precio},"
                f"MATCH(\"{prenda}\",PRECIOS!$B$8:$B${ultima_precio},0)))")

    # ---------------------------------------------------------------- SELECCIONES ROPA 2027
    se = wb.create_sheet("SELECCIONES ROPA 2027")
    logo(se, "logo_fevochi.png")
    encabezado(se, "SELECCIONES 2027: ROPA VALORIZADA POR CATEGORÍA",
               "Celdas amarillas: jugadores, unidades por jugador y canje (editables). CANJE SÍ = 100% de descuento en esa "
               "prenda. El precio público solo valoriza el canje.")
    dv_canje = DataValidation(type="list", formula1='"SÍ,NO"', allow_blank=True, errorTitle="Canje",
                              error="Elige SÍ (canje, 100% de descuento) o NO.")
    r = 5
    totales_sel = []  # (título, [(categoría, primera fila, fila subtotal)], fila total)
    for titulo, cats in selecciones:
        celda(se, f"B{r}", titulo, f_sec, alinear=Alignment(vertical="center"), borde=False)
        se.row_dimensions[r].height = 20
        r += 1
        cabecera(se, r, 2, ["CATEGORÍA", "CANTIDAD DE JUGADORES" if "MASCULINA" in titulo else "CANTIDAD DE JUGADORAS",
                            "PRENDA", "COLORES", "UNIDADES POR JUGADOR" if "MASCULINA" in titulo else
                            "UNIDADES POR JUGADORA", "TOTAL UNIDADES", "PRECIO PÚBLICO",
                            "PRECIO FEDERACIÓN", "CANJE", "VALOR A PAGAR"])
        r += 1
        filas_cat = []
        for cat, jugadores, items in cats:
            f0 = r
            canje = "SÍ" if cat.upper().startswith("ADULTO") else "NO"  # canje: equipos adultos
            for k, (prenda, unid, colores) in enumerate(items):
                if k == 0:
                    celda(se, f"B{r}", cat, f_tot)
                    entrada(se, f"C{r}", jugadores, NUM)
                else:
                    celda(se, f"B{r}", None)
                    celda(se, f"C{r}", f"=C{f0}", f_gris, NUM)
                celda(se, f"D{r}", prenda, alinear=izq)
                entrada(se, f"E{r}", colores or None, alinear=izq)
                entrada(se, f"F{r}", unid, NUM)
                celda(se, f"G{r}", f"=C{r}*F{r}", formato=NUM)
                celda(se, f"H{r}", "=" + precio_de(prenda, "C"), f_gris, PESOS)
                celda(se, f"I{r}", "=" + precio_de(prenda), formato=PESOS)
                entrada(se, f"J{r}", canje)
                celda(se, f"K{r}", f'=IF(J{r}="SÍ",0,G{r}*I{r})', f_tot, PESOS)
                r += 1
            dv_canje.add(f"J{f0}:J{r - 1}")
            celda(se, f"B{r}", f"Total {cat}", f_tot, relleno=r_sub)
            for col in "DEFHIJ":
                celda(se, f"{col}{r}", None, relleno=r_sub)
            celda(se, f"C{r}", f"=C{f0}", f_tot, NUM, r_sub)
            celda(se, f"G{r}", f"=SUM(G{f0}:G{r - 1})", f_tot, NUM, r_sub)
            celda(se, f"K{r}", f"=SUM(K{f0}:K{r - 1})", f_tot, PESOS, r_sub)
            filas_cat.append((cat, f0, r))
            r += 1
        celda(se, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)  # el título de la sección va arriba
        for col in "CDEFGHIJK":
            celda(se, f"{col}{r}", None, f_gran, relleno=r_gran)
        celda(se, f"C{r}", "=" + "+".join(f"C{s}" for _, _, s in filas_cat), f_gran, NUM, r_gran)
        celda(se, f"G{r}", "=" + "+".join(f"G{s}" for _, _, s in filas_cat), f_gran, NUM, r_gran)
        celda(se, f"K{r}", "=" + "+".join(f"K{s}" for _, _, s in filas_cat), f_gran, PESOS, r_gran)
        se.row_dimensions[r].height = 20
        totales_sel.append((titulo, filas_cat, r))
        r += 3
    se.add_data_validation(dv_canje)
    for col, ancho in zip("BCDEFGHIJK", (20, 14, 33, 22, 13, 12, 15, 13, 10, 16)):
        se.column_dimensions[col].width = ancho
    dv2 = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                         errorTitle="Cantidad", error="Ingresa un número entero (0 o más).")
    se.add_data_validation(dv2)
    for _, filas_cat, _ in totales_sel:
        for _, f0, s in filas_cat:
            dv2.add(f"C{f0}")
            dv2.add(f"F{f0}:F{s - 1}")

    # ---------------------------------------------------------------- CUERPO TÉCNICO 2027
    ct = wb.create_sheet("CUERPO TÉCNICO 2027")
    logo(ct, "logo_fevochi_2.png")
    encabezado(ct, "CUERPOS TÉCNICOS 2027: ROPA VALORIZADA",
               "Celdas amarillas: personas, cantidad por técnico y canje (editables). CANJE SÍ = 100% de descuento en esa "
               "prenda. El precio público solo valoriza el canje.")
    dv_canje_ct = DataValidation(type="list", formula1='"SÍ,NO"', allow_blank=True, errorTitle="Canje",
                                 error="Elige SÍ (canje, 100% de descuento) o NO.")
    r = 5
    totales_ct = []  # (título, primera fila, fila total)
    for titulo, personas, items in tecnicos:
        celda(ct, f"B{r}", titulo, f_sec, alinear=Alignment(vertical="center"), borde=False)
        ct.row_dimensions[r].height = 20
        r += 1
        cabecera(ct, r, 2, ["INDUMENTARIA COMPETENCIAS", "PERSONAS", "CANTIDAD POR TÉCNICO", "TOTAL UNIDADES",
                            "PRECIO PÚBLICO", "PRECIO FEDERACIÓN", "CANJE", "VALOR A PAGAR"])
        r += 1
        f0 = r
        for k, (prenda, unid) in enumerate(items):
            celda(ct, f"B{r}", prenda, alinear=izq)
            if k == 0:
                entrada(ct, f"C{r}", personas, NUM)
            else:
                celda(ct, f"C{r}", f"=C{f0}", f_gris, NUM)
            entrada(ct, f"D{r}", unid, NUM)
            celda(ct, f"E{r}", f"=C{r}*D{r}", formato=NUM)
            celda(ct, f"F{r}", "=" + precio_de(prenda, "C"), f_gris, PESOS)
            celda(ct, f"G{r}", "=" + precio_de(prenda), formato=PESOS)
            entrada(ct, f"H{r}", "NO")
            celda(ct, f"I{r}", f'=IF(H{r}="SÍ",0,E{r}*G{r})', f_tot, PESOS)
            r += 1
        dv_canje_ct.add(f"H{f0}:H{r - 1}")
        celda(ct, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
        for col in "CDEFGHI":
            celda(ct, f"{col}{r}", None, f_gran, relleno=r_gran)
        celda(ct, f"C{r}", f"=C{f0}", f_gran, NUM, r_gran)
        celda(ct, f"E{r}", f"=SUM(E{f0}:E{r - 1})", f_gran, NUM, r_gran)
        celda(ct, f"I{r}", f"=SUM(I{f0}:I{r - 1})", f_gran, PESOS, r_gran)
        ct.row_dimensions[r].height = 20
        totales_ct.append((titulo, f0, r))
        ct.add_data_validation(dv3 := DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0",
                                                     allow_blank=True, errorTitle="Cantidad",
                                                     error="Ingresa un número entero (0 o más)."))
        dv3.add(f"C{f0}")
        dv3.add(f"D{f0}:D{r - 1}")
        r += 3
    ct.add_data_validation(dv_canje_ct)
    for col, ancho in zip("BCDEFGHI", (36, 11, 13, 12, 15, 13, 10, 16)):
        ct.column_dimensions[col].width = ancho

    # ---------------------------------------------------------------- RESUMEN
    rs = wb.create_sheet("RESUMEN", 0)
    logo(rs, "logo_fevochi.png")
    encabezado(rs, "VALORIZACIÓN ROPA SELECCIONES FEVOCHI 2027",
               "Valores con IVA. El canje (100% de descuento) se valoriza a precio público general; el resto, a precio "
               "federación.")
    cabecera(rs, 5, 2, ["SELECCIÓN", "CATEGORÍA", "JUGADORES O PERSONAS", "TOTAL UNIDADES", "VALOR TOTAL DEL CANJE (PRECIO PÚBLICO)",
                        "VALOR PRECIO FEDERACIÓN", "NETO", "IVA"], alto=36)
    S, T = "'SELECCIONES ROPA 2027'", "'CUERPO TÉCNICO 2027'"
    r = 6
    filas_total = []

    def fila_resumen(r, sel, cat, jug, unid, canje, pagar, fuente=f_norm, relleno=None):
        celda(rs, f"B{r}", sel, fuente, relleno=relleno, alinear=izq)
        celda(rs, f"C{r}", cat, fuente, relleno=relleno, alinear=izq)
        celda(rs, f"D{r}", jug, fuente, NUM, relleno)
        celda(rs, f"E{r}", unid, fuente, NUM, relleno)
        celda(rs, f"F{r}", canje, fuente, PESOS, relleno)
        celda(rs, f"G{r}", pagar, fuente if relleno else f_tot, PESOS, relleno)
        celda(rs, f"H{r}", f"=ROUND(G{r}/(1+PRECIOS!$C$4),0)", fuente, PESOS, relleno)
        celda(rs, f"I{r}", f"=G{r}-H{r}", fuente, PESOS, relleno)

    def rango(hoja, col, a, b):
        return f"{hoja}!{col}{a}:{col}{b}"

    for titulo, filas_cat, ft in totales_sel:
        nombre = titulo.replace("SELECCIÓN ", "").capitalize()
        r0 = r
        for k, (cat, f0, s) in enumerate(filas_cat):
            g, h, j = rango(S, "G", f0, s - 1), rango(S, "H", f0, s - 1), rango(S, "J", f0, s - 1)
            fila_resumen(r, nombre if k == 0 else None, cat, f"={S}!C{s}", f"={S}!G{s}",
                         f'=SUMPRODUCT(({j}="SÍ")*{g}*{h})', f"={S}!K{s}")
            r += 1
        fila_resumen(r, f"Total {nombre.lower()}", None, *[f"=SUM({c}{r0}:{c}{r - 1})" for c in "DEFG"], f_tot, r_sub)
        filas_total.append(r)
        r += 1
    fct0 = r
    for k, (titulo, f0, ft) in enumerate(totales_ct):
        nombre = titulo.replace("CUERPO TÉCNICO ", "").capitalize()
        e, f, h = rango(T, "E", f0, ft - 1), rango(T, "F", f0, ft - 1), rango(T, "H", f0, ft - 1)
        fila_resumen(r, "Cuerpos técnicos" if k == 0 else None, nombre, f"={T}!C{ft}", f"={T}!E{ft}",
                     f'=SUMPRODUCT(({h}="SÍ")*{e}*{f})', f"={T}!I{ft}")
        r += 1
    fila_resumen(r, "Total cuerpos técnicos", None, *[f"=SUM({c}{fct0}:{c}{r - 1})" for c in "DEFG"], f_tot, r_sub)
    filas_total.append(r)
    r += 1
    fila_resumen(r, "TOTAL GENERAL", None, *["=" + "+".join(f"{col}{x}" for x in filas_total) for col in "DEFG"],
                 f_gran, r_gran)
    rs.row_dimensions[r].height = 22
    total_general = r

    r += 4
    celda(rs, f"B{r}", "VALOR POR PRENDA", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    cabecera(rs, r, 2, ["PRENDA", None, "PRECIO PÚBLICO", "DESCUENTO", "PRECIO FEDERACIÓN",
                        "TOTAL UNIDADES", "VALOR TOTAL DEL CANJE (PRECIO PÚBLICO)", "VALOR PRECIO FEDERACIÓN"], alto=36)
    rs.merge_cells(f"B{r}:C{r}")
    r += 1
    p0 = r
    for _, prendas in PRENDAS:
        for p in prendas:
            fp = fila_precio[p]
            celda(rs, f"B{r}", p, alinear=izq)
            celda(rs, f"C{r}", None)
            rs.merge_cells(f"B{r}:C{r}")
            celda(rs, f"D{r}", f"=PRECIOS!C{fp}", f_gris, PESOS)
            celda(rs, f"E{r}", f"=IF(N(D{r})=0,0,1-F{r}/D{r})", formato='0.0%;-0.0%;"-"')
            celda(rs, f"F{r}", f"=PRECIOS!E{fp}", formato=PESOS)
            celda(rs, f"G{r}", f'=SUMIF({S}!$D:$D,"{p}",{S}!$G:$G)+SUMIF({T}!$B:$B,"{p}",{T}!$E:$E)', formato=NUM)
            celda(rs, f"H{r}", f'=(SUMIFS({S}!$G:$G,{S}!$D:$D,"{p}",{S}!$J:$J,"SÍ")'
                               f'+SUMIFS({T}!$E:$E,{T}!$B:$B,"{p}",{T}!$H:$H,"SÍ"))*D{r}', formato=PESOS)
            celda(rs, f"I{r}", f'=SUMIF({S}!$D:$D,"{p}",{S}!$K:$K)+SUMIF({T}!$B:$B,"{p}",{T}!$I:$I)', f_tot, PESOS)
            r += 1
    celda(rs, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    for col in "CDEF":
        celda(rs, f"{col}{r}", None, f_gran, relleno=r_gran)
    rs.merge_cells(f"B{r}:C{r}")
    for col, fmt in (("G", NUM), ("H", PESOS), ("I", PESOS)):
        celda(rs, f"{col}{r}", f"=SUM({col}{p0}:{col}{r - 1})", f_gran, fmt, r_gran)
    celda(rs, f"B{r + 1}", f'=IF(AND(H{r}=F{total_general},I{r}=G{total_general}),"Control: la suma por prenda '
                           f'coincide con el total general.","Revisar: la suma por prenda no coincide con el total '
                           f'general.")', f_nota, alinear=Alignment(vertical="center"), borde=False)
    for col, ancho in zip("BCDEFGHI", (31, 18, 15, 13, 17, 17, 17, 15)):
        rs.column_dimensions[col].width = ancho
    fila_prenda_rs = {p: p0 + k for k, p in enumerate(p for _, ps in PRENDAS for p in ps)}
    rs.print_area = f"A1:I{r + 1}"  # el vínculo del PDF queda fuera de lo que se imprime

    # vínculo que genera el PDF para la federación (macro GenerarPDFFederacion, vía Workbook_SheetFollowHyperlink)
    rs.merge_cells("K2:M3")
    celda(rs, "K2", "GENERAR PDF PARA LA FEDERACIÓN", Font(name="Calibri", size=11, bold=True, color="FFFFFF",
                                                                    underline="single"), relleno=r_gran)
    for col in "LM":
        for fila in (2, 3):
            rs[f"{col}{fila}"].fill = r_gran
    rs["K2"].hyperlink = Hyperlink(ref="K2", location="RESUMEN!K2",
                                   tooltip="Generar PDF para la federacion (todas las hojas menos COSTOS y RESUMEN NEGOCIO)")
    celda(rs, "K4", "Exporta todas las hojas menos COSTOS y RESUMEN NEGOCIO (uso interno) a un PDF en la misma carpeta.", f_nota,
          alinear=Alignment(vertical="top", wrap_text=True), borde=False)
    celda(rs, "K6", "Requiere habilitar macros. Si no funciona: Archivo, Exportar, PDF, con las hojas RESUMEN, PRECIOS, "
                    "SELECCIONES ROPA 2027 y CUERPO TÉCNICO 2027 seleccionadas.", f_nota,
          alinear=Alignment(vertical="top", wrap_text=True), borde=False)
    rs.merge_cells("K4:M5")
    rs.merge_cells("K6:M9")
    for col in "KLM":
        rs.column_dimensions[col].width = 14
    rs.row_dimensions[2].height = rs.row_dimensions[3].height = 18

    # ---------------------------------------------------------------- COSTOS (uso interno)
    co = wb.create_sheet(HOJA_INTERNA)
    co.sheet_properties.tabColor = "C00000"
    logo(co, "logo_fevochi.png")
    encabezado(co, "COSTOS DEL CONVENIO (USO INTERNO, NO VA EN EL PDF)",
               "Celdas amarillas: código de inventario y costo unitario neto (sin IVA) de cada prenda. Unidades y "
               "ventas vienen de las demás hojas.")
    cabecera(co, 5, 2, ["PRENDA", "CÓDIGO INVENTARIO", "COSTO UNITARIO NETO", "UNIDADES EN CANJE",
                        "UNIDADES VENDIDAS", "TOTAL UNIDADES", "COSTO DEL CANJE", "COSTO DE LO VENDIDO",
                        "COSTO TOTAL (INVENTARIO)", "VENTA NETA FEDERACIÓN", "MARGEN DE LA VENTA", "MARGEN %"], alto=40)
    r = 6
    c0 = r
    for _, prendas in PRENDAS:
        for p in prendas:
            fr = fila_prenda_rs[p]
            codigo, costo = previo["costos"].get(p, (None, None)) if previo else (None, None)
            celda(co, f"B{r}", p, alinear=izq)
            celda(co, f"C{r}", codigo, f_input, relleno=r_input, alinear=izq)
            celda(co, f"D{r}", costo, f_input, PESOS, r_input)
            celda(co, f"E{r}", f'=SUMIFS({S}!$G:$G,{S}!$D:$D,"{p}",{S}!$J:$J,"SÍ")'
                               f'+SUMIFS({T}!$E:$E,{T}!$B:$B,"{p}",{T}!$H:$H,"SÍ")', formato=NUM)
            celda(co, f"F{r}", f"=G{r}-E{r}", formato=NUM)
            celda(co, f"G{r}", f"=RESUMEN!G{fr}", formato=NUM)
            celda(co, f"H{r}", f"=E{r}*N(D{r})", formato=PESOS)
            celda(co, f"I{r}", f"=F{r}*N(D{r})", formato=PESOS)
            celda(co, f"J{r}", f"=H{r}+I{r}", f_tot, PESOS)
            celda(co, f"K{r}", f"=ROUND(RESUMEN!I{fr}/(1+PRECIOS!$C$4),0)", formato=PESOS)
            celda(co, f"L{r}", f"=K{r}-I{r}", f_tot, PESOS)
            celda(co, f"M{r}", f'=IF(OR(K{r}=0,N(D{r})=0),"",L{r}/K{r})', formato='0.0%;-0.0%;"-"')
            r += 1
    celda(co, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    for col in "CD":
        celda(co, f"{col}{r}", None, f_gran, relleno=r_gran)
    for col in "EFGHIJKL":
        celda(co, f"{col}{r}", f"=SUM({col}{c0}:{col}{r - 1})", f_gran, NUM if col in "EFG" else PESOS, r_gran)
    celda(co, f"M{r}", f'=IF(OR(K{r}=0,COUNT(D{c0}:D{r - 1})<ROWS(D{c0}:D{r - 1})),"",L{r}/K{r})', f_gran,
          '0.0%;-0.0%;"-"', r_gran)
    tc = r
    r += 3
    celda(co, f"B{r}", "RESULTADO DEL CONVENIO", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    resultado = [
        ("Valor del canje para la federación (precio público, con IVA)", f"=RESUMEN!F{total_general}", f_norm),
        ("Costo real del canje para Playmaker (neto)", f"=H{tc}", f_norm),
        ("Venta a la federación (neto, sin IVA)", f"=K{tc}", f_norm),
        ("Costo de lo vendido (neto)", f"=I{tc}", f_norm),
        ("Margen de la venta", f"=L{tc}", f_tot),
        ("Resultado del convenio (margen de la venta menos costo del canje)", f"=L{tc}-H{tc}", f_tot),
        ("Costo total de inventario a producir (canje y venta)", f"=J{tc}", f_tot),
    ]
    for k, (txt, f, fuente) in enumerate(resultado):
        celda(co, f"B{r}", txt, fuente, alinear=izq)
        for col in "CDEF":
            celda(co, f"{col}{r}", None)
        co.merge_cells(f"B{r}:F{r}")
        celda(co, f"G{r}", f, fuente, PESOS, r_sub if fuente is f_tot else None)
        r += 1
    co.conditional_formatting.add(f"G{r - 2}", CellIsRule(operator="lessThan", formula=["0"],
                                                          fill=PatternFill("solid", fgColor="F6D5D0")))
    celda(co, f"B{r + 1}", "Si falta el costo de una prenda, sus costos quedan en cero: completa la columna COSTO "
                           "UNITARIO NETO para que el resultado sea real.", f_nota, alinear=Alignment(vertical="center"),
          borde=False)
    dvc = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                         errorTitle="Costo", error="Ingresa un costo en pesos (0 o más).")
    co.add_data_validation(dvc)
    dvc.add(f"D{c0}:D{tc - 1}")
    for col, ancho in zip("BCDEFGHIJKLM", (34, 15, 13, 12, 12, 12, 15, 15, 16, 16, 15, 10)):
        co.column_dimensions[col].width = ancho

    # ---------------------------------------------------------------- RESUMEN NEGOCIO (uso interno)
    sn = wb.create_sheet(HOJA_NEGOCIO, 1)
    sn.sheet_properties.tabColor = "C00000"
    logo(sn, "logo_fevochi.png")
    encabezado(sn, "RESUMEN DEL NEGOCIO FEVOCHI 2027: VENTA NETA, COSTOS Y MARGEN TOTAL (USO INTERNO, NO VA EN EL PDF)",
               "Todo neto, sin IVA, salvo el canje a precio público. Se actualiza solo con lo cargado en las demás hojas "
               "(precios, jugadores, unidades, canje y costos unitarios de la hoja COSTOS).")
    PCT = '0.0%;-0.0%;"-"'
    otros_txt = "Otros costos del negocio (% de la venta neta: despacho, comisiones, etc.)"
    otros_v = previo.get("supuestos", {}).get(otros_txt) if previo else None
    celda(sn, "B5", otros_txt, f_tot, alinear=izq)
    celda(sn, "C5", otros_v if otros_v is not None else 0, f_input, "0%", r_input)
    celda(sn, "D5", "Supuesto para simular: parte en 0%.", f_nota, alinear=Alignment(vertical="center"), borde=False)
    dvs = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=False,
                         errorTitle="Supuesto", error="Ingresa un porcentaje entre 0% y 100%.")
    sn.add_data_validation(dvs)
    dvs.add("C5")
    for g0, g1, txt, fondo in (("C", "G", "VENTA A LA FEDERACIÓN (SIN IVA)", "2F5597"),
                               ("H", "J", "CANJE (100% DE DESCUENTO)", "7030A0"), ("K", "L", "RESULTADO", NAVY)):
        celda(sn, f"{g0}7", txt, Font(name="Calibri", size=10, bold=True, color="FFFFFF"),
              relleno=PatternFill("solid", fgColor=fondo))
        sn.merge_cells(f"{g0}7:{g1}7")
    cabecera(sn, 8, 2, ["LÍNEA", "UNIDADES VENDIDAS", "VENTA NETA", "COSTO DE LO VENDIDO", "MARGEN DE LA VENTA",
                        "MARGEN % DE LA VENTA", "UNIDADES EN CANJE", "CANJE A PRECIO PÚBLICO (CON IVA)",
                        "COSTO DEL CANJE", "MARGEN TOTAL", "MARGEN TOTAL % SOBRE VENTA"], alto=40)
    costo_n, costo_d = f"COSTOS!$B${c0}:$B${tc - 1}", f"COSTOS!$D${c0}:$D${tc - 1}"

    def suma(hoja, rangos, expr):
        """SUMPRODUCT de expr (con {p} prenda, {u} unidades, {h} precio público, {c} canje) sobre cada rango."""
        partes = []
        for a, b, cp, cu, ch, cc in rangos:
            rg = {k: f"{hoja}!{col}{a}:{col}{b}" for k, col in (("p", cp), ("u", cu), ("h", ch), ("c", cc))}
            rg["costo"] = f"SUMIF({costo_n},{rg['p']},{costo_d})"
            partes.append("SUMPRODUCT(" + expr.format(**rg) + ")")
        return "+".join(partes)

    def fila_neg(r, txt, uv, venta, cv, uc, canje, cc, fuente=f_norm, relleno=None):
        celda(sn, f"B{r}", txt, fuente, relleno=relleno, alinear=izq)
        for col, v, fmt in (("C", uv, NUM), ("D", venta, PESOS), ("E", cv, PESOS), ("H", uc, NUM), ("I", canje, PESOS),
                            ("J", cc, PESOS)):
            celda(sn, f"{col}{r}", v, fuente, fmt, relleno)
        celda(sn, f"F{r}", f"=D{r}-E{r}", fuente if relleno else f_tot, PESOS, relleno)
        celda(sn, f"G{r}", f'=IF(D{r}=0,"",F{r}/D{r})', fuente, PCT, relleno)
        celda(sn, f"K{r}", f"=F{r}-J{r}", fuente if relleno else f_tot, PESOS, relleno)
        celda(sn, f"L{r}", f'=IF(D{r}=0,"",K{r}/D{r})', fuente, PCT, relleno)

    def titulo_neg(r, txt):
        celda(sn, f"B{r}", txt, Font(name="Calibri", size=10, bold=True, color=NAVY), relleno=r_sub, alinear=izq)
        for col in "CDEFGHIJKL":
            celda(sn, f"{col}{r}", None, relleno=r_sub)

    def fila_de(r, txt, hoja, rangos, total_pagar):
        fila_neg(r, txt, "=" + suma(hoja, rangos, '{u}*({c}<>"SÍ")'),
                 f"=ROUND({total_pagar}/(1+PRECIOS!$C$4),0)", "=" + suma(hoja, rangos, '{costo}*{u}*({c}<>"SÍ")'),
                 "=" + suma(hoja, rangos, '{u}*({c}="SÍ")'), "=" + suma(hoja, rangos, '{u}*{h}*({c}="SÍ")'),
                 "=" + suma(hoja, rangos, '{costo}*{u}*({c}="SÍ")'))

    r = 9
    titulo_neg(r, "SELECCIONES")
    r += 1
    s0 = r
    for titulo, filas_cat, ft in totales_sel:
        rangos = [(f0, s_ - 1, "D", "G", "H", "J") for _, f0, s_ in filas_cat]
        fila_de(r, "Selección " + titulo.replace("SELECCIÓN ", "").lower(), S, rangos, f"{S}!K{ft}")
        r += 1
    fila_neg(r, "Total selecciones", *[f"=SUM({c}{s0}:{c}{r - 1})" for c in "CDEHIJ"], fuente=f_tot, relleno=r_sub)
    sub = [r]
    r += 1
    titulo_neg(r, "CUERPOS TÉCNICOS")
    r += 1
    s0 = r
    for titulo, f0, ft in totales_ct:
        fila_de(r, titulo.capitalize(), T, [(f0, ft - 1, "B", "E", "F", "H")], f"{T}!I{ft}")
        r += 1
    fila_neg(r, "Total cuerpos técnicos", *[f"=SUM({c}{s0}:{c}{r - 1})" for c in "CDEHIJ"], fuente=f_tot,
             relleno=r_sub)
    sub.append(r)
    r += 1
    titulo_neg(r, "OTROS COSTOS")
    r += 1
    fila_neg(r, "Otros costos del negocio (% de la venta neta)", None, 0, "=ROUND((" + "+".join(f"D{x}" for x in sub)
             + ")*$C$5,0)", None, 0, 0)
    otros = r
    r += 1
    fila_neg(r, "MARGEN TOTAL DEL NEGOCIO", *["=" + "+".join(f"{c}{x}" for x in sub + [otros]) for c in "CDEHIJ"],
             fuente=f_gran, relleno=r_gran)
    tn = r
    sn.row_dimensions[r].height = 22
    for col in "FGKL":
        sn.conditional_formatting.add(f"{col}{tn}", CellIsRule(operator="lessThan", formula=["0"],
                                                               fill=PatternFill("solid", fgColor="C00000")))
    celda(sn, f"B{r + 1}", f'=IF(AND(ABS(D{tn}-COSTOS!K{tc})<=10,ROUND(E{tn}-E{otros},0)=COSTOS!I{tc},J{tn}=COSTOS!H{tc}),"Control: '
                           f'coincide con la hoja COSTOS (la venta neta puede diferir en unos pesos por redondeo).",'
                           f'"Revisar: no coincide con la hoja COSTOS.")', f_nota,
          alinear=Alignment(vertical="center"), borde=False)

    r += 4
    celda(sn, f"B{r}", "RESULTADO DEL NEGOCIO 2027", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    cabecera(sn, r, 2, ["CONCEPTO", None, "MONTO", "% SOBRE VENTA NETA"], alto=24)
    sn.merge_cells(f"B{r}:C{r}")
    r += 1
    ev, fv = ("+".join(f"{c}{x}" for x in sub) for c in "EF")  # costo y margen de la venta (sin otros costos)
    m_venta = f"IF(D{tn}=0,0,({fv})/D{tn})"
    kpis = [
        ("Venta neta a la federación (sin IVA)", f"=D{tn}", True, f_norm),
        ("Costo de lo vendido", f"={ev}", True, f_norm),
        ("Margen de la venta", f"={fv}", True, f_tot),
        ("Costo del canje (inversión en la federación)", f"=J{tn}", True, f_norm),
        ("Otros costos del negocio", f"=E{otros}", True, f_norm),
        ("MARGEN TOTAL DEL NEGOCIO", f"=K{tn}", True, f_gran),
        (None, None, None, None),
        ("Canje entregado a la federación, a precio público (con IVA)", f"=I{tn}", False, f_norm),
        ("Costo total a producir (canje y venta)", f"={ev}+J{tn}", False, f_norm),
        ("Unidades a producir (canje y venta)", f"=C{tn}+H{tn}", False, f_norm),
        ("Venta neta necesaria para cubrir el canje y los otros costos (punto de equilibrio, con el margen % actual "
         "de la venta)", f'=IF({m_venta}-$C$5<=0,"No se cubre",ROUND(J{tn}/({m_venta}-$C$5),0))', False,
         f_norm),
        ("Venta neta actual sobre el punto de equilibrio", "PE", False, f_norm),
    ]
    fila_pe = r + len(kpis) - 2
    for txt, f, con_pct, fuente in kpis:
        if txt is None:
            r += 1
            continue
        relleno = r_gran if fuente is f_gran else (r_sub if fuente is f_tot else None)
        celda(sn, f"B{r}", txt, fuente, relleno=relleno, alinear=izq)
        celda(sn, f"C{r}", None, fuente, relleno=relleno)
        sn.merge_cells(f"B{r}:C{r}")
        if f == "PE":
            celda(sn, f"D{r}", f'=IF(ISNUMBER(D{fila_pe}),IF(D{fila_pe}=0,"",D{tn}/D{fila_pe}),"")', fuente, "0%",
                  relleno)
        else:
            celda(sn, f"D{r}", f, fuente, NUM if txt.startswith("Unidades") else PESOS, relleno)
        celda(sn, f"E{r}", f'=IF(D{tn}=0,"",D{r}/D{tn})' if con_pct else None, fuente, PCT, relleno)
        if fuente is f_gran:
            sn.row_dimensions[r].height = 22
            sn.conditional_formatting.add(f"D{r}:E{r}", CellIsRule(operator="lessThan", formula=["0"],
                                                                    fill=PatternFill("solid", fgColor="C00000")))
        if len(txt) > 70:
            sn.row_dimensions[r].height = 30
        r += 1
    celda(sn, f"B{r + 1}", "Si falta el costo de una prenda (hoja COSTOS), su costo queda en cero y el margen se ve "
                           "mayor de lo real.", f_nota, alinear=Alignment(vertical="center"), borde=False)
    for col, ancho in zip("BCDEFGHIJKL", (50, 12, 15, 15, 15, 11, 12, 16, 15, 15, 12)):
        sn.column_dimensions[col].width = ancho
    sn.freeze_panes = "C9"

    # celdas que el usuario agregó fuera de las tablas (abajo o a la derecha de lo generado): se conservan
    if previo:
        for hoja, celdas_ in previo["extras"].items():
            if hoja not in wb.sheetnames:
                continue
            ws = wb[hoja]
            lim_r, lim_c = ws.max_row, ws.max_column
            for fila, col, valor, formato, negrita in celdas_:
                if fila > lim_r or col > lim_c:
                    c = ws.cell(fila, col, valor)
                    c.number_format, c.font = formato, Font(name="Calibri", size=11, bold=negrita)

    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
        ws.page_setup.orientation = "landscape" if ws.title != "PRECIOS" else "portrait"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    se.freeze_panes = "B5"
    for k, ws in enumerate(wb.worksheets, start=1):  # nombres VBA de las hojas (como los asigna Excel)
        ws.sheet_properties.codeName = f"Sheet{k}"
    agregar_vba(wb, MACRO_PDF, EVENTO_VINCULO)
    wb.save(SALIDA)
    n_filas = sum(len(items) for _, cats in selecciones for _, _, items in cats)
    print(f"OK  {SALIDA.name}  ({len(selecciones)} selecciones, {n_filas} filas de prendas, {len(tecnicos)} cuerpos técnicos)")


if __name__ == "__main__":
    main()
