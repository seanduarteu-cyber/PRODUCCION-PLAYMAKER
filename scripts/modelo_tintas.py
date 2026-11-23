# Modelo de consumo de tinta por canal (Blue, Yellow, Magenta, Black) - Mimaki TS100-1600, sublimación.
# Genera: Excel con fórmulas (supuestos editables) y PDF con el informe.
# Uso: python3 -I scripts/modelo_tintas.py PMK_Receta_Produccion.xlsx salida.xlsx salida.pdf
import sys, math
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as L

SRC, XLSX, PDF = sys.argv[1:4]
PRECIO_L = load_workbook(SRC, data_only=True)['Precios']['U7'].value or 72119   # $ por litro (receta, POR CONFIRMAR)

CANALES = ['Blue', 'Yellow', 'Magenta', 'Black']
ANCHO = 1.60
ML_100 = {'Bajo': 3.0, 'Base': 4.0, 'Alto': 5.0}     # ml por m² de UN canal impreso al 100% (supuesto de modelación)
MANT = 0.08                                          # tinta de limpiezas y chequeos, que el RIP no cuenta (supuesto)
ESC = {   # cobertura del papel, carga de tinta promedio sobre lo impreso (suma CMYK), reparto por canal B/Y/M/K
    'A': dict(nom='Predominantemente oscura', det='Azul marino, negro, azul rey, fondos oscuros', cob=0.80, carga=2.60, rep=[0.34, 0.08, 0.24, 0.34],
              por='Azul marino y azul rey se forman con mucho Blue y algo de Magenta; el negro y los fondos oscuros cargan Black y se refuerzan con Blue/Magenta (negro enriquecido). El Yellow casi no se usa.'),
    'B': dict(nom='Multicolor', det='Rojos, azules, amarillos, verdes, degradados, diseños variados', cob=0.60, carga=1.70, rep=[0.27, 0.28, 0.27, 0.18],
              por='Rojos = Magenta + Yellow; verdes = Blue + Yellow; amarillos = Yellow. El Yellow sube y queda parejo con Blue y Magenta. El Black solo en textos, sombras y contornos.'),
    'C': dict(nom='Alta cobertura', det='Fondos completos, grandes superficies, diseños complejos multicolor', cob=0.95, carga=2.30, rep=[0.28, 0.22, 0.28, 0.22],
              por='Casi todo el papel impreso con colores medios a oscuros: los cuatro canales trabajan, con Blue y Magenta algo arriba porque forman la mayoría de los tonos de equipo.'),
}
MEZCLA = {'A': 0.30, 'B': 0.40, 'C': 0.30}           # mezcla mensual supuesta para la proyección
METROS_CASO = 2500
VOL_MES = [1500, 2500, 4000]
DIAS_MES, LEAD, SEGURIDAD = 22, 7, 5                 # días hábiles/mes, días de reposición, días de colchón

# ---------------- cálculo (mismo que las fórmulas del Excel)
def calc(e, nivel='Base'):
    x = ESC[e]; tot = x['cob'] * x['carga'] * ML_100[nivel]            # ml/m² de papel, impresión (lo que ve el RIP)
    can = [tot * s for s in x['rep']]
    real = [c * (1 + MANT) for c in can]                                  # con mantención (lo que sale de la botella)
    return dict(tot=tot, can=can, real=real,
                ml_ml=[r * ANCHO for r in real],                          # ml por metro lineal
                rinde=[1000 / (r * ANCHO) for r in real],                 # metros lineales por botella de 1.000 cc
                caso=[r * METROS_CASO * ANCHO for r in real])             # ml en 2.500 m
R = {e: {n: calc(e, n) for n in ML_100} for e in ESC}
def mezcla(n='Base'):
    ml = [sum(MEZCLA[e] * R[e][n]['ml_ml'][i] for e in ESC) for i in range(4)]
    return dict(ml_ml=ml, rinde=[1000 / v for v in ml])
MZ = {n: mezcla(n) for n in ML_100}

# ---------------- EXCEL
AZUL = PatternFill('solid', fgColor='DDEBF7'); GRIS = PatternFill('solid', fgColor='F2F2F2'); HF = PatternFill('solid', fgColor='1F3864'); AMA = PatternFill('solid', fgColor='FFF2CC')
H = Font(bold=True, color='FFFFFF'); B = Font(bold=True); WC = Alignment(wrap_text=True, vertical='center', horizontal='center')
MONEY = '"$"#,##0'
wb = Workbook(); ws = wb.active; ws.title = 'Supuestos'
def enc(w, r, c0, cols, anchos=None):
    for i, t in enumerate(cols):
        x = w.cell(r, c0 + i, t); x.font = H; x.fill = HF; x.alignment = WC
        if anchos: w.column_dimensions[L(c0 + i)].width = anchos[i]
    w.row_dimensions[r].height = 32
