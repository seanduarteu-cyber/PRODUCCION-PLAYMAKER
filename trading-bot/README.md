# Bot de scalping para Binance Futures

Bot en Python que lee velas de 5 minutos de varias criptomonedas y genera señales con 4 estrategias. Abre y cierra operaciones en Binance Futures (USDⓈ-M) con stop loss y take profit puestos **en la exchange**. Primero se prueba con datos históricos, luego en simulación y en la cuenta **Demo** de Binance, y solo pasa a dinero real si demuestra resultados.

> ⚠️ **Ningún bot garantiza rentabilidad.** Este bot no promete ganancias. Lo que sí hace es medir de forma honesta si una estrategia tiene ventaja después de comisiones, y **se niega a operar con dinero real** si no la tiene (ver [Compuerta](#compuerta-de-rendimiento)).

## Resultado del primer backtest (noviembre 2026)

Datos reales de Binance Futures, de mayo a noviembre de 2026, con 5 pares (BTC, ETH, SOL, BNB y XRP). Se incluyen comisiones de nivel VIP 0 y deslizamiento de precio. El periodo **fuera de muestra** va del 1 de septiembre al 20 de noviembre de 2026: son datos que no se usaron para elegir los parámetros.

| Estrategia (5m) | Operaciones | Aciertos | Esperanza por operación | Factor de beneficio | Retorno |
|---|---|---|---|---|---|
| Tendencia (EMA pullback) | 401 | 37% | −0,42R | 0,55 | −14,2% (kill switch) |
| Reversión (Bollinger + RSI) | 243 | 29% | −0,37R | 0,63 | −8,1% |
| Ruptura con volumen | 428 | 33% | −0,40R | 0,59 | −14,6% (kill switch) |
| Wyckoff spring/upthrust | 419 | 30% | −0,37R | 0,65 | −12,4% (kill switch) |

**Ninguna pasa la compuerta.** El optimizador probó 70 combinaciones de parámetros y ninguna tuvo esperanza positiva, ni siquiera dentro de muestra.

La causa principal son los **costos**. En 5 minutos el stop queda a ~0,25% del precio, y comisiones más deslizamiento cuestan ~0,3R por operación. Las mismas estrategias en velas de 1 hora pierden 10 a 20 veces menos (`python backtest.py --temporalidad 1h`), aunque en este periodo tampoco llegan a ganar.

Usa la cuenta demo para validar que la integración funciona y para probar ideas nuevas, no para esperar ganancias con estas reglas tal como están.

## Instalación

Requiere Python 3.11 o superior.

```bash
cd trading-bot
python -m venv .venv
source .venv/bin/activate          # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Paso a paso

### 1. Descargar datos históricos (gratis, sin claves)

```bash
python descargar_datos.py
```

Descarga velas de 5 minutos desde `data.binance.vision`, el archivo público de Binance, y las guarda en `datos/`. Los pares y las fechas se configuran en `config.yaml`.

### 2. Backtest: comparar estrategias

```bash
python backtest.py                       # las 4 estrategias, todos los pares
python backtest.py --detalle             # además, el resultado por par
python backtest.py --temporalidad 15m    # probar velas de 15m o 1h
python backtest.py --sin-kill-switch     # medir la ventaja sin cortar la simulación
```

Qué significa cada columna:
- **esperanza**: ganancia media por operación, medida en "R" (1R = lo que se arriesga si salta el stop). Si es negativa, la estrategia pierde a la larga.
- **f.benef**: factor de beneficio, las ganancias totales divididas por las pérdidas totales. Tiene que ser mayor que 1.
- **sin comis.**: el retorno que habría tenido sin comisiones. Muestra cuánto se comen los costos.
- **kill sw.**: en cuántos pares se activó el kill switch.

Los resultados quedan en `resultados/`.

### 3. Optimizar sin hacerse trampa

```bash
python optimizar.py
```

Busca parámetros **solo con datos dentro de muestra** y luego prueba a los mejores fuera de muestra. Si una combinación es buena dentro y mala fuera, está sobreajustada y no sirve.

### 4. Modo paper: simulación con precios en vivo

```bash
python run.py --modo paper
```

No necesita claves. Lee los precios reales de Binance y simula las órdenes con **exactamente las mismas reglas que el backtest**; hay una prueba automática que lo verifica. Las operaciones quedan en `logs/operaciones_paper.csv`.

### 5. Modo demo: cuenta Demo Trading de Binance

1. Entra a <https://demo.binance.com> con tu cuenta de Binance. La cuenta demo trae saldo ficticio.
2. Ve a **API Management** dentro de la demo y crea una clave API. Las claves demo son **distintas** de las reales.
3. Copia `.env.example` como `.env` y completa `BINANCE_DEMO_API_KEY` y `BINANCE_DEMO_API_SECRET`.
4. Ejecuta:

```bash
python run.py --modo demo
```

El bot hace lo siguiente:
- **Configura cada par** en margen aislado y con el apalancamiento máximo de `config.yaml`.
- **Al cierre de cada vela de 5 minutos**, si hay señal y el control de riesgo lo permite, coloca una **orden límite**, que paga la comisión maker, la más barata.
- **Cada 10 segundos** revisa si la orden se llenó. Apenas se llena, pone el **stop loss** (stop-market) y el **take profit** (límite) en la exchange, de modo que la posición queda protegida aunque el bot se caiga.
- **Si la orden no se llena en 2 velas**, la cancela. Si la operación dura más de 3 horas, la cierra a mercado.
- **Guarda su estado** en `logs/estado_demo.json` y lo recupera si se reinicia.
- **Registra cada operación** en `logs/operaciones_demo.csv`.

### 6. Modo real: bloqueado hasta aprobar la compuerta

```bash
python run.py --modo real --confirmo-dinero-real
```

Se niega a arrancar si no se cumple **todo** lo siguiente:
- **Backtest aprobado:** el backtest fuera de muestra de cada estrategia activa aprobó la compuerta.
- **Historial demo suficiente:** hay al menos 50 operaciones en la cuenta demo (`min_operaciones_demo`) que también aprueban la compuerta.
- **Confirmación explícita:** se pasó el parámetro `--confirmo-dinero-real`.

## Compuerta de rendimiento

Está definida en `config.yaml`, en la sección `compuerta`:

| Requisito | Valor por defecto |
|---|---|
| Mínimo de operaciones (backtest fuera de muestra) | 100 |
| Factor de beneficio mínimo | 1,2 |
| Esperanza mínima por operación | +0,05R |
| Caída máxima | 15% |
| Mínimo de operaciones en la cuenta demo | 50 |

## Gestión de riesgo

Se configura en la sección `riesgo` de `config.yaml`:
- **Riesgo por operación:** 0,5% del capital si salta el stop. El tamaño de cada posición se calcula para cumplirlo.
- **Apalancamiento máximo:** 3x. Pone un tope al tamaño cuando el stop está muy cerca.
- **Pérdida diaria máxima:** 3%. Si se alcanza, el bot no abre más operaciones hasta el día siguiente (UTC).
- **Kill switch:** si el capital cae 15% desde su máximo, el bot se apaga.
- **Máximo de posiciones abiertas:** 3 a la vez.

## Estrategias

| Nombre | Idea | Archivo |
|---|---|---|
| `ema_pullback` | Tendencia: EMA9 > EMA21 > EMA200; entra cuando el precio retrocede a la EMA21 | `bot/estrategias/ema_pullback.py` |
| `bollinger_rsi` | Reversión: cierre fuera de la banda de Bollinger con RSI extremo y ADX bajo (mercado lateral) | `bot/estrategias/bollinger_rsi.py` |
| `ruptura_volumen` | Ruptura del canal de 20 velas con volumen, tras una compresión de volatilidad | `bot/estrategias/ruptura_volumen.py` |
| `wyckoff` | Spring (falsa ruptura del piso del rango) y upthrust (falsa ruptura del techo), con volumen | `bot/estrategias/wyckoff.py` |

**Para agregar una estrategia:**
1. Crea un archivo con una función `calcular(df, params)` que devuelva las columnas `senal`, `entrada`, `stop` y `objetivo`. Usa los demás archivos como modelo.
2. Regístrala en `bot/estrategias/__init__.py`.
3. Agrega sus parámetros en `config.yaml`.

Las pruebas verifican automáticamente que no "mire el futuro".

**Cómo simula las órdenes el backtest.** Es conservador a propósito (detalle en `bot/simulador.py`):
- **Orden límite:** se llena como maker solo si el precio atraviesa el límite.
- **Stop y objetivo en la misma vela:** se cuenta como stop.
- **Stop:** paga comisión taker más deslizamiento.
- **Objetivo:** paga comisión maker.

## Dejarlo corriendo 24/7

El bot tiene que estar siempre encendido: en un VPS (~USD 5–10 al mes) o en un PC que no se apague.

**Binance bloquea algunas regiones (por ejemplo EE. UU.)**, así que el servidor tiene que estar en un país permitido. En Linux lo más simple es usar `tmux`:

```bash
tmux new -s bot
python run.py --modo demo
# salir sin detenerlo: Ctrl+B y luego D. Volver: tmux attach -t bot
```

**Alertas por Telegram (opcional):** completa `TELEGRAM_TOKEN` y `TELEGRAM_CHAT_ID` en el `.env` y el bot te avisará de cada orden y cada cierre.

## Seguridad

- **Las claves van solo en `.env`.** El `.gitignore` impide que el archivo se suba a GitHub. Nunca las pegues en un chat.
- **Claves reales sin permiso de retiro** y con **lista blanca de IP** (la IP de tu VPS).
- **Empieza con poco capital** aunque la compuerta apruebe.

## Limitaciones conocidas

- **Funding:** el backtest no cuenta los pagos de funding. Como las operaciones duran máximo 3 horas, el efecto es pequeño.
- **Ventana sin protección:** entre que se llena la entrada y se ponen el stop y el take profit pasan hasta 10 segundos.
- **Capital por par:** en el backtest cada par opera con su propio capital; en vivo, el capital es uno solo y compartido.
- **Liquidez de la demo:** la cuenta demo puede llenar órdenes distinto que el mercado real.
- **Futuro:** los resultados pasados no garantizan resultados futuros.

## Pruebas

```bash
python -m pytest -q
```

Verifican:
- **Reglas de llenado** del simulador: maker y taker, gaps, stop antes que objetivo, cierre por tiempo.
- **Estrategias:** que ninguna use datos futuros y que el stop y el objetivo queden del lado correcto.
- **Riesgo:** tamaño de posición, límite diario, kill switch y compuerta.
- **Paridad:** que el modo paper haga las mismas operaciones que el backtest.
- **Flujo demo completo** con una exchange simulada: orden, llenado, protecciones, cierre, registro y recuperación del estado.

## Estructura

```
trading-bot/
├── config.yaml            # pares, temporalidad, costos, riesgo, compuerta, parámetros
├── .env.example           # plantilla de claves (copiar como .env)
├── descargar_datos.py     # histórico gratis de Binance
├── backtest.py            # compara estrategias dentro y fuera de muestra
├── optimizar.py           # búsqueda de parámetros con validación fuera de muestra
├── run.py                 # bot en vivo: paper / demo / real
├── bot/
│   ├── estrategias/       # ema_pullback, bollinger_rsi, ruptura_volumen, wyckoff
│   ├── indicadores.py     # EMA, RSI, ATR, Bollinger, ADX
│   ├── simulador.py       # reglas de llenado (backtest y paper)
│   ├── backtester.py
│   ├── metricas.py
│   ├── riesgo.py          # tamaño de posición, límite diario, kill switch
│   ├── compuerta.py
│   ├── exchange.py        # conexión ccxt con Binance (demo / real)
│   └── ejecutor.py        # lógica en vivo
└── tests/
```
