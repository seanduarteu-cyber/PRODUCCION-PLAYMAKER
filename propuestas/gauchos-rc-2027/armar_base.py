"""Arma la base de la propuesta a partir del PDF original: agrega la Parka larga y quita las
fichas que no tienen render (Bermuda sastre y Accesorios del club).

Uso:
    python3 propuestas/gauchos-rc-2027/armar_base.py

Lee  base/Propuesta_Gauchos_Rugby_Club_2027_base.pdf    (original, no se modifica)
Crea base/Propuesta_Gauchos_Rugby_Club_2027_base_v2.pdf  (la que usa propuesta.json)

Resultado (22 productos en tres categorías, 30 páginas):
  - Presentación y abrigo queda: ... 19 Polera de algodón, 20 Bermuda deportiva, 21 Pantalón pitillo,
    22 Parka larga (ficha nueva con el mismo diseño de las demás).
  - Sin Bermuda sastre ni la categoría Accesorios.
  - Portada, "Sobre esta propuesta", catálogo y cuadro de valores actualizados; páginas renumeradas.
  - Dos páginas nuevas después de "Cómo trabajamos": "Preventa Oficial Gauchos" (programa para socios con
    royalty por tramos) y "Transparencia y pagos" (cómo se liquida y qué aporta cada parte).
    Sus textos y porcentajes están en PROGRAMA, más abajo.
Los textos se dibujan con las mismas fuentes, tamaños, colores y espaciado que la base.
"""

import io
from pathlib import Path

import pdfplumber
import pymupdf
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

DIR = Path(__file__).parent
BASE = DIR / "base" / "Propuesta_Gauchos_Rugby_Club_2027_base.pdf"
SALIDA = DIR / "base" / "Propuesta_Gauchos_Rugby_Club_2027_base_v2.pdf"
FUENTES = DIR.parent / "_recursos" / "fonts"
for nombre in ("Poppins-Regular", "Poppins-SemiBold", "PlayfairDisplay-Regular",
               "PlayfairDisplay-Italic", "PlayfairDisplay-Bold"):
    pdfmetrics.registerFont(TTFont(nombre, str(FUENTES / f"{nombre}.ttf")))

# páginas de la base (índice 0)
P_PORTADA, P_SOBRE, P_CATALOGO, P_MODELO_FICHA = 0, 1, 2, 3
P_BERMUDA_SASTRE, P_BERMUDA_DEP, P_PITILLO, P_ACCESORIOS, P_CUADRO = 22, 23, 24, 25, 26
P_COMO, P_PASOS = 27, 28
PARKA_PAG, PREVENTA_PAG, TRANSPARENCIA_PAG = "parka", "preventa", "transparencia"
# páginas nuevas: copias de una página de la base que se vacían y se vuelven a llenar
COPIAS = {PARKA_PAG: P_MODELO_FICHA, PREVENTA_PAG: P_COMO, TRANSPARENCIA_PAG: P_COMO}
# orden de las páginas del documento final (índices de la base o páginas nuevas)
ORDEN = ([i for i in range(P_BERMUDA_SASTRE)] +
         [P_BERMUDA_DEP, P_PITILLO, PARKA_PAG, P_CUADRO, P_COMO, PREVENTA_PAG, TRANSPARENCIA_PAG, P_PASOS])

PARKA = {
    "ficha": "FICHA 22 · PRESENTACIÓN Y ABRIGO",
    "codigo": "GAU-22",
    "titulo": "Parka larga",
    "bajada": "Negra, con paneles rojos y vivos blancos, capucha con visera y largo a medio muslo",
    "tallas": "5XS a 5XL",
    "bloques": [
        ("CAPUCHA", "Capucha con visera y ajuste con tanca."),
        ("CIERRE", "Cierre completo central y bolsillos laterales con cremallera invertida."),
        ("CUERPO", "Negro con paneles rojos y vivos blancos en hombros y mangas; largo a la altura "
                   "de los muslos."),
        ("PUÑOS", "Puños ajustables con velcro y puño interior."),
        ("APLICACIONES", "Escudo Gauchos al pecho izquierdo e isotipo Playmaker al pecho derecho y "
                         "en la capucha."),
        ("TELA", "100% poliéster."),
    ],
}
# fichas que suben un número al salir la Bermuda sastre
RENUMERAR = {P_BERMUDA_DEP: ("FICHA 20 · PRESENTACIÓN Y ABRIGO", "GAU-20"),
             P_PITILLO: ("FICHA 21 · PRESENTACIÓN Y ABRIGO", "GAU-21")}