ws['A1'] = 'TINTAS SUBLIMACIÓN - MIMAKI TS100-1600 - SUPUESTOS'; ws['A1'].font = Font(bold=True, size=14, color='1F3864')
ws['A2'] = 'Azul = supuesto editable (reemplazar con la medición real). Gris = se calcula. Ningún supuesto es dato del fabricante.'; ws['A2'].font = Font(italic=True, color='595959')
enc(ws, 4, 1, ['Parámetro', 'Valor', 'Qué es / de dónde sale'], [46, 14, 90])
par = [('Ancho del papel (m)', ANCHO, 'Dato Playmaker.', '0.00'),
       ('ml por m² de UN canal al 100% - nivel BAJO', ML_100['Bajo'], 'SUPUESTO. Rango calibrado con cifras de proveedores (8-15 ml/m² a cobertura total con límite de tinta 200-300%).', '0.0'),
       ('ml por m² de UN canal al 100% - nivel BASE', ML_100['Base'], 'SUPUESTO central.', '0.0'),
       ('ml por m² de UN canal al 100% - nivel ALTO', ML_100['Alto'], 'SUPUESTO.', '0.0'),
       ('Tinta de mantención (% sobre impresión)', MANT, 'SUPUESTO: limpiezas de cabezal, chequeos de inyectores, purgas. El RIP no la cuenta; la botella sí.', '0%'),
       ('Precio tinta $ por litro (igual los 4 colores)', PRECIO_L, 'Hoja Precios de la receta (U7), POR CONFIRMAR. Si un color cuesta distinto, cambiarlo abajo.', MONEY),
       ('Días hábiles por mes', DIAS_MES, 'Supuesto.', '0'), ('Días de reposición (desde que se pide hasta que llega)', LEAD, 'Supuesto: confirmar con el proveedor.', '0'),
       ('Días de colchón (stock de seguridad)', SEGURIDAD, 'Supuesto.', '0'), ('Metros lineales del caso práctico', METROS_CASO, 'Caso pedido: 2.500 m x 1,60 = 4.000 m².', '#,##0')]
NOMBRE = {}
for i, (a, v, n, f) in enumerate(par):
    r = 5 + i; ws.cell(r, 1, a); c = ws.cell(r, 2, v); c.fill = AZUL; c.number_format = f; ws.cell(r, 3, n)
    NOMBRE[a] = f'Supuestos!$B${r}'
AN, MLB, MLM, MLA, MN, PL, DM, LT, SG, MC = [NOMBRE[p[0]] for p in par]
r0 = 17
ws.cell(r0 - 1, 1, 'Precio por color ($ por litro)').font = B
enc(ws, r0, 1, ['Color'] + CANALES)
ws.cell(r0 + 1, 1, '$ por litro')
for j in range(4): c = ws.cell(r0 + 1, 2 + j, f'={PL}'); c.fill = AZUL; c.number_format = MONEY
PRC = [f'Supuestos!${L(2 + j)}${r0 + 1}' for j in range(4)]
r1 = r0 + 4
ws.cell(r1 - 1, 1, 'Escenarios de producción').font = B
enc(ws, r1, 1, ['Escenario', 'Cobertura del papel', 'Carga de tinta (suma CMYK sobre lo impreso)', 'Reparto Blue', 'Reparto Yellow', 'Reparto Magenta', 'Reparto Black', 'Suma reparto', 'Mezcla mensual'], [46, 14, 18, 12, 12, 12, 12, 12, 12])
FILA_E = {}
for i, e in enumerate(ESC):
    r = r1 + 1 + i; x = ESC[e]; FILA_E[e] = r
    ws.cell(r, 1, f'{e} - {x["nom"]}')
    for c, v, f in [(2, x['cob'], '0%'), (3, x['carga'], '0%')] + [(4 + j, x['rep'][j], '0%') for j in range(4)] + [(9, MEZCLA[e], '0%')]:
        cc = ws.cell(r, c, v); cc.fill = AZUL; cc.number_format = f
    cc = ws.cell(r, 8, f'=SUM(D{r}:G{r})'); cc.fill = GRIS; cc.number_format = '0%'
ws.cell(r1 + 5, 1, 'Cobertura = parte del papel que lleva tinta. Carga = suma de los 4 canales sobre la zona impresa (100% = un canal sólido). Reparto = qué parte de la tinta es de cada color: debe sumar 100%.').font = Font(italic=True, color='595959', size=9)
ws.freeze_panes = 'A5'

