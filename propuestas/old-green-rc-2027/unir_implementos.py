"""Une la propuesta de Old Green con el catálogo de implementos como anexo, en un solo PDF.

Uso:
    python3 propuestas/old-green-rc-2027/unir_implementos.py

Lee  Propuesta_Old_Green_Rugby_Club_2027.pdf (montar_propuesta.py) y genera el catálogo de implementos en
modo anexo, con las páginas numeradas a continuación de la propuesta. Crea
Propuesta_Old_Green_Rugby_Club_2027_completa.pdf; los campos de precio y cantidad siguen editables.
"""

import subprocess
from pathlib import Path

from pypdf import PdfReader, PdfWriter

DIR = Path(__file__).parent
IMPLEMENTOS = DIR.parent / "implementos"
PROPUESTA = DIR / "Propuesta_Old_Green_Rugby_Club_2027.pdf"
SALIDA = DIR / "Propuesta_Old_Green_Rugby_Club_2027_completa.pdf"

paginas = len(PdfReader(PROPUESTA).pages)
subprocess.run(["bash", str(IMPLEMENTOS / "exportar.sh"), "--anexo", str(paginas + 1)], check=True,
               stdout=subprocess.DEVNULL)
anexo = IMPLEMENTOS / "Catalogo_Implementos_Rugby_anexo.pdf"

writer = PdfWriter(clone_from=PROPUESTA)
writer.append(str(anexo))
writer.add_metadata({"/Title": "Propuesta Old Green Rugby Club 2027 con anexo de balones e implementos"})
with open(SALIDA, "wb") as fh:
    writer.write(fh)
total = len(PdfReader(SALIDA).pages)
print(f"OK  {SALIDA.name}  ({paginas} páginas de propuesta + {total - paginas} de anexo)")
