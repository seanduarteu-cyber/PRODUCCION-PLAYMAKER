"""Genera el banco de contenido: un JSON por asignatura y nivel en contenido/<nivel>/<asignatura>.json,
más contenido/indice.json con la lista de archivos, objetivos y tramos.

Uso:  python3 herramientas/generar.py
"""
import json
import os

from objetivos import OBJETIVOS
import matematica_1_2, matematica_3_4, lenguaje_1_2, lenguaje_3_4

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "contenido")
GENERADORES = {**matematica_1_2.GENERADORES, **matematica_3_4.GENERADORES,
               **lenguaje_1_2.GENERADORES, **lenguaje_3_4.GENERADORES}
ORDEN_NIVELES = ["1_basico", "2_basico", "3_basico", "4_basico"]
NOMBRE_NIVEL = {"1_basico": "1° básico", "2_basico": "2° básico", "3_basico": "3° básico", "4_basico": "4° básico"}
NOMBRE_ASIG = {"matematica": "Matemática", "lenguaje": "Lenguaje y Comunicación"}


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
    assert not faltan, f"OA sin generador: {faltan}"
    archivos, tramos = [], []
    for nivel in ORDEN_NIVELES:
        for asig in ("matematica", "lenguaje"):
            oas = [o for o in OBJETIVOS if o["nivel"] == nivel and o["asignatura"] == asig]
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
