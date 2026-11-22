"""Registro de estrategias disponibles."""
from __future__ import annotations

import math

import pandas as pd

from . import bollinger_rsi, ema_pullback, ruptura_volumen, wyckoff
from .base import Senal

ESTRATEGIAS = {
    "ema_pullback": ema_pullback.calcular,
    "bollinger_rsi": bollinger_rsi.calcular,
    "ruptura_volumen": ruptura_volumen.calcular,
    "wyckoff": wyckoff.calcular,
}

DESCRIPCION = {
    "ema_pullback": "Tendencia: retroceso a la EMA 21",
    "bollinger_rsi": "Reversión a la media: Bollinger + RSI",
    "ruptura_volumen": "Ruptura con volumen tras compresión",
    "wyckoff": "Wyckoff: spring / upthrust",
}


def calcular(nombre: str, df: pd.DataFrame, params: dict) -> pd.DataFrame:
    if nombre not in ESTRATEGIAS:
        raise ValueError(f"Estrategia desconocida: {nombre}. Opciones: {list(ESTRATEGIAS)}")
    return ESTRATEGIAS[nombre](df, params)


def ultima_senal(nombre: str, df: pd.DataFrame, params: dict) -> Senal | None:
    """Señal en la última vela CERRADA de df (la que usa el bot en vivo)."""
    fila = calcular(nombre, df, params).iloc[-1]
    if fila["senal"] == 0 or any(math.isnan(fila[k]) for k in ("entrada", "stop", "objetivo")):
        return None
    return Senal(int(fila["senal"]), float(fila["entrada"]), float(fila["stop"]),
                 float(fila["objetivo"]), nombre)
