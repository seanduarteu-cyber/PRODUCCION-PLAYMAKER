#!/usr/bin/env bash
# Exporta el catálogo de implementos a PDF y a Word desde catalogo.json.
# Uso: bash propuestas/implementos/exportar.sh
#      bash propuestas/implementos/exportar.sh --anexo 24   (además, Catalogo_Implementos_Rugby_anexo.pdf:
#      el catálogo como anexo de una propuesta, con las páginas numeradas desde la 24)
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
node "$DIR/generar_html.js"
node "$DIR/generar_word.js"
# Chromium sin interfaz del entorno (la versión instalada puede cambiar entre sesiones)
if [ -z "${CHROME:-}" ]; then
  for c in /opt/pw-browsers/chromium_headless_shell-*/chrome-*/{headless_shell,chrome-headless-shell}; do
    [ -x "$c" ] && CHROME="$c" && break
  done
fi
[ -n "${CHROME:-}" ] || { echo "No se encontró Chromium en /opt/pw-browsers" >&2; exit 1; }
"$CHROME" --no-sandbox --disable-gpu --virtual-time-budget=5000 --no-pdf-header-footer \
  --print-to-pdf="$DIR/Catalogo_Implementos_Rugby.pdf" "file://$DIR/catalogo_implementos.html" 2>/dev/null
echo "OK  $DIR/Catalogo_Implementos_Rugby.pdf"
if [ "${1:-}" = "--anexo" ]; then
  node "$DIR/generar_html.js" --anexo "$2"
  "$CHROME" --no-sandbox --disable-gpu --virtual-time-budget=5000 --no-pdf-header-footer \
    --print-to-pdf="$DIR/Catalogo_Implementos_Rugby_anexo.pdf" "file://$DIR/catalogo_implementos_anexo.html" 2>/dev/null
  echo "OK  $DIR/Catalogo_Implementos_Rugby_anexo.pdf"
fi
