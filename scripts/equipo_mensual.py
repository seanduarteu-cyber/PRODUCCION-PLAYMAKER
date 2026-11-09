"""Presentación mensual para el equipo de producción: largo plazo (12 meses) y corto plazo (últimos 3 meses),
con el resultado del mes al final. Sin costos, ventas ni nombres de personas.
Datos en datos_pmk.py; textos del mes en el bloque TEXTOS. Uso: python3 equipo_mensual.py <pptx_base> <salida.pptx>"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lxml import etree
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
import datos_pmk as D

# ================================================================== DATOS (derivados de datos_pmk)
CUR, PREV, NEXT = D.MES_ACTUAL, D.shift(D.MES_ACTUAL, -1), D.shift(D.MES_ACTUAL, 1)
W3, W12 = D.ventana(3), D.ventana(12)
MES = f'{D.nombre(CUR)} {D.ym(CUR)[0]}'
MES_ANT, MES_SIG = D.nombre(PREV).lower(), D.nombre(NEXT).lower()


def _row(k):
    d = D.MESES[k]
    return (D.nombre(k) + ('*' if d.get('est') else ''), round(d['prod']), round(d['rep']), round(D.pct(k), 1), d['ev'])


HIST = [_row(k) for k in sorted(D.MESES) if k < CUR]
ACT = _row(CUR)
RUTA = [(D.corto(k), mp, mm, round(D.pct(k), 1) if (k in D.MESES and k < CUR) else None) for k, (mp, mm) in sorted(D.METAS.items())]
CORTOS = [D.corto(k) for k in sorted(D.MESES)] + [D.corto(D.shift(CUR, i)) for i in range(1, 4)]
NOMBRES_CAUSA = ['Armado de mesa / papel', 'Sublimación', 'Pendientes en taller', 'Faltó impresión', 'Corte', 'Confección', 'Diseño / ficha']

# ================================================================== TEXTOS DEL MES (revisar cada mes)
LECTURAS = [  # (color, ícono, título, texto) — lectura de los últimos 3 meses
    ('27AE60', '▼', 'Bajaron en 3 meses', 'Armado de mesa / papel (15 → 10 → 3), sublimación (12 → 12 → 7) y diseño / ficha (5 → 7 → 0).'),
    ('E74C3C', '▲', 'Ojo', 'Pendientes en taller volvió a subir (12 → 7 → 9): es el foco de noviembre.'),
    ('ED6C23', '●', 'Nuevo: la línea ETAPA', '24 de 28 pedidos la usaron, y 8 se frenaron antes de sublimar: ahí no se pierde tela.')]
CIERRE_NUMEROS = 'Más trabajo y menos pedidos. ¿Y el resultado?'
FRASE_RESULTADO = 'De cada 100 metros, cerca de 4 fueron para repetir. En septiembre eran 6 y en agosto, 14.'
META_SIG_TXT = 'PRÓXIMA META · NOVIEMBRE ≤6% (≤121 m)  ·  ya estamos bajo la meta de diciembre (5%)'
MENSAJE_MEJORA = ['¡FELICITACIONES, EQUIPO!', 'De 13,9% a 4,1% en dos meses: ya estamos bajo la meta de diciembre.', 'Este logro es de todos.']
DESAFIO = 'PRÓXIMO DESAFÍO: MANTENERNOS BAJO EL 5%   ·   NOVIEMBRE ≤6%'
PUNTOS_TRABAJO = [  # (título, párrafos, dato que lo respalda) — puntos de mejora del mes
    ('REVISAR SEGÚN LA ETAPA',
     ['Reforzamos la revisión de cada proyecto según la etapa en la que está.',
      'Si evitamos que un pendiente pase a la etapa siguiente, evitamos el reproceso.'],
     'Pendientes en taller fue la causa n.º 1 de octubre: 9 de 28 pedidos.'),
    ('DISEÑO: CRITERIOS COMUNES',
     ['Aunamos criterios: todo el equipo de diseño trabaja con los criterios de toda el área.',
      'No hay criterios que solo algunos conozcan.'],
     'Diseño / ficha bajó de 7 pedidos a 0 en octubre. Con criterios comunes, lo mantenemos.')]
# ================================================================== ACUERDOS DEL EQUIPO (cambiar solo si cambian)
HORA_LLEGADA = '9:00'
COLACION = ['13:00 a 14:00', '14:00 a 15:00']       # dos turnos
REUNION = ('Lunes a viernes', '9:15')
TRES_PREGUNTAS = ['¿Qué hice ayer?', '¿Qué haré hoy?', '¿Hay alguna condición que me impida cumplir con mi tarea de hoy?']
AGRADECIMIENTO = 'Gracias a cada uno de ustedes por la dedicación que han puesto en sus tareas.'
MEJORA_CONTINUA = ('Siempre hay algo que podemos mejorar: ', 'eso es mejora continua.')
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
                               [('→  ', {}), ('el resultado', {'bold': True, 'color': ORANGE}), ('  →  cómo seguimos mejorando.', {})]],
   size=11, color=LIGHT, space=4)
tb(sl, 6.6, 4.95, 3.0, 0.25, 'UN CLUB, UNA FAMILIA', size=9, color=ORANGE, bold=True, align='r')
tb(sl, 6.6, 5.20, 3.0, 0.22, 'www.playmaker.cl', size=8.5, color=GREY, italic=True, align='r')
notes(sl, f'Abrir con la pregunta. Orden: qué medimos, cómo venimos, qué pasó en {ACT[0].lower()}, el resultado '
          'y, para cerrar, los puntos de mejora.')

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

def cat_labels(keys):
    return [D.corto(k, con_anio=(i == 0 or D.ym(k)[1] == 1)) for i, k in enumerate(keys)]


def overlay_sin_registro(sl, cx, cw, cy, chh, n_vacios, pad=0.12):
    if not n_vacios:
        return
    pw = cw - pad - 0.12
    r = rect(sl, cx + pad + 0.02, cy + 0.20, pw * n_vacios / 12 - 0.04, chh - 0.62, None, line=MUTED, lw=0.75)
    r.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    write(r, ['Sin registro', [(f'(medimos desde {D.corto(D.INICIO_REGISTRO).lower()}-26)', {'size': 7.5})]],
          size=8.5, italic=True, color=GREY, align='c', anchor='m')


def chart12(sl, x, y, w, h, keys, ocultar_actual):
    vals, fills, lcols = [], [], []
    for k in keys:
        if k in D.MESES and not (ocultar_actual and k == CUR):
            p = round(D.pct(k), 1)
            vals.append(p)
            if ocultar_actual:
                f, t = sem(p)
            else:
                f, t = (sem(p) if k == CUR else (MUTED, GREY))
            fills.append(f); lcols.append(t)
        else:
            vals.append(None); fills.append(MUTED); lcols.append(GREY)
    ch = col_chart(sl, x, y, w, h, cat_labels(keys), vals, fills, lcols)
    for s_ in ch.plots[0].series:
        s_.data_labels.font.size = Pt(8.5)
    ch.category_axis.tick_labels.font.size = Pt(8)
    vac = sum(1 for k in keys if k not in D.MESES)
    overlay_sin_registro(sl, x, w, y, h, vac)
    if ocultar_actual:
        pw = w - 0.24
        cxm = x + 0.12 + pw * (len(keys) - 0.5) / len(keys)
        r = rect(sl, cxm - 0.17, y + h - 1.05, 0.34, 0.62, None, line=ORANGE, lw=1.25)
        write(r, ['?'], size=16, bold=True, color=ORANGE, align='c', anchor='m')
    return ch


def flechas(vals, fmt, last_color):
    runs = []
    for i, v in enumerate(vals):
        if i:
            runs.append(('  →  ', {'color': GREY, 'size': 12}))
        runs.append((fmt(v), {'color': last_color if i == len(vals) - 1 else LIGHT}))
    return runs


# ================================================================== 3. CÓMO VENIMOS: LARGO Y CORTO PLAZO
sl = new_slide(); base(sl, '2 · CÓMO VENIMOS', 'LARGO PLAZO Y CORTO PLAZO')
tb(sl, 0.45, 1.22, 5.6, 0.25, 'LARGO PLAZO — % DE REPROCESO, ÚLTIMOS 12 MESES', size=9, color=GREY, bold=True)
chart12(sl, 0.30, 1.42, 5.75, 3.45, W12, ocultar_actual=True)
tb(sl, 0.45, 4.98, 5.5, 0.2, '* Julio estimado (registro de ploteo incompleto).', size=7.5, color=GREY, italic=True)
X, WR = 6.30, 3.30
tb(sl, X, 1.22, WR, 0.25, 'CORTO PLAZO — ÚLTIMOS 3 MESES', size=10, bold=True, color=ORANGE)
cols = [('MES', 1.15, 'l'), ('%', 0.65, 'c'), ('M REPETIDOS', 0.85, 'c'), ('PEDIDOS', 0.65, 'c')]
rect(sl, X, 1.52, WR, 0.36, ORANGE)
cx = X
for t, w, _ in cols:
    tb(sl, cx + 0.03, 1.52, w - 0.06, 0.36, t, size=8, bold=True, color=BLACK, align='c', anchor='m'); cx += w
for i, k in enumerate(W3):
    y = 1.94 + i * 0.58
    hide = k == CUR
    rect(sl, X, y, WR, 0.52, None if hide else (PANEL if i % 2 == 0 else PANEL2), line=ORANGE if hide else None, lw=1.25)
    d = D.MESES[k]
    p = D.pct(k)
    cells = [(D.nombre(k), ORANGE if hide else WHITE, True, 'l')] + (
        [('?', ORANGE, True, 'c')] * 3 if hide else
        [(pct(p), sem(p)[1], True, 'c'), (num(d['rep']) + ' m', LIGHT, False, 'c'), (str(d['ev']), LIGHT, False, 'c')])
    cx = X
    for (t, w, _), (txt, col, b, al) in zip(cols, cells):
        tb(sl, cx + (0.10 if al == 'l' else 0.03), y, w - 0.13, 0.52, txt, size=14 if txt == '?' else (11 if al == 'l' else 11.5),
           bold=b, color=col, align=al, anchor='m')
        cx += w
p0, pp = D.pct(W3[0]), D.pct(PREV)
tb(sl, X, 3.80, WR, 1.05, [[('Venimos de ', {'color': LIGHT}), (pct(p0), {'bold': True, 'color': sem(p0)[1]}),
                            (f' en {D.nombre(W3[0]).lower()} a ', {'color': LIGHT}), (pct(pp), {'bold': True, 'color': sem(pp)[1]}),
                            (f' en {MES_ANT}.', {'color': LIGHT})],
                           [(f'¿Y {D.nombre(CUR).lower()}? ', {'bold': True}), ('Lo vemos al final.', {'color': ORANGE, 'bold': True})]],
   size=11.5, space=6)
notes(sl, 'Izquierda, largo plazo: cómo se movió el % de reproceso en los últimos 12 meses (medimos desde mayo). '
          f'Derecha, corto plazo: los últimos 3 meses. {D.nombre(CUR).capitalize()} queda oculto hasta el final.')

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

# ================================================================== 5. EL MES EN NÚMEROS (comparativa 3 meses)
sl = new_slide(); base(sl, f'4 · QUÉ PASÓ EN {ACT[0]}', f'{ACT[0]} EN NÚMEROS')
max_prod = max(h[1] for h in HIST)
prod_txt = 'de producción: el mes más alto desde mayo' if ACT[1] > max_prod else 'de producción en el mes'
evs = [D.MESES[k]['ev'] for k in W3]
for i, (big, small, col) in enumerate([(num(ACT[1]) + ' m', prod_txt, WHITE),
                                       (str(ACT[4]), 'pedidos de reimpresión en el chat  (' + ' → '.join(map(str, evs)) + ' en 3 meses)', ORANGE)]):
    x = 0.45 + i * 2.75
    rect(sl, x, 1.25, 2.6, 1.05, PANEL)
    tb(sl, x + 0.15, 1.32, 2.3, 0.5, big, size=26, bold=True, color=col)
    tb(sl, x + 0.15, 1.82, 2.3, 0.45, small, size=9, color=LIGHT)
SER_COL = ['4A4A4A', '8A8A8A', ORANGE]
tb(sl, 0.45, 2.42, 5.5, 0.25, [[('¿EN QUÉ ETAPA NACIÓ CADA PEDIDO?   ', {'color': GREY})] +
                               sum([[(D.nombre(k).lower(), {'color': c if c != '4A4A4A' else '6A6A6A'}), ('  ·  ', {'color': GREY})] for k, c in zip(W3, SER_COL)], [])[:-1]],
   size=9, bold=True)
cd = CategoryChartData()
cd.categories = list(reversed(NOMBRES_CAUSA))
for k in reversed(W3):                     # en barras horizontales la 1ª serie queda abajo
    cd.add_series(D.nombre(k).capitalize(), list(reversed(D.CAUSAS_MES[k])))
ch = sl.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, E(0.30), E(2.62), E(5.6), E(2.45), cd).chart
chart_clean(ch)
pl = ch.plots[0]; pl.gap_width = 35; pl.overlap = -5
for s_, col in zip(pl.series, list(reversed(SER_COL))):
    s_.format.fill.solid(); s_.format.fill.fore_color.rgb = RGBColor.from_string(col)
    d = s_.data_labels; d.show_value = True; d.position = XL_LABEL_POSITION.OUTSIDE_END
    d.font.size = Pt(7.5); d.font.bold = True; d.font.color.rgb = RGBColor.from_string(LIGHT if col == ORANGE else GREY)
va = ch.value_axis; va.visible = False; va.has_major_gridlines = False
va.maximum_scale = max(max(D.CAUSAS_MES[k]) for k in W3) + 2
ca = ch.category_axis; ca.tick_labels.font.size = Pt(8.5); ca.tick_labels.font.color.rgb = RGBColor.from_string(LIGHT)
ca.format.line.color.rgb = RGBColor.from_string(MUTED)
X = 6.15
tb(sl, X, 1.25, 3.45, 0.25, 'LO QUE NOS DICEN LOS ÚLTIMOS 3 MESES', size=10, bold=True, color=ORANGE)
for i, (col, ico, t, d) in enumerate(LECTURAS):
    y = 1.60 + i * 1.02
    rect(sl, X, y, 3.45, 0.92, PANEL)
    tb(sl, X + 0.12, y + 0.10, 0.35, 0.35, ico, size=14, bold=True, color=col, align='c')
    tb(sl, X + 0.52, y + 0.10, 2.8, 0.25, t.upper(), size=10, bold=True, color=col)
    tb(sl, X + 0.52, y + 0.36, 2.83, 0.55, d, size=9.5, color=LIGHT)
tb(sl, X, 4.72, 3.45, 0.25, CIERRE_NUMEROS, size=10.5, bold=True)
notes(sl, f'{ACT[0].capitalize()}: {num(ACT[1])} m de producción y {ACT[4]} pedidos en el chat. Comparar los últimos 3 meses por etapa '
          '(hablar de procesos, no de personas). Reconocer el uso de la línea ETAPA.')

# ================================================================== 6. EL RESULTADO (corto y largo plazo)
sl = new_slide(); base(sl, '5 · EL RESULTADO', f'¿Y CÓMO TERMINÓ {ACT[0]}?')
f_act, t_act = sem(PCT)
tb(sl, 0.45, 1.12, 3.3, 1.15, pct(PCT), size=62, bold=True, color=t_act)
tb(sl, 3.60, 1.32, 2.4, 0.3, 'DE REPROCESO', size=14, bold=True)
badge = rect(sl, 3.60, 1.70, 2.40, 0.36, GREEN_F if META_OK else ORANGE)
write(badge, [f'META ≤{META_MES}%  ✓  CUMPLIDA' if META_OK else f'META ≤{META_MES}%: NO ALCANZADA'], size=10, bold=True,
      color=WHITE if META_OK else BLACK, align='c', anchor='m')
tb(sl, 0.45, 2.22, 5.6, 0.45, FRASE_RESULTADO, size=11, color=LIGHT)
tb(sl, 0.45, 2.70, 5.6, 0.22, 'LARGO PLAZO — ÚLTIMOS 12 MESES', size=8.5, color=GREY, bold=True)
chart12(sl, 0.30, 2.86, 5.8, 2.15, W12, ocultar_actual=False)
tb(sl, 0.45, 5.02, 3, 0.2, '* Julio estimado', size=7.5, color=GREY, italic=True)
X = 6.35
tb(sl, X, 1.12, 3.25, 0.25, 'CORTO PLAZO — ÚLTIMOS 3 MESES', size=10, bold=True, color=ORANGE)
tiles = [('% DE REPROCESO', [D.pct(k) for k in W3], pct, t_act),
         ('METROS REPETIDOS', [D.MESES[k]['rep'] for k in W3], lambda v: num(v), GREEN if ACT[2] < HIST[-1][2] else ORANGE),
         ('PEDIDOS EN EL CHAT', [D.MESES[k]['ev'] for k in W3], lambda v: str(v), GREEN if ACT[4] < HIST[-1][4] else ORANGE)]
for i, (lab, vals, fmt, lc) in enumerate(tiles):
    y = 1.45 + i * 0.95
    rect(sl, X, y, 3.25, 0.85, PANEL)
    tb(sl, X + 0.15, y + 0.08, 3.0, 0.22, lab + '  (' + ' · '.join(D.corto(k).lower() for k in W3) + ')', size=8, bold=True, color=GREY)
    tb(sl, X + 0.15, y + 0.33, 3.0, 0.45, [flechas(vals, fmt, lc)], size=17, bold=True)
r = rect(sl, X, 4.35, 3.25, 0.66, PANEL2, line=ORANGE)
write(r, [META_SIG_TXT], size=9, bold=True, color=ORANGE, align='c', anchor='m')
r.text_frame.margin_left = r.text_frame.margin_right = E(0.12)
notes(sl, f'Revelar: {ACT[0].lower()} cerró en {pct(PCT)} (meta del mes ≤{META_MES}%: ' + ('cumplida' if META_OK else 'no alcanzada') + '). '
          'Corto plazo: comparar los últimos 3 meses. Largo plazo: mirar el gráfico de 12 meses completo, ahora con el mes revelado.')

# ================================================================== 7. PUNTOS DE MEJORA: EL TRABAJO
sl = new_slide(); base(sl, '6 · PUNTOS DE MEJORA', 'CÓMO EVITAMOS EL PRÓXIMO REPROCESO')
ETAPAS = ['DISEÑO / FICHA', 'IMPRESIÓN', 'ARMADO DE MESA', 'SUBLIMACIÓN', 'CORTE', 'CONFECCIÓN']
bw, gap = 1.25, 0.32
for i, et in enumerate(ETAPAS):
    x = 0.45 + i * (bw + gap)
    rect(sl, x, 1.25, bw, 0.62, PANEL)
    rect(sl, x, 1.25, bw, 0.05, GREEN)
    tb(sl, x + 0.04, 1.36, bw - 0.08, 0.25, et, size=9, bold=True, align='c')
    tb(sl, x + 0.04, 1.60, bw - 0.08, 0.22, '✓ revisado', size=8.5, bold=True, color=GREEN, align='c')
    if i:
        tb(sl, x - gap, 1.25, gap, 0.62, '→', size=14, bold=True, color=ORANGE, align='c', anchor='m')
tb(sl, 0.45, 1.98, 9.1, 0.25, 'Revisamos cada proyecto en la etapa en que está, antes de pasarlo a la siguiente.',
   size=10, color=GREY, italic=True)
for i, (tit, parrafos, dato) in enumerate(PUNTOS_TRABAJO):
    x = 0.45 + i * 4.65
    rect(sl, x, 2.40, 4.45, 2.55, PANEL)
    rect(sl, x, 2.40, 4.45, 0.06, ORANGE)
    tb(sl, x + 0.22, 2.55, 0.5, 0.55, str(i + 1), size=30, bold=True, color=ORANGE)
    tb(sl, x + 0.80, 2.64, 3.45, 0.3, tit, size=13, bold=True)
    tb(sl, x + 0.80, 3.02, 3.45, 1.15, parrafos, size=11, color=LIGHT, space=5)
    rect(sl, x + 0.22, 4.28, 4.01, 0.52, PANEL2)
    tb(sl, x + 0.35, 4.28, 3.78, 0.52, dato, size=9.5, bold=True, color=ORANGE, anchor='m')
notes(sl, 'Puntos de mejora en el trabajo. (1) Revisar cada proyecto según la etapa en que está: un pendiente que no pasa a la '
          'etapa siguiente es un reproceso que no ocurre. (2) Diseño: criterios comunes para toda el área; '
          'ningún criterio debe depender de que solo algunos lo conozcan.')

# ================================================================== 8. PUNTOS DE MEJORA: NUESTRO DÍA
sl = new_slide(); base(sl, '6 · PUNTOS DE MEJORA', 'NUESTRO DÍA: HORARIOS Y PLANIFICACIÓN')
bloques = [([HORA_LLEGADA], 'LLEGADA', 'Todo el equipo de producción'),
           ([REUNION[1]], 'REUNIÓN DE PLANIFICACIÓN', REUNION[0]),
           (COLACION, 'COLACIÓN', 'En dos turnos')]
for i, (horas, lab, sub) in enumerate(bloques):
    x = 0.45 + i * 3.1
    rect(sl, x, 1.25, 2.9, 1.30, PANEL)
    rect(sl, x, 1.25, 0.06, 1.30, ORANGE)
    tb(sl, x + 0.25, 1.32, 2.5, 0.62, horas, size=30 if len(horas) == 1 else 15, bold=True, color=ORANGE, anchor='m')
    tb(sl, x + 0.25, 1.98, 2.5, 0.25, lab, size=10.5, bold=True)
    tb(sl, x + 0.25, 2.22, 2.5, 0.25, sub, size=9.5, color=GREY)
tb(sl, 0.45, 2.80, 9.1, 0.25, f'A LA REUNIÓN DE LAS {REUNION[1]} LLEGAMOS CLAROS EN TRES PREGUNTAS', size=10.5, bold=True, color=ORANGE)
for i, q in enumerate(TRES_PREGUNTAS):
    x = 0.45 + i * 3.1
    rect(sl, x, 3.12, 2.9, 1.30, PANEL)
    tb(sl, x + 0.18, 3.12, 0.5, 1.30, str(i + 1), size=30, bold=True, color=ORANGE, anchor='m')
    tb(sl, x + 0.70, 3.12, 2.05, 1.30, q, size=13, bold=True, anchor='m')
tb(sl, 0.45, 4.62, 9.1, 0.3, 'Si algo nos impide avanzar, la reunión es el momento para decirlo y resolverlo juntos.',
   size=10.5, color=LIGHT, italic=True)
notes(sl, f'Reforzar con todo el equipo de producción: llegada a las {HORA_LLEGADA}; colación en dos turnos '
          f'({COLACION[0]} y {COLACION[1]}). Reunión de planificación {REUNION[0].lower()} a las {REUNION[1]}: '
          'cada uno llega con sus tres respuestas claras.')

# ================================================================== 9. MENSAJE FINAL
sl = new_slide(); base(sl, None, None, tag=False)
panel = rect(sl, 0.85, 0.75, 8.3, 2.95, BAND)
write(panel, [[(FINAL[0], {'size': 34, 'bold': True})], [(' ', {'size': 8})], [(FINAL[1], {'size': 16})],
              [(FINAL[2], {'size': 16, 'bold': True})], [(' ', {'size': 8})], [(AGRADECIMIENTO, {'size': 14, 'italic': True})]],
      color=WHITE, align='c', anchor='m', space=2)
panel.text_frame.margin_left = panel.text_frame.margin_right = E(0.3)
tb(sl, 0.85, 3.92, 8.3, 0.3, [[(MEJORA_CONTINUA[0], {}), (MEJORA_CONTINUA[1], {'bold': True, 'color': ORANGE})]],
   size=14, color=WHITE, align='c')
tb(sl, 0.85, 4.35, 8.3, 0.35, DESAFIO, size=15, bold=True, color=ORANGE, align='c')
tb(sl, 0.85, 4.92, 8.3, 0.25, 'UN CLUB, UNA FAMILIA', size=10, bold=True, color=GREY, align='c')
click_fade(sl, panel)
notes(sl, f'RESULTADO DEL MES: {ESTADO} ({pct(PCT_ANT)} → {pct(PCT)}). El mensaje aparece con un clic.\n\n'
          'SIEMPRE, cualquiera sea el resultado: agradecer a cada uno su dedicación e invitar a seguir mejorando '
          '(mejora continua: siempre hay algo que podemos mejorar).\n\n'
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
