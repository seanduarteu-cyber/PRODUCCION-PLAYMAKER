"""Métricas de rendimiento de un conjunto de operaciones."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd


def calcular_metricas(ops: pd.DataFrame, curva: pd.Series, capital_inicial: float) -> dict:
    """`curva` es el capital marcado a mercado en cada vela (índice = tiempo)."""
    dias = max((curva.index[-1] - curva.index[0]).total_seconds() / 86400, 1e-9) if len(curva) > 1 else 1.0
    base = {"operaciones": 0, "por_dia": 0.0, "aciertos": 0.0, "ganancia_media_r": 0.0,
            "perdida_media_r": 0.0, "esperanza_r": 0.0, "factor_beneficio": 0.0,
            "retorno": 0.0, "retorno_sin_comisiones": 0.0, "caida_max": 0.0,
            "comisiones": 0.0, "sharpe": 0.0, "dias": dias}
    if ops is None or len(ops) == 0:
        return base

    gan = ops[ops["pnl"] > 0]
    per = ops[ops["pnl"] <= 0]
    perdida_total = -per["pnl"].sum()
    pf = gan["pnl"].sum() / perdida_total if perdida_total > 0 else math.inf

    dd = float((curva / curva.cummax() - 1).min()) if len(curva) else 0.0
    diario = curva.resample("1D").last().pct_change().dropna()
    sharpe = float(diario.mean() / diario.std() * np.sqrt(365)) if len(diario) > 2 and diario.std() > 0 else 0.0

    base.update({
        "operaciones": int(len(ops)),
        "por_dia": len(ops) / dias,
        "aciertos": len(gan) / len(ops),
        "ganancia_media_r": float(gan["r"].mean()) if len(gan) else 0.0,
        "perdida_media_r": float(per["r"].mean()) if len(per) else 0.0,
        "esperanza_r": float(ops["r"].mean()),
        "factor_beneficio": float(pf),
        "retorno": float(curva.iloc[-1] / capital_inicial - 1),
        "retorno_sin_comisiones": float(ops["bruto"].sum() / capital_inicial),
        "caida_max": -dd,
        "comisiones": float(ops["comisiones"].sum()),
        "sharpe": sharpe,
    })
    return base
