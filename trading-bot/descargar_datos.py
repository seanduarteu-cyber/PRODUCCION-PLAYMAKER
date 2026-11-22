"""Descarga velas históricas de Binance Futures (USDⓈ-M) desde data.binance.vision.

Es el archivo público y gratuito de Binance: no necesita claves ni cuenta.

Uso:
    python descargar_datos.py                              # usa config.yaml
    python descargar_datos.py --pares BTCUSDT ETHUSDT --desde 2026-05 --hasta 2026-10
"""
from __future__ import annotations

import argparse
import io
import zipfile
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

from bot.config import cargar_config

BASE = "https://data.binance.vision/data/futures/um"
COLUMNAS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
            "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


def _leer_zip(contenido: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(contenido)) as z:
        with z.open(z.namelist()[0]) as f:
            df = pd.read_csv(f, header=None, names=COLUMNAS)
    # Algunos archivos traen fila de encabezado y otros no.
    df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()].copy()
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = df[c].astype(float)
    t = df["open_time"].astype("int64")
    unidad = "us" if t.iloc[0] > 10**14 else "ms"   # Binance usa microsegundos en algunos sets
    df["time"] = pd.to_datetime(t, unit=unidad, utc=True)
    return df[["time", "open", "high", "low", "close", "volume"]]


def _bajar(url: str) -> bytes | None:
    r = requests.get(url, timeout=60)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.content


def _meses(desde: str, hasta: str) -> list[str]:
    y, m = map(int, desde.split("-"))
    y2, m2 = map(int, hasta.split("-"))
    out = []
    while (y, m) <= (y2, m2):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def descargar_par(par: str, intervalo: str, desde: str, hasta: str,
                  dias_extra: bool, carpeta: Path) -> Path:
    partes = []
    for mes in _meses(desde, hasta):
        url = f"{BASE}/monthly/klines/{par}/{intervalo}/{par}-{intervalo}-{mes}.zip"
        contenido = _bajar(url)
        if contenido is None:
            print(f"  {par} {mes}: no disponible")
            continue
        partes.append(_leer_zip(contenido))
        print(f"  {par} {mes}: {len(partes[-1])} velas")

    if dias_extra:
        # Días del mes siguiente a 'hasta' (los meses en curso solo existen como diarios).
        y, m = map(int, hasta.split("-"))
        d = date(y + (m == 12), m % 12 + 1, 1)
        hoy = date.today()
        n = 0
        while d < hoy:
            url = f"{BASE}/daily/klines/{par}/{intervalo}/{par}-{intervalo}-{d.isoformat()}.zip"
            contenido = _bajar(url)
            if contenido is not None:
                partes.append(_leer_zip(contenido))
                n += 1
            d += timedelta(days=1)
        print(f"  {par} diarios extra: {n} días")

    if not partes:
        raise RuntimeError(f"No se descargaron datos para {par}")
    df = pd.concat(partes).drop_duplicates("time").sort_values("time").reset_index(drop=True)
    carpeta.mkdir(parents=True, exist_ok=True)
    destino = carpeta / f"{par}_{intervalo}.csv.gz"
    df.to_csv(destino, index=False)
    return destino


def main() -> None:
    cfg = cargar_config()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pares", nargs="+", default=[p.replace("/", "").split(":")[0] for p in cfg["pares"]])
    ap.add_argument("--intervalo", default=cfg["temporalidad"])
    ap.add_argument("--desde", default=cfg["backtest"]["desde"], help="AAAA-MM")
    ap.add_argument("--hasta", default=cfg["backtest"]["hasta"], help="AAAA-MM")
    ap.add_argument("--sin-diarios", action="store_true", help="No bajar los días del mes en curso")
    ap.add_argument("--carpeta", default="datos")
    a = ap.parse_args()

    for par in a.pares:
        print(f"Descargando {par}...")
        destino = descargar_par(par, a.intervalo, a.desde, a.hasta, not a.sin_diarios, Path(a.carpeta))
        print(f"  -> {destino}")


if __name__ == "__main__":
    main()
