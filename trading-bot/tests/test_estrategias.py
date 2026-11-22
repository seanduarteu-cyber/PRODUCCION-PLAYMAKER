import numpy as np
import pytest

from bot import estrategias


@pytest.mark.parametrize("nombre", list(estrategias.ESTRATEGIAS))
def test_sin_mirar_el_futuro(nombre, velas, cfg):
    """La señal de cada vela debe ser idéntica si se calcula con o sin las velas posteriores."""
    p = cfg["parametros"][nombre]
    completo = estrategias.calcular(nombre, velas, p)
    for k in (800, 2500, 4999):
        parcial = estrategias.calcular(nombre, velas.iloc[:k], p)
        np.testing.assert_array_equal(parcial["senal"].to_numpy(), completo["senal"].iloc[:k].to_numpy())
        for col in ("entrada", "stop", "objetivo"):
            np.testing.assert_allclose(parcial[col].to_numpy(), completo[col].iloc[:k].to_numpy(),
                                       equal_nan=True)


@pytest.mark.parametrize("nombre", list(estrategias.ESTRATEGIAS))
def test_stop_y_objetivo_del_lado_correcto(nombre, velas, cfg):
    s = estrategias.calcular(nombre, velas, cfg["parametros"][nombre])
    largos, cortos = s[s.senal == 1], s[s.senal == -1]
    assert len(largos) + len(cortos) > 0, "los datos de prueba deberían generar alguna señal"
    assert (largos.stop < largos.entrada).all() and (largos.objetivo > largos.entrada).all()
    assert (cortos.stop > cortos.entrada).all() and (cortos.objetivo < cortos.entrada).all()


def test_ultima_senal_coincide_con_la_ultima_fila(velas, cfg):
    nombre = "ema_pullback"
    p = cfg["parametros"][nombre]
    s = estrategias.calcular(nombre, velas, p)
    k = int(np.flatnonzero(s.senal.to_numpy() != 0)[-1]) + 1
    sen = estrategias.ultima_senal(nombre, velas.iloc[:k], p)
    assert sen is not None and sen.lado == s.senal.iloc[k - 1]
    assert sen.stop == pytest.approx(s.stop.iloc[k - 1])
