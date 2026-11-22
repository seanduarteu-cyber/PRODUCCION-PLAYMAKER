"""Wyckoff simplificado: spring (largo) y upthrust (corto) dentro de un rango lateral.

Rango:     máximo y mínimo de las últimas `rango_velas` velas (sin contar la actual), con un
           ancho entre ancho_min_atr y ancho_max_atr veces el ATR (lateral, no tendencia).
Spring:    la vela perfora el piso del rango, cierra de vuelta adentro, en su mitad superior,
           con volumen > vol_mult x el promedio del rango.
Upthrust:  espejo en el techo del rango.
Stop:      más allá de la mecha de la vela (+ stop_margen_atr x ATR).
Objetivo:  el lado opuesto del rango. Solo opera si objetivo >= rr_min x riesgo.
"""
from __future__ import annotations

import pandas as pd

from ..indicadores import atr
from .base import armar, filtro_rr


def calcular(df: pd.DataFrame, p: dict) -> pd.DataFrame:
    c, h, l, v = df["close"], df["high"], df["low"], df["volume"]
    n = p["rango_velas"]
    piso = l.rolling(n, min_periods=n).min().shift(1)
    techo = h.rolling(n, min_periods=n).max().shift(1)
    a = atr(df, p["atr"])
    ancho = (techo - piso) / a
    en_rango = (ancho <= p["ancho_max_atr"]) & (ancho >= p["ancho_min_atr"])
    vol_ok = v > p["vol_mult"] * v.rolling(n, min_periods=n).mean().shift(1)
    mitad = (h + l) / 2

    spring = en_rango & (l < piso) & (c > piso) & (c > mitad) & vol_ok
    upthrust = en_rango & (h > techo) & (c < techo) & (c < mitad) & vol_ok

    m = p["stop_margen_atr"] * a
    stop_l, stop_c = l - m, h + m
    spring &= filtro_rr(c, stop_l, techo, p["rr_min"])
    upthrust &= filtro_rr(c, stop_c, piso, p["rr_min"])

    return armar(df, spring, upthrust, c,
                 stop_l, stop_c,
                 techo, piso)
