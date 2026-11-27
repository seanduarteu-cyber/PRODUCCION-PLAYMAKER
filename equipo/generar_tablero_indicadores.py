"""Genera el tablero de indicadores del Responsable Comercial y de Marketing.

Uso:
    python3 equipo/generar_tablero_indicadores.py            # plantilla vacía
    python3 equipo/generar_tablero_indicadores.py --ejemplo  # con datos de prueba (solo para revisar fórmulas)

Hojas:
    TABLERO              parámetros, situación a la fecha de corte, indicadores mensuales y anuales
    CONSULTAS Y VENTAS   una fila por consulta: origen, cotización, cierre, venta, costo y margen
    FACTURAS Y COBRANZA  una fila por factura: emisión, vencimiento, pago y días de cobro
    MARKETING MENSUAL    avisos, costo del departamento, web, redes y calendario de contenido
    PREVENTAS            una fila por campaña de preventa
    CLIENTES             ventas anuales por cliente (concentración y recompra)
    LISTAS               canales de origen, líneas de negocio, vendedores y estados
"""
import sys
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

AQUI = Path(__file__).parent
SALIDA = AQUI / "Tablero_Indicadores_Comercial_Marketing.xlsx"
EJEMPLO = "--ejemplo" in sys.argv
if EJEMPLO:
    SALIDA = AQUI / "_prueba_tablero.xlsx"

NAVY, ORO, MARFIL = "141E3C", "B1A542", "F7F3E7"
F_TIT = Font(name="Calibri", size=14, bold=True, color=NAVY)
F_SUB = Font(name="Calibri", size=10, color="595959")
F_CAB = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
F_SEC = Font(name="Calibri", size=10, bold=True, color=NAVY)
F_NORM = Font(name="Calibri", size=10)
F_BOLD = Font(name="Calibri", size=10, bold=True)
F_INPUT = Font(name="Calibri", size=10, color="0000FF")
F_GRIS = Font(name="Calibri", size=9, color="6E7280")
FILL_NAVY = PatternFill("solid", fgColor=NAVY)
FILL_MARFIL = PatternFill("solid", fgColor=MARFIL)
FILL_ORO = PatternFill("solid", fgColor="E9E4C4")
LINEA = Side(style="thin", color="DCD8CB")
BORDE = Border(bottom=LINEA)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTRO = Alignment(horizontal="center", vertical="center", wrap_text=True)

FMT_PESO = '"$"#,##0;[Red]-"$"#,##0;"-"'
FMT_PCT = '0.0%;[Red]-0.0%;"-"'
FMT_NUM = '#,##0;[Red]-#,##0;"-"'
FMT_DIAS = '#,##0.0;[Red]-#,##0.0;"-"'
FMT_VECES = '0.0"x";[Red]-0.0"x";"-"'
FMT_FECHA = "dd-mm-yyyy"
FMT_MES = "mmm-yy"

N_FILAS = 500          # filas preparadas en los registros
F0 = 6                 # primera fila de datos en los registros
F1 = F0 + N_FILAS - 1  # última fila de datos
MESES = 13             # dic-26 a dic-27
COL_M0 = 4             # columna D = primer mes
COLS_MES = [get_column_letter(COL_M0 + i) for i in range(MESES)]
COL_ACUM = get_column_letter(COL_M0 + MESES)

CANALES = [  # (canal de origen, ¿es de marketing?)
    ("Avisos pagados", "Sí"),
    ("Redes sociales (orgánico)", "Sí"),
    ("Web y tienda en línea", "Sí"),
    ("Prensa y relaciones públicas", "Sí"),
    ("Eventos y torneos", "Sí"),
    ("Referido de un cliente", "No"),
    ("Prospección del vendedor", "No"),
    ("Cliente actual (recompra)", "No"),
    ("Otro", "No"),
]
LINEAS = ["Clubes y federaciones", "Tiendas de clubes", "Web y tienda en línea", "Otros"]
VENDEDORES = ["Vendedor 1", "Vendedor 2", "Responsable comercial", "Gerencia"]
ESTADOS = ["Abierta", "Ganada", "Perdida"]
TIPOS = ["Nuevo", "Actual"]


def rng(hoja, col):
    return f"'{hoja}'!${col}${F0}:${col}${F1}"


CV = "CONSULTAS Y VENTAS"
FC = "FACTURAS Y COBRANZA"
MM = "MARKETING MENSUAL"
PV = "PREVENTAS"
CL = "CLIENTES"
LS = "LISTAS"
TB = "TABLERO"


def cab(ws, fila, textos, col0=2, alto=30):
    for i, t in enumerate(textos):
        c = ws.cell(fila, col0 + i, t)
        c.font, c.fill, c.alignment = F_CAB, FILL_NAVY, CENTRO
    ws.row_dimensions[fila].height = alto


def titulo(ws, texto, sub):
    ws["B1"] = texto
    ws["B1"].font = F_TIT
    ws["B2"] = sub
    ws["B2"].font = F_SUB
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 2


def validar(ws, col, formula, estilo="stop", desde=F0, hasta=F1):
    dv = DataValidation(type="list", formula1=formula, allow_blank=True, errorStyle=estilo,
                        error="Elige un valor de la lista (hoja LISTAS).", errorTitle="Valor fuera de la lista")
    ws.add_data_validation(dv)
    dv.add(f"{col}{desde}:{col}{hasta}")


wb = Workbook()
tb = wb.active
tb.title = TB
cv = wb.create_sheet(CV)
fc = wb.create_sheet(FC)
mm = wb.create_sheet(MM)
pv = wb.create_sheet(PV)
cl = wb.create_sheet(CL)
ls = wb.create_sheet(LS)

# ---------------------------------------------------------------- LISTAS
titulo(ls, "LISTAS", "Valores de las listas desplegables. Se pueden cambiar los nombres en azul; el tablero se actualiza solo.")
cab(ls, 4, ["CANAL DE ORIGEN", "¿ES DE MARKETING?"], col0=2)
cab(ls, 4, ["LÍNEA DE NEGOCIO"], col0=5)
cab(ls, 4, ["VENDEDOR"], col0=7)
cab(ls, 4, ["ESTADO"], col0=9)
cab(ls, 4, ["TIPO DE CLIENTE"], col0=11)
for i, (canal, mk) in enumerate(CANALES):
    ls.cell(5 + i, 2, canal).font = F_INPUT
    ls.cell(5 + i, 3, mk).font = F_INPUT
