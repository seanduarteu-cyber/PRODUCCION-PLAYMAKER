"""Ruptura: tras una compresión de volatilidad, entrar cuando el precio rompe el canal con volumen.

Compresión: el ancho de Bollinger de la vela anterior está en el percentil bajo de la última
            ventana (por defecto 288 velas = 1 día).
Largo:  cierre sobre el máximo de las últimas `canal` velas y volumen > vol_mult x promedio.
Corto:  espejo con el mínimo.
Stop:   stop_atr x ATR.   Objetivo: objetivo_r veces el riesgo.
"""
from __future__ import annotations

import pandas as pd

from ..indicadores import atr, bollinger, sma
from .base import armar


def calcular(df: pd.DataFrame, p: dict) -> pd.DataFrame:
    c, v = df["close"], df["volume"]
    n = p["canal"]
    techo = df["high"].rolling(n, min_periods=n).max().shift(1)
    piso = df["low"].rolling(n, min_periods=n).min().shift(1)
    vol_ok = v > p["vol_mult"] * sma(v, 20).shift(1)

    inf, media, sup = bollinger(c, 20, 2.0)
    ancho = (sup - inf) / media
    w = p["compresion_ventana"]
    umbral = ancho.rolling(w, min_periods=w).quantile(p["compresion_percentil"])
    comprimido = ancho.shift(1) <= umbral.shift(1)

    dist = p["stop_atr"] * atr(df, p["atr"])
    largo = (c > techo) & vol_ok & comprimido
    corto = (c < piso) & vol_ok & comprimido

    r = p["objetivo_r"]
    return armar(df, largo, corto, c,
                 c - dist, c + dist,
                 c + r * dist, c - r * dist)
