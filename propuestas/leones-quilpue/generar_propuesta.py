"""Propuesta comercial 2027 para Club Deportivo Colegio Los Leones de Quilpué (básquetbol).

Uso:
    python3 propuestas/leones-quilpue/generar_propuesta.py

Lee la solicitud del club (Solicitud_indumentaria_CDC_Los_Leones_2027.xlsx: hojas LNB y LNF, prendas por talla)
y genera:
  - Propuesta_Los_Leones_Quilpue_2027.pdf: primera propuesta, solo el canje de los primeros equipos y el cuerpo
    técnico (lo que pidió el club, sin prendas extra), con su detalle, el convenio y los próximos pasos.
  - Canje_Leones_Quilpue_2027.xlsx (uso interno): simulador por prenda del canje versus el retorno. Para cada
    prenda se define el % de canje (el resto lo compra el club) y las ventas proyectadas a formativas y en la tienda;
    los precios y costos se editan en la hoja Precios y todo se recalcula.
Los precios de lista, el descuento para formativas y el costo de producción están en PRODUCTOS y PARAMETROS.
Las prendas adicionales de PRODUCTOS (adicional=True) no entran al canje: quedan solo en la planilla de precios.
"""

import subprocess
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

DIR = Path(__file__).parent
SOLICITUD = DIR / "Solicitud_indumentaria_CDC_Los_Leones_2027.xlsx"
HTML = DIR / "propuesta_2027.html"
PDF = DIR / "Propuesta_Los_Leones_Quilpue_2027.pdf"
EXCEL = DIR / "Canje_Leones_Quilpue_2027.xlsx"

FECHA = "Santiago, 18 de noviembre de 2026"
PARAMETROS = {"iva": 0.19, "descuento_formativas": 0.10, "costo_produccion": 0.45}

# producto: (nombre, línea, precio de lista con IVA, adicional al pedido del club, referencia de precio)
PRODUCTOS = {
    "camiseta_juego": ("Camiseta de juego", "Juego", 20900, False, "Sudadera sin mangas, lista Old Green"),
    "short_juego": ("Short de juego", "Juego", 18900, False, "Short de juego, lista Old Green"),
    "polera_calentamiento": ("Polera de calentamiento", "Juego", 19900, False, "Camiseta de llegada, lista Old Green"),
    "calcetas": ("Calcetas de juego", "Juego", 10900, True, "Medias personalizadas, lista Old Green"),
    "camiseta_reversible": ("Camiseta reversible", "Entrenamiento", 27900, False, "Línea reversible Playmaker"),
    "short_entrenamiento": ("Short de entrenamiento", "Entrenamiento", 18900, False, "Short de juego, lista Old Green"),
    "polera_entrenamiento": ("Polera de entrenamiento", "Entrenamiento", 19900, False, "Camiseta de llegada, lista Old Green"),
    "poleron_entrenamiento": ("Polerón de entrenamiento medio cierre", "Entrenamiento", 33900, False, "Polerón medio cierre, lista Old Green"),
    "pantalon_buzo": ("Pantalón de buzo", "Presentación y viaje", 25900, False, "Pantalón de buzo, lista Old Green"),
    "poleron_buzo": ("Polerón de buzo con cierre", "Presentación y viaje", 33900, False, "Polerón medio cierre, lista Old Green"),
    "chaqueta": ("Chaqueta de viaje", "Presentación y viaje", 39900, False, "Cortaviento con capucha, lista Old Green"),
    "polo": ("Polo piqué", "Presentación y viaje", 23900, False, "Polo piqué, lista Old Green"),
    "polera_algodon": ("Polera de algodón", "Presentación y viaje", 16900, False, "Polera de algodón, lista Old Green"),
    "short_viaje": ("Short de viaje", "Presentación y viaje", 21900, False, "Short de presentación, lista Old Green"),
    "hoodie": ("Polerón hoodie", "Socios e hinchas", 29900, True, "Polerón hoodie, lista Old Green"),
    "poleron_basic": ("Polerón algodón basic", "Socios e hinchas", 22900, True, "Polerón algodón basic, lista Old Green"),
    "cortaviento": ("Cortaviento", "Socios e hinchas", 36900, True, "Cortaviento sin capucha, lista Old Green"),
    "parka": ("Parka larga impermeable", "Socios e hinchas", 79900, True, "Parka larga, lista Old Green"),
}

