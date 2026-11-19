"""Une la propuesta de Stade Français con el catálogo de implementos como anexo, en un solo PDF.

Uso:
    python3 propuestas/stade-francais-2027/unir_implementos.py

Arma el catálogo de implementos en modo anexo, con las páginas numeradas a continuación de la propuesta y
con las fotos de img/implementos (las de trabajos para Stade Français, con el escudo nuevo) en lugar de las
originales. Crea Propuesta_Stade_Francais_2027_completa.pdf.
"""

import subprocess
from pathlib import Path

from pypdf import PdfReader, PdfWriter

DIR = Path(__file__).parent
IMPLEMENTOS = DIR.parent / "implementos"
PROPUESTA = DIR / "Propuesta_Stade_Francais_2027.pdf"
SALIDA = DIR / "Propuesta_Stade_Francais_2027_completa.pdf"
HTML = IMPLEMENTOS / "catalogo_implementos_stade.html"
ANEXO = DIR / "base" / "Catalogo_Implementos_Rugby_anexo_stade.pdf"


def chromium():
    for patron in ("chromium_headless_shell-*/chrome-*/headless_shell", "chromium_headless_shell-*/chrome-*/chrome-headless-shell"):
        for c in sorted(Path("/opt/pw-browsers").glob(patron)):
            if c.is_file():
                return str(c)
    raise SystemExit("No se encontró Chromium en /opt/pw-browsers")


paginas = len(PdfReader(PROPUESTA).pages)
fotos = Path("..") / DIR.name / "img" / "implementos"
subprocess.run(["node", str(IMPLEMENTOS / "generar_html.js"), "--anexo", str(paginas + 1), "--fotos", str(fotos),
                "--salida", HTML.name], check=True, stdout=subprocess.DEVNULL)
subprocess.run([chromium(), "--no-sandbox", "--disable-gpu", "--virtual-time-budget=5000", "--no-pdf-header-footer",
                f"--print-to-pdf={ANEXO}", f"file://{HTML}"], check=True, stdout=subprocess.DEVNULL,
               stderr=subprocess.DEVNULL)

writer = PdfWriter(clone_from=PROPUESTA)
writer.append(str(ANEXO))
writer.add_metadata({"/Title": "Propuesta Stade Français 2027 con anexo de balones e implementos"})
with open(SALIDA, "wb") as fh:
    writer.write(fh)
total = len(PdfReader(SALIDA).pages)
print(f"OK  {SALIDA.name}  ({paginas} páginas de propuesta + {total - paginas} de anexo)")