def hoja_escenarios():
    w = wb.create_sheet('Caso 2500 m')
    w['A1'] = 'CASO PRÁCTICO: 2.500 METROS LINEALES x 1,60 m = 4.000 m²'; w['A1'].font = Font(bold=True, size=14, color='1F3864')
    w['A2'] = 'Nivel BASE de los supuestos. "Rinde por envase" es el número para el sistema: «un envase de 1.000 cc rinde ___ metros».'; w['A2'].font = Font(italic=True, color='595959')
    w.column_dimensions['A'].width = 42
    r = 4
    for e in ESC:
        fe = FILA_E[e]
        w.cell(r, 1, f'Escenario {e}: {ESC[e]["nom"]}').font = Font(bold=True, size=12, color='1F3864'); r += 1
        enc(w, r, 1, ['Indicador'] + CANALES + ['TOTAL'], [42, 14, 14, 14, 14, 14]); r += 1
        tot = f'Supuestos!$B${fe}*Supuestos!$C${fe}*{MLM}'
        filas = [('ml por m² (impresión, RIP)', lambda j: f'={tot}*Supuestos!{L(4 + j)}${fe}', '0.00'),
                 ('ml por m² (con mantención, botella)', lambda j: f'={L(2 + j)}{r}*(1+{MN})', '0.00'),
                 ('Consumo en 2.500 m (cc)', lambda j: f'={L(2 + j)}{r + 1}*{MC}*{AN}', '#,##0'),
                 ('Consumo por 1.000 m (cc)', lambda j: f'={L(2 + j)}{r + 1}*1000*{AN}', '#,##0'),
                 ('RINDE POR ENVASE 1.000 cc (metros lineales)', lambda j: f'=1000/({L(2 + j)}{r + 1}*{AN})', '#,##0'),
                 ('Rinde por litro (m² de papel)', lambda j: f'=1000/{L(2 + j)}{r + 1}', '#,##0'),
                 ('Botellas necesarias para 2.500 m', lambda j: f'=ROUNDUP({L(2 + j)}{r + 2}/1000,0)', '0'),
                 ('Costo tinta por metro lineal', lambda j: f'={L(2 + j)}{r + 1}*{AN}*{PRC[j]}/1000', MONEY),
                 ('Costo tinta por m²', lambda j: f'={L(2 + j)}{r + 1}*{PRC[j]}/1000', MONEY)]
        for k, (t, f, fmt) in enumerate(filas):
            rr = r + k; w.cell(rr, 1, t).font = B if 'RINDE' in t else Font()
            for j in range(4):
                c = w.cell(rr, 2 + j, f(j)); c.number_format = fmt; c.fill = AMA if 'RINDE' in t else GRIS
            if 'RINDE' not in t and 'Rinde por litro' not in t:
                c = w.cell(rr, 6, f'=SUM(B{rr}:E{rr})'); c.number_format = fmt; c.font = B
        r += len(filas) + 2
hoja_escenarios()

w = wb.create_sheet('Proyección mensual')
w['A1'] = 'PROYECCIÓN MENSUAL, STOCK Y COMPRAS (mezcla de escenarios de la hoja Supuestos, nivel BASE)'; w['A1'].font = Font(bold=True, size=13, color='1F3864')
w.column_dimensions['A'].width = 46
w['A3'] = 'Metros lineales impresos por mes'; w['B3'] = 2500; w['B3'].fill = AZUL; w['B3'].number_format = '#,##0'
enc(w, 5, 1, ['Indicador'] + CANALES + ['TOTAL'], [46, 14, 14, 14, 14, 14])
def mlml(j):   # ml por metro lineal, mezcla, con mantención
    return '+'.join(f'Supuestos!$I${FILA_E[e]}*Supuestos!$B${FILA_E[e]}*Supuestos!$C${FILA_E[e]}*{MLM}*Supuestos!{L(4 + j)}${FILA_E[e]}' for e in ESC) + f'*1'
filas = [('ml por metro lineal (mezcla, con mantención)', lambda j: f'=({mlml(j)})*(1+{MN})*{AN}', '0.00'),
         ('RINDE POR ENVASE 1.000 cc (metros) - valor para el sistema', lambda j: f'=1000/{L(2 + j)}6', '#,##0'),
         ('Consumo del mes (cc)', lambda j: f'={L(2 + j)}6*$B$3', '#,##0'),
         ('Botellas por mes', lambda j: f'={L(2 + j)}8/1000', '0.0'),
         ('Compra mensual (botellas enteras)', lambda j: f'=ROUNDUP({L(2 + j)}9,0)', '0'),
         ('Compra mensual ($)', lambda j: f'={L(2 + j)}10*{PRC[j]}', MONEY),
         ('Consumo por día hábil (cc)', lambda j: f'={L(2 + j)}8/{DM}', '#,##0'),
         ('Una botella dura (días hábiles)', lambda j: f'=1000/{L(2 + j)}12', '0.0'),
         ('STOCK MÍNIMO (botellas): reposición + colchón', lambda j: f'=ROUNDUP({L(2 + j)}12*({LT}+{SG})/1000,0)+1', '0'),
         ('Pedir cada (días hábiles), comprando de a 1 botella', lambda j: f'={L(2 + j)}13', '0.0'),
         ('Costo tinta por metro lineal', lambda j: f'={L(2 + j)}6*{PRC[j]}/1000', MONEY),
         ('Costo tinta por m²', lambda j: f'={L(2 + j)}6/{AN}*{PRC[j]}/1000', MONEY)]