# prenda de la solicitud (minúsculas, espacios simples) -> (nombre en la propuesta, productos que la componen)
PRENDAS = {
    "camiseta de juego rojo": ("Camiseta de juego roja", ["camiseta_juego"]),
    "short de juego rojo": ("Short de juego rojo", ["short_juego"]),
    "camiseta de juego azul": ("Camiseta de juego azul", ["camiseta_juego"]),
    "short de juego azul": ("Short de juego azul", ["short_juego"]),
    "camiseta juego negro": ("Camiseta de juego negra", ["camiseta_juego"]),
    "short de juego negro": ("Short de juego negro", ["short_juego"]),
    "camiseta de juego blanco": ("Camiseta de juego blanca", ["camiseta_juego"]),
    "short de juego blanco": ("Short de juego blanco", ["short_juego"]),
    "polera de calentamiento azul": ("Polera de calentamiento azul", ["polera_calentamiento"]),
    "polera de calentamiento rojo": ("Polera de calentamiento roja", ["polera_calentamiento"]),
    "polera de calentamiento blanco": ("Polera de calentamiento blanca", ["polera_calentamiento"]),
    "polera de viaje jugadores 1": ("Polera de viaje 1 (polo piqué)", ["polo"]),
    "polera de viaje jugadores 2": ("Polera de viaje 2 (polera de algodón)", ["polera_algodon"]),
    "polerón de buzo jugadores": ("Polerón de buzo", ["poleron_buzo"]),
    "pantalón de buzo jugadores": ("Pantalón de buzo", ["pantalon_buzo"]),
    "chaqueta jugadores": ("Chaqueta de viaje", ["chaqueta"]),
    "short de viaje": ("Short de viaje", ["short_viaje"]),
    "camiseta reversible color a y b con short": ("Camiseta reversible (colores A y B) con short",
                                                  ["camiseta_reversible", "short_entrenamiento"]),
    "camiseta reversible color c y d": ("Camiseta reversible (colores C y D)", ["camiseta_reversible"]),
    "short de entrenamiento": ("Short de entrenamiento", ["short_entrenamiento"]),
    "polera blanca para dirigir": ("Polera blanca para dirigir (polo piqué)", ["polo"]),
    "polera azul para dirigir": ("Polera azul para dirigir (polo piqué)", ["polo"]),
    "polera de entrenamiento ct 1": ("Polera de entrenamiento 1", ["polera_entrenamiento"]),
    "polera de entrenamiento ct 2": ("Polera de entrenamiento 2", ["polera_entrenamiento"]),
    "polerón de entrenamiento ct": ("Polerón de entrenamiento", ["poleron_entrenamiento"]),
    "short de entrenamiento ct": ("Short de entrenamiento", ["short_entrenamiento"]),
    "pantalón de buzo entrenamiento ct": ("Pantalón de buzo de entrenamiento", ["pantalon_buzo"]),
    "polera de viaje ct 1": ("Polera de viaje 1 (polo piqué)", ["polo"]),
    "polera de viaje ct 2": ("Polera de viaje 2 (polera de algodón)", ["polera_algodon"]),
    "polerón de viaje ct": ("Polerón de viaje", ["poleron_buzo"]),
    "pantalón de viaje ct": ("Pantalón de viaje", ["pantalon_buzo"]),
    "short de viaje ct": ("Short de viaje", ["short_viaje"]),
    "chaqueta ct": ("Chaqueta de viaje", ["chaqueta"]),
}
SECCIONES = {  # sección de la solicitud -> nombre en la propuesta
    "indumentaria de juego": "Jugadores: indumentaria de juego",
    "ropa de presentación": "Jugadores: presentación y viaje",
    "ropa de entrenamiento": "Jugadores: entrenamiento",
    "ropa presentación ct": "Cuerpo técnico: presentación en cancha",
    "ropa de entrenamiento ct": "Cuerpo técnico: entrenamiento",
    "ropa de presentación delegación": "Cuerpo técnico: viaje y delegación",
}
def clave(texto):
    return " ".join(str(texto).lower().split())


def pesos(n):
    return "$" + f"{round(n):,}".replace(",", ".")


def precio_formativas(lista):
    """Precio de lista menos el descuento, llevado al valor terminado en 900 más cercano."""
    p = lista * (1 - PARAMETROS["descuento_formativas"])
    return int((p - 900) / 1000 + 0.5) * 1000 + 900


def leer_solicitud():
    """Prendas por sección en orden de la solicitud: [(sección, [(clave, nombre, productos, lnb, lnf)])]."""
    wb = openpyxl.load_workbook(SOLICITUD, data_only=False)
    cantidades, orden = {}, []
    for hoja in ("LNB", "LNF"):
        ws = wb[hoja]
        seccion = None
        for fila in range(3, ws.max_row + 1):
            a, b = ws.cell(fila, 1).value, ws.cell(fila, 2).value
            if a:
                seccion = SECCIONES[clave(a)]
            if not b or clave(b) not in PRENDAS:
                continue
            n = sum(v for v in (ws.cell(fila, c).value for c in range(4, 13)) if isinstance(v, (int, float)))
            k = (seccion, clave(b))
            if k not in cantidades:
                cantidades[k] = {"LNB": 0, "LNF": 0}
                orden.append(k)
            cantidades[k][hoja] += n
    secciones = []
    for seccion in SECCIONES.values():
        filas = []
        for s, k in orden:
            if s != seccion:
                continue
            c = cantidades[(s, k)]
            if c["LNB"] + c["LNF"] == 0:
                continue  # sin cantidades en la solicitud
            nombre, productos = PRENDAS[k]
            filas.append((k, nombre, productos, c["LNB"], c["LNF"]))
        secciones.append((seccion, filas))
    sin_cantidad = sorted({PRENDAS[k][0] for (s, k), c in cantidades.items() if c["LNB"] + c["LNF"] == 0})
    return secciones, sin_cantidad


