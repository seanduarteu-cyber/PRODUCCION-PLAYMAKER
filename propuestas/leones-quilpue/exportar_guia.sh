#!/usr/bin/env bash
# Exporta la guía de reunión con Los Leones de Quilpué a PDF con el Chromium del entorno.
# Uso: bash propuestas/leones-quilpue/exportar_guia.sh
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
# Chromium sin interfaz del entorno (la versión instalada puede cambiar entre sesiones)
if [ -z "${CHROME:-}" ]; then
  for c in /opt/pw-browsers/chromium_headless_shell-*/chrome-*/{headless_shell,chrome-headless-shell}; do
    [ -x "$c" ] && CHROME="$c" && break
  done
fi
[ -n "${CHROME:-}" ] || { echo "No se encontró Chromium en /opt/pw-browsers" >&2; exit 1; }
"$CHROME" --no-sandbox --disable-gpu --virtual-time-budget=5000 --no-pdf-header-footer \
  --print-to-pdf="$DIR/Guia_Reunion_Leones_Quilpue.pdf" "file://$DIR/guia_reunion.html" 2>/dev/null
echo "OK  $DIR/Guia_Reunion_Leones_Quilpue.pdf"
