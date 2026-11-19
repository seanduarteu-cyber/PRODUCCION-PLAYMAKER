"""Reemplaza en los renders los logos aproximados por los logos oficiales (club y Playmaker).

Uso:
    python3 propuestas/reemplazar_logos.py propuestas/gauchos-rc-2027/logos.json

logos.json:
    {"logos": {"escudo":  {"archivo": "img/escudo_gauchos.png", "color": "original"},
               "isotipo": {"archivo": "../_recursos/playmaker_isotipo_blanco.png", "color": "tinta"}},
     "salida": "img/con_logos",
     "renders": {"img/01_player_tee_home_op1.jpg": [
         {"logo": "escudo",  "caja": [x0, y0, x1, y1]},
         {"logo": "isotipo", "zona": [x0, y0, x1, y1], "lateral": true},
         {"borrar": [x0, y0, x1, y1]}]}}

- "caja": el logo anterior ocupa exactamente esa caja.
- "zona": caja holgada (con tela alrededor); el logo anterior se ubica solo dentro de ella.
- "lateral": vista de costado; el logo se angosta al ancho del anterior (o al factor indicado).
- "tela": color RGB de la prenda, cuando el logo está al borde y la zona no puede quedar solo sobre tela.
- "pegar_en": caja donde pegar el logo nuevo, si no debe ir exactamente donde estaba el anterior.
- "blanco": el logo anterior es blanco (o gris claro) y la zona cruza tela de distintos colores
  (franjas): se ubica por su color y no por el contraste con la tela. "minimo" (140 por defecto) es
  el brillo mínimo del logo; más bajo para letras grises, como las de la etiqueta del cuello.
- "franjas" (con "caja"): la tela alrededor del logo tiene varios colores (franjas); se borra solo lo
  que no se parece a ninguno de los colores de tela que hay alrededor de la caja.
- "por_ancho": el logo nuevo toma el ancho del anterior en vez del alto (para que su cinta cubra la
  del escudo anterior); con "caja" o con "zona" sobre tela de un solo color.
- "extruir" (con "caja"): el logo está sobre franjas diagonales rectas (p. ej. un galón en V); la caja
  se rellena continuando las franjas desde sus dos costados, con la pendiente dada (dy/dx de las
  franjas en la imagen: negativa si suben hacia la derecha), en vez de reconstruirla por inpainting.
  Con [pendiente, "izq"] o [pendiente, "der"] toma solo ese costado (cuando el otro no es tela limpia).
  Con "bordes", busca los bordes entre colores de tela en los dos costados y los une en línea recta
  (para franjas que no son paralelas o que se curvan con la caída de la tela).
  También sirve con "borrar": la zona se rellena así en vez de reconstruirse por inpainting.
- "completa" (con "caja"): se reconstruye toda la caja y no solo lo que difiere de la tela (parches
  bordados con fondo de otro tono); conviene sumarle "textura".
- "escala" (con "caja"): factor sobre el alto del logo nuevo (p. ej. 0.85 cuando el anterior era un
  escudo relleno, más grande a la vista que uno de solo trazos).
- "contorno": [ancho, [r, g, b]]: el logo nuevo lleva un borde de ese color (como un parche bordado),
  para que se lea sobre telas claras.
- "rgb": [r, g, b]: color fijo del logo nuevo (en vez del color del anterior).
- "textura": [x0, y0, x1, y1]: zona de tela limpia de la que se copia el relieve (malla, felpa) sobre lo
  reconstruido, repetida en mosaico, para que no quede una mancha lisa donde estaba el logo anterior.
- "excluir" (con "blanco"): caja dentro de la zona que no se toca (p. ej. la talla bajo la marca).
- "borrar": borra la gráfica que hay dentro de la zona (sin los trazos chicos, p. ej. letras
  vecinas) y no pone nada.
- color "original": se pega con sus colores (blanco ajustado al brillo del render);
  color "tinta": se pinta del color del logo anterior (blanco sobre oscuro, negro sobre claro).

Por cada logo: se borra el anterior reconstruyendo la tela (inpainting) y se pega el oficial a la
misma altura y centrado. Los renders originales no se modifican.
"""

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

