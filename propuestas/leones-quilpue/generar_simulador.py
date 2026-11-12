"""Simulador del convenio con Los Leones de Quilpué (básquetbol): canje del primer equipo,
venta a formativas y preventa de hinchas.

Uso:
    python3 propuestas/leones-quilpue/generar_simulador.py
    python3 <skill xlsx>/scripts/recalc.py propuestas/leones-quilpue/Simulador_Canje_Leones_Quilpue.xlsx

Crea Simulador_Canje_Leones_Quilpue.xlsx. Todo lo amarillo es un supuesto editable; el resto son fórmulas.
"""

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

SALIDA = Path(__file__).parent / "Simulador_Canje_Leones_Quilpue.xlsx"

NAVY, ORO, GRIS = "141E3C", "B1A542", "6E7280"
F_TITULO = Font(name="Arial", size=14, bold=True, color=NAVY)
F_NOTA = Font(name="Arial", size=9, italic=True, color=GRIS)
F_SECCION = Font(name="Arial", size=10, bold=True, color=ORO)
F_CAB = Font(name="Arial", size=9, bold=True, color="FFFFFF")
F_NORMAL = Font(name="Arial", size=10, color="000000")
F_INPUT = Font(name="Arial", size=10, color="0000FF")
F_TOTAL = Font(name="Arial", size=10, bold=True, color=NAVY)
R_CAB = PatternFill("solid", fgColor=NAVY)
R_INPUT = PatternFill("solid", fgColor="FFF2CC")
R_TOTAL = PatternFill("solid", fgColor="EDEBE4")
LINEA = Border(bottom=Side(style="thin", color="DCD8CB"))
PESOS, PCT, NUM = '"$"#,##0;("$"#,##0);"-"', "0%", "#,##0"

# producto, precio de venta con IVA, referencia (listas de precios de Playmaker)
PRODUCTOS = [
    ("Camiseta de juego básquetbol", 20900, "Sudadera sin mangas, lista Old Green"),
    ("Short de juego básquetbol", 18900, "Short de juego, lista Old Green"),
    ("Camiseta reversible de entrenamiento", 27900, "Línea reversible Playmaker"),
    ("Polerón hoodie", 29900, "Polerón hoodie, lista Old Green"),
    ("Polera de presentación (polo piqué)", 23900, "Polo piqué, lista Old Green"),
    ("Chaqueta de buzo", 37900, "Polerón cierre completo, lista Gauchos"),
    ("Pantalón de buzo", 25900, "Pantalón de buzo, lista Old Green"),
    ("Polera de salida de cancha", 19900, "Camiseta de llegada, lista Old Green"),
]
N = len(PRODUCTOS)
# unidades por jugador y por integrante del staff en el canje; por jugador de formativas
CANJE_JUGADOR = [2, 2, 0, 1, 1, 1, 1, 1]
CANJE_STAFF = [0, 0, 0, 1, 1, 0, 0, 0]
FORMATIVAS_PACK = [1, 1, 0, 1, 0, 0, 0, 0]
CATEGORIAS = ["Sub-11", "Sub-13", "Sub-14", "Sub-16", "Sub-18", "Sub-20"]
TRAMOS = [("Hasta 100", 0, 0.11), ("101 a 200", 101, 0.12), ("201 a 350", 201, 0.13),
          ("351 a 500", 351, 0.14), ("Más de 500", 501, 0.15)]


def celda(ws, ref, valor, fuente=F_NORMAL, formato=None, relleno=None, alinear=None):
    c = ws[ref]
    c.value = valor
    c.font = fuente
    if formato:
        c.number_format = formato
    if relleno:
        c.fill = relleno
    if alinear:
        c.alignment = Alignment(horizontal=alinear, vertical="center", wrap_text=True)
    return c


def entrada(ws, ref, valor, formato=None):
    return celda(ws, ref, valor, F_INPUT, formato, R_INPUT, "right")


def cabecera(ws, fila, textos, col0=1):
    for i, txt in enumerate(textos):
        c = ws.cell(row=fila, column=col0 + i, value=txt)
        c.font, c.fill = F_CAB, R_CAB
        c.alignment = Alignment(horizontal="center" if i else "left", vertical="center", wrap_text=True)
    ws.row_dimensions[fila].height = 30


def encabezado(ws, titulo, nota):
    celda(ws, "A1", titulo, F_TITULO)
    celda(ws, "A2", nota, F_NOTA)


def anchos(ws, valores):
    for letra, ancho in valores.items():
        ws.column_dimensions[letra].width = ancho


wb = Workbook()

