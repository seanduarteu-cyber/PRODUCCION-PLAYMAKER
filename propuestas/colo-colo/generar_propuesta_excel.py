"""Propuesta comercial 2027 para las ramas deportivas del CSD Colo-Colo, en Excel con macros.

Uso:
    python3 propuestas/colo-colo/generar_propuesta_excel.py

Lee el requerimiento del club (Requerimiento_Indumentaria_2027_CSD_Colo_Colo.xlsx: pestañas CANJE 1EROS EQUIPOS,
FORMATIVAS y COMERCIAL) y crea Propuesta_Comercial_CSD_Colo_Colo_2027.xlsm, con el formato de la valorización
FEVOCHI y de Los Leones:
  - PRECIOS: por disciplina (básquetbol, futsal, vóleibol, patín, Esperanza Alba e institucional), cada producto
    con su precio (la camiseta de juego de básquetbol es distinta de la de futsal o la de vóleibol). Un precio
    público por producto (se escribe una sola vez) y tres descuentos, uno por categoría:
    canje (100%), formativas y cuerpo técnico, y comercial (stock que el club compra para su tienda). Cada precio
    sale del público con su descuento, terminado en 900. Un producto puede tener su propio descuento en cada
    categoría. Al lado, fuera de lo que se imprime, el costo unitario neto y el margen de cada precio.
  - CANJE PRIMEROS EQUIPOS, FORMATIVAS Y CT, COMERCIAL: lo pedido por el club, por rama, con el producto
    Playmaker (lista desplegable), cantidades, precio, valor a precio público, valor a pagar y descuento (en el
    canje, el valor del canje). Columnas internas de costo fuera de lo que se imprime.
  - RESUMEN: por categoría y rama, valor del canje y ventas (neto e IVA); valor por producto. Vínculo GENERAR PDF
    PARA EL CLUB (macro): exporta todas las hojas menos COSTOS.
  - COSTOS (uso interno): costo y margen por producto y resultado de la propuesta.
En formativas y comercial se usa la cantidad ajustada del club (Q ADAPTADA o Q MODIFICADA) y, si no la tiene,
la cantidad pedida. Si la planilla ya existe, se conservan los precios, descuentos, costos y cantidades cargados.
"""

import re
import sys
from pathlib import Path

import openpyxl
import openpyxl.utils
from openpyxl.drawing.image import Image as XLImage
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.hyperlink import Hyperlink

DIR = Path(__file__).parent
sys.path.insert(0, str(DIR.parent))
from vba_proyecto import agregar_vba  # noqa: E402

REQUERIMIENTO = DIR / "Requerimiento_Indumentaria_2027_CSD_Colo_Colo.xlsx"
SALIDA = DIR / "Propuesta_Comercial_CSD_Colo_Colo_2027.xlsm"
LOGO = DIR.parent / "_recursos" / "playmaker_logo_horizontal_navy.png"
IVA = 0.19
HOJA_INTERNA = "COSTOS"

# categorías: clave, pestaña del requerimiento, hoja de la propuesta, título, descuento general, etiqueta del precio
CATEGORIAS = [
    ("canje", "CANJE 1EROS EQUIPOS", "CANJE PRIMEROS EQUIPOS", "Canje primeros equipos", 1.00, "CANJE"),
    ("formativas", "FORMATIVAS", "FORMATIVAS Y CT", "Formativas y cuerpo técnico", 0.15, "FORMATIVAS Y CT"),
    ("comercial", "COMERCIAL", "COMERCIAL", "Comercial (stock para la tienda)", 0.30, "COMERCIAL"),
]