for k, (t, f, fmt) in enumerate(filas):
    rr = 6 + k; w.cell(rr, 1, t).font = B if ('RINDE' in t or 'STOCK' in t) else Font()
    for j in range(4):
        c = w.cell(rr, 2 + j, f(j)); c.number_format = fmt; c.fill = AMA if ('RINDE' in t or 'STOCK' in t) else GRIS
    if any(s in t for s in ('ml por', 'Consumo del', 'Botellas por', 'Compra', 'Consumo por día', 'Costo')):
        c = w.cell(rr, 6, f'=SUM(B{rr}:E{rr})'); c.number_format = fmt; c.font = B
w['A19'] = 'Stock mínimo = consumo diario x (días de reposición + días de colchón), redondeado a botellas, + 1 botella abierta en la máquina.'; w['A19'].font = Font(italic=True, color='595959', size=9)

# Registro de medición real
w = wb.create_sheet('Registro real')
w['A1'] = 'REGISTRO DE MEDICIÓN REAL - llenar cada trabajo y cada botella'; w['A1'].font = Font(bold=True, size=13, color='1F3864')
w['A2'] = 'Parte 1: por trabajo, desde RasterLink (Calculate Ink Consumption). Parte 2: cada botella que se termina. Parte 3: se calcula el rendimiento real del mes.'; w['A2'].font = Font(italic=True, color='595959')
enc(w, 4, 1, ['Fecha', 'OT / trabajo', 'Escenario (A/B/C)', 'Metros lineales', 'cc Blue (RIP)', 'cc Yellow (RIP)', 'cc Magenta (RIP)', 'cc Black (RIP)', 'cc total (RIP)', 'cc por metro (RIP)'], [12, 16, 12, 12, 12, 12, 12, 12, 12, 12])
for r in range(5, 205):
    for c in range(1, 9): w.cell(r, c).fill = AZUL
    w.cell(r, 9, f'=IF(D{r}="","",SUM(E{r}:H{r}))').fill = GRIS
    c = w.cell(r, 10, f'=IF(N(D{r})=0,"",I{r}/D{r})'); c.fill = GRIS; c.number_format = '0.00'
enc(w, 4, 12, ['Fecha botella terminada', 'Color', 'cc de la botella'], [14, 12, 12])
for r in range(5, 105):
    for c in (12, 13): w.cell(r, c).fill = AZUL
    w.cell(r, 14, f'=IF(M{r}="","",1000)').fill = GRIS
enc(w, 4, 16, ['RESULTADO DEL PERÍODO', 'Blue', 'Yellow', 'Magenta', 'Black'], [36, 12, 12, 12, 12])
w['P5'] = 'cc según RIP'; w['P6'] = 'cc según botellas'; w['P7'] = 'Factor real / RIP (mantención y error del RIP)'; w['P8'] = 'Metros lineales impresos'
w['P9'] = 'RINDE REAL POR ENVASE (metros) - cargar en el sistema'; w['P9'].font = B
for j, col in enumerate('QRST'):
    w[f'{col}5'] = f'=SUM({L(5 + j)}5:{L(5 + j)}204)'
    w[f'{col}6'] = f'=SUMIF($M$5:$M$104,"{CANALES[j]}",$N$5:$N$104)'
    w[f'{col}7'] = f'=IF(N({col}5)=0,"",{col}6/{col}5)'; w[f'{col}7'].number_format = '0.00'
    w[f'{col}8'] = '=SUM($D$5:$D$204)'
    w[f'{col}9'] = f'=IF(N({col}6)=0,"",{col}8/({col}6/1000))'; w[f'{col}9'].number_format = '#,##0'; w[f'{col}9'].fill = AMA; w[f'{col}9'].font = B
w['P11'] = 'Con pocas botellas el resultado es grueso: usar al menos 2-3 botellas terminadas por color (un trimestre).'; w['P11'].font = Font(italic=True, color='595959', size=9)
wb.save(XLSX)

# ---------------- PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.utils import simpleSplit
W, Hh = letter; X0, X1 = 40, W - 40
AZ = HexColor('#1F3864'); GR = HexColor('#595959'); BAN = HexColor('#F2F2F2'); AM = HexColor('#FFF2CC')
COLS = {'Blue': HexColor('#1F6FB4'), 'Yellow': HexColor('#B08900'), 'Magenta': HexColor('#B4237A'), 'Black': HexColor('#222222')}
c = canvas.Canvas(PDF, pagesize=letter); c.setTitle('PMK - Consumo de tintas Mimaki TS100-1600')
pg = [0]
def f0(x): return f'{x:,.0f}'.replace(',', '.')
def f1(x, d=1): return f'{x:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def plata(x): return '$' + f0(x)
def t(x, y, s, size=9, bold=False, color=black, right=False, center=False):
    c.setFont('Helvetica-Bold' if bold else 'Helvetica', size); c.setFillColor(color)
    (c.drawRightString if right else c.drawCentredString if center else c.drawString)(x, y, s); c.setFillColor(black)
