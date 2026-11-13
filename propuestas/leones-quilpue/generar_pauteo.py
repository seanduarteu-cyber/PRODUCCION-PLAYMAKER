"""Pauteo de la primera reunión (virtual) con Los Leones de Quilpué, en PDF rellenable.

Uso:
    python3 propuestas/leones-quilpue/generar_pauteo.py

Arma pauteo_reunion.html, lo imprime a PDF con html_a_pdf.sh y agrega un campo de texto (o casilla) sobre
cada recuadro de respuesta. Crea Pauteo_Reunion_Leones_Quilpue.pdf: se llena en pantalla (Chrome, Edge,
Acrobat) o impreso, a mano.
"""

import subprocess
from pathlib import Path

import pymupdf

DIR = Path(__file__).parent
HTML = DIR / "pauteo_reunion.html"
PDF = DIR / "Pauteo_Reunion_Leones_Quilpue.pdf"

FECHA = "13 de noviembre de 2026"
AGENDA = [
    ("0 a 5", "Presentaciones", "Quiénes participan y su rol. Agradecer el espacio."),
    ("5 a 10", "Playmaker", "Quiénes somos, planta propia en Santiago y clubes con los que trabajamos."),
    ("10 a 30", "Escuchar al club", "Puntos a definir y preguntas clave. Anotar todo."),
    ("30 a 40", "Ideas de trabajo", "Primeros equipos, formativas y tienda oficial para hinchas."),
    ("40 a 45", "Cierre", "Acuerdos, escudo y fecha de la siguiente reunión."),
]
PUNTOS = [
    "Fecha de término del contrato actual",
    "Qué incluye hoy el canje (prendas por jugador y por staff)",
    "Jugadores por equipo adulto (damas y varones) y staff",
    "CATEGORIAS",  # tabla de jugadores por categoría
    "Qué compran hoy las formativas y a qué precio",
    "Quién decide el proveedor y en qué plazo",
    "Fecha en que necesitan la ropa para 2027",
    "Siguiente reunión y fecha de entrega de la propuesta",
]
CATEGORIAS = ["Sub-11", "Sub-13", "Sub-14", "Sub-16", "Sub-18", "Sub-20"]
RAMAS = ["Damas", "Varones"]
PREGUNTAS = [
    "¿Cuáles son los objetivos del club para 2027?",
    "¿Qué incluye hoy su acuerdo de indumentaria y cuándo termina?",
    "¿Qué les ha funcionado y qué mejorarían?",
    "¿Qué paga el club y qué pagan las familias en formativas?",
    "¿Cuántos jugadores tienen por equipo y por categoría?",
    "¿Venden indumentaria a hinchas hoy? ¿Cuánto y cómo?",
    "¿Qué haría ganadora una propuesta para ustedes?",
    "¿Quién toma la decisión y cuándo?",
    "¿Les interesa incluir al colegio, con buzos y ropa de educación física?",
]
CIERRE = ["Escudo en alta resolución pedido", "Siguiente reunión agendada", "Fecha de entrega de la propuesta acordada"]

# recuadros de respuesta: el color de fondo los identifica en el PDF para ponerles un campo encima
FONDO_TEXTO, FONDO_CASILLA = (252, 251, 247), (255, 255, 254)


def campo(clase=""):
    return f'<div class="resp {clase}"></div>'


