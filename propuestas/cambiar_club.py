"""Pasa la propuesta base de un club a otro club con el mismo modelo comercial.

Uso:
    python3 propuestas/cambiar_club.py propuestas/old-green-rc-2027/club.json

club.json (rutas relativas al JSON):
    "base":       PDF base del club de origen, ya armado (p. ej. la base_v2 de Gauchos)
    "salida":     PDF base del nuevo club (la que usa su propuesta.json)
    "codigo":     ["GAU", "OGR"]  prefijo de los códigos de producto (GAU-01 -> OGR-01)
    "reemplazos": [["Gauchos", "Old Green"], ...]  en todo el documento, salvo en las fichas que se
                  reescriben; cada párrafo que cambia se vuelve a armar con su estilo y su ancho
    "paleta":     [["Verde", "#1F5B3A"], ...]  colores del recuadro PALETA DEL CLUB (hasta 6)
    "fichas":     {"01": {"titulo": "...", "bajada": "...", "bloques": [["CUELLO", "..."], ...]}}
                  bajada y bloques (hasta 6, en dos columnas) de cada ficha; titulo es opcional

Los textos nuevos se dibujan con las mismas fuentes, tamaños, colores y espaciado que la base.
"""

import json
import re
import sys
from pathlib import Path

import pdfplumber
import pymupdf
from pypdf import PdfReader

from base_pdf import Capa, Estilo, guardar, partir, runs_de

X0, X1 = 58.0, 537.3  # caja de texto de la base
ZONA_BLOQUES = (480, 700)  # top de etiquetas y textos de los bloques de una ficha


def parrafos_de(runs):
    """Agrupa los tramos en párrafos: mismo estilo, mismo margen izquierdo e interlineado parejo."""
    grupos = {}
    for r in runs:
        if r.espaciado is None:
            continue
        grupos.setdefault((r.fuente, round(r.size, 1), round(r.x0)), []).append(r)
    parrafos = []
    for lineas in grupos.values():
        lineas.sort(key=lambda r: -r.base)
        actual = [lineas[0]]
        for a, b in zip(lineas, lineas[1:]):
            if a.base - b.base < 1.3 * a.size * 1.4:
                actual.append(b)
            else:
                parrafos.append(actual)
                actual = [b]
        parrafos.append(actual)
    return parrafos