UMBRAL = 60  # diferencia de color (suma RGB) para considerar que un píxel no es tela


def color_tela(img, x0, y0, x1, y1):
    zona = img[y0:y1, x0:x1].astype(int)
    borde = np.concatenate([zona[:2].reshape(-1, 3), zona[-2:].reshape(-1, 3),
                            zona[:, :2].reshape(-1, 3), zona[:, -2:].reshape(-1, 3)])
    return np.median(borde, axis=0)


def tinta(img, x0, y0, x1, y1, tela=None):
    """Píxeles (en la caja) que se alejan del color de la tela alrededor."""
    tela = color_tela(img, x0, y0, x1, y1) if tela is None else tela
    dist = np.abs(img[y0:y1, x0:x1].astype(int) - tela).sum(axis=2)
    return dist > UMBRAL, dist


def ubicar(img, zona, rel_min=0.04, incluir_borde=False, tela=None, borde_ok=False):
    """Dentro de una zona holgada: caja ajustada del logo y sus componentes (sin lo que toca el borde)."""
    x0, y0, x1, y1 = zona
    _, dist = tinta(img, x0, y0, x1, y1, tela)
    # umbral relativo al contraste del logo, para no confundir la textura de la tela con el logo
    m = dist > max(UMBRAL, 0.4 * np.percentile(dist, 99.5))
    n, etiquetas, stats, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
    h, w = m.shape
    toca = {i for i in range(1, n) if stats[i, 0] == 0 or stats[i, 1] == 0
            or stats[i, 0] + stats[i, 2] >= w or stats[i, 1] + stats[i, 3] >= h}
    validos = [i for i in range(1, n) if incluir_borde or i not in toca]
    if not validos:
        raise ValueError(f"No se encontró un logo dentro de la zona {zona}")
    mayor = max(stats[i, 4] for i in validos)
    if not (incluir_borde or borde_ok) and any(stats[i, 4] >= 0.25 * mayor for i in toca):
        raise ValueError(f"El logo toca el borde de la zona {zona}: agrandar la zona")
    validos = [i for i in validos if stats[i, 4] >= rel_min * mayor]
    comp = np.isin(etiquetas, validos)
    ys, xs = np.where(comp)
    caja = [x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1]
    mascara = np.zeros(img.shape[:2], np.uint8)
    mascara[y0:y1, x0:x1] = comp.astype(np.uint8) * 255
    return caja, mascara


def ubicar_blanco(img, zona, minimo=140, excluir=None):
    """Logo blanco dentro de una zona, aunque la tela de alrededor tenga franjas de varios colores."""
    x0, y0, x1, y1 = zona
    z = img[y0:y1, x0:x1].astype(int)
    m = (z.min(axis=2) > minimo) & (z.max(axis=2) - z.min(axis=2) < 70)
    if excluir:
        ex0, ey0, ex1, ey1 = excluir
        m[max(ey0 - y0, 0):max(ey1 - y0, 0), max(ex0 - x0, 0):max(ex1 - x0, 0)] = False
    n, etiquetas, stats, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
    validos = [i for i in range(1, n) if stats[i, 4] >= 4]
    if not validos:
        raise ValueError(f"No se encontró un logo blanco dentro de la zona {zona}")
    comp = np.isin(etiquetas, validos)
    ys, xs = np.where(comp)
    caja = [x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1]
    mascara = np.zeros(img.shape[:2], np.uint8)
    mascara[y0:y1, x0:x1] = comp.astype(np.uint8) * 255
    return caja, cv2.dilate(mascara, np.ones((3, 3), np.uint8), iterations=2)  # incluye el borde suavizado


