"""Monta renders y campos de valor editables sobre una propuesta comercial base.

Uso:
    python3 propuestas/montar_propuesta.py propuestas/gauchos-rc-2027/propuesta.json

La propuesta base (PDF) trae en cada ficha un "ESPACIO RESERVADO PARA RENDER" y
los valores como marcadores "$[00.000]" / "[00]". Este script:
  1. Pone cada render del JSON en el espacio reservado de su ficha (GAU-XX).
  2. Reemplaza los marcadores por campos de formulario editables:
     - Valor unitario: un solo campo por producto, visible en su ficha y en el
       cuadro de valores (se escribe una vez y aparece en ambos lugares).
     - Cantidad por producto en el cuadro de valores.
     - Subtotal neto, IVA y total, calculados solos en Acrobat / Chrome / Edge /
       Firefox (Vista Previa de macOS no ejecuta cálculos: ahí se escriben a mano).
  3. Si el JSON trae "precios", los deja escritos en los campos (siguen editables).
     Con "precios_con_iva": true, los precios incluyen IVA: el total con IVA es la suma de
     cantidad × precio, y el subtotal neto y el IVA se calculan desde ese total.
"""

import io
import json
import re
import sys
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium
from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import (ArrayObject, BooleanObject, DecodedStreamObject, DictionaryObject,
                           FloatObject, NameObject, NumberObject, TextStringObject)
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

RECURSOS = Path(__file__).parent / "_recursos"
FUENTES = {  # nombre en el PDF -> archivo (las mismas familias que usa la propuesta base)
    "PopR": "Poppins-Regular.ttf",
    "PopSB": "Poppins-SemiBold.ttf",
    "PfdB": "PlayfairDisplay-Bold.ttf",
}
NAVY = "0.078 0.118 0.235 rg"
GRIS_OSCURO = "0.227 0.247 0.322 rg"
CREMA = "0.969 0.953 0.906 rg"
FONDO_RENDER = (0.980392, 0.976471, 0.960784)
PADDING_RENDER = 7  # pt entre el render y el borde del espacio reservado

FMT_PESOS = 'AFNumber_Format(0, 2, 0, 0, "$", true);'
KEY_PESOS = 'AFNumber_Keystroke(0, 2, 0, 0, "$", true);'
FMT_NUM = 'AFNumber_Format(0, 2, 0, 0, "", true);'
KEY_NUM = 'AFNumber_Keystroke(0, 2, 0, 0, "", true);'
# Lee un campo como número aunque venga escrito a mano como "$12.990" (p. ej. desde Vista Previa).
JS_NUM = ('var d = this;'
          'function n(name) { var f = d.getField(name); if (!f) return 0;'
          ' var v = String(f.value).replace(/[^0-9,\\-]/g, "").replace(",", ".");'
          ' return v === "" ? 0 : (Number(v) || 0); }')


# ---------------------------------------------------------------- lectura de la base

def _bbox(w):
    return (w["x0"], w["top"], w["x1"], w["bottom"])