for i, v in enumerate(LINEAS):
    ls.cell(5 + i, 5, v).font = F_INPUT
for i, v in enumerate(VENDEDORES):
    ls.cell(5 + i, 7, v).font = F_INPUT
for i, v in enumerate(ESTADOS):
    ls.cell(5 + i, 9, v).font = F_NORM
for i, v in enumerate(TIPOS):
    ls.cell(5 + i, 11, v).font = F_NORM
for col, w in {"B": 30, "C": 18, "D": 3, "E": 24, "F": 3, "G": 24, "H": 3, "I": 14, "J": 3, "K": 16}.items():
    ls.column_dimensions[col].width = w
ls["B15"] = "Los estados (Abierta, Ganada, Perdida) y los tipos de cliente no se cambian: las fórmulas los usan."
ls["B15"].font = F_GRIS
validar(ls, "C", '"Sí,No"', desde=5, hasta=13)
L_CANAL = f"{LS}!$B$5:$B${4 + len(CANALES)}"
L_CANAL_MK = f"{LS}!$B$5:$C${4 + len(CANALES)}"
L_LINEA = f"{LS}!$E$5:$E${4 + len(LINEAS)}"
L_VEND = f"{LS}!$G$5:$G${4 + len(VENDEDORES)}"
L_ESTADO = f"{LS}!$I$5:$I$7"
L_TIPO = f"{LS}!$K$5:$K$6"

# ---------------------------------------------------------------- TABLERO: parámetros
titulo(tb, "TABLERO DE INDICADORES COMERCIAL Y DE MARKETING",
       "Playmaker SpA. Se calcula solo a partir de los registros. Celdas azules: se completan a mano. Celdas negras: fórmulas.")
tb["B4"] = "PARÁMETROS"
tb["B4"].font = F_SEC
PARAMS = [  # (fila, etiqueta, valor, formato)
    (5, "Mes de inicio del tablero", date(2026, 12, 1), FMT_MES),
    (6, "Punto de equilibrio mensual (ventas netas)", 30_000_000, FMT_PESO),
    (7, "Capacidad mensual de producción (prendas)", 3000, FMT_NUM),
    (8, "IVA", 0.19, "0%"),
    (9, "Tope de inversión en avisos sobre las ventas que generan", 0.05, "0%"),
    (10, "Plazo de pago por defecto (días)", 30, FMT_NUM),
    (11, "Fecha de corte (hoy, o la fecha que se quiera revisar)", "=TODAY()", FMT_FECHA),
]
for f, etq, val, fmt in PARAMS:
    tb.cell(f, 2, etq).font = F_NORM
    c = tb.cell(f, 3, val)
    c.number_format = fmt
    c.font = F_NORM if isinstance(val, str) and val.startswith("=") else F_INPUT
    c.fill = FILL_MARFIL
    tb.cell(f, 2).border = tb.cell(f, 3).border = BORDE
P_INICIO, P_PE, P_CAP, P_IVA, P_TOPE, P_PLAZO, P_CORTE = (f"{TB}!$C${f}" for f in range(5, 12))
CORTE = "$C$11"

tb.merge_cells("F4:P11")
tb["F4"] = (
    "CÓMO SE USA\n"
    "1. Cada consulta nueva se anota en CONSULTAS Y VENTAS con su canal de origen. Al cotizar, ganar o perder, se actualiza la misma fila.\n"
    "2. Cada factura se anota en FACTURAS Y COBRANZA; al recibir el pago se anota la fecha de pago. "
    "Las ventas de la tienda en línea se pueden anotar como una fila mensual con el total de boletas.\n"
    "3. Cada mes se completa MARKETING MENSUAL, y al cerrar una campaña se agrega una fila en PREVENTAS.\n"
    "4. Una vez al trimestre se revisa la lista de CLIENTES para la concentración y la recompra."
)
tb["F4"].font = Font(name="Calibri", size=9, color=NAVY)
tb["F4"].alignment = WRAP
tb["F4"].fill = FILL_MARFIL

# ---------------------------------------------------------------- TABLERO: situación a la fecha de corte
tb["B13"] = "SITUACIÓN A LA FECHA DE CORTE"
tb["B13"].font = F_SEC
CVr = {c: rng(CV, c) for c in "ABCDEFGHIJKLMNOPQRSTUV"}
FCr = {c: rng(FC, c) for c in "ABCDEFGHIJKLMNO"}
FOTO = [
    ("Pipeline abierto (monto cotizado neto)", f'=SUMIFS({CVr["J"]},{CVr["K"]},"Abierta")', FMT_PESO),
    ("Pipeline con cierre esperado dentro de 90 días", f'=SUMIFS({CVr["J"]},{CVr["K"]},"Abierta",{CVr["L"]},"<="&({CORTE}+90))', FMT_PESO),
    ("Oportunidades abiertas (número)", f'=COUNTIFS({CVr["K"]},"Abierta")', FMT_NUM),
    ("Oportunidades abiertas con fecha de cierre esperado ya pasada", f'=COUNTIFS({CVr["K"]},"Abierta",{CVr["L"]},"<"&{CORTE})', FMT_NUM),
    ("Cuentas por cobrar (con IVA)", f'=SUMIFS({FCr["H"]},{FCr["M"]},"Vencida")+SUMIFS({FCr["H"]},{FCr["M"]},"Por vencer")', FMT_PESO),
    ("Cartera vencida (con IVA)", f'=SUMIFS({FCr["H"]},{FCr["M"]},"Vencida")', FMT_PESO),
    ("Cartera vencida con más de 30 días de atraso", f'=SUMIFS({FCr["H"]},{FCr["M"]},"Vencida",{FCr["N"]},">30")', FMT_PESO),
    ("Facturas vencidas (número)", f'=COUNTIFS({FCr["M"]},"Vencida")', FMT_NUM),
    ("Días de cobro estimados (por cobrar sobre ventas de 30 días)",
     f'=IFERROR(C18/SUMIFS({FCr["H"]},{FCr["B"]},">"&({CORTE}-30),{FCr["B"]},"<="&{CORTE})*30,"")', FMT_DIAS),
]
for i, (etq, fml, fmt) in enumerate(FOTO):
    f = 14 + i
    tb.cell(f, 2, etq).font = F_NORM
    c = tb.cell(f, 3, fml)
    c.number_format, c.font = fmt, F_BOLD
    tb.cell(f, 2).border = tb.cell(f, 3).border = BORDE
