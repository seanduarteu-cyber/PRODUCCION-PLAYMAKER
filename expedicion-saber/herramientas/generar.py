"""Genera el banco de contenido: un JSON por asignatura y nivel en contenido/<nivel>/<asignatura>.json,
más contenido/indice.json con la lista de archivos, objetivos y tramos.

Uso:  python3 herramientas/generar.py
"""
import importlib
import json
import os

from objetivos import OBJETIVOS

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "contenido")
NOMBRES_MODULOS = ["matematica_1_2", "matematica_3_4", "matematica_5_8", "lenguaje_1_2", "lenguaje_3_4", "lenguaje_5_8",
                   "ciencias_1_4", "ciencias_5_8", "ingles_1_4", "ingles_5_8"]
MODULOS = []
for _n in NOMBRES_MODULOS:
    try:
        MODULOS.append(importlib.import_module(_n))
    except ModuleNotFoundError as e:
        if e.name != _n:
            raise
        print(f"Aviso: falta el banco {_n}.py; sus OA quedan sin publicar.")
GENERADORES = {}
for _m in MODULOS:
    repetidos = GENERADORES.keys() & _m.GENERADORES.keys()
    assert not repetidos, f"OA con dos generadores: {repetidos}"
    GENERADORES.update(_m.GENERADORES)
ORDEN_NIVELES = [f"{n}_basico" for n in range(1, 9)]
NOMBRE_NIVEL = {f"{n}_basico": f"{n}° básico" for n in range(1, 9)}
NOMBRE_ASIG = {"matematica": "Matemática", "lenguaje": "Lenguaje y Comunicación", "ciencias": "Ciencias Naturales",
               "ingles": "Inglés"}


def bloque(oa):
    desafios = GENERADORES[oa["id_objetivo"]]()
    desafios.sort(key=lambda d: (d["dificultad"], d["id"]))
    return {
        "nivel": oa["nivel"],
        "asignatura": oa["asignatura"],
        "eje": oa["eje"],
        "objetivo_oficial": oa["objetivo_oficial"],
        "dificultad": oa["dificultad"],
        "prerequisitos": oa["prerequisitos"],
        "id_objetivo": oa["id_objetivo"],
        "verificacion": oa["verificacion"],
        "desafios": desafios,
    }


def main():
    faltan = [o["id_objetivo"] for o in OBJETIVOS if o["id_objetivo"] not in GENERADORES]
    sobran = [k for k in GENERADORES if k not in {o["id_objetivo"] for o in OBJETIVOS}]
    assert not sobran, f"Generadores sin OA registrado en objetivos.py: {sobran}"
    if faltan:
        print(f"Aviso: {len(faltan)} OA registrados aún sin desafíos: {', '.join(faltan)}")
    archivos, tramos = [], []
    for nivel in ORDEN_NIVELES:
        for asig in NOMBRE_ASIG:
            oas = [o for o in OBJETIVOS if o["nivel"] == nivel and o["asignatura"] == asig and o["id_objetivo"] in GENERADORES]
            if not oas:
                continue
            datos = [bloque(o) for o in oas]
            ruta = os.path.join(RAIZ, nivel, f"{asig}.json")
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
                f.write("\n")
            rel = f"{nivel}/{asig}.json"
            archivos.append({"archivo": rel, "nivel": nivel, "asignatura": asig,
                             "objetivos": [o["id_objetivo"] for o in oas],
                             "desafios": sum(len(d["desafios"]) for d in datos)})
            tramos.append({"id": f"{nivel}.{asig}", "nombre": f"{NOMBRE_ASIG[asig]} {NOMBRE_NIVEL[nivel]}",
                           "objetivos": [o["id_objetivo"] for o in oas]})
    indice = {"version": 1, "niveles": ORDEN_NIVELES, "nombres_nivel": NOMBRE_NIVEL, "asignaturas": NOMBRE_ASIG,
              "archivos": archivos, "tramos": tramos}
    with open(os.path.join(RAIZ, "indice.json"), "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)
        f.write("\n")
    total = sum(a["desafios"] for a in archivos)
    print(f"{len(archivos)} archivos, {len(OBJETIVOS)} objetivos, {total} desafíos")


if __name__ == "__main__":
    main()