def analizar_base(ruta):
    """Ubica espacios de render y marcadores de valor en cada página de la base."""
    fichas, cuadro = {}, None
    with pdfplumber.open(ruta) as pdf:
        for i, page in enumerate(pdf.pages):
            words = page.extract_words(extra_attrs=["size"])
            texts = [w["text"] for w in words]
            if "ESPACIO" in texts and "RESERVADO" in texts:
                code = next(w["text"] for w in words if re.fullmatch(r"GAU-\d+", w["text"]) and w["top"] < 100)
                box = next(r for r in page.rects if r["fill"] and r["width"] > 300 and r["height"] > 150
                           and tuple(round(c, 3) for c in r["non_stroking_color"]) == tuple(round(c, 3) for c in FONDO_RENDER))
                valor = next(w for w in words if w["text"] == "$[00.000]")
                fichas[code] = {"page": i, "box": (box["x0"], box["top"], box["x1"], box["bottom"]),
                                "valor": _bbox(valor), "size": valor["size"]}
            elif "CANTIDAD" in texts and texts.count("[00]") > 1:
                filas = {}
                for w in words:
                    if re.fullmatch(r"GAU-\d+", w["text"]):
                        mismas = [o for o in words if abs(o["top"] - w["top"]) < 2]
                        cant = next(o for o in mismas if o["text"] == "[00]")
                        valor = next(o for o in mismas if o["text"] == "$[00.000]")
                        filas[w["text"]] = {"cant": _bbox(cant), "valor": _bbox(valor), "size": valor["size"]}
                totales = {}
                for w in words:
                    if w["text"] != "$[00.000]" or any(abs(w["top"] - f["valor"][1]) < 2 for f in filas.values()):
                        continue
                    linea = " ".join(o["text"] for o in words if abs(o["top"] - w["top"]) < 6 and o["x1"] < w["x0"])
                    clave = "total" if "TOTAL" in linea else "iva" if "IVA" in linea else "subtotal"
                    totales[clave] = {"bbox": _bbox(w), "size": w["size"]}
                cuadro = {"page": i, "filas": filas, "totales": totales}
    return fichas, cuadro


def analizar_portada(ruta):
    """Emblema de la portada (recuadro blanco central) y color de fondo de la página."""
    with pdfplumber.open(ruta) as pdf:
        page = pdf.pages[0]
        fondo = next(r for r in page.rects if r["fill"] and r["width"] > page.width - 1)
        emblema = next(r for r in page.rects if r["fill"] and 100 < r["width"] < 300 and 100 < r["height"] < 300)
        return {"fondo": tuple(fondo["non_stroking_color"]),
                "emblema": (emblema["x0"], emblema["top"], emblema["x1"], emblema["bottom"])}