assert tb.cell(18, 2).value.startswith("Cuentas por cobrar")

# ---------------------------------------------------------------- TABLERO: indicadores mensuales
FH = 25  # fila de encabezado de meses
tb.cell(FH - 1, 2, "INDICADORES MENSUALES").font = F_SEC
cab(tb, FH, ["INDICADOR", "UNIDAD"], col0=2)
for i, col in enumerate(COLS_MES):
    c = tb[f"{col}{FH}"]
    c.value = f"={P_INICIO}" if i == 0 else f"=EDATE({COLS_MES[i - 1]}{FH},1)"
    c.number_format = FMT_MES
    c.font, c.fill, c.alignment = F_CAB, FILL_NAVY, CENTRO
c = tb[f"{COL_ACUM}{FH}"]
c.value, c.font, c.fill, c.alignment = "ACUMULADO", F_CAB, FILL_NAVY, CENTRO


def en_mes(rango, col):
    return f'{rango},">="&{col}${FH},{rango},"<="&EOMONTH({col}${FH},0)'


filas = {}   # clave -> fila
fila = FH + 1


def seccion(texto):
    global fila
    for k in range(2, COL_M0 + MESES + 1):
        tb.cell(fila, k).fill = FILL_ORO
    tb.cell(fila, 2, texto).font = F_SEC
    fila += 1


def indicador(clave, etiqueta, unidad, plantilla, fmt, suma=False, negrita=False, sangria=False):
    """plantilla: función col -> fórmula (sin '=')."""
    global fila
    c = tb.cell(fila, 2, etiqueta)
    c.font = F_BOLD if negrita else F_NORM
    if sangria:
        c.alignment = Alignment(indent=2)
    tb.cell(fila, 3, unidad).font = F_GRIS
    for col in COLS_MES:
        cc = tb[f"{col}{fila}"]
        cc.value = "=" + plantilla(col)
        cc.number_format = fmt
        cc.font = F_BOLD if negrita else F_NORM
    if suma:
        cc = tb[f"{COL_ACUM}{fila}"]
        cc.value = f"=SUM({COLS_MES[0]}{fila}:{COLS_MES[-1]}{fila})"
        cc.number_format, cc.font = fmt, F_BOLD
    for k in range(2, COL_M0 + MESES + 1):
        tb.cell(fila, k).border = BORDE
    filas[clave] = fila
    fila += 1


def R(clave, col):
    return f"{col}{filas[clave]}"


# --- área comercial
seccion("ÁREA COMERCIAL")
indicador("vtas", "Ventas netas facturadas", "$", lambda c: f"SUMIFS({FCr['F']},{en_mes(FCr['B'], c)})", FMT_PESO, suma=True, negrita=True)
for i, linea in enumerate(LINEAS):
    indicador(f"vtas_l{i}", f"={LS}!$E${5 + i}", "$",
              lambda c, i=i: f"SUMIFS({FCr['F']},{FCr['D']},{LS}!$E${5 + i},{en_mes(FCr['B'], c)})", FMT_PESO, suma=True, sangria=True)
indicador("pe", "Punto de equilibrio (meses hasta la fecha de corte)", "$", lambda c: f'IF({c}${FH}>{P_CORTE},"",{P_PE})', FMT_PESO, suma=True)
indicador("dif_pe", "Diferencia con el punto de equilibrio", "$", lambda c: f'IF({R("pe", c)}="","",{R("vtas", c)}-{R("pe", c)})', FMT_PESO, suma=True, negrita=True)
indicador("av_pe", "Avance sobre el punto de equilibrio", "%", lambda c: f"IFERROR({R('vtas', c)}/{R('pe', c)},\"\")", FMT_PCT)
indicador("cerr", "Ventas cerradas (órdenes de compra)", "$",
          lambda c: f'SUMIFS({CVr["N"]},{CVr["K"]},"Ganada",{en_mes(CVr["M"], c)})', FMT_PESO, suma=True, negrita=True)
indicador("n_gan", "Ventas cerradas (número)", "n°",
          lambda c: f'COUNTIFS({CVr["K"]},"Ganada",{en_mes(CVr["M"], c)})', FMT_NUM, suma=True)
indicador("ticket", "Ticket promedio", "$", lambda c: f"IFERROR({R('cerr', c)}/{R('n_gan', c)},\"\")", FMT_PESO)
indicador("mg", "Margen de contribución", "$",
          lambda c: f'SUMIFS({CVr["P"]},{CVr["K"]},"Ganada",{en_mes(CVr["M"], c)})', FMT_PESO, suma=True)
indicador("mg_pct", "Margen de contribución (sobre ventas con costo registrado)", "%",
          lambda c: f'IFERROR({R("mg", c)}/SUMIFS({CVr["N"]},{CVr["K"]},"Ganada",{CVr["O"]},"<>",{en_mes(CVr["M"], c)}),"")', FMT_PCT, negrita=True)
indicador("desc", "Descuento promedio sobre precio de lista", "%",
          lambda c: f'IFERROR(AVERAGEIFS({CVr["R"]},{CVr["K"]},"Ganada",{CVr["R"]},"<>",{en_mes(CVr["M"], c)}),"")', FMT_PCT)
indicador("cot", "Cotizaciones emitidas", "n°", lambda c: f"COUNTIFS({en_mes(CVr['I'], c)})", FMT_NUM, suma=True)
indicador("n_per", "Cotizaciones perdidas", "n°",
          lambda c: f'COUNTIFS({CVr["K"]},"Perdida",{en_mes(CVr["M"], c)})', FMT_NUM, suma=True)
