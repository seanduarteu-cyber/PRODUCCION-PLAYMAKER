"""Compuerta de rendimiento: decide si una estrategia puede pasar a dinero real.

Es la versión honesta de "asegurar rentabilidad": nada la garantiza, pero el bot se niega a
operar con dinero real si la estrategia no demostró ventaja en datos que no se usaron para
diseñarla (fuera de muestra) y luego en la cuenta demo.
"""
from __future__ import annotations


def evaluar(m: dict, req: dict, min_operaciones: int | None = None) -> tuple[bool, list[str]]:
    motivos = []
    n_min = req["min_operaciones"] if min_operaciones is None else min_operaciones
    if m["operaciones"] < n_min:
        motivos.append(f"pocas operaciones ({m['operaciones']} < {n_min})")
    if m["factor_beneficio"] < req["factor_beneficio_min"]:
        motivos.append(f"factor de beneficio {m['factor_beneficio']:.2f} < {req['factor_beneficio_min']}")
    if m["esperanza_r"] < req["esperanza_min_r"]:
        motivos.append(f"esperanza {m['esperanza_r']:+.3f}R < {req['esperanza_min_r']}R")
    if m["caida_max"] > req["caida_max"]:
        motivos.append(f"caída máxima {m['caida_max']:.1%} > {req['caida_max']:.0%}")
    return (not motivos), motivos
