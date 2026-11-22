"""Indicadores técnicos. Todos son causales: el valor en la vela i usa solo velas <= i."""
from __future__ import annotations

import numpy as np
import pandas as pd


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n, min_periods=n).mean()


def rma(s: pd.Series, n: int) -> pd.Series:
    """Media de Wilder (usada por RSI, ATR y ADX)."""
    return s.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    delta = close.diff()
    sube = rma(delta.clip(lower=0), n)
    baja = rma(-delta.clip(upper=0), n)
    rs = sube / baja.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(100.0).where(baja.notna())


def true_range(df: pd.DataFrame) -> pd.Series:
    prev = df["close"].shift(1)
    return pd.concat([df["high"] - df["low"],
                      (df["high"] - prev).abs(),
                      (df["low"] - prev).abs()], axis=1).max(axis=1)


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    return rma(true_range(df), n)


def bollinger(close: pd.Series, n: int = 20, k: float = 2.0):
    media = sma(close, n)
    desv = close.rolling(n, min_periods=n).std(ddof=0)
    return media - k * desv, media, media + k * desv


def adx(df: pd.DataFrame, n: int = 14) -> pd.Series:
    sube = df["high"].diff()
    baja = -df["low"].diff()
    dm_mas = pd.Series(np.where((sube > baja) & (sube > 0), sube, 0.0), index=df.index)
    dm_menos = pd.Series(np.where((baja > sube) & (baja > 0), baja, 0.0), index=df.index)
    tr = rma(true_range(df), n)
    di_mas = 100 * rma(dm_mas, n) / tr
    di_menos = 100 * rma(dm_menos, n) / tr
    dx = 100 * (di_mas - di_menos).abs() / (di_mas + di_menos).replace(0, np.nan)
    return rma(dx, n)