def parche(bitmap, escala, bbox):
    """Color de fondo y rect (coordenadas pdfplumber) que tapa por completo un marcador.

    El fondo se toma a los lados del marcador (misma fila de la tabla); el alto se ajusta a
    la tinta real, porque los corchetes sobresalen de la caja tipográfica.
    """
    x0, top, x1, bottom = bbox
    m = 4.5
    px = [bitmap.getpixel((int(x * escala), int(y * escala)))
          for x in (x0 - m, x1 + m) for y in (top + 1, (top + bottom) / 2, bottom - 1)]
    fondo = tuple(sorted(c)[len(c) // 2] for c in list(zip(*px))[:3])
    lum = lambda p: 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]
    filas = [y for y in range(int((top - 4) * escala), int((bottom + 2) * escala))
             if any(abs(lum(bitmap.getpixel((x, y))) - lum(fondo)) > 40
                    for x in range(int(x0 * escala), int(x1 * escala), 1))]
    arriba = min([top] + [y / escala - 0.8 for y in filas])
    abajo = max([bottom] + [(y + 1) / escala + 0.8 for y in filas])
    return tuple(c / 255 for c in fondo), (x0 - 1.5, arriba, x1 + 1.5, abajo)


# ---------------------------------------------------------------- capa visual (reportlab)

def construir_capa(base_path, cfg_dir, cfg, fichas, cuadro, portada, n_paginas, w, h):
    """Una página de superposición por página de la base: renders + parches sobre marcadores."""
    doc = pdfium.PdfDocument(base_path)
    escala = 3
    parches = {}  # page -> [(bbox, color)]
    for code, f in fichas.items():
        parches.setdefault(f["page"], []).append(f["valor"])
    if cuadro:
        for fila in cuadro["filas"].values():
            parches.setdefault(cuadro["page"], []).extend([fila["cant"], fila["valor"]])
        parches[cuadro["page"]].extend(t["bbox"] for t in cuadro["totales"].values())

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    renders_por_pagina = {fichas[code]["page"]: (code, r) for code, r in cfg["renders"].items() if code in fichas}
    for i in range(n_paginas):
        if i == 0 and portada:
            # tapa el emblema genérico; el escudo vectorial se monta después en main()
            x0, top, x1, bottom = portada["emblema"]
            c.setFillColorRGB(*portada["fondo"])
            c.rect(x0 - 1, h - bottom - 1, x1 - x0 + 2, bottom - top + 2, stroke=0, fill=1)
        if i in parches:
            bmp = doc[i].render(scale=escala).to_pil().convert("RGB")
            for bbox in parches[i]:
                fondo, (x0, top, x1, bottom) = parche(bmp, escala, bbox)
                c.setFillColorRGB(*fondo)
                c.rect(x0, h - bottom, x1 - x0, bottom - top, stroke=0, fill=1)
        if i in renders_por_pagina:
            code, r = renders_por_pagina[i]
            x0, top, x1, bottom = fichas[code]["box"]
            # tapa el texto "ESPACIO RESERVADO" e isotipo, dejando el borde de la caja
            c.setFillColorRGB(*FONDO_RENDER)
            c.rect(x0 + 1, h - bottom + 1, x1 - x0 - 2, bottom - top - 2, stroke=0, fill=1)
            img = Image.open(cfg_dir / r["imagen"])
            if "recorte" in r:
                img = img.crop(tuple(r["recorte"]))
            bw, bh = x1 - x0 - 2 * PADDING_RENDER, bottom - top - 2 * PADDING_RENDER
            s = min(bw / img.width, bh / img.height)
            iw, ih = img.width * s, img.height * s
            ix, iy = x0 + (x1 - x0 - iw) / 2, h - bottom + (bottom - top - ih) / 2
            if "recorte" in r:
                tmp = io.BytesIO()
                img.convert("RGB").save(tmp, "JPEG", quality=92)
                tmp.seek(0)
                c.drawImage(ImageReader(tmp), ix, iy, iw, ih)
            else:
                c.drawImage(str(cfg_dir / r["imagen"]), ix, iy, iw, ih)  # JPEG embebido tal cual
        c.showPage()
    c.save()
    buf.seek(0)
    return PdfReader(buf)


# ---------------------------------------------------------------- formulario (pypdf)

def fuente_truetype(writer, archivo, nombre):
    """Incrusta una TrueType (subconjunto Windows-1252) usable por los campos de formulario."""
    font = TTFont(RECURSOS / "fonts" / archivo)
    codigos = {}
    for b in range(32, 256):
        try:
            codigos[b] = bytes([b]).decode("cp1252")
        except UnicodeDecodeError:
            pass
    opts = subset.Options()
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    opts.layout_features = []
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=[ord(ch) for ch in codigos.values()])
    sub.subset(font)
    data = io.BytesIO()
    font.save(data)
    data = data.getvalue()

    upm = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    widths = [NumberObject(round(hmtx[cmap[ord(codigos[b])]][0] * 1000 / upm)) if b in codigos and ord(codigos[b]) in cmap
              else NumberObject(0) for b in range(32, 256)]
    head, os2 = font["head"], font["OS/2"]
    k = 1000 / upm

    ff = DecodedStreamObject()
    ff.set_data(data)
    ff[NameObject("/Length1")] = NumberObject(len(data))
    ff = ff.flate_encode()
    desc = DictionaryObject({
        NameObject("/Type"): NameObject("/FontDescriptor"),
        NameObject("/FontName"): NameObject("/" + nombre),
        NameObject("/Flags"): NumberObject(32),
        NameObject("/FontBBox"): ArrayObject([NumberObject(round(v * k)) for v in
                                              (head.xMin, head.yMin, head.xMax, head.yMax)]),
        NameObject("/ItalicAngle"): NumberObject(0),
        NameObject("/Ascent"): NumberObject(round(os2.sTypoAscender * k)),
        NameObject("/Descent"): NumberObject(round(os2.sTypoDescender * k)),
        NameObject("/CapHeight"): NumberObject(round(getattr(os2, "sCapHeight", os2.sTypoAscender) * k)),
        NameObject("/StemV"): NumberObject(80),
        NameObject("/FontFile2"): writer._add_object(ff),
    })
    return writer._add_object(DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/TrueType"),
        NameObject("/BaseFont"): NameObject("/" + nombre),
        NameObject("/FirstChar"): NumberObject(32),
        NameObject("/LastChar"): NumberObject(255),
        NameObject("/Widths"): ArrayObject(widths),
        NameObject("/Encoding"): NameObject("/WinAnsiEncoding"),
        NameObject("/FontDescriptor"): writer._add_object(desc),
    }))


