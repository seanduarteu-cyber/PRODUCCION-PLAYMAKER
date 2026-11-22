import pandas as pd
import pytest

from bot.estrategias.base import Senal
from bot.simulador import SimuladorPar

COSTOS = {"comision_maker": 0.0002, "comision_taker": 0.0005, "deslizamiento": 0.0002}
EJEC = {"tipo_entrada": "limit", "velas_validez_entrada": 2, "velas_max_en_operacion": 5}
T = pd.Timestamp("2026-01-01", tz="UTC")


def sim_con_orden(lado=1, entrada=100.0, stop=99.0, objetivo=102.0, ejec=EJEC):
    s = SimuladorPar(COSTOS, ejec, 1000.0)
    s.colocar(Senal(lado, entrada, stop, objetivo, "x"), qty=1.0, riesgo_usdt=1.0, t=T)
    return s


def test_limite_solo_se_llena_si_el_precio_lo_atraviesa():
    s = sim_con_orden()
    s.procesar_vela(T, 100.5, 101, 100.0, 100.5)    # toca 100 pero no lo cruza
    assert s.pos is None and s.orden is not None
    s.procesar_vela(T, 100.5, 101, 99.9, 100.5)     # lo cruza -> maker a 100
    assert s.pos is not None and s.pos.entrada == 100.0
    assert s.pos.comision_entrada == pytest.approx(100.0 * 0.0002)


def test_limite_cruzado_en_la_apertura_es_taker_al_precio_de_apertura():
    s = sim_con_orden()
    s.procesar_vela(T, 99.8, 100.2, 99.5, 100.0)
    assert s.pos.entrada == 99.8
    assert s.pos.comision_entrada == pytest.approx(99.8 * 0.0005)


def test_orden_vence_si_no_se_llena():
    s = sim_con_orden()
    s.procesar_vela(T, 101, 102, 100.5, 101)
    s.procesar_vela(T, 101, 102, 100.5, 101)
    assert s.orden is None and s.pos is None


def test_stop_y_objetivo_en_la_misma_vela_cuenta_como_stop():
    s = sim_con_orden()
    s.procesar_vela(T, 100.5, 100.6, 99.95, 100.2)   # entra
    ops = s.procesar_vela(T, 100.2, 103.0, 98.5, 101)  # toca objetivo Y stop
    assert ops[0]["motivo"] == "stop"
    assert ops[0]["salida"] == pytest.approx(99.0 * (1 - 0.0002))


def test_en_la_vela_de_entrada_no_se_toma_el_objetivo():
    s = sim_con_orden()
    s.procesar_vela(T, 100.5, 103.0, 99.95, 102.5)  # entra y el máximo supera el objetivo
    assert s.pos is not None


def test_objetivo_es_maker_y_calcula_pnl_neto():
    s = sim_con_orden()
    s.procesar_vela(T, 100.5, 100.6, 99.95, 100.2)
    op = s.procesar_vela(T, 100.2, 102.5, 100.1, 102.2)[0]
    assert op["motivo"] == "objetivo" and op["salida"] == 102.0
    comis = 100 * 0.0002 + 102 * 0.0002
    assert op["comisiones"] == pytest.approx(comis)
    assert op["pnl"] == pytest.approx(2.0 - comis)
    assert s.capital == pytest.approx(1000 + 2.0 - comis)


def test_gap_mas_alla_del_stop_sale_en_la_apertura():
    s = sim_con_orden()
    s.procesar_vela(T, 100.5, 100.6, 99.95, 100.2)
    op = s.procesar_vela(T, 98.0, 98.5, 97.5, 98.2)[0]
    assert op["salida"] == pytest.approx(98.0 * (1 - 0.0002))


def test_corto_simetrico():
    s = sim_con_orden(lado=-1, entrada=100.0, stop=101.0, objetivo=98.0)
    s.procesar_vela(T, 99.5, 100.05, 99.4, 99.8)
    op = s.procesar_vela(T, 99.8, 99.9, 97.9, 98.1)[0]
    assert op["motivo"] == "objetivo" and op["bruto"] == pytest.approx(2.0)


def test_cierre_por_tiempo():
    s = sim_con_orden()
    s.procesar_vela(T, 100.5, 100.6, 99.95, 100.2)
    ops = []
    for _ in range(10):
        ops += s.procesar_vela(T, 100.2, 100.5, 99.8, 100.3)
    assert len(ops) == 1 and ops[0]["motivo"] == "tiempo"
