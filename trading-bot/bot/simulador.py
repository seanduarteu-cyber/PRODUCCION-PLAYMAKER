"""Simulador de ejecución vela a vela para un par.

Lo usan el backtest y el modo `paper`, para que ambos llenen órdenes con las mismas reglas.
Las reglas son conservadoras a propósito:

* Orden límite: se llena como maker solo si el precio ATRAVIESA el límite (no basta con tocarlo).
  Si la vela abre ya cruzando el límite, se llena al precio de apertura como taker.
* Orden a mercado: se llena en la apertura de la vela siguiente + deslizamiento, como taker.
* Si en la misma vela se alcanzan el stop y el objetivo, se asume que saltó el STOP.
* En la vela en que se llena la entrada solo se revisa el stop (no el objetivo).
* Stop: sale como taker al stop - deslizamiento, o a la apertura si la vela abre más allá.
* Objetivo: orden límite que espera en el libro (maker), se llena si el precio lo atraviesa.
* Cierre por tiempo: tras `velas_max_en_operacion` velas sale a mercado al cierre (taker).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from .estrategias.base import Senal


@dataclass
class Orden:
    senal: Senal
    qty: float
    riesgo_usdt: float
    tipo: str              # "limit" | "market"
    velas_restantes: int
    t_senal: pd.Timestamp


@dataclass
class Posicion:
    lado: int
    entrada: float
    stop: float
    objetivo: float
    qty: float
    riesgo_usdt: float
    comision_entrada: float
    t_entrada: pd.Timestamp
    estrategia: str
    velas: int = 0


@dataclass
class SimuladorPar:
    costos: dict
    ejecucion: dict
    capital: float
    par: str = ""
    orden: Orden | None = None
    pos: Posicion | None = None
    operaciones: list = field(default_factory=list)

    @property
    def libre(self) -> bool:
        return self.orden is None and self.pos is None

    def colocar(self, senal: Senal, qty: float, riesgo_usdt: float, t: pd.Timestamp) -> None:
        if not self.libre or qty <= 0:
            return
        tipo = self.ejecucion.get("tipo_entrada", "limit")
        validez = 1 if tipo == "market" else self.ejecucion["velas_validez_entrada"]
        self.orden = Orden(senal, qty, riesgo_usdt, tipo, validez, t)

    def equity(self, precio: float) -> float:
        if self.pos is None:
            return self.capital
        p = self.pos
        return self.capital + p.lado * p.qty * (precio - p.entrada) - p.comision_entrada

    # ------------------------------------------------------------------
    def procesar_vela(self, t, o: float, h: float, l: float, c: float) -> list[dict]:
        """Avanza una vela. Devuelve las operaciones cerradas en ella."""
        cerradas: list[dict] = []
        recien_abierta = False

        if self.orden is not None and self.pos is None:
            recien_abierta = self._intentar_llenar(t, o, h, l)

        if self.pos is not None:
            op = self._revisar_salida(t, o, h, l, c, solo_stop=recien_abierta)
            if op:
                cerradas.append(op)
        return cerradas

    def cerrar_a_mercado(self, t, precio: float, motivo: str = "fin") -> dict | None:
        if self.pos is None:
            return None
        slip = self.costos["deslizamiento"]
        salida = precio * (1 - slip) if self.pos.lado == 1 else precio * (1 + slip)
        return self._cerrar(t, salida, self.costos["comision_taker"], motivo)

    # ------------------------------------------------------------------
    def _intentar_llenar(self, t, o, h, l) -> bool:
        od, s = self.orden, self.orden.senal
        maker, taker, slip = (self.costos["comision_maker"], self.costos["comision_taker"],
                              self.costos["deslizamiento"])
        precio = comision = None

        if od.tipo == "market":
            precio = o * (1 + slip) if s.lado == 1 else o * (1 - slip)
            comision = taker
        elif s.lado == 1:
            # Si la vela abre justo en el límite, la orden queda esperando en el libro (maker);
            # solo es taker si abre claramente por debajo (la orden ya cruza el precio).
            if o < s.entrada:
                precio, comision = o, taker
            elif l < s.entrada:
                precio, comision = s.entrada, maker
        else:
            if o > s.entrada:
                precio, comision = o, taker
            elif h > s.entrada:
                precio, comision = s.entrada, maker

        if precio is None:
            od.velas_restantes -= 1
            if od.velas_restantes <= 0:
                self.orden = None
            return False

        # Si el precio de llenado ya está más allá del stop, la operación no tiene sentido: se descarta.
        if (s.lado == 1 and precio <= s.stop) or (s.lado == -1 and precio >= s.stop):
            self.orden = None
            return False

        self.pos = Posicion(s.lado, precio, s.stop, s.objetivo, od.qty, od.riesgo_usdt,
                            od.qty * precio * comision, t, s.estrategia)
        self.orden = None
        return True

    def _revisar_salida(self, t, o, h, l, c, solo_stop: bool) -> dict | None:
        p = self.pos
        maker, taker, slip = (self.costos["comision_maker"], self.costos["comision_taker"],
                              self.costos["deslizamiento"])
        if p.lado == 1:
            if o <= p.stop:
                return self._cerrar(t, o * (1 - slip), taker, "stop")
            if l <= p.stop:
                return self._cerrar(t, p.stop * (1 - slip), taker, "stop")
            if not solo_stop and h > p.objetivo:
                return self._cerrar(t, p.objetivo, maker, "objetivo")
        else:
            if o >= p.stop:
                return self._cerrar(t, o * (1 + slip), taker, "stop")
            if h >= p.stop:
                return self._cerrar(t, p.stop * (1 + slip), taker, "stop")
            if not solo_stop and l < p.objetivo:
                return self._cerrar(t, p.objetivo, maker, "objetivo")

        p.velas += 1
        if p.velas >= self.ejecucion["velas_max_en_operacion"]:
            return self.cerrar_a_mercado(t, c, "tiempo")
        return None

    def _cerrar(self, t, salida: float, comision: float, motivo: str) -> dict:
        p = self.pos
        bruto = p.lado * p.qty * (salida - p.entrada)
        com_salida = p.qty * salida * comision
        comisiones = p.comision_entrada + com_salida
        neto = bruto - comisiones
        self.capital += neto
        op = {
            "par": self.par, "estrategia": p.estrategia,
            "lado": "LARGO" if p.lado == 1 else "CORTO",
            "t_entrada": p.t_entrada, "t_salida": t,
            "entrada": p.entrada, "salida": salida, "stop": p.stop, "objetivo": p.objetivo,
            "qty": p.qty, "bruto": bruto, "comisiones": comisiones, "pnl": neto,
            "r": neto / p.riesgo_usdt if p.riesgo_usdt else 0.0,
            "motivo": motivo, "capital": self.capital,
        }
        self.operaciones.append(op)
        self.pos = None
        return op