def valor_lista(productos):
    return sum(PRODUCTOS[p][2] for p in productos)


# ---------------------------------------------------------------- propuesta (HTML -> PDF)

def pie(num):
    return (f'<div class="pie"><span>UN CLUB, UNA FAMILIA.</span>'
            f'<img src="../_recursos/playmaker_logo_horizontal_navy.png" alt="Playmaker"><span class="num">{num:02d}</span></div>')


def cab(izq, der):
    return f'<div class="cab"><b>{izq}</b><span>{der}</span></div>'


def html(secciones):
    filas_canje = [f for _, filas in secciones for f in filas]
    unidades = sum(f[3] + f[4] for f in filas_canje)
    unidades_lnb = sum(f[3] for f in filas_canje)
    unidades_lnf = sum(f[4] for f in filas_canje)
    valor = sum((f[3] + f[4]) * valor_lista(f[2]) for f in filas_canje)
    paginas = []

    # 1. portada
    paginas.append(f"""<section class="page portada">
  <img class="logo" src="../_recursos/playmaker_logo_horizontal_blanco.png" alt="Playmaker">
  <div class="kicker">PROPUESTA DE CANJE 2027</div>
  <h1>Club Deportivo Colegio<br>Los Leones de Quilpué</h1>
  <p class="sub">Indumentaria de juego, entrenamiento, presentación y viaje para los primeros equipos de la LNB y la LNF y su cuerpo técnico</p>
  <div class="regla"></div>
  <div class="ligas"><div><b>LNB</b><span>Liga Nacional de Básquetbol</span></div><div><b>LNF</b><span>Liga Nacional Femenina</span></div><div><b>{unidades}</b><span>prendas por temporada</span></div></div>
  <div class="firma"><small>PRESENTADA POR</small><b>Sean Duarte</b><span>Playmaker SpA, sduarte@playmaker.cl, +56 9 3928 3323</span><span>{FECHA}. Validez: 30 días</span></div>
  {pie(1)}
</section>""")

    # 2. la propuesta
    jug = [f for sec, filas in secciones if sec.startswith("Jugadores") for f in filas]
    ct = [f for sec, filas in secciones if sec.startswith("Cuerpo técnico") for f in filas]
    paginas.append(f"""<section class="page marfil">
  {cab("SECCIÓN 01", "LA PROPUESTA")}
  <h1>Canje de indumentaria para la temporada 2027</h1>
  <p class="intro">Playmaker propone vestir sin costo para el club a los dos primeros equipos de Los Leones de Quilpué y a su
    cuerpo técnico durante la temporada 2027: indumentaria de juego, entrenamiento, presentación y viaje, según la solicitud
    entregada por el club.</p>
  <div class="pilares">
    <div><em>01</em><b>Plantel LNB</b><p>Indumentaria de juego, calentamiento, entrenamiento, presentación y viaje para el plantel masculino.</p><span>{sum(f[3] for f in jug)} prendas</span></div>
    <div><em>02</em><b>Plantel LNF</b><p>Indumentaria de juego, calentamiento, entrenamiento, presentación y viaje para el plantel femenino.</p><span>{sum(f[4] for f in jug)} prendas</span></div>
    <div><em>03</em><b>Cuerpo técnico y delegación</b><p>Ropa para dirigir, de entrenamiento y de viaje para el cuerpo técnico y la delegación de ambos planteles.</p><span>{sum(f[3] + f[4] for f in ct)} prendas</span></div>
  </div>
  <div class="criterios">
    <h2>CRITERIOS COMUNES A TODA LA PROPUESTA</h2>
    <div class="fila"><b>IDENTIDAD</b><p>Escudo, colores del club (rojo, blanco, negro y azul) y diseño exclusivo para cada prenda, aprobado por el club antes de producir.</p></div>
    <div class="fila"><b>IMPRESIÓN</b><p>Sublimación total en las prendas de juego y entrenamiento: el diseño no se despega, no se agrieta ni pierde color con el uso o el lavado.</p></div>
    <div class="fila"><b>TALLAJE</b><p>Curva completa para adultos, de XS a 4XL, con moldes de hombre y de mujer.</p></div>
    <div class="fila"><b>PRODUCCIÓN</b><p>Fabricación en planta propia en Santiago, con control directo de diseño, sublimación, corte y confección.</p></div>
    <div class="fila"><b>ATENCIÓN</b><p>Un ejecutivo de Playmaker dedicado al club para cambios de talla, reposiciones y seguimiento.</p></div>
  </div>
  {pie(2)}
</section>""")

    # 3. canje: resumen
    resumen = []
    for seccion, filas in secciones:
        lnb, lnf = sum(f[3] for f in filas), sum(f[4] for f in filas)
        resumen.append(f"<tr><td>{seccion}</td><td class='n'>{len(filas)}</td><td class='n'>{lnb}</td><td class='n'>{lnf}</td><td class='n b'>{lnb + lnf}</td></tr>")
    paginas.append(f"""<section class="page">
  {cab("SECCIÓN 02", "CANJE PRIMEROS EQUIPOS")}
  <h1>Canje para los primeros equipos y el cuerpo técnico</h1>
  <p class="intro">Playmaker entrega sin costo para el club toda la indumentaria de la temporada 2027 que el club solicitó para los
    planteles de la Liga Nacional de Básquetbol y la Liga Nacional Femenina, y para su cuerpo técnico y delegación.</p>
  <table class="tabla">
    <tr><th>GRUPO</th><th class="n">PRENDAS</th><th class="n">LNB</th><th class="n">LNF</th><th class="n">TOTAL</th></tr>
    {''.join(resumen)}
    <tr class="total"><td>Total de unidades por temporada</td><td></td><td class="n">{unidades_lnb}</td><td class="n">{unidades_lnf}</td><td class="n">{unidades}</td></tr>
  </table>
  <div class="cifra"><div><small>VALOR COMERCIAL DEL CANJE</small><b>{pesos(valor)}</b><span>por temporada, a precio de lista con IVA incluido</span></div>
    <p>El detalle por prenda está en la página siguiente. Las cantidades corresponden a la solicitud entregada por el club.</p></div>
  <div class="dos">
    <div><h2>QUÉ INCLUYE</h2><ul class="puntos">
      <li>Diseño exclusivo de cada uniforme y prenda, aprobado por el club.</li>
      <li>Nombre y número en las prendas de juego.</li>
      <li>Tallas según la curva entregada por el club, con moldes de hombre y de mujer.</li>
      <li>Entrega consolidada en el club antes del inicio de la temporada.</li></ul></div>
    <div><h2>CONDICIONES</h2><ul class="puntos">
      <li>Cantidades según la solicitud del club para la temporada 2027.</li>
      <li>Cambios de talla sin costo dentro de los 15 días siguientes a la entrega.</li>
      <li>Incorporaciones y reposiciones durante la temporada, a precio preferencial para el club.</li>
      <li>Convenio por dos temporadas, 2027 y 2028, con revisión anual de cantidades.</li></ul></div>
  </div>
  {pie(3)}
</section>""")

    # 4. canje: detalle, jugadores y cuerpo técnico en dos columnas
    def tabla_detalle(grupo, titulo):
        filas_html = []
        lnb_t = lnf_t = 0
        for seccion, filas in secciones:
            if not seccion.startswith(grupo):
                continue
            filas_html.append(f"<tr class='sec'><td colspan='4'>{seccion.split(': ')[1].upper()}</td></tr>")
            for _, nombre, _, lnb, lnf in filas:
                lnb_t, lnf_t = lnb_t + lnb, lnf_t + lnf
                filas_html.append(f"<tr><td>{nombre}</td><td class='n'>{lnb or ''}</td><td class='n'>{lnf or ''}</td>"
                                  f"<td class='n b'>{lnb + lnf}</td></tr>")
        return (f"<table class='tabla detalle'><tr><th>{titulo}</th><th class='n'>LNB</th><th class='n'>LNF</th>"
                f"<th class='n'>TOTAL</th></tr>{''.join(filas_html)}<tr class='total'><td>Subtotal</td>"
                f"<td class='n'>{lnb_t}</td><td class='n'>{lnf_t}</td><td class='n'>{lnb_t + lnf_t}</td></tr></table>")

    paginas.append(f"""<section class="page">
  {cab("SECCIÓN 02", "DETALLE DEL CANJE")}
  <h1>Detalle del canje</h1>
  <p class="intro">Unidades por prenda para cada plantel, según la solicitud del club. LNB: plantel masculino. LNF: plantel femenino.</p>
  <div class="dos detalle-canje">
    <div>{tabla_detalle("Jugadores", "JUGADORES")}</div>
    <div>{tabla_detalle("Cuerpo técnico", "CUERPO TÉCNICO")}</div>
  </div>
  <div class="cifra total-canje"><div><small>TOTAL DEL CANJE POR TEMPORADA</small><b>{unidades} prendas</b><span>{unidades_lnb} para la LNB y {unidades_lnf} para la LNF</span></div></div>
  {pie(4)}
</section>""")

    # 5. lo que aporta cada parte
    paginas.append(f"""<section class="page">
  {cab("SECCIÓN 02", "CONVENIO")}
  <h1>Lo que aporta cada parte</h1>
  <p class="intro">El canje se enmarca en un convenio de proveedor técnico oficial por dos temporadas. Estas son las bases
    que proponemos para conversar con el club.</p>
  <div class="aportes">
    <div><h2>PLAYMAKER APORTA</h2><ul class="puntos">
      <li>El canje completo de los primeros equipos, el cuerpo técnico y la delegación: {unidades} prendas por temporada.</li>
      <li>Diseño exclusivo de toda la línea, con los colores y el escudo oficiales del club.</li>
      <li>Producción en planta propia en Santiago y entrega antes del inicio de la temporada.</li>
      <li>Un ejecutivo dedicado al club para cambios de talla, reposiciones e incorporaciones.</li></ul></div>
    <div><h2>EL CLUB APORTA</h2><ul class="puntos">
      <li>Nombrar a Playmaker proveedor técnico oficial de los primeros equipos.</li>
      <li>Logo Playmaker en los uniformes de juego, calentamiento y presentación de ambos primeros equipos.</li>
      <li>Exclusividad de indumentaria para los primeros equipos y el cuerpo técnico durante el convenio.</li>
      <li>Difusión en las redes del club del lanzamiento de los uniformes.</li>
      <li>Espacio de marca en el gimnasio del club.</li>
      <li>Una sesión de fotos y video con jugadores de ambos planteles para campañas.</li></ul></div>
  </div>
  <div class="nota-caja"><b>VIGENCIA</b>Temporadas 2027 y 2028. Al cierre de cada temporada se revisan las cantidades del canje según los planteles y las necesidades del club.</div>
  {pie(5)}
</section>""")

    # 6. próximos pasos
    paginas.append(f"""<section class="page portada cierre">
  <div class="kicker">PRÓXIMOS PASOS</div>
  <h1>De la propuesta a la cancha</h1>
  <div class="pasos-cierre">
    <div><em>01</em><div><b>Revisión de la propuesta</b><p>El club revisa el canje y las condiciones, y define sus comentarios.</p></div></div>
    <div><em>02</em><div><b>Diseño de la línea 2027</b><p>Playmaker presenta los diseños de cada uniforme y prenda para su aprobación.</p></div></div>
    <div><em>03</em><div><b>Firma del convenio</b><p>Se acuerdan las bases del convenio por las temporadas 2027 y 2028.</p></div></div>
    <div><em>04</em><div><b>Producción y entrega</b><p>Entrega del canje en el club antes del inicio de la temporada 2027.</p></div></div>
  </div>
  <p class="lema">"Un club, una familia."</p>
  <div class="firma"><b>Sean Duarte</b><span>Playmaker SpA</span><span>sduarte@playmaker.cl, +56 9 3928 3323, www.playmaker.cl</span></div>
  {pie(6)}
</section>""")

    css = (DIR / "estilo_propuesta.css").read_text(encoding="utf-8")
    HTML.write_text(f"""<!doctype html>
<!-- Generado por generar_propuesta.py: no editar a mano. -->
<html lang="es"><head><meta charset="utf-8"><title>Propuesta 2027 para Los Leones de Quilpué</title>
<style>
{css}</style></head><body>
{chr(10).join(paginas)}
</body></html>
""", encoding="utf-8")
    subprocess.run(["bash", str(DIR.parent / "html_a_pdf.sh"), str(HTML), str(PDF)], check=True, stdout=subprocess.DEVNULL)
    return unidades, valor


