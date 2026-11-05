"""Presentación mensual para el equipo de producción (contexto e historial primero, resultado al final).
Sin costos, ventas ni nombres de personas. Para un mes nuevo: actualizar sólo el bloque DATOS.
Uso: python3 equipo_mensual.py <pptx_base_con_tema> <salida.pptx>"""
import sys
from lxml import etree
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# ================================================================== DATOS DEL MES
MES, MES_ANT, MES_SIG = 'OCTUBRE 2026', 'septiembre', 'noviembre'
# (mes, metros impresos, metros reprocesados, % reproceso, pedidos en el chat)
HIST = [('MAYO', 1890, 133, 6.6, 25), ('JUNIO', 1864, 149, 7.4, 55), ('JULIO*', 1901, 245, 11.4, 48),
        ('AGOSTO', 1722, 279, 13.9, 57), ('SEPTIEMBRE', 2098, 127, 5.7, 51)]
ACT = ('OCTUBRE', 2195, 95, 4.1, 28)
# hoja de ruta: (mes corto, meta %, meta metros, resultado real o None)
RUTA = [('SEP', 11, 235, 5.7), ('OCT', 8, 165, None), ('NOV', 6, 121, None), ('DIC', 5, 100, None)]
# pedidos del chat por etapa: (etapa, mes anterior, mes actual)
CAUSAS = [('Armado de mesa / papel', 10, 3), ('Sublimación', 12, 7), ('Pendientes en taller', 7, 9), ('Corte', 7, 6),
          ('Diseño / ficha', 7, 0), ('Confección', 6, 1), ('Faltó impresión', 2, 2)]
LECTURAS = [  # (color, ícono, título, texto)
    ('27AE60', '▼', 'Bajaron', 'Armado de mesa / papel (10 → 3), sublimación (12 → 7), confección (6 → 1) y diseño / ficha (7 → 0).'),
    ('E74C3C', '▲', 'Subieron', 'Pendientes en taller (7 → 9): hoy es la etapa con más casos y el foco de noviembre.'),
    ('ED6C23', '●', 'Nuevo: la línea ETAPA', '24 de 28 pedidos la usaron, y 8 se frenaron antes de sublimar: ahí no se pierde tela.')]
