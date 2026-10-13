"""Constructores de desafíos y registro de objetivos de aprendizaje (OA).

Cada desafío sigue el esquema del banco de contenido. Los campos comunes son
id, tipo, dificultad, enunciado, pista, explicacion_error y monedas; cada tipo
agrega los suyos (ver docs/contenido.md).

Tokens de ambientación: {personaje}, {objeto}, {objetos}, {un_objeto}, {los_objetos},
{lugar}, {contenedor}, {contenedores}, {el_contenedor}, {la_construccion}, {junto}.
El motor los reemplaza según el mundo elegido (mundos/mundos.json).
"""
import random

MONEDAS_BASE = 10


def _base(id_, tipo, dificultad, enunciado, pista, explicacion_error):
    return {
        "id": id_,
        "tipo": tipo,
        "dificultad": dificultad,
        "enunciado": enunciado,
        "pista": pista,
        "explicacion_error": explicacion_error,
        "monedas": MONEDAS_BASE,
    }


def _ordenar_campos(d, extra):
    out = {k: d[k] for k in ("id", "tipo", "dificultad", "enunciado")}
    out.update(extra)
    out.update({k: d[k] for k in ("pista", "explicacion_error", "monedas")})
    return out


def _txt(x):
    """Texto de una alternativa: los negativos llevan signo menos tipográfico y los decimales, coma."""
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return str(x)
    s = str(x).replace(".", ",")
    return "−" + s[1:] if x < 0 else s


def opcion_multiple(id_, dificultad, enunciado, correcta, distractores, pista, explicacion, rng=None):
    """correcta: texto de la alternativa correcta; distractores: 3 textos distintos."""
    rng = rng or random.Random(id_)  # semilla fija por id: el banco es reproducible
    alts = [_txt(correcta)] + [_txt(d) for d in distractores]
    assert len(alts) == 4 and len(set(alts)) == 4, (id_, alts)
    rng.shuffle(alts)
    d = _base(id_, "opcion_multiple", dificultad, enunciado, pista, explicacion)
    return _ordenar_campos(d, {"alternativas": alts, "correcta": alts.index(_txt(correcta))})


def completar(id_, dificultad, enunciado, correcta, distractores, pista, explicacion, rng=None):
    """enunciado contiene '___' donde va la alternativa elegida."""
    assert "___" in enunciado, id_
    rng = rng or random.Random(id_)  # semilla fija por id: el banco es reproducible
    alts = [_txt(correcta)] + [_txt(d) for d in distractores]
    assert len(alts) == 4 and len(set(alts)) == 4, (id_, alts)
    rng.shuffle(alts)
    d = _base(id_, "completar", dificultad, enunciado, pista, explicacion)
    return _ordenar_campos(d, {"alternativas": alts, "correcta": alts.index(_txt(correcta))})


def ordenar(id_, dificultad, enunciado, elementos_en_orden, pista, explicacion):
    """elementos_en_orden: lista en el orden correcto; el motor la desordena."""
    els = [str(e) for e in elementos_en_orden]
    assert 3 <= len(els) <= 6 and len(set(els)) == len(els), (id_, els)
    d = _base(id_, "ordenar_secuencia", dificultad, enunciado, pista, explicacion)
    return _ordenar_campos(d, {"elementos": els})


def emparejar(id_, dificultad, enunciado, pares, pista, explicacion):
    """pares: lista de [izquierda, derecha]; ambos lados sin repetidos."""
    pares = [[str(a), str(b)] for a, b in pares]
    assert 3 <= len(pares) <= 5, id_
    assert len({a for a, _ in pares}) == len(pares) and len({b for _, b in pares}) == len(pares), (id_, pares)
    d = _base(id_, "emparejar", dificultad, enunciado, pista, explicacion)
    return _ordenar_campos(d, {"pares": pares})


def categoria(id_, dificultad, enunciado, categorias, elementos, pista, explicacion):
    """elementos: lista de (texto, índice de categoría)."""
    els = [{"texto": str(t), "categoria": c} for t, c in elementos]
    assert 2 <= len(categorias) <= 3 and 4 <= len(els) <= 8, id_
    assert len({e["texto"] for e in els}) == len(els), (id_, els)
    assert all(0 <= e["categoria"] < len(categorias) for e in els), id_
    assert all(any(e["categoria"] == i for e in els) for i in range(len(categorias))), id_
    d = _base(id_, "arrastrar_categoria", dificultad, enunciado, pista, explicacion)
    return _ordenar_campos(d, {"categorias": list(categorias), "elementos": els})


def numerica(id_, dificultad, enunciado, respuesta, pista, explicacion, tolerancia=0, unidad=""):
    d = _base(id_, "respuesta_numerica", dificultad, enunciado, pista, explicacion)
    extra = {"respuesta": respuesta, "tolerancia": tolerancia}
    if unidad:
        extra["unidad"] = unidad
    return _ordenar_campos(d, extra)


def distractores_numericos(correcta, candidatos, n=3, minimo=0):
    """Elige n distractores distintos de la respuesta correcta, no negativos."""
    out = []
    for c in candidatos:
        if c != correcta and c >= minimo and c not in out:
            out.append(c)
        if len(out) == n:
            return out
    k = 1
    while len(out) < n:
        for c in (correcta + k, correcta - k):
            if c != correcta and c >= minimo and c not in out and len(out) < n:
                out.append(c)
        k += 1
    return out


def rng_para(semilla):
    return random.Random(semilla)