# producto: (nombre, línea, precio público de referencia con IVA, referencia del precio,
#            costo unitario neto de referencia: costos cargados en la propuesta de Los Leones o su prenda más parecida)
PRODUCTOS = {
    "camiseta_juego": ("Camiseta de juego", "Juego", 30900, "Lista Los Leones 2027", 14653),
    "short_juego": ("Short de juego", "Juego", 22900, "Lista Los Leones 2027", 11600),
    "calza_juego": ("Calza de juego", "Juego", 22900, "Referencia: short de juego", 11600),
    "medias": ("Calcetas o medias de juego", "Juego", 12900, "Lista Los Leones 2027", 5000),
    "salida_mc": ("Camiseta de salida manga corta", "Juego", 20900, "Referencia: polera de calentamiento", 10008),
    "salida_ml": ("Camiseta de salida manga larga", "Juego", 24900, "Estimado: confirmar", 11500),
    "reversible": ("Camiseta reversible", "Entrenamiento", 29900, "Lista Los Leones 2027", 11640),
    "short_entr": ("Short de entrenamiento", "Entrenamiento", 18900, "Lista Los Leones 2027", 9268),
    "calza_entr": ("Calza de entrenamiento", "Entrenamiento", 19900, "Estimado: confirmar", 9268),
    "polera_entr": ("Polera de entrenamiento", "Entrenamiento", 19900, "Lista Los Leones 2027", 10531),
    "polera_sm": ("Polera de entrenamiento sin manga", "Entrenamiento", 20900, "Referencia: sudadera Old Green", 10008),
    "poleron_entr": ("Polerón de entrenamiento cierre 1/4", "Entrenamiento", 33900, "Lista Los Leones 2027", 15000),
    "pantalon_entr": ("Pantalón de entrenamiento", "Entrenamiento", 28900, "Referencia: pantalón de buzo", 13000),
    "polera_pres": ("Polera de presentación", "Presentación", 23900, "Referencia: polo piqué", 13000),
    "poleron_pres": ("Polerón de presentación", "Presentación", 35900, "Lista Los Leones 2027", 12000),
    "pantalon_pres": ("Pantalón de presentación", "Presentación", 28900, "Lista Los Leones 2027", 13000),
    "short_pres": ("Short de presentación", "Presentación", 22900, "Lista Los Leones 2027", 11000),
    "chaqueta_pres": ("Chaqueta de presentación", "Presentación", 65900, "Lista Los Leones 2027", 28000),
    "parka": ("Parka", "Presentación", 79900, "Lista Los Leones 2027", 35000),
}
# disciplina de cada rama del requerimiento: cada disciplina tiene su propia lista de productos y precios (su camiseta
# de juego, su short, etc.). Cuerpo técnico, directorio y oficina comparten la ropa institucional.
RAMA_DISCIPLINA = {"Cuerpo Técnico": "Institucional", "Directorio": "Institucional", "Oficina": "Institucional"}
TITULO_DISCIPLINA = {"Institucional": "INSTITUCIONAL (CUERPO TÉCNICO, DIRECTORIO Y OFICINA)"}
SUFIJO_DISCIPLINA = {"Esperanza Alba": "Esperanza Alba"}  # en el nombre del producto; las demás van en minúscula


def disciplina_de(rama):
    return RAMA_DISCIPLINA.get(rama, rama)


def nombre_producto(k, disciplina):
    return f"{PRODUCTOS[k][0]} {SUFIJO_DISCIPLINA.get(disciplina, disciplina.lower())}"
# prenda del requerimiento (normalizada) -> producto
MAPA = {
    "camiseta juego": "camiseta_juego", "short juego": "short_juego", "calzas juego": "calza_juego",
    "calcetas juego": "medias", "medias juego": "medias",
    "camiseta salida manga corta": "salida_mc", "camiseta salida manga larga": "salida_ml",
    "camiseta reversible": "reversible", "short entrenamiento": "short_entr", "calza entrenamiento": "calza_entr",
    "calza/short entrenamiento": "calza_entr", "polera entrenamiento": "polera_entr",
    "polera entrenamiento sin manga": "polera_sm", "polerón entrenamiento": "poleron_entr",
    "pantalón entrenamiento": "pantalon_entr", "polera presentación": "polera_pres",
    "polerón presentación": "poleron_pres", "pantalón presentación": "pantalon_pres",
    "pantalon presentación": "pantalon_pres", "short presentación": "short_pres",
    "chaqueta presentación": "chaqueta_pres", "parka": "parka",
}

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
    ruta = ThisWorkbook.Path & Application.PathSeparator & "Propuesta_Comercial_CSD_Colo_Colo_2027.pdf"
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


def norm(s):
    s = str(s or "").lower().replace("à", "á").replace("ò", "ó").replace("è", "é").replace("ì", "í")
    return " ".join(re.sub(r"\bde\b", " ", s).split())


def titulo_rama(s):
    t = norm(s).replace("voleibol", "vóleibol")
    return " ".join(w.capitalize() for w in t.split())


def leer_requerimiento():
    """Por categoría: [(rama, tipo, prenda, modelo, color, producto, cantidad pedida, cantidad ajustada)]."""
    wb = openpyxl.load_workbook(REQUERIMIENTO)
    datos = {}
    for clave, pestaña, *_x in CATEGORIAS:
        ws = wb[pestaña]
        cab = next(r for r in range(1, 15) if norm(ws.cell(r, 2).value) == "rama")
        filas, rama, tipo = [], None, None
        for r in range(cab + 1, ws.max_row + 1):
            b, c, d = ws.cell(r, 2).value, ws.cell(r, 3).value, ws.cell(r, 4).value
            if b:
                rama = titulo_rama(b)
            if c:
                tipo = texto(c).replace("Ò", "Ó").capitalize()
            if not d:
                continue
            k = MAPA.get(norm(d))
            if k is None:
                sys.exit(f"Prenda sin producto asignado: {d} (agrégala en MAPA)")
            g, h = ws.cell(r, 7).value, ws.cell(r, 8).value
            pedida = g if isinstance(g, (int, float)) else 0
            ajustada = h if isinstance(h, (int, float)) else pedida
            prenda = texto(d).replace("ò", "ó").replace("à", "á")
            filas.append((rama, tipo, prenda[0].upper() + prenda[1:], texto(ws.cell(r, 5).value).capitalize(),
                          texto(ws.cell(r, 6).value), k, pedida, ajustada if clave != "canje" else pedida))
        datos[clave] = filas
    return datos