indicador("conv_n", "Conversión de cotización a venta (número)", "%",
          lambda c: f"IFERROR({R('n_gan', c)}/({R('n_gan', c)}+{R('n_per', c)}),\"\")", FMT_PCT, negrita=True)
indicador("conv_m", "Conversión de cotización a venta (monto cotizado)", "%",
          lambda c: (f'IFERROR(SUMIFS({CVr["J"]},{CVr["K"]},"Ganada",{en_mes(CVr["M"], c)})/'
                     f'(SUMIFS({CVr["J"]},{CVr["K"]},"Ganada",{en_mes(CVr["M"], c)})+'
                     f'SUMIFS({CVr["J"]},{CVr["K"]},"Perdida",{en_mes(CVr["M"], c)})),"")'), FMT_PCT)
indicador("ciclo", "Ciclo de venta promedio (consulta a orden de compra)", "días",
          lambda c: f'IFERROR(AVERAGEIFS({CVr["U"]},{CVr["K"]},"Ganada",{en_mes(CVr["M"], c)}),"")', FMT_DIAS)
indicador("nuevos", "Clientes nuevos ganados", "n°",
          lambda c: f'COUNTIFS({CVr["D"]},"Nuevo",{CVr["K"]},"Ganada",{en_mes(CVr["M"], c)})', FMT_NUM, suma=True)
indicador("dias_cobro", "Días de cobro promedio (facturas pagadas en el mes)", "días",
          lambda c: f"IFERROR(AVERAGEIFS({FCr['L']},{en_mes(FCr['K'], c)}),\"\")", FMT_DIAS, negrita=True)
indicador("prendas", "Prendas comprometidas con entrega en el mes", "prendas",
          lambda c: f'SUMIFS({CVr["S"]},{CVr["K"]},"Ganada",{en_mes(CVr["T"], c)})', FMT_NUM, suma=True)
indicador("cap", "Uso de la capacidad de producción", "%", lambda c: f"IFERROR({R('prendas', c)}/{P_CAP},\"\")", FMT_PCT, negrita=True)
for i in range(len(VENDEDORES)):
    indicador(f"vend{i}", f'="Ventas facturadas: "&{LS}!$G${5 + i}', "$",
              lambda c, i=i: f"SUMIFS({FCr['F']},{FCr['E']},{LS}!$G${5 + i},{en_mes(FCr['B'], c)})", FMT_PESO, suma=True, sangria=True)

# --- marketing
seccion("MARKETING")
indicador("cons", "Consultas recibidas", "n°", lambda c: f"COUNTIFS({en_mes(CVr['B'], c)})", FMT_NUM, suma=True, negrita=True)
for i in range(len(CANALES)):
    indicador(f"canal{i}", f"={LS}!$B${5 + i}", "n°",
              lambda c, i=i: f"COUNTIFS({CVr['F']},{LS}!$B${5 + i},{en_mes(CVr['B'], c)})", FMT_NUM, suma=True, sangria=True)
indicador("cons_mk", "Consultas de canales de marketing", "n°",
          lambda c: f'COUNTIFS({CVr["G"]},"Sí",{en_mes(CVr["B"], c)})', FMT_NUM, suma=True)
indicador("cons_cot", "Consultas que llegan a cotización", "%",
          lambda c: f'IFERROR(COUNTIFS({CVr["I"]},"<>",{en_mes(CVr["B"], c)})/{R("cons", c)},"")', FMT_PCT)
indicador("vta_mk", "Ventas originadas por marketing", "$",
          lambda c: f'SUMIFS({CVr["N"]},{CVr["K"]},"Ganada",{CVr["G"]},"Sí",{en_mes(CVr["M"], c)})', FMT_PESO, suma=True, negrita=True)
indicador("vta_mk_pct", "Ventas originadas por marketing sobre ventas cerradas", "%",
          lambda c: f"IFERROR({R('vta_mk', c)}/{R('cerr', c)},\"\")", FMT_PCT)
# filas de MARKETING MENSUAL (se definen más abajo con las mismas columnas)
MM_FILAS = {}
MM_DEF = [
    ("INVERSIÓN EN AVISOS", None),
    ("av_meta", "Meta (Instagram y Facebook)"),
    ("av_google", "Google"),
    ("av_otros", "Otras plataformas"),
    ("av_total", "Total inversión en avisos"),
    ("COSTO DEL DEPARTAMENTO DE MARKETING", None),
    ("dep_hon", "Honorarios o sueldos (parte asignada a marketing)"),
    ("dep_herr", "Herramientas y software"),
    ("dep_prod", "Producción de contenido (fotos, video, diseño)"),
    ("dep_total", "Total costo del departamento"),
    ("REFERENCIA", None),
    ("agencia", "Costo mensual de la agencia anterior"),
    ("WEB Y TIENDA EN LÍNEA", None),
    ("web_vis", "Visitas"),
    ("web_ped", "Pedidos"),
    ("REDES SOCIALES", None),
    ("rs_alc", "Alcance del mes"),
    ("rs_int", "Interacciones del mes"),
    ("rs_seg", "Seguidores al cierre del mes"),
    ("CALENDARIO DE CONTENIDO", None),
    ("cal_plan", "Publicaciones planificadas"),
    ("cal_real", "Publicaciones realizadas"),
]
f_mm = 6
for clave, etq in MM_DEF:
    MM_FILAS[clave] = f_mm
    f_mm += 1


def M(clave, col):
    return f"'{MM}'!{col}{MM_FILAS[clave]}"


indicador("inv", "Inversión en avisos", "$", lambda c: M("av_total", c), FMT_PESO, suma=True)
indicador("vta_av", f"Ventas generadas por avisos", "$",
          lambda c: f'SUMIFS({CVr["N"]},{CVr["K"]},"Ganada",{CVr["F"]},{LS}!$B$5,{en_mes(CVr["M"], c)})', FMT_PESO, suma=True)
