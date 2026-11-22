"""Ejecuta el bot en vivo.

    python run.py --modo paper     # simulado con precios reales, sin claves
    python run.py --modo demo      # cuenta Demo Trading de Binance (claves demo en .env)
    python run.py --modo real --confirmo-dinero-real   # solo si la compuerta lo aprueba

Detener: Ctrl+C. El estado se guarda en logs/ y se recupera al reiniciar.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import pandas as pd

from bot import compuerta
from bot.config import RAIZ, cargar_config
from bot.metricas import calcular_metricas


def configurar_logs(modo: str) -> None:
    carpeta = RAIZ / "logs"
    carpeta.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler(carpeta / f"bot_{modo}.log", encoding="utf-8")],
    )


def verificar_compuerta_real(cfg: dict) -> list[str]:
    """Devuelve la lista de motivos por los que NO se permite operar con dinero real."""
    motivos = []
    req = cfg["compuerta"]
    ruta = RAIZ / "resultados" / "compuerta.json"
    if not ruta.exists():
        return ["no hay backtest: ejecuta python backtest.py"]
    informe = json.loads(ruta.read_text(encoding="utf-8"))["estrategias"]
    for nombre in cfg["estrategias_activas"]:
        inf = informe.get(nombre)
        if not inf or not inf["aprobada"]:
            motivos.append(f"backtest fuera de muestra de '{nombre}' no aprobado: "
                           f"{'; '.join(inf['motivos']) if inf else 'sin datos'}")

    ruta_demo = RAIZ / "logs" / "operaciones_demo.csv"
    if not ruta_demo.exists():
        motivos.append("no hay historial en la cuenta demo (logs/operaciones_demo.csv)")
    else:
        ops = pd.read_csv(ruta_demo, parse_dates=["t_salida"])
        ops = ops[ops["estrategia"].isin(cfg["estrategias_activas"])]
        if len(ops) == 0:
            motivos.append("la cuenta demo no tiene operaciones de las estrategias activas")
        else:
            capital0 = ops["capital"].iloc[0] - ops["pnl"].iloc[0]
            curva = pd.Series(ops["capital"].to_numpy(), index=pd.to_datetime(ops["t_salida"], utc=True))
            m = calcular_metricas(ops, curva, capital0)
            ok, mot = compuerta.evaluar(m, req, req["min_operaciones_demo"])
            if not ok:
                motivos.append("resultados en demo insuficientes: " + "; ".join(mot))
    return motivos


def main() -> None:
    cfg = cargar_config()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modo", choices=["paper", "demo", "real"], default=cfg.get("modo", "paper"))
    ap.add_argument("--confirmo-dinero-real", action="store_true")
    ap.add_argument("--una-vez", action="store_true", help="Ejecuta un solo ciclo (para probar)")
    a = ap.parse_args()

    configurar_logs(a.modo)
    log = logging.getLogger("bot")

    if a.modo == "real":
        motivos = verificar_compuerta_real(cfg)
        if motivos or not a.confirmo_dinero_real:
            log.error("MODO REAL BLOQUEADO.")
            for m in motivos:
                log.error("  - %s", m)
            if not a.confirmo_dinero_real:
                log.error("  - falta el parámetro --confirmo-dinero-real")
            sys.exit(1)

    from bot.ejecutor import EjecutorExchange, EjecutorPaper
    from bot.exchange import ConexionBinance

    import ccxt
    try:
        cx = ConexionBinance(a.modo)
    except ccxt.AuthenticationError as e:
        log.error("Binance rechazó las claves API (%s). Revisa el .env: las claves demo se crean en "
                  "demo.binance.com > API Management y son distintas de las reales.", type(e).__name__)
        sys.exit(1)
    except ccxt.NetworkError as e:
        log.error("No se pudo conectar con Binance: %s\nRevisa tu internet. Binance bloquea algunas "
                  "regiones (por ejemplo EE. UU.); el bot debe correr desde un país permitido.", e)
        sys.exit(1)
    carpeta = RAIZ / "logs"
    bot = EjecutorPaper(cfg, cx, carpeta) if a.modo == "paper" else EjecutorExchange(cfg, cx, a.modo, carpeta)
    try:
        bot.ejecutar(una_vez=a.una_vez)
    except KeyboardInterrupt:
        log.info("Bot detenido por el usuario. Las órdenes de stop y take profit siguen en la exchange.")


if __name__ == "__main__":
    main()
