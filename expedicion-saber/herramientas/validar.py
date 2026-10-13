"""Valida el banco de contenido generado (contenido/**/*.json).

Revisa: esquema de cada OA y de cada tipo de desafío (incluido el audio opcional), mínimo 15 desafíos
por OA con al menos 3 en cada nivel de dificultad 1-5, ids únicos, prerequisitos existentes y sin
ciclos, tokens de ambientación conocidos y monedas base = 10. Avisa (sin fallar) si un desafío tiene
tanto texto que no se alcanzaría a resolver en 30 segundos. Lista los códigos pendientes de verificación.

Uso:  python3 herramientas/validar.py      (sale con código 1 si hay errores)
"""
import json
import os
import re
import sys

from objetivos import POR_ID

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "contenido")
TIPOS = {"opcion_multiple", "completar", "ordenar_secuencia", "emparejar", "arrastrar_categoria", "respuesta_numerica"}
TOKENS = {"personaje", "objeto", "objetos", "un_objeto", "los_objetos", "lugar", "contenedor", "contenedores",
          "el_contenedor", "la_construccion", "junto"}
CAMPOS_OA = ["nivel", "asignatura", "eje", "objetivo_oficial", "dificultad", "prerequisitos", "id_objetivo", "verificacion", "desafios"]
LIMITE_PALABRAS = 80  # texto + enunciado; más que esto difícilmente se lee y responde en 30 s
NIVELES = ["1_basico", "2_basico", "3_basico", "4_basico", "5_basico", "6_basico", "7_basico", "8_basico",
           "1_medio", "2_medio", "3_medio", "4_medio"]


def textos(d):
    """Todos los textos visibles de un desafío (para revisar tokens)."""
    out = [d.get("enunciado", ""), d.get("texto", ""), d.get("pista", ""), d.get("explicacion_error", ""),
           (d.get("audio") or {}).get("texto", "")]
    out += [str(x) for x in d.get("alternativas", [])] + [str(x) for x in d.get("elementos", []) if not isinstance(x, dict)]
    out += [e["texto"] for e in d.get("elementos", []) if isinstance(e, dict)]
    out += [x for p in d.get("pares", []) for x in p] + d.get("categorias", [])
    return out


def validar_desafio(d, err):
    pre = d.get("id", "?")
    for c in ("id", "tipo", "dificultad", "enunciado", "pista", "explicacion_error", "monedas"):
        if c not in d or d[c] in ("", None):
            err.append(f"{pre}: falta '{c}'")
    if d.get("tipo") not in TIPOS:
        err.append(f"{pre}: tipo desconocido {d.get('tipo')}")
    if d.get("dificultad") not in (1, 2, 3, 4, 5):
        err.append(f"{pre}: dificultad fuera de 1-5")
    if d.get("monedas") != 10:
        err.append(f"{pre}: monedas base distinta de 10")
    if "audio" in d:
        au = d["audio"]
        if not isinstance(au, dict) or not str(au.get("texto", "")).strip() or au.get("idioma") not in ("en", "es"):
            err.append(f"{pre}: 'audio' debe ser {{texto, idioma: en|es}}")
    t = d.get("tipo")
    if t in ("opcion_multiple", "completar"):
        a = d.get("alternativas", [])
        if len(a) != 4 or len(set(a)) != 4:
            err.append(f"{pre}: necesita 4 alternativas distintas")
        if not isinstance(d.get("correcta"), int) or not 0 <= d["correcta"] < len(a):
            err.append(f"{pre}: índice 'correcta' inválido")
        if t == "completar" and "___" not in d.get("enunciado", ""):
            err.append(f"{pre}: completar sin '___'")
    elif t == "ordenar_secuencia":
        e = d.get("elementos", [])
        if len(e) < 3 or len(set(e)) != len(e):
            err.append(f"{pre}: ordenar necesita 3+ elementos distintos")
    elif t == "emparejar":
        p = d.get("pares", [])
        if len(p) < 3 or len({x[0] for x in p}) != len(p) or len({x[1] for x in p}) != len(p):
            err.append(f"{pre}: emparejar necesita 3+ pares sin repetir")
    elif t == "arrastrar_categoria":
        cats, els = d.get("categorias", []), d.get("elementos", [])
        if len(cats) < 2 or len(els) < 4:
            err.append(f"{pre}: categoría necesita 2+ categorías y 4+ elementos")
        if any(not 0 <= e.get("categoria", -1) < len(cats) for e in els):
            err.append(f"{pre}: elemento con categoría inválida")
    elif t == "respuesta_numerica":
        if not isinstance(d.get("respuesta"), (int, float)) or not isinstance(d.get("tolerancia"), (int, float)) or d["tolerancia"] < 0:
            err.append(f"{pre}: respuesta o tolerancia inválidas")
    for txt in textos(d):
        for tok in re.findall(r"\{(\w+)\}", txt):
            if tok not in TOKENS:
                err.append(f"{pre}: token desconocido {{{tok}}}")