# ---------------------------------------------------------------- planilla interna

# ventas proyectadas de ejemplo por temporada (unidades a formativas, unidades en la tienda), por prenda de jugadores;
# 180 jugadores formativos: 6 categorías, damas y varones, unos 15 por categoría
VENTAS_EJEMPLO = {
    "camiseta de juego rojo": (180, 80), "short de juego rojo": (180, 20), "camiseta de juego blanco": (0, 30),
    "camiseta de juego azul": (0, 15), "camiseta juego negro": (0, 15), "polera de calentamiento rojo": (0, 20),
    "camiseta reversible color a y b con short": (180, 0), "polerón de buzo jugadores": (60, 30),
    "pantalón de buzo jugadores": (60, 20), "chaqueta jugadores": (0, 15), "polera de viaje jugadores 1": (0, 20),
    "polera de viaje jugadores 2": (0, 40), "short de viaje": (0, 10),
}
VENTAS_OTROS = {"calcetas": (180, 20), "hoodie": (0, 50), "poleron_basic": (0, 20), "cortaviento": (0, 10), "parka": (0, 5)}
TRAMOS = [("Hasta 100", 0, 0.11), ("101 a 200", 101, 0.12), ("201 a 350", 201, 0.13), ("351 a 500", 351, 0.14),
          ("Más de 500", 501, 0.15)]


