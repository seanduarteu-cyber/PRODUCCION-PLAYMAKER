"""Piezas comunes a todas las estrategias.

Cada estrategia es una función `calcular(df, params) -> DataFrame` que devuelve, para cada vela,
las columnas:
    senal     1 = largo, -1 = corto, 0 = nada
    entrada   precio de la orden límite (normalmente el cierre de la vela de la señal)
    stop      precio del stop loss
    objetivo  precio del take profit

La señal de la vela i se calcula SOLO con velas <= i (sin mirar el futuro). La orden se coloca
después del cierre de la vela i, así que el backtest y el bot en vivo usan exactamente el mismo código.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class Senal:
    lado: int          # 1 largo, -1 corto
    entrada: float
    stop: float
    objetivo: float
    estrategia: str

    @property
    def lado_txt(self) -> str:
        return "LARGO" if self.lado == 1 else "CORTO"


def armar(df: pd.DataFrame, largo, corto, entrada,
          stop_largo, stop_corto, obj_largo, obj_corto) -> pd.DataFrame:
    largo = np.asarray(largo, dtype=bool)
    corto = np.asarray(corto, dtype=bool) & ~largo
    senal = np.where(largo, 1, np.where(corto, -1, 0))
    entrada = np.asarray(entrada, dtype=float)
    stop = np.where(largo, stop_largo, np.where(corto, stop_corto, np.nan)).astype(float)
    obj = np.where(largo, obj_largo, np.where(corto, obj_corto, np.nan)).astype(float)

    with np.errstate(invalid="ignore"):
        valido = (((senal == 1) & (stop < entrada) & (obj > entrada)) |
                  ((senal == -1) & (stop > entrada) & (obj < entrada)))
    senal = np.where(valido, senal, 0)
    return pd.DataFrame({
        "senal": senal,
        "entrada": np.where(valido, entrada, np.nan),
        "stop": np.where(valido, stop, np.nan),
        "objetivo": np.where(valido, obj, np.nan),
    }, index=df.index)


def filtro_rr(entrada, stop, objetivo, rr_min: float):
    """True donde (ganancia potencial) >= rr_min * (riesgo)."""
    riesgo = np.abs(np.asarray(entrada) - np.asarray(stop))
    premio = np.abs(np.asarray(objetivo) - np.asarray(entrada))
    with np.errstate(invalid="ignore"):
        return premio >= rr_min * riesgo