indicador("inv_pct", "Inversión en avisos sobre ventas generadas", "%",
          lambda c: f"IF({R('inv', c)}=0,\"\",IFERROR({R('inv', c)}/{R('vta_av', c)},\"SIN VENTAS\"))", FMT_PCT, negrita=True)
indicador("tope", "Control del tope de inversión en avisos", "estado",
          lambda c: (f'IF({R("inv", c)}=0,"",IF({R("vta_av", c)}=0,"SOBRE EL TOPE",'
                     f'IF({R("inv", c)}/{R("vta_av", c)}<={P_TOPE},"DENTRO DEL TOPE","SOBRE EL TOPE")))'), "@", negrita=True)
indicador("roas", "Retorno de los avisos (ventas sobre inversión)", "veces",
          lambda c: f"IFERROR({R('vta_av', c)}/{R('inv', c)},\"\")", FMT_VECES)
indicador("cpc", "Costo por consulta de avisos", "$",
          lambda c: f"IFERROR({R('inv', c)}/{R('canal0', c)},\"\")", FMT_PESO)
indicador("dep", "Costo del departamento de marketing", "$", lambda c: M("dep_total", c), FMT_PESO, suma=True)
indicador("ag", "Costo de la agencia anterior (referencia)", "$", lambda c: M("agencia", c), FMT_PESO, suma=True)
indicador("dif_ag", "Diferencia: departamento menos agencia", "$", lambda c: f"{R('dep', c)}-{R('ag', c)}", FMT_PESO, suma=True)
indicador("cac", "Costo de conseguir un cliente nuevo", "$",
          lambda c: f"IFERROR(({R('inv', c)}+{R('dep', c)})/{R('nuevos', c)},\"\")", FMT_PESO, negrita=True)
indicador("web_vis", "Web: visitas", "n°", lambda c: M("web_vis", c), FMT_NUM, suma=True)
indicador("web_ped", "Web: pedidos", "n°", lambda c: M("web_ped", c), FMT_NUM, suma=True)
indicador("web_conv", "Web: conversión (pedidos sobre visitas)", "%",
          lambda c: f"IFERROR({R('web_ped', c)}/{R('web_vis', c)},\"\")", FMT_PCT)
indicador("web_ticket", "Web: ticket promedio (ventas web sobre pedidos)", "$",
          lambda c: f"IFERROR({R('vtas_l2', c)}/{R('web_ped', c)},\"\")", FMT_PESO)
indicador("rs_alc", "Redes: alcance", "n°", lambda c: M("rs_alc", c), FMT_NUM, suma=True)
indicador("rs_tasa", "Redes: tasa de interacción (interacciones sobre alcance)", "%",
          lambda c: f"IFERROR({M('rs_int', c)}/{R('rs_alc', c)},\"\")", FMT_PCT)
indicador("rs_seg", "Redes: seguidores al cierre", "n°", lambda c: M("rs_seg", c), FMT_NUM)
indicador("rs_crec", "Redes: crecimiento de seguidores", "%",
          lambda c: ('""' if c == COLS_MES[0] else
                     f"IF(OR({R('rs_seg', c)}=0,{R('rs_seg', COLS_MES[COLS_MES.index(c) - 1])}=0),\"\","
                     f"{R('rs_seg', c)}/{R('rs_seg', COLS_MES[COLS_MES.index(c) - 1])}-1)"), FMT_PCT)
indicador("cal", "Cumplimiento del calendario de contenido", "%",
          lambda c: f"IFERROR({M('cal_real', c)}/{M('cal_plan', c)},\"\")", FMT_PCT, negrita=True)
indicador("pv_u", "Preventas: unidades (campañas cerradas en el mes)", "prendas",
          lambda c: f"SUMIFS({rng(PV, 'F')},{en_mes(rng(PV, 'E'), c)})", FMT_NUM, suma=True)
indicador("pv_v", "Preventas: venta neta (campañas cerradas en el mes)", "$",
          lambda c: f"SUMIFS({rng(PV, 'G')},{en_mes(rng(PV, 'E'), c)})", FMT_PESO, suma=True)
ULT_MENSUAL = fila - 1

# ---------------------------------------------------------------- TABLERO: indicadores anuales
fila += 1
FA = fila + 1
tb.cell(fila, 2, "INDICADORES ANUALES (se revisan cada trimestre)").font = F_SEC
cab(tb, FA, ["INDICADOR", "UNIDAD"], col0=2)
CLr = {c: rng(CL, c) for c in "DEF"}
for j, col in enumerate(["D", "E", "F"]):
    c = tb[f"{col}{FA}"]
    c.value = f"={CL}!{col}5"
    c.font, c.fill, c.alignment = F_CAB, FILL_NAVY, CENTRO
    c.number_format = "0"
ANUALES = [
    ("Ventas netas facturadas del año", "$",
     lambda col: f'=SUMIFS({FCr["F"]},{FCr["B"]},">="&DATE({col}${FA},1,1),{FCr["B"]},"<="&DATE({col}${FA},12,31))', FMT_PESO),
    ("Ventas del año de los clientes de la hoja CLIENTES (control)", "$", lambda col: f"=SUM({CLr[col]})", FMT_PESO),
    ("Clientes con compras en el año", "n°", lambda col: f'=COUNTIF({CLr[col]},">0")', FMT_NUM),
    ("Concentración: ventas de los 5 clientes mayores", "%",
     lambda col: "=IFERROR((" + "+".join(f"IFERROR(LARGE({CLr[col]},{k}),0)" for k in range(1, 6)) + f")/{col}{FA + 1},\"\")", FMT_PCT),
    ("Recompra: clientes del año anterior que vuelven a comprar", "%",
     lambda col: ('=""' if col == "D" else
                  f'=IF({col}{FA + 1}=0,"",IFERROR(COUNTIFS({CLr[chr(ord(col) - 1)]},">0",{CLr[col]},">0")/COUNTIF({CLr[chr(ord(col) - 1)]},">0"),""))'), FMT_PCT),
]
for i, (etq, uni, pl, fmt) in enumerate(ANUALES):
    f = FA + 1 + i
    tb.cell(f, 2, etq).font = F_NORM
    tb.cell(f, 3, uni).font = F_GRIS
    for col in "DEF":
        c = tb[f"{col}{f}"]
        c.value, c.number_format, c.font = pl(col), fmt, F_BOLD
    for k in range(2, 7):
        tb.cell(f, k).border = BORDE