def par(y, s, size=9, color=black, bold=False, w=None, lead=None):
    for ln in simpleSplit(s, 'Helvetica-Bold' if bold else 'Helvetica', size, w or (X1 - X0)):
        t(X0, y, ln, size, bold, color); y -= lead or size + 3
    return y
def pie():
    t(X0, 20, 'Playmaker - Consumo de tintas por canal, Mimaki TS100-1600. Noviembre 2026.', 7, color=GR); t(X1, 20, f'Pagina {pg[0]}', 7, color=GR, right=True)
def nueva(tit, sub=''):
    if pg[0]: pie(); c.showPage()
    pg[0] += 1
    c.setFillColor(AZ); c.rect(0, Hh - 54, W, 54, fill=1, stroke=0)
    t(X0, Hh - 30, tit, 15, True, white); t(X0, Hh - 45, sub, 8.5, False, white)
    return Hh - 78
def h2(y, s):
    if y < 120: y = nueva('CONSUMO DE TINTAS (continuacion)')
    t(X0, y, s, 11.5, True, AZ); return y - 17
def tabla(y, cab, filas, anchos, resaltar=(), size=8.5, colcolor=True):
    xs = [X0]; [xs.append(xs[-1] + a) for a in anchos]
    c.setFillColor(HexColor('#D9D9D9')); c.rect(X0, y - 4, sum(anchos), 15, fill=1, stroke=0)
    for i, h in enumerate(cab):
        col = COLS.get(h, black) if colcolor else black
        (t(xs[i] + 3, y, h, 8, True, col) if i == 0 else t(xs[i + 1] - 4, y, h, 8, True, col, right=True))
    y -= 16
    for k, f in enumerate(filas):
        if k in resaltar: c.setFillColor(AM); c.rect(X0, y - 4, sum(anchos), 14, fill=1, stroke=0)
        elif k % 2: c.setFillColor(BAN); c.rect(X0, y - 4, sum(anchos), 14, fill=1, stroke=0)
        for i, v in enumerate(f):
            (t(xs[i] + 3, y, v, size, k in resaltar) if i == 0 else t(xs[i + 1] - 4, y, v, size, k in resaltar, right=True))
        y -= 14
    return y - 6

# Página 1: respuesta corta
y = nueva('CONSUMO DE TINTAS POR COLOR - MIMAKI TS100-1600', 'Modelo tecnico y financiero para Playmaker. Sublimacion, papel de 1,60 m, tintas Blue, Yellow, Magenta y Black en botellas de 1.000 cc.')
y = h2(y, 'Respuesta corta')
y = par(y, 'Mimaki no publica cuánto consume cada color por metro, y tampoco hay mediciones independientes publicadas para este equipo. '
           'Por eso los números de este informe son ESCENARIOS con supuestos a la vista, no datos. Sirven para partir; el valor definitivo se obtiene '
           'midiendo 2-3 meses con el método de la última página (contador del RIP + botellas terminadas).', 9.5)
y -= 6
y = par(y, 'Valor para cargar hoy en el sistema («un envase de 1.000 cc rinde ___ metros»), con la mezcla supuesta de producción '
           f'(A {MEZCLA["A"]:.0%} oscura, B {MEZCLA["B"]:.0%} multicolor, C {MEZCLA["C"]:.0%} alta cobertura):', 9.5, bold=True)
y -= 4
fil = [['Rinde por envase - nivel BASE (cargar este)'] + [f0(v) + ' m' for v in MZ['Base']['rinde']],
       ['Rango probable (supuesto alto - bajo)'] + [f'{f0(MZ["Alto"]["rinde"][i])} - {f0(MZ["Bajo"]["rinde"][i])} m' for i in range(4)],
       ['ml por metro lineal (base)'] + [f1(v, 2) for v in MZ['Base']['ml_ml']],
       ['Costo tinta por metro lineal (base)'] + [plata(v * PRECIO_L / 1000) for v in MZ['Base']['ml_ml']]]
y = tabla(y, ['', 'Blue', 'Yellow', 'Magenta', 'Black'], fil, [212, 75, 75, 75, 95], resaltar=(0,))
tot_ml = sum(MZ['Base']['ml_ml'])
y = par(y, f'Tinta total (4 colores) por metro lineal, base: {f1(tot_ml, 1)} ml  =  {plata(tot_ml * PRECIO_L / 1000)} por metro lineal  =  '
           f'{plata(tot_ml / ANCHO * PRECIO_L / 1000)} por m² de papel, con la tinta a {plata(PRECIO_L)} el litro (precio de la receta, POR CONFIRMAR). '
           'Este valor reemplaza el "$0 de impresión" que hoy tiene la receta de costos.', 9)