def main():
    err, ids, oas, pendientes, largos, sin_contenido = [], set(), {}, [], [], set()
    indice = json.load(open(os.path.join(RAIZ, "indice.json"), encoding="utf-8"))
    for a in indice["archivos"]:
        datos = json.load(open(os.path.join(RAIZ, a["archivo"]), encoding="utf-8"))
        for oa in datos:
            oid = oa.get("id_objetivo", "?")
            faltan = [c for c in CAMPOS_OA if c not in oa]
            if faltan:
                err.append(f"{oid}: faltan campos {faltan}")
            if oa["nivel"] != a["nivel"] or oa["asignatura"] != a["asignatura"]:
                err.append(f"{oid}: nivel/asignatura no coinciden con el archivo")
            if not re.fullmatch(r"\d_(basico|medio)\.\w+\.OA\d+", oid):
                err.append(f"{oid}: id de objetivo con formato inválido")
            oficial = oa["verificacion"].get("codigo_oficial")
            if not (oa["objetivo_oficial"].startswith("OA ") or (oficial and oa["objetivo_oficial"].startswith(oficial + ":"))):
                err.append(f"{oid}: objetivo_oficial debe empezar con 'OA n:' o con su código oficial")
            if oa["verificacion"]["codigo"] != "verificado":
                pendientes.append(oid)
            ds = oa["desafios"]
            if len(ds) < 15:
                err.append(f"{oid}: solo {len(ds)} desafíos (mínimo 15)")
            for n in range(1, 6):
                k = sum(1 for d in ds if d.get("dificultad") == n)
                if k < 3:
                    err.append(f"{oid}: nivel {n} tiene {k} desafíos (mínimo 3)")
            for d in ds:
                if d.get("id") in ids:
                    err.append(f"{d.get('id')}: id repetido")
                ids.add(d.get("id"))
                validar_desafio(d, err)
                palabras = len(f"{d.get('texto', '')} {d.get('enunciado', '')}".split())
                if palabras > LIMITE_PALABRAS:
                    largos.append(f"{d.get('id')} ({palabras} palabras)")
            oas[oid] = oa
    # prerequisitos: existen, no apuntan a un nivel superior y no forman ciclos
    for oid, oa in oas.items():
        for p in oa["prerequisitos"]:
            if p not in oas and p in POR_ID:
                sin_contenido.add(p)  # registrado en objetivos.py, con su banco aún en preparación
            elif p not in oas:
                err.append(f"{oid}: prerequisito inexistente {p}")
            elif NIVELES.index(oas[p]["nivel"]) > NIVELES.index(oa["nivel"]):
                err.append(f"{oid}: prerequisito {p} es de un nivel superior")
    estado = {}

    def visitar(o, camino):
        if estado.get(o) == 1:
            err.append(f"ciclo de prerequisitos: {' -> '.join(camino + [o])}")
            return
        if estado.get(o) == 2:
            return
        estado[o] = 1
        for p in oas.get(o, {}).get("prerequisitos", []):
            visitar(p, camino + [o])
        estado[o] = 2

    for o in oas:
        visitar(o, [])
    for t in indice["tramos"]:
        for o in t["objetivos"]:
            if o not in oas:
                err.append(f"tramo {t['id']}: objetivo inexistente {o}")
    total = sum(len(o["desafios"]) for o in oas.values())
    print(f"Objetivos: {len(oas)} | desafíos: {total} | ids únicos: {len(ids)}")
    print(f"Códigos pendientes de verificación ({len(pendientes)}): {', '.join(pendientes) or 'ninguno'}")
    if sin_contenido:
        print(f"Aviso: prerequisitos registrados aún sin desafíos (no bloquean al jugador): {', '.join(sorted(sin_contenido))}")
    if largos:
        print(f"Aviso: {len(largos)} desafíos con más de {LIMITE_PALABRAS} palabras de lectura: {', '.join(largos[:20])}")
    if err:
        print(f"\n{len(err)} errores:")
        for e in err[:60]:
            print(" -", e)
        sys.exit(1)
    print("Banco válido.")


if __name__ == "__main__":
    main()
