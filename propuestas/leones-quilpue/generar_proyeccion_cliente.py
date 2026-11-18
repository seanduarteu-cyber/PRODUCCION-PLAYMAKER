"""Planilla para que Los Leones de Quilpué completen su proyección de compra (formativas y tienda), sin precios.

Uso:
    python3 propuestas/leones-quilpue/generar_proyeccion_cliente.py

Crea Proyeccion_Compra_Los_Leones_Quilpue.xlsx con todas las prendas de PRODUCTOS (generar_propuesta.py), por línea
y con los colores de juego del club. El club anota unidades estimadas para todo el convenio (2027 y 2028), una
sola cifra por prenda, para las formativas y para la tienda oficial. Sin valores: solo cantidades. La hoja va
protegida sin clave para que solo se editen las celdas de respuesta.
"""

import sys
from pathlib import Path

import openpyxl
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.worksheet.datavalidation import DataValidation

DIR = Path(__file__).parent
sys.path.insert(0, str(DIR))
from generar_propuesta import PRODUCTOS  # noqa: E402

SALIDA = DIR / "Proyeccion_Compra_Los_Leones_Quilpue.xlsx"
LOGO = DIR.parent / "_recursos" / "playmaker_logo_horizontal_navy.png"
CLUB = "Club Deportivo Colegio Los Leones de Quilpué"

LINEAS = [
    ("Juego", "LÍNEA DE JUEGO"),
    ("Entrenamiento", "LÍNEA DE ENTRENAMIENTO"),
    ("Presentación y viaje", "LÍNEA DE PRESENTACIÓN Y VIAJE"),
    ("Socios e hinchas", "LÍNEA CASUAL PARA SOCIOS E HINCHAS"),
]
# colores o versiones por prenda (las demás van en una sola fila)
VARIANTES = {
    "camiseta_juego": ["Roja", "Azul", "Blanca", "Negra"],
    "short_juego": ["Rojo", "Azul", "Blanco", "Negro"],
    "polera_calentamiento": ["Roja", "Azul", "Blanca"],
    "camiseta_reversible": ["Colores A y B"],
}
OTRAS_FILAS = 4  # filas en blanco para prendas que el club quiera sumar

INSTRUCCIONES = [
    "Anote cuántas unidades estiman comprar de cada prenda durante todo el convenio (temporadas 2027 y 2028), "
    "en una sola cifra por prenda.",
    "Formativas: prendas que comprarían los jugadores de las series formativas (Sub-11 a Sub-20, damas y varones).",
    "Tienda oficial: unidades que estiman vender a apoderados, socios e hinchas en la tienda en línea del club.",
    "Si una prenda no aplica, déjela en blanco. Al final puede agregar prendas que no estén en la lista.",
]


