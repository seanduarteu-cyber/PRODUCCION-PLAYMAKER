"""Conexión con Binance Futures USDⓈ-M a través de ccxt.

modo "paper": solo datos públicos (no necesita claves).
modo "demo":  cuenta Demo Trading de Binance (demo.binance.com), dinero ficticio.
modo "real":  cuenta real. Usa claves SIN permiso de retiro y con lista blanca de IP.
"""
from __future__ import annotations

import logging
import time

import ccxt
import pandas as pd

from .config import cargar_claves

log = logging.getLogger("bot")


class ConexionBinance:
    def __init__(self, modo: str):
        opciones = {"enableRateLimit": True,
                    "options": {"defaultType": "future", "adjustForTimeDifference": True}}
        if modo in ("demo", "real"):
            key, secret = cargar_claves(modo)
            opciones.update(apiKey=key, secret=secret)
        self.ex = ccxt.binanceusdm(opciones)
        if modo == "demo":
            self.ex.enable_demo_trading(True)
        self.modo = modo
        self.ex.load_markets()

    # ---------------------------------------------------------------- datos
    def velas(self, par: str, tf: str, n: int = 500) -> pd.DataFrame:
        """Velas CERRADAS (descarta la vela que todavía se está formando)."""
        filas = self.ex.fetch_ohlcv(par, tf, limit=n)
        df = pd.DataFrame(filas, columns=["ts", "open", "high", "low", "close", "volume"])
        dur_ms = self.ex.parse_timeframe(tf) * 1000
        ahora_ms = self.ex.milliseconds()
        df = df[df["ts"] + dur_ms <= ahora_ms]
        df["time"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
        return df.set_index("time")[["open", "high", "low", "close", "volume"]].astype(float)

    def ahora_ms(self) -> int:
        return self.ex.milliseconds()

    # --------------------------------------------------------------- cuenta
    def capital(self) -> float:
        bal = self.ex.fetch_balance()
        return float(bal.get("USDT", {}).get("total") or 0.0)

    def preparar_par(self, par: str, apalancamiento: int, margen: str) -> None:
        for accion in (lambda: self.ex.set_margin_mode(margen, par),
                       lambda: self.ex.set_leverage(int(apalancamiento), par)):
            try:
                accion()
            except ccxt.BaseError as e:      # p. ej. "No need to change margin type"
                log.debug("preparar_par %s: %s", par, e)

    def posicion(self, par: str) -> dict | None:
        for p in self.ex.fetch_positions([par]):
            qty = float(p.get("contracts") or 0)
            if qty > 0:
                return {"lado": 1 if p.get("side") == "long" else -1, "qty": qty,
                        "entrada": float(p.get("entryPrice") or 0)}
        return None

    # -------------------------------------------------------------- órdenes
    def cantidad(self, par: str, qty: float) -> float:
        return float(self.ex.amount_to_precision(par, qty))

    def precio(self, par: str, precio: float) -> float:
        return float(self.ex.price_to_precision(par, precio))

    def minimo_ok(self, par: str, qty: float, precio: float) -> tuple[bool, str]:
        lim = self.ex.market(par)["limits"]
        q_min = (lim.get("amount") or {}).get("min") or 0
        c_min = (lim.get("cost") or {}).get("min") or 0
        if qty < q_min:
            return False, f"cantidad {qty} < mínimo {q_min}"
        if qty * precio < c_min:
            return False, f"nocional {qty * precio:.2f} < mínimo {c_min} USDT"
        return True, ""

    def entrada_limite(self, par: str, lado: int, qty: float, precio: float) -> str:
        o = self.ex.create_order(par, "limit", "buy" if lado == 1 else "sell", qty, precio)
        return str(o["id"])

    def entrada_mercado(self, par: str, lado: int, qty: float) -> str:
        o = self.ex.create_order(par, "market", "buy" if lado == 1 else "sell", qty)
        return str(o["id"])

    def orden(self, par: str, orden_id: str) -> dict:
        o = self.ex.fetch_order(orden_id, par)
        return {"estado": o.get("status"), "llenado": float(o.get("filled") or 0),
                "precio_medio": float(o.get("average") or o.get("price") or 0)}

    def cancelar(self, par: str, orden_id: str) -> None:
        try:
            self.ex.cancel_order(orden_id, par)
        except ccxt.OrderNotFound:
            pass

    def proteger(self, par: str, lado: int, qty: float, stop: float, objetivo: float) -> tuple[str, str]:
        """Pone el stop loss (stop-market) y el take profit (límite) EN LA EXCHANGE,
        así la posición queda protegida aunque el bot se caiga."""
        cierre = "sell" if lado == 1 else "buy"
        o_stop = self.ex.create_order(par, "market", cierre, qty, None,
                                      {"stopLossPrice": stop, "reduceOnly": True})
        o_tp = self.ex.create_order(par, "limit", cierre, qty, objetivo, {"reduceOnly": True})
        return str(o_stop["id"]), str(o_tp["id"])

    def cancelar_todo(self, par: str) -> None:
        for params in ({}, {"trigger": True}):     # órdenes normales y condicionales (stops)
            try:
                self.ex.cancel_all_orders(par, params)
            except ccxt.BaseError as e:
                log.debug("cancelar_todo %s %s: %s", par, params, e)

    def cerrar_mercado(self, par: str, lado: int, qty: float) -> None:
        self.ex.create_order(par, "market", "sell" if lado == 1 else "buy", qty, None, {"reduceOnly": True})

    def resultado_desde(self, par: str, desde_ms: int) -> dict:
        """PnL realizado y comisiones de las ejecuciones del par desde `desde_ms`."""
        time.sleep(1)  # dar tiempo a que la exchange registre la ejecución
        trades = self.ex.fetch_my_trades(par, since=desde_ms)
        pnl = sum(float(t["info"].get("realizedPnl", 0)) for t in trades)
        comis = sum(float((t.get("fee") or {}).get("cost") or 0) for t in trades)
        salidas = [t for t in trades if float(t["info"].get("realizedPnl", 0)) != 0]
        precio_salida = salidas[-1]["price"] if salidas else None
        return {"pnl": pnl - comis, "comisiones": comis, "salida": precio_salida}