# filas del catálogo y del cuadro: el código queda, cambia el producto
FILAS = {"Bermuda sastre": "Bermuda deportiva", "Bermuda deportiva": "Pantalón pitillo",
         "Pantalón pitillo": "Parka larga"}
TEXTOS = [  # (página, línea donde está, texto viejo, texto nuevo); el párrafo completo se vuelve a armar
    (P_PORTADA, "Línea completa", "presentación y accesorios", "presentación y abrigo"),
    (P_SOBRE, "documento cubre", "presentación, abrigo y accesorios—", "presentación y abrigo—"),
    (P_CATALOGO, "Veintitrés", "Veintitrés líneas de producto agrupadas en cuatro categorías",
     "Veintidós líneas de producto agrupadas en tres categorías"),
]

PROGRAMA = {
    "preventa": {
        "seccion": "SECCIÓN 05",
        "tema": "PROGRAMA PARA SOCIOS",
        "titulo": "Preventa Oficial Gauchos",
        "intro": ("Una vitrina propia del club en playmaker.cl, dentro de la sección de clubes e instituciones, "
                  "donde socios, jugadores y familias compran la colección Gauchos en fechas de preventa. "
                  "Playmaker se encarga del cobro, la producción y la entrega; el club recibe un royalty por "
                  "cada venta, sin invertir en stock."),
        "banda_etiqueta": "PARA LOS SOCIOS",
        "banda": "El {base}% de cada compra va directo a Gauchos",
        "pasos": [
            ("Difusión del club", "El club comparte el link y el código QR de la página Gauchos en sus canales."),
            ("Compra en línea", "Socios y familias eligen producto, talla y personalización, y pagan en "
                                "playmaker.cl con boleta electrónica."),
            ("Producción por lote", "Al cierre de la preventa, Playmaker fabrica todo lo vendido en su "
                                    "planta en Santiago."),
            ("Entrega en el club", "Los pedidos llegan consolidados al club, listos para entregar a cada socio."),
        ],
        "preventas": [("PREVENTA 1", "Inicio de temporada"), ("PREVENTA 2", "Mitad de temporada"),
                      ("PREVENTA 3", "Fin de año")],
        "preventas_nota": "Fechas a definir con el club",
        # (unidades vendidas a socios en la temporada, royalty sobre la venta neta)
        "tramos": [("Hasta 150 unidades", 10), ("De 151 a 400 unidades", 11), ("Más de 400 unidades", 12)],
        "bono_credito": 30,
    },
    "transparencia": {
        "seccion": "SECCIÓN 06",
        "tema": "PREVENTA OFICIAL GAUCHOS",
        "titulo": "Transparencia y pagos",
        "intro": ("Playmaker administra el cobro de la preventa y el club puede comprobar cada venta. Estas "
                  "reglas son parte del convenio y se aplican desde la primera preventa."),
        "recuadro": "CÓMO SE LIQUIDA EL ROYALTY",
        "reglas": [
            ("LIQUIDACIÓN", "Al cierre de cada preventa, el club recibe el detalle de cada venta: producto, "
                            "talla, comprador, monto neto, número de boleta y royalty."),
            ("RESPALDO", "Se adjunta la exportación directa de la plataforma de pago con la que se cobró."),
            ("CONTROL EN LA ENTREGA", "El club recibe y cuenta los pedidos consolidados y firma la guía de "
                                      "entrega; el royalty se calcula sobre esas mismas unidades."),
            ("PLAZO DE PAGO", "15 días desde el cierre de cada preventa, por transferencia o como crédito en "
                              "productos con un {bono}% adicional."),
            ("BASE DEL ROYALTY", "Venta neta: sin IVA y descontadas las devoluciones."),
            ("REVISIÓN", "El club puede pedir el respaldo de cualquier venta en cualquier momento."),
            ("PREVENTA PILOTO", "La primera preventa funciona como piloto para validar el proceso con la "
                                "directiva del club."),
        ],
        "aportes": [
            ("PLAYMAKER APORTA", [
                "Página Gauchos en playmaker.cl con todos los productos en preventa.",
                "Cobro, producción, atención a socios y entrega consolidada en el club.",
                "Contenido para redes con los montajes de la colección.",
                "Kit de tallas para que los socios se prueben antes de comprar.",
                "Liquidación y reporte al cierre de cada preventa.",
            ]),
            ("EL CLUB APORTA", [
                "Difusión de cada preventa en sus redes, web y grupos de socios.",
                "Espacio en partidos y entrenamientos para el kit de tallas.",
                "Aprobación de cada diseño antes de publicarlo.",
                "Recepción y control de los pedidos en el club.",
            ]),
        ],
    },
}


