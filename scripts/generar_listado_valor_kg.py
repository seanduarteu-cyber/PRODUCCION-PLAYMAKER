# Listado único de telas: valor por kg (neto) y, aparte, las telas en que no hay certeza de si el precio es por kg o por metro.
# La segunda parte es rellenable (campos TELA_xxx__unidad / __precio / __se_usa / __obs, los lee importar_formulario_receta.py).
# Uso: python3 -I scripts/generar_listado_valor_kg.py PMK_Receta_Produccion.xlsx salida.pdf
import sys, re
from openpyxl import load_workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.utils import simpleSplit

SRC, DST = sys.argv[1:3]
wb = load_workbook(SRC, data_only=True); P, D = wb['Precios'], wb['Despiece']
N = lambda x: isinstance(x, (int, float))
def san(s): return re.sub(r'[^A-Za-z0-9]+', '_', str(s or '')).strip('_')[:40]
def plata(x): return '$' + f'{x:,.0f}'.replace(',', '.') if N(x) else '-'
def dec(x): return f'{x:.2f}'.replace('.', ',') if N(x) else '-'
uso = {}
for r in range(5, 1005):
    t, m = D.cell(r, 5).value, D.cell(r, 1).value
    if t and m: uso.setdefault(str(t).strip().upper(), set()).add(str(m).split(' · ')[0])
DUDA_UNIDAD = {'GABARDINA 7Z': 'Anotaste "kg", pero $1.490/kg es muy barato (las demas por kg: $5.544 a $14.084). ¿Es por metro?'}

telas = []
for r in range(5, 125):
    n = P.cell(r, 1).value
    if not n: continue
    telas.append(dict(n=n, tipo=P.cell(r, 2).value, prov=P.cell(r, 3).value, u=P.cell(r, 4).value, pr=P.cell(r, 5).value,
                      iva=P.cell(r, 6).value, kgm=P.cell(r, 7).value, an=P.cell(r, 8).value, kg=P.cell(r, 9).value, m=P.cell(r, 10).value,
                      nota=P.cell(r, 12).value or ''))
dudosas = [t for t in telas if t['u'] not in ('kg', 'metro') or t['n'] in DUDA_UNIDAD]
seguras = sorted([t for t in telas if t not in dudosas], key=lambda t: t['n'])

W, H = letter; X0, X1 = 30, W - 30
AZUL = HexColor('#1F3864'); GRIS = HexColor('#595959'); FONDO = HexColor('#EAF1FB'); LINEA = HexColor('#BFBFBF'); BANDA = HexColor('#F2F2F2'); AMA = HexColor('#FFF2CC')
c = canvas.Canvas(DST, pagesize=letter); c.setTitle('PMK - Valor por kg de telas'); form = c.acroForm
pag = [0]
def txt(x, y, s, size=8.5, bold=False, color=black, right=False):
    c.setFont('Helvetica-Bold' if bold else 'Helvetica', size); c.setFillColor(color)
    (c.drawRightString if right else c.drawString)(x, y, s); c.setFillColor(black)
def campo(n, x, y, w, v='', h=13):
    form.textfield(name=n, tooltip=n, x=x, y=y - 3, width=w, height=h, value=str(v or ''), fontName='Helvetica', fontSize=8.5,
                   borderWidth=0.5, borderColor=LINEA, fillColor=FONDO, textColor=black, forceBorder=True)
def pie():
    txt(X0, 16, 'Playmaker - Valor por kg de telas (neto, sin IVA). 16-11-2026.', 7, color=GRIS); txt(X1, 16, f'Pagina {pag[0]}', 7, color=GRIS, right=True)
def nueva(t, s=''):
    if pag[0]: pie(); c.showPage()
    pag[0] += 1
    c.setFillColor(AZUL); c.rect(0, H - 52, W, 52, fill=1, stroke=0)
    txt(X0, H - 29, t, 15, True, white); txt(X0, H - 44, s, 8.5, False, white)
    return H - 74

# ---------- 1. Listado único con valor por kg
y = nueva('VALOR POR KG DE TELAS', f'{len(seguras)} telas con la unidad clara. Las {len(dudosas)} en que no se sabe si el precio es por kg o por metro van en la parte 2.')
COL = [(0, 'Tela'), (190, 'Proveedor'), (300, 'Se compra'), (350, 'Precio actual'), (425, 'Kg por metro'), ]
def enc(y):
    c.setFillColor(HexColor('#D9D9D9')); c.rect(X0, y - 4, X1 - X0, 15, fill=1, stroke=0)
    for x, t in COL: txt(X0 + x + 3, y, t, 8, True)
    txt(X1 - 6, y, '$ POR KG (neto)', 8, True, right=True)
    return y - 17
