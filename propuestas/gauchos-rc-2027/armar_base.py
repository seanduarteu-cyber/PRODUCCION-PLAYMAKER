"""Arma la base de la propuesta a partir del PDF original: agrega la Parka larga y quita las
fichas que no tienen render (Bermuda sastre y Accesorios del club).

Uso:
    python3 propuestas/gauchos-rc-2027/armar_base.py

Lee  base/Propuesta_Gauchos_Rugby_Club_2027_base.pdf    (original, no se modifica)
Crea base/Propuesta_Gauchos_Rugby_Club_2027_base_v2.pdf  (la que usa propuesta.json)

Resultado (22 productos en tres categorías):
  - Presentación y abrigo queda: ... 19 Polera de algodón, 20 Bermuda deportiva, 21 Pantalón pitillo,
    22 Parka larga (ficha nueva con el mismo diseño de las demás).
  - Sin Bermuda sastre ni la categoría Accesorios.
  - Portada, "Sobre esta propuesta", catálogo y cuadro de valores actualizados; páginas renumeradas.
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
PARKA_PAG = "parka"
# orden de las páginas del documento final (índices de la base; la parka es una copia de la ficha modelo)
ORDEN = [i for i in range(P_BERMUDA_SASTRE)] + [P_BERMUDA_DEP, P_PITILLO, PARKA_PAG, P_CUADRO, 27, 28]

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


# ---------------------------------------------------------------- principal

def main():
    with pdfplumber.open(BASE) as pdf:
        R = {i: runs_de(pdf.pages[i]) for i in range(len(pdf.pages))}
        lineas = {i: pdf.pages[i].lines for i in (P_CATALOGO, P_CUADRO)}
        rects_cuadro = pdf.pages[P_CUADRO].rects
        w, h = pdf.pages[0].width, pdf.pages[0].height

    # documento con las páginas en el orden final
    doc = pymupdf.open(BASE)
    doc.insert_pdf(pymupdf.open(BASE), from_page=P_MODELO_FICHA, to_page=P_MODELO_FICHA, start_at=doc.page_count)
    copia = doc.page_count - 1
    doc.select([copia if i == PARKA_PAG else i for i in ORDEN])
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
        origen = P_MODELO_FICHA if pag == PARKA_PAG else pag
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

    # 7. Borrar lo reemplazado y superponer lo nuevo
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
