"""Informe de gestión: septiembre -> octubre 2026 (mayo–octubre)."""
import copy, sys
from lxml import etree
from pptx import Presentation
from pptx.util import Emu
from pptx.chart.data import CategoryChartData

SRC, OUT = sys.argv[1], sys.argv[2]
IN = 914400
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
C = '{http://schemas.openxmlformats.org/drawingml/2006/chart}'
ORANGE, GREEN, GREEN_TXT, GREY, BAR_GREY, WHITE = 'ED6C23', '1B7F4A', '27AE60', '9A9A9A', '4A4A4A', 'FFFFFF'

prs = Presentation(SRC)
S = list(prs.slides)
_next = [5000]


def ids(sl):
    return {s.shape_id: s for s in sl.shapes}


def set_paras(sh, texts):
    tx = sh.text_frame._txBody
    ps = tx.findall(f'{A}p')
    while len(ps) < len(texts):
        ps[-1].addnext(copy.deepcopy(ps[-1])); ps = tx.findall(f'{A}p')
    for p, t in zip(ps, texts):
        rs = p.findall(f'{A}r')
        for r in rs[1:]:
            p.remove(r)
        rs[0].find(f'{A}t').text = t
    for p in ps[len(texts):]:
        tx.remove(p)


def T(sh, t):
    set_paras(sh, [t])


def color(sh, hexv, bold=None):
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            rp = r._r.find(f'{A}rPr')
            rp.find(f'{A}solidFill/{A}srgbClr').set('val', hexv)
            if bold is True: rp.set('b', '1')
            elif bold is False and 'b' in rp.attrib: del rp.attrib['b']


def fill(sh, hexv):
    sh._element.find(f'{P}spPr/{A}solidFill/{A}srgbClr').set('val', hexv)


def geom(sh, x=None, y=None, w=None, h=None):
    if x is not None: sh.left = Emu(round(x * IN))
    if y is not None: sh.top = Emu(round(y * IN))
    if w is not None: sh.width = Emu(round(max(w, 0.02) * IN))
    if h is not None: sh.height = Emu(round(h * IN))


def dup(sl, sh, dx=0.0, dy=0.0, after=None):
    el = copy.deepcopy(sh._element)
    (after._element if after is not None else sh._element).addnext(el)
    _next[0] += 1
    c = el.find(f'.//{P}cNvPr'); c.set('id', str(_next[0])); c.set('name', f'Shape {_next[0]}')
    new = [s for s in sl.shapes if s._element is el][0]
    new.left = Emu(sh.left + round(dx * IN)); new.top = Emu(sh.top + round(dy * IN))
    return new


# ================================================================ 1. portada
s = ids(S[0])
T(s[9], 'Octubre 2026   |   Indicadores verificados contra chat WA   |   % = reproc/(prod+reproc)')
T(s[12], '264 EVENTOS   •   1.216 PRENDAS   •   $5.948.184 CLP COSTO ESTIMADO')
T(s[1001], 'OCTUBRE: 4,1% REPROCESO (META ≤8% ✓)   •   95 m   •   28 EVENTOS')

# ================================================================ 2. resumen ejecutivo
sl = S[1]; s = ids(sl)
T(s[10], '1.028 m'); T(s[11], 'may–oct (jul. estimado)')
T(s[15], '8.1%'); T(s[20], '264')
T(s[25], '$5.948.184'); T(s[26], 'CLP may–oct · según etapa')
ROW = 260604 / IN
for i in range(107, 123):
    geom(s[i], y=s[i].top / IN + ROW)
for i, t in zip(range(110, 123, 2), ['11.670m', '1.028m', '8.1%', '264', '1.216', '$5.948.184', '12.697m']):
    T(s[i], t)
last = s[1017]
vals = ['OCTUBRE 2026', '2.195m', '95m', '4.1%', '28', '171', '$531.852', '2.290m']
k = 0
for i in range(91, 107):                     # fila de agosto (relleno 1E1E1E) dos filas más abajo
    last = dup(sl, s[i], dy=2 * ROW, after=last)
    if i % 2 == 0:
        T(last, vals[k]); k += 1
        if k == 4:
            color(last, GREEN)
geom(s[123], y=4.86, h=0.56)
set_paras(s[123], [
    '* Julio extrapolado (registro de ploteo incompleto). Octubre según Control de Ploteo al 31-oct (2 filas de producción del 14-oct sin metros).',
    '** Costo = metros de reproceso del Control de Ploteo × $6.000/m si la pieza ya se había sublimado, o × $2.400/m si se frenó antes de sublimar '
    '(sólo mesa + ploteo). Desde octubre la etapa sale de la línea ETAPA del chat; sin dato se asume completo. Detalle en la slide 3.'])