# ---------------------------------------------------------------- Supuestos
sup = wb.active
sup.title = "Supuestos"
encabezado(sup, "SUPUESTOS Y PRECIOS DE REFERENCIA",
           "Celdas amarillas = supuestos editables. Precios de venta Playmaker con IVA incluido, tomados de las listas vigentes.")
celda(sup, "A4", "PARÁMETROS", F_SECCION)
celda(sup, "A5", "IVA")
entrada(sup, "B5", 0.19, PCT)
celda(sup, "A6", "Costo de producción Playmaker (% del precio neto)")
entrada(sup, "B6", 0.45, PCT)
celda(sup, "C6", "Supuesto: reemplazar por el costo real promedio", F_NOTA)
celda(sup, "A8", "PRECIOS DE REFERENCIA", F_SECCION)
cabecera(sup, 9, ["Producto", "Precio venta\ncon IVA", "Precio neto\n(sin IVA)", "Costo Playmaker\npor unidad", "Referencia"])
P0 = 10  # primera fila de productos
for i, (nombre, precio, ref) in enumerate(PRODUCTOS):
    r = P0 + i
    celda(sup, f"A{r}", nombre)
    entrada(sup, f"B{r}", precio, PESOS)
    celda(sup, f"C{r}", f"=ROUND(B{r}/(1+$B$5),0)", formato=PESOS)
    celda(sup, f"D{r}", f"=ROUND(C{r}*$B$6,0)", formato=PESOS)
    celda(sup, f"E{r}", ref, F_NOTA)
    for col in "ABCDE":
        sup[f"{col}{r}"].border = LINEA
PF = P0 + N - 1
anchos(sup, {"A": 44, "B": 14, "C": 14, "D": 16, "E": 40})


def precio(col, i):  # referencia absoluta a la lista de precios
    return f"Supuestos!${col}${P0 + i}"


# ---------------------------------------------------------------- Canje primer equipo
can = wb.create_sheet("Canje primer equipo")
encabezado(can, "CANJE: PRIMER EQUIPO FEMENINO Y MASCULINO",
           "Indumentaria que Playmaker entrega sin costo por temporada. Valor comercial = a precio de venta; costo = lo que le cuesta a Playmaker producirla.")
celda(can, "A4", "PLANTELES", F_SECCION)
for r, (txt, val) in enumerate([("Jugadores por equipo", 20), ("Equipos (femenino y masculino)", 2),
                                ("Staff técnico por equipo", 6)], start=5):
    celda(can, f"A{r}", txt)
    entrada(can, f"B{r}", val, NUM)
celda(can, "A8", "Total jugadores", F_TOTAL)
celda(can, "B8", "=B5*B6", F_TOTAL, NUM)
celda(can, "A9", "Total staff técnico", F_TOTAL)
celda(can, "B9", "=B7*B6", F_TOTAL, NUM)
cabecera(can, 11, ["Producto", "Por\njugador", "Por integrante\nde staff", "Unidades", "Valor comercial\ncon IVA", "Valor neto", "Costo\nPlaymaker"])
C0 = 12
for i, (nombre, _, _) in enumerate(PRODUCTOS):
    r = C0 + i
    celda(can, f"A{r}", nombre)
    entrada(can, f"B{r}", CANJE_JUGADOR[i], NUM)
    entrada(can, f"C{r}", CANJE_STAFF[i], NUM)
    celda(can, f"D{r}", f"=B{r}*$B$8+C{r}*$B$9", formato=NUM)
    celda(can, f"E{r}", f"=D{r}*{precio('B', i)}", formato=PESOS)
    celda(can, f"F{r}", f"=D{r}*{precio('C', i)}", formato=PESOS)
    celda(can, f"G{r}", f"=D{r}*{precio('D', i)}", formato=PESOS)
    for col in "ABCDEFG":
        can[f"{col}{r}"].border = LINEA
CF = C0 + N - 1
CT = CF + 1
celda(can, f"A{CT}", "TOTAL POR TEMPORADA", F_TOTAL, relleno=R_TOTAL)
for col in "DEFG":
    celda(can, f"{col}{CT}", f"=SUM({col}{C0}:{col}{CF})", F_TOTAL, NUM if col == "D" else PESOS, R_TOTAL)
for col in "BC":
    can[f"{col}{CT}"].fill = R_TOTAL