def mascara_caja(img, caja, pad=3, tela=None):
    h, w = img.shape[:2]
    x0, y0, x1, y1 = caja
    X0, Y0, X1, Y1 = max(x0 - pad, 0), max(y0 - pad, 0), min(x1 + pad, w), min(y1 + pad, h)
    m, _ = tinta(img, X0, Y0, X1, Y1, tela)
    mascara = np.zeros((h, w), np.uint8)
    mascara[Y0:Y1, X0:X1] = m.astype(np.uint8) * 255
    recorte = np.zeros_like(mascara)
    recorte[y0:y1, x0:x1] = 255
    return cv2.bitwise_and(mascara, recorte)


def mascara_franjas(img, caja, anillo=12):
    """Logo sobre tela de varios colores: píxeles de la caja lejos de todos los colores de tela vecinos."""
    h, w = img.shape[:2]
    x0, y0, x1, y1 = caja
    X0, Y0, X1, Y1 = max(x0 - anillo, 0), max(y0 - anillo, 0), min(x1 + anillo, w), min(y1 + anillo, h)
    fuera = np.ones((Y1 - Y0, X1 - X0), bool)
    fuera[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = False
    px = img[Y0:Y1, X0:X1][fuera].reshape(-1, 3).astype(np.float32)
    criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1.0)
    _, etiquetas, centros = cv2.kmeans(px, 4, None, criterio, 3, cv2.KMEANS_PP_CENTERS)
    telas = [c for k, c in enumerate(centros) if (etiquetas == k).mean() >= 0.08]
    zona = img[y0:y1, x0:x1].astype(int)
    lejos = np.all([np.abs(zona - t).sum(axis=2) > UMBRAL for t in telas], axis=0)
    mascara = np.zeros((h, w), np.uint8)
    mascara[y0:y1, x0:x1] = lejos.astype(np.uint8) * 255
    return cv2.dilate(mascara, np.ones((3, 3), np.uint8), iterations=1)


def bordes_columna(img, x, ya, yb, centros):
    """Bordes entre colores de tela en una columna: [(y, color_arriba, color_abajo)]."""
    col = img[ya:yb, x].astype(np.float32)
    clase = np.argmin([np.abs(col - c).sum(axis=1) for c in centros], axis=0)
    clase = cv2.medianBlur(clase.astype(np.uint8).reshape(-1, 1), 5).ravel()
    return [(ya + i, int(clase[i - 1]), int(clase[i])) for i in range(1, len(clase)) if clase[i] != clase[i - 1]]


def muestra(img, y, x):
    """Color en una fila no entera (interpolación lineal entre las dos filas vecinas)."""
    y = min(max(y, 0), img.shape[0] - 1.001)
    f = int(y)
    k = y - f
    return (1 - k) * img[f, x].astype(float) + k * img[f + 1, x].astype(float)


