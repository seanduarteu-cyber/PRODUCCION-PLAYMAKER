"""Tendencia: entrar a favor de la tendencia cuando el precio retrocede a la EMA lenta.

Largo:  EMA9 > EMA21 > EMA200, la EMA200 sube, la vela toca la EMA21 y cierra
        sobre la EMA9 como vela alcista.
Corto:  espejo.
Stop:   stop_atr x ATR.   Objetivo: objetivo_r veces el riesgo.
"""
from __future__ import annotations

import pandas as pd

from ..indicadores import atr, ema
from .base import armar


def calcular(df: pd.DataFrame, p: dict) -> pd.DataFrame:
    c = df["close"]
    rapida = ema(c, p["ema_rapida"])
    lenta = ema(c, p["ema_lenta"])
    tend = ema(c, p["ema_tendencia"])
    pendiente = tend - tend.shift(12)
    dist = p["stop_atr"] * atr(df, p["atr"])

    alcista = (rapida > lenta) & (lenta > tend) & (pendiente > 0)
    bajista = (rapida < lenta) & (lenta < tend) & (pendiente < 0)
    largo = alcista & (df["low"] <= lenta) & (c > rapida) & (c > df["open"])
    corto = bajista & (df["high"] >= lenta) & (c < rapida) & (c < df["open"])

    r = p["objetivo_r"]
    return armar(df, largo, corto, c,
                 c - dist, c + dist,
                 c + r * dist, c - r * dist)
