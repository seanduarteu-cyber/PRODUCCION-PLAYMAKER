"""Reversión a la media: comprar sobreventa / vender sobrecompra cuando NO hay tendencia.

Largo:  cierre bajo la banda inferior de Bollinger, RSI < rsi_bajo y ADX < adx_max (mercado lateral).
Corto:  espejo con la banda superior y RSI > rsi_alto.
Stop:   stop_atr x ATR.   Objetivo: la media de Bollinger (vuelta a la media).
Solo opera si el objetivo está al menos a rr_min veces el riesgo.
"""
from __future__ import annotations

import pandas as pd

from ..indicadores import adx, atr, bollinger, rsi
from .base import armar, filtro_rr


def calcular(df: pd.DataFrame, p: dict) -> pd.DataFrame:
    c = df["close"]
    inf, media, sup = bollinger(c, p["periodo"], p["desv"])
    r = rsi(c, p["rsi"])
    lateral = adx(df, 14) < p["adx_max"]
    dist = p["stop_atr"] * atr(df, p["atr"])

    largo = (c < inf) & (r < p["rsi_bajo"]) & lateral
    corto = (c > sup) & (r > p["rsi_alto"]) & lateral
    largo &= filtro_rr(c, c - dist, media, p["rr_min"])
    corto &= filtro_rr(c, c + dist, media, p["rr_min"])

    return armar(df, largo, corto, c,
                 c - dist, c + dist,
                 media, media)