# ---------------------------------------------------------------- lectura de estilos

class Run:
    """Tramo de texto de la base con su estilo (fuente, tamaño, color, espaciado, línea base)."""

    def __init__(self, chars):
        self.chars = chars
        self.texto = "".join(c["text"] for c in chars)
        c0 = chars[0]
        self.fuente = c0["fontname"].split("+")[-1]
        self.size = c0["size"]
        self.color = tuple(c0["non_stroking_color"])
        self.base = c0["matrix"][5]  # línea base, coordenadas PDF
        self.top = c0["top"]
        self.x0, self.x1 = c0["x0"], chars[-1]["x1"]
        if self.fuente not in pdfmetrics.getRegisteredFontNames():
            self.espaciado = None  # fuente que no se reescribe (p. ej. Anton del pie de página)
            return
        anchos = [b["x0"] - a["x0"] - pdfmetrics.stringWidth(a["text"], self.fuente, self.size)
                  for a, b in zip(chars, chars[1:])]
        self.espaciado = sum(anchos) / len(anchos) if anchos else 0.0


def runs_de(page):
    """Tramos de texto por línea base, cortados donde hay un hueco grande."""
    lineas = {}
    for ch in page.chars:
        lineas.setdefault(round(ch["matrix"][5], 1), []).append(ch)
    runs = []
    for base in sorted(lineas, reverse=True):
        cs = sorted(lineas[base], key=lambda c: c["x0"])
        actual = [cs[0]]
        for a, b in zip(cs, cs[1:]):
            if b["x0"] - a["x1"] > 15:
                runs.append(Run(actual))
                actual = [b]
            else:
                actual.append(b)
        runs.append(Run(actual))
    return runs


def buscar(runs, inicio, cerca_de=None):
    candidatos = [r for r in runs if r.texto.startswith(inicio)]
    if cerca_de is not None:
        candidatos.sort(key=lambda r: abs(r.top - cerca_de))
    if not candidatos:
        raise LookupError(f"No se encontró «{inicio}» en la base")
    return candidatos[0]


def parrafo(runs, contiene):
    """Líneas del párrafo (mismo estilo, interlineado parejo) que contiene un texto."""
    ancla = next(r for r in runs if contiene in r.texto)
    lineas = sorted([r for r in runs if r.fuente == ancla.fuente and abs(r.size - ancla.size) < 0.1
                     and abs(r.x0 - ancla.x0) < 1], key=lambda r: -r.base)
    i = lineas.index(ancla)
    paso = 1.3 * ancla.size * 1.4
    ini = i
    while ini > 0 and lineas[ini - 1].base - lineas[ini].base < paso:
        ini -= 1
    fin = i
    while fin + 1 < len(lineas) and lineas[fin].base - lineas[fin + 1].base < paso:
        fin += 1
    return lineas[ini:fin + 1]


# ---------------------------------------------------------------- escritura