CIERRE_NUMEROS = 'Más trabajo y menos pedidos. ¿Y el resultado?'
CORTOS = ['MAY', 'JUN', 'JUL*', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']      # rótulos de los gráficos
FRASE_RESULTADO = 'De cada 100 metros, cerca de 4 fueron para repetir. En septiembre eran 6 y en agosto, 14.'
TILE_3 = ('≤6%', 'próxima meta: noviembre (≤121 m) · ya estamos bajo la meta de diciembre (5%)')
MENSAJE_MEJORA = ['¡FELICITACIONES, EQUIPO!', 'Dos meses seguidos bajando: de 13,9% a 4,1%. Ya estamos bajo la meta de diciembre.', 'Este logro es de todos.']
DESAFIO = 'PRÓXIMO DESAFÍO: MANTENERNOS BAJO EL 5%   ·   NOVIEMBRE ≤6%'
# ==================================================================

SRC, OUT = sys.argv[1], sys.argv[2]
IN = 914400
P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
C = '{http://schemas.openxmlformats.org/drawingml/2006/chart}'
BG, PANEL, PANEL2, MUTED = '000000', '2D2D2D', '1E1E1E', '4A4A4A'
ORANGE, GREEN_F, GREEN, RED_F, RED, WHITE, GREY, LIGHT, BLACK = (
    'ED6C23', '1B7F4A', '27AE60', 'C0392B', 'E74C3C', 'FFFFFF', '9A9A9A', 'D0D0D0', '000000')
MESES_LARGOS = {'SEP': 'SEPTIEMBRE', 'OCT': 'OCTUBRE', 'NOV': 'NOVIEMBRE', 'DIC': 'DICIEMBRE'}

PCT, PCT_ANT = ACT[3], HIST[-1][3]
META_MES = next(r[1] for r in RUTA if MESES_LARGOS[r[0]] == ACT[0])
META_OK = PCT <= META_MES
delta = PCT - PCT_ANT
if delta <= -0.5:
    ESTADO, BAND, FINAL = 'MEJORA', GREEN_F, MENSAJE_MEJORA
elif delta < 0.5:
    ESTADO, BAND = 'SE MANTUVO', ORANGE
    FINAL = ['MANTUVIMOS EL NIVEL. VAMOS POR MÁS.', 'El siguiente paso está en los detalles: revisar el papel antes de sublimar.',
             'Vamos juntos por la meta del próximo mes.']
else:
    ESTADO, BAND = 'NO FUE LO ESPERADO', '2C5F8A'
    FINAL = ['ESTE MES NOS COSTÓ, Y ESTÁ BIEN DECIRLO.', 'Cada error nos muestra dónde mejorar: miremos juntos las causas.',
             'Confiamos en este equipo.']


def num(v):
    return f'{v:,.0f}'.replace(',', '.')


def pct(v):
    return f'{v:.1f}%'.replace('.', ',')


def sem(v):
    return (GREEN_F, GREEN) if v < 7 else ((ORANGE, ORANGE) if v <= 10 else (RED_F, RED))


prs = Presentation(SRC)
LAYOUT = prs.slides[0].slide_layout
N_ORIG = len(prs.slides)
E = lambda v: Emu(int(round(v * IN)))


def rect(sl, x, y, w, h, fill, line=None, lw=1.0):
    s = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = RGBColor.from_string(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = RGBColor.from_string(line); s.line.width = Pt(lw)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def write(shape, paras, size=11, color=WHITE, bold=False, italic=False, align='l', anchor='t', space=0):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
        if space:
            p.space_after = Pt(space)
        for run in (para if isinstance(para, list) else [para]):
            text, o = (run, {}) if isinstance(run, str) else run
            r = p.add_run(); r.text = text
            f = r.font; f.name = 'Arial'
            f.size = Pt(o.get('size', size)); f.bold = o.get('bold', bold); f.italic = o.get('italic', italic)
            f.color.rgb = RGBColor.from_string(o.get('color', color))
    return shape


def tb(sl, x, y, w, h, paras, **kw):
    return write(sl.shapes.add_textbox(E(x), E(y), E(w), E(h)), paras if isinstance(paras, list) else [paras], **kw)


def base(sl, kicker, title, tag=True):
    rect(sl, 0, 0, 10, 5.625, BG)
    rect(sl, 0, 0, 0.12, 5.625, ORANGE)
    rect(sl, 0.12, 5.545, 9.88, 0.08, ORANGE)
    if kicker:
        tb(sl, 0.45, 0.30, 8.5, 0.25, kicker, size=10.5, color=ORANGE, bold=True)
    if title:
        tb(sl, 0.45, 0.55, 9.1, 0.55, title, size=24, bold=True)
    if tag:
        tb(sl, 5.6, 5.22, 4.0, 0.2, f'EQUIPO PRODUCCIÓN  ·  {MES}', size=7.5, color=GREY, align='r')


def chart_clean(ch):
    cs = ch._chartSpace
    nf = ('<c:spPr xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
          'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:noFill/><a:ln><a:noFill/></a:ln></c:spPr>')
    cs.find(f'.//{C}plotArea').append(etree.fromstring(nf))
    sp = etree.fromstring(nf); tx = cs.find(f'{C}txPr')
    (tx.addprevious(sp) if tx is not None else cs.find(f'{C}chart').addnext(sp))
    ch.has_legend = False; ch.has_title = False
    ch.font.name = 'Arial'; ch.font.size = Pt(9); ch.font.color.rgb = RGBColor.from_string(GREY)


def col_chart(sl, x, y, w, h, cats, vals, fills, lcols, labels=None, vmax=16):
    cd = CategoryChartData(); cd.categories = cats; cd.add_series('% reproceso', vals)
    ch = sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, E(x), E(y), E(w), E(h), cd).chart
    chart_clean(ch)
    plot = ch.plots[0]; plot.gap_width = 50
    ser = plot.series[0]
    dl = ser.data_labels; dl.show_value = True
    dl.number_format = '0.0"%"'; dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(10); dl.font.bold = True; dl.font.color.rgb = RGBColor.from_string(LIGHT)
    for i, (f, lc) in enumerate(zip(fills, lcols)):
        pt = ser.points[i]
        if f is None:
            pt.format.fill.background()
            pt.format.line.color.rgb = RGBColor.from_string(ORANGE); pt.format.line.width = Pt(1.5)
        else:
            pt.format.fill.solid(); pt.format.fill.fore_color.rgb = RGBColor.from_string(f)
        d = pt.data_label
        d.font.size = Pt(10); d.font.bold = True; d.font.color.rgb = RGBColor.from_string(lc)
        d.position = XL_LABEL_POSITION.OUTSIDE_END
        if labels and labels[i]:
            d.text_frame.text = labels[i]
            for r in d.text_frame.paragraphs[0].runs:
                r.font.size = Pt(10); r.font.bold = True; r.font.color.rgb = RGBColor.from_string(lc)
    va = ch.value_axis; va.visible = False; va.has_major_gridlines = False; va.maximum_scale = vmax; va.minimum_scale = 0
    ca = ch.category_axis
    ca.tick_labels.font.size = Pt(9.5); ca.tick_labels.font.bold = True; ca.tick_labels.font.color.rgb = RGBColor.from_string(GREY)
    ca.format.line.color.rgb = RGBColor.from_string(MUTED); ca.has_major_gridlines = False
    return ch


def notes(sl, text):
    sl.notes_slide.notes_text_frame.text = text


def click_fade(sl, shape):
    spid = shape.shape_id
    xml = (f'<p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst><p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="5" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="clickEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:set><p:cBhvr><p:cTn id="6" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set><p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="7" dur="800"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn></p:par></p:tnLst><p:bldLst><p:bldP spid="{spid}" grpId="0" animBg="1"/></p:bldLst></p:timing>')
    sld = sl._element; ext = sld.find(f'{P}extLst'); el = etree.fromstring(xml)
    (ext.addprevious(el) if ext is not None else sld.append(el))


def new_slide():
    sl = prs.slides.add_slide(LAYOUT)
    for sp in list(sl.shapes):
        sp._element.getparent().remove(sp._element)
    return sl


mes_t = ACT[0].capitalize()
ruta_mes = [r for r in RUTA if r[3] is None]          # metas aún por jugar (incluye el mes actual)
ruta_hecha = [r for r in RUTA if r[3] is not None]

# ================================================================== 1. PORTADA
sl = new_slide(); base(sl, None, None, tag=False)
tb(sl, 0.45, 1.05, 9, 0.3, 'EQUIPO PRODUCCIÓN  ·  PLAYMAKER', size=13, color=ORANGE, bold=True)
tb(sl, 0.45, 1.45, 9.1, 1.5, ['¿CÓMO NOS FUE', f'EN {ACT[0]}?'], size=44, bold=True)
tb(sl, 0.45, 3.15, 9, 0.3, 'Revisión mensual de calidad de producción', size=13, color=GREY, italic=True)
rect(sl, 0.45, 3.70, 5.6, 0.85, PANEL)
tb(sl, 0.65, 3.82, 5.3, 0.65, [f'Hoy:  qué medimos  →  cómo venimos  →  qué pasó en {ACT[0].lower()}',
                               [('y al final, ', {}), ('el resultado.', {'bold': True, 'color': ORANGE})]], size=11, color=LIGHT, space=4)
tb(sl, 6.6, 4.95, 3.0, 0.25, 'UN CLUB, UNA FAMILIA', size=9, color=ORANGE, bold=True, align='r')
tb(sl, 6.6, 5.20, 3.0, 0.22, 'www.playmaker.cl', size=8.5, color=GREY, italic=True, align='r')
notes(sl, f'Abrir con la pregunta. Orden: qué medimos, cómo venimos, qué pasó en {ACT[0].lower()} y, al final, el resultado.')

# ================================================================== 2. QUÉ ESTAMOS MIDIENDO
sl = new_slide(); base(sl, '1 · QUÉ ESTAMOS MIDIENDO', 'EL NÚMERO QUE SEGUIMOS CADA MES')
Y = 1.35
for x, w, col, t, d in [(0.45, 2.55, ORANGE, 'METROS REPROCESADOS', 'Lo que tuvimos que volver a imprimir en el mes.'),
                        (3.45, 2.95, MUTED, 'TOTAL IMPRESO', 'Metros de producción + metros reprocesados.'),
                        (6.85, 2.75, GREEN_F, '% DE REPROCESO', 'De cada 100 metros que imprimimos, cuántos fueron para repetir.')]:
    rect(sl, x, Y, w, 1.05, PANEL); rect(sl, x, Y, w, 0.06, col)
    tb(sl, x + 0.15, Y + 0.18, w - 0.3, 0.25, t, size=11, bold=True)
    tb(sl, x + 0.15, Y + 0.48, w - 0.3, 0.5, d, size=9.5, color=LIGHT)
tb(sl, 3.0, Y + 0.25, 0.45, 0.5, '÷', size=26, bold=True, color=ORANGE, align='c')
tb(sl, 6.40, Y + 0.25, 0.45, 0.5, '=', size=26, bold=True, color=ORANGE, align='c')
tb(sl, 0.45, 2.55, 9.15, 0.25, 'Ejemplo: si en un mes imprimimos 100 metros y 6 fueron para repetir, el reproceso es 6%.  Los datos salen del Control de Ploteo.',
   size=9.5, color=GREY, italic=True)
tb(sl, 0.45, 2.98, 6, 0.25, 'CÓMO LEER EL RESULTADO', size=10, color=ORANGE, bold=True)
for i, (f, tc, t, d) in enumerate([(GREEN_F, WHITE, 'VERDE', 'menos de 7%'), (ORANGE, BLACK, 'NARANJA', 'entre 7% y 10%'), (RED_F, WHITE, 'ROJO', 'más de 10%')]):
    x = 0.45 + i * 2.05
    rect(sl, x, 3.28, 1.95, 0.62, f)
    tb(sl, x + 0.12, 3.33, 1.71, 0.55, [t, [(d, {'bold': False, 'size': 9.5})]], size=11, bold=True, color=tc, anchor='m')
rect(sl, 6.65, 3.28, 2.95, 0.62, PANEL, line=ORANGE)
tb(sl, 6.78, 3.33, 2.7, 0.55, ['META DICIEMBRE: 5%', [('1 de cada 20 metros', {'bold': False, 'size': 9.5, 'color': LIGHT})]], size=11, bold=True, color=ORANGE, anchor='m')
rect(sl, 0.45, 4.15, 9.15, 0.85, PANEL2)
tb(sl, 0.65, 4.25, 8.8, 0.7, [[('Y ADEMÁS: ', {'bold': True, 'color': ORANGE}),
                              ('contamos cada pedido de reimpresión del chat PENDIENTES PMK, en qué etapa nació el error '
                               'y si se detectó antes o después de sublimar (línea ETAPA). Eso nos dice dónde mirar.', {})]],
   size=10.5, color=LIGHT, anchor='m')
notes(sl, 'Explicar el indicador: metros reprocesados dividido por el total impreso. Mide el proceso, no a personas. '
          'Semáforo: verde bajo 7%, naranja 7–10%, rojo sobre 10%. Meta de diciembre: 5% (1 de cada 20 metros).')

# ================================================================== 3. EL HISTORIAL
sl = new_slide(); base(sl, '2 · CÓMO VENIMOS', 'EL HISTORIAL, MES A MES')
COLS = [(0.45, 1.85, 'MES'), (2.30, 1.75, 'METROS IMPRESOS'), (4.05, 1.85, 'METROS REPROCESADOS'),
        (5.90, 1.70, '% REPROCESO'), (7.60, 2.00, 'PEDIDOS EN EL CHAT')]
HY, HH = 1.28, 0.40
n = len(HIST) + 1
RH = min(0.44, (2.70 - 0.04 * n) / n); ST = RH + 0.05
rect(sl, 0.45, HY, 9.15, HH, ORANGE)
for x, w, t in COLS:
    tb(sl, x + 0.05, HY, w - 0.1, HH, t, size=9, bold=True, color=BLACK, align='c', anchor='m')
for i, (m, prod, rep, p, ev) in enumerate(HIST):
    y = HY + HH + 0.06 + i * ST
    rect(sl, 0.45, y, 9.15, RH, PANEL if i % 2 == 0 else PANEL2)
    f, tcol = sem(p)
    for (x, w, _), (t, c, b, al) in zip(COLS, [(m, WHITE, True, 'l'), (num(prod) + ' m', LIGHT, False, 'c'),
                                               (num(rep) + ' m', LIGHT, False, 'c'), (pct(p), tcol, True, 'c'), (str(ev), LIGHT, False, 'c')]):
        tb(sl, x + (0.15 if al == 'l' else 0.05), y, w - 0.2, RH, t, size=12 if c == tcol and al == 'c' else 11, color=c, bold=b, align=al, anchor='m')
y = HY + HH + 0.06 + len(HIST) * ST
rect(sl, 0.45, y, 9.15, RH, None, line=ORANGE, lw=1.25)
tb(sl, 0.60, y, 1.7, RH, ACT[0], size=11, bold=True, color=ORANGE, anchor='m')
for x, w, _ in COLS[1:]:
    tb(sl, x + 0.05, y, w - 0.1, RH, '?', size=15, bold=True, color=ORANGE, align='c', anchor='m')
hi = max(HIST, key=lambda h: h[3])
tb(sl, 0.45, y + RH + 0.15, 9.15, 0.3, [[('Subimos hasta ', {'color': LIGHT}), (f'{pct(hi[3])} en {hi[0].lower()}', {'bold': True}),
                                         (f' y en {MES_ANT} bajamos a ', {'color': LIGHT}), (pct(PCT_ANT), {'bold': True, 'color': sem(PCT_ANT)[1]}),
                                         (f'. ¿Y {ACT[0].lower()}? Al final.', {'color': LIGHT})]], size=11.5)
tb(sl, 0.45, 4.98, 9.0, 0.2, '* Julio estimado (el registro de ploteo de ese mes quedó incompleto).  Mayo: el chat de pendientes comenzó el 19-may.',
   size=7.5, color=GREY, italic=True)
notes(sl, f'Recorrer la tabla mes a mes con el semáforo. {ACT[0].capitalize()} queda tapado: el resultado se ve al final.')

# ================================================================== 4. LA HOJA DE RUTA
sl = new_slide(); base(sl, '3 · LA META QUE NOS PUSIMOS', 'LA HOJA DE RUTA HASTA DICIEMBRE')
tb(sl, 0.45, 1.22, 5.6, 0.25, '% DE REPROCESO REAL Y METAS MENSUALES QUE VIENEN', size=9, color=GREY, bold=True)
cats = CORTOS[:len(HIST)] + [r[0] for r in ruta_mes]
vals = [h[3] for h in HIST] + [r[1] for r in ruta_mes]
fills = [sem(h[3])[0] for h in HIST] + [None] * len(ruta_mes)
lcols = [sem(h[3])[1] for h in HIST] + [ORANGE] * len(ruta_mes)
labs = [None] * len(HIST) + [f'≤{r[1]}%' for r in ruta_mes]
col_chart(sl, 0.30, 1.45, 5.9, 3.45, cats, vals, fills, lcols, labels=labs)
tb(sl, 0.45, 4.98, 5.5, 0.2, '* Julio estimado.  Barras con borde = meta del mes.', size=7.5, color=GREY, italic=True)
X = 6.45
tb(sl, X, 1.30, 3.15, 0.85, 'Bajar mes a mes hasta llegar al 5% en diciembre.', size=15, bold=True)
for i, (m, p, mts, real) in enumerate(RUTA):
    y = 2.25 + i * 0.47
    last = i == len(RUTA) - 1
    done = real is not None
    rect(sl, X, y, 3.15, 0.40, GREEN_F if done else (ORANGE if last else PANEL))
    tb(sl, X + 0.15, y, 1.5, 0.40, MESES_LARGOS[m], size=10.5, bold=True, color=BLACK if (last and not done) else WHITE, anchor='m')
    right = f'≤{p}%  ✓ {pct(real)}' if done else f'≤{p}%  ·  ≤{mts} m'
    tb(sl, X + 1.45, y, 1.55, 0.40, right, size=10.5, bold=True, color=WHITE if done else (BLACK if last else ORANGE), align='r', anchor='m')
rect(sl, X, 4.22, 3.15, 0.70, PANEL2, line=ORANGE)
tb(sl, X + 0.15, 4.22, 2.85, 0.70, [f'{ACT[0].capitalize()} era la siguiente prueba:', [('¿lo logramos?', {'color': ORANGE, 'size': 13})]],
   size=11, bold=True, anchor='m')
notes(sl, 'Metas por mes: septiembre ≤11%, octubre ≤8%, noviembre ≤6% y diciembre ≤5%. '
          + ' '.join(f'{MESES_LARGOS[r[0]].capitalize()} ya se cumplió ({pct(r[3])}).' for r in ruta_hecha)
          + f' Dejar abierta la pregunta de {ACT[0].lower()}.')

# ================================================================== 5. EL MES EN NÚMEROS
sl = new_slide(); base(sl, f'4 · QUÉ PASÓ EN {ACT[0]}', f'{ACT[0]} EN NÚMEROS')
max_prod = max(h[1] for h in HIST)
prod_txt = 'impresos: el mes de mayor producción desde mayo' if ACT[1] > max_prod else 'impresos en el mes'
for i, (big, small, col) in enumerate([(num(ACT[1]) + ' m', prod_txt, WHITE),
                                       (str(ACT[4]), f'pedidos de reimpresión en el chat ({HIST[-1][4]} en {MES_ANT})', ORANGE)]):
    x = 0.45 + i * 2.75
    rect(sl, x, 1.25, 2.6, 1.05, PANEL)
    tb(sl, x + 0.15, 1.32, 2.3, 0.5, big, size=26, bold=True, color=col)
    tb(sl, x + 0.15, 1.82, 2.3, 0.45, small, size=9, color=LIGHT)
tb(sl, 0.45, 2.45, 5.4, 0.25, [[('¿EN QUÉ ETAPA NACIÓ CADA PEDIDO?  ', {'color': GREY}), (MES_ANT, {'color': '8A8A8A'}),
                               ('  vs  ', {'color': GREY}), (ACT[0].lower(), {'color': ORANGE})]], size=9, bold=True)
cd = CategoryChartData()
cd.categories = [c[0] for c in reversed(CAUSAS)]
cd.add_series(ACT[0].capitalize(), [c[2] for c in reversed(CAUSAS)])   # en barras horizontales la 1ª serie queda abajo
cd.add_series(MES_ANT.capitalize(), [c[1] for c in reversed(CAUSAS)])
ch = sl.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, E(0.30), E(2.68), E(5.6), E(2.32), cd).chart
chart_clean(ch)
pl = ch.plots[0]; pl.gap_width = 45; pl.overlap = -5
for s_, col in zip(pl.series, (ORANGE, '5A5A5A')):
    s_.format.fill.solid(); s_.format.fill.fore_color.rgb = RGBColor.from_string(col)
    d = s_.data_labels; d.show_value = True; d.position = XL_LABEL_POSITION.OUTSIDE_END
    d.font.size = Pt(8.5); d.font.bold = True; d.font.color.rgb = RGBColor.from_string(LIGHT if col == ORANGE else GREY)
