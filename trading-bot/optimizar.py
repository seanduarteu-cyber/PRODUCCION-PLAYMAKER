"""Búsqueda de parámetros SIN hacerse trampa.

1. Prueba combinaciones de parámetros SOLO con datos dentro de muestra.
2. Elige las mejores por esperanza (ganancia media por operación, en R).
3. Recién entonces las prueba con datos fuera de muestra, que no participaron en la elección.

Si una combinación brilla dentro de muestra y se cae fuera de muestra, está sobreajustada:
no sirve para operar.

Uso:
    python optimizar.py                     # todas las estrategias
    python optimizar.py --estrategias wyckoff --top 5
"""
from __future__ import annotations

import argparse
import copy
import itertools
from pathlib import Path

import pandas as pd

from bot.backtester import cargar_velas, combinar, ejecutar, senales_de
from bot.config import cargar_config

# Valores a probar para cada estrategia (el resto de parámetros queda como en config.yaml).
GRILLAS = {
    "ema_pullback": {"stop_atr": [1.5, 2.5, 4.0], "objetivo_r": [1.0, 1.5, 2.5], "ema_tendencia": [100, 200]},
    "bollinger_rsi": {"stop_atr": [1.5, 2.5, 4.0], "rsi_bajo": [20, 25, 30], "adx_max": [20, 30]},
    "ruptura_volumen": {"stop_atr": [1.5, 2.5, 4.0], "objetivo_r": [1.5, 2.5, 4.0], "vol_mult": [1.5, 2.5]},
    "wyckoff": {"rango_velas": [48, 96], "vol_mult": [1.5, 2.5], "rr_min": [1.0, 2.0], "ancho_max_atr": [8, 15]},
}


def evaluar(velas: dict, nombre: str, params: dict, cfg: dict, desde=None, hasta=None) -> dict:
    res = []
    for par, df in velas.items():
        s = senales_de(nombre, df, params)
        res.append(ejecutar(df, s, cfg, par, desde=desde, hasta=hasta))
    return combinar(res, cfg["riesgo"]["capital_inicial"])


def main() -> None:
    cfg = cargar_config()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--estrategias", nargs="+", default=list(GRILLAS))
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--min-ops", type=int, default=100)
    ap.add_argument("--datos", default="datos")
    a = ap.parse_args()

    # Para medir la ventaja real se desactiva el kill switch (si no, corta la muestra).
    cfg_eval = copy.deepcopy(cfg)
    cfg_eval["riesgo"]["caida_max"] = 1.0
    cfg_eval["riesgo"]["perdida_diaria_max"] = 1.0

    pares = [p.replace("/", "").split(":")[0] for p in cfg["pares"]]
    velas = {p: cargar_velas(Path(a.datos) / f"{p}_{cfg['temporalidad']}.csv.gz") for p in pares}
    corte = cfg["backtest"]["fuera_de_muestra_desde"]

    filas = []
    for nombre in a.estrategias:
        grilla = GRILLAS[nombre]
        combos = [dict(zip(grilla, v)) for v in itertools.product(*grilla.values())]
        print(f"\n{nombre}: probando {len(combos)} combinaciones dentro de muestra...")
        candidatos = []
        for cambio in combos:
            params = {**cfg["parametros"][nombre], **cambio}
            m = evaluar(velas, nombre, params, cfg_eval, hasta=corte)
            if m["operaciones"] >= a.min_ops:
                candidatos.append((m["esperanza_r"], cambio, params, m))
        candidatos.sort(key=lambda x: x[0], reverse=True)

        for esperanza, cambio, params, m_in in candidatos[:a.top]:
            m_out = evaluar(velas, nombre, params, cfg_eval, desde=corte)
            filas.append({
                "estrategia": nombre, "parametros": ", ".join(f"{k}={v}" for k, v in cambio.items()),
                "ops_dentro": m_in["operaciones"], "esperanza_dentro": f"{m_in['esperanza_r']:+.3f}R",
                "retorno_dentro": f"{m_in['retorno']:+.1%}",
                "ops_fuera": m_out["operaciones"], "esperanza_fuera": f"{m_out['esperanza_r']:+.3f}R",
                "f.benef_fuera": f"{m_out['factor_beneficio']:.2f}",
                "retorno_fuera": f"{m_out['retorno']:+.1%}", "caída_fuera": f"{m_out['caida_max']:.1%}",
            })

    tabla = pd.DataFrame(filas)
    Path("resultados").mkdir(exist_ok=True)
    tabla.to_csv("resultados/optimizacion.csv", index=False)
    print("\n=== MEJORES COMBINACIONES (elegidas solo con datos dentro de muestra) ===")
    print("Sin kill switch, para medir la ventaja completa. Comisiones incluidas.\n")
    print(tabla.to_string(index=False))
    print("\nGuardado en resultados/optimizacion.csv")
    print("Para usar una combinación, copia sus valores a la sección 'parametros' de config.yaml "
          "y vuelve a correr backtest.py.")


if __name__ == "__main__":
    main()