y -= 6
y = par(y, 'Por qué los colores rinden distinto: el Yellow es el que más rinde porque casi no entra en azules, negros ni fondos oscuros, '
           'que son la mayor parte de los uniformes. Blue y Magenta son los que más se gastan porque forman los azules, morados, rojos y negros enriquecidos. '
           'El Black depende mucho de cuántos fondos oscuros y negros se imprimen.', 9)
y -= 8
y = h2(y, 'Qué es dato y qué es supuesto')
items = [('DATO DEL FABRICANTE', 'Mimaki TS100-1600: tinta de sublimación Sb610 en 4 colores (Blue, Magenta, Yellow, Black), botellas de 1 litro; resoluciones 360, 600, 720 y 900 dpi; gota mínima 5 pl; ancho máximo de impresión 1.610 mm; velocidad máxima 70 m²/h (modo rápido), 46 m²/h (calidad práctica) y 19 m²/h (alta calidad).'),
         ('DATO DEL FABRICANTE', 'RasterLink (el RIP de Mimaki) calcula el consumo de tinta por trabajo (opción "Calculate Ink Consumption"). Mimaki aclara que es aproximado y depende del perfil y del modo de impresión.'),
         ('NO EXISTE PÚBLICO', 'Consumo por canal (ml por m² de Blue, Yellow, Magenta o Black) para la TS100-1600 o la tinta Sb610.'),
         ('REFERENCIAS DE TERCEROS', 'Proveedores de tinta indican 8-15 ml/m² (hasta 20-30 ml/m²) con el papel impreso al 100%. Un taller que midió en Epson F6300 y Mutoh reportó solo 1-2 ml/m² en producción normal, con límite de tinta de 200-220%. Son cifras sin control ni detalle por color.'),
         ('SUPUESTO DE ESTE MODELO', f'Un canal impreso al 100% gasta {f1(ML_100["Bajo"])} a {f1(ML_100["Alto"])} ml/m² (base {f1(ML_100["Base"])}); cobertura, carga de tinta y reparto por color de cada escenario; {MANT:.0%} extra por limpiezas; mezcla mensual {MEZCLA["A"]:.0%}/{MEZCLA["B"]:.0%}/{MEZCLA["C"]:.0%}.')]
for a, b in items:
    if y < 70: y = nueva('CONSUMO DE TINTAS (continuacion)')
    t(X0, y, a, 8, True, AZ if 'DATO' in a else HexColor('#C00000') if 'NO' in a else HexColor('#9C5700'))
    y = par(y - 11, b, 8.5, lead=11) - 4

# Página 2: método y escenarios
y = nueva('COMO SE CALCULA', 'Una sola formula para todos los escenarios: cambia lo que imprime, no la maquina.')
y = par(y, 'ml por m² de papel (un color) = cobertura del papel  x  carga de tinta  x  ml de un canal al 100%  x  reparto de ese color  x  (1 + mantención)', 9.5, bold=True)
y -= 4
for s in ['Cobertura: qué parte del papel lleva tinta (los espacios entre piezas y los blancos no gastan).',
          'Carga de tinta: suma de los 4 canales sobre lo impreso. Un color puro = 100%; un azul marino puede llevar 250%+; el límite lo fija el perfil ICC/RIP.',
          f'ml de un canal al 100%: cuánta tinta deja un color sólido por m². Supuesto {f1(ML_100["Bajo"])}-{f1(ML_100["Alto"])} ml/m², coherente con las cifras de proveedores (8-15 ml/m² a 200-300% de carga).',
          'Reparto: qué parte de esa tinta es de cada color, según los colores que dominan los diseños.',
          f'Mantención: limpiezas de cabezal y chequeos de inyectores. Salen de la botella pero el RIP no las cuenta. Supuesto {MANT:.0%}.',
          'Rinde por envase (metros lineales) = 1.000 cc / (ml por m² x 1,60 m).']:
    y = par(y, '-  ' + s, 8.5, lead=11)
y -= 8
y = h2(y, 'Los tres escenarios (supuestos)')
fil = []
for e, x in ESC.items():
    fil.append([f'{e}  {x["nom"]}', f'{x["cob"]:.0%}', f'{x["carga"]:.0%}'] + [f'{v:.0%}' for v in x['rep']] + [f1(R[e]['Base']['tot'], 1)])
y = tabla(y, ['Escenario', 'Cobertura', 'Carga', 'Blue', 'Yellow', 'Magenta', 'Black', 'ml/m² base'], fil, [160, 55, 50, 45, 50, 55, 50, 67], size=8.5)
for e, x in ESC.items():
    if y < 80: y = nueva('COMO SE CALCULA (continuacion)')
    t(X0, y, f'{e} - {x["nom"]}: {x["det"]}', 8.5, True); y = par(y - 11, x['por'], 8.5, GR, lead=11) - 4