def extruir_bordes(destino, img, caja, margen=4, alcance=70):
    """Rellena la caja uniendo los bordes de franjas que se ven en sus dos costados."""
    h, w = img.shape[:2]
    x0, y0, x1, y1 = caja
    xl, xr = max(x0 - margen, 0), min(x1 - 1 + margen, w - 1)
    ya, yb = max(y0 - alcance, 0), min(y1 + alcance, h)
    px = np.concatenate([img[ya:yb, max(xl - 6, 0):xl + 1].reshape(-1, 3), img[ya:yb, xr:xr + 7].reshape(-1, 3)])
    criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1.0)
    _, etq, centros = cv2.kmeans(px.astype(np.float32), 3, None, criterio, 3, cv2.KMEANS_PP_CENTERS)
    bl, br = bordes_columna(img, xl, ya, yb, centros), bordes_columna(img, xr, ya, yb, centros)
    pares, usados = [], set()
    for y, a, b in bl:  # cada borde de la izquierda con el mismo tipo de borde a la derecha
        cand = [(abs(yr - y), i) for i, (yr, ar, br_) in enumerate(br) if (ar, br_) == (a, b) and i not in usados]
        if cand:
            i = min(cand)[1]
            usados.add(i)
            pares.append((y, br[i][0]))
    pares.sort()
    for x in range(x0, x1):
        t = (x - xl) / max(xr - xl, 1)
        bx = [(1 - t) * l + t * r for l, r in pares]
        for y in range(y0, y1):
            k = sum(1 for b in bx if b <= y)  # franja en la que cae y
            if 0 < k < len(pares):
                s_ = (y - bx[k - 1]) / max(bx[k] - bx[k - 1], 1e-6)
                yl = pares[k - 1][0] + s_ * (pares[k][0] - pares[k - 1][0])
                yr = pares[k - 1][1] + s_ * (pares[k][1] - pares[k - 1][1])
            elif k == 0 and pares:
                yl, yr = pares[0][0] + (y - bx[0]), pares[0][1] + (y - bx[0])
            elif pares:
                yl, yr = pares[-1][0] + (y - bx[-1]), pares[-1][1] + (y - bx[-1])
            else:
                yl = yr = y
            destino[y, x] = ((1 - t) * muestra(img, yl, xl) + t * muestra(img, yr, xr)).astype(np.uint8)


def texturizar(destino, img, mascara, fuente, sigma=2.5):
    """Suma a lo reconstruido (bajo la máscara) el relieve fino de una zona de tela limpia, en mosaico."""
    x0, y0, x1, y1 = fuente
    f = img[y0:y1, x0:x1].astype(np.float32)
    detalle = f - cv2.GaussianBlur(f, (0, 0), sigma)
    ys, xs = np.where(mascara > 0)
    if not len(ys):
        return
    base = cv2.GaussianBlur(destino.astype(np.float32), (0, 0), sigma)
    hs, ws = detalle.shape[:2]
    rel = detalle[(ys - ys.min()) % hs, (xs - xs.min()) % ws]
    destino[ys, xs] = np.clip(base[ys, xs] + rel, 0, 255).astype(np.uint8)


def extruir(destino, img, caja, pendiente, margen=4):
    """Rellena la caja continuando franjas diagonales rectas desde sus dos costados (mezcla lineal)."""
    if pendiente == "bordes":
        return extruir_bordes(destino, img, caja, margen)
    lado = None
    if isinstance(pendiente, (list, tuple)):
        pendiente, lado = pendiente
    h, w = img.shape[:2]
    x0, y0, x1, y1 = caja
    xl, xr = max(x0 - margen, 0), min(x1 - 1 + margen, w - 1)
    for x in range(x0, x1):
        t = {"izq": 0.0, "der": 1.0}.get(lado, (x - xl) / max(xr - xl, 1))
        ys = np.arange(y0, y1)
        yl = np.clip(np.round(ys + pendiente * (xl - x)).astype(int), 0, h - 1)
        yr = np.clip(np.round(ys + pendiente * (xr - x)).astype(int), 0, h - 1)
        destino[y0:y1, x] = ((1 - t) * img[yl, xl].astype(float) + t * img[yr, xr].astype(float)).astype(np.uint8)


def color_tinta(img, mascara, tela=None):
    """Color del logo anterior: mediana de sus píxeles más contrastados."""
    ys, xs = np.where(mascara > 0)
    px = img[ys, xs].astype(int)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    if tela is None:
        tela = color_tela(img, max(x0 - 4, 0), max(y0 - 4, 0), x1 + 4, y1 + 4)
    dist = np.abs(px - tela).sum(axis=1)
    fuertes = px[dist >= np.percentile(dist, 60)]
    return np.median(fuertes, axis=0)[::-1]  # BGR -> RGB


