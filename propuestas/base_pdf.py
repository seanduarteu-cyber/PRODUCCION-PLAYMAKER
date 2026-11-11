"""Lectura y reescritura de textos de una propuesta base en PDF, con su mismo estilo.

Lo usan armar_base.py (de cada club) y cambiar_club.py: se leen los tramos de texto de la base
(fuente, tamaño, color, espaciado y línea base), se borran con redacciones y se vuelve a escribir
encima con reportlab y las mismas fuentes.
"""

import io
from pathlib import Path

import pymupdf
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FUENTES = Path(__file__).parent / "_recursos" / "fonts"
for nombre in ("Poppins-Regular", "Poppins-SemiBold", "PlayfairDisplay-Regular",
               "PlayfairDisplay-Italic", "PlayfairDisplay-Bold"):
    pdfmetrics.registerFont(TTFont(nombre, str(FUENTES / f"{nombre}.ttf")))


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


def guardar(doc, tachar, borrar_graficos, capa, salida, metadata):
    """Borra lo reemplazado (tachar: rects por página), superpone la capa y escribe el PDF."""
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
    writer.add_metadata(metadata)
    with open(salida, "wb") as fh:
        writer.write(fh)
    return len(writer.pages)