celda(can, f"A{CT + 2}", "Valor comercial por jugador (con IVA)")
celda(can, f"B{CT + 2}", f"=SUMPRODUCT(B{C0}:B{CF},Supuestos!$B${P0}:$B${PF})", formato=PESOS)
celda(can, f"A{CT + 3}", "Valor comercial por integrante de staff (con IVA)")
celda(can, f"B{CT + 3}", f"=SUMPRODUCT(C{C0}:C{CF},Supuestos!$B${P0}:$B${PF})", formato=PESOS)
celda(can, f"A{CT + 5}", "Supuesto: buzo = chaqueta + pantalón; salida de cancha = polera de calentamiento. "
                         "Dos uniformes de juego por jugador (local y visita).", F_NOTA)
anchos(can, {"A": 44, "B": 11, "C": 15, "D": 11, "E": 16, "F": 14, "G": 14})

# ---------------------------------------------------------------- Formativas
frm = wb.create_sheet("Formativas")
encabezado(frm, "CATEGORÍAS FORMATIVAS: VENTA POR TEMPORADA",
           "Jugadores por categoría y lo que compra cada uno. Completa la rama femenina si el club la tiene.")
cabecera(frm, 4, ["Categoría", "Rama\nmasculina", "Rama\nfemenina", "Total\njugadores"])
for i, cat in enumerate(CATEGORIAS):
    r = 5 + i
    celda(frm, f"A{r}", cat)
    entrada(frm, f"B{r}", 15, NUM)
    entrada(frm, f"C{r}", 0, NUM)
    celda(frm, f"D{r}", f"=B{r}+C{r}", formato=NUM)
    for col in "ABCD":
        frm[f"{col}{r}"].border = LINEA
KF = 5 + len(CATEGORIAS) - 1
KT = KF + 1
celda(frm, f"A{KT}", "TOTAL", F_TOTAL, relleno=R_TOTAL)
for col in "BCD":
    celda(frm, f"{col}{KT}", f"=SUM({col}5:{col}{KF})", F_TOTAL, NUM, R_TOTAL)

F0 = KT + 3
celda(frm, f"A{F0 - 1}", "LO QUE COMPRA CADA JUGADOR EN LA TEMPORADA", F_SECCION)
cabecera(frm, F0, ["Producto", "Unidades por\njugador", "Unidades\ntotales", "Venta\ncon IVA", "Venta neta", "Costo\nPlaymaker", "Margen\nPlaymaker"])
for i, (nombre, _, _) in enumerate(PRODUCTOS):
    r = F0 + 1 + i
    celda(frm, f"A{r}", nombre)
    entrada(frm, f"B{r}", FORMATIVAS_PACK[i], NUM)
    celda(frm, f"C{r}", f"=B{r}*$D${KT}", formato=NUM)
    celda(frm, f"D{r}", f"=C{r}*{precio('B', i)}", formato=PESOS)
    celda(frm, f"E{r}", f"=C{r}*{precio('C', i)}", formato=PESOS)
    celda(frm, f"F{r}", f"=C{r}*{precio('D', i)}", formato=PESOS)
    celda(frm, f"G{r}", f"=E{r}-F{r}", formato=PESOS)
    for col in "ABCDEFG":
        frm[f"{col}{r}"].border = LINEA
FF = F0 + N
FT = FF + 1
celda(frm, f"A{FT}", "TOTAL POR TEMPORADA", F_TOTAL, relleno=R_TOTAL)
frm[f"B{FT}"].fill = R_TOTAL
for col in "CDEFG":
    celda(frm, f"{col}{FT}", f"=SUM({col}{F0 + 1}:{col}{FF})", F_TOTAL, NUM if col == "C" else PESOS, R_TOTAL)
celda(frm, f"A{FT + 2}", "Compra por jugador (con IVA)")
celda(frm, f"B{FT + 2}", f"=SUMPRODUCT(B{F0 + 1}:B{FF},Supuestos!$B${P0}:$B${PF})", formato=PESOS)
celda(frm, f"A{FT + 3}", "Margen de Playmaker por jugador")
celda(frm, f"B{FT + 3}", f"=IF($D${KT}=0,0,ROUND(G{FT}/$D${KT},0))", formato=PESOS)
anchos(frm, {"A": 44, "B": 13, "C": 12, "D": 14, "E": 14, "F": 14, "G": 14})

# ---------------------------------------------------------------- Preventa hinchas
hin = wb.create_sheet("Preventa hinchas")
encabezado(hin, "PREVENTA OFICIAL PARA HINCHAS Y SOCIOS",
           "Tienda del club en playmaker.cl. El royalty sale del tramo que alcanza la temporada y se aplica a todas las unidades.")
