# Hoja (PDF rellenable) con las telas a las que les falta algún dato, y la lista de las que ya están completas.
# Los campos usan los nombres que lee importar_formulario_receta.py (TELA_xxx__nombre/precio/unidad/iva/kgm/ancho).
# Uso: python3 -I scripts/generar_hoja_telas_faltantes.py PMK_Receta_Produccion.xlsx salida.pdf
import sys, re
from openpyxl import load_workbook
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.utils import simpleSplit

SRC, DST = sys.argv[1:3]
P = load_workbook(SRC, data_only=True)['Precios']
N = lambda x: isinstance(x, (int, float))
def san(s): return re.sub(r'[^A-Za-z0-9]+', '_', str(s or '')).strip('_')[:40]
def plata(x): return '$' + f'{x:,.0f}'.replace(',', '.') if N(x) else ''
def dec(x): return f'{x:.2f}'.replace('.', ',') if N(x) else ''

pesar, confirmar, sin_datos, ok = [], [], [], []
for r in range(5, 125):
    n = P.cell(r, 1).value
    if not n: continue
    t = dict(n=n, prov=P.cell(r, 3).value, u=P.cell(r, 4).value, pr=P.cell(r, 5).value, iva=P.cell(r, 6).value,
             kgm=P.cell(r, 7).value, an=P.cell(r, 8).value, kg=P.cell(r, 9).value, nota=P.cell(r, 12).value or '')
    duda = t['nota'].split('REVISAR:')[1].strip() if 'REVISAR:' in t['nota'] else ''
    duda = re.sub(r'\s*(Precio actualizado|Ancho útil medido|Precio actual releído).*$', '', duda)
    if t['u'] not in ('kg', 'metro'): sin_datos.append(t)
    elif not N(t['kgm']): pesar.append(t)
    elif duda: t['duda'] = duda; confirmar.append(t)
    else: ok.append(t)

W, H = landscape(letter); X0, X1 = 30, W - 30
AZUL = HexColor('#1F3864'); GRIS = HexColor('#595959'); FONDO = HexColor('#EAF1FB'); LINEA = HexColor('#BFBFBF'); BANDA = HexColor('#F2F2F2')
c = canvas.Canvas(DST, pagesize=(W, H)); c.setTitle('PMK - Telas: datos que faltan'); form = c.acroForm
pag = [0]
def campo(n, x, y, w, v='', h=13):
    form.textfield(name=n, tooltip=n, x=x, y=y - 3, width=w, height=h, value=str(v or ''), fontName='Helvetica', fontSize=8.5,
                   borderWidth=0.5, borderColor=LINEA, fillColor=FONDO, textColor=black, forceBorder=True)
def txt(x, y, s, size=8.5, bold=False, color=black):
    c.setFont('Helvetica-Bold' if bold else 'Helvetica', size); c.setFillColor(color); c.drawString(x, y, s); c.setFillColor(black)
def pie():
    txt(X0, 16, 'Playmaker - Telas: datos que faltan. Completar los campos azules y devolver el PDF (o una foto) para actualizar la receta.', 7, color=GRIS)
    c.drawRightString(X1, 16, f'Pagina {pag[0]}')
def nueva(t, s=''):
    if pag[0]: pie(); c.showPage()
    pag[0] += 1
    c.setFillColor(AZUL); c.rect(0, H - 50, W, 50, fill=1, stroke=0)
    txt(X0, H - 28, t, 15, True, white); txt(X0, H - 42, s, 8.5, False, white)
    return H - 70
def sec(y, t, sub):
    if y < 120: y = nueva('TELAS: DATOS QUE FALTAN (continuacion)')
    txt(X0, y, t, 11, True, AZUL); txt(X0, y - 12, sub, 8, color=GRIS); return y - 28
def enc(y, cols):
    c.setFillColor(HexColor('#D9D9D9')); c.rect(X0, y - 4, X1 - X0, 14, fill=1, stroke=0)
    for x, t in cols: txt(X0 + x + 2, y, t, 7.5, True)
    return y - 17
def nombre(k, t, y):   # nombre fijo, oculto como campo para el importador
    form.textfield(name=f'{k}__nombre', tooltip='tela', x=-100, y=-100, width=1, height=1, value=t['n'])
    txt(X0 + 2, y, t['n'][:38], 8.5, True)