class Estilo:
    """Estilo de texto para contenido nuevo (mismos atributos que Run)."""

    def __init__(self, fuente, size, color, espaciado=0.0):
        self.fuente, self.size, self.color, self.espaciado = fuente, size, tuple(color), espaciado


class Capa:
    """Superposición reportlab: una página por página del documento final."""

    def __init__(self, n, w, h):
        self.buf = io.BytesIO()
        self.c = canvas.Canvas(self.buf, pagesize=(w, h))
        self.h = h
        self.paginas = {i: [] for i in range(n)}

    def texto(self, pagina, estilo, texto, x, base, alinear="izq"):
        self.paginas[pagina].append(("t", estilo, texto, x, base, alinear))

    def rect(self, pagina, color, x0, top, x1, bottom):
        self.paginas[pagina].append(("r", color, x0, top, x1, bottom))

    def linea(self, pagina, color, ancho, x0, x1, top):
        self.paginas[pagina].append(("l", color, ancho, x0, x1, top))

    def marco(self, pagina, color, ancho, x0, top, x1, bottom):
        self.paginas[pagina].append(("m", color, ancho, x0, top, x1, bottom))

    def ancho(self, estilo, texto):
        return pdfmetrics.stringWidth(texto, estilo.fuente, estilo.size) + estilo.espaciado * (len(texto) - 1)

    def lector(self):
        c = self.c
        for i in sorted(self.paginas):
            for op in self.paginas[i]:
                if op[0] == "r":
                    _, color, x0, top, x1, bottom = op
                    c.setFillColorRGB(*color)
                    c.rect(x0, self.h - bottom, x1 - x0, bottom - top, stroke=0, fill=1)
                elif op[0] == "l":
                    _, color, ancho, x0, x1, top = op
                    c.setStrokeColorRGB(*color)
                    c.setLineWidth(ancho)
                    c.line(x0, self.h - top, x1, self.h - top)
                elif op[0] == "m":
                    _, color, ancho, x0, top, x1, bottom = op
                    c.setStrokeColorRGB(*color)
                    c.setLineWidth(ancho)
                    c.rect(x0, self.h - bottom, x1 - x0, bottom - top, stroke=1, fill=0)
            for op in self.paginas[i]:
                if op[0] == "t":
                    _, e, texto, x, base, alinear = op
                    if alinear == "der":
                        x -= self.ancho(e, texto)
                    elif alinear == "centro":
                        x -= self.ancho(e, texto) / 2
                    t = c.beginText(x, base)
                    t.setFont(e.fuente, e.size)
                    t.setCharSpace(e.espaciado)
                    t.setFillColorRGB(*e.color)
                    t.textOut(texto)
                    c.drawText(t)
            c.showPage()
        c.save()
        self.buf.seek(0)
        return PdfReader(self.buf)


def partir(capa, estilo, texto, ancho_max):
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = f"{actual} {palabra}".strip()
        if actual and capa.ancho(estilo, prueba) > ancho_max:
            lineas.append(actual)
            actual = palabra
        else:
            actual = prueba
    return lineas + [actual]


# ---------------------------------------------------------------- páginas del programa

