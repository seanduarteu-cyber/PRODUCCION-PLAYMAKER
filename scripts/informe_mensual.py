"""Informe de gestión mensual PMK: corto plazo (últimos 3 meses) y largo plazo (12 meses).
Uso: python3 informe_mensual.py <pptx_base_con_tema> <salida.pptx>   (datos en datos_pmk.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lxml import etree
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_MARKER_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
import datos_pmk as D

SRC, OUT = sys.argv[1], sys.argv[2]
IN = 914400
C = '{http://schemas.openxmlformats.org/drawingml/2006/chart}'
BG, PANEL, PANEL2, DARK, MUTED = '000000', '2D2D2D', '1E1E1E', '1A1A1A', '4A4A4A'
ORANGE, GREEN_F, GREEN, RED_F, RED, BLUE = 'ED6C23', '1B7F4A', '27AE60', 'C0392B', 'E74C3C', '2C5F8A'
WHITE, GREY, LIGHT, BLACK = 'FFFFFF', '9A9A9A', 'D0D0D0', '000000'

CUR, PREV = D.MES_ACTUAL, D.shift(D.MES_ACTUAL, -1)
W3, W12 = D.ventana(3), D.ventana(12)
T3, T12 = D.total(W3), D.total(W12)
P = {k: D.pct(k) for k in W12 if k in D.MESES}
NOM, NOM_PREV = D.nombre(CUR), D.nombre(PREV)
MES_TXT = f'{NOM.capitalize()} {D.ym(CUR)[0]}'
META = D.METAS.get(CUR)
NEXT = D.shift(CUR, 1); META_NEXT = D.METAS.get(NEXT)
SIN_DATOS = [k for k in W12 if k not in D.MESES]
NOTA12 = (f'* 12 meses = {D.corto(W12[0]).lower()}-{str(D.ym(W12[0])[0])[2:]} a {D.corto(CUR).lower()}-{str(D.ym(CUR)[0])[2:]}'
          + (f'; registro desde may-26 ({T12["meses"]} meses con datos).' if SIN_DATOS else '.'))
F, FP, CLP = D.fmt_num, D.fmt_pct, D.fmt_clp


def dpts(v):
    return (('+' if v > 0 else '−' if v < 0 else '') + D.fmt_num(abs(v), 1) + ' pts')


def sem_txt(p):
    return {'verde': GREEN, 'naranja': ORANGE, 'rojo': RED}[D.semaforo(p)]


def sem_fill(p):
    return {'verde': GREEN_F, 'naranja': ORANGE, 'rojo': RED_F}[D.semaforo(p)]


def flechas(vals, fmt):
    return ' → '.join(fmt(v) for v in vals)


prs = Presentation(SRC)
LAYOUT = prs.slides[0].slide_layout
N_ORIG = len(prs.slides)
E = lambda v: Emu(int(round(v * IN)))


def rect(sl, x, y, w, h, fill, line=None, lw=1.0, dash=False):
    s = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    if fill: s.fill.solid(); s.fill.fore_color.rgb = RGBColor.from_string(fill)
    else: s.fill.background()
    if line:
        s.line.color.rgb = RGBColor.from_string(line); s.line.width = Pt(lw)
        if dash: s.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    else: s.line.fill.background()
    s.shadow.inherit = False
    return s


def write(shape, paras, size=10, color=WHITE, bold=False, italic=False, align='l', anchor='t', space=0):
    tf = shape.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
        if space: p.space_after = Pt(space)
        for run in (para if isinstance(para, list) else [para]):
            text, o = (run, {}) if isinstance(run, str) else run
            r = p.add_run(); r.text = text
            f = r.font; f.name = 'Arial'; f.size = Pt(o.get('size', size))
            f.bold = o.get('bold', bold); f.italic = o.get('italic', italic)
            f.color.rgb = RGBColor.from_string(o.get('color', color))
    return shape


def tb(sl, x, y, w, h, paras, **kw):
    return write(sl.shapes.add_textbox(E(x), E(y), E(w), E(h)), paras if isinstance(paras, list) else [paras], **kw)


def new_slide():
    sl = prs.slides.add_slide(LAYOUT)
    for sp in list(sl.shapes): sp._element.getparent().remove(sp._element)
    return sl


def content(title, subtitle):
    sl = new_slide()
    rect(sl, 0, 0, 10, 5.625, BG); rect(sl, 0, 0, 10, 0.82, PANEL); rect(sl, 0, 0, 0.06, 0.82, ORANGE)
    tb(sl, 0.25, 0.16, 9.5, 0.38, title, size=16, bold=True)
    tb(sl, 0.25, 0.50, 9.5, 0.25, subtitle, size=8.5, italic=True, color=GREY)
    return sl


def framed():
    sl = new_slide()
    rect(sl, 0, 0, 10, 5.625, BG); rect(sl, 0, 0, 0.12, 5.625, ORANGE); rect(sl, 0.12, 5.545, 9.88, 0.08, ORANGE)
    return sl


def chart_clean(ch, legend=False):
    cs = ch._chartSpace
    nf = ('<c:spPr xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
          'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:noFill/><a:ln><a:noFill/></a:ln></c:spPr>')
    cs.find(f'.//{C}plotArea').append(etree.fromstring(nf))
    sp = etree.fromstring(nf); tx = cs.find(f'{C}txPr')
    (tx.addprevious(sp) if tx is not None else cs.find(f'{C}chart').addnext(sp))
    ch.has_title = False; ch.has_legend = legend
    ch.font.name = 'Arial'; ch.font.size = Pt(8); ch.font.color.rgb = RGBColor.from_string(GREY)


def axis_style(ch, vmax=None, show_val=True):
    va = ch.value_axis
    va.has_major_gridlines = show_val
    if show_val:
        va.major_gridlines.format.line.color.rgb = RGBColor.from_string('333333')
        va.format.line.color.rgb = RGBColor.from_string('888888')
        va.tick_labels.font.size = Pt(8); va.tick_labels.font.color.rgb = RGBColor.from_string(GREY)
    else:
        va.visible = False
    if vmax: va.maximum_scale = vmax
    va.minimum_scale = 0
    ca = ch.category_axis
    ca.tick_labels.font.size = Pt(8); ca.tick_labels.font.color.rgb = RGBColor.from_string(LIGHT)
    ca.format.line.color.rgb = RGBColor.from_string('888888')


def cat_labels(keys):
    out = []
    for i, k in enumerate(keys):
        y, m = D.ym(k)
        out.append(D.corto(k, con_anio=(i == 0 or m == 1)))
    return out


def sin_datos_overlay(sl, cx, cw, cy, ch_h, n_vacios, n_total=12, left_pad=0.45):
    if not n_vacios: return
    pw = cw - left_pad - 0.15
    w = pw * n_vacios / n_total
    r = rect(sl, cx + left_pad + 0.03, cy + 0.25, w - 0.06, ch_h - 0.85, None, line=MUTED, lw=0.75, dash=True)
    write(r, ['Sin registro', [(f'(la medición comenzó en {D.corto(D.INICIO_REGISTRO).lower()}-26)', {'size': 7.5})]],
          size=8.5, italic=True, color=GREY, align='c', anchor='m')


def table(sl, x, y, cols, rows, row_h=0.30, gap=0.02, head_h=0.34, size=8):
    """cols: [(titulo, ancho, align)], rows: [dict(cells=[(texto, color, bold)], fill=hex, tcolor=hex)]"""
    cx = x
    rect(sl, x, y, sum(c[1] for c in cols), head_h, ORANGE)
    for t, w, _ in cols:
        tb(sl, cx + 0.04, y, w - 0.08, head_h, t, size=7, bold=True, color=BLACK, align='c', anchor='m'); cx += w
    yy = y + head_h + 0.06
    for r in rows:
        rect(sl, x, yy, sum(c[1] for c in cols), row_h, r['fill'])
        cx = x
        for (t, w, al), (txt, col, b) in zip(cols, r['cells']):
            tb(sl, cx + (0.06 if al == 'l' else 0.03), yy, w - 0.09, row_h, txt, size=size, bold=b, color=col, align=al, anchor='m')
            cx += w
        yy += row_h + gap
    return yy


# ================================================================== 1. PORTADA
sl = framed()
tb(sl, 0.40, 0.85, 9.0, 1.0, 'PLAYMAKER', size=52, bold=True)
tb(sl, 0.40, 1.95, 9.0, 0.5, 'INFORME INTEGRADO — PRODUCCIÓN VS. DEFECTOS', size=16, bold=True, color=ORANGE)
rect(sl, 0.40, 2.58, 4.5, 0.04, ORANGE)
tb(sl, 0.40, 2.70, 9.0, 0.3, 'Control de Ploteo  +  Control de Defectos de Producción', size=12, italic=True, color=GREY)
tb(sl, 0.40, 3.06, 9.0, 0.28, f'{MES_TXT}   |   Corto plazo: últimos 3 meses   ·   Largo plazo: 12 meses*   |   % = reproc/(prod+reproc)',
   size=10, italic=True, color=GREY)
rect(sl, 0.40, 3.60, 5.9, 1.22, PANEL); rect(sl, 0.40, 3.60, 5.9, 0.06, ORANGE)
ok = META and P[CUR] <= META[0]
tb(sl, 0.55, 3.76, 5.6, 1.0, [
    [(f'{NOM}: {FP(P[CUR])} REPROCESO' + (f' (META ≤{META[0]}% ✓)' if ok else (f' (META ≤{META[0]}%)' if META else '')), {'bold': True}),
     (f'   •   {F(D.MESES[CUR]["rep"])} m   •   {D.MESES[CUR]["ev"]} EVENTOS', {})],
    [('ÚLTIMOS 3 MESES:  ', {'bold': True, 'color': ORANGE}), (flechas([P[k] for k in W3], FP), {'color': WHITE})],
    [('12 MESES*:  ', {'bold': True, 'color': ORANGE}),
     (f'{T12["ev"]} EVENTOS  •  {F(T12["pr"])} PRENDAS  •  {CLP(T12["costo"])} CLP COSTO ESTIMADO', {})]],
   size=10, color=WHITE, space=5)
tb(sl, 0.40, 4.92, 6.5, 0.25, NOTA12, size=7, italic=True, color=GREY)
tb(sl, 7.20, 4.95, 2.6, 0.35, 'UN CLUB, UNA FAMILIA', size=9, bold=True, color=ORANGE, align='r')
tb(sl, 7.20, 5.20, 2.6, 0.28, 'www.playmaker.cl', size=8.5, italic=True, color=GREY, align='r')

# ================================================================== 2. RESUMEN EJECUTIVO
sl = content('RESUMEN EJECUTIVO', '% reproceso = reproc ÷ (prod+reproc)   |   Corto plazo = últimos 3 meses   ·   Largo plazo = 12 meses*   |   '
             'Costo: $6.000/m si ya se sublimó · $2.400/m si se frenó antes')
cards = [(f'% REPROCESO {NOM}', FP(P[CUR]), sem_txt(P[CUR]), ' · '.join(f'{D.corto(k).lower()}. {FP(P[k])}' for k in reversed(W3[:-1]))),
         (f'METROS REPROCESADOS {D.corto(CUR)}.', f'{F(D.MESES[CUR]["rep"])} m', ORANGE, '3 meses: ' + flechas([D.MESES[k]['rep'] for k in W3], F) + ' m'),
         ('% REPROCESO 12 MESES*', FP(T12['pct']), sem_txt(T12['pct']), f'{F(T12["rep"])} m reprocesados'),
         ('COSTO 12 MESES*', CLP(T12['costo']), ORANGE, f'según etapa · {D.corto(CUR).lower()}. {CLP(D.costo(CUR))}')]
for i, (lab, val, col, sub) in enumerate(cards):
    x = 0.18 + i * 2.38
    rect(sl, x, 0.95, 2.26, 1.08, PANEL); rect(sl, x, 0.95, 2.26, 0.05, ORANGE)
    tb(sl, x + 0.14, 1.07, 2.0, 0.22, lab, size=7.5, bold=True, color=GREY)
    tb(sl, x + 0.14, 1.27, 2.0, 0.48, val, size=22, bold=True, color=col)
    tb(sl, x + 0.14, 1.75, 2.0, 0.22, sub, size=8, italic=True, color=GREY)
tb(sl, 0.18, 2.16, 6, 0.22, 'CORTO PLAZO — ÚLTIMOS 3 MESES   ·   LARGO PLAZO — 12 MESES*', size=8.5, bold=True, color=ORANGE)
cols = [('MES', 1.70, 'l'), ('MTS PROD.', 1.05, 'c'), ('MTS REPROC.', 1.05, 'c'), ('% REPROC.', 0.95, 'c'), ('EVENTOS', 0.85, 'c'),
        ('PRENDAS', 0.85, 'c'), ('COSTO POR ETAPA**', 1.65, 'c'), ('BASE (P+R)', 1.54, 'c')]
rows = []
for i, k in enumerate(W3):
    d = D.MESES[k]
    rows.append(dict(fill=PANEL if i % 2 == 0 else PANEL2, cells=[
        (f'{D.nombre(k)}{"*" if d.get("est") else ""} {D.ym(k)[0]}', WHITE, True), (F(d['prod']) + 'm', WHITE, False),
        (F(d['rep']) + 'm', WHITE, False), (FP(P[k]), sem_txt(P[k]), True), (str(d['ev']), WHITE, False),
        (F(d['pr']), WHITE, False), (CLP(D.costo(k)), ORANGE, False), (F(d['prod'] + d['rep']) + 'm', WHITE, False)]))
for lab, t, fill, tc in [('TOTAL 3 MESES', T3, '3A3A3A', WHITE), ('TOTAL 12 MESES*', T12, ORANGE, BLACK)]:
    rows.append(dict(fill=fill, cells=[(lab, tc, True), (F(t['prod']) + 'm', tc, True), (F(t['rep']) + 'm', tc, True),
                                       (FP(t['pct']), tc if fill == ORANGE else sem_txt(t['pct']), True), (str(t['ev']), tc, True),
                                       (F(t['pr']), tc, True), (CLP(t['costo']), tc, True), (F(t['prod'] + t['rep']) + 'm', tc, True)]))
yy = table(sl, 0.18, 2.42, cols, rows, row_h=0.30)
dprev, dcur = D.MESES[PREV], D.MESES[CUR]
var = lambda a, b: f'{(b - a) / a * 100:+.0f}%'.replace('+', '+').replace('-', '−')
tb(sl, 0.18, yy + 0.08, 9.6, 0.24, [[(f'Variación {D.corto(CUR).lower()}. vs {D.corto(PREV).lower()}.:  ', {'bold': True, 'color': ORANGE}),
                                     ('% reproceso ' + dpts(P[CUR] - P[PREV])
                                      + f'   ·   metros reprocesados {var(dprev["rep"], dcur["rep"])}   ·   eventos {var(dprev["ev"], dcur["ev"])}'
                                      + f'   ·   producción {var(dprev["prod"], dcur["prod"])}', {})]], size=8.5, color=LIGHT)
tb(sl, 0.18, 4.86, 9.6, 0.56, [NOTA12 + ' Julio extrapolado (registro de ploteo incompleto).',
                               '** Costo = metros de reproceso del Control de Ploteo × $6.000/m si la pieza ya se había sublimado, o × $2.400/m si se frenó antes '
                               '(sólo mesa + ploteo). La etapa sale de la línea ETAPA del chat; sin dato se asume completo. Detalle en la slide 3.'],
   size=7, italic=True, color=GREY)

# ================================================================== 3. COSTO POR ETAPA
sl = content('COSTO DE REPROCESO — SEGÚN ETAPA DE DETECCIÓN',
             'Costo por metro $6.000 = tela 40% + armado de mesa y ploteo 40% + sublimación 20%   |   Metros reales del Control de Ploteo')
tb(sl, 0.18, 0.95, 6.0, 0.24, '¿QUÉ SE PIERDE EN CADA REPROCESO?  (por metro)', size=9, bold=True, color=ORANGE)
x = 0.18
for lab, fr, col, tc in [('ARMADO DE MESA + PLOTEO  ·  40%  ·  $2.400', 0.4, GREEN_F, WHITE), ('TELA  ·  40%  ·  $2.400', 0.4, ORANGE, BLACK),
                         ('SUBLIMACIÓN  ·  20%  ·  $1.200', 0.2, 'B4501A', WHITE)]:
    w = 9.64 * fr - (0.03 if fr != 0.2 else 0)
    r = rect(sl, x, 1.24, w, 0.42, col); write(r, [lab], size=8, bold=True, color=tc, align='c', anchor='m'); x += 9.64 * fr
tb(sl, 0.18, 1.74, 3.86, 0.22, '▲ FRENADO ANTES DE SUBLIMAR → sólo se reimprime: $2.400/m', size=8, bold=True, color=GREEN)
tb(sl, 4.04, 1.74, 5.78, 0.22, 'YA SUBLIMADO → se pierden las 3 partes: $6.000/m ▲', size=8, bold=True, color=ORANGE, align='r')
cols = [('MES', 1.30, 'l'), ('SOLO REIMPR.', 1.10, 'c'), ('COMPLETO', 1.10, 'c'), ('COSTO (CLP)', 1.30, 'c')]
rows = []
for i, k in enumerate(W3):
    d = D.MESES[k]
    rows.append(dict(fill=PANEL if i % 2 == 0 else PANEL2, cells=[(D.nombre(k), WHITE, True), (F(d['antes']) + ' m', GREEN, False),
                                                                  (F(d['rep'] - d['antes']) + ' m', WHITE, False), (CLP(D.costo(k)), ORANGE, False)]))
for lab, t, fill, tc in [('TOTAL 3 MESES', T3, '3A3A3A', WHITE), ('12 MESES*', T12, ORANGE, BLACK)]:
    rows.append(dict(fill=fill, cells=[(lab, tc, True), (F(t['antes']) + ' m', tc if fill == ORANGE else GREEN, True),
                                       (F(t['rep'] - t['antes']) + ' m', tc, True), (CLP(t['costo']), tc, True)]))
yy = table(sl, 0.18, 2.12, cols, rows, row_h=0.28)
share = [100 * D.MESES[k]['antes'] / D.MESES[k]['rep'] for k in W3]
tb(sl, 0.18, yy + 0.10, 4.8, 0.40, [[('FRENADO ANTES DE SUBLIMAR:  ', {'bold': True, 'color': GREY}),
                                     ('  →  '.join(f'{D.corto(k)} {FP(s)}' for k, s in zip(W3, share)), {'bold': True, 'color': GREEN})]], size=8.5)
tb(sl, 0.18, yy + 0.52, 4.8, 0.7, [NOTA12 + ' Julio extrapolado con la misma proporción de etapas del resto del período.',
                                   'Desde octubre la etapa sale de la línea ETAPA del chat. Sin evidencia se asume reproceso completo. Corte no valorizado.'],
   size=7, italic=True, color=GREY)
for i, (lab, val, sub, acc, vc) in enumerate([
        ('SOLO REIMPRESIÓN (12 MESES*)', CLP(T12['antes'] * D.COSTO_M_ANTES), f'{F(T12["antes"])} m · {100 * T12["antes"] / T12["rep"]:.0f}% de los metros', GREEN_F, GREEN),
        ('REPROCESO COMPLETO (12 MESES*)', CLP((T12['rep'] - T12['antes']) * D.COSTO_M_COMPLETO),
         f'{F(T12["rep"] - T12["antes"])} m · {100 - 100 * T12["antes"] / T12["rep"]:.0f}% de los metros', ORANGE, ORANGE)]):
    x = 5.30 + i * 2.32
    rect(sl, x, 2.12, 2.20, 1.00, PANEL); rect(sl, x, 2.12, 2.20, 0.05, acc)
    tb(sl, x + 0.14, 2.24, 1.95, 0.22, lab, size=7, bold=True, color=GREY)
    tb(sl, x + 0.14, 2.44, 1.95, 0.42, val, size=18, bold=True, color=vc)
    tb(sl, x + 0.14, 2.84, 1.95, 0.22, sub, size=8, italic=True, color=GREY)
ahorro = T12['antes'] * (D.COSTO_M_COMPLETO - D.COSTO_M_ANTES)
r = rect(sl, 5.30, 3.26, 4.52, 0.92, ORANGE)
tb(sl, 5.45, 3.32, 4.22, 0.82, [[(f'DETECTAR ANTES DE SUBLIMAR AHORRÓ {CLP(ahorro)} (12 MESES*)', {'bold': True, 'size': 9.5})],
                                [(f'Corto plazo: en {NOM.lower()} el {share[-1]:.0f}% de los metros se frenó antes de sublimar '
                                  f'({share[-2]:.0f}% en {NOM_PREV.lower()}, {share[-3]:.0f}% en {D.nombre(W3[0]).lower()}). Cada metro frenado a tiempo ahorra $3.600.', {'size': 8})]],
   color=BLACK, space=3)
rect(sl, 5.30, 4.30, 4.52, 0.88, DARK)
tb(sl, 5.45, 4.37, 4.22, 0.22, 'COSTO 12 MESES* (SEGÚN ETAPA)', size=8, bold=True, color=GREY)
tb(sl, 5.45, 4.55, 4.22, 0.36, CLP(T12['costo']) + ' CLP', size=16, bold=True, color=ORANGE)
tb(sl, 5.45, 4.92, 4.22, 0.20, f'Últimos 3 meses: {CLP(T3["costo"])}   ·   Si todo fuera completo (12m): {CLP(T12["rep"] * D.COSTO_M_COMPLETO)}',
   size=7.5, italic=True, color=GREY)

# ================================================================== 4. LARGO PLAZO: PRODUCCIÓN VS REPROCESO
sl = content('LARGO PLAZO — METROS PRODUCCIÓN VS. REPROCESO (12 MESES)',
             '% = reproc ÷ (prod+reproc)   |   Base excluye moldes, muestras y pruebas de color   |   ' + NOTA12[2:])
cd = CategoryChartData(); cd.categories = cat_labels(W12)
cd.add_series('Producción (m)', [round(D.MESES[k]['prod']) if k in D.MESES else None for k in W12])
cd.add_series('Reproceso (m)', [round(D.MESES[k]['rep']) if k in D.MESES else None for k in W12])
CX, CY, CW, CH = 0.18, 0.90, 5.85, 4.30
ch = sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, E(CX), E(CY), E(CW), E(CH), cd).chart
chart_clean(ch, legend=True)
ch.legend.include_in_layout = False; ch.legend.font.size = Pt(8); ch.legend.font.color.rgb = RGBColor.from_string(LIGHT)
from pptx.enum.chart import XL_LEGEND_POSITION
ch.legend.position = XL_LEGEND_POSITION.BOTTOM
pl = ch.plots[0]; pl.gap_width = 45; pl.overlap = 100
for s_, col in zip(pl.series, (GREEN_F, ORANGE)):
    s_.format.fill.solid(); s_.format.fill.fore_color.rgb = RGBColor.from_string(col)
    d = s_.data_labels; d.show_value = True; d.number_format = '#,##0'; d.number_format_is_linked = False
    d.position = XL_LABEL_POSITION.CENTER; d.font.size = Pt(7.5); d.font.color.rgb = RGBColor.from_string(WHITE)
axis_style(ch, vmax=2500)
sin_datos_overlay(sl, CX, CW, CY, CH, len(SIN_DATOS))
rect(sl, 6.20, 0.90, 3.62, 4.30, PANEL); rect(sl, 6.20, 0.90, 3.62, 0.05, ORANGE)
tb(sl, 6.35, 1.00, 3.35, 0.30, 'CORTO PLAZO — ÚLTIMOS 3 MESES', size=10, bold=True, color=ORANGE)
TINT = {'verde': '0A2D17', 'naranja': '2D1A0A', 'rojo': '2D0A0A'}
EST = {'verde': '✓ BAJO', 'naranja': '⚠ MOD.', 'rojo': '✗ ALTO'}
for i, k in enumerate(W3):
    y = 1.40 + i * 0.50
    sm = D.semaforo(P[k])
    rect(sl, 6.35, y, 3.35, 0.44, TINT[sm])
    tb(sl, 6.48, y, 1.30, 0.44, D.nombre(k) + ('*' if D.MESES[k].get('est') else ''), size=9.5, bold=True, anchor='m')
    tb(sl, 7.75, y, 1.10, 0.44, FP(P[k]), size=16, bold=True, color=sem_txt(P[k]), align='c', anchor='m')
    tb(sl, 8.80, y, 0.85, 0.44, EST[sm], size=8.5, bold=True, color=sem_txt(P[k]), align='r', anchor='m')
both_green = all(D.semaforo(P[k]) == 'verde' for k in W3[-2:])
msg = ('DOS MESES SEGUIDOS EN VERDE' if both_green else f'{NOM}: {FP(P[CUR])}')
r = rect(sl, 6.20, 2.98, 3.62, 0.62, GREEN_F if D.semaforo(P[CUR]) == 'verde' else ORANGE)
tb(sl, 6.35, 3.02, 3.38, 0.56, [msg, [(f'{D.corto(CUR).capitalize()}. vs {D.corto(PREV).lower()}.: ' + dpts(P[CUR] - P[PREV])
                                       + (f'  ·  meta del mes ≤{META[0]}% ✓' if ok else ''), {'bold': False, 'size': 8.5})]],
   size=9, bold=True, color=WHITE, anchor='m')
rect(sl, 6.20, 3.70, 3.62, 1.50, DARK)
tb(sl, 6.35, 3.78, 3.38, 0.22, 'LARGO PLAZO — 12 MESES*', size=8, bold=True, color=GREY)
tb(sl, 6.35, 4.00, 3.38, 0.40, f'{FP(T12["pct"])} promedio', size=16, bold=True, color=sem_txt(T12['pct']))
mx = max(P, key=P.get)
tb(sl, 6.35, 4.42, 3.38, 0.72, [f'{F(T12["rep"])} m reprocesados de {F(T12["prod"] + T12["rep"])} m impresos.',
                                f'Máximo: {FP(P[mx])} en {D.nombre(mx).lower()}  ·  Mínimo: {FP(min(P.values()))} en {D.nombre(min(P, key=P.get)).lower()}.'],
   size=8, color=LIGHT, space=2)
tb(sl, 0.18, 5.25, 9.5, 0.25, '* Julio extrapolado. % real: 11,4%. Datos según Control de Ploteo al cierre de cada mes.', size=7, italic=True, color=GREY)

# ================================================================== 5. LARGO PLAZO: TENDENCIA %
sl = content(f'LARGO PLAZO — TENDENCIA % REPROCESO (12 MESES) · META ≤{D.META_FINAL}%',
             f'% = reproc ÷ (prod+reproc)   |   {D.corto(CUR).capitalize()}.: {FP(P[CUR])}' + (f' (meta del mes ≤{META[0]}% cumplida)' if ok else '')
             + (f' — bajo la meta de diciembre (≤{D.META_FINAL}%)' if P[CUR] <= D.META_FINAL else ''))
cd = CategoryChartData(); cd.categories = cat_labels(W12)
cd.add_series('% real', [round(P[k], 1) if k in P else None for k in W12])
cd.add_series('Meta del mes (hoja de ruta)', [D.METAS[k][0] if k in D.METAS else None for k in W12])
cd.add_series(f'Meta ≤{D.META_FINAL}%', [D.META_FINAL] * 12)
CX, CY, CW, CH = 0.18, 0.88, 6.35, 4.35
ch = sl.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, E(CX), E(CY), E(CW), E(CH), cd).chart
chart_clean(ch, legend=True)
ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False
ch.legend.font.size = Pt(8); ch.legend.font.color.rgb = RGBColor.from_string(LIGHT)
for s_, col in zip(ch.plots[0].series, (WHITE, '5B8DBE', GREEN)):
    s_.format.line.color.rgb = RGBColor.from_string(col); s_.format.line.width = Pt(2.25); s_.smooth = False
    s_.marker.style = XL_MARKER_STYLE.CIRCLE; s_.marker.size = 7
    s_.marker.format.fill.solid(); s_.marker.format.fill.fore_color.rgb = RGBColor.from_string(col)
    s_.marker.format.line.color.rgb = RGBColor.from_string(col)
real = ch.plots[0].series[0]
for i, k in enumerate(W12):
    if k not in P: continue
    d = real.points[i].data_label
    d.has_text_frame = True; d.text_frame.text = f'{P[k]:.1f}'
    rr = d.text_frame.paragraphs[0].runs[0]; rr.font.size = Pt(9); rr.font.bold = True
    rr.font.color.rgb = RGBColor.from_string(WHITE if k != CUR else sem_txt(P[k]))
    v = P[k]
    d.position = XL_LABEL_POSITION.BELOW if v < D.META_FINAL else (XL_LABEL_POSITION.RIGHT if v < D.META_FINAL + 1.5 else XL_LABEL_POSITION.ABOVE)
axis_style(ch, vmax=16)
sin_datos_overlay(sl, CX, CW, CY, CH, len(SIN_DATOS), left_pad=0.40)
rect(sl, 6.70, 0.88, 3.12, 4.35, PANEL); rect(sl, 6.70, 0.88, 3.12, 0.05, ORANGE)
tb(sl, 6.85, 0.97, 2.9, 0.30, 'HOJA DE RUTA Q4 2026', size=10, bold=True, color=ORANGE)
tb(sl, 6.85, 1.31, 2.9, 0.22, 'Meta mensual de % reproceso y metros', size=8, italic=True, color=GREY)
ACC = {'2026-09': 'Control diario papel y calandra', '2026-10': 'Chequeo mesa 100% antes imprimir',
       '2026-11': 'Revisión semanal del equipo', '2026-12': 'META — KPI operativo consolidado'}
for i, (k, (mp, mm)) in enumerate(sorted(D.METAS.items())):
    y = 1.60 + i * 0.68
    done = k in P
    hit = done and P[k] <= mp
    rect(sl, 6.85, y, 0.55, 0.58, GREEN_F if hit else (ORANGE if k == max(D.METAS) else DARK))
    tb(sl, 6.85, y, 0.55, 0.58, D.corto(k) + '.', size=9, bold=True, color=WHITE if (hit or k != max(D.METAS)) else BLACK, align='c', anchor='m')
    rect(sl, 7.45, y, 0.72, 0.58, DARK)
    tb(sl, 7.45, y + 0.06, 0.72, 0.22, f'≤{mp}%', size=10, bold=True, color=ORANGE, align='c')
    tb(sl, 7.45, y + 0.31, 0.72, 0.20, f'≤{mm}m', size=8, italic=True, color=GREY, align='c')
    lines = ([[(f'✓ Real: {FP(P[k])} · {F(D.MESES[k]["rep"])}m', {'bold': True, 'color': GREEN})]] if hit else
             ([[(f'Real: {FP(P[k])} · {F(D.MESES[k]["rep"])}m', {'bold': True, 'color': ORANGE})]] if done else []))
    tb(sl, 8.22, y + 0.02, 1.52, 0.56, lines + [ACC.get(k, '')], size=8, color=WHITE, anchor='m')
rect(sl, 6.70, 4.48, 3.12, 0.75, ORANGE)
tb(sl, 6.85, 4.55, 2.88, 0.62, [f'META Q4: ≤100m/mes', [(f'{D.META_FINAL}% (prod+reproc) = ≤1 de cada 20m reimpresos', {'bold': False, 'size': 8.5})]],
   size=9.5, bold=True, color=BLACK, space=4)
tb(sl, 0.18, 5.25, 6.3, 0.27, '* Jul. extrapolado. Blanco = % real. Azul = meta del mes según hoja de ruta. Verde = meta ≤5% en dic.', size=7, italic=True, color=GREY)

# ================================================================== 6. MOTIVOS
sl = content('MOTIVOS DE REPROCESO — CAUSA RAÍZ REAL',
             'Verificado registro a registro contra chat WA. Papel/calandra → Mesa. Pendientes reales separados.   |   Izquierda: largo plazo · Derecha: corto plazo')
rect(sl, 4.95, 0.95, 0.04, 4.15, ORANGE)
C12 = D.causas_total(W12)
rect(sl, 0.18, 0.95, 4.70, 0.28, PANEL)
tb(sl, 0.25, 0.95, 4.55, 0.28, f'LARGO PLAZO — 12 MESES*  ({sum(C12)} eventos)', size=8.5, bold=True, color=ORANGE, anchor='m')
mx = max(C12)
for i, (cat, v) in enumerate(zip(D.CATEGORIAS, C12)):
    y = 1.38 + i * 0.47
    top = v == mx
    tb(sl, 0.18, y, 1.18, 0.34, cat, size=8, bold=top, color=WHITE if top else GREY, anchor='m')
    w = max(2.45 * v / mx, 0.02)
    rect(sl, 1.40, y, w, 0.34, ORANGE if top else MUTED)
    tb(sl, 1.40 + w + 0.06, y, 1.0, 0.34, f'{v}  {FP(100 * v / sum(C12))}', size=8, bold=top, color=ORANGE if top else GREY, anchor='m')
rect(sl, 5.12, 0.95, 4.70, 0.28, PANEL)
tb(sl, 5.20, 0.95, 4.55, 0.28, 'CORTO PLAZO — ÚLTIMOS 3 MESES  (eventos por mes)', size=8.5, bold=True, color=ORANGE, anchor='m')
cols = [('CAUSA', 1.40, 'l')] + [(D.corto(k), 0.72, 'c') for k in W3] + [(f'{D.corto(CUR)} VS {D.corto(PREV)}', 1.14, 'c')]
rows = []
ms = [D.CAUSAS_MES[k] for k in W3]
for i, cat in enumerate(D.CATEGORIAS):
    vals = [m[i] for m in ms]
    dlt = vals[-1] - vals[-2]
    trend = ('▼ −' + str(-dlt), GREEN) if dlt < 0 else (('▲ +' + str(dlt), RED) if dlt > 0 else ('=', GREY))
    vmax = max(vals)
    cells = [(cat, WHITE, False)] + [(str(v), ORANGE if (j == len(vals) - 1) else LIGHT, j == len(vals) - 1) for j, v in enumerate(vals)] + [(trend[0], trend[1], True)]
    rows.append(dict(fill=PANEL if i % 2 == 0 else PANEL2, cells=cells))
tot = [sum(m) for m in ms]
rows.append(dict(fill=ORANGE, cells=[('TOTAL', BLACK, True)] + [(str(t), BLACK, True) for t in tot] +
                 [(f'{(tot[-1] - tot[-2]) / tot[-2] * 100:+.0f}%'.replace('-', '−'), BLACK, True)]))
table(sl, 5.12, 1.30, cols, rows, row_h=0.36, gap=0.03, head_h=0.32, size=9)
top_cur = sorted(zip(D.CAUSAS_MES[CUR], D.CATEGORIAS), reverse=True)[:3]
tb(sl, 0.18, 5.22, 9.6, 0.25, f'Naranja = mayor del período   |   ▲▼ = {NOM.lower()} vs {NOM_PREV.lower()}   |   {NOM.capitalize()}: '
   + ', '.join(f'{c} {v}' for v, c in top_cur) + '  —  Verificado vs chat WA', size=7, italic=True, color=GREY)

# ================================================================== 7. PLAN DE ACCIÓN
sl = content('PLAN DE ACCIÓN — 5 PASOS CONCRETOS', f'Estado a {NOM.lower()} {D.ym(CUR)[0]}')
uso = D.ETAPA_CHAT.get(CUR)
steps = [(RED_F, '01', 'URGENTE', 'Completar registro ploteo julio', 'Solo 221m vs ~2.100m esperados. Recuperar datos para validar el 11,4%.'),
         (ORANGE, '02', 'PRIORITARIO', 'Agregar "Mesa / Papel" al chat WA', f'{C12[0]} eventos de papel/calandra (12 meses*) categorizados como otra causa. Nueva categoría en PENDIENTES PMK.'),
         (ORANGE, '03', 'PRIORITARIO', 'Umbral alerta 8% mensual en ploteo', 'Verde <7%, Naranja 7–10%, Rojo >10% sobre (prod+reproc). Dashboard ya lo calcula.'),
         (BLUE, '04', 'IMPORTANTE', 'Unificar categorías y registrar etapa',
          (f'La línea ETAPA ya se usa en el chat ({uso[0]} de {uso[1]} registros en {D.corto(CUR).lower()}.). ' if uso else '')
          + 'Falta la columna "Etapa detectada" en el Control de Ploteo.'),
         (GREEN_F, '05', 'PRÓXIMO', 'Ingresar ventas en Excel Maestro', 'Columna Venta en Datos_Maestro lista. Activa % pérdida sobre venta automático.')]
for i, (col, n, tag, t, d) in enumerate(steps):
    x = 0.18 if i < 3 else 5.15
    y = 0.95 + (i % 3) * 1.42
    rect(sl, x, y, 0.50, 1.28, col)
    tb(sl, x, y, 0.50, 1.28, n, size=16, bold=True, color=BLACK, align='c', anchor='m')
    rect(sl, x + 0.50, y, 4.25 if i < 3 else 4.25, 1.28, PANEL)
    tb(sl, x + 0.62, y + 0.07, 3.95, 0.22, tag, size=7.5, bold=True, color=col if col != GREEN_F else GREEN)
    tb(sl, x + 0.62, y + 0.28, 3.95, 0.34, t, size=10, bold=True)
    tb(sl, x + 0.62, y + 0.62, 3.95, 0.60, d, size=8.5, color=GREY)
rect(sl, 5.15, 3.79, 4.75, 1.28, ORANGE)
tb(sl, 5.32, 3.89, 4.35, 1.1, [['META Q4 2026'], [(' ', {'size': 6})],
                               f'% reproceso: {FP(P[CUR])} en {D.corto(CUR).lower()}. (12 meses*: {FP(T12["pct"])}) → mantener ≤{D.META_FINAL}%',
                               f'Reproc. {F(D.MESES[CUR]["rep"])}m en {D.corto(CUR).lower()}. → meta ≤100m/mes' + (' ✓' if D.MESES[CUR]['rep'] <= 100 else '')],
   size=10, bold=True, color=BLACK)

# ================================================================== 8. CIERRE
sl = framed()
p0, p1 = P[W3[0]], P[CUR]
verbo = 'BAJÓ' if p1 < p0 else ('SUBIÓ' if p1 > p0 else 'SE MANTUVO')
tb(sl, 0.45, 0.55, 8.5, 2.5, [f'EL REPROCESO {verbo}', f'DE {FP(p0)} → {FP(p1)}', f'EN {len(W3) - 1} MESES.' if len(W3) - 1 != 2 else 'EN DOS MESES.'],
   size=30, bold=True)
evs = [D.MESES[k]['ev'] for k in W3]
tb(sl, 0.45, 3.10, 9.0, 0.65, ('Y LOS PEDIDOS TAMBIÉN: ' if evs[-1] < evs[0] else 'LOS PEDIDOS: ') + ' → '.join(map(str, evs)) + '.',
   size=18, bold=True, color=ORANGE)
rect(sl, 0.45, 3.95, 9.20, 0.82, PANEL)
tb(sl, 0.62, 3.95, 8.90, 0.82, [f'12 meses*: {CLP(T12["costo"])} CLP costo estimado   |   {F(T12["rep"])}m reprocesados   |   {FP(T12["pct"])} promedio   |   '
                                f'{D.corto(CUR).capitalize()}.: {F(D.MESES[CUR]["rep"])}m (meta ≤100m' + (' ✓)' if D.MESES[CUR]['rep'] <= 100 else ')')],
   size=10, align='c', anchor='m')
tb(sl, 0.45, 5.18, 9.20, 0.28, 'UN CLUB, UNA FAMILIA   |   www.playmaker.cl', size=8.5, color=GREY, align='c')

# ------------------------------------------------------------------
lst = prs.slides._sldIdLst
for sid in list(lst)[:N_ORIG]:
    rid = sid.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
    lst.remove(sid); prs.part.drop_rel(rid)
prs.core_properties.title = f'PMK Informe {MES_TXT}'
prs.save(OUT)
print('saved', OUT)
