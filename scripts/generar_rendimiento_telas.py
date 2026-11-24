# Lista de rendimiento de telas: kilos por metro, metros por kilo, m² por kilo y gramaje (g/m²), con su valor por metro.
# Uso: python3 -I scripts/generar_rendimiento_telas.py PMK_Receta_Produccion.xlsx salida.pdf
import sys
from openpyxl import load_workbook
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white

SRC, DST = sys.argv[1:3]
P = load_workbook(SRC, data_only=True)['Precios']
N = lambda x: isinstance(x, (int, float)) and x > 0
telas = []
for r in range(5, 125):
    n = P.cell(r, 1).value
    if not n or P.cell(r, 4).value not in ('kg', 'metro'): continue
    telas.append(dict(n=n, prov=P.cell(r, 3).value, u=P.cell(r, 4).value, kgm=P.cell(r, 7).value, an=P.cell(r, 8).value,
                      kg=P.cell(r, 9).value, m=P.cell(r, 10).value, nota=P.cell(r, 12).value or ''))
con = sorted([t for t in telas if N(t['kgm'])], key=lambda t: -1 / t['kgm'])
sin = sorted([t for t in telas if not N(t['kgm'])], key=lambda t: t['n'])

W, H = landscape(letter); X0, X1 = 30, W - 30
AZ = HexColor('#1F3864'); GR = HexColor('#595959'); BAN = HexColor('#F2F2F2'); AM = HexColor('#FFF2CC')
c = canvas.Canvas(DST, pagesize=(W, H)); c.setTitle('PMK - Rendimiento de telas')
pg = [0]
def d(x, k=2): return f'{x:,.{k}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
def plata(x): return '$' + f'{x:,.0f}'.replace(',', '.') if N(x) else '-'
def t(x, y, s, size=8.5, bold=False, color=black, right=False):
    c.setFont('Helvetica-Bold' if bold else 'Helvetica', size); c.setFillColor(color)
    (c.drawRightString if right else c.drawString)(x, y, s); c.setFillColor(black)
def pie():
    t(X0, 16, 'Playmaker - Rendimiento de telas. Peso de 1 metro lineal (todo el ancho) del registro de telas y de la receta. 24-11-2026.', 7, color=GR)
    t(X1, 16, f'Pagina {pg[0]}', 7, color=GR, right=True)
def nueva(tit, sub):
    if pg[0]: pie(); c.showPage()
    pg[0] += 1
    c.setFillColor(AZ); c.rect(0, H - 52, W, 52, fill=1, stroke=0)
    t(X0, H - 29, tit, 15, True, white); t(X0, H - 44, sub, 8.5, False, white)
    return H - 74
COL = [('Tela', 0, False), ('Proveedor', 190, False), ('Compra', 300, False), ('Ancho util', 395, True), ('Kilos por metro', 470, True),
       ('METROS POR KILO', 560, True), ('m² por kilo', 612, True), ('Gramaje g/m²', 670, True), ('$ por metro', 732, True)]
def enc(y):
    c.setFillColor(HexColor('#D9D9D9')); c.rect(X0, y - 4, X1 - X0, 15, fill=1, stroke=0)
    for h, x, der in COL: t(X0 + x + (0 if der else 3), y, h, 7.8, True, right=der)
    return y - 17
y = nueva('RENDIMIENTO DE TELAS', f'{len(con)} telas con el peso de 1 metro, de la que mas rinde a la que menos. Al final: {len(sin)} telas sin pesar.')
y = enc(y)
for i, x in enumerate(con):
    if y < 70: y = nueva('RENDIMIENTO DE TELAS (continuacion)', ''); y = enc(y)
    if 'borr' in x['nota']: c.setFillColor(AM); c.rect(X0, y - 4, X1 - X0, 14, fill=1, stroke=0)
    elif i % 2: c.setFillColor(BAN); c.rect(X0, y - 4, X1 - X0, 14, fill=1, stroke=0)
    mpk = 1 / x['kgm']; m2 = mpk * x['an'] if N(x['an']) else None; gr = x['kgm'] / x['an'] * 1000 if N(x['an']) else None
    vals = [x['n'][:34] + (' (1)' if 'borr' in x['nota'] else ''), str(x['prov'] or '-')[:20], 'por kg' if x['u'] == 'kg' else 'por metro',
            (d(x['an']) + ' m') if N(x['an']) else '-', d(x['kgm'], 2) + ' kg', d(mpk, 2) + ' m', d(m2, 2) if m2 else '-', d(gr, 0) if gr else '-', plata(x['m'])]
    for k, (h, xx, der) in enumerate(COL):
        t(X0 + xx + (0 if der else 3), y, vals[k], 8.5, k in (0, 5), right=der)
    y -= 14
y -= 6
for l in ('Metros por kilo = 1 / kilos por metro: cuantos metros lineales salen de 1 kg. m² por kilo = metros por kilo x ancho util. Gramaje = kilos por metro / ancho x 1.000.',
          'Para telas que se compran por kg, el rendimiento convierte el precio: $ por metro = $ por kg / metros por kilo. Mas metros por kilo = tela mas liviana y mas metros por cada kilo pagado.',
          '(1) Montesimone: los kilos por metro (0,19) estan escritos sobre un borron. Conviene pesar 1 metro de nuevo.'):
    t(X0, y, l, 7.6, color=GR); y -= 10
y -= 10
if y < 160: y = nueva('RENDIMIENTO DE TELAS (continuacion)', '')
t(X0, y, f'TELAS SIN PESAR ({len(sin)}): falta el peso de 1 metro lineal para calcular su rendimiento', 11, True, AZ); y -= 18
c.setFillColor(HexColor('#D9D9D9')); c.rect(X0, y - 4, X1 - X0, 15, fill=1, stroke=0)
for h, x in (('Tela', 0), ('Proveedor', 230), ('Compra', 360), ('Ancho util', 450), ('Kilos por metro (anotar)', 560)): t(X0 + x + 3, y, h, 7.8, True)
y -= 17
for i, x in enumerate(sin):
    if y < 40: y = nueva('RENDIMIENTO DE TELAS (continuacion)', '')
    if i % 2: c.setFillColor(BAN); c.rect(X0, y - 4, X1 - X0, 14, fill=1, stroke=0)
    t(X0 + 3, y, x['n'], 8.5, True); t(X0 + 233, y, str(x['prov'] or '-')[:24]); t(X0 + 363, y, 'por kg' if x['u'] == 'kg' else 'por metro')
    t(X0 + 453, y, (d(x['an']) + ' m') if N(x['an']) else '-')
    c.setStrokeColor(HexColor('#BFBFBF')); c.line(X0 + 563, y - 2, X0 + 680, y - 2); c.setStrokeColor(black)
    y -= 15
pie(); c.save(); print('ok', len(con), 'con peso,', len(sin), 'sin peso,', pg[0], 'paginas')
for x in con: print(x['n'], x['kgm'], round(1 / x['kgm'], 2), x['an'])
