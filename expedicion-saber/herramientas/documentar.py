"""Regenera las partes de la documentación que salen del banco: la tabla de cobertura y los códigos pendientes
(docs/contenido.md) y el árbol de prerequisitos (docs/progresion.md). Reemplaza solo lo que está entre las
marcas <!-- inicio:X --> y <!-- fin:X -->.

Uso:  python3 herramientas/documentar.py      (después de generar.py)
"""
import json
import os
import re

from objetivos import OBJETIVOS, POR_ID

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CONTENIDO = os.path.join(BASE, "contenido")
CORTA = {"matematica": "Mat", "lenguaje": "Len", "ciencias": "Cie", "ingles": "Ing"}
CODIGO = {"matematica": "MA", "lenguaje": "LE", "ciencias": "CN", "ingles": "EN"}
# En media, Inglés usa IN y algunas asignaturas cambian de prefijo (se completa al verificar cada código).
PREFIJO_MEDIO = {("ingles", n): "IN" for n in "1234"}
# Por qué cada código quedó pendiente (se muestra en docs/contenido.md).
MOTIVOS = {
    "1_basico.lenguaje.OA4": "aparece en el eje Lectura de 1° básico (texto «Leo Primero»), pero no se pudo confirmar su redacción.",
    "1_basico.lenguaje.OA8": "aparece en el eje Lectura de 1° básico (texto «Leo Primero»), pero no se pudo confirmar su redacción.",
    "2_basico.lenguaje.OA21": "la lista de contenidos ortográficos apareció junto a otro código en la fuente; falta confirmar que el número sea 21.",
    "6_basico.lenguaje.OA21": "el número y el tema (participios irregulares) salen de un documento secundario; falta confirmarlos en una página oficial.",
    "1_basico.ingles.OA13": "las páginas del Mineduc sobre la propuesta curricular de Inglés de 1° básico se contradicen en qué eje corresponde a cada número; conviene revisar el PDF oficial.",
    "2_basico.ingles.OA13": "no se pudo confirmar su redacción en una página oficial; se supuso igual al OA 13 de 3° y 4° básico, que sí está verificado.",
}


def nivel_num(nivel):
    """Posición del curso: 1° a 8° básico = 1 a 8; 1° a 4° medio = 9 a 12."""
    n, tipo = nivel.split("_")
    return int(n) + (8 if tipo == "medio" else 0)


def nombre_nivel(nivel):
    n, tipo = nivel.split("_")
    return f"{n}° {'medio' if tipo == 'medio' else 'básico'}"


def etiqueta(oid):
    nivel, asig, oa = oid.split(".")
    n, tipo = nivel.split("_")
    oficial = POR_ID.get(oid, {}).get("verificacion", {}).get("codigo_oficial")
    return f"{n}°{'M' if tipo == 'medio' else ''} {CORTA[asig]} {(oficial.split('-')[1] + ' OAC ' + oficial.split('-')[-1]) if oficial else 'OA ' + oa[2:]}"


def codigo_oficial(o):
    if o["verificacion"].get("codigo_oficial"):
        return o["verificacion"]["codigo_oficial"]
    n, tipo = o["nivel"].split("_")
    num = int(o["id_objetivo"].split(".OA")[1])
    if tipo == "medio":
        return f"{PREFIJO_MEDIO.get((o['asignatura'], n), CODIGO[o['asignatura']])}{n}M OA {num:02d}"
    pref = "IN" if o["asignatura"] == "ingles" and int(n) >= 5 else CODIGO[o["asignatura"]]
    return f"{pref}{int(n):02d} OA {num:02d}"


def reemplazar(ruta, marca, nuevo):
    txt = open(ruta, encoding="utf-8").read()
    patron = re.compile(rf"(<!-- inicio:{marca} -->\n).*?(<!-- fin:{marca} -->)", re.S)
    assert patron.search(txt), f"faltan las marcas {marca} en {ruta}"
    txt = patron.sub(lambda m: m.group(1) + nuevo.rstrip() + "\n" + m.group(2), txt)
    open(ruta, "w", encoding="utf-8").write(txt)


