"""Backtest vela a vela de una estrategia sobre un par."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from . import estrategias
from .estrategias.base import Senal
from .metricas import calcular_metricas
from .riesgo import ControlRiesgo, tamano_posicion
from .simulador import SimuladorPar


@dataclass
class Resultado:
    operaciones: pd.DataFrame
    curva: pd.Series
    metricas: dict
    kill_switch: bool


def cargar_velas(ruta: str | Path) -> pd.DataFrame:
    df = pd.read_csv(ruta, parse_dates=["time"])
    df["time"] = pd.to_datetime(df["time"], utc=True)
    return df.set_index("time").sort_index()


def remuestrear(df: pd.DataFrame, tf: str) -> pd.DataFrame:
    """Arma velas más largas (15m, 1h, 4h...) a partir de velas cortas."""
    regla = tf.replace("m", "min")
    out = df.resample(regla, label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
    return out.dropna()


def _utc(x) -> pd.Timestamp:
    t = pd.Timestamp(x)
    return t.tz_localize("UTC") if t.tzinfo is None else t.tz_convert("UTC")


def ejecutar(df: pd.DataFrame, senales: pd.DataFrame, cfg: dict, par: str = "",
             desde=None, hasta=None) -> Resultado:
    """Simula la estrategia entre `desde` y `hasta` (las señales ya vienen calculadas con
    todo el histórico previo, así que los indicadores están "calientes" al empezar)."""
    r = cfg["riesgo"]
    capital0 = r["capital_inicial"]
    sim = SimuladorPar(cfg["costos"], cfg["ejecucion"], capital0, par=par)
    ctrl = ControlRiesgo(r["perdida_diaria_max"], r["caida_max"], 1)

    idx = df.index
    i0 = 0 if desde is None else idx.searchsorted(_utc(desde))
    i1 = len(idx) if hasta is None else idx.searchsorted(_utc(hasta))
    o, h, l, c = (df[k].to_numpy() for k in ("open", "high", "low", "close"))
    sen = senales["senal"].to_numpy()
    ent, stp, obj = (senales[k].to_numpy() for k in ("entrada", "stop", "objetivo"))
    nombre = senales.attrs.get("estrategia", "")

    curva = np.empty(max(i1 - i0, 0))
    for k, i in enumerate(range(i0, i1)):
        t = idx[i]
        sim.procesar_vela(t, o[i], h[i], l[i], c[i])
        eq = sim.equity(c[i])
        ctrl.actualizar(eq, t)
        if sen[i] != 0 and sim.libre and i < i1 - 1:
            ok, _ = ctrl.puede_operar(eq)
            if ok:
                qty = tamano_posicion(eq, ent[i], stp[i], r["riesgo_por_operacion"], r["apalancamiento_max"])
                riesgo_usdt = qty * abs(ent[i] - stp[i])
                sim.colocar(Senal(int(sen[i]), ent[i], stp[i], obj[i], nombre), qty, riesgo_usdt, t)
        curva[k] = eq

    if sim.pos is not None and i1 > i0:
        sim.cerrar_a_mercado(idx[i1 - 1], c[i1 - 1], "fin")
        curva[-1] = sim.capital

    serie = pd.Series(curva, index=idx[i0:i1])
    ops = pd.DataFrame(sim.operaciones)
    m = calcular_metricas(ops, serie, capital0)
    m["kill_switch"] = ctrl.apagado
    return Resultado(ops, serie, m, ctrl.apagado)


def senales_de(nombre: str, df: pd.DataFrame, params: dict) -> pd.DataFrame:
    s = estrategias.calcular(nombre, df, params)
    s.attrs["estrategia"] = nombre
    return s


def combinar(resultados: list[Resultado], capital_por_par: float) -> dict:
    """Métricas de cartera: cada par opera con su propio capital y se suman las curvas."""
    ops = pd.concat([r.operaciones for r in resultados if len(r.operaciones)], ignore_index=True) \
        if any(len(r.operaciones) for r in resultados) else pd.DataFrame()
    curvas = pd.concat([r.curva for r in resultados], axis=1).ffill().bfill()
    total = curvas.sum(axis=1)
    m = calcular_metricas(ops, total, capital_por_par * len(resultados))
    m["kill_switch"] = sum(r.kill_switch for r in resultados)
    return m
