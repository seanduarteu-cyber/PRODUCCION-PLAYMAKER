"""Compara las estrategias de scalping con datos históricos reales, comisiones incluidas.

Separa el periodo en dos:
  * DENTRO de muestra: datos que se pueden usar para ajustar parámetros.
  * FUERA de muestra: datos que la estrategia nunca "vio". Es el que cuenta para la compuerta.

Uso:
    python backtest.py                         # todas las estrategias, todos los pares
    python backtest.py --estrategias wyckoff --detalle
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from bot import compuerta
from bot.backtester import cargar_velas, combinar, ejecutar, remuestrear, senales_de
from bot.config import cargar_config
from bot.estrategias import DESCRIPCION


def _fmt(m: dict) -> dict:
    pf = m["factor_beneficio"]
    return {
        "ops": m["operaciones"],
        "ops/día": f"{m['por_dia']:.1f}",
        "aciertos": f"{m['aciertos']:.0%}",
        "esperanza": f"{m['esperanza_r']:+.3f}R",
        "f.benef": "inf" if pf == float("inf") else f"{pf:.2f}",
        "retorno": f"{m['retorno']:+.1%}",
        "sin comis.": f"{m['retorno_sin_comisiones']:+.1%}",
        "comisiones": f"{m['comisiones']:,.0f}",
        "caída máx": f"{m['caida_max']:.1%}",
        "sharpe": f"{m['sharpe']:.2f}",
        "kill sw.": m["kill_switch"],
    }


def main() -> None:
    cfg = cargar_config()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--estrategias", nargs="+", default=list(cfg["parametros"]))
    ap.add_argument("--pares", nargs="+", default=[p.replace("/", "").split(":")[0] for p in cfg["pares"]])
    ap.add_argument("--datos", default="datos")
    ap.add_argument("--salida", default="resultados")
    ap.add_argument("--detalle", action="store_true", help="Muestra resultados por par")
    ap.add_argument("--temporalidad", default=cfg["temporalidad"],
                    help="Ej. 15m o 1h: arma esas velas desde las de config.yaml")
    ap.add_argument("--sin-kill-switch", action="store_true",
                    help="No corta la simulación al caer 15%% (para medir la ventaja completa)")
    a = ap.parse_args()
    if a.sin_kill_switch:
        cfg["riesgo"]["caida_max"] = 1.0
        cfg["riesgo"]["perdida_diaria_max"] = 1.0

    corte = cfg["backtest"]["fuera_de_muestra_desde"]
    capital = cfg["riesgo"]["capital_inicial"]
    salida = Path(a.salida)
    salida.mkdir(exist_ok=True)

    velas = {}
    for par in a.pares:
        ruta = Path(a.datos) / f"{par}_{cfg['temporalidad']}.csv.gz"
        if not ruta.exists():
            raise SystemExit(f"No existe {ruta}. Ejecuta primero: python descargar_datos.py")
        velas[par] = cargar_velas(ruta)
        if a.temporalidad != cfg["temporalidad"]:
            velas[par] = remuestrear(velas[par], a.temporalidad)
    inicio = min(df.index[0] for df in velas.values())
    fin = max(df.index[-1] for df in velas.values())

    print(f"\nDatos: {inicio:%Y-%m-%d} a {fin:%Y-%m-%d} | velas de {a.temporalidad} | pares: {', '.join(a.pares)}")
    print(f"Dentro de muestra: hasta {corte} | Fuera de muestra: desde {corte}")
    c = cfg["costos"]
    print(f"Comisiones: maker {c['comision_maker']:.3%}, taker {c['comision_taker']:.3%}, "
          f"deslizamiento {c['deslizamiento']:.3%} | capital {capital:,.0f} USDT por par | "
          f"riesgo {cfg['riesgo']['riesgo_por_operacion']:.1%} por operación\n")

    filas, informe_compuerta = [], {}
    for nombre in a.estrategias:
        params = cfg["parametros"][nombre]
        res = {"dentro": [], "fuera": []}
        for par, df in velas.items():
            s = senales_de(nombre, df, params)
            r_in = ejecutar(df, s, cfg, par, hasta=corte)
            r_out = ejecutar(df, s, cfg, par, desde=corte)
            res["dentro"].append(r_in)
            res["fuera"].append(r_out)
            if a.detalle:
                for periodo, r in (("dentro", r_in), ("fuera", r_out)):
                    filas.append({"estrategia": nombre, "par": par, "periodo": periodo, **r.metricas})
            if len(r_out.operaciones):
                r_out.operaciones.to_csv(salida / f"operaciones_{nombre}_{par}.csv", index=False)

        for periodo in ("dentro", "fuera"):
            m = combinar(res[periodo], capital)
            filas.append({"estrategia": nombre, "par": "CARTERA", "periodo": periodo, **m})
            if periodo == "fuera":
                ok, motivos = compuerta.evaluar(m, cfg["compuerta"])
                informe_compuerta[nombre] = {"aprobada": ok, "motivos": motivos,
                                             "metricas_fuera_de_muestra": m}

    tabla = pd.DataFrame(filas)
    tabla.to_csv(salida / "resumen.csv", index=False)
    with open(salida / "compuerta.json", "w", encoding="utf-8") as f:
        json.dump({"corte": corte, "estrategias": informe_compuerta}, f, indent=2, ensure_ascii=False, default=str)

    for periodo, titulo in (("dentro", "DENTRO DE MUESTRA"), ("fuera", "FUERA DE MUESTRA (el que cuenta)")):
        sub = tabla[(tabla.periodo == periodo) & (tabla.par == "CARTERA")]
        vista = pd.DataFrame([{"estrategia": f["estrategia"], **_fmt(f)} for f in sub.to_dict("records")])
        print(f"=== {titulo} — cartera de {len(velas)} pares ===")
        print(vista.to_string(index=False))
        print()

    if a.detalle:
        sub = tabla[tabla.par != "CARTERA"]
        vista = pd.DataFrame([{"estrategia": f["estrategia"], "par": f["par"], "periodo": f["periodo"], **_fmt(f)}
                              for f in sub.to_dict("records")])
        print("=== DETALLE POR PAR ===")
        print(vista.to_string(index=False))
        print()

    print("=== COMPUERTA (requisitos para dinero real, sobre datos fuera de muestra) ===")
    for nombre, inf in informe_compuerta.items():
        estado = "APROBADA" if inf["aprobada"] else "NO APROBADA"
        print(f"  {nombre:<16} {estado:<12} {DESCRIPCION.get(nombre, '')}")
        for mot in inf["motivos"]:
            print(f"      - {mot}")
    print(f"\nResultados guardados en {salida}/ (resumen.csv, compuerta.json, operaciones_*.csv)")


if __name__ == "__main__":
    main()
