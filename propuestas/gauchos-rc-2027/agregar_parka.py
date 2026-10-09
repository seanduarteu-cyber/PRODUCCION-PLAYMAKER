"""Agrega la Parka larga (GAU-23) a la propuesta base y pasa Accesorios a GAU-24.

Uso:
    python3 propuestas/gauchos-rc-2027/agregar_parka.py

Lee  base/Propuesta_Gauchos_Rugby_Club_2027_base.pdf   (original, no se modifica)
Crea base/Propuesta_Gauchos_Rugby_Club_2027_base_v2.pdf (la que usa propuesta.json)

Cambios:
  - Ficha nueva "Parka larga" (FICHA 23 · PRESENTACIÓN Y ABRIGO) después del Pantalón pitillo,
    con el mismo diseño de las demás fichas.
  - Accesorios del club pasa a FICHA 24 / GAU-24.
  - Catálogo: "Veinticuatro líneas", fila nueva GAU-23 y Accesorios como GAU-24.
  - Cuadro de valores: fila nueva GAU-23 y Accesorios como GAU-24 (totales reacomodados).
  - Numeración de páginas corrida desde la ficha nueva.
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
P_CATALOGO, P_MODELO_FICHA, P_PITILLO, P_ACCESORIOS, P_CUADRO = 2, 3, 24, 25, 26
NUEVA = P_PITILLO + 1  # la parka queda justo después del Pantalón pitillo

PARKA = {
    "ficha": "FICHA 23 · PRESENTACIÓN Y ABRIGO",
    "codigo": "GAU-23",
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


# ---------------------------------------------------------------- lectura de estilos

class Run:
    """Tramo de texto de la base con su estilo (fuente, tamaño, color, espaciado, línea base)."""

    def __init__(self, chars, alto_pagina):
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
                runs.append(Run(actual, page.height))
                actual = [b]
            else:
                actual.append(b)
        runs.append(Run(actual, page.height))
    return runs


def buscar(runs, inicio, cerca_de=None):
    candidatos = [r for r in runs if r.texto.startswith(inicio)]
    if cerca_de is not None:
        candidatos.sort(key=lambda r: abs(r.top - cerca_de))
    if not candidatos:
        raise LookupError(f"No se encontró «{inicio}» en la base")
    return candidatos[0]


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
        lineas_catalogo = pdf.pages[P_CATALOGO].lines
        lineas_cuadro = pdf.pages[P_CUADRO].lines
        rects_cuadro = pdf.pages[P_CUADRO].rects
        w, h = pdf.pages[0].width, pdf.pages[0].height
        n_base = len(pdf.pages)

    doc = pymupdf.open(BASE)
    doc.insert_pdf(pymupdf.open(BASE), from_page=P_MODELO_FICHA, to_page=P_MODELO_FICHA, start_at=NUEVA)
    final = lambda i: i if i < NUEVA else i + 1  # índice en el documento nuevo
    capa = Capa(len(doc), w, h)
    tachar = {i: [] for i in range(len(doc))}  # rects (top-based) a borrar por página
    borrar_graficos = set()

    def reemplazar(pag_base, run, texto, alinear="izq", pag_final=None):
        """Borra un tramo de la base y escribe otro texto con el mismo estilo y posición."""
        p = final(pag_base) if pag_final is None else pag_final
        tachar[p].append((run.x0 - 1, run.top - 1.5, run.x1 + 1, run.top + run.size * 1.25))
        x = run.x1 if alinear == "der" else run.x0
        capa.texto(p, run, texto, x, run.base, alinear)

    # 1. Ficha nueva (copia de la ficha modelo con sus textos cambiados)
    m = R[P_MODELO_FICHA]
    reemplazar(P_MODELO_FICHA, buscar(m, "FICHA"), PARKA["ficha"], pag_final=NUEVA)
    reemplazar(P_MODELO_FICHA, buscar(m, "GAU-"), PARKA["codigo"], "der", pag_final=NUEVA)
    reemplazar(P_MODELO_FICHA, buscar(m, "Camiseta"), PARKA["titulo"], pag_final=NUEVA)
    reemplazar(P_MODELO_FICHA, buscar(m, "Negra con"), PARKA["bajada"], pag_final=NUEVA)
    reemplazar(P_MODELO_FICHA, buscar(m, "XS a 5XL"), PARKA["tallas"], pag_final=NUEVA)
    etiquetas = [r for r in m if r.fuente == "Poppins-SemiBold" and 480 < r.top < 700 and r.size < 7]
    cuerpos = [r for r in m if r.fuente == "Poppins-Regular" and 480 < r.top < 700]
    for r in etiquetas + cuerpos:
        tachar[NUEVA].append((r.x0 - 1, r.top - 1.5, r.x1 + 1, r.top + r.size * 1.25))
    etiquetas.sort(key=lambda r: (round(r.top), r.x0))
    estilo_cuerpo = cuerpos[0]
    interlinea = sorted({round(r.base, 1) for r in cuerpos}, reverse=True)
    interlinea = min(a - b for a, b in zip(interlinea, interlinea[1:]) if a - b > 1)
    primera = min(r.base for r in cuerpos if abs(r.top - etiquetas[0].top) < 20)
    salto_etiqueta = etiquetas[0].base - primera
    ancho_col = etiquetas[1].x0 - etiquetas[0].x0 - 18
    for etq, (titulo, cuerpo) in zip(etiquetas, PARKA["bloques"]):
        capa.texto(NUEVA, etq, titulo, etq.x0, etq.base)
        for k, linea in enumerate(partir(capa, estilo_cuerpo, cuerpo, ancho_col)):
            capa.texto(NUEVA, estilo_cuerpo, linea, etq.x0, etq.base - salto_etiqueta - k * interlinea)

    # 2. Ficha de accesorios pasa a 24
    a = R[P_ACCESORIOS]
    reemplazar(P_ACCESORIOS, buscar(a, "FICHA"), "FICHA 24 · ACCESORIOS")
    reemplazar(P_ACCESORIOS, buscar(a, "GAU-"), "GAU-24", "der")

    # 3. Numeración de páginas desde la ficha nueva
    for i in range(P_PITILLO, n_base):
        num = [r for r in R[i] if r.top > 790 and r.texto.isdigit()]
        if not num:
            continue
        if i == P_PITILLO:  # la ficha nueva hereda el número del modelo, corrido
            reemplazar(P_MODELO_FICHA, buscar(R[P_MODELO_FICHA], "04", cerca_de=801),
                       f"{int(num[0].texto) + 1:02d}", "der", pag_final=NUEVA)
        else:
            reemplazar(i, num[0], f"{int(num[0].texto) + 1:02d}", "der")

    # 4. Catálogo: texto de introducción, fila nueva y Accesorios como GAU-24
    c = R[P_CATALOGO]
    intro = [buscar(c, "Veintitrés"), buscar(c, "en las páginas")]
    for r in intro:
        tachar[P_CATALOGO].append((r.x0 - 1, r.top - 1.5, r.x1 + 1, r.top + r.size * 1.3))
    texto_intro = " ".join(r.texto for r in intro).replace("Veintitrés", "Veinticuatro")
    paso_intro = intro[0].base - intro[1].base
    for k, linea in enumerate(partir(capa, intro[0], texto_intro, intro[0].x1 - intro[0].x0 + 3.5)):
        capa.texto(P_CATALOGO, intro[0], linea, intro[0].x0, intro[0].base - k * paso_intro)

    fila = {"cod": buscar(c, "GAU-22"), "nom": buscar(c, "Pantalón pitillo"),
            "ficha": buscar(c, "Ficha 22")}
    paso = buscar(c, "GAU-21").base - fila["cod"].base  # distancia entre filas
    cab_acc, cod_acc = buscar(c, "ACCESORIOS"), buscar(c, "GAU-23")
    zona_top = fila["nom"].top + 14
    tachar[P_CATALOGO].append((40, zona_top, w - 40, cod_acc.top + 16))
    borrar_graficos.add(P_CATALOGO)
    for clave, texto, al in (("cod", "GAU-23", "izq"), ("nom", "Parka larga", "izq"), ("ficha", "Ficha 23", "der")):
        r = fila[clave]
        capa.texto(P_CATALOGO, r, texto, r.x1 if al == "der" else r.x0, r.base - paso, al)
    capa.texto(P_CATALOGO, cab_acc, cab_acc.texto, cab_acc.x0, cab_acc.base - paso)
    for clave, texto, al in (("cod", "GAU-24", "izq"), ("nom", "Accesorios del club", "izq"),
                             ("ficha", "Ficha 24", "der")):
        r = fila[clave]
        capa.texto(P_CATALOGO, r, texto, r.x1 if al == "der" else r.x0,
                   cod_acc.base - (fila["cod"].base - r.base) - paso, al)
    regla = next(l for l in lineas_catalogo if zona_top < l["top"] < cod_acc.top)
    capa.linea(P_CATALOGO, regla["stroking_color"], regla["linewidth"], regla["x0"], regla["x1"],
               regla["top"] + paso)

    # 5. Cuadro de valores
    q = R[P_CUADRO]
    PQ = final(P_CUADRO)
    fila = {k: buscar(q, t, cerca_de=636) for k, t in
            (("cod", "GAU-22"), ("nom", "Pantalón pitillo"), ("cant", "[00]"), ("valor", "$[00.000]"))}
    paso = buscar(q, "GAU-21").base - fila["cod"].base  # distancia entre filas
    zona_top = fila["nom"].top + 10
    regla = next(l for l in lineas_cuadro if zona_top < l["top"] < 760)
    caja = next(r for r in rects_cuadro if r["fill"] and r["top"] > 700 and r["width"] > 200)
    cebras = [r for r in rects_cuadro if r["fill"] and r["height"] < 25 and r["width"] > 400
              and min(r["non_stroking_color"]) > 0.8 and r["top"] < fila["cod"].top]  # franjas grises
    modelo = cebras[-1]
    cod_modelo = min((r for r in q if r.texto.startswith("GAU-")), key=lambda r: abs(r.top - modelo["top"] - 4.7))
    cebra_off = modelo["top"] - cod_modelo.top
    tachar[PQ].append((40, zona_top, w - 40, caja["bottom"] + 4))
    borrar_graficos.add(PQ)

    def fila_cuadro(base_cod, cod, nombre):
        for clave, texto in (("cod", cod), ("nom", nombre), ("cant", "[00]"), ("valor", "$[00.000]")):
            r = fila[clave]
            capa.texto(PQ, r, texto, r.x0, base_cod - (fila["cod"].base - r.base))

    def cebra(base_cod):
        top = fila["cod"].top + (fila["cod"].base - base_cod) + cebra_off
        capa.rect(PQ, modelo["non_stroking_color"], modelo["x0"], top, modelo["x1"], top + modelo["height"])

    base_parka = fila["cod"].base - paso
    cebra(base_parka)
    fila_cuadro(base_parka, "GAU-23", "Parka larga")
    cab = buscar(q, "ACCESORIOS")
    cod_viejo = buscar(q, "GAU-23")
    corrimiento = 13.0  # se comprime el espacio entre grupos para que entren los totales
    capa.texto(PQ, cab, cab.texto, cab.x0, cab.base - corrimiento)
    base_acc = cod_viejo.base - corrimiento
    cebra(base_acc)
    fila_cuadro(base_acc, "GAU-24", "Accesorios del club")
    d_tot = 1.0  # los totales bajan apenas: se quita aire entre líneas
    capa.linea(PQ, regla["stroking_color"], regla["linewidth"], regla["x0"], regla["x1"], regla["top"] + 7)
    sub_l, sub_v = buscar(q, "Subtotal"), buscar(q, "$[00.000]", cerca_de=713.7)
    iva_l, iva_v = buscar(q, "IVA 19%"), buscar(q, "$[00.000]", cerca_de=731.7)
    for r, dy in ((sub_l, 4.8), (sub_v, 4.8), (iva_l, 2.3), (iva_v, 2.3)):
        capa.texto(PQ, r, r.texto, r.x0, r.base - dy)
    capa.rect(PQ, caja["non_stroking_color"], caja["x0"], caja["top"] + d_tot, caja["x1"], caja["bottom"] + d_tot)
    for r in (buscar(q, "TOTAL"), buscar(q, "$[00.000]", cerca_de=753.8)):
        capa.texto(PQ, r, r.texto, r.x0, r.base - d_tot)

    # 6. Borrar lo reemplazado y superponer lo nuevo
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
