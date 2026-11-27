"""Propuesta comercial 2027 para las ramas deportivas del CSD Colo-Colo, en Excel con macros.

Uso:
    python3 propuestas/colo-colo/generar_propuesta_excel.py

Lee el requerimiento del club (Requerimiento_Indumentaria_2027_CSD_Colo_Colo.xlsx: pestañas CANJE 1EROS EQUIPOS,
FORMATIVAS y COMERCIAL) y crea Propuesta_Comercial_CSD_Colo_Colo_2027.xlsm, con el formato de la valorización
FEVOCHI y de Los Leones:
  - PRECIOS: por disciplina (básquetbol, futsal, vóleibol, patín, Esperanza Alba e institucional), cada producto
    con su precio (la camiseta de juego de básquetbol es distinta de la de futsal o la de vóleibol). Por producto se
    escribe una vez el valor formativas y cuerpo técnico: es lo que paga el club por las escuelas formativas y el
    cuerpo técnico, y el valor con que se calcula el canje (100% de descuento). El precio comercial de la tienda sale
    de ese valor con un descuento general (un producto puede tener uno propio), terminado en 900. Los descuentos, el
    costo unitario neto y los márgenes quedan fuera de lo que se imprime.
  - CANJE PRIMEROS EQUIPOS, FORMATIVAS Y CT, COMERCIAL: lo pedido por el club, por rama, con el producto
    Playmaker (lista desplegable), cantidades, valor formativas y CT, precio de la categoría y valor a pagar (en el
    canje, el valor del canje). Columnas internas de costo fuera de lo que se imprime.
  - RESUMEN: por categoría y rama, valor del canje y ventas (neto e IVA); valor por producto. Vínculo GENERAR PDF
    PARA EL CLUB (macro): exporta todas las hojas menos COSTOS y RESUMEN NEGOCIO.
  - ENTREGAS 2027: tres entregas (equipos de marzo, stock de la tienda de marzo y agosto), la entrega de cada rama por
    categoría, prendas, canje y compras por entrega, cronograma con fechas editables (contrato y orden de compra,
    diseños, muestras y tallas, producción, despacho y entrega) con control interno de la capacidad del taller externo,
    y el canje proporcional a las compras (proporción, diferencia por entrega y simulación).
  - RESUMEN NEGOCIO (uso interno): resultado del negocio por disciplina o rama: venta neta de formativas y cuerpo
    técnico y del stock comercial, costo de lo vendido y margen, canje de los primeros equipos (a valor formativas y CT
    y a costo) y margen total, con un supuesto de otros costos (% de la venta) y el punto de equilibrio.
  - COSTOS (uso interno): costo y margen por producto y resultado de la propuesta.
En formativas y comercial se usa la cantidad ajustada del club (Q ADAPTADA o Q MODIFICADA); si la dejó en blanco,
queda en 0, igual que en los totales de su planilla (esas filas se marcan para revisarlas). Si la planilla ya existe, se conservan los precios, descuentos, costos y cantidades cargados,
y las celdas que el usuario haya agregado debajo o a la derecha de las tablas.
"""

import re
import sys
from datetime import datetime
from pathlib import Path

import openpyxl
import openpyxl.utils
from openpyxl.drawing.image import Image as XLImage
from openpyxl.formatting.rule import CellIsRule, FormulaRule
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
HOJA_NEGOCIO = "RESUMEN NEGOCIO"  # uso interno, no va en el PDF
HOJA_ENTREGAS = "ENTREGAS 2027"
# entregas del año (nombre, fecha por defecto). La entrega de cada rama se elige por categoría (primer equipo, formativas
# y cuerpo técnico, comercial): las ramas de marzo reciben sus equipos el 1 de marzo y el stock de la tienda el 22 de
# marzo (la capacidad del taller no alcanza para todo el 1 de marzo); vóleibol y patín, todo en agosto.
ENTREGAS = [("MARZO EQUIPOS", datetime(2027, 3, 1)), ("MARZO TIENDA", datetime(2027, 3, 22)),
            ("AGOSTO", datetime(2027, 8, 2))]
CATEGORIAS_ENTREGA = [("canje", "PRIMER EQUIPO"), ("formativas", "FORMATIVAS Y CT"), ("comercial", "COMERCIAL")]
ENTREGA_DEFECTO = {"canje": "MARZO EQUIPOS", "formativas": "MARZO EQUIPOS", "comercial": "MARZO TIENDA"}
ENTREGA_RAMA = {"Vóleibol": "AGOSTO", "Patín": "AGOSTO"}  # estas ramas, todo en agosto
PARAMETROS_ENTREGA = [  # parámetros internos del cronograma: clave, texto, valor por defecto
    ("capacidad", "Capacidad de producción del taller externo (prendas por mes)", 3000),
]
# hitos del cronograma: texto, detalle, fecha por defecto de cada entrega (None: la fecha de la entrega). Primero el
# contrato y la orden de compra (una vez aprobado el presupuesto); después diseños, muestras, tallas y producción.
HITOS = [
    ("Contrato y orden de compra", "Una vez aprobado el presupuesto: firma del contrato y orden de compra con el abono de "
     "la parte del pedido de cada entrega.", datetime(2026, 12, 9), datetime(2026, 12, 9), datetime(2027, 5, 10)),
    ("Aprobación de diseños", "El club aprueba los diseños de juego, entrenamiento y presentación de cada rama.",
     datetime(2026, 12, 15), datetime(2026, 12, 15), datetime(2027, 5, 17)),
    ("Entrega de muestras", "Playmaker entrega muestras de cada prenda para el visto bueno del club.",
     datetime(2026, 12, 22), datetime(2026, 12, 22), datetime(2027, 5, 24)),
    ("Visto bueno de muestras y curva de tallas", "El club aprueba las muestras y entrega las tallas por rama y "
     "categoría; la producción se fabrica según las muestras aprobadas.", datetime(2026, 12, 29), datetime(2026, 12, 29),
     datetime(2027, 5, 31)),
    ("Inicio de producción", "Producción con supervisión y control de calidad de Playmaker.", datetime(2027, 1, 4),
     datetime(2027, 2, 25), datetime(2027, 6, 14)),
    ("Control de calidad y despacho", "Revisión, etiquetado por rama y categoría, y despacho.", datetime(2027, 2, 25),
     datetime(2027, 3, 16), datetime(2027, 7, 26)),
    ("Entrega en el club", "Toda la indumentaria de esta entrega.", None, None, None),
]