tb.column_dimensions["B"].width = 58
tb.column_dimensions["C"].width = 16
for col in COLS_MES:
    tb.column_dimensions[col].width = 13.5
tb.column_dimensions[COL_ACUM].width = 15
tb.freeze_panes = f"D{FH + 1}"

# formato condicional del tablero
ROJO = PatternFill("solid", fgColor="F8D7DA")
VERDE = PatternFill("solid", fgColor="D9EAD3")
AMBAR = PatternFill("solid", fgColor="FCE8B2")
rango_meses = lambda k: f"{COLS_MES[0]}{filas[k]}:{COLS_MES[-1]}{filas[k]}"
tb.conditional_formatting.add(rango_meses("dif_pe"), CellIsRule(operator="lessThan", formula=["0"], fill=ROJO))
tb.conditional_formatting.add(rango_meses("cap"), FormulaRule(formula=[f'AND(ISNUMBER({COLS_MES[0]}{filas["cap"]}),{COLS_MES[0]}{filas["cap"]}>1)'], fill=ROJO))
tb.conditional_formatting.add(rango_meses("tope"), CellIsRule(operator="equal", formula=['"SOBRE EL TOPE"'], fill=ROJO))
tb.conditional_formatting.add(rango_meses("tope"), CellIsRule(operator="equal", formula=['"DENTRO DEL TOPE"'], fill=VERDE))
tb.conditional_formatting.add("C19:C21", CellIsRule(operator="greaterThan", formula=["0"], fill=ROJO))

# ---------------------------------------------------------------- CONSULTAS Y VENTAS
titulo(cv, "REGISTRO DE CONSULTAS Y VENTAS",
       "Una fila por consulta, desde que llega hasta que se gana o se pierde. Azul: se completa. Negro: fórmula.")
cv["B3"] = ("Fecha de cierre: la fecha de la orden de compra si se gana, o la fecha en que se pierde. "
            "Cierre esperado: solo para las abiertas. Mes de entrega: el primer día del mes en que se entregan las prendas.")
cv["B3"].font = F_GRIS
COLS_CV = [
    ("A", "N°", 5, None), ("B", "FECHA DE CONSULTA", 12, FMT_FECHA), ("C", "CLIENTE", 28, None),
    ("D", "TIPO DE CLIENTE", 11, None), ("E", "LÍNEA DE NEGOCIO", 20, None), ("F", "CANAL DE ORIGEN", 24, None),
    ("G", "¿MARKETING?", 11, None), ("H", "VENDEDOR", 18, None), ("I", "FECHA DE COTIZACIÓN", 12, FMT_FECHA),
    ("J", "MONTO COTIZADO NETO", 15, FMT_PESO), ("K", "ESTADO", 10, None), ("L", "CIERRE ESPERADO", 12, FMT_FECHA),
    ("M", "FECHA DE CIERRE", 12, FMT_FECHA), ("N", "VENTA NETA (OC)", 15, FMT_PESO), ("O", "COSTO DIRECTO", 15, FMT_PESO),
    ("P", "MARGEN", 14, FMT_PESO), ("Q", "MARGEN %", 10, FMT_PCT), ("R", "DESCUENTO SOBRE LISTA", 11, FMT_PCT),
    ("S", "PRENDAS", 10, FMT_NUM), ("T", "MES DE ENTREGA", 11, FMT_MES), ("U", "DÍAS DE CICLO", 10, FMT_NUM),
    ("V", "OBSERVACIONES", 36, None),
]
FORM_CV = {
    "A": lambda r: f'=IF(C{r}="","",ROW()-{F0 - 1})',
    "G": lambda r: f'=IF(F{r}="","",IFERROR(VLOOKUP(F{r},{L_CANAL_MK},2,0),"No"))',
    "P": lambda r: f'=IF(OR(N{r}="",O{r}=""),"",N{r}-O{r})',
    "Q": lambda r: f'=IF(OR(P{r}="",N{r}=0),"",P{r}/N{r})',
    "U": lambda r: f'=IF(OR(B{r}="",M{r}="",K{r}<>"Ganada"),"",M{r}-B{r})',
}


def registro(ws, cols, formulas):
    cab(ws, F0 - 1, [c[1] for c in cols], col0=1, alto=34)
    for col, _, ancho, fmt in cols:
        ws.column_dimensions[col].width = ancho
        for r in range(F0, F1 + 1):
            c = ws[f"{col}{r}"]
            if col in formulas:
                c.value = formulas[col](r)
                c.font = F_NORM
            else:
                c.font = F_INPUT
            if fmt:
                c.number_format = fmt
    ws.freeze_panes = ws[f"C{F0}"]
    ws.auto_filter.ref = f"A{F0 - 1}:{cols[-1][0]}{F1}"


registro(cv, COLS_CV, FORM_CV)
validar(cv, "D", L_TIPO)
validar(cv, "E", L_LINEA)
validar(cv, "F", L_CANAL)
validar(cv, "H", L_VEND, estilo="warning")
validar(cv, "K", L_ESTADO)
validar(cv, "C", f"{CL}!$B${F0}:$B${F0 + 199}", estilo="information")
cv.conditional_formatting.add(f"K{F0}:K{F1}", CellIsRule(operator="equal", formula=['"Ganada"'], fill=VERDE))
cv.conditional_formatting.add(f"K{F0}:K{F1}", CellIsRule(operator="equal", formula=['"Perdida"'], fill=ROJO))
cv.conditional_formatting.add(f"Q{F0}:Q{F1}", FormulaRule(formula=[f'AND(ISNUMBER(Q{F0}),Q{F0}<0)'], fill=ROJO))

# ---------------------------------------------------------------- FACTURAS Y COBRANZA
titulo(fc, "REGISTRO DE FACTURAS Y COBRANZA",
       "Una fila por factura. Al recibir el pago se anota la fecha de pago. Azul: se completa. Negro: fórmula.")