def js(code):
    return DictionaryObject({NameObject("/S"): NameObject("/JavaScript"), NameObject("/JS"): TextStringObject(code)})


def acciones(formato=None, tecla=None, calculo=None):
    aa = DictionaryObject()
    if tecla:
        aa[NameObject("/K")] = js(tecla)
    if formato:
        aa[NameObject("/F")] = js(formato)
    if calculo:
        aa[NameObject("/C")] = js(calculo)
    return aa


def rect_campo(bbox, h, izquierda, derecha_extra=2.0, alto=None):
    """Rect PDF para un campo alineado a la derecha donde estaba el marcador."""
    x0, top, x1, bottom = bbox
    alto = alto or (bottom - top) + 6
    centro = h - (top + bottom) / 2
    return ArrayObject([FloatObject(round(v, 2)) for v in
                        (izquierda, centro - alto / 2, x1 + derecha_extra, centro + alto / 2)])


def widget(writer, page, rect, da, padre=None):
    d = DictionaryObject({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Widget"),
        NameObject("/Rect"): rect,
        NameObject("/P"): page.indirect_reference,
        NameObject("/F"): NumberObject(4),
        NameObject("/DA"): TextStringObject(da),
        NameObject("/Q"): NumberObject(2),
        NameObject("/MK"): DictionaryObject(),
    })
    if padre is not None:
        d[NameObject("/Parent")] = padre
    ref = writer._add_object(d)
    page.setdefault(NameObject("/Annots"), ArrayObject()).append(ref)
    return ref


def ancho_texto(archivo, texto, size, _cache={}):
    if archivo not in _cache:
        f = TTFont(RECURSOS / "fonts" / archivo)
        _cache[archivo] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    cmap, hmtx, upm = _cache[archivo]
    return sum(hmtx[cmap[ord(ch)]][0] for ch in texto) * size / upm


def pesos(valor):
    return "$" + f"{int(valor):,}".replace(",", ".")


def apariencia(writer, rect, texto, fuente, fuente_ref, size, color):
    """Apariencia de un campo con su texto ya formateado, alineado a la derecha como el campo (Q=2)."""
    ancho = float(rect[2]) - float(rect[0])
    alto = float(rect[3]) - float(rect[1])
    x = ancho - 2 - ancho_texto(FUENTES[fuente], texto, size)
    y = (alto - 0.7 * size) / 2
    st = DecodedStreamObject()
    st.set_data((f"/Tx BMC q BT /{fuente} {size:.1f} Tf {color} {x:.2f} {y:.2f} Td ({texto}) Tj ET Q EMC").encode("latin-1"))
    st.update({
        NameObject("/Type"): NameObject("/XObject"),
        NameObject("/Subtype"): NameObject("/Form"),
        NameObject("/BBox"): ArrayObject([FloatObject(0), FloatObject(0), FloatObject(round(ancho, 2)),
                                          FloatObject(round(alto, 2))]),
        NameObject("/Resources"): DictionaryObject({NameObject("/Font"): DictionaryObject(
            {NameObject("/" + fuente): fuente_ref})}),
    })
    return DictionaryObject({NameObject("/N"): writer._add_object(st)})


def campo(writer, nombre, ayuda, aa, valor=""):
    return DictionaryObject({
        NameObject("/FT"): NameObject("/Tx"),
        NameObject("/T"): TextStringObject(nombre),
        NameObject("/TU"): TextStringObject(ayuda),
        NameObject("/V"): TextStringObject(valor),
        NameObject("/Q"): NumberObject(2),
        NameObject("/AA"): aa,
    })