def leer_previo():
    if not SALIDA.exists():
        return None
    wb = openpyxl.load_workbook(SALIDA)
    azul = lambda c: c.font is not None and c.font.color is not None and str(c.font.color.rgb)[-6:] == "0000FF"  # noqa: E731
    previo = {"precios": {}, "generales": {}, "celdas": {}}
    pr = wb["PRECIOS"]
    for r in range(4, 9):
        etq = texto(pr.cell(r, 2).value).lower()
        for clave, *_x in CATEGORIAS:
            if clave in etq or (clave == "formativas" and "formativas" in etq):
                previo["generales"][clave] = pr.cell(r, 3).value
        if etq == "iva":
            previo["generales"]["iva"] = pr.cell(r, 3).value
    cab = next(r for r in range(1, 15) if texto(pr.cell(r, 2).value) == "PRODUCTO")
    cols = {texto(pr.cell(cab, c).value): c for c in range(2, pr.max_column + 1)}
    for r in range(cab + 1, pr.max_row + 1):
        if pr.cell(r, 2).value and azul(pr.cell(r, 4)):
            previo["precios"][texto(pr.cell(r, 2).value)] = {t: pr.cell(r, c).value for t, c in cols.items()}
    for _c, _p, hoja, *_x in CATEGORIAS:
        if hoja not in wb.sheetnames:
            continue
        ws = wb[hoja]
        cab = next((r for r in range(1, 15) if texto(ws.cell(r, 2).value) == "RAMA"), None)
        if cab is None:
            continue
        nombres = {c: texto(ws.cell(cab, c).value) for c in range(2, ws.max_column + 1)}
        for row in ws.iter_rows(min_row=cab + 1):
            for c in row:
                if azul(c) and c.value is not None and nombres.get(c.column):
                    previo["celdas"][(hoja, c.row, nombres[c.column])] = c.value
    return previo