y = enc(y)
for i, t in enumerate(seguras):
    if y < 70: y = nueva('VALOR POR KG DE TELAS (continuacion)'); y = enc(y)
    if i % 2: c.setFillColor(BANDA); c.rect(X0, y - 4, X1 - X0, 14, fill=1, stroke=0)
    txt(X0 + 3, y, t['n'][:34] + (' (1)' if t['n'] == 'MONTESIMONE TRAINING (fut pro)' else ''), 8.5, True)
    txt(X0 + 193, y, str(t['prov'] or '-')[:20]); txt(X0 + 303, y, t['u'])
    txt(X0 + 353, y, plata(t['pr']) + ('/kg' if t['u'] == 'kg' else '/m')); txt(X0 + 428, y, dec(t['kgm']))
    if N(t['kg']): txt(X1 - 6, y, plata(t['kg']), 9.5, True, right=True)
    else:
        c.setFillColor(AMA); c.rect(X0 + 538, y - 4, X1 - X0 - 538, 14, fill=1, stroke=0)
        txt(X1 - 6, y, 'falta pesar 1 m', 8, False, HexColor('#9C5700'), right=True)
    y -= 14
y -= 6
for l in ('Por kg: el precio de la factura ya es el valor por kg. Por metro: $ por kg = precio por metro / kilos por metro.',
          '"falta pesar 1 m": se compra por metro y no tiene el peso de 1 metro lineal; su precio por metro esta en "Precio actual".',
          '(1) Montesimone: los kilos por metro (0,19) estan escritos sobre un borron; si pesa mas, su valor por kg baja.'):
    txt(X0, y, l, 7.5, color=GRIS); y -= 10

# ---------- 2. Telas sin certeza de unidad
y = nueva('TELAS POR CONFIRMAR: ¿EL PRECIO ES POR KG O POR METRO?',
          'Marca la unidad, corrige el precio si cambio y escribe NO en "Se usa" si ya no se compra. Devuelve el PDF o una foto.')
for l in simpleSplit('Estas telas vienen del sistema anterior, que anotaba todo "por kg". Pero ya se vio que varias Pro (Montesimone, Jacquard, '
                     'Falcao, Novak) en realidad se compran por metro. Como referencia: las telas que se compran por kg cuestan entre $5.544 y $14.084 el kg; '
                     'las que se compran por metro, entre $757 y $8.352 el metro. Un precio bajo (menos de $4.500) probablemente es por metro.',
                     'Helvetica', 8.3, X1 - X0):
    txt(X0, y, l, 8.3); y -= 11
y -= 16
for t in dudosas:
    caja = 66
    if y - caja < 40: y = nueva('TELAS POR CONFIRMAR (continuacion)')
    k = f'TELA_{san(t["n"])}'
    form.textfield(name=f'{k}__nombre', tooltip='tela', x=-100, y=-100, width=1, height=1, value=t['n'])
    c.setStrokeColor(LINEA); c.setFillColor(HexColor('#FAFAFA')); c.rect(X0, y - caja + 12, X1 - X0, caja, fill=1, stroke=1); c.setStrokeColor(black)
    txt(X0 + 8, y, t['n'], 10.5, True, AZUL)
    pista = 'parece POR METRO' if N(t['pr']) and t['pr'] < 4500 else 'parece POR KG'
    txt(X1 - 8, y, pista, 8, True, HexColor('#9C5700'), right=True)
    y -= 14
    usado = ', '.join(sorted(uso.get(t['n'].upper(), [])))
    datos = [('Proveedor', t['prov'] or 'sin dato'), ('Tipo', t['tipo'] or 'sin dato'), ('Precio registrado', plata(t['pr'])),
             ('Kg por metro', dec(t['kgm']) if N(t['kgm']) else 'sin dato'), ('Ancho', (dec(t['an']) + ' m') if N(t['an']) else 'sin dato')]
    x = X0 + 8
    for a, b in datos:
        txt(x, y, a + ':', 7.5, color=GRIS); txt(x + c.stringWidth(a + ':', 'Helvetica', 7.5) + 3, y, str(b), 8, True)
        x += 108
    y -= 12
    det = DUDA_UNIDAD.get(t['n']) or ('Usada en moldes: ' + usado if usado else 'No esta como tela por defecto en ningun molde de la receta.')
    det += f'   Si es por kg: {plata(t["pr"])}/kg.  Si es por metro: {plata(t["pr"])}/m.'
    txt(X0 + 8, y, det[:175], 7.5, color=GRIS); y -= 16
    txt(X0 + 8, y, 'Es por (kg / metro):', 8, True); campo(f'{k}__unidad', X0 + 100, y, 55, t['u'] or '')
    txt(X0 + 170, y, 'Precio actual:', 8, True); campo(f'{k}__precio', X0 + 232, y, 65)
    txt(X0 + 310, y, 'Se usa (Si/No):', 8, True); campo(f'{k}__se_usa', X0 + 378, y, 35)
    txt(X0 + 425, y, 'Kg por metro:', 8, True); campo(f'{k}__kgm', X0 + 484, y, 54, dec(t['kgm']) if N(t['kgm']) else '')
    y -= caja - 42
pie(); c.save(); print('ok', len(seguras), 'con unidad clara;', len(dudosas), 'por confirmar;', pag[0], 'paginas')