def campo_simple(writer, page, nombre, ayuda, rect, da, aa):
    d = campo(writer, nombre, ayuda, aa)
    d.update({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Widget"),
        NameObject("/Rect"): rect,
        NameObject("/P"): page.indirect_reference,
        NameObject("/F"): NumberObject(4),
        NameObject("/DA"): TextStringObject(da),
        NameObject("/MK"): DictionaryObject(),
    })
    ref = writer._add_object(d)
    page.setdefault(NameObject("/Annots"), ArrayObject()).append(ref)
    return ref


def agregar_formulario(writer, fichas, cuadro, iva, h, fuentes, precios=None, con_iva=False):
    campos, orden_calculo = ArrayObject(), ArrayObject()
    codigos = sorted(set(fichas) | set(cuadro["filas"] if cuadro else []))
    precios = precios or {}
    ayuda_valor = "Precio socio {} (CLP, IVA incluido)" if con_iva else "Valor unitario {} (CLP, neto)"

    for code in codigos:
        # valor unitario: un campo, un widget por cada página donde aparece
        precio = precios.get(code)
        padre = writer._add_object(campo(writer, f"valor_{code}", ayuda_valor.format(code),
                                         acciones(FMT_PESOS, KEY_PESOS), "" if precio is None else str(precio)))
        kids = ArrayObject()
        lugares = []
        if code in fichas:
            f = fichas[code]
            lugares.append((writer.pages[f["page"]], rect_campo(f["valor"], h, f["valor"][0] - 30), f["size"]))
        if cuadro and code in cuadro["filas"]:
            f = cuadro["filas"][code]
            lugares.append((writer.pages[cuadro["page"]], rect_campo(f["valor"], h, f["valor"][0] - 34), f["size"]))
        for page, rect, size in lugares:
            ref = widget(writer, page, rect, f"/PopSB {size:.1f} Tf {NAVY}", padre)
            if precio is not None:
                ref.get_object()[NameObject("/AP")] = apariencia(writer, rect, pesos(precio), "PopSB",
                                                                 fuentes["/PopSB"], size, NAVY)
            kids.append(ref)
        padre.get_object()[NameObject("/Kids")] = kids
        campos.append(padre)

    if not cuadro:
        return campos, orden_calculo
    page = writer.pages[cuadro["page"]]
    for code in codigos:
        f = cuadro["filas"].get(code)
        if f:
            campos.append(campo_simple(writer, page, f"cant_{code}", f"Cantidad {code}",
                                       rect_campo(f["cant"], h, f["cant"][0] - 28), f"/PopR {f['size']:.1f} Tf {NAVY}",
                                       acciones(FMT_NUM, KEY_NUM)))

    lista = ", ".join(f'"{c}"' for c in cuadro["filas"])
    suma = (f'var c = [{lista}], s = 0;'
            'for (var i = 0; i < c.length; i++) s += n("cant_" + c[i]) * n("valor_" + c[i]);'
            'event.value = s > 0 ? Math.round(s) : "";')
    if con_iva:  # precios con IVA: el total es la suma y el neto se calcula hacia atrás
        calc = {
            "total": JS_NUM + suma,
            "subtotal": JS_NUM + f'var t = n("total_con_iva"); event.value = t > 0 ? Math.round(t / {1 + iva}) : "";',
            "iva": JS_NUM + 'var t = n("total_con_iva"); event.value = t > 0 ? t - n("subtotal_neto") : "";',
        }
    else:
        calc = {
            "subtotal": JS_NUM + suma,
            "iva": JS_NUM + f'var s = n("subtotal_neto"); event.value = s > 0 ? Math.round(s * {iva}) : "";',
            "total": JS_NUM + 'var s = n("subtotal_neto"); event.value = s > 0 ? s + n("iva") : "";',
        }
    nombres = {"subtotal": ("subtotal_neto", "Subtotal neto"), "iva": ("iva", f"IVA {round(iva * 100)}%"),
               "total": ("total_con_iva", "Total con IVA")}
    estilos = {"subtotal": f"/PopSB 9 Tf {GRIS_OSCURO}", "iva": f"/PopSB 9 Tf {GRIS_OSCURO}",
               "total": f"/PfdB 13 Tf {CREMA}"}
    for clave in calc:  # en el orden en que deben calcularse
        t = cuadro["totales"][clave]
        nombre, ayuda = nombres[clave]
        izquierda = t["bbox"][0] - (70 if clave == "total" else 44)
        ref = campo_simple(writer, page, nombre, ayuda + " (se calcula solo)",
                           rect_campo(t["bbox"], h, izquierda, alto=(18 if clave == "total" else None)),
                           estilos[clave], acciones(FMT_PESOS, None, calc[clave]))
        campos.append(ref)
        orden_calculo.append(ref)
    return campos, orden_calculo


