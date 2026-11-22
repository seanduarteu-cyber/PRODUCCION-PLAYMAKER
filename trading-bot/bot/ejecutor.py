"""Bot en vivo: lee velas, genera señales, aplica el riesgo y opera.

Hay dos ejecutores con la misma lógica de señales y riesgo:
  * EjecutorPaper:    simula las órdenes con SimuladorPar (las mismas reglas que el backtest)
                      sobre precios reales. No necesita claves.
  * EjecutorExchange: envía órdenes reales a Binance (cuenta demo o real). El stop loss y el
                      take profit quedan puestos EN LA EXCHANGE apenas se llena la entrada.
"""
from __future__ import annotations

import csv
import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

from . import estrategias
from .riesgo import ControlRiesgo, tamano_posicion
from .simulador import SimuladorPar

log = logging.getLogger("bot")

def tf_a_ms(tf: str) -> int:
    unidades = {"m": 60, "h": 3600, "d": 86400}
    return int(tf[:-1]) * unidades[tf[-1]] * 1000


CAMPOS_OPERACION = ["par", "estrategia", "lado", "t_entrada", "t_salida", "entrada", "salida",
                    "stop", "objetivo", "qty", "bruto", "comisiones", "pnl", "r", "motivo", "capital"]


def avisar(msg: str) -> None:
    """Registra el mensaje y, si hay TELEGRAM_TOKEN y TELEGRAM_CHAT_ID en el .env, lo envía."""
    log.info(msg)
    token, chat = os.getenv("TELEGRAM_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    if token and chat:
        try:
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          json={"chat_id": chat, "text": msg}, timeout=10)
        except requests.RequestException as e:
            log.warning("No se pudo enviar a Telegram: %s", e)