def paginas_programa(capa, tachar, borrar_graficos, plantilla, pag_preventa, pag_transparencia, w, h):
    """Dibuja "Preventa Oficial Gauchos" y "Transparencia y pagos" con el estilo de "Cómo trabajamos"."""
    seccion, tema = buscar(plantilla, "SECCIÓN"), buscar(plantilla, "CONDICIONES COMERCIALES")
    titulo, intro = buscar(plantilla, "Cómo trabajamos"), buscar(plantilla, "Playmaker fabrica")
    cab_rec, etq_rec = buscar(plantilla, "CONDICIONES DE"), buscar(plantilla, "ABONO")
    val_rec = buscar(plantilla, "Abono del")
    paso_intro = intro.base - buscar(plantilla, "club sin depender").base
    NAVY, ORO, MARFIL = titulo.color, seccion.color, etq_rec.color
    TEXTO, REGLA, BLANCO = (0.227, 0.247, 0.322), (0.863, 0.847, 0.796), (1, 1, 1)
    X0, X1 = 58.0, 537.3
    ANCHO = X1 - X0

    def asc(r):  # distancia de la parte superior del texto a su línea base
        return (h - r.base) - r.top

    etiqueta = Estilo("Poppins-SemiBold", 7.4, ORO, 2.2)
    cuerpo = Estilo("Poppins-Regular", 8.1, TEXTO)
    sub = Estilo("Poppins-SemiBold", 9.5, NAVY)
    numero = Estilo("PlayfairDisplay-Bold", 20, ORO)
    nota = Estilo("Poppins-Regular", 7.6, (0.431, 0.447, 0.502))

    def escribir(pag, e, texto, x, yb, alinear="izq"):  # yb: línea base medida desde arriba
        capa.texto(pag, e, texto, x, h - yb, alinear)

    def parrafo_en(pag, e, texto, x, yb, ancho, paso):
        lineas = partir(capa, e, texto, ancho)
        for k, linea in enumerate(lineas):
            escribir(pag, e, linea, x, yb + k * paso)
        return yb + (len(lineas) - 1) * paso

    def encabezado(pag, cfg):
        tachar[pag].append((30, 60, w - 30, 785))  # vacía la copia: textos, recuadro y regla del encabezado
        borrar_graficos.add(pag)
        escribir(pag, seccion, cfg["seccion"], seccion.x0, h - seccion.base)
        escribir(pag, tema, cfg["tema"], tema.x1, h - tema.base, "der")
        capa.linea(pag, REGLA, 0.6, X0, X1, 87.0)
        escribir(pag, titulo, cfg["titulo"], titulo.x0, h - titulo.base)
        return parrafo_en(pag, intro, cfg["intro"], X0, h - intro.base, ANCHO, paso_intro)

    def rotulo(pag, texto, top):
        escribir(pag, etiqueta, texto, X0, top + 6)
        capa.linea(pag, REGLA, 0.6, X0, X1, top + 13)
        return top + 13

    def recuadro_navy(pag, top, bottom):
        capa.rect(pag, NAVY, 40, top, w - 40, bottom)
        capa.marco(pag, ORO, 0.7, 48, top + 8, w - 48, bottom - 8)

    def vineta(pag, x, yb):
        capa.rect(pag, ORO, x, yb - 5, x + 3, yb - 2)

    # ---- Preventa Oficial Gauchos
    cfg = PROGRAMA["preventa"]
    pag = pag_preventa
    y = encabezado(pag, cfg)
    top = y + 22
    recuadro_navy(pag, top, top + 72)
    escribir(pag, cab_rec, cfg["banda_etiqueta"], w / 2, top + 30, "centro")
    escribir(pag, Estilo("PlayfairDisplay-Bold", 19, MARFIL), cfg["banda"].format(base=cfg["tramos"][0][1]),
             w / 2, top + 54, "centro")

    y = rotulo(pag, "CÓMO FUNCIONA", top + 72 + 24)
    sep = 16
    col = (ANCHO - sep * 3) / 4
    fondo_pasos = y
    for i, (tit, txt) in enumerate(cfg["pasos"]):
        x = X0 + i * (col + sep)
        escribir(pag, numero, f"{i + 1:02d}", x, y + 30)
        escribir(pag, sub, tit, x, y + 47)
        fondo_pasos = max(fondo_pasos, parrafo_en(pag, cuerpo, txt, x, y + 61, col, 10.6))

    y = rotulo(pag, "CALENDARIO DE PREVENTAS", fondo_pasos + 24)
    col3 = (ANCHO - sep * 2) / 3
    for i, (etq, tit) in enumerate(cfg["preventas"]):
        x = X0 + i * (col3 + sep)
        capa.rect(pag, BLANCO, x, y + 12, x + col3, y + 62)
        capa.marco(pag, REGLA, 0.6, x, y + 12, x + col3, y + 62)
        escribir(pag, Estilo("Poppins-SemiBold", 6.6, ORO, 1.4), etq, x + 12, y + 27)
        escribir(pag, sub, tit, x + 12, y + 41)
        escribir(pag, cuerpo, cfg["preventas_nota"], x + 12, y + 54)

    y = rotulo(pag, "ROYALTY PARA EL CLUB", y + 62 + 24)
    top = y + 12
    capa.rect(pag, NAVY, 46, top, w - 46, top + 20)
    cab = Estilo("Poppins-SemiBold", 6.6, MARFIL, 1.4)
    escribir(pag, cab, "UNIDADES VENDIDAS A SOCIOS EN LA TEMPORADA", X0, top + 13)
    escribir(pag, cab, "ROYALTY SOBRE VENTA NETA", X1, top + 13, "der")
    fila = Estilo("Poppins-Regular", 9.0, (0.043, 0.071, 0.149))
    pct = Estilo("Poppins-SemiBold", 11, NAVY)
    for i, (txt, valor) in enumerate(cfg["tramos"]):
        ft = top + 20 + i * 22
        capa.rect(pag, BLANCO if i % 2 == 0 else (0.965, 0.961, 0.949), 46, ft, w - 46, ft + 22)
        escribir(pag, fila, txt, X0, ft + 14.5)
        escribir(pag, pct, f"{valor}%", X1, ft + 15, "der")
    fin_tabla = top + 20 + len(cfg["tramos"]) * 22
    capa.linea(pag, REGLA, 0.6, 46, w - 46, fin_tabla)
    notas = [
        "El porcentaje del tramo alcanzado se aplica a todas las unidades vendidas en la temporada.",
        "Venta neta: sin IVA y descontadas las devoluciones.",
        f"Si el club elige recibir el royalty en productos, se abona un {cfg['bono_credito']}% adicional "
        "en crédito para indumentaria.",
    ]
    y = fin_tabla + 18
    for n in notas:
        vineta(pag, X0, y)
        y = parrafo_en(pag, nota, n, X0 + 9, y, ANCHO - 9, 10) + 13

    # ---- Transparencia y pagos
    cfg = PROGRAMA["transparencia"]
    pag = pag_transparencia
    y = encabezado(pag, cfg)
    top = y + 24
    filas, yy = [], top + 55  # mismas medidas que el recuadro de "Cómo trabajamos"
    for etq, txt in cfg["reglas"]:
        lineas = partir(capa, val_rec, txt.format(bono=PROGRAMA["preventa"]["bono_credito"]), 335)
        filas.append((etq, lineas, yy))
        yy += 20 + 11 * (len(lineas) - 1)
    bottom = yy - 20 + 55
    recuadro_navy(pag, top, bottom)
    escribir(pag, cab_rec, cfg["recuadro"], 70, top + 29 + asc(cab_rec))
    for etq, lineas, ft in filas:
        escribir(pag, etq_rec, etq, 70, ft + 1 + asc(etq_rec))
        for k, linea in enumerate(lineas):
            escribir(pag, val_rec, linea, 196, ft + asc(val_rec) + k * 11)

    y = bottom + 30
    col2 = (ANCHO - 30) / 2
    for i, (tit, items) in enumerate(cfg["aportes"]):
        x = X0 + i * (col2 + 30)
        escribir(pag, etiqueta, tit, x, y + 6)
        capa.linea(pag, REGLA, 0.6, x, x + col2, y + 13)
        yy = y + 30
        for item in items:
            vineta(pag, x, yy)
            yy = parrafo_en(pag, cuerpo, item, x + 10, yy, col2 - 10, 10.6) + 17


