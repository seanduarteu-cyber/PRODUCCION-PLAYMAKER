#!/usr/bin/env bash
# Exporta la lista de precios a PNG (3200 x 2200 px) con el Chromium del entorno.
# Uso: bash propuestas/listas-de-precios/exportar.sh
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
CHROME="${CHROME:-/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell}"
"$CHROME" --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size=1600,1100 --virtual-time-budget=3000 \
  --screenshot="$DIR/Lista_Precios_Futbol.png" "file://$DIR/lista_precios_futbol.html" 2>/dev/null
echo "OK  $DIR/Lista_Precios_Futbol.png"
