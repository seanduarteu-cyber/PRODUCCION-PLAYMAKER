import pandas as pd
import pytest

from bot import compuerta
from bot.riesgo import ControlRiesgo, tamano_posicion


def test_tamano_arriesga_el_porcentaje_indicado():
    qty = tamano_posicion(1000, entrada=100, stop=99, riesgo_pct=0.005, apalancamiento_max=10)
    assert qty * (100 - 99) == pytest.approx(5.0)


def test_tamano_limitado_por_apalancamiento():
    # stop muy cerca -> pediría un tamaño enorme; se limita a 3x el capital
    qty = tamano_posicion(1000, entrada=100, stop=99.99, riesgo_pct=0.005, apalancamiento_max=3)
    assert qty * 100 == pytest.approx(3000)


def test_limite_diario_y_reinicio_al_dia_siguiente():
    c = ControlRiesgo(perdida_diaria_max=0.03, caida_max=0.5)
    c.actualizar(1000, pd.Timestamp("2026-01-01 00:00", tz="UTC"))
    c.actualizar(965, pd.Timestamp("2026-01-01 10:00", tz="UTC"))
    assert not c.puede_operar(965)[0]
    c.actualizar(965, pd.Timestamp("2026-01-02 00:05", tz="UTC"))
    assert c.puede_operar(965)[0]


def test_kill_switch_es_permanente():
    c = ControlRiesgo(perdida_diaria_max=1.0, caida_max=0.15)
    c.actualizar(1000, pd.Timestamp("2026-01-01", tz="UTC"))
    c.actualizar(840, pd.Timestamp("2026-01-05", tz="UTC"))
    c.actualizar(2000, pd.Timestamp("2026-01-09", tz="UTC"))
    ok, motivo = c.puede_operar(2000)
    assert not ok and "KILL SWITCH" in motivo


def test_estado_se_puede_guardar_y_recuperar():
    c = ControlRiesgo(0.03, 0.15)
    c.actualizar(1000, pd.Timestamp("2026-01-01", tz="UTC"))
    d = ControlRiesgo(0.03, 0.15)
    d.cargar_dict(c.a_dict())
    assert d.a_dict() == c.a_dict()


def test_compuerta(cfg):
    bueno = {"operaciones": 150, "factor_beneficio": 1.5, "esperanza_r": 0.12, "caida_max": 0.08}
    assert compuerta.evaluar(bueno, cfg["compuerta"])[0]
    malo = dict(bueno, factor_beneficio=0.9, operaciones=20)
    ok, motivos = compuerta.evaluar(malo, cfg["compuerta"])
    assert not ok and len(motivos) == 2
