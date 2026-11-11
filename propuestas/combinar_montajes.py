"""Junta montajes de una misma prenda (p. ej. corte hombre y corte mujer) en una sola imagen para la ficha.

Uso:
    python3 propuestas/combinar_montajes.py propuestas/old-green-rc-2027/combinados.json

combinados.json (rutas relativas al JSON):
    {"aspecto": 1.93, "color": [250, 249, 245],
     "combinados": {"img/montaje_final/01_camiseta_local.jpg": [
         ["img/montaje_final/01_camiseta_local_hombre.jpg", "HOMBRE"],
         ["img/montaje_final/01_camiseta_local_mujer.jpg", "MUJER"]]}}

Cada montaje se recorta a sus prendas, se ponen en fila a la misma altura con su rótulo debajo y la
imagen queda con las proporciones del espacio del render en la ficha (aspecto = ancho / alto).
Con muchas piezas (p. ej. cinco colores de una polera), en vez de la lista va
{"columnas": 3, "piezas": [...]} y se arman varias filas.
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ANCHO = 3000
FUENTE = Path(__file__).parent / "_recursos" / "fonts" / "Poppins-SemiBold.ttf"
GRIS = (110, 114, 128)


def recortar(img, color, margen=12):
    a = np.asarray(img).astype(int)
    ys, xs = np.where(np.abs(a - color).sum(axis=2) > 30)
    return img.crop((max(xs.min() - margen, 0), max(ys.min() - margen, 0),
                     min(xs.max() + margen, img.width), min(ys.max() + margen, img.height)))


def rotulo(draw, texto, cx, y, fuente, espaciado):
    anchos = [draw.textlength(c, font=fuente) for c in texto]
    x = cx - (sum(anchos) + espaciado * (len(texto) - 1)) / 2
    for c, a in zip(texto, anchos):
        draw.text((x, y), c, font=fuente, fill=GRIS)
        x += a + espaciado


def combinar(piezas, aspecto, color, columnas=None):
    alto_total = round(ANCHO / aspecto)
    margen, separacion = 70, 150
    alto_rotulo = 110
    recortes = [(recortar(im, color), texto) for im, texto in piezas]
    columnas = columnas or len(recortes)
    filas = [recortes[i:i + columnas] for i in range(0, len(recortes), columnas)]
    # misma altura para todas las piezas, lo más grandes que quepan en ancho y en alto
    alto = min(min((ANCHO - 2 * margen - separacion * (len(f) - 1)) / sum(r.width / r.height for r, _ in f)
                   for f in filas),
               (alto_total - 2 * margen - separacion / 2 * (len(filas) - 1)) / len(filas) - alto_rotulo)
    lienzo = Image.new("RGB", (ANCHO, alto_total), tuple(color))
    draw = ImageDraw.Draw(lienzo)
    fuente = ImageFont.truetype(str(FUENTE), 34)
    alto_fila = alto + alto_rotulo + separacion / 2
    y = (alto_total - len(filas) * alto_fila + separacion / 2) / 2
    for fila in filas:
        anchos = [r.width * alto / r.height for r, _ in fila]
        x = (ANCHO - sum(anchos) - separacion * (len(fila) - 1)) / 2
        for (r, texto), w in zip(fila, anchos):
            lienzo.paste(r.resize((round(w), round(alto)), Image.LANCZOS), (round(x), round(y)))
            rotulo(draw, texto, x + w / 2, y + alto + 55, fuente, 9)
            x += w + separacion
        y += alto_fila
    return lienzo


def main(cfg_path):
    cfg_path = Path(cfg_path).resolve()
    d = cfg_path.parent
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    color = cfg.get("color", [250, 249, 245])
    for salida, piezas in cfg["combinados"].items():
        columnas = None
        if isinstance(piezas, dict):
            columnas, piezas = piezas.get("columnas"), piezas["piezas"]
        imgs = [(Image.open(d / ruta).convert("RGB"), texto) for ruta, texto in piezas]
        combinar(imgs, cfg["aspecto"], color, columnas).save(d / salida, quality=93, subsampling=0)
        print(f"OK  {salida}  ({len(piezas)} montajes)")


if __name__ == "__main__":
    main(sys.argv[1])