# Página 3: caso 2.500 m
y = nueva('CASO PRACTICO: 2.500 METROS LINEALES = 4.000 m²', 'Nivel BASE de los supuestos. Consumo incluye mantencion. Botellas de 1.000 cc. Tinta a ' + plata(PRECIO_L) + ' el litro.')
for e, x in ESC.items():
    r = R[e]['Base']
    y = h2(y, f'Escenario {e}: {x["nom"]}')
    fil = [['Consumo en 2.500 m (cc)'] + [f0(v) for v in r['caso']] + [f0(sum(r['caso']))],
           ['Consumo por 1.000 m (cc)'] + [f0(v * 1000 / METROS_CASO) for v in r['caso']] + [f0(sum(r['caso']) * 1000 / METROS_CASO)],
           ['Rinde por envase 1.000 cc (metros lineales)'] + [f0(v) for v in r['rinde']] + [''],
           ['Rinde por litro (m² de papel)'] + [f0(1000 / v) for v in r['real']] + [''],
           ['Botellas necesarias'] + [str(math.ceil(v / 1000)) for v in r['caso']] + [str(sum(math.ceil(v / 1000) for v in r['caso']))],
           ['Costo tinta por metro lineal'] + [plata(v * PRECIO_L / 1000) for v in r['ml_ml']] + [plata(sum(r['ml_ml']) * PRECIO_L / 1000)],
           ['Costo tinta por m²'] + [plata(v * PRECIO_L / 1000) for v in r['real']] + [plata(sum(r['real']) * PRECIO_L / 1000)]]
    y = tabla(y, ['Indicador', 'Blue', 'Yellow', 'Magenta', 'Black', 'TOTAL'], fil, [200, 60, 60, 60, 60, 92], resaltar=(2,), size=8.3)
lo = [sum(R[e]['Bajo']['caso']) for e in ESC]; hi = [sum(R[e]['Alto']['caso']) for e in ESC]
y = par(y, 'Sensibilidad: con el supuesto bajo o alto de tinta por canal, el total de 2.500 m queda en ' +
           '; '.join(f'{e}: {f1(lo[i] / 1000, 1)}-{f1(hi[i] / 1000, 1)} litros' for i, e in enumerate(ESC)) +
           '. La diferencia entre escenarios (qué se imprime) pesa tanto como el supuesto de la máquina: por eso hay que medir por tipo de trabajo.', 8.5, GR, lead=11)

# Página 4: proyección mensual y stock
y = nueva('PROYECCION MENSUAL, STOCK Y COMPRAS', f'Mezcla supuesta: {MEZCLA["A"]:.0%} oscura, {MEZCLA["B"]:.0%} multicolor, {MEZCLA["C"]:.0%} alta cobertura. Nivel BASE.')
y = h2(y, 'Consumo y compra mensual según volumen')
fil = []
for v in VOL_MES:
    cc = [m * v for m in MZ['Base']['ml_ml']]
    fil.append([f'{f0(v)} m/mes  ({f0(v * ANCHO)} m²)'] + [f'{f1(x / 1000, 1)} bot.' for x in cc] + [plata(sum(math.ceil(x / 1000) * PRECIO_L for x in cc))])
y = tabla(y, ['Metros lineales por mes', 'Blue', 'Yellow', 'Magenta', 'Black', 'Compra $/mes'], fil, [170, 60, 60, 60, 60, 122], size=8.5)
y = par(y, 'Compra $/mes = botellas enteras de cada color x precio por litro. Las botellas con decimales muestran el consumo real del mes.', 8, GR, lead=10) - 6
y = h2(y, f'Stock mínimo y reposición (con 2.500 m por mes)')
dia = [m * 2500 / DIAS_MES for m in MZ['Base']['ml_ml']]
fil = [['Consumo por día hábil (cc)'] + [f0(d) for d in dia],
       ['Una botella dura (días hábiles)'] + [f1(1000 / d, 1) for d in dia],
       ['STOCK MÍNIMO (botellas, incluye la abierta)'] + [str(math.ceil(d * (LEAD + SEGURIDAD) / 1000) + 1) for d in dia],
       ['Compra mensual (botellas)'] + [str(math.ceil(d * DIAS_MES / 1000)) for d in dia]]
y = tabla(y, ['', 'Blue', 'Yellow', 'Magenta', 'Black'], fil, [232, 75, 75, 75, 75], resaltar=(2,))
y = par(y, f'Stock mínimo = consumo diario x ({LEAD} días que demora el proveedor + {SEGURIDAD} días de colchón), redondeado hacia arriba, + 1 botella abierta en la máquina. '
           'Regla de reposición: cuando un color llega a su stock mínimo, se pide. Con el consumo real medido, el Excel recalcula todo solo.', 8.5, lead=11)