fc["B3"] = ("Plazo de pago: si se deja en blanco se usa el plazo por defecto del TABLERO. "
            "Las boletas de la tienda en línea se pueden anotar como una fila mensual con su total.")
fc["B3"].font = F_GRIS
COLS_FC = [
    ("A", "N° DE FACTURA", 11, None), ("B", "FECHA DE EMISIÓN", 12, FMT_FECHA), ("C", "CLIENTE", 28, None),
    ("D", "LÍNEA DE NEGOCIO", 20, None), ("E", "VENDEDOR", 18, None), ("F", "MONTO NETO", 15, FMT_PESO),
    ("G", "IVA", 13, FMT_PESO), ("H", "TOTAL", 15, FMT_PESO), ("I", "PLAZO DE PAGO (DÍAS)", 10, FMT_NUM),
    ("J", "FECHA DE VENCIMIENTO", 12, FMT_FECHA), ("K", "FECHA DE PAGO", 12, FMT_FECHA), ("L", "DÍAS DE COBRO", 10, FMT_NUM),
    ("M", "ESTADO", 12, None), ("N", "DÍAS DE ATRASO", 10, FMT_NUM), ("O", "OBSERVACIONES", 36, None),
]
FORM_FC = {
    "G": lambda r: f'=IF(F{r}="","",ROUND(F{r}*{P_IVA},0))',
    "H": lambda r: f'=IF(F{r}="","",F{r}+G{r})',
    "J": lambda r: f'=IF(B{r}="","",B{r}+IF(I{r}="",{P_PLAZO},I{r}))',
    "L": lambda r: f'=IF(OR(B{r}="",K{r}=""),"",K{r}-B{r})',
    "M": lambda r: f'=IF(B{r}="","",IF(K{r}<>"","Pagada",IF(J{r}<{P_CORTE},"Vencida","Por vencer")))',
    "N": lambda r: f'=IF(M{r}="Vencida",{P_CORTE}-J{r},"")',
}
registro(fc, COLS_FC, FORM_FC)
validar(fc, "D", L_LINEA)
validar(fc, "E", L_VEND, estilo="warning")
validar(fc, "C", f"{CL}!$B${F0}:$B${F0 + 199}", estilo="information")
fc.conditional_formatting.add(f"M{F0}:M{F1}", CellIsRule(operator="equal", formula=['"Vencida"'], fill=ROJO))
fc.conditional_formatting.add(f"M{F0}:M{F1}", CellIsRule(operator="equal", formula=['"Por vencer"'], fill=AMBAR))
fc.conditional_formatting.add(f"M{F0}:M{F1}", CellIsRule(operator="equal", formula=['"Pagada"'], fill=VERDE))

# ---------------------------------------------------------------- MARKETING MENSUAL
titulo(mm, "MARKETING MENSUAL", "Datos que se completan a mano una vez al mes. Los meses siguen al TABLERO.")
cab(mm, 5, ["CONCEPTO", "UNIDAD"], col0=2)
for i, col in enumerate(COLS_MES):
    c = mm[f"{col}5"]
    c.value = f"={TB}!{col}{FH}"
    c.number_format = FMT_MES
    c.font, c.fill, c.alignment = F_CAB, FILL_NAVY, CENTRO
TOTALES_MM = {"av_total": ("av_meta", "av_otros"), "dep_total": ("dep_hon", "dep_prod")}
UNID_MM = {"web_vis": "n°", "web_ped": "n°", "rs_alc": "n°", "rs_int": "n°", "rs_seg": "n°", "cal_plan": "n°", "cal_real": "n°"}
for clave, etq in MM_DEF:
    f = MM_FILAS[clave]
    if etq is None:
        for k in range(2, COL_M0 + MESES):
            mm.cell(f, k).fill = FILL_ORO
        mm.cell(f, 2, clave).font = F_SEC
        continue
    total = clave in TOTALES_MM
    mm.cell(f, 2, etq).font = F_BOLD if total else F_NORM
    unidad = UNID_MM.get(clave, "$")
    mm.cell(f, 3, unidad).font = F_GRIS
    for col in COLS_MES:
        c = mm[f"{col}{f}"]
        if total:
            a, b = TOTALES_MM[clave]
            c.value = f"=SUM({col}{MM_FILAS[a]}:{col}{MM_FILAS[b]})"
            c.font = F_BOLD
        else:
            c.font = F_INPUT
            c.fill = FILL_MARFIL
        c.number_format = FMT_PESO if unidad == "$" else FMT_NUM
    for k in range(2, COL_M0 + MESES):
        mm.cell(f, k).border = BORDE
mm.column_dimensions["B"].width = 50
mm.column_dimensions["C"].width = 9
for col in COLS_MES:
    mm.column_dimensions[col].width = 13.5
mm.freeze_panes = "D6"

# ---------------------------------------------------------------- PREVENTAS
titulo(pv, "PREVENTAS", "Una fila por campaña de preventa con un club. La variación se compara con la campaña anterior del mismo club.")
COLS_PV = [
    ("A", "N°", 5, None), ("B", "CAMPAÑA", 28, None), ("C", "CLUB", 24, None), ("D", "FECHA DE INICIO", 12, FMT_FECHA),
    ("E", "FECHA DE CIERRE", 12, FMT_FECHA), ("F", "UNIDADES VENDIDAS", 11, FMT_NUM), ("G", "VENTA NETA", 15, FMT_PESO),
    ("H", "UNIDADES CAMPAÑA ANTERIOR", 12, FMT_NUM), ("I", "VENTA NETA CAMPAÑA ANTERIOR", 15, FMT_PESO),
    ("J", "VARIACIÓN UNIDADES", 11, FMT_PCT), ("K", "VARIACIÓN VENTA", 11, FMT_PCT), ("L", "OBSERVACIONES", 36, None),
]
FORM_PV = {
    "A": lambda r: f'=IF(B{r}="","",ROW()-{F0 - 1})',
    "J": lambda r: f'=IF(OR(F{r}="",N(H{r})=0),"",F{r}/H{r}-1)',
    "K": lambda r: f'=IF(OR(G{r}="",N(I{r})=0),"",G{r}/I{r}-1)',
}
registro(pv, COLS_PV, FORM_PV)

