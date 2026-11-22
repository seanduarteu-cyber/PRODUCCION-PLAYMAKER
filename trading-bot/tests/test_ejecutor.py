"""Pruebas del bot en vivo con una exchange falsa (sin red)."""
import copy
from unittest.mock import MagicMock

import pandas as pd
import pytest

from bot.backtester import ejecutar, senales_de
from bot.ejecutor import EjecutorExchange, EjecutorPaper
from bot.estrategias.base import Senal
from bot.exchange import ConexionBinance


class ReplayVelas:
    """Sirve velas históricas como si fueran en vivo, avanzando el reloj vela a vela."""

    def __init__(self, df: pd.DataFrame, inicio: int):
        self.df = df
        self.i = inicio                      # índice de la próxima vela que "cierra"

    def ahora_ms(self) -> int:
        # 1 s después del cierre de la vela i-1 (= apertura de la vela i)
        return int(self.df.index[self.i - 1].value // 10**6) + 300_000 + 1000

    def velas(self, par, tf, n=500):
        return self.df.iloc[max(0, self.i - n):self.i]


def test_paper_hace_las_mismas_operaciones_que_el_backtest(velas, cfg, tmp_path):
    cfg = copy.deepcopy(cfg)
    par = "BTC/USDT:USDT"
    cfg["pares"] = [par]
    cfg["estrategias_activas"] = ["ema_pullback"]
    cfg["riesgo"]["max_posiciones"] = 1

    inicio = 1000
    desde = velas.index[inicio]
    bt = ejecutar(velas, senales_de("ema_pullback", velas, cfg["parametros"]["ema_pullback"]),
                  cfg, par, desde=desde)
    assert len(bt.operaciones) > 5

    cx = ReplayVelas(velas, inicio + 1)
    bot = EjecutorPaper(cfg, cx, tmp_path)
    for i in range(inicio + 1, len(velas) + 1):
        cx.i = i
        bot.ciclo()
        bot.ciclo()          # un segundo chequeo en la misma vela no debe duplicar nada

    paper = bot.sims[par].operaciones
    # el backtest cierra la última posición al final; el paper la deja abierta
    bt_ops = bt.operaciones[bt.operaciones.motivo != "fin"]
    assert len(paper) == len(bt_ops)
    for a, b in zip(paper, bt_ops.to_dict("records")):
        assert a["t_entrada"] == b["t_entrada"] and a["motivo"] == b["motivo"]
        assert a["pnl"] == pytest.approx(b["pnl"])
    assert (tmp_path / "operaciones_paper.csv").exists()


class ExchangeFalsa:
    def __init__(self, df):
        self.df = df
        self.t = int(df.index[-1].value // 10**6) + 300_000 + 1000
        self.ordenes = {}
        self.pos = None
        self.protecciones = []
        self.cancelado_todo = 0
        self.saldo = 1000.0

    def ahora_ms(self): return self.t
    def velas(self, par, tf, n=500): return self.df
    def capital(self): return self.saldo
    def preparar_par(self, *a): pass
    def posicion(self, par): return self.pos
    def cantidad(self, par, q): return round(q, 3)
    def precio(self, par, p): return round(p, 2)
    def minimo_ok(self, par, q, p): return (q * p >= 5, "nocional bajo")

    def entrada_limite(self, par, lado, qty, precio):
        self.ordenes["1"] = {"estado": "open", "llenado": 0.0, "precio_medio": 0.0}
        self.ultima_entrada = (lado, qty, precio)
        return "1"

    def orden(self, par, oid): return self.ordenes[oid]
    def cancelar(self, par, oid): self.ordenes[oid]["estado"] = "canceled"

    def proteger(self, par, lado, qty, stop, objetivo):
        self.protecciones.append((lado, qty, stop, objetivo))
        return "s1", "t1"

    def cancelar_todo(self, par): self.cancelado_todo += 1
    def cerrar_mercado(self, par, lado, qty): self.pos = None

    def resultado_desde(self, par, desde_ms):
        return {"pnl": 9.5, "comisiones": 0.5, "salida": 102.0}


def test_flujo_completo_demo(velas, cfg, tmp_path, monkeypatch):
    cfg = copy.deepcopy(cfg)
    par = "BTC/USDT:USDT"
    cfg["pares"] = [par]
    fx = ExchangeFalsa(velas.iloc[:500])
    bot = EjecutorExchange(cfg, fx, "demo", tmp_path)
    monkeypatch.setattr(bot, "senal", lambda df: Senal(1, 100.0, 99.0, 102.0, "ema_pullback"))

    bot.ciclo()                                   # vela nueva + señal -> orden límite
    assert bot.estado[par]["fase"] == "entrada_pendiente"
    lado, qty, precio = fx.ultima_entrada
    assert lado == 1 and precio == 100.0
    assert qty * (100 - 99) == pytest.approx(1000 * cfg["riesgo"]["riesgo_por_operacion"], rel=0.01)

    fx.ordenes["1"] = {"estado": "closed", "llenado": qty, "precio_medio": 100.0}
    fx.pos = {"lado": 1, "qty": qty, "entrada": 100.0}
    bot.ciclo()                                   # detecta llenado -> pone stop y TP en la exchange
    assert bot.estado[par]["fase"] == "en_posicion"
    assert fx.protecciones == [(1, qty, 99.0, 102.0)]

    fx.pos = None                                 # el take profit cerró la posición
    bot.ciclo()
    assert bot.estado[par]["fase"] == "libre"
    assert fx.cancelado_todo == 1                 # retiró el stop que sobraba
    ops = pd.read_csv(tmp_path / "operaciones_demo.csv")
    assert len(ops) == 1 and ops.motivo[0] == "objetivo" and ops.pnl[0] == pytest.approx(9.5)

    # el estado se guarda y se recupera al reiniciar
    bot2 = EjecutorExchange(cfg, fx, "demo", tmp_path)
    assert bot2.estado[par]["fase"] == "libre"
    assert bot2.ultima_vela == bot.ultima_vela


def test_entrada_que_no_se_llena_se_cancela(velas, cfg, tmp_path, monkeypatch):
    cfg = copy.deepcopy(cfg)
    par = "BTC/USDT:USDT"
    cfg["pares"] = [par]
    fx = ExchangeFalsa(velas.iloc[:500])
    bot = EjecutorExchange(cfg, fx, "demo", tmp_path)
    monkeypatch.setattr(bot, "senal", lambda df: Senal(1, 100.0, 99.0, 102.0, "ema_pullback"))
    bot.ciclo()
    for k in range(cfg["ejecucion"]["velas_validez_entrada"]):
        fx.df = velas.iloc[:501 + k]              # cierra una vela nueva
        fx.t += 300_000
        bot.ciclo()
    assert fx.ordenes["1"]["estado"] == "canceled"
    bot.ciclo()
    assert bot.estado[par]["fase"] == "libre"


def test_ordenes_de_proteccion_que_envia_a_binance():
    cx = object.__new__(ConexionBinance)
    cx.ex = MagicMock()
    cx.ex.create_order.return_value = {"id": 7}
    cx.proteger("BTC/USDT:USDT", 1, 0.01, 95000.0, 97000.0)
    stop, tp = cx.ex.create_order.call_args_list
    assert stop.args == ("BTC/USDT:USDT", "market", "sell", 0.01, None,
                         {"stopLossPrice": 95000.0, "reduceOnly": True})
    assert tp.args == ("BTC/USDT:USDT", "limit", "sell", 0.01, 97000.0, {"reduceOnly": True})