va = ch.value_axis; va.visible = False; va.has_major_gridlines = False
va.maximum_scale = max(max(c[1], c[2]) for c in CAUSAS) + 2
ca = ch.category_axis; ca.tick_labels.font.size = Pt(9); ca.tick_labels.font.color.rgb = RGBColor.from_string(LIGHT)
ca.format.line.color.rgb = RGBColor.from_string(MUTED)
X = 6.15
tb(sl, X, 1.25, 3.45, 0.25, 'LO QUE NOS DICEN LOS NÚMEROS', size=10, bold=True, color=ORANGE)
for i, (col, ico, t, d) in enumerate(LECTURAS):
    y = 1.60 + i * 1.02
    rect(sl, X, y, 3.45, 0.92, PANEL)
    tb(sl, X + 0.12, y + 0.10, 0.35, 0.35, ico, size=14, bold=True, color=col, align='c')
    tb(sl, X + 0.52, y + 0.10, 2.8, 0.25, t.upper(), size=10, bold=True, color=col)
    tb(sl, X + 0.52, y + 0.36, 2.83, 0.55, d, size=9.5, color=LIGHT)
tb(sl, X, 4.72, 3.45, 0.25, CIERRE_NUMEROS, size=10.5, bold=True)
notes(sl, f'{ACT[0].capitalize()}: {num(ACT[1])} m impresos y {ACT[4]} pedidos en el chat ({HIST[-1][4]} en {MES_ANT}). '
          'Comentar qué etapas bajaron y cuáles subieron, hablando de procesos y no de personas. Reconocer el uso de la línea ETAPA.')

