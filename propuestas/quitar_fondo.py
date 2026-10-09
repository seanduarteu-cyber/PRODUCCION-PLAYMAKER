"""Cambia el fondo gris de estudio de los montajes por el color marfil de la propuesta.

Uso:
    python3 propuestas/quitar_fondo.py propuestas/gauchos-rc-2027/fondo.json

fondo.json:
    {"color": [250, 249, 245], "entrada": "img/con_logos", "salida": "img/montaje_final",
     "cache_mascaras": "/tmp/mascaras"}

Se mantiene todo lo que no es fondo: prendas (recortadas con el modelo BiRefNet), textos y
etiquetas del montaje, recuadros de detalle y la franja negra del encabezado. El borde de cada
prenda se descontamina del gris antes de mezclarlo con el marfil, para que no quede halo.

Requiere onnxruntime y el modelo BiRefNet-general en ~/.rembg/models/birefnet-general/
(se descarga solo con: python3 -c "from rembg import new_session; new_session('birefnet-general')").
"""

import json
import sys
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image

MODELO = Path.home() / ".rembg/models/birefnet-general/birefnet-general.onnx"


# ---------------------------------------------------------------- prendas (BiRefNet)

def sesion():
    so = ort.SessionOptions()  # modo de bajo consumo: el modelo pide ~14 GB con las opciones por defecto
    so.enable_cpu_mem_arena = False
    so.enable_mem_pattern = False
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_BASIC
    return ort.InferenceSession(str(MODELO), so, providers=["CPUExecutionProvider"])


def mascara_prendas(ses, pil):
    im = pil.convert("RGB").resize((1024, 1024), Image.BICUBIC)
    x = (np.asarray(im).astype(np.float32) / 255 - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    out = ses.run(None, {ses.get_inputs()[0].name: x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
    m = Image.fromarray((255 / (1 + np.exp(-out))).astype(np.uint8)).resize(pil.size, Image.BILINEAR)
    return np.asarray(m).astype(float) / 255


# ---------------------------------------------------------------- resto del montaje

def fondo_estimado(img, lum, prendas):
    """Gris de estudio (degradado suave) estimado a partir de lo que no es prenda."""
    fuera = ((prendas < 0.1) & (lum > 140)).astype(np.uint8)
    fuera = cv2.erode(fuera, np.ones((9, 9), np.uint8)).astype(float)
    fondo = None
    for k in (61, 151, 401):  # de más local a más global, para rellenar huecos
        num = cv2.blur(img * fuera[..., None], (k, k))
        den = cv2.blur(fuera, (k, k))[..., None]
        est = num / np.maximum(den, 1e-6)
        fondo = np.where(den > 0.05, est, np.nan) if fondo is None else np.where(np.isnan(fondo) & (den > 0.01), est, fondo)
    return np.where(np.isnan(fondo), img, fondo)


def textos(img, lum, fondo):
    """Textos y etiquetas: mucho contraste con el fondo, o contraste medio con borde nítido."""
    dist = np.abs(img - fondo).max(axis=2)
    paso_alto = np.abs(lum - cv2.GaussianBlur(lum, (0, 0), 2.0))
    nitido = cv2.dilate((paso_alto > 10).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(float)
    return np.maximum(np.clip((dist - 70) / 40, 0, 1), np.clip((dist - 32) / 30, 0, 1) * nitido)


def recuadros(img_u8):
    """Fotos rectangulares de detalle dentro del montaje."""
    bordes = cv2.Canny(cv2.GaussianBlur(img_u8, (3, 3), 0), 30, 90)
    bordes = cv2.dilate(bordes, np.ones((3, 3), np.uint8))
    cnts, _ = cv2.findContours(bordes, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    h, w = img_u8.shape[:2]
    rects = []
    for c in cnts:
        x, y, cw, ch = cv2.boundingRect(c)
        if cw < 90 or ch < 70 or cw > 0.5 * w or ch > 0.5 * h:
            continue
        ap = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
        if len(ap) == 4 and cv2.contourArea(ap) > 0.85 * cw * ch:
            rects.append((x, y, x + cw, y + ch))
    return [r for r in rects if not any(o != r and o[0] <= r[0] and o[1] <= r[1] and o[2] >= r[2] and o[3] >= r[3]
                                        for o in rects)]


def procesar(img_u8, prendas, color):
    img = img_u8.astype(float)
    lum = cv2.cvtColor(img_u8, cv2.COLOR_RGB2GRAY).astype(float)
    fondo = fondo_estimado(img, lum, prendas)
    alfa = np.maximum(prendas, textos(img, lum, fondo))
    for x0, y0, x1, y1 in recuadros(img_u8):
        alfa[y0:y1, x0:x1] = 1
    fin = 0  # franja negra del encabezado
    while fin < img.shape[0] and np.median(lum[fin]) < 70:
        fin += 1
    alfa[:fin] = 1
    # descontaminar el borde: quitar la parte de gris que trae cada píxel semitransparente
    a = alfa[..., None]
    frente = np.where(a > 0.05, (img - (1 - a) * fondo) / np.maximum(a, 0.05), img).clip(0, 255)
    return (frente * a + np.array(color, float) * (1 - a)).clip(0, 255).astype(np.uint8)


def main(cfg_path, solo=None):
    cfg_path = Path(cfg_path).resolve()
    d = cfg_path.parent
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    entrada, salida = d / cfg["entrada"], d / cfg["salida"]
    cache = Path(cfg.get("cache_mascaras", salida / "_mascaras"))
    cache.mkdir(parents=True, exist_ok=True)
    salida.mkdir(parents=True, exist_ok=True)
    ses = None
    for ruta in sorted(entrada.glob("*.jpg")):
        if solo and solo not in ruta.name:
            continue
        pil = Image.open(ruta).convert("RGB")
        ruta_m = cache / ruta.with_suffix(".png").name
        if ruta_m.exists() and ruta_m.stat().st_mtime >= ruta.stat().st_mtime:
            prendas = np.asarray(Image.open(ruta_m)).astype(float) / 255
        else:
            ses = ses or sesion()
            prendas = mascara_prendas(ses, pil)
            Image.fromarray((prendas * 255).astype(np.uint8)).save(ruta_m)
        Image.fromarray(procesar(np.asarray(pil), prendas, cfg.get("color", [250, 249, 245]))).save(
            salida / ruta.name, quality=93, subsampling=0)
        print(f"OK  {(salida / ruta.name).relative_to(d)}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