celda(hin, "A4", "SUPUESTOS DE VENTA", F_SECCION)
celda(hin, "A5", "Unidades vendidas a hinchas en la temporada")
entrada(hin, "B5", 150, NUM)
celda(hin, "A6", "Precio promedio por unidad (con IVA)")
entrada(hin, "B6", 25000, PESOS)
celda(hin, "A8", "TRAMOS DE ROYALTY", F_SECCION)
cabecera(hin, 9, ["Unidades en la temporada", "Desde", "Royalty"])
for i, (txt, desde, pct) in enumerate(TRAMOS):
    r = 10 + i
    celda(hin, f"A{r}", txt)
    entrada(hin, f"B{r}", desde, NUM)
    entrada(hin, f"C{r}", pct, PCT)
    for col in "ABC":
        hin[f"{col}{r}"].border = LINEA
celda(hin, "A16", "RESULTADO DE LA TEMPORADA", F_SECCION)
filas = [
    ("Venta a hinchas (con IVA)", "=B5*B6", PESOS),
    ("Venta neta (sin IVA)", "=ROUND(B17/(1+Supuestos!$B$5),0)", PESOS),
    ("Tramo alcanzado", "=IF(B5=0,0,INDEX($C$10:$C$14,MATCH(B5,$B$10:$B$14,1)))", PCT),
    ("Royalty para el club", "=ROUND(B18*B19,0)", PESOS),
    ("Costo Playmaker", "=ROUND(B18*Supuestos!$B$6,0)", PESOS),
    ("Margen Playmaker después del royalty", "=B18-B20-B21", PESOS),
]
for k, (txt, f, fmt) in enumerate(filas):
    r = 17 + k
    celda(hin, f"A{r}", txt, F_TOTAL if k in (3, 5) else F_NORMAL)
    celda(hin, f"B{r}", f, F_TOTAL if k in (3, 5) else F_NORMAL, fmt)
    hin[f"A{r}"].border = hin[f"B{r}"].border = LINEA
anchos(hin, {"A": 44, "B": 16, "C": 12})

# ---------------------------------------------------------------- Resumen (primera hoja)
res = wb.create_sheet("Resumen", 0)
encabezado(res, "LOS LEONES DE QUILPUÉ — CONVENIO DE PROVEEDOR TÉCNICO OFICIAL",
           "Resumen por temporada. Se calcula solo con lo que está en las otras hojas.")
bloques = [
    ("LO QUE INVIERTE PLAYMAKER", [
        ("Costo del canje del primer equipo", f"='Canje primer equipo'!G{CT}"),
    ]),
    ("LO QUE RECUPERA PLAYMAKER", [
        ("Margen por venta a formativas", f"=Formativas!G{FT}"),
        ("Margen por preventa a hinchas (después del royalty)", "='Preventa hinchas'!B22"),
    ]),
    ("RESULTADO", [
        ("Resultado de la temporada para Playmaker", "=B8+B9-B5"),
        ("Cobertura del canje solo con formativas", "=IF(B5=0,0,B8/B5)"),
        ("Jugadores de formativas que cubren el canje", f"=IF(Formativas!B{FT + 3}=0,0,ROUNDUP(B5/Formativas!B{FT + 3},0))"),
    ]),
    ("LO QUE RECIBE EL CLUB", [
        ("Indumentaria del primer equipo y staff (valor comercial con IVA)", f"='Canje primer equipo'!E{CT}"),
        ("Royalty por preventa a hinchas", "='Preventa hinchas'!B20"),
        ("Total para el club", "=B17+B18"),
    ]),
]
r = 4
formatos = {"Cobertura del canje solo con formativas": PCT, "Jugadores de formativas que cubren el canje": NUM}
for titulo, filas in bloques:
    celda(res, f"A{r}", titulo, F_SECCION)
    r += 1
    for txt, f in filas:
        destacado = txt.startswith(("Resultado", "Total"))
        celda(res, f"A{r}", txt, F_TOTAL if destacado else F_NORMAL, relleno=R_TOTAL if destacado else None)
        celda(res, f"B{r}", f, F_TOTAL if destacado else F_NORMAL, formatos.get(txt, PESOS), R_TOTAL if destacado else None)
        res[f"A{r}"].border = res[f"B{r}"].border = LINEA
        r += 1
    r += 1
celda(res, f"A{r}", "Valores por temporada, en pesos chilenos. Supuestos editables en las hojas Supuestos, "
                    "Canje primer equipo, Formativas y Preventa hinchas.", F_NOTA)
anchos(res, {"A": 62, "B": 18})

for ws in wb.worksheets:  # sin cuadrícula; al imprimir, cada hoja en una página horizontal
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 1
wb.save(SALIDA)
print(f"OK  {SALIDA}")