def main():
    navy, oro = "141E3C", "B1A542"
    f_tit = Font(name="Arial", size=15, bold=True, color=navy)
    f_sub = Font(name="Arial", size=10, color="3A3F52")
    f_nota = Font(name="Arial", size=9, italic=True, color="6E7280")
    f_sec = Font(name="Arial", size=9, bold=True, color=oro)
    f_cab = Font(name="Arial", size=9, bold=True, color="FFFFFF")
    f_norm = Font(name="Arial", size=10, color="1C2233")
    f_input = Font(name="Arial", size=10, color=navy, bold=True)
    f_total = Font(name="Arial", size=10, bold=True, color=navy)
    r_cab = PatternFill("solid", fgColor=navy)
    r_input = PatternFill("solid", fgColor="FBF8EE")
    r_total = PatternFill("solid", fgColor="EDEBE4")
    fino = Side(style="thin", color="DCD8CB")
    caja = Border(left=fino, right=fino, top=fino, bottom=fino)
    linea = Border(bottom=fino)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Proyección de compra"
    ws.sheet_view.showGridLines = False
    for col, ancho in zip("ABCDEF", (6, 38, 18, 17, 17, 42)):
        ws.column_dimensions[col].width = ancho

    def entrada(ref, formato=None):
        c = ws[ref]
        c.font, c.fill, c.border = f_input, r_input, caja
        c.protection = Protection(locked=False)
        c.alignment = Alignment(horizontal="center" if formato else "left", vertical="center", wrap_text=not formato)
        if formato:
            c.number_format = formato
        return c

    # encabezado
    if LOGO.exists():
        logo = Image(str(LOGO))
        escala = 26 / logo.height
        logo.width, logo.height = logo.width * escala, 26
        ws.add_image(logo, "B1")
    ws.row_dimensions[1].height = 24
    ws["B3"], ws["B3"].font = "PROYECCIÓN DE COMPRA DE INDUMENTARIA", f_tit
    ws["B4"], ws["B4"].font = f"{CLUB}. Convenio temporadas 2027 y 2028.", f_sub
    ws["B5"], ws["B5"].font = ("Solo cantidades estimadas, sin valores. Con esta información preparamos la propuesta "
                               "para formativas y la tienda oficial."), f_nota

    # datos de quien completa
    r = 7
    ws[f"B{r}"], ws[f"B{r}"].font = "DATOS DE QUIEN COMPLETA", f_sec
    r += 1
    for etiqueta in ("Nombre", "Cargo en el club", "Fecha"):
        ws[f"B{r}"], ws[f"B{r}"].font = etiqueta, f_norm
        ws.merge_cells(f"C{r}:F{r}")
        entrada(f"C{r}")
        for col in "DEF":
            ws[f"{col}{r}"].border = caja
        ws.row_dimensions[r].height = 20
        r += 1
    ws[f"B{r}"], ws[f"B{r}"].font = "Jugadores en series formativas", f_norm
    ws[f"C{r}"], ws[f"C{r}"].font = "Damas", f_nota
    ws[f"C{r}"].alignment = Alignment(horizontal="right", vertical="center")
    entrada(f"D{r}", "#,##0")
    ws[f"E{r}"], ws[f"E{r}"].font = "Varones", f_nota
    ws[f"E{r}"].alignment = Alignment(horizontal="right", vertical="center")
    entrada(f"F{r}", "#,##0").alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[r].height = 20
    jugadores = r

    # instrucciones
    r += 2
    ws[f"B{r}"], ws[f"B{r}"].font = "CÓMO COMPLETAR", f_sec
    r += 1
    for i, texto in enumerate(INSTRUCCIONES, start=1):
        ws[f"A{r}"], ws[f"A{r}"].font = i, f_sec
        ws[f"A{r}"].alignment = Alignment(horizontal="center", vertical="top")
        ws.merge_cells(f"B{r}:F{r}")
        ws[f"B{r}"], ws[f"B{r}"].font = texto, f_norm
        ws[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 16
        r += 1

    # tabla
    r += 1
    cab = r
    for col, txt in zip("ABCDEF", ("N°", "Prenda", "Color o versión", "Formativas\n(unidades)",
                                   "Tienda oficial\n(unidades)", "Comentarios (tallas, colores, detalles)")):
        c = ws[f"{col}{r}"]
        c.value, c.font, c.fill = txt, f_cab, r_cab
        c.alignment = Alignment(horizontal="left" if col in "BF" else "center", vertical="center", wrap_text=True)
    ws.row_dimensions[r].height = 32
    r += 1
    filas = []
    n = 0
    for linea_clave, titulo in LINEAS:
        ws[f"B{r}"], ws[f"B{r}"].font = titulo, f_sec
        ws.row_dimensions[r].height = 22
        ws[f"B{r}"].alignment = Alignment(vertical="bottom")
        r += 1
        for clave, (nombre, linea_prod, _precio, _adicional, _ref) in PRODUCTOS.items():
            if linea_prod != linea_clave:
                continue
            for variante in VARIANTES.get(clave, [""]):
                n += 1
                ws[f"A{r}"], ws[f"A{r}"].font = n, f_nota
                ws[f"A{r}"].alignment = Alignment(horizontal="center", vertical="center")
                ws[f"B{r}"], ws[f"B{r}"].font = nombre, f_norm
                ws[f"C{r}"], ws[f"C{r}"].font = variante, f_norm
                for col in "ABC":
                    ws[f"{col}{r}"].border = linea
                    ws[f"{col}{r}"].alignment = Alignment(vertical="center", horizontal="center" if col == "A" else "left")
                entrada(f"D{r}", "#,##0")
                entrada(f"E{r}", "#,##0")
                entrada(f"F{r}")
                ws.row_dimensions[r].height = 19
                filas.append(r)
                r += 1

    ws[f"B{r}"], ws[f"B{r}"].font = "OTRAS PRENDAS QUE LES INTERESARÍA INCLUIR", f_sec
    ws.row_dimensions[r].height = 22
    ws[f"B{r}"].alignment = Alignment(vertical="bottom")
    r += 1
    for _ in range(OTRAS_FILAS):
        n += 1
        ws[f"A{r}"], ws[f"A{r}"].font = n, f_nota
        ws[f"A{r}"].alignment = Alignment(horizontal="center", vertical="center")
        entrada(f"B{r}")
        entrada(f"C{r}")
        entrada(f"D{r}", "#,##0")
        entrada(f"E{r}", "#,##0")
        entrada(f"F{r}")
        ws.row_dimensions[r].height = 19
        filas.append(r)
        r += 1

    total = r
    ws[f"B{total}"] = "TOTAL DE UNIDADES"
    for col in "ABCDEF":
        ws[f"{col}{total}"].fill = r_total
        ws[f"{col}{total}"].font = f_total
    for col in "DE":
        c = ws[f"{col}{total}"]
        c.value = f"=SUM({col}{filas[0]}:{col}{filas[-1]})"
        c.number_format = "#,##0"
        c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[total].height = 22
    ws[f"B{total + 2}"] = "Playmaker SpA. Planilla para completar por el club. No incluye precios."
    ws[f"B{total + 2}"].font = f_nota

    dv = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                        errorTitle="Cantidad", error="Ingrese un número entero de unidades (0 o más).")
    ws.add_data_validation(dv)
    dv.add(f"D{jugadores}")
    dv.add(f"F{jugadores}")
    dv.add(f"D{filas[0]}:E{filas[-1]}")

    ws.freeze_panes = f"A{cab + 1}"
    ws.protection.sheet = True
    ws.protection.formatColumns = False
    ws.protection.formatRows = False
    ws.page_setup.orientation = "portrait"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 1
    ws.print_title_rows = f"{cab}:{cab}"
    ws.page_margins.left = ws.page_margins.right = 0.4
    wb.save(SALIDA)
    print(f"OK  {SALIDA.name}  ({n - OTRAS_FILAS} prendas y colores, {OTRAS_FILAS} filas libres)")


if __name__ == "__main__":
    main()