y -= 8
y = h2(y, 'Costo de tinta para presupuestar')
fil = [[f'{e} - {ESC[e]["nom"]}', plata(sum(R[e]['Base']['ml_ml']) * PRECIO_L / 1000), plata(sum(R[e]['Base']['real']) * PRECIO_L / 1000)] for e in ESC]
fil.append(['Mezcla mensual', plata(sum(MZ['Base']['ml_ml']) * PRECIO_L / 1000), plata(sum(MZ['Base']['ml_ml']) / ANCHO * PRECIO_L / 1000)])
y = tabla(y, ['Tipo de trabajo', '$ por metro lineal', '$ por m²'], fil, [262, 135, 135], resaltar=(3,), colcolor=False)
y = par(y, 'Solo tinta. Falta sumar el papel de sublimación (precio del rollo / metros del rollo) para tener el costo de impresión por metro de la receta.', 8.5, GR, lead=11)

# Página 5: método de medición
y = nueva('COMO MEDIR EL CONSUMO REAL DE CADA COLOR', 'En 2-3 meses Playmaker tiene su propio estandar, con datos de su maquina, sus perfiles y sus disenos.')
pasos = [('1. Activar el contador del RIP', 'En RasterLink: Opciones > pestaña Job Control > marcar "Calculate Ink Consumption". Después de procesar (o con "RIP ONLY", sin imprimir), el consumo estimado aparece en las propiedades del trabajo (Results / Performance). Revisar si muestra el detalle por color; si solo da el total, anotar el total y usar la prueba del paso 4.'),
         ('2. Registrar cada trabajo', 'En la hoja "Registro real" del Excel: fecha, OT, tipo de trabajo (A, B o C), metros lineales impresos y cc por color que da el RIP. Una línea por trabajo.'),
         ('3. Registrar cada botella terminada', 'Al vaciar una botella, anotar fecha y color. Marcar en la botella la fecha en que se abrió. Al final del mes, contar también lo que queda en las botellas abiertas (a ojo por el nivel, o pesando: la tinta pesa cerca de 1 gramo por cc, confirmar con la ficha de la Sb610).'),
         ('4. Prueba controlada (una vez)', 'Imprimir 1 metro lineal de cada color sólido al 100% (Blue, Yellow, Magenta, Black) y 1 metro de un diseño típico de cada escenario, con el modo y perfil de producción. Anotar el consumo por color del RIP. Esto reemplaza los supuestos "ml de un canal al 100%" y el reparto por escenario.'),
         ('5. Cerrar el mes', 'El Excel compara cc del RIP con cc de botellas, color por color. La diferencia es la mantención (limpiezas) más el error del RIP: ese factor se aplica a los presupuestos. El "rinde real por envase" del mes es el número para cargar en el sistema.'),
         ('6. Usarlo para presupuestar', 'Con 2-3 meses de datos queda un costo de tinta por metro lineal para cada tipo de trabajo (A, B, C). Al cotizar un pedido se elige el tipo y se multiplica por los metros que ocupa la marcada impresa.'),
         ('Cuidados', 'No cambiar el perfil ICC, el modo (pasadas, dpi) ni el límite de tinta durante la medición sin anotarlo: cada cambio cambia el consumo. Medir separado si hay cambios de papel. Las purgas largas o limpiezas fuertes (por inyectores tapados) se anotan aparte.')]
for a, b in pasos:
    if y < 80: y = nueva('COMO MEDIR (continuacion)')
    t(X0, y, a, 9.5, True, AZ); y = par(y - 12, b, 8.8, lead=11.5) - 6
y -= 4
y = h2(y, 'Fuentes')
for s in ['Mimaki - TS100-1600 especificaciones: mimaki.com/product/inkjet/textile/ts100-1600/specification.html',
          'Mimaki - Catálogo TS100-1600 (DB30339-04): mimaki.com/archives/002/202209/DB30339-04_TS100-1600_EN.pdf',
          'Mimaki USA - Spec sheet TS100-1600: mimakiusa.com/wp-content/uploads/2021/01/Mimaki-TS100-1600-Spec-Sheet-1.pdf',
          'Mimaki - FAQ RasterLink, consumo de tinta: singapore.mimaki.com/support/faq/operation/entry-270605.html',
          'Mimaki Europe - FAQ "How much ink is consumed in an image": mimakieurope.com/faq/how-much-ink-is-consumed-in-an-image-2/',
          'Signs101 - foro "Ink consumption sublimation" (mediciones de un taller): signs101.com/threads/ink-consumption-sublimation.173390/',
          'FJK Sublimation - calculadora de consumo (cifras de proveedor): fjksubli.com/sublimation-ink-consumption-calculator/',
          'Inkbank - guía de tinta de sublimación textil (rendimiento m²/L de proveedor): en.inkbank.com.cn/product-news/sublimation-ink-textile-printing-guide-2026.html']:
    y = par(y, '-  ' + s, 7.8, GR, lead=10)
pie(); c.save()
print('ok', XLSX, PDF, pg[0], 'paginas')
print('rinde base mezcla', [round(v) for v in MZ['Base']['rinde']], 'alto', [round(v) for v in MZ['Alto']['rinde']], 'bajo', [round(v) for v in MZ['Bajo']['rinde']])
for e in ESC: print(e, [round(v) for v in R[e]['Base']['caso']], [round(v) for v in R[e]['Base']['rinde']])