def excel(secciones):
    """Simulador por prenda: % de canje, inversión, compra del club y ventas futuras (formativas y tienda)."""
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.worksheet.datavalidation import DataValidation

    NAVY = "141E3C"
    f_tit = Font(name="Arial", size=14, bold=True, color=NAVY)
    f_nota = Font(name="Arial", size=9, italic=True, color="6E7280")
    f_cab = Font(name="Arial", size=9, bold=True, color="FFFFFF")
    f_norm = Font(name="Arial", size=10)
    f_input = Font(name="Arial", size=10, color="0000FF")
    f_total = Font(name="Arial", size=10, bold=True, color=NAVY)
    f_sec = Font(name="Arial", size=10, bold=True, color="B1A542")
    r_cab = PatternFill("solid", fgColor=NAVY)
    r_grupo = PatternFill("solid", fgColor="3A4570")
    r_input = PatternFill("solid", fgColor="FFF2CC")
    r_total = PatternFill("solid", fgColor="EDEBE4")
    linea = Border(bottom=Side(style="thin", color="DCD8CB"))
    PESOS, PCT, NUM, VECES = '"$"#,##0;-"$"#,##0;"-"', "0%", "#,##0", '0.00" x"'

    def celda(ws, ref, valor, fuente=f_norm, formato=None, relleno=None):
        c = ws[ref]
        c.value, c.font = valor, fuente
        if formato:
            c.number_format = formato
        if relleno:
            c.fill = relleno
        return c

    def entrada(ws, ref, valor, formato=None):
        return celda(ws, ref, valor, f_input, formato, r_input)

    def cabecera(ws, fila, textos, col0=1):
        for i, t in enumerate(textos):
            c = ws.cell(fila, col0 + i, t)
            c.font, c.fill = f_cab, r_cab
            c.alignment = Alignment(horizontal="left" if i == 0 else "center", vertical="center", wrap_text=True)
        ws.row_dimensions[fila].height = 42

    wb = openpyxl.Workbook()

    # ---- Parámetros
    pa = wb.active
    pa.title = "Parámetros"
    celda(pa, "A1", "PARÁMETROS DEL SIMULADOR", f_tit)
    celda(pa, "A2", "Celdas amarillas editables.", f_nota)
    for r, (txt, v, fmt) in enumerate([("IVA", PARAMETROS["iva"], PCT),
                                       ("Costo de producción por defecto (% del precio neto)", PARAMETROS["costo_produccion"], PCT),
                                       ("Temporadas del convenio", 2, NUM)], start=4):
        celda(pa, f"A{r}", txt)
        entrada(pa, f"B{r}", v, fmt)
    celda(pa, "C5", "Se usa si no ingresas un costo propio por producto en la hoja Precios", f_nota)
    celda(pa, "A8", "ROYALTY DE LA TIENDA OFICIAL", f_sec)
    cabecera(pa, 9, ["Unidades vendidas en la tienda", "Desde", "Royalty"])
    for i, (txt, desde, pct) in enumerate(TRAMOS):
        r = 10 + i
        celda(pa, f"A{r}", txt)
        entrada(pa, f"B{r}", desde, NUM)
        entrada(pa, f"C{r}", pct, PCT)
    celda(pa, "A16", "Unidades vendidas en la tienda (de la hoja Simulación)")
    celda(pa, "A17", "Royalty del tramo alcanzado", f_total)
    pa.column_dimensions["A"].width = 54
    pa.column_dimensions["B"].width = 14
    pa.column_dimensions["C"].width = 14

    # ---- Precios
    pr = wb.create_sheet("Precios")
    celda(pr, "A1", "PRECIOS Y COSTOS POR PRODUCTO", f_tit)
    celda(pr, "A2", "Precios por unidad con IVA incluido. El costo se calcula con el % por defecto; reemplázalo por tu costo real si lo conoces.", f_nota)
    cabecera(pr, 4, ["Producto", "Línea", "Precio lista\n(tienda)", "Precio\nformativas", "Precio para el club\n(lo no canjeado)",
                     "Costo unitario\nPlaymaker", "Referencia del precio"])
    fila_p = {}
    for i, (k, (nombre, l, precio, adicional, ref)) in enumerate(PRODUCTOS.items()):
        r = 5 + i
        fila_p[k] = r
        celda(pr, f"A{r}", nombre + (" (nueva)" if adicional else ""))
        celda(pr, f"B{r}", l)
        entrada(pr, f"C{r}", precio, PESOS)
        entrada(pr, f"D{r}", precio_formativas(precio), PESOS)
        entrada(pr, f"E{r}", f"=D{r}", PESOS)
        entrada(pr, f"F{r}", f"=ROUND(C{r}/(1+Parámetros!$B$4)*Parámetros!$B$5,0)", PESOS)
        celda(pr, f"G{r}", ref, f_nota)
        for col in "ABCDEFG":
            pr[f"{col}{r}"].border = linea
    for col, ancho in zip("ABCDEFG", (36, 20, 13, 13, 17, 15, 38)):
        pr.column_dimensions[col].width = ancho

    def ref_precio(productos, col):
        return "+".join(f"Precios!${col}${fila_p[p]}" for p in productos)

    # ---- Simulación
    si = wb.create_sheet("Simulación", 0)
    celda(si, "A1", "SIMULACIÓN DEL CANJE POR PRENDA: INVERSIÓN VERSUS RETORNO POR TEMPORADA", f_tit)
    celda(si, "A2", "Amarillo = editable. % canje: parte de las unidades solicitadas que Playmaker entrega sin costo; el resto lo compra "
                    "el club al precio para el club. Ventas: unidades que proyectas vender en la temporada. Las ventas de ejemplo son supuestos.", f_nota)
    grupos = [(1, "PRENDA"), (4, "SOLICITUD Y CANJE"), (10, "COMPRA DEL CLUB"), (13, "VENTAS FUTURAS PROYECTADAS"),
              (20, "RESULTADO")]
    for col, txt in grupos:
        c = si.cell(4, col, txt)
        c.font, c.fill = Font(name="Arial", size=8, bold=True, color="FFFFFF"), r_grupo
    for col in range(1, 23):
        si.cell(4, col).fill = r_grupo
    cabecera(si, 5, ["Prenda", "Producto Playmaker", "Unidades\nsolicitadas", "Precio lista\ncon IVA", "Costo\nunitario",
                     "% canje", "Unidades\nen canje", "Inversión canje\n(costo)", "Valor comercial\ndel canje",
                     "Unidades que\ncompra el club", "Precio club\ncon IVA", "Margen compra\ndel club",
                     "Ventas a\nformativas (u.)", "Ventas en\ntienda (u.)", "Precio\nformativas", "Margen\nformativas",
                     "Venta neta\ntienda", "Royalty\nal club", "Margen tienda\n(sin royalty)", "Retorno\ntotal",
                     "Resultado\n(retorno - inversión)", "Retorno por\n$1 invertido"])

    def fila_sim(r, nombre, productos, solicitadas, canje, ventas):
        celda(si, f"A{r}", nombre)
        celda(si, f"B{r}", " y ".join(PRODUCTOS[p][0] for p in productos))
        celda(si, f"C{r}", solicitadas, formato=NUM)
        celda(si, f"D{r}", "=" + ref_precio(productos, "C"), formato=PESOS)
        celda(si, f"E{r}", "=" + ref_precio(productos, "F"), formato=PESOS)
        if canje is None:
            celda(si, f"F{r}", None)
            for col in "GHIJKL":
                celda(si, f"{col}{r}", None)
        else:
            entrada(si, f"F{r}", canje, PCT)
            celda(si, f"G{r}", f"=ROUND(C{r}*F{r},0)", formato=NUM)
            celda(si, f"H{r}", f"=G{r}*E{r}", formato=PESOS)
            celda(si, f"I{r}", f"=G{r}*D{r}", formato=PESOS)
            celda(si, f"J{r}", f"=C{r}-G{r}", formato=NUM)
            celda(si, f"K{r}", "=" + ref_precio(productos, "E"), formato=PESOS)
            celda(si, f"L{r}", f"=ROUND(J{r}*(K{r}/(1+Parámetros!$B$4)-E{r}),0)", formato=PESOS)
        entrada(si, f"M{r}", ventas[0], NUM)
        entrada(si, f"N{r}", ventas[1], NUM)
        celda(si, f"O{r}", "=" + ref_precio(productos, "D"), formato=PESOS)
        celda(si, f"P{r}", f"=ROUND(M{r}*(O{r}/(1+Parámetros!$B$4)-E{r}),0)", formato=PESOS)
        celda(si, f"Q{r}", f"=ROUND(N{r}*D{r}/(1+Parámetros!$B$4),0)", formato=PESOS)
        celda(si, f"R{r}", f"=ROUND(Q{r}*Parámetros!$B$17,0)", formato=PESOS)
        celda(si, f"S{r}", f"=Q{r}-R{r}-N{r}*E{r}", formato=PESOS)
        celda(si, f"T{r}", f"=SUM(L{r},P{r},S{r})", f_total, PESOS)
        celda(si, f"U{r}", f"=T{r}-N(H{r})", f_total, PESOS)
        celda(si, f"V{r}", f'=IF(N(H{r})=0,"",T{r}/H{r})', formato=VECES)
        for col in range(1, 23):
            si.cell(r, col).border = linea

    r = 6
    filas_datos = []
    for seccion, filas in secciones:
        celda(si, f"A{r}", seccion.upper(), f_sec)
        r += 1
        for k, nombre, productos, lnb, lnf in filas:
            ventas = VENTAS_EJEMPLO.get(k, (0, 0)) if seccion.startswith("Jugadores") else (0, 0)
            fila_sim(r, nombre, productos, lnb + lnf, 1.0, ventas)
            filas_datos.append(r)
            r += 1
    celda(si, f"A{r}", "OTROS PRODUCTOS (SOLO VENTA, SIN CANJE)", f_sec)
    r += 1
    for k, (nombre, l, precio, adicional, ref) in PRODUCTOS.items():
        if adicional:
            fila_sim(r, nombre, [k], 0, None, VENTAS_OTROS.get(k, (0, 0)))
            filas_datos.append(r)
            r += 1
    primera, ultima = filas_datos[0], filas_datos[-1]
    tot = r + 1
    celda(si, f"A{tot}", "TOTAL POR TEMPORADA", f_total, relleno=r_total)
    for col in range(2, 23):
        si.cell(tot, col).fill = r_total
    for col in "CGHIJLMNPQRSTU":
        celda(si, f"{col}{tot}", f"=SUM({col}{primera}:{col}{ultima})", f_total,
              NUM if col in "CGJMN" else PESOS, r_total)
    celda(si, f"F{tot}", f"=IF(C{tot}=0,0,G{tot}/C{tot})", f_total, PCT, r_total)
    celda(si, f"V{tot}", f'=IF(H{tot}=0,"",T{tot}/H{tot})', f_total, VECES, r_total)
    rojo = PatternFill("solid", fgColor="F6D5D0")
    verde = PatternFill("solid", fgColor="D8EBD5")
    rango = f"U{primera}:U{tot}"
    si.conditional_formatting.add(rango, CellIsRule(operator="lessThan", formula=["0"], fill=rojo))
    si.conditional_formatting.add(rango, CellIsRule(operator="greaterThan", formula=["0"], fill=verde))
    dv = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True,
                        error="Ingresa un porcentaje entre 0% y 100%.", errorTitle="% de canje")
    si.add_data_validation(dv)
    dv.add(f"F{primera}:F{ultima}")
    for col, ancho in zip("ABCDEFGHIJKLMNOPQRSTUV", (40, 34, 11, 12, 11, 9, 10, 15, 15, 12, 12, 14, 12, 11, 11, 14,
                                                    14, 12, 15, 14, 17, 12)):
        si.column_dimensions[col].width = ancho
    si.freeze_panes = "C6"
    pa["B16"], pa["B16"].number_format = f"=Simulación!N{tot}", NUM
    pa["B17"] = "=IF(B16=0,0,INDEX($C$10:$C$14,MATCH(B16,$B$10:$B$14,1)))"
    pa["B17"].number_format, pa["B17"].font = PCT, f_total

    # ---- Resumen
    rs = wb.create_sheet("Resumen", 0)
    celda(rs, "A1", "LOS LEONES DE QUILPUÉ 2027: CANJE VERSUS RETORNO", f_tit)
    celda(rs, "A2", "Uso interno. Se calcula con la hoja Simulación; ahí defines el % de canje y las ventas de cada prenda.", f_nota)
    t = tot
    filas_res = [
        ("EL CANJE", None, None),
        ("Unidades solicitadas por el club", f"=Simulación!C{t}", NUM),
        ("Unidades entregadas en canje", f"=Simulación!G{t}", NUM),
        ("% de la solicitud entregado en canje", f"=Simulación!F{t}", PCT),
        ("Valor comercial del canje (lo que recibe el club, con IVA)", f"=Simulación!I{t}", PESOS),
        ("Inversión de Playmaker en el canje (costo)", f"=Simulación!H{t}", PESOS),
        ("EL RETORNO", None, None),
        ("Margen por las unidades que compra el club", f"=Simulación!L{t}", PESOS),
        ("Margen por ventas a formativas", f"=Simulación!P{t}", PESOS),
        ("Margen por ventas en la tienda (después del royalty)", f"=Simulación!S{t}", PESOS),
        ("Royalty pagado al club por la tienda", f"=Simulación!R{t}", PESOS),
        ("Retorno total", f"=Simulación!T{t}", PESOS),
        ("RESULTADO", None, None),
        ("Resultado por temporada (retorno menos inversión)", "=B15-B9", PESOS),
        ("Retorno por cada $1 invertido en canje", '=IF(B9=0,"",B15/B9)', VECES),
        ("Resultado del convenio completo", "=B17*Parámetros!B6", PESOS),
        ("Margen promedio por unidad vendida (formativas y tienda)",
         f"=IF(Simulación!M{t}+Simulación!N{t}=0,0,ROUND((B12+B13)/(Simulación!M{t}+Simulación!N{t}),0))", PESOS),
        ("Unidades adicionales que habría que vender para cubrir el canje", '=IF(B17>=0,0,IF(B20=0,"",ROUNDUP(-B17/B20,0)))', NUM),
    ]
    for i, (txt, f, fmt) in enumerate(filas_res):
        rr = 4 + i
        if f is None:
            celda(rs, f"A{rr}", txt, f_sec)
            continue
        destacado = txt.startswith(("Resultado", "Inversión", "Retorno total"))
        celda(rs, f"A{rr}", txt, f_total if destacado else f_norm, relleno=r_total if destacado else None)
        celda(rs, f"B{rr}", f, f_total if destacado else f_norm, fmt, r_total if destacado else None)
        rs[f"A{rr}"].border = rs[f"B{rr}"].border = linea
    rs.conditional_formatting.add("B17", CellIsRule(operator="lessThan", formula=["0"], fill=rojo))
    rs.conditional_formatting.add("B17", CellIsRule(operator="greaterThan", formula=["0"], fill=verde))
    rs.conditional_formatting.add("B19", CellIsRule(operator="lessThan", formula=["0"], fill=rojo))
    rs.conditional_formatting.add("B19", CellIsRule(operator="greaterThan", formula=["0"], fill=verde))
    rs.column_dimensions["A"].width = 64
    rs.column_dimensions["B"].width = 18

    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
        ws.page_setup.orientation = "landscape"
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    wb.save(EXCEL)


def main():
    secciones, sin_cantidad = leer_solicitud()
    unidades, valor = html(secciones)
    excel(secciones)
    print(f"OK  {PDF.name}  ({unidades} prendas en el canje, valor comercial {pesos(valor)})")
    print(f"OK  {EXCEL.name}")
    if sin_cantidad:
        print("    Prendas de la solicitud sin cantidades (no van en el canje): " + ", ".join(sin_cantidad))


if __name__ == "__main__":
    main()