def main():
    indice = json.load(open(os.path.join(CONTENIDO, "indice.json"), encoding="utf-8"))
    oas = {}
    for a in indice["archivos"]:
        for oa in json.load(open(os.path.join(CONTENIDO, a["archivo"]), encoding="utf-8")):
            oas[oa["id_objetivo"]] = oa
    asignaturas = indice["asignaturas"]
    total = sum(len(o["desafios"]) for o in oas.values())
    con_audio = sum(1 for o in oas.values() for d in o["desafios"] if "audio" in d)

    # ---------- cobertura ----------
    lineas = [f"{len(oas)} objetivos y {total:,} desafíos ({con_audio} con audio en inglés).".replace(",", ".") + " Resumen por asignatura:", "",
              "| Asignatura | Cursos | OA | Desafíos |", "|---|---|---|---|"]
    for asig, nombre in asignaturas.items():
        de = [o for o in oas.values() if o["asignatura"] == asig]
        if not de:
            continue
        cursos = sorted({o["nivel"] for o in de}, key=nivel_num)
        lineas.append(f"| {nombre} | {nombre_nivel(cursos[0])} a {nombre_nivel(cursos[-1])} | {len(de)} | {sum(len(o['desafios']) for o in de)} |")
    sin_banco = [o["id_objetivo"] for o in OBJETIVOS if o["id_objetivo"] not in oas]
    if sin_banco:
        lineas += ["", f"Registrados en `herramientas/objetivos.py` y aún sin desafíos ({len(sin_banco)}): "
                   + ", ".join(etiqueta(x) for x in sin_banco) + "."]
    for asig, nombre in asignaturas.items():
        de = sorted((o for o in oas.values() if o["asignatura"] == asig),
                    key=lambda o: (nivel_num(o["nivel"]), int(o["id_objetivo"].split(".OA")[1])))
        if not de:
            continue
        lineas += ["", f"### {nombre}", "", "| Nivel | OA | Eje | Desafíos | Código | Prerequisitos |", "|---|---|---|---|---|---|"]
        for o in de:
            num = o["id_objetivo"].split(".OA")[1]
            cod = "verificado" if o["verificacion"]["codigo"] == "verificado" else "**pendiente**"
            pre = ", ".join(etiqueta(p) for p in o["prerequisitos"]) or "—"
            cod_txt = o["verificacion"].get("codigo_oficial") or f"OA {num}"
            lineas.append(f"| {nombre_nivel(o['nivel'])} | [{cod_txt}]({o['verificacion']['fuente']}) | {o['eje']} | "
                          f"{len(o['desafios'])} | {cod} | {pre} |")
    reemplazar(os.path.join(BASE, "docs", "contenido.md"), "cobertura", "\n".join(lineas))

    # ---------- pendientes de verificación ----------
    pend = [o for o in OBJETIVOS if o["verificacion"]["codigo"] != "verificado"]
    lineas = [f"- **{codigo_oficial(o)}** ({o['objetivo_oficial'].split(': ', 1)[1].rstrip('.').lower()[:80]}…): "
              + MOTIVOS.get(o["id_objetivo"], "no se pudo confirmar su redacción en una página oficial.") for o in pend]
    reemplazar(os.path.join(BASE, "docs", "contenido.md"), "pendientes", "\n".join(lineas))

    # ---------- árbol de prerequisitos, un diagrama por asignatura ----------
    nodo = lambda oid: re.sub(r"\W", "_", oid)
    lineas = []
    for asig, nombre in asignaturas.items():
        de = [oid for oid in oas if oas[oid]["asignatura"] == asig]
        if not de:
            continue
        lineas += [f"#### {nombre}", "", "```mermaid", "flowchart LR"]
        con_flecha = set()
        for oid in sorted(de, key=lambda x: (nivel_num(oas[x]["nivel"]), int(x.split(".OA")[1]))):
            for p in oas[oid]["prerequisitos"]:
                if p in oas:
                    lineas.append(f'  {nodo(p)}["{etiqueta(p)}"] --> {nodo(oid)}["{etiqueta(oid)}"]')
                    con_flecha |= {p, oid}
        sueltos = [oid for oid in de if oid not in con_flecha]
        lineas += [f'  {nodo(oid)}["{etiqueta(oid)}"]' for oid in sueltos]
        lineas += ["```", ""]
    reemplazar(os.path.join(BASE, "docs", "progresion.md"), "arbol", "\n".join(lineas))
    print(f"Documentación actualizada: {len(oas)} OA, {total} desafíos, {len(pend)} códigos pendientes.")


if __name__ == "__main__":
    main()