def html():
    nombres = []  # nombre de cada campo, en el orden de lectura (arriba abajo, izquierda derecha)
    ficha = []
    for etq in ("Fecha y hora", "Participantes del club", "Plataforma"):
        ficha.append(f'<div><small>{etq.upper()}</small>{campo()}</div>')
        nombres.append(("texto", etq, False))
    agenda = "\n".join(f'<tr><td class="min">{m}</td><td class="que">{q}</td><td>{c}</td></tr>' for m, q, c in AGENDA)

    puntos = []
    for i, p in enumerate(PUNTOS, start=1):
        if p == "CATEGORIAS":
            cab = "".join(f"<th>{c.upper()}</th>" for c in CATEGORIAS)
            filas = ""
            for rama in RAMAS:
                filas += f"<tr><td class='rama'>{rama}</td>" + "".join(f"<td>{campo('celda')}</td>" for _ in CATEGORIAS) + "</tr>"
                nombres += [("texto", f"{rama} {c}", False) for c in CATEGORIAS]
            puntos.append(f'<div class="punto ancho"><p><b>{i}</b>Jugadores por categoría formativa</p>'
                          f'<table class="cat"><tr><th></th>{cab}</tr>{filas}</table></div>')
        else:
            puntos.append(f'<div class="punto"><p><b>{i}</b>{p}</p>{campo()}</div>')
            nombres.append(("texto", f"Punto {i}: {p}", True))
    preguntas = []
    for i, q in enumerate(PREGUNTAS, start=1):
        preguntas.append(f'<div class="pregunta"><p><b>{i}</b>{q}</p>{campo("alta")}</div>')
        nombres.append(("texto", f"Pregunta {i}: {q}", True))
    cierre = []
    for c in CIERRE:
        cierre.append(f'<div class="cierre"><div class="resp casilla"></div><span>{c}</span>{campo("corta")}</div>')
        nombres += [("casilla", c, False), ("texto", f"{c}: detalle", False)]
    nombres.append(("texto", "Notas", True))

    css = (DIR / "estilo_pauteo.css").read_text(encoding="utf-8")
    pagina = f"""<!doctype html>
<!-- Generado por generar_pauteo.py: no editar a mano. -->
<html lang="es"><head><meta charset="utf-8"><title>Pauteo de reunión con Los Leones de Quilpué</title>
<style>
{css}</style></head><body>

<section class="page">
  <div class="cab"><img src="../_recursos/playmaker_logo_horizontal_navy.png" alt="Playmaker"><span>USO INTERNO</span></div>
  <div class="kicker">PAUTEO DE REUNIÓN VIRTUAL</div>
  <h1>Club Deportivo Colegio Los Leones de Quilpué</h1>
  <p class="bajada">Primera reunión, {FECHA}</p>
  <div class="ficha">{''.join(ficha)}</div>
  <div class="objetivo"><b>OBJETIVO</b>Conocer los objetivos y necesidades del club para 2027, presentar a Playmaker y salir con
    los datos para preparar la propuesta, el escudo y la fecha de la siguiente reunión.</div>
  <h2>MINUTO A MINUTO</h2>
  <table class="agenda"><tr><th>MINUTOS</th><th>QUÉ</th><th>CÓMO</th></tr>{agenda}</table>
  <h2>PUNTOS A DEFINIR</h2>
  <div class="puntos">{''.join(puntos)}</div>
  <div class="pie"><span>PLAYMAKER SPA. PAUTEO DE REUNIÓN PARA USO INTERNO.</span><span>1 DE 2</span></div>
</section>

<section class="page">
  <div class="cab"><img src="../_recursos/playmaker_logo_horizontal_navy.png" alt="Playmaker"><span>LOS LEONES DE QUILPUÉ</span></div>
  <h2 class="primero">PREGUNTAS CLAVE</h2>
  <div class="preguntas">{''.join(preguntas)}</div>
  <h2>ANTES DE CORTAR</h2>
  <div class="cierres">{''.join(cierre)}</div>
  <h2>NOTAS</h2>
  {campo("notas")}
  <div class="pie"><span>PLAYMAKER SPA. PAUTEO DE REUNIÓN PARA USO INTERNO.</span><span>2 DE 2</span></div>
</section>

</body></html>
"""
    HTML.write_text(pagina, encoding="utf-8")
    return nombres


def recuadros(doc):
    """Recuadros de respuesta del PDF impreso, en orden de lectura: (página, rect, es_casilla)."""
    encontrados = []
    for n, page in enumerate(doc):
        for d in page.get_drawings():
            fill = d.get("fill")
            if not fill:
                continue
            rgb = tuple(round(c * 255) for c in fill)
            if rgb in (FONDO_TEXTO, FONDO_CASILLA) and d["rect"].width > 4:
                encontrados.append((n, d["rect"], rgb == FONDO_CASILLA))
    # por fila (centro vertical, para que una casilla quede antes del campo de su misma fila) y luego por columna
    return sorted(encontrados, key=lambda e: (e[0], round((e[1].y0 + e[1].y1) / 2 / 6), e[1].x0))


def main():
    nombres = html()
    subprocess.run(["bash", str(DIR.parent / "html_a_pdf.sh"), str(HTML), str(PDF)], check=True, stdout=subprocess.DEVNULL)
    doc = pymupdf.open(PDF)
    cajas = recuadros(doc)
    if len(cajas) != len(nombres):
        raise SystemExit(f"Se esperaban {len(nombres)} recuadros y hay {len(cajas)}")
    for (n, rect, es_casilla), (tipo, nombre, multilinea) in zip(cajas, nombres):
        if es_casilla != (tipo == "casilla"):
            raise SystemExit(f"El recuadro de «{nombre}» no es del tipo esperado")
        w = pymupdf.Widget()
        w.field_name = nombre
        w.field_label = nombre
        w.rect = rect + (1, 1, -1, -1)
        w.border_width = 0
        if tipo == "casilla":
            w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
            w.field_value = False
        else:
            w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
            w.text_font = "Helv"
            w.text_fontsize = 9
            w.text_color = (0.08, 0.12, 0.24)
            if multilinea:
                w.field_flags |= pymupdf.PDF_TX_FIELD_IS_MULTILINE
        doc[n].add_widget(w)
    doc.save(PDF, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)
    print(f"OK  {PDF}  ({len(doc)} páginas, {len(nombres)} campos)")


if __name__ == "__main__":
    main()
