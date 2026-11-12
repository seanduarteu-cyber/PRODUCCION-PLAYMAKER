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
    "variantes":  {"15": [{"rotulo": "SIN CAPUCHA", "codigo": "OGR-10A", "producto": "Cortaviento sin capucha",
                           "fila": "14"}, ...]}  ficha con un precio por variante (de izquierda a derecha); en el
                  cuadro de valores, cada variante ocupa la fila de la ficha "fila" de la base (aunque esa
                  ficha salga), con su código y su nombre
    "simbolos":   [[" · ", "   "]]  se cambian en todo texto que se escribe (incluidos los que no cambian de
                  otro modo), después de los reemplazos
    "quitar":     ["04", "08"]  fichas que no van: salen sus páginas y sus filas del catálogo y del
                  cuadro de valores, y las demás se renumeran (ficha, código y página)
Las fichas se nombran siempre con el número de la base de origen; el resultado lleva la numeración
nueva (la que usa propuesta.json).

Los textos nuevos se dibujan con las mismas fuentes, tamaños, colores y espaciado que la base.
"""

import json
import re
import sys
from pathlib import Path

import pdfplumber
import pymupdf
from pypdf import PdfReader

from base_pdf import Capa, Estilo, Run, guardar, partir, runs_de

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


def separar_marcador(runs):
    """El rótulo del precio y su marcador "$[00.000]" vienen en un mismo tramo: se separan para poder
    reescribir el rótulo sin tocar el marcador (que después reemplaza montar_propuesta.py)."""
    salida = []
    for r in runs:
        k = r.texto.find("$[")
        if k > 0 and r.texto[:k].strip():
            izq = r.chars[:k]
            while izq and izq[-1]["text"] == " ":
                izq = izq[:-1]
            rotulo = Run(izq)
            rotulo.fin_derecha = True  # el rótulo nuevo termina donde terminaba el anterior
            salida += [rotulo, Run(r.chars[k:])]
        else:
            salida.append(r)
    return salida


def main(cfg_path):
    cfg_path = Path(cfg_path).resolve()
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    base, salida = cfg_path.parent / cfg["base"], cfg_path.parent / cfg["salida"]
    viejo_cod, nuevo_cod = cfg["codigo"]
    reemplazos = cfg.get("reemplazos", [])

    with pdfplumber.open(base) as pdf:
        R = [separar_marcador(runs_de(p)) for p in pdf.pages]
        rects = [p.rects for p in pdf.pages]
        trazos = [p.lines for p in pdf.pages]
        w, h = pdf.pages[0].width, pdf.pages[0].height

    doc = pymupdf.open(base)
    capa = Capa(len(doc), w, h)
    simbolos = cfg.get("simbolos", [])

    def limpiar(texto):
        for viejo, nuevo in simbolos:
            texto = texto.replace(viejo, nuevo)
        return texto

    dibujar = capa.texto  # todo lo que se escribe pasa por la limpieza de símbolos
    capa.texto = lambda pag, e, texto, x, base, modo="izq": dibujar(pag, e, limpiar(texto), x, base, modo)
    tachar = {i: [] for i in range(len(doc))}
    borrar_graficos = set()
    hecho = set()  # tramos ya reescritos (id)

    def borrar(pag, run, alto=1.25):
        tachar[pag].append((run.x0 - 1, run.top - 1.5, run.x1 + 1, run.top + run.size * alto))
        hecho.add(id(run))

    def alinear(run, pag):
        if getattr(run, "fin_derecha", False):
            return "der", run.x1
        # centrado: su centro es el de la página y no comparte el margen izquierdo con otro texto
        margen_comun = any(o is not run and abs(o.x0 - run.x0) < 1 for o in R[pag])
        if abs((run.x0 + run.x1) / 2 - w / 2) < 3 and run.x0 > X0 + 5 and not margen_comun:
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
            modo, x = alinear(e, pag)
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

    productos = {}  # nombre anterior -> nombre nuevo, para el catálogo y el cuadro de valores
    for num, f in cfg.get("fichas", {}).items():
        if num not in fichas:
            sys.exit(f"La base no tiene la ficha {num}")
        pag, runs = fichas[num], R[fichas[num]]
        titulo = next(r for r in runs if r.fuente == "PlayfairDisplay-Bold" and r.size > 18)
        if f.get("titulo"):
            borrar(pag, titulo, alto=1.0)  # la bajada en cursiva va justo debajo
            capa.texto(pag, titulo, f["titulo"], titulo.x0, titulo.base)
            productos[titulo.texto] = f["titulo"]
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

    variantes = cfg.get("variantes", {})
    for num, lista in variantes.items():  # un rótulo y un marcador de precio por variante
        pag = fichas[num]
        rotulo = next(r for r in R[pag] if getattr(r, "fin_derecha", False))
        marcador = next(r for r in R[pag] if r.texto.startswith("$[") and abs(r.top - rotulo.top) < 3)
        separacion = marcador.x0 - rotulo.x1
        borrar(pag, rotulo)
        derecha = marcador.x1  # el último usa el marcador que ya está; los anteriores van a su izquierda
        for k, v in enumerate(reversed(lista)):
            if k:
                capa.texto(pag, marcador, "$[00.000]", derecha, marcador.base, "der")
            fin_rotulo = derecha - (marcador.x1 - marcador.x0) - separacion
            capa.texto(pag, rotulo, v["rotulo"], fin_rotulo, rotulo.base, "der")
            derecha = fin_rotulo - capa.ancho(rotulo, v["rotulo"]) - 24

    # 2. Fichas que salen: el resto sube de número (ficha, código y página)
    quitar = sorted(cfg.get("quitar", []))
    if any(n not in fichas for n in quitar):
        sys.exit(f"La base no tiene alguna de las fichas a quitar: {quitar}")
    nuevo_num = {n: f"{k + 1:02d}" for k, n in enumerate(n for n in sorted(fichas) if n not in quitar)}
    paginas_fuera = [fichas[n] for n in quitar]
    paginas = [i for i in range(len(R)) if i not in paginas_fuera]
    patron = re.compile(rf"\b{viejo_cod}-(\d+)")

    def codigo_nuevo(texto):
        return patron.sub(lambda m: f"{nuevo_cod}-{nuevo_num.get(m.group(1), m.group(1))}", texto)

    for num, nuevo in nuevo_num.items():
        if nuevo != num:
            r = next(r for r in R[fichas[num]] if r.top < 100 and r.texto.startswith(f"FICHA {num}"))
            borrar(fichas[num], r)
            capa.texto(fichas[num], r, r.texto.replace(f"FICHA {num}", f"FICHA {nuevo}", 1), r.x0, r.base)
    for k, pag in enumerate(paginas):  # número de página del pie
        num = next((r for r in R[pag] if r.top > 790 and r.texto.isdigit()), None)
        if num and int(num.texto) != k + 1:
            borrar(pag, num)
            capa.texto(pag, num, f"{k + 1:02d}", num.x1, num.base, "der")

    # 3. Catálogo y cuadro de valores: sin las filas que salen, todo lo de abajo sube y se renumera
    for pag, runs in enumerate(R):
        filas = sorted([r for r in runs if r.top > 100 and patron.fullmatch(r.texto)], key=lambda r: r.top)
        if len(filas) < 5:
            continue
        paso = min(b.top - a.top for a, b in zip(filas, filas[1:]))
        ini, fin = filas[0].top - 30, 770
        en_cuadro = any(r.texto == "CANTIDAD" for r in runs)
        # en el cuadro, las variantes ocupan las filas indicadas (aunque su ficha salga) con código y nombre propios
        por_fila = {v["fila"]: v for lista in variantes.values() for v in lista} if en_cuadro else {}
        textos_variante = {}
        for r in filas:
            v = por_fila.get(patron.fullmatch(r.texto).group(1))
            if v:
                textos_variante[id(r)] = v["codigo"]
                nombre = next(o for o in runs if abs(o.top - r.top) < 3 and r.x1 < o.x0 < 300)
                textos_variante[id(nombre)] = v["producto"]
        bandas = [(r.top - 6, r.top - 6 + paso) for r in filas
                  if patron.fullmatch(r.texto).group(1) in quitar and patron.fullmatch(r.texto).group(1) not in por_fila]

        def mover(top):  # nuevo top, o None si el elemento es de una fila que sale
            if any(a <= top < b for a, b in bandas):
                return None
            return top - paso * sum(1 for a, b in bandas if b <= top)

        tachar[pag].append((30, ini, w - 30, fin))
        borrar_graficos.add(pag)
        cebra = [r for r in rects[pag] if r["fill"] and ini <= r["top"] <= fin and r["height"] < 20
                 and r["width"] > 400 and min(r["non_stroking_color"]) > 0.9]
        for r in rects[pag]:
            if r in cebra or not ini <= r["top"] <= fin or (top := mover(r["top"])) is None:
                continue
            if r["fill"]:
                capa.rect(pag, r["non_stroking_color"], r["x0"], top, r["x1"], top + r["height"])
            if r["stroke"]:
                capa.marco(pag, r["stroking_color"], r["linewidth"], r["x0"], top, r["x1"], top + r["height"])
        for ln in trazos[pag]:
            if ini <= ln["top"] <= fin and (top := mover(ln["top"])) is not None:
                capa.linea(pag, ln["stroking_color"], ln["linewidth"], ln["x0"], ln["x1"], top)
        quedan = []  # filas que quedan, con su categoría, para volver a poner la cebra
        categoria = None
        for r in sorted((r for r in runs if ini <= r.top <= fin), key=lambda r: r.top):
            hecho.add(id(r))
            if (top := mover(r.top)) is None:
                continue
            if r.fuente == "Poppins-SemiBold" and r.texto.isupper() and r.x0 < X0 + 1:
                categoria = r
            texto = textos_variante.get(id(r)) or codigo_nuevo(productos.get(r.texto, r.texto))
            if re.fullmatch(r"Ficha \d+", texto):
                texto = f"Ficha {nuevo_num[texto[-2:]]}"
            if patron.fullmatch(r.texto):
                quedan.append((categoria, top))
            modo, x = alinear(r, pag)
            capa.texto(pag, r, texto, x, r.base + (r.top - top), modo)
        if cebra:
            fila0 = min(filas, key=lambda r: abs(r.top - cebra[0]["top"]))
            arriba, alto, c0 = fila0.top - cebra[0]["top"], cebra[0]["height"], cebra[0]
            for k, (cat, top) in enumerate(quedan):
                if sum(1 for c, _ in quedan[:k] if c is cat) % 2 == 0:
                    capa.rect(pag, c0["non_stroking_color"], c0["x0"], top - arriba, c0["x1"], top - arriba + alto)

    for pag, runs in enumerate(R):  # productos renombrados en el resto del documento
        for r in runs:
            if id(r) not in hecho and r.texto in productos:
                borrar(pag, r)
                capa.texto(pag, r, productos[r.texto], r.x0, r.base)

    # 4. Códigos de producto en el encabezado de cada ficha
    for pag, runs in enumerate(R):
        for r in runs:
            if id(r) not in hecho and patron.search(r.texto):
                borrar(pag, r)
                modo, x = alinear(r, pag)
                capa.texto(pag, r, codigo_nuevo(r.texto), x, r.base, modo)

    # 5. Paleta del club (antes de los textos: sus etiquetas anteriores no se reescriben)
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
            capa.texto(pag, estilo, f"{nombre} {hexa.upper()}", x0 + m0["width"] / 2, nombres[0].base, "centro")
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

    # 6. Nombre del club y demás textos: cada párrafo que cambia se vuelve a armar
    for pag, runs in enumerate(R):
        for lineas in parrafos_de([r for r in runs if id(r) not in hecho]):
            texto = " ".join(r.texto for r in lineas)
            nuevo = texto
            for viejo, reemplazo in reemplazos:
                nuevo = nuevo.replace(viejo, reemplazo)
            nuevo = limpiar(nuevo)
            if nuevo == texto:
                continue
            n = escribir_parrafo(pag, lineas, nuevo)
            if n > len(lineas):
                print(f"    Aviso: página {pag + 1}, «{nuevo[:50]}…» pasa de {len(lineas)} a {n} líneas")

    # 7. Lo que quedó con el nombre del club de origen (para revisarlo a mano)
    for pag, runs in enumerate(R):
        for r in runs:
            if id(r) not in hecho and any(v in r.texto for v, _ in reemplazos + simbolos):
                print(f"    Aviso: página {pag + 1} sin cambiar: «{r.texto[:60]}»")

    salida.parent.mkdir(parents=True, exist_ok=True)
    n = guardar(doc, tachar, borrar_graficos, capa, salida, PdfReader(base).metadata, paginas_fuera)
    print(f"OK  {salida.relative_to(cfg_path.parent)}  ({n} páginas, {len(cfg.get('fichas', {}))} fichas reescritas"
          f"{f', sin las fichas ' + ', '.join(quitar) if quitar else ''})")
    if quitar:
        print("    Códigos nuevos: " + ", ".join(f"{viejo_cod}-{a} -> {nuevo_cod}-{b}" for a, b in nuevo_num.items()))


if __name__ == "__main__":
    main(sys.argv[1])
