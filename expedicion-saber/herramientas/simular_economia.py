"""Simula la economía con las mismas reglas del motor (js/motor.js) para justificar la tabla de costos.

Modelo de jugador: probabilidad de acertar al primer intento
  p1 = min(0,95, habilidad + APRENDIZAJE × desafíos practicados en ese OA) − 0,07 × (dificultad − 1).
El término de aprendizaje refleja que practicar un objetivo mejora el desempeño en él.
Si falla, acierta al segundo intento con 60 % y al tercero con 60 %. Juega sesiones de 10 desafíos sobre
el objetivo recomendado y pasa al siguiente cuando lo domina. Cada tramo tiene los OA reales del banco.

Uso:  python3 herramientas/simular_economia.py
"""
import json
import os
import random
import statistics

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ECO = json.load(open(os.path.join(RAIZ, "mundos", "mundos.json"), encoding="utf-8"))["economia"]
INDICE = json.load(open(os.path.join(RAIZ, "contenido", "indice.json"), encoding="utf-8"))
OA_POR_TRAMO = statistics.mean(len(t["objetivos"]) for t in INDICE["tramos"])
COSTOS = ECO["costos_por_nivel"]
APRENDIZAJE = 0.01  # mejora de la probabilidad de acierto por cada desafío practicado en un OA


def simular(habilidad, dias_por_semana, sesiones_max=400, semilla=0):
    r = random.Random(semilla)
    monedas, racha, sesiones = 0, 0, 0
    nivel, ok, fallos, dominados, practica = 1, 0, 0, 0, 0
    hitos = {}
    dia, jugados_semana = 0, 0
    while sesiones < sesiones_max:
        # calendario: juega los primeros `dias_por_semana` días de cada semana, una sesión por día
        jugado_ayer = dia > 0 and (dia - 1) % 7 < dias_por_semana
        if dia % 7 >= dias_por_semana:
            dia += 1
            continue
        racha = racha + 1 if jugado_ayer else 1
        for _ in range(ECO["desafios_por_sesion"]):
            p1 = max(0.15, min(0.95, habilidad + APRENDIZAJE * practica) - 0.07 * (nivel - 1))
            practica += 1
            if r.random() < p1:
                intento = 1
            elif r.random() < 0.6:
                intento = 2
            elif r.random() < 0.6:
                intento = 3
            else:
                intento = 0
            if intento:
                monedas += ECO["monedas_por_intento"][intento - 1]
            if intento == 1:
                ok, fallos = ok + 1, 0
                if ok >= 3:
                    ok = 0
                    if nivel < 5:
                        nivel += 1
                    else:
                        dominados += 1
                        monedas += ECO["bono_dominio_objetivo"]
                        hitos.setdefault("dominar 1 OA", sesiones + 1)
                        if dominados >= OA_POR_TRAMO:
                            hitos.setdefault("dominar 1 tramo", sesiones + 1)
                        nivel, practica = 1, 0  # siguiente objetivo
            else:
                ok, fallos = 0, fallos + 1
                if fallos >= 2:
                    fallos = 0
                    nivel = max(1, nivel - 1)
        monedas += ECO["bono_sesion"] + min(racha * ECO["racha"]["bono_por_dia"], ECO["racha"]["tope"])
        sesiones += 1
        if sesiones == 1:
            hitos["monedas 1a sesión"] = monedas
        for nombre, meta in [("primera mejora (50)", COSTOS[0]), ("juntar mejora intermedia (400)", COSTOS[2]),
                             ("juntar nivel 4 (800)", COSTOS[3]), ("juntar mejora final (1800)", COSTOS[4]),
                             ("avatar completo de un mundo", 5 * sum(COSTOS))]:
            if monedas >= meta:
                hitos.setdefault(nombre, sesiones)
        dia += 1
    hitos["monedas por sesión"] = monedas / sesiones
    return hitos


def main():
    perfiles = [("Le cuesta (habilidad 0,55)", 0.55), ("Promedio (0,70)", 0.70), ("Le va muy bien (0,85)", 0.85)]
    claves = ["monedas 1a sesión", "monedas por sesión", "primera mejora (50)", "juntar mejora intermedia (400)",
              "juntar nivel 4 (800)", "dominar 1 OA", "dominar 1 tramo", "juntar mejora final (1800)", "avatar completo de un mundo"]
    print(f"OA por tramo (promedio del banco): {OA_POR_TRAMO:.2f}\n")
    for dias in (7, 4):
        print(f"### Juega {dias} días por semana (1 sesión por día)\n")
        print("| Hito | " + " | ".join(n for n, _ in perfiles) + " |")
        print("|---|" + "---|" * len(perfiles))
        res = {n: [simular(h, dias, semilla=s) for s in range(300)] for n, h in perfiles}
        for k in claves:
            fila = []
            for n, _ in perfiles:
                vals = [x[k] for x in res[n] if k in x]
                if not vals:
                    fila.append("—")
                elif k.startswith("monedas"):
                    fila.append(f"{statistics.mean(vals):.0f}")
                else:
                    fila.append(f"{statistics.median(vals):.0f} ses.")
            print(f"| {k} | " + " | ".join(fila) + " |")
        print()


if __name__ == "__main__":
    main()