def main():
    datos = leer_requerimiento()
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
    r_int = PatternFill("solid", fgColor="C00000")
    r_int_suave = PatternFill("solid", fgColor="FBE5E1")
    fino = Side(style="thin", color="A6A6A6")
    caja = Border(left=fino, right=fino, top=fino, bottom=fino)
    PESOS = '"$"#,##0;-"$"#,##0;"-"'
    NUM = '#,##0;-#,##0;"-"'
    PCT = '0.0%;-0.0%;"-"'
    centro = Alignment(horizontal="center", vertical="center", wrap_text=True)
    izq = Alignment(horizontal="left", vertical="center", wrap_text=True)

    wb = openpyxl.Workbook()
    cabeceras = {}

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
        c = ws[ref]
        nombre = cabeceras.get(ws.title, {}).get(c.column_letter)
        v = previo["celdas"].get((ws.title, c.row, nombre), valor) if previo and nombre else valor
        return celda(ws, ref, v, f_input, formato, r_input, alinear)

    def cabecera(ws, fila, col0, textos, alto=36, relleno=r_cab):
        cabeceras.setdefault(ws.title, {})
        for k, t in enumerate(textos):
            letra = openpyxl.utils.get_column_letter(col0 + k)
            cabeceras[ws.title].setdefault(letra, t)
            celda(ws, f"{letra}{fila}", t, f_cab, relleno=relleno)
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

    # ---------------------------------------------------------------- producto de cada fila, por disciplina
    disciplinas = []
    for clave in ("canje", "formativas", "comercial"):
        for fila in datos[clave]:
            d = disciplina_de(fila[0])
            if d not in disciplinas:
                disciplinas.append(d)
    disciplinas.sort(key=lambda d: d == "Institucional")  # institucional al final
    por_base = {v[0]: k for k, v in PRODUCTOS.items()}  # nombres del formato anterior (sin disciplina)
    por_nombre_var = {nombre_producto(k, d): (d, k) for d in disciplinas for k in PRODUCTOS}
    asignado, usados = {}, set()
    for clave, _p, hoja, *_x in CATEGORIAS:
        for i, fila in enumerate(datos[clave]):
            d, k = disciplina_de(fila[0]), fila[5]
            v = previo["celdas"].get((hoja, 6 + i, "PRODUCTO PLAYMAKER")) if previo else None
            if v in por_nombre_var:
                d, k = por_nombre_var[v]
            elif v in por_base:
                k = por_base[v]
            asignado[(clave, i)] = (d, k)
            usados.add((d, k))
    lista_productos = [(d, k) for d in disciplinas for k in PRODUCTOS if (d, k) in usados]

    # ---------------------------------------------------------------- PRECIOS
    pr = wb.active
    pr.title = "PRECIOS"
    encabezado(pr, "LISTA DE PRECIOS 2027 POR DISCIPLINA", "Cada disciplina con sus productos. El precio público se "
                                                          "escribe una vez; cada categoría tiene su descuento general "
                                                          "(arriba) y un producto puede tener uno propio. Precios con "
                                                          "IVA, terminados en 900.")
    gen = previo["generales"] if previo else {}
    celda(pr, "B4", "IVA", f_tot, alinear=izq)
    celda(pr, "C4", gen.get("iva", IVA), f_input, "0%", r_input)
    fila_general = {}
    for i, (clave, _p, _h, titulo, desc, _e) in enumerate(CATEGORIAS):
        fila = 5 + i
        fila_general[clave] = fila
        celda(pr, f"B{fila}", f"Descuento {titulo.lower()}", f_tot, alinear=izq)
        v = gen.get(clave)
        celda(pr, f"C{fila}", v if v is not None else desc, f_input, "0%", r_input)
    celda(pr, "D5", "Canje: 100% de descuento (el club no paga). Se valoriza a precio público.", f_nota,
          alinear=Alignment(vertical="center"), borde=False)
    cab_precios = ["PRODUCTO", "LÍNEA", "PRECIO PÚBLICO (CON IVA)"]
    for clave, _p, _h, _t, _d, etq in CATEGORIAS:
        cab_precios += [f"DESCUENTO {etq}", f"PRECIO {etq}"]
    cab_precios += ["OBSERVACIONES"]
    cabecera(pr, 9, 2, cab_precios, alto=40)
    cabecera(pr, 9, 13, ["COSTO UNITARIO NETO (INTERNO)", "MARGEN FORMATIVAS Y CT (INTERNO)",
                         "MARGEN COMERCIAL (INTERNO)", "MARGEN PÚBLICO (INTERNO)",
                         "REFERENCIA DEL PRECIO (INTERNO)"], alto=40, relleno=r_int)
    col_desc = {"canje": "E", "formativas": "G", "comercial": "I"}
    col_precio = {"canje": "F", "formativas": "H", "comercial": "J"}
    fila_precio, r = {}, 10
    for disc in disciplinas:
        celda(pr, f"B{r}", TITULO_DISCIPLINA.get(disc, disc.upper()), Font(name="Calibri", size=10, bold=True,
              color=NAVY), relleno=r_sub, alinear=izq)
        for col in "CDEFGHIJK":
            celda(pr, f"{col}{r}", None, relleno=r_sub)
        r += 1
        for d, k in lista_productos:
            if d != disc:
                continue
            base, l, precio, ref, costo = PRODUCTOS[k]
            nombre = nombre_producto(k, d)
            fila_precio[(d, k)] = r
            # valores cargados: los de este producto o, del formato anterior, los del producto sin disciplina
            pv = (previo["precios"].get(nombre) or previo["precios"].get(base) or {}) if previo else {}
            celda(pr, f"B{r}", nombre, alinear=izq)
            celda(pr, f"C{r}", l, f_gris, alinear=izq)
            celda(pr, f"D{r}", pv.get("PRECIO PÚBLICO (CON IVA)", precio), f_input, PESOS, r_input)
            for clave, *_x in CATEGORIAS:
                cd, cp, etq = col_desc[clave], col_precio[clave], _x[-1]
                celda(pr, f"{cd}{r}", pv.get(f"DESCUENTO {etq}"), f_input, "0%", r_input)
                neto = f'N(D{r})*(1-IF({cd}{r}="",$C${fila_general[clave]},{cd}{r}))'
                celda(pr, f"{cp}{r}", f"=IF({neto}<=0,0,MAX(0,ROUND(({neto}-900)/1000,0)*1000+900))", f_tot, PESOS)
            celda(pr, f"K{r}", pv.get("OBSERVACIONES"), f_input, relleno=r_input, alinear=izq)
            celda(pr, f"Q{r}", pv.get("REFERENCIA DEL PRECIO (INTERNO)", ref), f_input, relleno=r_input, alinear=izq)
            celda(pr, f"M{r}", pv.get("COSTO UNITARIO NETO (INTERNO)", costo), f_input, PESOS, r_input)
            for col, cp in (("N", "H"), ("O", "J"), ("P", "D")):
                celda(pr, f"{col}{r}", f'=IF(OR(N({cp}{r})=0,N(M{r})=0),"",1-M{r}/({cp}{r}/(1+$C$4)))', formato=PCT)
            r += 1
    ultima_precio = r - 1
    for col, ancho in zip("BCDEFGHIJKLMNOPQ", (46, 14, 14, 12, 12, 13, 14, 12, 13, 28, 2, 15, 14, 14, 14, 34)):
        pr.column_dimensions[col].width = ancho
    pr.print_area = f"A1:K{ultima_precio}"
    dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                        errorTitle="Precio", error="Ingresa un valor en pesos (0 o más).")
    pr.add_data_validation(dv)
    dv.add(f"D10:D{ultima_precio}")
    dv.add(f"M10:M{ultima_precio}")
    dvp = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True,
                         errorTitle="Descuento", error="Ingresa un porcentaje entre 0% y 100%.")
    pr.add_data_validation(dvp)
    dvp.add("C5:C7")
    for clave in col_desc:
        dvp.add(f"{col_desc[clave]}10:{col_desc[clave]}{ultima_precio}")
    for col in "NOP":
        pr.conditional_formatting.add(f"{col}10:{col}{ultima_precio}", CellIsRule(
            operator="lessThan", formula=["0"], fill=PatternFill("solid", fgColor="F6D5D0")))
    nombres_rango = f"PRECIOS!$B$10:$B${ultima_precio}"

    def por_nombre(ref, col):
        return (f"IFERROR(N(INDEX(PRECIOS!${col}$10:${col}${ultima_precio},MATCH({ref},{nombres_rango},0))),0)")

    # ---------------------------------------------------------------- hojas por categoría
    detalle = {}  # clave -> (hoja, ramas [(rama, primera fila, última fila)], fila total)
    for clave, pestaña, hoja, titulo, _d, etq in CATEGORIAS:
        ws = wb.create_sheet(hoja)
        es_canje = clave == "canje"
        encabezado(ws, f"{titulo.upper()} 2027",
                   ("Todo en canje: el valor del canje es el valor a precio público menos lo que paga el club (con "
                    "100% de descuento, el club no paga)." if es_canje else
                    f"Precio {etq.lower()} de la hoja PRECIOS. CANTIDAD: la ajustada por el club (o la pedida si no "
                    "la ajustó).") + " Celdas amarillas editables.")
        cabecera(ws, 5, 2, ["RAMA", "TIPO", "PRENDA SOLICITADA", "MODELO", "COLOR", "PRODUCTO PLAYMAKER",
                            "CANTIDAD PEDIDA", "CANTIDAD", "PRECIO PÚBLICO", f"PRECIO {etq}",
                            "VALOR A PRECIO PÚBLICO", "VALOR A PAGAR", "VALOR DEL CANJE" if es_canje else
                            "DESCUENTO OTORGADO"])
        cabecera(ws, 5, 16, ["COSTO UNITARIO (INTERNO)", "COSTO TOTAL (INTERNO)"], relleno=r_int)
        dv_prod = DataValidation(type="list", formula1=f"={nombres_rango}", allow_blank=False,
                                 errorTitle="Producto", error="Elige un producto de la hoja PRECIOS.")
        dv_u = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                              errorTitle="Cantidad", error="Ingresa un número entero (0 o más).")
        r, ramas, rama_actual, f0 = 6, [], None, None
        filas = datos[clave]
        for i, (rama, tipo, prenda, modelo, color, k, pedida, cant) in enumerate(filas):
            if rama != rama_actual:
                if rama_actual is not None:
                    ramas.append((rama_actual, f0, r - 1))
                rama_actual, f0 = rama, r
            primera = r == f0
            celda(ws, f"B{r}", rama, f_tot if primera else f_gris, alinear=izq)
            celda(ws, f"C{r}", tipo, f_gris, alinear=izq)
            celda(ws, f"D{r}", prenda, alinear=izq)
            celda(ws, f"E{r}", modelo or None, f_gris, alinear=izq)
            celda(ws, f"F{r}", color, f_gris, alinear=izq)
            d_, k_ = asignado[(clave, i)]
            celda(ws, f"G{r}", nombre_producto(k_, d_), f_input, relleno=r_input, alinear=izq)
            celda(ws, f"H{r}", pedida, f_gris, NUM)
            entrada(ws, f"I{r}", cant, NUM)
            celda(ws, f"J{r}", "=" + por_nombre(f"G{r}", "D"), f_gris, PESOS)
            celda(ws, f"K{r}", "=" + por_nombre(f"G{r}", col_precio[clave]), formato=PESOS)
            celda(ws, f"L{r}", f"=N(I{r})*J{r}", formato=PESOS)
            celda(ws, f"M{r}", f"=N(I{r})*K{r}", f_tot, PESOS)
            celda(ws, f"N{r}", f"=L{r}-M{r}", f_tot if es_canje else f_norm, PESOS)
            celda(ws, f"P{r}", "=" + por_nombre(f"G{r}", "M"), f_gris, PESOS)
            celda(ws, f"Q{r}", f"=N(I{r})*P{r}", formato=PESOS)
            r += 1
        ramas.append((rama_actual, f0, r - 1))
        dv_prod.add(f"G6:G{r - 1}")
        dv_u.add(f"I6:I{r - 1}")
        ws.add_data_validation(dv_prod)
        ws.add_data_validation(dv_u)
        celda(ws, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
        for col in "CDEFGJK":
            celda(ws, f"{col}{r}", None, f_gran, relleno=r_gran)
        for col, fmt in (("H", NUM), ("I", NUM), ("L", PESOS), ("M", PESOS), ("N", PESOS)):
            celda(ws, f"{col}{r}", f"=SUM({col}6:{col}{r - 1})", f_gran, fmt, r_gran)
        celda(ws, f"P{r}", None, relleno=r_int)
        celda(ws, f"Q{r}", f"=SUM(Q6:Q{r - 1})", f_gran, PESOS, r_int)
        ws.row_dimensions[r].height = 20
        tot = r
        # separación visual entre ramas
        for _rama, a, _b in ramas[1:]:
            for col in "BCDEFGHIJKLMN":
                ws[f"{col}{a}"].border = Border(left=fino, right=fino, bottom=fino,
                                                top=Side(style="medium", color=NAVY))
        for col, ancho in zip("BCDEFGHIJKLMNOPQ", (15, 14, 30, 11, 13, 44, 10, 10, 12, 13, 14, 14, 14, 2, 13, 14)):
            ws.column_dimensions[col].width = ancho
        ws.freeze_panes = "D6"
        ws.print_area = f"A1:N{tot}"
        # totales internos a la derecha
        celda(ws, "S4", "TOTALES (USO INTERNO, NO SE IMPRIME)", Font(name="Calibri", size=10, bold=True, color="C00000"),
              alinear=izq, borde=False)
        cabecera(ws, 5, 19, ["CONCEPTO", "VALOR"], relleno=r_int)
        filas_int = ([("Valor del canje (precio público, con IVA)", f"=N{tot}"), ("Costo del canje (neto)", f"=Q{tot}")]
                     if es_canje else
                     [("Ventas (con IVA)", f"=M{tot}"), ("Ventas netas (sin IVA)", f"=ROUND(M{tot}/(1+PRECIOS!$C$4),0)"),
                      ("Costo (neto)", f"=Q{tot}"), ("Margen", "=T7-T8"),
                      ("Margen %", '=IF(T7=0,"",T9/T7)')])
        for i, (txt, f) in enumerate(filas_int):
            celda(ws, f"S{6 + i}", txt, f_tot, relleno=r_int_suave, alinear=izq)
            celda(ws, f"T{6 + i}", f, f_tot, PCT if txt == "Margen %" else PESOS)
        ws.column_dimensions["S"].width = 36
        ws.column_dimensions["T"].width = 15
        detalle[clave] = (hoja, ramas, tot)

    # ---------------------------------------------------------------- RESUMEN
    rs = wb.create_sheet("RESUMEN", 0)
    encabezado(rs, "PROPUESTA COMERCIAL 2027: RAMAS DEPORTIVAS CSD COLO-COLO",
               "Valores con IVA. Canje de los primeros equipos valorizado a precio público; ventas de formativas, "
               "cuerpo técnico y stock comercial a su precio de la hoja PRECIOS.")
    cabecera(rs, 5, 2, ["CATEGORÍA", "RAMA", "UNIDADES", "VALOR DEL CANJE (PRECIO PÚBLICO)", "VENTAS (CON IVA)",
                        "NETO VENTAS", "IVA VENTAS"], alto=40)
    r, filas_total = 6, []

    def fila_resumen(r, cat, rama, unid, canje, ventas, fuente=f_norm, relleno=None):
        celda(rs, f"B{r}", cat, fuente, relleno=relleno, alinear=izq)
        celda(rs, f"C{r}", rama, fuente, relleno=relleno, alinear=izq)
        celda(rs, f"D{r}", unid, fuente, NUM, relleno)
        celda(rs, f"E{r}", canje, fuente if relleno else f_tot, PESOS, relleno)
        celda(rs, f"F{r}", ventas, fuente if relleno else f_tot, PESOS, relleno)
        celda(rs, f"G{r}", f"=ROUND(F{r}/(1+PRECIOS!$C$4),0)", fuente, PESOS, relleno)
        celda(rs, f"H{r}", f"=F{r}-G{r}", fuente, PESOS, relleno)

    for clave, _p, hoja, titulo, _d, _e in CATEGORIAS:
        _h, ramas, tot = detalle[clave]
        H = f"'{hoja}'"
        r0 = r
        for k, (rama, a, b) in enumerate(ramas):
            fila_resumen(r, titulo if k == 0 else None, rama, f"=SUM({H}!I{a}:I{b})",
                         f"=SUM({H}!N{a}:N{b})" if clave == "canje" else 0, f"=SUM({H}!M{a}:M{b})")
            r += 1
        fila_resumen(r, f"Total {titulo.split(' (')[0].lower()}", None, *[f"=SUM({c}{r0}:{c}{r - 1})" for c in "DEF"],
                     fuente=f_tot, relleno=r_sub)
        filas_total.append(r)
        r += 1
    fila_resumen(r, "TOTAL PROPUESTA", None, *["=" + "+".join(f"{c}{x}" for x in filas_total) for c in "DEF"],
                 fuente=f_gran, relleno=r_gran)
    rs.row_dimensions[r].height = 22
    total_general = r

    r += 4
    celda(rs, f"B{r}", "VALOR POR PRODUCTO", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    cabecera(rs, r, 2, ["PRODUCTO", "PRECIO PÚBLICO", "PRECIO FORMATIVAS Y CT", "PRECIO COMERCIAL",
                        "UNIDADES CANJE", "UNIDADES FORMATIVAS Y CT", "UNIDADES COMERCIAL",
                        "VALOR DEL CANJE (PRECIO PÚBLICO)", "VENTAS (CON IVA)"], alto=40)
    r += 1
    p0 = r
    fila_producto = {}
    hojas = {clave: f"'{detalle[clave][0]}'" for clave in col_precio}
    disc_actual = None
    for d, k in lista_productos:
        if d != disc_actual:
            disc_actual = d
            celda(rs, f"B{r}", TITULO_DISCIPLINA.get(d, d.upper()), Font(name="Calibri", size=10, bold=True,
                  color=NAVY), relleno=r_sub, alinear=izq)
            for col in "CDEFGHIJ":
                celda(rs, f"{col}{r}", None, relleno=r_sub)
            r += 1
        nombre = nombre_producto(k, d)
        fp = fila_precio[(d, k)]
        fila_producto[(d, k)] = r
        celda(rs, f"B{r}", nombre, alinear=izq)
        celda(rs, f"C{r}", f"=PRECIOS!D{fp}", f_gris, PESOS)
        celda(rs, f"D{r}", f"=PRECIOS!H{fp}", formato=PESOS)
        celda(rs, f"E{r}", f"=PRECIOS!J{fp}", formato=PESOS)
        for col, clave in (("F", "canje"), ("G", "formativas"), ("H", "comercial")):
            h = hojas[clave]
            celda(rs, f"{col}{r}", f'=SUMIF({h}!$G:$G,"{nombre}",{h}!$I:$I)', formato=NUM)
        h = hojas["canje"]
        celda(rs, f"I{r}", f'=SUMIF({h}!$G:$G,"{nombre}",{h}!$N:$N)', f_tot, PESOS)
        celda(rs, f"J{r}", "=" + "+".join(f'SUMIF({hojas[c]}!$G:$G,"{nombre}",{hojas[c]}!$M:$M)' for c in col_precio),
              f_tot, PESOS)
        r += 1
    celda(rs, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    for col in "CDE":
        celda(rs, f"{col}{r}", None, f_gran, relleno=r_gran)
    for col, fmt in (("F", NUM), ("G", NUM), ("H", NUM), ("I", PESOS), ("J", PESOS)):
        celda(rs, f"{col}{r}", f"=SUM({col}{p0}:{col}{r - 1})", f_gran, fmt, r_gran)
    tg = total_general
    celda(rs, f"B{r + 1}", f'=IF(AND(I{r}=E{tg},J{r}=F{tg},F{r}+G{r}+H{r}=D{tg}),"Control: la suma por producto '
                           f'coincide con el total de la propuesta.","Revisar: la suma por producto no coincide con el '
                           f'total.")', f_nota, alinear=Alignment(vertical="center"), borde=False)
    for col, ancho in zip("BCDEFGHIJ", (46, 30, 13, 15, 15, 13, 14, 14, 17)):
        rs.column_dimensions[col].width = ancho
    rs.column_dimensions["J"].width = 17
    rs.print_area = f"A1:J{r + 1}"

    # vínculo que genera el PDF para el club (macro GenerarPDFClub vía Workbook_SheetFollowHyperlink)
    celda(rs, "L2", "GENERAR PDF PARA EL CLUB", Font(name="Calibri", size=11, bold=True, color="FFFFFF",
                                                       underline="single"), relleno=r_gran)
    for col in "LMN":
        for fila in (2, 3):
            rs[f"{col}{fila}"].fill = r_gran
    rs.merge_cells("L2:N3")
    rs["L2"].hyperlink = Hyperlink(ref="L2", location="RESUMEN!L2",
                                   tooltip="Generar PDF para el club (todas las hojas menos COSTOS)")
    celda(rs, "L4", "Exporta todas las hojas menos COSTOS a un PDF en la misma carpeta de esta planilla.", f_nota,
          alinear=Alignment(vertical="top", wrap_text=True), borde=False)
    rs.merge_cells("L4:N5")
    celda(rs, "L6", "Requiere habilitar macros. Si no funciona: Archivo, Exportar, PDF, con todas las hojas menos "
                    "COSTOS seleccionadas.", f_nota, alinear=Alignment(vertical="top", wrap_text=True), borde=False)
    rs.merge_cells("L6:N9")
    for col in "LMN":
        rs.column_dimensions[col].width = 14

    # ---------------------------------------------------------------- COSTOS (uso interno)
    co = wb.create_sheet(HOJA_INTERNA)
    co.sheet_properties.tabColor = "C00000"
    encabezado(co, "COSTOS DE LA PROPUESTA (USO INTERNO, NO VA EN EL PDF)",
               "El costo unitario se escribe en la hoja PRECIOS (columna COSTO UNITARIO NETO). Unidades y ventas vienen "
               "de las demás hojas.")
    cabecera(co, 5, 2, ["PRODUCTO", "COSTO UNITARIO NETO", "UNIDADES CANJE", "UNIDADES VENDIDAS", "TOTAL UNIDADES",
                        "COSTO DEL CANJE", "COSTO DE LO VENDIDO", "COSTO TOTAL (INVENTARIO)", "VENTA NETA",
                        "MARGEN DE LA VENTA", "MARGEN %"], alto=40)
    r = 6
    c0 = r
    disc_actual = None
    for d, k in lista_productos:
        if d != disc_actual:
            disc_actual = d
            celda(co, f"B{r}", TITULO_DISCIPLINA.get(d, d.upper()), Font(name="Calibri", size=10, bold=True,
                  color=NAVY), relleno=r_sub, alinear=izq)
            for col in "CDEFGHIJKL":
                celda(co, f"{col}{r}", None, relleno=r_sub)
            r += 1
        fr = fila_producto[(d, k)]
        celda(co, f"B{r}", nombre_producto(k, d), alinear=izq)
        celda(co, f"C{r}", f"=N(PRECIOS!M{fila_precio[(d, k)]})", formato=PESOS)
        celda(co, f"D{r}", f"=RESUMEN!F{fr}", formato=NUM)
        celda(co, f"E{r}", f"=RESUMEN!G{fr}+RESUMEN!H{fr}", formato=NUM)
        celda(co, f"F{r}", f"=D{r}+E{r}", formato=NUM)
        celda(co, f"G{r}", f"=D{r}*C{r}", formato=PESOS)
        celda(co, f"H{r}", f"=E{r}*C{r}", formato=PESOS)
        celda(co, f"I{r}", f"=G{r}+H{r}", f_tot, PESOS)
        celda(co, f"J{r}", f"=ROUND(RESUMEN!J{fr}/(1+PRECIOS!$C$4),0)", formato=PESOS)
        celda(co, f"K{r}", f"=J{r}-H{r}", f_tot, PESOS)
        celda(co, f"L{r}", f'=IF(OR(J{r}=0,C{r}=0),"",K{r}/J{r})', formato=PCT)
        r += 1
    celda(co, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    celda(co, f"C{r}", None, f_gran, relleno=r_gran)
    for col in "DEFGHIJK":
        celda(co, f"{col}{r}", f"=SUM({col}{c0}:{col}{r - 1})", f_gran, NUM if col in "DEF" else PESOS, r_gran)
    celda(co, f"L{r}", f'=IF(J{r}=0,"",K{r}/J{r})', f_gran, PCT, r_gran)
    tc = r
    r += 3
    celda(co, f"B{r}", "RESULTADO DE LA PROPUESTA", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    can, fo_, com = (f"'{detalle[c][0]}'" for c in ("canje", "formativas", "comercial"))
    tcan, tfo, tcom = (detalle[c][2] for c in ("canje", "formativas", "comercial"))
    for txt, f, fuente in [
        ("Valor del canje para el club (precio público, con IVA)", f"={can}!N{tcan}", f_norm),
        ("Costo del canje (neto)", f"=G{tc}", f_norm),
        ("Ventas formativas y cuerpo técnico (con IVA)", f"={fo_}!M{tfo}", f_norm),
        ("Ventas comercial (con IVA)", f"={com}!M{tcom}", f_norm),
        ("Ventas netas (sin IVA)", f"=J{tc}", f_norm),
        ("Costo de lo vendido (neto)", f"=H{tc}", f_norm),
        ("Margen de la venta", f"=K{tc}", f_tot),
        ("Resultado (margen de la venta menos costo del canje)", f"=K{tc}-G{tc}", f_tot),
        ("Costo total a producir (canje y venta)", f"=I{tc}", f_tot),
    ]:
        celda(co, f"B{r}", txt, fuente, alinear=izq)
        for col in "CDEF":
            celda(co, f"{col}{r}", None)
        co.merge_cells(f"B{r}:F{r}")
        celda(co, f"G{r}", f, fuente, PESOS, r_sub if fuente is f_tot else None)
        if txt.startswith("Resultado"):
            co.conditional_formatting.add(f"G{r}", CellIsRule(operator="lessThan", formula=["0"],
                                                              fill=PatternFill("solid", fgColor="F6D5D0")))
        r += 1
    celda(co, f"B{r + 1}", "Si falta el costo de un producto, sus costos quedan en cero: completa la columna COSTO "
                           "UNITARIO NETO en la hoja PRECIOS.", f_nota, alinear=Alignment(vertical="center"), borde=False)
    for col, ancho in zip("BCDEFGHIJKL", (46, 13, 12, 12, 12, 15, 15, 16, 15, 15, 10)):
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
    resumen = ", ".join(f"{c}: {len(datos[c])} filas" for c in datos)
    print(f"OK  {SALIDA.name}  ({resumen})")


if __name__ == "__main__":
    main()