# ---------------------------------------------------------------- CLIENTES
titulo(cl, "CLIENTES", "Lista de clientes, escritos igual que en los registros. Las ventas del año se calculan desde FACTURAS Y COBRANZA.")
cab(cl, F0 - 1, ["N°", "CLIENTE", "LÍNEA DE NEGOCIO"], col0=1, alto=34)
for j, (col, anio) in enumerate(zip("DEF", (2026, 2027, 2028))):
    c = cl[f"{col}{F0 - 1}"]
    c.value, c.font, c.fill, c.alignment = anio, Font(name="Calibri", size=10, bold=True, color="FFFFFF"), FILL_NAVY, CENTRO
cl["D4"] = "Ventas netas facturadas por año (los años del encabezado se pueden cambiar):"
cl["D4"].font = F_GRIS
for r in range(F0, F0 + 200):
    cl[f"A{r}"] = f'=IF(B{r}="","",ROW()-{F0 - 1})'
    cl[f"B{r}"].font = F_INPUT
    cl[f"C{r}"].font = F_INPUT
    for col in "DEF":
        c = cl[f"{col}{r}"]
        c.value = (f'=IF($B{r}="","",SUMIFS({FCr["F"]},{FCr["C"]},$B{r},'
                   f'{FCr["B"]},">="&DATE({col}${F0 - 1},1,1),{FCr["B"]},"<="&DATE({col}${F0 - 1},12,31)))')
        c.number_format = FMT_PESO
validar(cl, "C", L_LINEA, desde=F0, hasta=F0 + 199)
for col, w in {"A": 5, "B": 32, "C": 22, "D": 16, "E": 16, "F": 16}.items():
    cl.column_dimensions[col].width = w
cl.freeze_panes = f"C{F0}"
# los años de CLIENTES quedan en la fila 5; el tablero anual los lee de ahí
assert F0 - 1 == 5

# ---------------------------------------------------------------- datos de prueba
if EJEMPLO:
    d = date
    consultas = [  # fecha, cliente, tipo, línea, canal, vend, f_cot, cotizado, estado, cierre_esp, f_cierre, venta, costo, desc, prendas, mes_entrega
        (d(2026, 12, 2), "Club A", "Nuevo", LINEAS[0], CANALES[0][0], VENDEDORES[0], d(2026, 12, 5), 10_000_000, "Ganada", None, d(2026, 12, 20), 9_000_000, 6_000_000, 0.1, 400, d(2027, 3, 1)),
        (d(2026, 12, 3), "Club B", "Actual", LINEAS[0], CANALES[7][0], VENDEDORES[1], d(2026, 12, 6), 5_000_000, "Perdida", None, d(2026, 12, 18), None, None, None, None, None),
        (d(2026, 12, 10), "Club C", "Nuevo", LINEAS[1], CANALES[1][0], VENDEDORES[0], d(2026, 12, 12), 8_000_000, "Abierta", d(2027, 1, 15), None, None, None, None, None, None),
        (d(2026, 12, 11), "Club D", "Nuevo", LINEAS[0], CANALES[6][0], VENDEDORES[1], None, None, "Abierta", None, None, None, None, None, None, None),
        (d(2027, 1, 4), "Club C", "Nuevo", LINEAS[0], CANALES[0][0], VENDEDORES[0], d(2027, 1, 6), 4_000_000, "Ganada", None, d(2027, 1, 20), 4_000_000, None, 0.0, 200, d(2027, 3, 1)),
    ]
    for i, fila_d in enumerate(consultas):
        r = F0 + i
        for col, v in zip("BCDEFHIJKLMNORST", fila_d):
            if v is not None:
                cv[f"{col}{r}"] = v
    facturas = [  # n°, emisión, cliente, línea, vendedor, neto, plazo, pago
        (101, d(2026, 12, 1), "Club A", LINEAS[0], VENDEDORES[0], 20_000_000, None, d(2026, 12, 31)),
        (102, d(2026, 12, 5), "Club B", LINEAS[1], VENDEDORES[1], 10_000_000, 15, None),
        (103, d(2026, 12, 20), "Club C", LINEAS[2], VENDEDORES[0], 6_000_000, None, d(2027, 1, 9)),
        (104, d(2027, 1, 10), "Club A", LINEAS[0], VENDEDORES[0], 5_000_000, None, None),
    ]
    for i, fila_d in enumerate(facturas):
        r = F0 + i
        for col, v in zip("ABCDEFIK", fila_d):
            if v is not None:
                fc[f"{col}{r}"] = v
    mm[f"D{MM_FILAS['av_meta']}"] = 300_000
    mm[f"D{MM_FILAS['av_google']}"] = 150_000
    mm[f"D{MM_FILAS['dep_hon']}"] = 500_000
    mm[f"D{MM_FILAS['agencia']}"] = 800_000
    mm[f"D{MM_FILAS['web_vis']}"] = 1000
    mm[f"D{MM_FILAS['web_ped']}"] = 20
    mm[f"D{MM_FILAS['rs_seg']}"] = 5000
    mm[f"E{MM_FILAS['rs_seg']}"] = 5250
    mm[f"D{MM_FILAS['cal_plan']}"] = 12
    mm[f"D{MM_FILAS['cal_real']}"] = 9
    pv["B6"], pv["C6"], pv["D6"], pv["E6"], pv["F6"], pv["G6"], pv["H6"], pv["I6"] = "Camisetas 2027", "Club A", d(2026, 12, 1), d(2026, 12, 15), 120, 2_400_000, 100, 2_000_000
    for i, cli in enumerate(["Club A", "Club B", "Club C"]):
        cl[f"B{F0 + i}"] = cli
    tb["C11"] = d(2027, 1, 15)

wb._sheets.sort(key=lambda s: [TB, CV, FC, MM, PV, CL, LS].index(s.title))
wb.active = 0
wb.save(SALIDA)
print(SALIDA, "| filas tablero:", FH, "a", ULT_MENSUAL, "| anual desde", FA)
