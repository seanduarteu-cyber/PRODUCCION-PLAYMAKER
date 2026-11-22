import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bot.config import cargar_config  # noqa: E402


@pytest.fixture
def cfg():
    return cargar_config()


def velas_sinteticas(n: int = 6000, semilla: int = 7) -> pd.DataFrame:
    """Paseo aleatorio con tramos de tendencia y de rango, para que haya señales de todo tipo."""
    rng = np.random.default_rng(semilla)
    deriva = np.repeat(rng.choice([-0.0004, 0.0, 0.0004], size=n // 300 + 1), 300)[:n]
    ret = deriva + rng.normal(0, 0.002, n)
    close = 100 * np.exp(np.cumsum(ret))
    open_ = np.concatenate([[100.0], close[:-1]])
    amp = np.abs(rng.normal(0, 0.0015, n)) * close
    high = np.maximum(open_, close) + amp
    low = np.minimum(open_, close) - amp
    vol = rng.lognormal(3, 0.6, n)
    idx = pd.date_range("2026-01-01", periods=n, freq="5min", tz="UTC")
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": vol}, index=idx)


@pytest.fixture
def velas():
    return velas_sinteticas()