# ================================================================== 6. EL RESULTADO
sl = new_slide(); base(sl, '5 · EL RESULTADO', f'¿Y CÓMO TERMINÓ {ACT[0]}?')
f_act, t_act = sem(PCT)
tb(sl, 0.45, 1.15, 3.3, 1.15, pct(PCT), size=66, bold=True, color=t_act)
tb(sl, 3.75, 1.38, 2.3, 0.3, 'DE REPROCESO', size=14, bold=True)
badge = rect(sl, 3.75, 1.78, 2.25, 0.36, GREEN_F if META_OK else ORANGE)
write(badge, [f'META ≤{META_MES}%  ✓  CUMPLIDA' if META_OK else f'META ≤{META_MES}%: NO ALCANZADA'], size=10, bold=True,
      color=WHITE if META_OK else BLACK, align='c', anchor='m')
tb(sl, 0.45, 2.38, 5.6, 0.45, FRASE_RESULTADO,
   size=11.5, color=LIGHT)
col_chart(sl, 0.30, 2.80, 5.8, 2.15, CORTOS[:len(HIST) + 1], [h[3] for h in HIST] + [PCT],
          [MUTED] * len(HIST) + [f_act], [GREY] * len(HIST) + [t_act])
tb(sl, 0.45, 4.98, 3, 0.2, '* Julio estimado', size=7.5, color=GREY, italic=True)
X = 6.40
for i, (big, col, d) in enumerate([(num(ACT[2]) + ' m', GREEN if ACT[2] < HIST[-1][2] else ORANGE, f'repetidos en el mes ({HIST[-1][2]} m en {MES_ANT})'),
                                   (num(ACT[1]) + ' m', WHITE, prod_txt),
                                   (TILE_3[0], ORANGE, TILE_3[1])]):
    y = 1.20 + i * 1.22
    rect(sl, X, y, 3.2, 1.10, PANEL)
    tb(sl, X + 0.18, y + 0.10, 2.9, 0.5, big, size=24, bold=True, color=col)
    tb(sl, X + 0.18, y + 0.60, 2.9, 0.45, d, size=9.5, color=LIGHT)
