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
                total = cv2.bitwise_or(total, cv2.dilate(m, np.ones((5, 5), np.uint8)))
            elif "caja" in op:
                caja = op["caja"]
                m = mascara_caja(img, caja, pad=4)
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
            continue
        total = cv2.bitwise_or(total, m)
        pegar.append((op, caja, m, tela))
    if ruta_revision:
        ruta_revision.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(ruta_revision), revision)
    total = cv2.dilate(total, np.ones((5, 5), np.uint8), iterations=1)
    limpio = cv2.inpaint(img, total, 5, cv2.INPAINT_TELEA)

    lienzo = Image.fromarray(cv2.cvtColor(limpio, cv2.COLOR_BGR2RGB)).convert("RGBA")
    for op, caja, m, tela in pegar:
        nombre = op["logo"]
        logo, cfg_logo = logos[nombre]
        x0, y0, x1, y1 = op.get("pegar_en", caja)[:4]
        bw, bh = x1 - x0, y1 - y0
        if "caja" in op:  # escudos marcados a mano: misma altura que el anterior
            alto = bh * 1.04
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
