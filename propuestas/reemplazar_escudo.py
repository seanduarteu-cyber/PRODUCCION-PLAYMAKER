"""Reemplaza el escudo aproximado de los renders por el escudo oficial del club.

Uso:
    python3 propuestas/reemplazar_escudo.py propuestas/gauchos-rc-2027/escudos.json

escudos.json indica, por render, las cajas (x0, y0, x1, y1 en píxeles) donde aparece el escudo:
    {"escudo": "img/escudo_gauchos.png", "salida": "img/con_escudo",
     "renders": {"img/01_player_tee_home_op1.jpg": [[425, 350, 492, 447], ...]}}
Una caja puede llevar un quinto valor (0-1) para angostar el escudo en vistas laterales.

Por cada caja: borra el escudo anterior (inpainting sobre la tela), y pega el oficial a la
misma altura, centrado, con el blanco ajustado al brillo del render. Los originales no se tocan.
"""

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def mascara_escudo(img, x0, y0, x1, y1, pad=4):
    """Píxeles del escudo anterior: los que se alejan del color de la tela alrededor."""
    h, w = img.shape[:2]
    X0, Y0, X1, Y1 = max(x0 - pad, 0), max(y0 - pad, 0), min(x1 + pad, w), min(y1 + pad, h)
    zona = img[Y0:Y1, X0:X1].astype(int)
    borde = np.concatenate([zona[:2].reshape(-1, 3), zona[-2:].reshape(-1, 3),
                            zona[:, :2].reshape(-1, 3), zona[:, -2:].reshape(-1, 3)])
    tela = np.median(borde, axis=0)
    dist = np.abs(zona - tela).sum(axis=2)
    m = np.zeros((h, w), np.uint8)
    m[Y0:Y1, X0:X1] = (dist > 60).astype(np.uint8) * 255
    recorte = np.zeros_like(m)
    recorte[y0:y1, x0:x1] = 255  # solo dentro de la caja
    m = cv2.bitwise_and(m, recorte)
    return cv2.dilate(m, np.ones((5, 5), np.uint8), iterations=1)


def reemplazar(ruta_img, cajas, escudo, ruta_salida):
    img = cv2.imread(str(ruta_img))
    brillos = []
    mascara = np.zeros(img.shape[:2], np.uint8)
    for caja in cajas:
        x0, y0, x1, y1 = caja[:4]
        m = mascara_escudo(img, x0, y0, x1, y1)
        lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[m > 0]
        brillos.append(np.percentile(lum, 97) if lum.size else 235)
        mascara = cv2.bitwise_or(mascara, m)
    limpio = cv2.inpaint(img, mascara, 5, cv2.INPAINT_TELEA)

    lienzo = Image.fromarray(cv2.cvtColor(limpio, cv2.COLOR_BGR2RGB)).convert("RGBA")
    for caja, brillo in zip(cajas, brillos):
        x0, y0, x1, y1 = caja[:4]
        angosto = caja[4] if len(caja) > 4 else 1.0
        alto = (y1 - y0) * 1.04
        ancho = alto * escudo.width / escudo.height * angosto
        e = escudo.resize((max(int(round(ancho)), 1), max(int(round(alto)), 1)), Image.LANCZOS)
        k = min(max(brillo / 255, 0.78), 1.0)  # el blanco del render rara vez es 255
        rgb = (np.asarray(e)[..., :3].astype(float) * k).astype(np.uint8)
        e = Image.fromarray(np.dstack([rgb, np.asarray(e)[..., 3]]), "RGBA")
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        lienzo.alpha_composite(e, (int(round(cx - e.width / 2)), int(round(cy - e.height / 2))))
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    lienzo.convert("RGB").save(ruta_salida, "JPEG", quality=93)


def main(cfg_path):
    cfg_path = Path(cfg_path).resolve()
    d = cfg_path.parent
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    escudo = Image.open(d / cfg["escudo"]).convert("RGBA")
    for rel, cajas in cfg["renders"].items():
        salida = d / cfg["salida"] / Path(rel).name
        reemplazar(d / rel, cajas, escudo, salida)
        print(f"OK  {salida.relative_to(d)}  ({len(cajas)} escudos)")


if __name__ == "__main__":
    main(sys.argv[1])