# ================================================================ 3. costo por etapa
sl = S[2]; s = ids(sl)
STEP = s[2031].top / IN - s[2023].top / IN
for i in range(2063, 2071):
    geom(s[i], y=s[i].top / IN + STEP)
last = s[2062]
vals = {2051: 'OCTUBRE', 2052: '10 m', 2053: '85 m', 2054: '$531.852'}
for i in range(2047, 2055):                  # fila de agosto (1E1E1E) dos filas más abajo
    last = dup(sl, s[i], dy=2 * STEP, after=last)
    if i in vals:
        T(last, vals[i])
for i, t in zip(range(2068, 2071), ['61 m', '967 m', '$5.948.184']):
    T(s[i], t)
geom(s[2071], y=4.62, h=0.82)
set_paras(s[2071], [
    '* Julio extrapolado (245 m) con la misma proporción de etapas del resto del período.',
    'Desde octubre la etapa sale de la línea ETAPA del chat (24 de 28 registros la traen). Sin evidencia se asume reproceso completo. Corte no valorizado.'])
T(s[2075], '$145.224'); T(s[2076], '61 m · 6% de los metros')
T(s[2080], '$5.802.960'); T(s[2081], '967 m · 94% de los metros')
set_paras(s[2083], ['DETECTAR ANTES DE SUBLIMAR AHORRÓ $217.836',
                    'En octubre, con la línea ETAPA, el 11% de los metros se frenó antes de sublimar (5% en septiembre). Cada metro frenado a tiempo ahorra $3.600.'])
T(s[2085], 'COSTO TOTAL MAY–OCT (SEGÚN ETAPA)'); T(s[2086], '$5.948.184 CLP')
T(s[2087], 'Si todo se contara como reproceso completo: $6.166.020')

# ================================================================ 4. proyección (barras)
sl = S[3]; s = ids(sl)
ch = [x for x in sl.shapes if x.has_chart][0].chart
cd = CategoryChartData(); cd.categories = ['MAY', 'JUN', 'JUL*', 'AGO', 'SEP', 'OCT']
cd.add_series('Producción (m)', (1890, 1864, 1901, 1722, 2098, 2195))
cd.add_series('Reproceso (m)', (133, 149, 245, 279, 127, 95))
ch.replace_data(cd)
rows = [(11, 12, 13, 14), (15, 16, 17, 18), (19, 20, 21, 22), (23, 24, 25, 26), (1018, 1019, 1020, 1021)]
Y0, ST, H = 1.38, 0.38, 0.34
for k, grp in enumerate(rows):
    y = Y0 + k * ST
    geom(s[grp[0]], y=y, h=H)
    for t in grp[1:]:
        geom(s[t], y=y + 0.01)
last = s[1021]; new = []
for i in (1018, 1019, 1020, 1021):
    last = dup(sl, s[i], dy=ST, after=last); new.append(last)
T(new[1], 'OCTUBRE'); T(new[2], '4.1%'); T(new[3], '✓ BAJO')
set_paras(s[28], ['DOS MESES SEGUIDOS EN VERDE', 'Oct. 4,1% (meta ≤8% ✓)  ·  bajo la meta de dic. (5%)'])
T(s[31], '$5.948.184 CLP')
T(s[32], '* Julio extrapolado. % real: 11,4%. Octubre según Control de Ploteo al 31-oct.')

# ================================================================ 5. tendencia (líneas)
sl = S[4]; s = ids(sl)
ch = [x for x in sl.shapes if x.has_chart][0].chart
cd = CategoryChartData(); cd.categories = ['MAY', 'JUN', 'JUL*', 'AGO', 'SEP.', 'OCT.', 'NOV.', 'DIC.']
cd.add_series('% Real / estimado', (6.6, 7.4, 11.4, 13.9, 5.7, 4.1, None, None))
cd.add_series('Meta mensual (hoja de ruta)', (None, None, None, None, 11, 8, 6, 5))
cd.add_series('Meta ≤5%', (5,) * 8)
ch.replace_data(cd)
dl = ch._chartSpace.findall(f'.//{C}ser')[0].find(f'{C}dLbls')
p4 = [d for d in dl.findall(f'{C}dLbl') if d.find(f'{C}idx').get('val') == '4'][0]
p5 = copy.deepcopy(p4); p5.find(f'{C}idx').set('val', '5'); p5.find(f'{C}dLblPos').set('val', 'b')
p4.addnext(p5)
T(s[6], '% = reproc ÷ (prod+reproc)  |  Oct.: 4,1% (meta del mes ≤8% cumplida) — ya bajo la meta de diciembre (≤5%)')
fill(s[18], GREEN); color(s[19], WHITE)
s[23]._element.remove(s[23]._element.find(f'{P}txBody'))
s[23]._element.append(copy.deepcopy(s[17]._element.find(f'{P}txBody')))
geom(s[23], y=s[18].top / IN + 0.03, h=0.52)
set_paras(s[23], ['✓ Real: 4,1% · 95m', 'Chequeo mesa 100% antes imprimir'])