# ---------------------------------------------------------------- principal

def main(cfg_path):
    cfg_path = Path(cfg_path).resolve()
    cfg_dir = cfg_path.parent
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    base = cfg_dir / cfg["base"]

    fichas, cuadro = analizar_base(base)
    faltan = [c for c in cfg["renders"] if c not in fichas]
    if faltan:
        sys.exit(f"Códigos sin ficha en la base: {faltan}")

    escudo = cfg.get("escudo_portada")
    portada = analizar_portada(base) if escudo else None

    writer = PdfWriter(clone_from=str(base))
    w, h = float(writer.pages[0].mediabox.width), float(writer.pages[0].mediabox.height)
    capa = construir_capa(base, cfg_dir, cfg, fichas, cuadro, portada, len(writer.pages), w, h)
    for page, over in zip(writer.pages, capa.pages):
        page.merge_page(over)

    if escudo:
        # escudo vectorial (fondo transparente) centrado donde estaba el emblema
        pagina_escudo = PdfReader(cfg_dir / escudo["pdf"]).pages[0]
        ew, eh = float(pagina_escudo.mediabox.width), float(pagina_escudo.mediabox.height)
        s = escudo.get("alto", 160) / eh
        x0, top, x1, bottom = portada["emblema"]
        cx, cy = (x0 + x1) / 2, h - (top + bottom) / 2
        writer.pages[0].merge_transformed_page(
            pagina_escudo, Transformation().scale(s).translate(cx - ew * s / 2, cy - eh * s / 2))

    fuentes = DictionaryObject({NameObject("/" + k): fuente_truetype(writer, v, k) for k, v in FUENTES.items()})
    precios = cfg.get("precios", {})
    campos, orden = agregar_formulario(writer, fichas, cuadro, cfg.get("iva", 0.19), h, fuentes,
                                       precios, cfg.get("precios_con_iva", False))
    writer._root_object[NameObject("/AcroForm")] = writer._add_object(DictionaryObject({
        NameObject("/Fields"): campos,
        NameObject("/CO"): orden,
        # con precios ya escritos, cada visor usa la apariencia formateada ($29.900) en vez de rehacerla
        NameObject("/NeedAppearances"): BooleanObject(not precios),
        NameObject("/DR"): DictionaryObject({NameObject("/Font"): fuentes}),
        NameObject("/DA"): TextStringObject(f"/PopR 9 Tf {NAVY}"),
    }))

    salida = cfg_dir / cfg["salida"]
    writer.compress_identical_objects()
    with open(salida, "wb") as fh:
        writer.write(fh)
    con_render = ", ".join(sorted(cfg["renders"]))
    sin_render = ", ".join(c for c in sorted(fichas) if c not in cfg["renders"])
    print(f"OK  {salida}  ({salida.stat().st_size / 1024:.0f} KB)")
    print(f"    Con render: {con_render}")
    print(f"    Sin render: {sin_render or '—'}")
    print(f"    Campos: {len(campos)} (valor unitario x{len(fichas)}, cantidades, subtotal, IVA, total)")
    if precios:
        print(f"    Precios cargados: {len(precios)} ({'con IVA' if cfg.get('precios_con_iva') else 'netos'})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent / "gauchos-rc-2027" / "propuesta.json")
