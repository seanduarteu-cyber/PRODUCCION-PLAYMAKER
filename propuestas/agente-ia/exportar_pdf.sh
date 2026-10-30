#!/usr/bin/env bash
# Exporta la base de conocimiento (Markdown) a PDF con el estilo de Playmaker.
# Uso: bash propuestas/agente-ia/exportar_pdf.sh
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
MD="$DIR/Base_Conocimiento_Futbol_Playmaker.md"
HTML="$DIR/.Base_Conocimiento_Futbol_Playmaker.html"
PDF="$DIR/Base_Conocimiento_Futbol_Playmaker.pdf"
CHROME="${CHROME:-/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell}"

cuerpo="$(pandoc -f gfm -t html "$MD" \
  | sed 's|\[PEGAR AQUÍ EL ENLACE DE DRIVE DE LA GUÍA DE TALLAS\]|<span class="pendiente">[PEGAR AQUÍ EL ENLACE DE DRIVE DE LA GUÍA DE TALLAS]</span>|')"
actualizado="$(grep -m1 '^Última actualización' "$MD" | sed 's/^Última actualización: //; s/\.$//')"

cat > "$HTML" <<EOF
<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Base de conocimiento: fútbol – Playmaker</title>
<link rel="stylesheet" href="estilo_pdf.css"></head><body>
<div class="portada">
  <img src="../_recursos/playmaker_logo_horizontal_blanco.png" alt="Playmaker">
  <div class="kicker">AGENTE DE IA DE VENTAS · BASE DE CONOCIMIENTO</div>
  <h1>Productos y precios de fútbol</h1>
  <p>Playmaker · playmaker.cl · Actualizado: ${actualizado}</p>
</div>
${cuerpo}
<div class="pie">Playmaker · Base de conocimiento para el agente de IA de ventas · Uso interno de la agencia administradora.</div>
</body></html>
EOF

"$CHROME" --no-sandbox --disable-gpu --virtual-time-budget=3000 --no-pdf-header-footer \
  --print-to-pdf="$PDF" "file://$HTML" 2>/dev/null
rm -f "$HTML"
echo "OK  $PDF"
