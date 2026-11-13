#!/usr/bin/env bash
# Imprime una página HTML a PDF con el Chromium del entorno.
# Uso: bash propuestas/html_a_pdf.sh entrada.html salida.pdf
set -euo pipefail
ENTRADA="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
SALIDA="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
# Chromium sin interfaz del entorno (la versión instalada puede cambiar entre sesiones)
if [ -z "${CHROME:-}" ]; then
  for c in /opt/pw-browsers/chromium_headless_shell-*/chrome-*/{headless_shell,chrome-headless-shell}; do
    [ -x "$c" ] && CHROME="$c" && break
  done
fi
[ -n "${CHROME:-}" ] || { echo "No se encontró Chromium en /opt/pw-browsers" >&2; exit 1; }
"$CHROME" --no-sandbox --disable-gpu --virtual-time-budget=5000 --no-pdf-header-footer \
  --print-to-pdf="$SALIDA" "file://$ENTRADA" 2>/dev/null
echo "OK  $SALIDA"