# ---------------------------------------------------------------- principal

def main():
    with pdfplumber.open(BASE) as pdf:
        R = {i: runs_de(pdf.pages[i]) for i in range(len(pdf.pages))}
        lineas = {i: pdf.pages[i].lines for i in (P_CATALOGO, P_CUADRO)}
        rects_cuadro = pdf.pages[P_CUADRO].rects
        w, h = pdf.pages[0].width, pdf.pages[0].height

    # documento con las páginas en el orden final
    doc = pymupdf.open(BASE)
    pos_copia = {}
    for clave, origen in COPIAS.items():
        doc.insert_pdf(pymupdf.open(BASE), from_page=origen, to_page=origen, start_at=doc.page_count)
        pos_copia[clave] = doc.page_count - 1
    doc.select([pos_copia.get(i, i) for i in ORDEN])
    final = ORDEN.index
    capa = Capa(len(doc), w, h)
    tachar = {i: [] for i in range(len(doc))}  # rects (top-based) a borrar por página final
    borrar_graficos = set()

    def borrar(pag_final, run, alto=1.25):
        tachar[pag_final].append((run.x0 - 1, run.top - 1.5, run.x1 + 1, run.top + run.size * alto))

    def reemplazar(pag_base, run, texto, alinear="izq", pag_final=None):
        """Borra un tramo de la base y escribe otro texto con el mismo estilo y posición."""
        p = final(pag_base) if pag_final is None else pag_final
        borrar(p, run)
        x = {"der": run.x1, "centro": (run.x0 + run.x1) / 2}.get(alinear, run.x0)
        capa.texto(p, run, texto, x, run.base, alinear)

    # 1. Ficha nueva: Parka larga (copia de la ficha modelo con sus textos cambiados)
    m, NUEVA = R[P_MODELO_FICHA], final(PARKA_PAG)
    reemplazar(None, buscar(m, "FICHA"), PARKA["ficha"], pag_final=NUEVA)
    reemplazar(None, buscar(m, "GAU-"), PARKA["codigo"], "der", pag_final=NUEVA)
    reemplazar(None, buscar(m, "Camiseta"), PARKA["titulo"], pag_final=NUEVA)
    reemplazar(None, buscar(m, "Negra con"), PARKA["bajada"], pag_final=NUEVA)
    reemplazar(None, buscar(m, "XS a 5XL"), PARKA["tallas"], pag_final=NUEVA)
    etiquetas = [r for r in m if r.fuente == "Poppins-SemiBold" and 480 < r.top < 700 and r.size < 7]
    cuerpos = [r for r in m if r.fuente == "Poppins-Regular" and 480 < r.top < 700]
    for r in etiquetas + cuerpos:
        borrar(NUEVA, r)
    etiquetas.sort(key=lambda r: (round(r.top), r.x0))
    estilo_cuerpo = cuerpos[0]
    bases = sorted({round(r.base, 1) for r in cuerpos}, reverse=True)
    interlinea = min(a - b for a, b in zip(bases, bases[1:]) if a - b > 1)
    primera = min(r.base for r in cuerpos if abs(r.top - etiquetas[0].top) < 20)
    salto_etiqueta = etiquetas[0].base - primera
    ancho_col = etiquetas[1].x0 - etiquetas[0].x0 - 18
    for etq, (titulo, cuerpo) in zip(etiquetas, PARKA["bloques"]):
        capa.texto(NUEVA, etq, titulo, etq.x0, etq.base)
        for k, linea in enumerate(partir(capa, estilo_cuerpo, cuerpo, ancho_col)):
            capa.texto(NUEVA, estilo_cuerpo, linea, etq.x0, etq.base - salto_etiqueta - k * interlinea)

    # 2. Fichas que suben un número
    for pag, (ficha, codigo) in RENUMERAR.items():
        reemplazar(pag, buscar(R[pag], "FICHA"), ficha)
        reemplazar(pag, buscar(R[pag], "GAU-"), codigo, "der")

    # 3. Numeración de páginas (pie de página)
    for k, pag in enumerate(ORDEN):
        origen = COPIAS.get(pag, pag)
        num = [r for r in R[origen] if r.top > 790 and r.texto.isdigit()]
        if num and int(num[0].texto) != k + 1:
            reemplazar(None, num[0], f"{k + 1:02d}", "der", pag_final=k)

    # 4. Textos que nombran los accesorios o el total de productos
    ancho_texto = 537 - 58  # ancho de la caja de texto de la base
    for pag, ancla, viejo, nuevo in TEXTOS:
        lineas_p = parrafo(R[pag], ancla)
        texto = " ".join(r.texto for r in lineas_p)
        assert viejo in texto, f"«{viejo}» no está en la página {pag + 1}"
        texto = texto.replace(viejo, nuevo)
        e = lineas_p[0]
        centrado = abs((e.x0 + e.x1) / 2 - w / 2) < 2 and len(lineas_p) == 1
        for r in lineas_p:
            borrar(final(pag), r, alto=1.35)
        if centrado:
            capa.texto(final(pag), e, texto, w / 2, e.base, "centro")
            continue
        paso = (lineas_p[0].base - lineas_p[1].base) if len(lineas_p) > 1 else e.size * 1.6
        for k, linea in enumerate(partir(capa, e, texto, ancho_texto)):
            capa.texto(final(pag), e, linea, e.x0, e.base - k * paso)

    # 5. Catálogo: filas renombradas y sin la categoría Accesorios
    c, PC = R[P_CATALOGO], final(P_CATALOGO)
    for viejo, nuevo in FILAS.items():
        reemplazar(P_CATALOGO, buscar(c, viejo), nuevo)
    cab, fila_acc = buscar(c, "ACCESORIOS"), buscar(c, "GAU-23")
    tachar[PC].append((40, cab.top - 6, w - 40, fila_acc.top + 16))
    borrar_graficos.add(PC)

    # 6. Cuadro de valores: filas renombradas, sin Accesorios y totales más arriba
    q, PQ = R[P_CUADRO], final(P_CUADRO)
    for viejo, nuevo in FILAS.items():
        reemplazar(P_CUADRO, buscar(q, viejo), nuevo)
    cab, fila_acc = buscar(q, "ACCESORIOS"), buscar(q, "GAU-23")
    ultima = buscar(q, "GAU-22")
    sube = ultima.base - fila_acc.base  # alto del bloque que sale (cabecera + fila); base PDF crece hacia arriba
    regla = next(l for l in lineas[P_CUADRO] if fila_acc.top < l["top"] < 760)
    caja = next(r for r in rects_cuadro if r["fill"] and r["top"] > 700 and r["width"] > 200)
    tachar[PQ].append((40, cab.top - 6, w - 40, caja["bottom"] + 4))
    borrar_graficos.add(PQ)
    capa.linea(PQ, regla["stroking_color"], regla["linewidth"], regla["x0"], regla["x1"], regla["top"] - sube)
    capa.rect(PQ, caja["non_stroking_color"], caja["x0"], caja["top"] - sube, caja["x1"], caja["bottom"] - sube)
    for r in q:
        if regla["top"] < r.top < caja["bottom"]:
            capa.texto(PQ, r, r.texto, r.x0, r.base + sube)

    # 7. Páginas nuevas del programa (sobre copias vaciadas de "Cómo trabajamos")
    paginas_programa(capa, tachar, borrar_graficos, R[P_COMO], final(PREVENTA_PAG), final(TRANSPARENCIA_PAG), w, h)

    # 8. Borrar lo reemplazado y superponer lo nuevo
    for i, rects in tachar.items():
        if not rects:
            continue
        page = doc[i]
        for x0, top, x1, bottom in rects:
            page.add_redact_annot(pymupdf.Rect(x0, top, x1, bottom), fill=False, cross_out=False)
        page.apply_redactions(
            images=pymupdf.PDF_REDACT_IMAGE_NONE,
            graphics=(pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED if i in borrar_graficos
                      else pymupdf.PDF_REDACT_LINE_ART_NONE),
            text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    limpio = io.BytesIO(doc.tobytes(garbage=3, deflate=True))
    writer = PdfWriter(clone_from=PdfReader(limpio))
    for page, over in zip(writer.pages, capa.lector().pages):
        page.merge_page(over)
    writer.add_metadata(PdfReader(BASE).metadata)
    with open(SALIDA, "wb") as fh:
        writer.write(fh)
    print(f"OK  {SALIDA.relative_to(DIR)}  ({len(writer.pages)} páginas)")


if __name__ == "__main__":
    main()