# categorías: clave, pestaña del requerimiento, hoja de la propuesta, título, descuento general, etiqueta del precio
CATEGORIAS = [
    ("canje", "CANJE 1EROS EQUIPOS", "CANJE PRIMEROS EQUIPOS", "Canje primeros equipos", None, "CANJE"),
    ("formativas", "FORMATIVAS", "FORMATIVAS Y CT", "Formativas y cuerpo técnico", None, "FORMATIVAS Y CT"),
    ("comercial", "COMERCIAL", "COMERCIAL", "Comercial (stock para la tienda)", None, "COMERCIAL"),
]

# precios: el valor formativas y cuerpo técnico (con IVA) es la base; el canje se valoriza a ese valor y el precio
# comercial de la tienda sale de él con un descuento (interno: no se muestra al club)
COL_BASE_PRECIO = "VALOR FORMATIVAS Y CUERPO TÉCNICO (CON IVA)"
COL_DESC_COMERCIAL = "DESCUENTO COMERCIAL (INTERNO, OPCIONAL)"
DESCUENTOS = {"canje": 1.00, "comercial": 0.10}  # descuentos generales por defecto sobre el valor formativas y CT
# producto: (nombre, línea, valor formativas y CT de referencia con IVA, referencia del precio,
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

MACRO_PDF = """' Genera el PDF de la propuesta para el club: todas las hojas visibles menos las internas (COSTOS y
' RESUMEN NEGOCIO).
Sub GenerarPDFClub()
    Dim hojas() As Variant, n As Integer, ws As Worksheet, ruta As String, activa As Worksheet
    Set activa = ActiveSheet
    For Each ws In ThisWorkbook.Worksheets
        If ws.Name <> "COSTOS" And InStr(1, ws.Name, "NEGOCIO", vbTextCompare) = 0 And ws.Visible = xlSheetVisible Then
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
    """Por categoría: [(rama, tipo, prenda, modelo, color, producto, cantidad pedida, cantidad ajustada, sin ajuste)].
    sin ajuste: el club dejó en blanco la cantidad ajustada (cuenta como 0, como en los totales de su planilla)."""
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
            ajustada = h if isinstance(h, (int, float)) else 0
            sin_ajuste = clave != "canje" and not isinstance(h, (int, float)) and pedida > 0
            prenda = texto(d).replace("ò", "ó").replace("à", "á")
            filas.append((rama, tipo, prenda[0].upper() + prenda[1:], texto(ws.cell(r, 5).value).capitalize(),
                          texto(ws.cell(r, 6).value), k, pedida, ajustada if clave != "canje" else pedida,
                          sin_ajuste))
        datos[clave] = filas
    return datos


def leer_previo():
    if not SALIDA.exists():
        return None
    wb = openpyxl.load_workbook(SALIDA)
    azul = lambda c: c.font is not None and c.font.color is not None and str(c.font.color.rgb)[-6:] == "0000FF"  # noqa: E731
    previo = {"precios": {}, "generales": {}, "celdas": {}, "supuestos": {}, "extras": {}, "entregas": {}}
    pr = wb["PRECIOS"]
    for r in range(4, 9):
        for c_etq, c_val in ((2, 3), (8, 12)):
            etq = texto(pr.cell(r, c_etq).value).lower()
            if not etq or pr.cell(r, c_val).value is None:
                continue
            for clave in ("canje", "comercial", "formativas"):
                if etq.startswith("descuento") and clave in etq.split(" (")[0]:
                    previo["generales"][clave] = pr.cell(r, c_val).value
            if etq == "iva":
                previo["generales"]["iva"] = pr.cell(r, c_val).value
    cab = next(r for r in range(1, 15) if texto(pr.cell(r, 2).value) == "PRODUCTO")
    cols = {texto(pr.cell(cab, c).value): c for c in range(2, pr.max_column + 1)}
    for r in range(cab + 1, pr.max_row + 1):
        if pr.cell(r, 2).value and azul(pr.cell(r, 4)):
            previo["precios"][texto(pr.cell(r, 2).value)] = {t: pr.cell(r, c).value for t, c in cols.items()}
    if HOJA_NEGOCIO in wb.sheetnames:
        sn = wb[HOJA_NEGOCIO]
        for r in range(4, 8):
            if sn.cell(r, 2).value and azul(sn.cell(r, 3)):
                previo["supuestos"][texto(sn.cell(r, 2).value)] = sn.cell(r, 3).value
    if HOJA_ENTREGAS in wb.sheetnames:
        en = wb[HOJA_ENTREGAS]
        modo, entregas_col = None, {}
        for r in range(1, en.max_row + 1):
            b = texto(en.cell(r, 2).value)
            if b in ("RAMA", "HITO"):
                modo = b
                if b == "HITO":  # columnas de fechas: "ENTREGA n: NOMBRE" (se guarda por nombre de la entrega)
                    entregas_col = {c: texto(en.cell(r, c).value).split(": ", 1)[-1] for c in range(3, 8)
                                    if texto(en.cell(r, c).value).startswith("ENTREGA ")}
            elif b == "TOTAL" or (modo == "HITO" and not b):
                modo = None
            elif modo == "HITO":
                for c, nombre_e in entregas_col.items():
                    if azul(en.cell(r, c)):
                        previo["entregas"][f"hito:{b}:{nombre_e}"] = en.cell(r, c).value
            elif modo == "RAMA":
                for c in range(3, 3 + len(CATEGORIAS_ENTREGA)):
                    if azul(en.cell(r, c)):
                        previo["entregas"][f"rama:{b}:{c}"] = en.cell(r, c).value
            elif b and azul(en.cell(r, 3)):
                previo["entregas"][b] = en.cell(r, 3).value
            for c_etq in (13, 14):  # parámetros internos (M/N en el formato anterior, N/O ahora)
                if en.cell(r, c_etq).value and azul(en.cell(r, c_etq + 1)):
                    previo["entregas"][texto(en.cell(r, c_etq).value)] = en.cell(r, c_etq + 1).value
    for hoja in ["RESUMEN", HOJA_ENTREGAS] + [c[2] for c in CATEGORIAS]:
        if hoja in wb.sheetnames:
            previo["extras"][hoja] = [(c.row, c.column, c.value, c.number_format, bool(c.font and c.font.b))
                                      for row in wb[hoja].iter_rows() for c in row if c.value is not None]
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
    encabezado(pr, "LISTA DE PRECIOS 2027 POR DISCIPLINA", "Cada disciplina con sus productos. El valor formativas y cuerpo "
                                                          "técnico se escribe una vez: es lo que paga el club por las "
                                                          "escuelas formativas y el cuerpo técnico, y el valor del canje. "
                                                          "Precios con IVA, terminados en 900.")
    gen = previo["generales"] if previo else {}
    celda(pr, "B4", "IVA", f_tot, alinear=izq)
    celda(pr, "C4", gen.get("iva", IVA), f_input, "0%", r_input)
    # descuentos generales (internos, fuera de lo que se imprime): canje y precio comercial de la tienda
    celda(pr, "H4", "PARÁMETROS (USO INTERNO, NO SE IMPRIME)", Font(name="Calibri", size=10, bold=True, color="C00000"),
          alinear=izq, borde=False)
    ref_general = {}
    for i, (clave, texto_gen) in enumerate((("canje", "Descuento canje primeros equipos (sobre el valor formativas y CT)"),
                                            ("comercial", "Descuento precio comercial tienda (sobre el valor formativas y CT)"))):
        fila = 5 + i
        celda(pr, f"H{fila}", texto_gen, f_tot, alinear=Alignment(vertical="center"), borde=False)
        v = gen.get(clave)
        celda(pr, f"L{fila}", v if v is not None else DESCUENTOS[clave], f_input, "0%", r_input)
        ref_general[clave] = f"$L${fila}"
    cabecera(pr, 9, 2, ["PRODUCTO", "LÍNEA", COL_BASE_PRECIO, "PRECIO COMERCIAL TIENDA (CON IVA)", "OBSERVACIONES"],
             alto=40)
    cabecera(pr, 9, 8, [COL_DESC_COMERCIAL, "PRECIO CANJE (INTERNO)", "COSTO UNITARIO NETO (INTERNO)",
                        "MARGEN FORMATIVAS Y CT (INTERNO)", "MARGEN COMERCIAL (INTERNO)", "REFERENCIA DEL PRECIO (INTERNO)"],
             alto=40, relleno=r_int)
    col_precio = {"canje": "I", "formativas": "D", "comercial": "E"}

    def redondeo(neto):
        return f"IF({neto}<=0,0,MAX(0,ROUND(({neto}-900)/1000,0)*1000+900))"

    fila_precio, r = {}, 10
    for disc in disciplinas:
        celda(pr, f"B{r}", TITULO_DISCIPLINA.get(disc, disc.upper()), Font(name="Calibri", size=10, bold=True,
              color=NAVY), relleno=r_sub, alinear=izq)
        for col in "CDEF":
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
            valor = pv.get(COL_BASE_PRECIO)
            if valor is None and pv.get("PRECIO PÚBLICO (CON IVA)") is not None:  # formato anterior: público y descuento
                d_fo = pv.get("DESCUENTO FORMATIVAS Y CT")
                d_fo = gen.get("formativas", 0) if d_fo is None else d_fo
                pub = pv["PRECIO PÚBLICO (CON IVA)"]
                valor = pub if not d_fo else max(0, round((pub * (1 - d_fo) - 900) / 1000) * 1000 + 900)
            celda(pr, f"B{r}", nombre, alinear=izq)
            celda(pr, f"C{r}", l, f_gris, alinear=izq)
            celda(pr, f"D{r}", precio if valor is None else valor, f_input, PESOS, r_input)
            d_co = pv.get(COL_DESC_COMERCIAL, pv.get("DESCUENTO COMERCIAL"))
            celda(pr, f"H{r}", d_co, f_input, "0%", r_input)
            celda(pr, f"E{r}", "=" + redondeo(f'N(D{r})*(1-IF(H{r}="",{ref_general["comercial"]},H{r}))'), f_tot, PESOS)
            celda(pr, f"I{r}", "=" + redondeo(f'N(D{r})*(1-{ref_general["canje"]})'), f_gris, PESOS)
            celda(pr, f"F{r}", pv.get("OBSERVACIONES"), f_input, relleno=r_input, alinear=izq)
            celda(pr, f"J{r}", pv.get("COSTO UNITARIO NETO (INTERNO)", costo), f_input, PESOS, r_input)
            for col, cp in (("K", "D"), ("L", "E")):
                celda(pr, f"{col}{r}", f'=IF(OR(N({cp}{r})=0,N(J{r})=0),"",1-J{r}/({cp}{r}/(1+$C$4)))', formato=PCT)
            celda(pr, f"M{r}", pv.get("REFERENCIA DEL PRECIO (INTERNO)", ref), f_input, relleno=r_input, alinear=izq)
            r += 1
    ultima_precio = r - 1
    for col, ancho in zip("BCDEFGHIJKLM", (46, 14, 18, 18, 30, 2, 14, 13, 15, 14, 14, 34)):
        pr.column_dimensions[col].width = ancho
    pr.print_area = f"A1:F{ultima_precio}"
    dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                        errorTitle="Precio", error="Ingresa un valor en pesos (0 o más).")
    pr.add_data_validation(dv)
    dv.add(f"D10:D{ultima_precio}")
    dv.add(f"J10:J{ultima_precio}")
    dvp = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True,
                         errorTitle="Descuento", error="Ingresa un porcentaje entre 0% y 100%.")
    pr.add_data_validation(dvp)
    dvp.add("L5:L6")
    dvp.add(f"H10:H{ultima_precio}")
    for col in "KL":
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
                   ("Todo en canje (100% de descuento, el club no paga): se valoriza a valor formativas y cuerpo "
                    "técnico." if es_canje else
                    ("Valor formativas y cuerpo técnico" if clave == "formativas" else "Precio comercial para la tienda")
                    + " de la hoja PRECIOS. CANTIDAD: la ajustada por el club (si la dejó en blanco, 0, como en sus "
                    "totales; esas filas quedan marcadas).") + " Celdas amarillas editables.")
        cabecera(ws, 5, 2, ["RAMA", "TIPO", "PRENDA SOLICITADA", "MODELO", "COLOR", "PRODUCTO PLAYMAKER",
                            "CANTIDAD PEDIDA", "CANTIDAD", "VALOR FORMATIVAS Y CT",
                            {"canje": "PRECIO CANJE", "formativas": "PRECIO A PAGAR", "comercial": "PRECIO COMERCIAL"}[clave],
                            "TOTAL A VALOR FORMATIVAS Y CT", "VALOR A PAGAR"] + (["VALOR DEL CANJE"] if es_canje else []))
        cabecera(ws, 5, 16, ["COSTO UNITARIO (INTERNO)", "COSTO TOTAL (INTERNO)"], relleno=r_int)
        dv_prod = DataValidation(type="list", formula1=f"={nombres_rango}", allow_blank=False,
                                 errorTitle="Producto", error="Elige un producto de la hoja PRECIOS.")
        dv_u = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                              errorTitle="Cantidad", error="Ingresa un número entero (0 o más).")
        r, ramas, rama_actual, f0 = 6, [], None, None
        filas = datos[clave]
        for i, (rama, tipo, prenda, modelo, color, k, pedida, cant, sin_ajuste) in enumerate(filas):
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
            v_prev = previo["celdas"].get((hoja, r, "CANTIDAD")) if previo else None
            if sin_ajuste and v_prev == pedida:  # el formato anterior ponía la pedida: pasa a 0 como en el club
                celda(ws, f"I{r}", cant, f_input, NUM, r_input)
            else:
                entrada(ws, f"I{r}", cant, NUM)
            celda(ws, f"J{r}", "=" + por_nombre(f"G{r}", "D"), f_gris, PESOS)
            celda(ws, f"K{r}", "=" + por_nombre(f"G{r}", col_precio[clave]), formato=PESOS)
            celda(ws, f"L{r}", f"=N(I{r})*J{r}", formato=PESOS)
            celda(ws, f"M{r}", f"=N(I{r})*K{r}", f_tot, PESOS)
            if es_canje:
                celda(ws, f"N{r}", f"=L{r}-M{r}", f_tot, PESOS)
            celda(ws, f"P{r}", "=" + por_nombre(f"G{r}", "J"), f_gris, PESOS)
            celda(ws, f"Q{r}", f"=N(I{r})*P{r}", formato=PESOS)
            r += 1
        ramas.append((rama_actual, f0, r - 1))
        dv_prod.add(f"G6:G{r - 1}")
        dv_u.add(f"I6:I{r - 1}")
        ws.add_data_validation(dv_prod)
        ws.add_data_validation(dv_u)
        if not es_canje:  # pedida por el club pero sin cantidad (Q en blanco o 0): se marca para revisarla
            ws.conditional_formatting.add(f"H6:I{r - 1}", FormulaRule(formula=["AND($H6>0,N($I6)=0)"],
                                                                      fill=PatternFill("solid", fgColor="F8CBAD")))
        celda(ws, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
        for col in "CDEFGJK":
            celda(ws, f"{col}{r}", None, f_gran, relleno=r_gran)
        for col, fmt in (("H", NUM), ("I", NUM), ("L", PESOS), ("M", PESOS)) + ((("N", PESOS),) if es_canje else ()):
            celda(ws, f"{col}{r}", f"=SUM({col}6:{col}{r - 1})", f_gran, fmt, r_gran)
        celda(ws, f"P{r}", None, relleno=r_int)
        celda(ws, f"Q{r}", f"=SUM(Q6:Q{r - 1})", f_gran, PESOS, r_int)
        ws.row_dimensions[r].height = 20
        tot = r
        # separación visual entre ramas
        for _rama, a, _b in ramas[1:]:
            for col in "BCDEFGHIJKLMN"[:13 if es_canje else 12]:
                ws[f"{col}{a}"].border = Border(left=fino, right=fino, bottom=fino,
                                                top=Side(style="medium", color=NAVY))
        for col, ancho in zip("BCDEFGHIJKLMNOPQ", (15, 14, 30, 11, 13, 44, 10, 10, 12, 13, 14, 14, 14, 2, 13, 14)):
            ws.column_dimensions[col].width = ancho
        ws.freeze_panes = "D6"
        ws.print_area = f"A1:{'N' if es_canje else 'M'}{tot}"
        # totales internos a la derecha
        celda(ws, "S4", "TOTALES (USO INTERNO, NO SE IMPRIME)", Font(name="Calibri", size=10, bold=True, color="C00000"),
              alinear=izq, borde=False)
        cabecera(ws, 5, 19, ["CONCEPTO", "VALOR"], relleno=r_int)
        filas_int = ([("Valor del canje (valor formativas y CT, con IVA)", f"=N{tot}"), ("Costo del canje (neto)", f"=Q{tot}")]
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
               "Valores con IVA. Canje de los primeros equipos valorizado a valor formativas y cuerpo técnico; ventas "
               "de formativas y cuerpo técnico a ese valor y stock para la tienda a precio comercial.")
    cabecera(rs, 5, 2, ["CATEGORÍA", "RAMA", "UNIDADES", "VALOR DEL CANJE (VALOR FORMATIVAS Y CT)", "VENTAS (CON IVA)",
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
    cabecera(rs, r, 2, ["PRODUCTO", "VALOR FORMATIVAS Y CT", "PRECIO COMERCIAL TIENDA", None,
                        "UNIDADES CANJE", "UNIDADES FORMATIVAS Y CT", "UNIDADES COMERCIAL",
                        "VALOR DEL CANJE (VALOR FORMATIVAS Y CT)", "VENTAS (CON IVA)"], alto=40)
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
        celda(rs, f"C{r}", f"=PRECIOS!D{fp}", formato=PESOS)
        celda(rs, f"D{r}", f"=PRECIOS!E{fp}", formato=PESOS)
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
                                   tooltip="Generar PDF para el club (todas las hojas menos COSTOS y RESUMEN NEGOCIO)")
    celda(rs, "L4", "Exporta todas las hojas menos COSTOS y RESUMEN NEGOCIO (uso interno) a un PDF en la misma carpeta.", f_nota,
          alinear=Alignment(vertical="top", wrap_text=True), borde=False)
    rs.merge_cells("L4:N5")
    celda(rs, "L6", "Requiere habilitar macros. Si no funciona: Archivo, Exportar, PDF, con todas las hojas menos "
                    "COSTOS y RESUMEN NEGOCIO seleccionadas.", f_nota, alinear=Alignment(vertical="top", wrap_text=True), borde=False)
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
        celda(co, f"C{r}", f"=N(PRECIOS!J{fila_precio[(d, k)]})", formato=PESOS)
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
        ("Valor del canje para el club (valor formativas y CT, con IVA)", f"={can}!N{tcan}", f_norm),
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

    # ---------------------------------------------------------------- RESUMEN NEGOCIO (uso interno)
    sn = wb.create_sheet(HOJA_NEGOCIO, 1)
    sn.sheet_properties.tabColor = "C00000"
    encabezado(sn, "RESUMEN DEL RESULTADO DEL NEGOCIO 2027: VENTA NETA, COSTOS Y MARGEN TOTAL (USO INTERNO, NO VA EN EL PDF)",
               "Todo neto, sin IVA, salvo el canje a valor formativas y CT. Por disciplina: ventas de formativas y cuerpo técnico y "
               "stock comercial, canje de los primeros equipos y margen. Se actualiza solo con las demás hojas.")
    sup = previo["supuestos"] if previo else {}
    otros_txt = "Otros costos del negocio (% de la venta neta: despacho, comisiones, etc.)"
    celda(sn, "B5", otros_txt, f_tot, alinear=izq)
    celda(sn, "C5", sup.get(otros_txt, 0), f_input, "0%", r_input)
    celda(sn, "D5", "Supuesto para simular: parte en 0%.", f_nota, alinear=Alignment(vertical="center"), borde=False)
    dvs = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=False,
                         errorTitle="Supuesto", error="Ingresa un porcentaje entre 0% y 100%.")
    sn.add_data_validation(dvs)
    dvs.add("C5")
    for g0, g1, txt, fondo in (("C", "I", "VENTAS (SIN IVA)", "2F5597"), ("J", "L", "CANJE PRIMEROS EQUIPOS", "7030A0"),
                               ("M", "N", "RESULTADO", NAVY)):
        celda(sn, f"{g0}7", txt, Font(name="Calibri", size=10, bold=True, color="FFFFFF"),
              relleno=PatternFill("solid", fgColor=fondo))
        sn.merge_cells(f"{g0}7:{g1}7")
    cabecera(sn, 8, 2, ["DISCIPLINA O RAMA", "UNIDADES VENDIDAS", "VENTA NETA FORMATIVAS Y CT", "VENTA NETA COMERCIAL",
                        "VENTA NETA TOTAL", "COSTO DE LO VENDIDO", "MARGEN DE LA VENTA", "MARGEN % DE LA VENTA",
                        "UNIDADES EN CANJE", "CANJE A VALOR FORMATIVAS Y CT (CON IVA)", "COSTO DEL CANJE", "MARGEN TOTAL",
                        "MARGEN TOTAL % SOBRE VENTA"], alto=48)
    hoja_q = {c: f"'{detalle[c][0]}'" for c in ("canje", "formativas", "comercial")}
    bloques = {c: {rama: (a, b) for rama, a, b in detalle[c][1]} for c in hoja_q}
    iva_ = "(1+PRECIOS!$C$4)"

    def suma_rama(clave, rama, col):
        ab = bloques[clave].get(rama)
        return f"SUM({hoja_q[clave]}!{col}{ab[0]}:{col}{ab[1]})" if ab else "0"

    def fila_neg(r, txt, uv, vfo, vco, vca, cv, uc, canje, cc, fuente=f_norm, relleno=None):
        celda(sn, f"B{r}", txt, fuente, relleno=relleno, alinear=izq)
        for col, v, fmt in (("C", uv, NUM), ("D", vfo, PESOS), ("E", vco, PESOS), ("G", cv, PESOS), ("J", uc, NUM),
                            ("K", canje, PESOS), ("L", cc, PESOS)):
            celda(sn, f"{col}{r}", v, fuente, fmt, relleno)
        celda(sn, f"F{r}", f"=D{r}+E{r}" + (f"+{vca}" if vca else ""), fuente if relleno else f_tot, PESOS, relleno)
        celda(sn, f"H{r}", f"=F{r}-G{r}", fuente if relleno else f_tot, PESOS, relleno)
        celda(sn, f"I{r}", f'=IF(F{r}=0,"",H{r}/F{r})', fuente, PCT, relleno)
        celda(sn, f"M{r}", f"=H{r}-L{r}", fuente if relleno else f_tot, PESOS, relleno)
        celda(sn, f"N{r}", f'=IF(F{r}=0,"",M{r}/F{r})', fuente, PCT, relleno)

    def titulo_neg(r, txt):
        celda(sn, f"B{r}", txt, Font(name="Calibri", size=10, bold=True, color=NAVY), relleno=r_sub, alinear=izq)
        for col in "CDEFGHIJKLMN":
            celda(sn, f"{col}{r}", None, relleno=r_sub)

    ramas_neg = []
    for clave in ("canje", "formativas", "comercial"):
        for rama, _a, _b in detalle[clave][1]:
            if rama not in ramas_neg:
                ramas_neg.append(rama)
    grupos = [("DISCIPLINAS DEPORTIVAS", "Total disciplinas", [x for x in ramas_neg if disciplina_de(x) != "Institucional"]),
              ("INSTITUCIONAL (CUERPO TÉCNICO, DIRECTORIO Y OFICINA)", "Total institucional",
               [x for x in ramas_neg if disciplina_de(x) == "Institucional"])]
    r, sub = 9, []
    for titulo_g, total_g, ramas_g in grupos:
        if not ramas_g:
            continue
        titulo_neg(r, titulo_g)
        r += 1
        g0 = r
        for rama in ramas_g:
            fo_r = lambda col: suma_rama("formativas", rama, col)  # noqa: E731
            co_r = lambda col: suma_rama("comercial", rama, col)  # noqa: E731
            ca_r = lambda col: suma_rama("canje", rama, col)  # noqa: E731
            pago_canje = ca_r("M")
            fila_neg(r, rama, f"={fo_r('I')}+{co_r('I')}", f"=ROUND({fo_r('M')}/{iva_},0)",
                     f"=ROUND({co_r('M')}/{iva_},0)", None if pago_canje == "0" else f"ROUND({pago_canje}/{iva_},0)",
                     f"={fo_r('Q')}+{co_r('Q')}", f"={ca_r('I')}", f"={ca_r('N')}", f"={ca_r('Q')}")
            r += 1
        fila_neg(r, total_g, *[f"=SUM({c}{g0}:{c}{r - 1})" for c in "CDE"], f"SUM(F{g0}:F{r - 1})-D{r}-E{r}",
                 *[f"=SUM({c}{g0}:{c}{r - 1})" for c in "GJKL"], fuente=f_tot, relleno=r_sub)
        sub.append(r)
        r += 1
    titulo_neg(r, "OTROS COSTOS")
    r += 1
    fila_neg(r, "Otros costos del negocio (% de la venta neta)", None, 0, 0, None,
             "=ROUND((" + "+".join(f"F{x}" for x in sub) + ")*$C$5,0)", None, 0, 0)
    otros = r
    r += 1
    fila_neg(r, "MARGEN TOTAL DEL NEGOCIO", *["=" + "+".join(f"{c}{x}" for x in sub) for c in "CDE"],
             "+".join(f"F{x}" for x in sub) + f"-D{r}-E{r}",
             *["=" + "+".join(f"{c}{x}" for x in sub + [otros]) for c in "G"],
             *["=" + "+".join(f"{c}{x}" for x in sub) for c in "JKL"], fuente=f_gran, relleno=r_gran)
    tn = r
    sn.row_dimensions[r].height = 22
    for col in "HIMN":
        sn.conditional_formatting.add(f"{col}{tn}", CellIsRule(operator="lessThan", formula=["0"],
                                                               fill=PatternFill("solid", fgColor="C00000")))
    celda(sn, f"B{r + 1}", f'=IF(AND(ABS(F{tn}-COSTOS!J{tc})<=10,G{tn}-G{otros}=COSTOS!H{tc},L{tn}=COSTOS!G{tc}),'
                           f'"Control: coincide con la hoja COSTOS (la venta neta puede diferir en unos pesos por '
                           f'redondeo).","Revisar: no coincide con la hoja COSTOS.")', f_nota,
          alinear=Alignment(vertical="center"), borde=False)

    r += 4
    celda(sn, f"B{r}", "RESULTADO DEL NEGOCIO 2027", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    cabecera(sn, r, 2, ["CONCEPTO", "MONTO", "% SOBRE VENTA NETA"], alto=24)
    r += 1
    gv, hv = ("+".join(f"{c}{x}" for x in sub) for c in "GH")  # costo y margen de la venta (sin otros costos)
    m_venta = f"IF(F{tn}=0,0,({hv})/F{tn})"
    kpis = [
        ("Venta neta formativas y cuerpo técnico", f"=D{tn}", True, f_norm),
        ("Venta neta comercial (stock para la tienda del club)", f"=E{tn}", True, f_norm),
        ("Venta neta total (sin IVA)", f"=F{tn}", True, f_tot),
        ("Costo de lo vendido", f"={gv}", True, f_norm),
        ("Margen de la venta", f"={hv}", True, f_tot),
        ("Costo del canje de los primeros equipos (inversión en el club)", f"=L{tn}", True, f_norm),
        ("Otros costos del negocio", f"=G{otros}", True, f_norm),
        ("MARGEN TOTAL DEL NEGOCIO", f"=M{tn}", True, f_gran),
        (None, None, None, None),
        ("Canje entregado al club, a valor formativas y CT (con IVA)", f"=K{tn}", False, f_norm),
        ("Costo total a producir (canje y venta)", f"={gv}+L{tn}", False, f_norm),
        ("Unidades a producir (canje y venta)", f"=C{tn}+J{tn}", False, f_norm),
        ("Venta neta necesaria para cubrir el canje y los otros costos (punto de equilibrio, con el margen % actual "
         "de la venta)", f'=IF({m_venta}-$C$5<=0,"No se cubre",ROUND(L{tn}/({m_venta}-$C$5),0))', False, f_norm),
        ("Venta neta actual sobre el punto de equilibrio", "PE", False, f_norm),
    ]
    fila_pe = r + len(kpis) - 2
    for txt, f, con_pct, fuente in kpis:
        if txt is None:
            r += 1
            continue
        relleno = r_gran if fuente is f_gran else (r_sub if fuente is f_tot else None)
        celda(sn, f"B{r}", txt, fuente, relleno=relleno, alinear=izq)
        if f == "PE":
            celda(sn, f"C{r}", f'=IF(ISNUMBER(C{fila_pe}),IF(C{fila_pe}=0,"",F{tn}/C{fila_pe}),"")', fuente, "0%",
                  relleno)
        else:
            celda(sn, f"C{r}", f, fuente, NUM if txt.startswith("Unidades") else PESOS, relleno)
        celda(sn, f"D{r}", f'=IF(F{tn}=0,"",C{r}/F{tn})' if con_pct else None, fuente, PCT, relleno)
        if fuente is f_gran:
            sn.row_dimensions[r].height = 22
            sn.conditional_formatting.add(f"C{r}:D{r}", CellIsRule(operator="lessThan", formula=["0"],
                                                                    fill=PatternFill("solid", fgColor="C00000")))
        if len(txt) > 60:
            sn.row_dimensions[r].height = 30
        r += 1
    celda(sn, f"B{r + 1}", "Costo unitario: costo directo de producción en taller externo (3.000 prendas al mes), sin gastos "
                           "generales de Playmaker. Si falta el costo de un producto (hoja PRECIOS), su costo queda en cero "
                           "y el margen se ve mayor de lo real.", f_nota, alinear=Alignment(vertical="center"), borde=False)
    for col, ancho in zip("BCDEFGHIJKLMN", (52, 15, 14, 14, 15, 15, 15, 11, 11, 16, 15, 15, 12)):
        sn.column_dimensions[col].width = ancho
    sn.freeze_panes = "C9"

    # ---------------------------------------------------------------- ENTREGAS 2027 (va en el PDF para el club)
    en = wb.create_sheet(HOJA_ENTREGAS, 1)
    encabezado(en, "CALENDARIO DE ENTREGAS 2027", "Tres entregas: equipos de marzo, stock de la tienda de marzo y agosto. "
               "La entrega se elige por rama y categoría. El canje se entrega en proporción a las compras.")
    pe = previo["entregas"] if previo else {}
    nombres_e = [n for n, _f in ENTREGAS]
    FECHA = '[$-340A]d "de" mmmm "de" yyyy'
    ref_fecha = {}
    for i, (nombre, fecha) in enumerate(ENTREGAS):
        txt = f"Fecha de la entrega {i + 1} ({nombre.lower()})"
        celda(en, f"B{5 + i}", txt, f_tot, alinear=izq)
        celda(en, f"C{5 + i}", pe.get(txt, fecha), f_input, FECHA, r_input)
        ref_fecha[nombre] = f"$C${5 + i}"
    celda(en, "N4", "PARÁMETROS DEL CRONOGRAMA (USO INTERNO, NO SE IMPRIME)",
          Font(name="Calibri", size=10, bold=True, color="C00000"), alinear=izq, borde=False)
    ref_par = {}
    for i, (k, txt, v) in enumerate(PARAMETROS_ENTREGA):
        celda(en, f"N{5 + i}", txt, f_tot, relleno=r_int_suave, alinear=izq)
        celda(en, f"O{5 + i}", pe.get(txt, v), f_input, NUM, r_input)
        ref_par[k] = f"$O${5 + i}"
    semana = f"(MAX(1,{ref_par['capacidad']})*12/52)"  # prendas por semana

    f0 = 5 + len(ENTREGAS) + 2
    celda(en, f"B{f0}", "PRENDAS Y VALORES POR RAMA", f_sec, alinear=Alignment(vertical="center"), borde=False)
    cabecera(en, f0 + 1, 2, ["RAMA"] + [f"ENTREGA {t}" for _c, t in CATEGORIAS_ENTREGA]
             + ["UNIDADES PRIMER EQUIPO (CANJE)", "UNIDADES FORMATIVAS Y CT", "UNIDADES COMERCIAL", "TOTAL UNIDADES",
                "VALOR DEL CANJE (VALOR FORMATIVAS Y CT)", "COMPRAS FORMATIVAS Y CT (CON IVA)",
                "COMPRAS COMERCIAL (CON IVA)"], alto=48)
    dv_e = DataValidation(type="list", formula1='"' + ",".join(nombres_e) + '"', allow_blank=False,
                          errorTitle="Entrega", error="Elige una entrega: " + ", ".join(nombres_e))
    en.add_data_validation(dv_e)
    r = e0 = f0 + 2
    for rama in ramas_neg:
        celda(en, f"B{r}", rama, alinear=izq)
        for j, (cat, _t) in enumerate(CATEGORIAS_ENTREGA):
            col = openpyxl.utils.get_column_letter(3 + j)
            v = pe.get(f"rama:{rama}:{3 + j}")
            if v not in nombres_e:
                v = ENTREGA_RAMA.get(rama, ENTREGA_DEFECTO[cat])
            celda(en, f"{col}{r}", v, f_input, relleno=r_input)
        celda(en, f"F{r}", "=" + suma_rama("canje", rama, "I"), formato=NUM)
        celda(en, f"G{r}", "=" + suma_rama("formativas", rama, "I"), formato=NUM)
        celda(en, f"H{r}", "=" + suma_rama("comercial", rama, "I"), formato=NUM)
        celda(en, f"I{r}", f"=F{r}+G{r}+H{r}", f_tot, NUM)
        celda(en, f"J{r}", "=" + suma_rama("canje", rama, "N"), formato=PESOS)
        celda(en, f"K{r}", "=" + suma_rama("formativas", rama, "M") + "+" + suma_rama("canje", rama, "M"), formato=PESOS)
        celda(en, f"L{r}", "=" + suma_rama("comercial", rama, "M"), formato=PESOS)
        r += 1
    dv_e.add(f"C{e0}:E{r - 1}")
    celda(en, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    for col in "CDE":
        celda(en, f"{col}{r}", None, f_gran, relleno=r_gran)
    for col in "FGHIJKL":
        celda(en, f"{col}{r}", f"=SUM({col}{e0}:{col}{r - 1})", f_gran, PESOS if col in "JKL" else NUM, r_gran)
    tr = r
    rng = lambda col: f"${col}${e0}:${col}${tr - 1}"  # noqa: E731

    r += 3
    celda(en, f"B{r}", "RESUMEN POR ENTREGA", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    cabecera(en, r, 2, ["ENTREGA", "FECHA", "UNIDADES PRIMER EQUIPO (CANJE)", "UNIDADES FORMATIVAS Y CT",
                        "UNIDADES COMERCIAL", "TOTAL UNIDADES", "VALOR DEL CANJE (VALOR FORMATIVAS Y CT)",
                        "COMPRAS (CON IVA)", "CANJE SOBRE COMPRAS"], alto=48)
    r += 1
    p0, fila_ent = r, {}
    for i, (nombre, _f) in enumerate(ENTREGAS):
        fila_ent[nombre] = r
        celda(en, f"B{r}", f"Entrega {i + 1}: {nombre.lower()}", f_tot, alinear=izq)
        celda(en, f"C{r}", f"={ref_fecha[nombre]}", formato=FECHA)
        celda(en, f"D{r}", f'=SUMIF({rng("C")},"{nombre}",{rng("F")})', formato=NUM)
        celda(en, f"E{r}", f'=SUMIF({rng("D")},"{nombre}",{rng("G")})', formato=NUM)
        celda(en, f"F{r}", f'=SUMIF({rng("E")},"{nombre}",{rng("H")})', formato=NUM)
        celda(en, f"G{r}", f"=D{r}+E{r}+F{r}", f_tot, NUM)
        celda(en, f"H{r}", f'=SUMIF({rng("C")},"{nombre}",{rng("J")})', f_tot, PESOS)
        celda(en, f"I{r}", f'=SUMIF({rng("D")},"{nombre}",{rng("K")})+SUMIF({rng("E")},"{nombre}",{rng("L")})', f_tot,
              PESOS)
        celda(en, f"J{r}", f'=IF(I{r}=0,"",H{r}/I{r})', formato=PCT)
        r += 1
    celda(en, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    celda(en, f"C{r}", None, f_gran, relleno=r_gran)
    for col in "DEFGHI":
        celda(en, f"{col}{r}", f"=SUM({col}{p0}:{col}{r - 1})", f_gran, PESOS if col in "HI" else NUM, r_gran)
    celda(en, f"J{r}", f'=IF(I{r}=0,"",H{r}/I{r})', f_gran, PCT, r_gran)
    tp = r
    celda(en, f"B{r + 1}", f'=IF(AND(G{tp}=I{tr},I{tp}=K{tr}+L{tr},H{tp}=J{tr}),"Control: todas las prendas tienen entrega '
                           f'asignada.","Revisar: hay prendas sin entrega asignada (columnas ENTREGA).")', f_nota,
          alinear=Alignment(vertical="center"), borde=False)

    r += 4
    celda(en, f"B{r}", "CANJE PROPORCIONAL A LAS COMPRAS", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    celda(en, f"B{r}", "Proporción canje / compras de la propuesta", f_tot, alinear=izq)
    celda(en, f"C{r}", f"=IF(I{tp}=0,0,H{tp}/I{tp})", f_tot, PCT, r_sub)
    prop = f"$C${r}"
    celda(en, f"D{r}", "El canje se entrega en esta proporción respecto de las compras que el club realice.", f_nota,
          alinear=Alignment(vertical="center"), borde=False)
    r += 1
    celda(en, f"B{r}", "Canje por cada $1.000.000 en compras", alinear=izq)
    celda(en, f"C{r}", f"=ROUND(1000000*{prop},0)", formato=PESOS)
    r += 1
    celda(en, f"B{r}", "Compras por cada $1.000.000 en canje", alinear=izq)
    celda(en, f"C{r}", f"=IF({prop}=0,0,ROUND(1000000/{prop},0))", formato=PESOS)
    r += 2
    cabecera(en, r, 2, ["ENTREGA", "COMPRAS DEL CLUB (CON IVA)", "CANJE QUE SE ENTREGA",
                        "CANJE QUE CORRESPONDE SEGÚN LAS COMPRAS", "DIFERENCIA", "DIFERENCIA ACUMULADA"], alto=40)
    r += 1
    q0 = r
    for i, (nombre, _f) in enumerate(ENTREGAS):
        fe = fila_ent[nombre]
        celda(en, f"B{r}", f"Entrega {i + 1}: {nombre.lower()}", f_tot, alinear=izq)
        celda(en, f"C{r}", f"=I{fe}", formato=PESOS)
        celda(en, f"D{r}", f"=H{fe}", formato=PESOS)
        celda(en, f"E{r}", f"=ROUND(C{r}*{prop},0)", formato=PESOS)
        celda(en, f"F{r}", f"=D{r}-E{r}", f_tot, PESOS)
        celda(en, f"G{r}", f"=F{r}" if i == 0 else f"=G{r - 1}+F{r}", formato=PESOS)
        r += 1
    celda(en, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    for col in "CDEF":
        celda(en, f"{col}{r}", f"=SUM({col}{q0}:{col}{r - 1})", f_gran, PESOS, r_gran)
    celda(en, f"G{r}", None, f_gran, relleno=r_gran)
    celda(en, f"B{r + 1}", "DIFERENCIA: canje que se entrega menos el que corresponde a las compras de esa entrega. La "
                           "primera lleva más canje (Esperanza Alba recibe solo canje y el stock de la tienda llega después) "
                           "y las siguientes menos: en el año queda en cero si el club realiza todas las compras.", f_nota,
          alinear=Alignment(vertical="top", wrap_text=True), borde=False)
    en.merge_cells(f"B{r + 1}:L{r + 2}")
    r += 4
    sim_txt = "Simulación: si el club compra (con IVA)"
    celda(en, f"B{r}", sim_txt, f_tot, alinear=izq)
    celda(en, f"C{r}", pe.get(sim_txt, 50000000), f_input, PESOS, r_input)
    celda(en, f"B{r + 1}", "El canje que le corresponde es", f_tot, alinear=izq)
    celda(en, f"C{r + 1}", f"=ROUND(C{r}*{prop},0)", f_tot, PESOS, r_sub)

    r += 4
    celda(en, f"B{r}", "CRONOGRAMA", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    cabecera(en, r, 2, ["HITO"] + [f"ENTREGA {i + 1}: {n}" for i, (n, _f) in enumerate(ENTREGAS)] + ["DETALLE"], alto=30)
    col_det = openpyxl.utils.get_column_letter(3 + len(ENTREGAS))
    en.merge_cells(f"{col_det}{r}:L{r}")
    r += 1
    h0 = r
    fila_hito = {}
    for k, (txt, det, *fechas) in enumerate(HITOS):
        fila_hito[txt] = r
        ultimo = k == len(HITOS) - 1
        celda(en, f"B{r}", txt, f_tot if ultimo else f_norm, alinear=izq)
        for i, (nombre, _f) in enumerate(ENTREGAS):
            col = openpyxl.utils.get_column_letter(3 + i)
            if fechas[i] is None:  # la entrega: la fecha de arriba
                celda(en, f"{col}{r}", f"={ref_fecha[nombre]}", f_tot, FECHA)
            else:
                celda(en, f"{col}{r}", pe.get(f"hito:{txt}:{nombre}", fechas[i]), f_input, FECHA, r_input)
        celda(en, f"{col_det}{r}", det, f_gris, alinear=izq)
        for c in range(4 + len(ENTREGAS), 13):
            celda(en, f"{openpyxl.utils.get_column_letter(c)}{r}", None)
        en.merge_cells(f"{col_det}{r}:L{r}")
        en.row_dimensions[r].height = 28
        r += 1
    # control interno: semanas de producción disponibles frente a las necesarias según el volumen y la capacidad
    fila_int = 6 + len(PARAMETROS_ENTREGA)
    fi, fd = fila_hito["Inicio de producción"], fila_hito["Control de calidad y despacho"]
    for i, (nombre, _f) in enumerate(ENTREGAS):
        col = openpyxl.utils.get_column_letter(3 + i)
        f = fila_int + 3 * i
        celda(en, f"N{f}", f"Semanas de producción disponibles, entrega {i + 1} ({nombre.lower()})", f_tot,
              relleno=r_int_suave, alinear=izq)
        celda(en, f"O{f}", f"=ROUND(({col}{fd}-{col}{fi})/7,1)", f_tot, '0.0')
        celda(en, f"N{f + 1}", f"Semanas necesarias según el volumen ({nombre.lower()})", f_tot, relleno=r_int_suave,
              alinear=izq)
        celda(en, f"O{f + 1}", f"=ROUNDUP(G{fila_ent[nombre]}/{semana},1)", f_tot, '0.0')
        celda(en, f"N{f + 2}", "Estado", f_tot, relleno=r_int_suave, alinear=izq)
        celda(en, f"O{f + 2}", f'=IF(O{f}>=O{f + 1},"OK","FALTAN SEMANAS")', f_tot)
        en.conditional_formatting.add(f"O{f + 2}", CellIsRule(operator="equal", formula=['"FALTAN SEMANAS"'],
                                                              fill=PatternFill("solid", fgColor="F8CBAD")))
    f = fila_int + 3 * len(ENTREGAS)
    celda(en, f"N{f}", "Producción en taller externo: el costo de la propuesta es costo directo, sin gastos generales de "
                       "Playmaker.", f_nota, alinear=Alignment(vertical="top", wrap_text=True), borde=False)
    en.merge_cells(f"N{f}:O{f + 1}")
    en.conditional_formatting.add(f"C{h0}:{openpyxl.utils.get_column_letter(2 + len(ENTREGAS))}{r - 1}",
                                  CellIsRule(operator="lessThan", formula=["TODAY()"],
                                             fill=PatternFill("solid", fgColor="F8CBAD")))
    celda(en, f"B{r}", "Primero el contrato y la orden de compra; después diseños, muestras y tallas, antes de fin de año, "
                       "para producir en enero y febrero. En rojo: fechas que ya pasaron.", f_nota,
          alinear=Alignment(vertical="center"), borde=False)
    for col, ancho in zip("BCDEFGHIJKL", (40, 20, 20, 20, 15, 14, 14, 13, 17, 17, 16)):
        en.column_dimensions[col].width = ancho
    en.column_dimensions["M"].width = 2
    en.column_dimensions["N"].width = 64
    en.column_dimensions["O"].width = 14
    en.print_area = f"A1:L{r}"

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
