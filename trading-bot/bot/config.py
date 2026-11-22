"""Carga de config.yaml y del archivo .env."""
from __future__ import annotations

import os
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent


def cargar_config(ruta: str | Path | None = None) -> dict:
    ruta = Path(ruta) if ruta else RAIZ / "config.yaml"
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f)


def cargar_claves(modo: str) -> tuple[str, str]:
    """Lee las claves del .env según el modo. Nunca las imprime."""
    try:
        from dotenv import load_dotenv
        load_dotenv(RAIZ / ".env")
    except ImportError:
        pass
    prefijo = "DEMO" if modo == "demo" else "REAL"
    key = os.getenv(f"BINANCE_{prefijo}_API_KEY", "")
    secret = os.getenv(f"BINANCE_{prefijo}_API_SECRET", "")
    if not key or not secret:
        raise SystemExit(
            f"Faltan BINANCE_{prefijo}_API_KEY / BINANCE_{prefijo}_API_SECRET en el archivo .env"
        )
    return key, secret