y = nueva('TELAS: DATOS QUE FALTAN', f'{len(pesar)} por pesar  -  {len(confirmar)} por confirmar  -  {len(sin_datos)} sin datos nuevos  -  {len(ok)} completas (al final)')
# 1. Falta pesar 1 metro
y = sec(y, f'1. FALTA PESAR 1 METRO LINEAL ({len(pesar)})', 'Pesar 1 metro lineal (todo el ancho) en kg, ej: 0,27. Con eso sale el $ por metro y el $ por kg.')
COL = [(0, 'Tela'), (215, 'Proveedor'), (330, 'Compra en'), (385, 'Precio actual'), (465, 'Ancho util (m)'), (545, 'KILOS POR METRO'), (640, 'Observacion')]
y = enc(y, COL)
for t in pesar:
    if y < 40: y = nueva('TELAS: DATOS QUE FALTAN (continuacion)'); y = enc(y, COL)
    k = f'TELA_{san(t["n"])}'; nombre(k, t, y)
    txt(X0 + 217, y, str(t['prov'] or '-')[:22]); txt(X0 + 332, y, t['u'])
    txt(X0 + 387, y, plata(t['pr']) + ('/kg' if t['u'] == 'kg' else '/m')); campo(f'{k}__ancho', X0 + 465, y, 60, dec(t['an']))
    campo(f'{k}__kgm', X0 + 545, y, 80); campo(f'{k}__obs', X0 + 640, y, X1 - X0 - 640)
    y -= 17
y -= 10
# 2. Confirmar
y = sec(y, f'2. CONFIRMAR ({len(confirmar)})', 'Ya tienen todos los datos, pero hay una duda. Si esta bien, deja el campo como esta; si no, corrigelo.')
COL2 = [(0, 'Tela'), (215, 'Precio actual'), (300, 'Kilos por metro'), (380, 'Duda'), (640, 'Proveedor')]
y = enc(y, COL2)
for t in confirmar:
    if y < 40: y = nueva('TELAS: DATOS QUE FALTAN (continuacion)'); y = enc(y, COL2)
    k = f'TELA_{san(t["n"])}'; nombre(k, t, y)
    campo(f'{k}__precio', X0 + 215, y, 75, f'{t["pr"]:,.0f}'.replace(',', '.') if N(t['pr']) else '')
    campo(f'{k}__kgm', X0 + 300, y, 70, dec(t['kgm']))
    for j, ln in enumerate(simpleSplit(t['duda'], 'Helvetica', 7, 250)[:2]): txt(X0 + 382, y + 2 - 8 * j, ln, 7)
    campo(f'{k}__proveedor_ok', X0 + 640, y, X1 - X0 - 640, t['prov'])
    y -= 19
y -= 10
# 3. Sin datos nuevos
y = sec(y, f'3. SIN DATOS NUEVOS ({len(sin_datos)}) - solo tienen el precio del sistema anterior',
        'Si ya no se usa, escribe NO en "Se usa". Si se usa: precio de la ultima factura, si es por kg o metro, IVA, kilos por metro y ancho util.')
COL3 = [(0, 'Tela'), (190, 'Precio anterior'), (265, 'Se usa'), (310, 'Precio actual'), (390, 'kg / metro'), (450, 'IVA S/N'), (500, 'Kilos por metro'), (575, 'Ancho util (m)'), (650, 'Proveedor')]
y = enc(y, COL3)
for t in sin_datos:
    if y < 40: y = nueva('TELAS: DATOS QUE FALTAN (continuacion)'); y = enc(y, COL3)
    k = f'TELA_{san(t["n"])}'; nombre(k, t, y)
    txt(X0 + 192, y, plata(t['pr']), 8.5, color=GRIS); campo(f'{k}__se_usa', X0 + 265, y, 38)
    campo(f'{k}__precio', X0 + 310, y, 72); campo(f'{k}__unidad', X0 + 390, y, 52); campo(f'{k}__iva', X0 + 450, y, 42)
    campo(f'{k}__kgm', X0 + 500, y, 68); campo(f'{k}__ancho', X0 + 575, y, 68); campo(f'{k}__proveedor_ok', X0 + 650, y, X1 - X0 - 650, t['prov'])
    y -= 17
# 4. Completas
y = nueva('TELAS COMPLETAS', f'{len(ok)} telas con precio actual, kilos por metro y ancho util, sin dudas pendientes. No hay que hacer nada.')
COL4 = [(0, 'Tela'), (240, 'Proveedor'), (390, 'Compra en'), (460, 'Kilos por metro'), (550, 'Ancho util'), (630, '$ POR KG neto')]
y = enc(y, COL4)
for i, t in enumerate(sorted(ok, key=lambda t: t['n'])):
    if i % 2: c.setFillColor(BANDA); c.rect(X0, y - 4, X1 - X0, 15, fill=1, stroke=0)
    txt(X0 + 2, y, t['n'], 9, True); txt(X0 + 242, y, str(t['prov'] or '-')[:28]); txt(X0 + 392, y, t['u'])
    txt(X0 + 462, y, dec(t['kgm'])); txt(X0 + 552, y, dec(t['an']) + ' m'); txt(X0 + 632, y, plata(t['kg']), 9, True)
    y -= 15
pie(); c.save(); print('ok', len(pesar), len(confirmar), len(sin_datos), len(ok), pag[0], 'paginas')