# ================================================================ 6. motivos
sl = S[5]; s = ids(sl)
T(s[9], 'ACUMULADO MAYO – OCTUBRE  (264 eventos)')
T(s[34], 'OCTUBRE 2026  (28 eventos) — Verificado')
BY0, BST, BH, MAXW = 1.24, 0.405, 0.34, 2.55


def bars(groups, x0, vals, total):
    mx = max(vals)
    for k, ((b, lab, val), v) in enumerate(zip(groups, vals)):
        y = BY0 + k * BST
        w = MAXW * v / mx
        geom(s[b], x=x0, y=y, w=w, h=BH)
        geom(s[val], x=x0 + max(w, 0.02) + 0.06)
        T(s[val], f'{v}  {v / total * 100:.1f}%')
        top = v == mx
        fill(s[b], ORANGE if top else BAR_GREY)
        color(s[lab], WHITE if top else GREY, bold=top)
        color(s[val], ORANGE if top else GREY, bold=top)


bars([(11 + 3 * k, 12 + 3 * k, 13 + 3 * k) for k in range(7)], 1.40, [83, 67, 39, 15, 26, 18, 16], 264)
bars([(36 + 3 * k, 37 + 3 * k, 38 + 3 * k) for k in range(7)], 6.34, [3, 7, 9, 2, 6, 1, 0], 28)
COLX = [1.50 + 0.54 * i for i in range(6)]
hdr = [59, 60, 61, 62, 1022]
oct_hdr = dup(sl, s[1022], after=s[1022]); T(oct_hdr, 'OCT')
for x, sh in zip(COLX, [s[i] for i in hdr] + [oct_hdr]):
    geom(sh, x=x, w=0.50)
TAB = {(64, 65, 66, 67, 68, 1023): [10, 23, 22, 15, 10, 3],
       (70, 71, 72, 73, 74, 1024): [6, 20, 10, 12, 12, 7],
       (76, 77, 78, 79, 80, 1025): [2, 5, 4, 12, 7, 9]}
for (lab, *cells), v in TAB.items():
    geom(s[lab], w=1.24)
    grey_src = next(s[c] for c, x in zip(cells, v) if x != max(v))
    n = dup(sl, grey_src, after=s[cells[-1]])
    geom(n, y=s[cells[-1]].top / IN)
    for x, sh, val in zip(COLX, [s[c] for c in cells] + [n], v):
        geom(sh, x=x, w=0.50); T(sh, str(val))
        color(sh, ORANGE if val == max(v) else GREY, bold=(val == max(v)))
T(s[1026], 'CAMBIOS VS. SEPTIEMBRE (EVENTOS)')
set_paras(s[1027], ['Mesa/Papel 10 → 3 ▼     Sublimación 12 → 7 ▼     Confección 6 → 1 ▼',
                    'Diseño/Ficha 7 → 0 ▼     Corte 7 → 6 ▼     Pendiente 7 → 9 ▲     Faltó imp. 2 → 2 =',
                    'Total: 51 → 28 eventos (−45%) y metros de reproceso 127 → 95 m (−25%).'])
T(s[81], '▲ Naranja = valor más alto   |   Octubre: Pendientes de taller pasa a Nº1 (9 ev.), Sublimación Nº2 (7), Corte Nº3 (6); Diseño/Ficha sin casos  —  Verificado vs chat WA')

# ================================================================ 7. plan de acción
s = ids(S[6])
T(s[17], '83 eventos de papel/calandra (may–oct) categorizados como otra causa. Nueva categoría en PENDIENTES PMK.')
T(s[29], 'La línea ETAPA ya se usa en el chat (24 de 28 registros en oct.). Falta la columna "Etapa detectada" en el Control de Ploteo (sigue en v4).')
set_paras(s[38], ['% reproceso: 4,1% en oct. → mantener ≤5%', 'Reproc. 95m en oct. → meta ≤100m/mes ✓'])

# ================================================================ 8. cierre
s = ids(S[7])
set_paras(s[5], ['EL REPROCESO BAJÓ', 'DE 13,9% → 4,1%', 'EN DOS MESES.'])
T(s[6], 'Y LOS PEDIDOS TAMBIÉN: 57 → 51 → 28.')
T(s[8], '$5.948.184 CLP costo estimado   |   1.028m reprocesados   |   83 eventos Mesa/Papel   |   Oct.: 95m (meta ≤100m ✓)')

prs.core_properties.title = 'PMK Informe Octubre 2026'
prs.save(OUT)
print('saved', OUT)