def preparar(logo, cfg_logo, ancho, alto, img, mascara, tela=None):
    e = logo.resize((max(int(round(ancho)), 1), max(int(round(alto)), 1)), Image.LANCZOS)
    arr = np.asarray(e).astype(float)
    if cfg_logo.get("color") == "tinta":
        arr[..., :3] = color_tinta(img, mascara, tela)
    else:
        ys, xs = np.where(mascara > 0)
        lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[ys, xs]
        k = min(max((np.percentile(lum, 97) if lum.size else 235) / 255, 0.78), 1.0)
        arr[..., :3] *= k  # el blanco del render rara vez es 255
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def procesar(ruta_img, ops, logos, ruta_salida, ruta_revision=None):
    img = cv2.imread(str(ruta_img))
    total = np.zeros(img.shape[:2], np.uint8)
    pegar, revision, errores = [], img.copy(), []
    for op in ops:
        zona = op.get("borrar") or op.get("zona") or op["caja"]
        tela = np.array(op["tela"][::-1]) if "tela" in op else None  # RGB -> BGR
        try:
            if "borrar" in op:
                caja, m = ubicar(img, op["borrar"], rel_min=op.get("rel_min", 0.1), incluir_borde=True)
                if "extruir" not in op:
                    total = cv2.bitwise_or(total, cv2.dilate(m, np.ones((5, 5), np.uint8)))
            elif "caja" in op:
                caja = op["caja"]
                if op.get("completa"):  # parche bordado de otro tono que la tela: se reconstruye toda la caja
                    m = np.zeros(img.shape[:2], np.uint8)
                    m[caja[1]:caja[3], caja[0]:caja[2]] = 255
                else:
                    m = mascara_franjas(img, caja) if op.get("franjas") else mascara_caja(img, caja, pad=4)
            elif op.get("blanco"):
                caja, m = ubicar_blanco(img, op["zona"], op.get("minimo", 140), op.get("excluir"))
            else:
                caja, comp = ubicar(img, op["zona"], rel_min=op.get("rel_min", 0.04), tela=tela,
                                    borde_ok="tela" in op)
                if tela is not None:  # logo al borde de la prenda: no tocar el fondo vecino
                    m = cv2.dilate(comp, np.ones((3, 3), np.uint8), iterations=1)
                else:
                    # margen para llevarse también sombras y relieve del bordado anterior, sin salir de la zona
                    mg = max(2, round(0.06 * max(caja[2] - caja[0], caja[3] - caja[1])))
                    z = op["zona"]
                    m = mascara_caja(img, [max(caja[0] - mg, z[0]), max(caja[1] - mg, z[1]),
                                           min(caja[2] + mg, z[2]), min(caja[3] + mg, z[3])], pad=0)
        except ValueError as e:
            errores.append(str(e))
            cv2.rectangle(revision, tuple(zona[:2]), tuple(zona[2:4]), (0, 0, 255), 2)
            continue
        cv2.rectangle(revision, tuple(zona[:2]), tuple(zona[2:4]), (255, 160, 0), 1)
        cv2.rectangle(revision, (int(caja[0]), int(caja[1])), (int(caja[2]), int(caja[3])), (0, 255, 0), 1)
        if "borrar" in op:
            if "extruir" in op:
                pegar.append((op, op["borrar"], m, tela))
            continue
        if "extruir" not in op:
            total = cv2.bitwise_or(total, m)
        pegar.append((op, caja, m, tela))
    if ruta_revision:
        ruta_revision.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(ruta_revision), revision)
    total = cv2.dilate(total, np.ones((5, 5), np.uint8), iterations=1)
    limpio = cv2.inpaint(img, total, 5, cv2.INPAINT_TELEA)
    for op, caja, _m, _t in pegar:
        if "extruir" in op:
            extruir(limpio, img, op.get("caja") or op["borrar"], op["extruir"])
    for op, _c, m, _t in pegar:
        if "textura" in op:
            texturizar(limpio, img, cv2.dilate(m, np.ones((9, 9), np.uint8)) & total, op["textura"])

    lienzo = Image.fromarray(cv2.cvtColor(limpio, cv2.COLOR_BGR2RGB)).convert("RGBA")
    for op, caja, m, tela in pegar:
        if "borrar" in op:
            continue
        nombre = op["logo"]
        logo, cfg_logo = logos[nombre]
        x0, y0, x1, y1 = op.get("pegar_en", caja)[:4]
        bw, bh = x1 - x0, y1 - y0
        if op.get("por_ancho"):  # escudo con cinta más ancha que el cuerpo: cubrir la anterior
            ancho = bw * 1.03
            alto = ancho * logo.height / logo.width
        elif "caja" in op:  # escudos marcados a mano: misma altura que el anterior
            alto = bh * 1.04 * op.get("escala", 1.0)
            ancho = alto * logo.width / logo.height * op.get("angosto", 1.0)
        elif cfg_logo.get("ajuste") == "contener":  # logos con texto: que quepan en la caja
            s = min(bw / logo.width, bh * cfg_logo.get("alto_max", 1.0) / logo.height)
            ancho, alto = logo.width * s, logo.height * s
        elif op.get("lateral"):  # vista de costado: mismo alto y ancho que el anterior
            alto = bh
            ancho = bw if op["lateral"] is True else alto * logo.width / logo.height * op["lateral"]
        else:  # misma superficie que el anterior, con las proporciones del logo oficial
            proporcion = logo.width / logo.height
            ancho = (bw * bh * proporcion) ** 0.5
            alto = ancho / proporcion
        e = preparar(logo, cfg_logo, ancho, alto, img, m, tela)
        if "rgb" in op:  # color fijo para el logo nuevo
            arr = np.asarray(e).copy()
            arr[..., :3] = op["rgb"]
            e = Image.fromarray(arr, "RGBA")
        if "contorno" in op:  # borde de color alrededor del logo (parche bordado)
            grosor, rgb = op["contorno"]
            a = ((np.asarray(e)[..., 3] > 40) * 255).astype(np.uint8)  # puntas finas: borde cerrado
            pad = grosor + 1
            base = Image.new("RGBA", (e.width + 2 * pad, e.height + 2 * pad), (0, 0, 0, 0))
            capa = np.zeros((base.height, base.width, 4), np.uint8)
            capa[..., :3] = rgb
            b = np.zeros((base.height, base.width), np.uint8)
            b[pad:pad + e.height, pad:pad + e.width] = a
            capa[..., 3] = cv2.GaussianBlur(cv2.dilate(b, cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (2 * grosor + 1, 2 * grosor + 1))), (3, 3), 0)
            base = Image.fromarray(capa, "RGBA")
            base.alpha_composite(e, (pad, pad))
            e = base
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        lienzo.alpha_composite(e, (int(round(cx - e.width / 2)), int(round(cy - e.height / 2))))
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    lienzo.convert("RGB").save(ruta_salida, "JPEG", quality=93)
    return errores


def main(cfg_path, solo=None, revision=None):
    cfg_path = Path(cfg_path).resolve()
    d = cfg_path.parent
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    logos = {k: (Image.open(d / v["archivo"]).convert("RGBA"), v) for k, v in cfg["logos"].items()}
    fallas = 0
    for rel, ops in cfg["renders"].items():
        if solo and solo not in rel:
            continue
        salida = d / cfg["salida"] / Path(rel).name
        rev = Path(revision) / Path(rel).name if revision else None
        errores = procesar(d / rel, ops, logos, salida, rev)
        fallas += len(errores)
        print(f"{'OK ' if not errores else 'REV'} {salida.relative_to(d)}  ({len(ops) - len(errores)}/{len(ops)} cambios)")
        for e in errores:
            print("     ", e)
    if fallas:
        sys.exit(f"{fallas} zonas sin logo: revisar las coordenadas")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--solo", help="procesar solo los renders cuyo nombre contenga este texto")
    ap.add_argument("--revision", help="carpeta donde dejar imágenes con las zonas (azul) y logos ubicados (verde)")
    a = ap.parse_args()
    main(a.config, a.solo, a.revision)
