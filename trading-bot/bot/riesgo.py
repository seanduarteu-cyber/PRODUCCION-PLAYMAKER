"""Gestión de riesgo: tamaño de posición, límite de pérdida diaria y kill switch.

Lo usan igual el backtest y el bot en vivo.
"""
from __future__ import annotations

from datetime import date

import pandas as pd


def tamano_posicion(capital: float, entrada: float, stop: float,
                    riesgo_pct: float, apalancamiento_max: float) -> float:
    """Cantidad (en monedas) para perder `riesgo_pct` del capital si salta el stop.

    Se limita para que el nocional no supere `apalancamiento_max` veces el capital.
    """
    dist = abs(entrada - stop)
    if dist <= 0 or capital <= 0 or entrada <= 0:
        return 0.0
    qty_riesgo = capital * riesgo_pct / dist
    qty_max = capital * apalancamiento_max / entrada
    return min(qty_riesgo, qty_max)


class ControlRiesgo:
    """Bloquea nuevas entradas si se pierde demasiado en el día o desde el máximo."""

    def __init__(self, perdida_diaria_max: float, caida_max: float, max_posiciones: int = 1):
        self.perdida_diaria_max = perdida_diaria_max
        self.caida_max = caida_max
        self.max_posiciones = max_posiciones
        self.pico: float | None = None
        self.dia: date | None = None
        self.capital_inicio_dia: float | None = None
        self.apagado = False
        self.motivo_apagado = ""

    @classmethod
    def desde_config(cls, riesgo: dict) -> "ControlRiesgo":
        return cls(riesgo["perdida_diaria_max"], riesgo["caida_max"], riesgo.get("max_posiciones", 1))

    def actualizar(self, capital: float, ahora: pd.Timestamp) -> None:
        ts = pd.Timestamp(ahora)
        dia = (ts.tz_convert("UTC") if ts.tzinfo else ts).date()
        if self.dia != dia:
            self.dia = dia
            self.capital_inicio_dia = capital
        self.pico = capital if self.pico is None else max(self.pico, capital)
        if not self.apagado and capital <= self.pico * (1 - self.caida_max):
            self.apagado = True
            self.motivo_apagado = (f"KILL SWITCH: caída de {1 - capital / self.pico:.1%} desde el máximo "
                                   f"({self.pico:.2f} -> {capital:.2f})")

    def puede_operar(self, capital: float, abiertas: int = 0) -> tuple[bool, str]:
        if self.apagado:
            return False, self.motivo_apagado
        if self.capital_inicio_dia and capital <= self.capital_inicio_dia * (1 - self.perdida_diaria_max):
            return False, "límite de pérdida diaria alcanzado; se reanuda mañana (UTC)"
        if abiertas >= self.max_posiciones:
            return False, "máximo de posiciones abiertas"
        return True, ""

    # Persistencia para el bot en vivo
    def a_dict(self) -> dict:
        return {"pico": self.pico, "dia": self.dia.isoformat() if self.dia else None,
                "capital_inicio_dia": self.capital_inicio_dia,
                "apagado": self.apagado, "motivo_apagado": self.motivo_apagado}

    def cargar_dict(self, d: dict) -> None:
        self.pico = d.get("pico")
        self.dia = date.fromisoformat(d["dia"]) if d.get("dia") else None
        self.capital_inicio_dia = d.get("capital_inicio_dia")
        self.apagado = d.get("apagado", False)
        self.motivo_apagado = d.get("motivo_apagado", "")