notes(sl, f'Revelar: {ACT[0].lower()} cerró en {pct(PCT)}. Meta del mes ≤{META_MES}%: ' + ('se cumplió. ' if META_OK else 'no se alcanzó. ')
          + f'Repetimos {ACT[2]} m contra {HIST[-1][2]} m en {MES_ANT}.')

# ================================================================== 7. MENSAJE FINAL
sl = new_slide(); base(sl, None, None, tag=False)
panel = rect(sl, 0.85, 0.95, 8.3, 2.95, BAND)
write(panel, [[(FINAL[0], {'size': 34, 'bold': True})], [(' ', {'size': 8})], [(FINAL[1], {'size': 16})], [(FINAL[2], {'size': 16, 'bold': True})]],
      color=WHITE, align='c', anchor='m', space=2)
panel.text_frame.margin_left = panel.text_frame.margin_right = E(0.3)
tb(sl, 0.85, 4.15, 8.3, 0.35, DESAFIO, size=15, bold=True, color=ORANGE, align='c')
tb(sl, 0.85, 4.75, 8.3, 0.25, 'UN CLUB, UNA FAMILIA', size=10, bold=True, color=GREY, align='c')
click_fade(sl, panel)
notes(sl, f'RESULTADO DEL MES: {ESTADO} ({pct(PCT_ANT)} → {pct(PCT)}). El mensaje aparece con un clic.\n\n'
          'CÓMO ELEGIR EL MENSAJE CADA MES (comparar el % de reproceso con el mes anterior):\n'
          '• MEJORÓ (bajó 0,5 puntos o más) → felicitar (panel verde).\n'
          '• SE MANTUVO (cambio menor a 0,5 puntos) → invitar a mejorar (panel naranja): "Mantuvimos el nivel. Vamos por más."\n'
          '• NO FUE LO ESPERADO (subió más de 0,5 puntos) → reflexión constructiva (panel azul): "Este mes nos costó, y está bien decirlo."\n\n'
          'NO SE MUESTRA AL EQUIPO: costos en pesos, ventas, nombres asociados a errores ni detalles de metodología.')

lst = prs.slides._sldIdLst
for sid in list(lst)[:N_ORIG]:
    rid = sid.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
    lst.remove(sid); prs.part.drop_rel(rid)
prs.core_properties.title = f'PMK Equipo Producción — {MES.title()}'
prs.save(OUT)
print('saved', OUT, ESTADO, len(prs.slides))