def main(cfg_path):
    cfg_path = Path(cfg_path).resolve()
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    base, salida = cfg_path.parent / cfg["base"], cfg_path.parent / cfg["salida"]
    viejo_cod, nuevo_cod = cfg["codigo"]
    reemplazos = cfg.get("reemplazos", [])

    with pdfplumber.open(base) as pdf:
        R = [runs_de(p) for p in pdf.pages]
        rects = [p.rects for p in pdf.pages]
        w, h = pdf.pages[0].width, pdf.pages[0].height

    doc = pymupdf.open(base)
    capa = Capa(len(doc), w, h)
    tachar = {i: [] for i in range(len(doc))}
    borrar_graficos = set()
    hecho = set()  # tramos ya reescritos (id)

    def borrar(pag, run, alto=1.25):
        tachar[pag].append((run.x0 - 1, run.top - 1.5, run.x1 + 1, run.top + run.size * alto))
        hecho.add(id(run))

    def alinear(run):
        if abs((run.x0 + run.x1) / 2 - w / 2) < 3 and run.x0 > X0 + 5:
            return "centro", w / 2
        if abs(run.x1 - X1) < 1.5 and run.x0 > X0 + 5:
            return "der", run.x1
        return "izq", run.x0

    def escribir_parrafo(pag, lineas, texto, ancho=None):
        """Reemplaza las líneas de un párrafo por otro texto (mismo estilo, margen e interlineado)."""
        e = lineas[0]
        for r in lineas:
            borrar(pag, r, alto=1.35)
        if len(lineas) == 1:
            modo, x = alinear(e)
            if modo != "izq" or capa.ancho(e, texto) <= (ancho or X1 - e.x0):
                capa.texto(pag, e, texto, x, e.base, modo)
                return 1
        paso = lineas[0].base - lineas[1].base if len(lineas) > 1 else e.size * 1.45
        ancho = ancho or max(r.x1 - r.x0 for r in lineas) + 2
        nuevas = partir(capa, e, texto, ancho)
        for k, linea in enumerate(nuevas):
            capa.texto(pag, e, linea, e.x0, e.base - k * paso)
        return len(nuevas)

    # 1. Fichas: código, título, bajada y bloques
    fichas = {}
    for i, runs in enumerate(R):
        ficha = next((r for r in runs if r.top < 100 and re.match(r"FICHA \d+", r.texto)), None)
        if ficha:
            fichas[re.match(r"FICHA (\d+)", ficha.texto).group(1)] = i
    modelo = next(i for i in fichas.values()
                  if len([r for r in R[i] if r.fuente == "Poppins-SemiBold" and r.size < 7
                          and ZONA_BLOQUES[0] < r.top < ZONA_BLOQUES[1]]) == 6)
    m = R[modelo]
    celdas = sorted([r for r in m if r.fuente == "Poppins-SemiBold" and r.size < 7
                     and ZONA_BLOQUES[0] < r.top < ZONA_BLOQUES[1]], key=lambda r: (round(r.top), r.x0))
    cuerpos_m = [r for r in m if r.fuente == "Poppins-Regular" and ZONA_BLOQUES[0] < r.top < ZONA_BLOQUES[1]]
    cuerpo = cuerpos_m[0]
    bases = sorted({round(r.base, 1) for r in cuerpos_m}, reverse=True)
    interlinea = min(a - b for a, b in zip(bases, bases[1:]) if a - b > 1)
    salto = celdas[0].base - max(r.base for r in cuerpos_m if abs(r.top - celdas[0].top) < 20)
    ancho_col = celdas[1].x0 - celdas[0].x0 - 18
    alto_celda = celdas[0].base - celdas[2].base  # distancia entre filas de bloques (base PDF crece hacia arriba)

    for num, f in cfg.get("fichas", {}).items():
        if num not in fichas:
            sys.exit(f"La base no tiene la ficha {num}")
        pag, runs = fichas[num], R[fichas[num]]
        titulo = next(r for r in runs if r.fuente == "PlayfairDisplay-Bold" and r.size > 18)
        if f.get("titulo"):
            borrar(pag, titulo, alto=1.0)  # la bajada en cursiva va justo debajo
            capa.texto(pag, titulo, f["titulo"], titulo.x0, titulo.base)
        bajada = next(r for r in runs if r.fuente == "PlayfairDisplay-Italic" and titulo.top < r.top < titulo.top + 50)
        if capa.ancho(bajada, f["bajada"]) > X1 - X0:
            sys.exit(f"Ficha {num}: la bajada no cabe en una línea")
        borrar(pag, bajada)
        capa.texto(pag, bajada, f["bajada"], bajada.x0, bajada.base)
        for r in runs:
            if r.fuente.startswith("Poppins") and ZONA_BLOQUES[0] < r.top < ZONA_BLOQUES[1]:
                borrar(pag, r)
        if len(f["bloques"]) > len(celdas):
            sys.exit(f"Ficha {num}: más de {len(celdas)} bloques")
        for celda, (etq, txt) in zip(celdas, f["bloques"]):
            capa.texto(pag, celda, etq, celda.x0, celda.base)
            lineas = partir(capa, cuerpo, txt, ancho_col)
            if salto + (len(lineas) - 1) * interlinea > alto_celda - 14:
                sys.exit(f"Ficha {num}, {etq}: el texto ocupa {len(lineas)} líneas y no cabe")
            for k, linea in enumerate(lineas):
                capa.texto(pag, cuerpo, linea, celda.x0, celda.base - salto - k * interlinea)

    # 2. Códigos de producto (encabezado de ficha, catálogo y cuadro de valores)
    patron = re.compile(rf"\b{viejo_cod}-(?=\d)")
    for pag, runs in enumerate(R):
        for r in runs:
            if id(r) not in hecho and patron.search(r.texto):
                borrar(pag, r)
                modo, x = alinear(r)
                capa.texto(pag, r, patron.sub(f"{nuevo_cod}-", r.texto), x, r.base, modo)

    # 3. Nombre del club y demás textos: cada párrafo que cambia se vuelve a armar
    for pag, runs in enumerate(R):
        for lineas in parrafos_de([r for r in runs if id(r) not in hecho]):
            texto = " ".join(r.texto for r in lineas)
            nuevo = texto
            for viejo, reemplazo in reemplazos:
                nuevo = nuevo.replace(viejo, reemplazo)
            if nuevo == texto:
                continue
            n = escribir_parrafo(pag, lineas, nuevo)
            if n > len(lineas):
                print(f"    Aviso: página {pag + 1}, «{nuevo[:50]}…» pasa de {len(lineas)} a {n} líneas")

    # 4. Paleta del club
    paleta = cfg.get("paleta")
    if paleta:
        pag = next(i for i, runs in enumerate(R) if any(r.texto == "PALETA DEL CLUB" for r in runs))
        rotulo = next(r for r in R[pag] if r.texto == "PALETA DEL CLUB")
        muestras = sorted([r for r in rects[pag] if r["fill"] and r["stroke"] and rotulo.top < r["top"] < rotulo.top + 40
                           and 15 < r["height"] < 40], key=lambda r: r["x0"])
        nombres = [r for r in R[pag] if muestras[0]["bottom"] < r.top < muestras[0]["bottom"] + 15]
        m0 = muestras[0]
        paso_x = muestras[1]["x0"] - m0["x0"]
        tachar[pag].append((m0["x0"] - 2, m0["top"] - 2, X1 + 1, max(r.top + r.size * 1.35 for r in nombres)))
        borrar_graficos.add(pag)
        hecho.update(id(r) for r in nombres)
        estilo = Estilo(nombres[0].fuente, nombres[0].size, nombres[0].color)
        for k, (nombre, hexa) in enumerate(paleta):
            x0 = m0["x0"] + k * paso_x
            color = tuple(int(hexa.lstrip("#")[j:j + 2], 16) / 255 for j in (0, 2, 4))
            capa.rect(pag, color, x0, m0["top"], x0 + m0["width"], m0["bottom"])
            capa.marco(pag, m0["stroking_color"], m0["linewidth"], x0, m0["top"], x0 + m0["width"], m0["bottom"])
            capa.texto(pag, estilo, f"{nombre} · {hexa.upper()}", x0 + m0["width"] / 2, nombres[0].base, "centro")
        # franja de colores bajo el emblema de la portada: mismo largo, un tramo por color
        franja = sorted([r for r in rects[0] if r["fill"] and r["height"] < 12 and r["width"] < 100],
                        key=lambda r: r["x0"])
        if franja:
            f0, f1 = franja[0], franja[-1]
            tachar[0].append((f0["x0"] - 1, f0["top"] - 1, f1["x1"] + 1, f0["bottom"] + 1))
            borrar_graficos.add(0)
            tramo = (f1["x1"] - f0["x0"]) / len(paleta)
            for k, (_, hexa) in enumerate(paleta):
                color = tuple(int(hexa.lstrip("#")[j:j + 2], 16) / 255 for j in (0, 2, 4))
                x0 = f0["x0"] + k * tramo
                capa.rect(0, color, x0, f0["top"], x0 + tramo, f0["bottom"])
                if f0["stroke"]:
                    capa.marco(0, f0["stroking_color"], f0["linewidth"], x0, f0["top"], x0 + tramo, f0["bottom"])

    # 5. Lo que quedó con el nombre del club de origen (para revisarlo a mano)
    for pag, runs in enumerate(R):
        for r in runs:
            if id(r) not in hecho and any(v in r.texto for v, _ in reemplazos):
                print(f"    Aviso: página {pag + 1} sin cambiar: «{r.texto[:60]}»")

    salida.parent.mkdir(parents=True, exist_ok=True)
    n = guardar(doc, tachar, borrar_graficos, capa, salida, PdfReader(base).metadata)
    print(f"OK  {salida.relative_to(cfg_path.parent)}  ({n} páginas, {len(cfg.get('fichas', {}))} fichas reescritas)")


if __name__ == "__main__":
    main(sys.argv[1])