class BotBase:
    def __init__(self, cfg: dict, conexion, modo: str, carpeta_logs: str | Path = "logs"):
        self.cfg = cfg
        self.cx = conexion
        self.modo = modo
        self.tf = cfg["temporalidad"]
        self.tf_ms = tf_a_ms(self.tf)
        # Historial suficiente para que las EMA largas converjan igual que en el backtest.
        self.n_velas = cfg["ejecucion"].get("velas_historial", 1500)
        self.pares = cfg["pares"]
        self.activas = cfg["estrategias_activas"]
        self.r = cfg["riesgo"]
        self.ctrl = ControlRiesgo.desde_config(self.r)
        self.logs = Path(carpeta_logs)
        self.logs.mkdir(exist_ok=True)
        self.ruta_estado = self.logs / f"estado_{modo}.json"
        self.ruta_ops = self.logs / f"operaciones_{modo}.csv"
        self.ultima_vela: dict[str, int] = {}   # par -> ms de apertura de la última vela procesada

    # ------------------------------------------------------------ comunes
    def senal(self, df: pd.DataFrame):
        for nombre in self.activas:
            s = estrategias.ultima_senal(nombre, df, self.cfg["parametros"][nombre])
            if s is not None:
                return s
        return None

    def registrar_operacion(self, op: dict) -> None:
        nuevo = not self.ruta_ops.exists()
        with open(self.ruta_ops, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CAMPOS_OPERACION, extrasaction="ignore")
            if nuevo:
                w.writeheader()
            w.writerow({k: (v.isoformat() if hasattr(v, "isoformat") else v) for k, v in op.items()})
        avisar(f"[{self.modo}] CERRADA {op['par']} {op['lado']} {op['estrategia']}: "
               f"{op['pnl']:+.2f} USDT ({op['r']:+.2f}R, {op['motivo']}) | capital {op['capital']:.2f}")

    def pares_con_vela_pendiente(self) -> list[str]:
        """Pares cuya última vela cerrada todavía no se procesó (evita pedir velas cada 10 s)."""
        esperada = (self.cx.ahora_ms() // self.tf_ms - 1) * self.tf_ms
        return [p for p in self.pares if self.ultima_vela.get(p) != esperada]

    def vela_nueva(self, par: str, df: pd.DataFrame) -> bool:
        if df.empty:
            return False
        ultima = int(df.index[-1].value // 10**6)
        if self.ultima_vela.get(par) == ultima:
            return False
        self.ultima_vela[par] = ultima
        return True

    def ejecutar(self, una_vez: bool = False) -> None:
        avisar(f"Bot iniciado en modo {self.modo.upper()} | pares: {', '.join(self.pares)} | "
               f"estrategias: {', '.join(self.activas)}")
        espera = self.cfg["ejecucion"].get("segundos_entre_chequeos", 10)
        while True:
            try:
                self.ciclo()
            except KeyboardInterrupt:
                raise
            except Exception as e:  # el bot no debe morir por un error de red puntual
                log.exception("Error en el ciclo: %s", e)
            if una_vez:
                return
            time.sleep(espera)


# =====================================================================
class EjecutorPaper(BotBase):
    """Simulación en vivo con precios reales y las mismas reglas de llenado que el backtest."""

    def __init__(self, cfg, conexion, carpeta_logs="logs"):
        super().__init__(cfg, conexion, "paper", carpeta_logs)
        capital_par = self.r["capital_inicial"] / len(self.pares)
        self.sims = {p: SimuladorPar(cfg["costos"], cfg["ejecucion"], capital_par, par=p) for p in self.pares}

    def capital(self, precios: dict | None = None) -> float:
        precios = precios or {}
        return sum(s.equity(precios[p]) if p in precios else s.capital for p, s in self.sims.items())

    def ciclo(self) -> None:
        precios = {}
        for par in self.pares_con_vela_pendiente():
            df = self.cx.velas(par, self.tf, self.n_velas)
            if not self.vela_nueva(par, df):
                continue
            sim = self.sims[par]
            v = df.iloc[-1]
            t = df.index[-1]
            for op in sim.procesar_vela(t, v.open, v.high, v.low, v.close):
                op["capital"] = self.capital()
                self.registrar_operacion(op)
            precios[par] = v.close

            capital = self.capital(precios)
            self.ctrl.actualizar(capital, t)
            if not sim.libre:
                continue
            s = self.senal(df)
            if s is None:
                continue
            abiertas = sum(not x.libre for x in self.sims.values())
            ok, motivo = self.ctrl.puede_operar(capital, abiertas)
            if not ok:
                log.info("Señal %s %s ignorada: %s", par, s.lado_txt, motivo)
                continue
            qty = tamano_posicion(capital, s.entrada, s.stop, self.r["riesgo_por_operacion"],
                                  self.r["apalancamiento_max"])
            sim.colocar(s, qty, qty * abs(s.entrada - s.stop), t)
            avisar(f"[paper] ORDEN {par} {s.lado_txt} {s.estrategia}: entrada {s.entrada:.6g} "
                   f"stop {s.stop:.6g} objetivo {s.objetivo:.6g} qty {qty:.6g}")


# =====================================================================
class EjecutorExchange(BotBase):
    """Opera en Binance (demo o real) con órdenes de verdad."""

    def __init__(self, cfg, conexion, modo: str, carpeta_logs="logs"):
        super().__init__(cfg, conexion, modo, carpeta_logs)
        self.estado = {p: {"fase": "libre"} for p in self.pares}
        self._cargar_estado()
        for par in self.pares:
            self.cx.preparar_par(par, self.r["apalancamiento_max"], self.r.get("margen", "isolated"))

    # ----------------------------------------------------------- estado
    def _cargar_estado(self) -> None:
        if self.ruta_estado.exists():
            d = json.loads(self.ruta_estado.read_text(encoding="utf-8"))
            self.estado.update({p: e for p, e in d.get("pares", {}).items() if p in self.estado})
            self.ctrl.cargar_dict(d.get("riesgo", {}))
            self.ultima_vela = d.get("ultima_vela", {})
            log.info("Estado recuperado de %s", self.ruta_estado)

    def _guardar_estado(self) -> None:
        tmp = self.ruta_estado.with_suffix(".tmp")
        tmp.write_text(json.dumps({"pares": self.estado, "riesgo": self.ctrl.a_dict(),
                                   "ultima_vela": self.ultima_vela}, indent=2, default=str),
                       encoding="utf-8")
        tmp.replace(self.ruta_estado)

    # ------------------------------------------------------------ ciclo
    def ciclo(self) -> None:
        capital = self.cx.capital()
        self.ctrl.actualizar(capital, pd.Timestamp.now(tz="UTC"))
        for par in self.pares:
            self._revisar_ordenes(par)
        for par in self.pares_con_vela_pendiente():
            df = self.cx.velas(par, self.tf, self.n_velas)
            if self.vela_nueva(par, df):
                self._al_cerrar_vela(par, df, capital)
        self._guardar_estado()

    def _revisar_ordenes(self, par: str) -> None:
        """Se ejecuta cada pocos segundos: detecta entradas llenadas y posiciones cerradas."""
        st = self.estado[par]
        if st["fase"] == "entrada_pendiente":
            o = self.cx.orden(par, st["orden_id"])
            if o["estado"] == "closed" or (o["estado"] in ("canceled", "expired") and o["llenado"] > 0):
                self._proteger(par, o["llenado"], o["precio_medio"])
            elif o["estado"] in ("canceled", "expired", "rejected"):
                log.info("%s: orden de entrada %s sin llenar (%s)", par, st["orden_id"], o["estado"])
                self.estado[par] = {"fase": "libre"}

        elif st["fase"] == "en_posicion":
            if self.cx.posicion(par) is None:          # la cerró el stop o el take profit
                self.cx.cancelar_todo(par)              # retira la protección que sobró
                self._cerrar_registro(par, "stop/objetivo")

    def _proteger(self, par: str, qty: float, precio: float) -> None:
        st = self.estado[par]
        s = st["senal"]
        stop_id, tp_id = self.cx.proteger(par, s["lado"], qty, s["stop"], s["objetivo"])
        st.update(fase="en_posicion", qty=qty, entrada_real=precio, stop_id=stop_id, tp_id=tp_id,
                  velas_en_pos=0)
        avisar(f"[{self.modo}] ABIERTA {par} {'LARGO' if s['lado'] == 1 else 'CORTO'} {s['estrategia']}: "
               f"{qty} @ {precio:.6g} | stop {s['stop']:.6g} | objetivo {s['objetivo']:.6g}")

    def _cerrar_registro(self, par: str, motivo: str) -> None:
        st = self.estado[par]
        s = st["senal"]
        res = self.cx.resultado_desde(par, st["t_orden_ms"])
        salida = res["salida"] or 0.0
        if motivo == "stop/objetivo" and salida:
            motivo = "objetivo" if (salida - st["entrada_real"]) * s["lado"] > 0 else "stop"
        bruto = res["pnl"] + res["comisiones"]
        self.registrar_operacion({
            "par": par, "estrategia": s["estrategia"], "lado": "LARGO" if s["lado"] == 1 else "CORTO",
            "t_entrada": datetime.fromtimestamp(st["t_orden_ms"] / 1000, timezone.utc),
            "t_salida": datetime.now(timezone.utc), "entrada": st["entrada_real"], "salida": salida,
            "stop": s["stop"], "objetivo": s["objetivo"], "qty": st["qty"], "bruto": bruto,
            "comisiones": res["comisiones"], "pnl": res["pnl"],
            "r": res["pnl"] / st["riesgo_usdt"] if st.get("riesgo_usdt") else 0.0,
            "motivo": motivo, "capital": self.cx.capital(),
        })
        self.estado[par] = {"fase": "libre"}

    def _al_cerrar_vela(self, par: str, df: pd.DataFrame, capital: float) -> None:
        st = self.estado[par]
        ej = self.cfg["ejecucion"]

        if st["fase"] == "entrada_pendiente":
            st["velas_espera"] = st.get("velas_espera", 0) + 1
            if st["velas_espera"] >= ej["velas_validez_entrada"]:
                self.cx.cancelar(par, st["orden_id"])   # la próxima revisión ve si hubo llenado parcial
            return

        if st["fase"] == "en_posicion":
            st["velas_en_pos"] = st.get("velas_en_pos", 0) + 1
            if st["velas_en_pos"] >= ej["velas_max_en_operacion"]:
                pos = self.cx.posicion(par)
                self.cx.cancelar_todo(par)
                if pos:
                    self.cx.cerrar_mercado(par, pos["lado"], pos["qty"])
                self._cerrar_registro(par, "tiempo")
            return

        # fase libre: ¿hay señal?
        if self.cx.posicion(par) is not None:
            log.warning("%s: hay una posición abierta que el bot no abrió; no la toca.", par)
            return
        s = self.senal(df)
        if s is None:
            return
        abiertas = sum(e["fase"] != "libre" for e in self.estado.values())
        ok, motivo = self.ctrl.puede_operar(capital, abiertas)
        if not ok:
            log.info("Señal %s %s ignorada: %s", par, s.lado_txt, motivo)
            return
        qty = tamano_posicion(capital, s.entrada, s.stop, self.r["riesgo_por_operacion"],
                              self.r["apalancamiento_max"])
        qty, precio = self.cx.cantidad(par, qty), self.cx.precio(par, s.entrada)
        stop, objetivo = self.cx.precio(par, s.stop), self.cx.precio(par, s.objetivo)
        valido, motivo = self.cx.minimo_ok(par, qty, precio)
        if not valido:
            log.info("Señal %s ignorada: %s (sube el capital o el riesgo por operación)", par, motivo)
            return
        t_orden_ms = self.cx.ahora_ms() - 5_000
        if ej.get("tipo_entrada", "limit") == "market":
            orden_id = self.cx.entrada_mercado(par, s.lado, qty)
        else:
            orden_id = self.cx.entrada_limite(par, s.lado, qty, precio)
        self.estado[par] = {
            "fase": "entrada_pendiente", "orden_id": orden_id, "velas_espera": 0,
            "t_orden_ms": t_orden_ms, "riesgo_usdt": qty * abs(precio - stop),
            "senal": {"lado": s.lado, "entrada": precio, "stop": stop, "objetivo": objetivo,
                      "estrategia": s.estrategia},
        }
        avisar(f"[{self.modo}] ORDEN {par} {s.lado_txt} {s.estrategia}: {qty} @ {precio:.6g} "
               f"| stop {stop:.6g} | objetivo {objetivo:.6g}")
