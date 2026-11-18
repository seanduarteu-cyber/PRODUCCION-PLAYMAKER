"""Propuesta comercial 2027 para Club Deportivo Colegio Los Leones de Quilpué (básquetbol).

Uso:
    python3 propuestas/leones-quilpue/generar_propuesta.py

Lee la solicitud del club (Solicitud_indumentaria_CDC_Los_Leones_2027.xlsx: hojas LNB y LNF, prendas por talla)
y genera:
  - Propuesta_Los_Leones_Quilpue_2027.pdf: canje de primeros equipos y cuerpo técnico, series formativas,
    tienda oficial online con royalty, catálogo con precios y próximos pasos.
  - Canje_Leones_Quilpue_2027.xlsx (uso interno): valorización del canje con fórmulas; los precios se editan
    en la hoja Precios y todo se recalcula.
Los precios de lista, el descuento para formativas y el costo de producción están en PRODUCTOS y PARAMETROS.
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
CATEGORIAS = ["Sub-11", "Sub-13", "Sub-14", "Sub-16", "Sub-18", "Sub-20"]
KITS = [  # kits sugeridos para formativas
    ("Kit de juego", "Camiseta y short de juego", ["camiseta_juego", "short_juego"]),
    ("Kit de entrenamiento", "Camiseta reversible y short", ["camiseta_reversible", "short_entrenamiento"]),
    ("Buzo del club", "Polerón y pantalón de buzo", ["poleron_buzo", "pantalon_buzo"]),
    ("Polerón del club", "Polerón hoodie", ["hoodie"]),
]
TRAMOS = [("Hasta 100 unidades", 11), ("De 101 a 200 unidades", 12), ("De 201 a 350 unidades", 13),
          ("De 351 a 500 unidades", 14), ("Más de 500 unidades", 15)]
BONO_CREDITO = 30


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
  <div class="kicker">PROPUESTA COMERCIAL 2027</div>
  <h1>Club Deportivo Colegio<br>Los Leones de Quilpué</h1>
  <p class="sub">Proveedor técnico oficial de los primeros equipos, el cuerpo técnico y las series formativas, con tienda oficial para socios e hinchas</p>
  <div class="regla"></div>
  <div class="ligas"><div><b>LNB</b><span>Liga Nacional de Básquetbol</span></div><div><b>LNF</b><span>Liga Nacional Femenina</span></div><div><b>6</b><span>categorías formativas</span></div></div>
  <div class="firma"><small>PRESENTADA POR</small><b>Sean Duarte</b><span>Playmaker SpA, sduarte@playmaker.cl, +56 9 3928 3323</span><span>{FECHA}. Validez: 30 días</span></div>
  {pie(1)}
</section>""")

    # 2. la propuesta en tres partes
    paginas.append(f"""<section class="page marfil">
  {cab("SECCIÓN 01", "LA PROPUESTA")}
  <h1>Una propuesta en tres partes</h1>
  <p class="intro">Playmaker propone ser el proveedor técnico oficial de Los Leones de Quilpué desde la temporada 2027: vestir a
    los dos primeros equipos y a su cuerpo técnico, equipar a todas las series formativas y abrir una tienda oficial del club en
    playmaker.cl, con un ingreso para el club por cada venta.</p>
  <div class="pilares">
    <div><em>01</em><b>Canje para los primeros equipos</b><p>Indumentaria de juego, entrenamiento, presentación y viaje para los planteles de la LNB y la LNF y su cuerpo técnico, sin costo para el club.</p><span>{unidades} prendas por temporada</span></div>
    <div><em>02</em><b>Series formativas</b><p>Kits de juego, entrenamiento y presentación para todas las categorías, con precio preferencial y pedidos por categoría.</p><span>De Sub-11 a Sub-20</span></div>
    <div><em>03</em><b>Tienda oficial del club</b><p>Toda la indumentaria del club a la venta en playmaker.cl para socios, familias e hinchas, sin stock ni costo para el club.</p><span>Royalty de 11% a 15%</span></div>
  </div>
  <div class="criterios">
    <h2>CRITERIOS COMUNES A TODA LA PROPUESTA</h2>
    <div class="fila"><b>IDENTIDAD</b><p>Escudo, colores del club (rojo, blanco, negro y azul) y diseño exclusivo para cada prenda, aprobado por el club antes de producir.</p></div>
    <div class="fila"><b>IMPRESIÓN</b><p>Sublimación total en las prendas de juego y entrenamiento: el diseño no se despega, no se agrieta ni pierde color con el uso o el lavado.</p></div>
    <div class="fila"><b>TALLAJE</b><p>Curva completa para adultos, de XS a 4XL, con moldes de hombre y de mujer, y tallas infantiles para las formativas.</p></div>
    <div class="fila"><b>PRODUCCIÓN</b><p>Fabricación a pedido en planta propia en Santiago, con entregas en 10 a 15 días hábiles desde la aprobación del diseño.</p></div>
    <div class="fila"><b>ATENCIÓN</b><p>Un ejecutivo de Playmaker dedicado al club para pedidos, cambios de talla y seguimiento.</p></div>
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
      <li>Incorporaciones y reposiciones durante la temporada, a precio de formativas.</li>
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
  <p class="intro">El canje de los primeros equipos es parte de un convenio de proveedor técnico oficial por dos temporadas. Estas
    son las bases que proponemos para conversar con el club.</p>
  <div class="aportes">
    <div><h2>PLAYMAKER APORTA</h2><ul class="puntos">
      <li>El canje completo de los primeros equipos, el cuerpo técnico y la delegación.</li>
      <li>Diseño exclusivo de toda la línea del club, con los colores y el escudo oficiales.</li>
      <li>Precios preferenciales y atención directa para las series formativas.</li>
      <li>La tienda oficial del club en playmaker.cl, sin stock ni costo para el club.</li>
      <li>Royalty para el club por cada venta de la tienda, con liquidación transparente.</li>
      <li>Producción en planta propia en Santiago y un ejecutivo dedicado al club.</li></ul></div>
    <div><h2>EL CLUB APORTA</h2><ul class="puntos">
      <li>Nombrar a Playmaker proveedor técnico oficial del club.</li>
      <li>Logo Playmaker en los uniformes de juego, calentamiento y presentación de ambos primeros equipos.</li>
      <li>Exclusividad de indumentaria para primeros equipos, formativas y tienda oficial durante el convenio.</li>
      <li>Difusión en las redes del club del lanzamiento de los uniformes y de cada preventa.</li>
      <li>Espacio de marca en el gimnasio del club.</li>
      <li>Una sesión de fotos y video con jugadores de ambos planteles para campañas.</li></ul></div>
  </div>
  <div class="nota-caja"><b>VIGENCIA</b>Temporadas 2027 y 2028. Al cierre de cada temporada se revisan las cantidades del canje según los planteles y las necesidades del club.</div>
  {pie(5)}
</section>""")

    # 6. formativas
    kits = []
    for nombre, detalle_kit, productos in KITS:
        lista = valor_lista(productos)
        form = sum(precio_formativas(PRODUCTOS[p][2]) for p in productos)
        kits.append(f"<tr><td><b>{nombre}</b><br><span class='suave'>{detalle_kit}</span></td><td class='n b'>{pesos(form)}</td><td class='n'>{pesos(lista)}</td></tr>")
    cats = "".join(f"<div>{c}</div>" for c in CATEGORIAS)
    paginas.append(f"""<section class="page">
  {cab("SECCIÓN 03", "SERIES FORMATIVAS")}
  <h1>Series formativas</h1>
  <p class="intro">Todas las categorías del club con la misma identidad de los primeros equipos. Las familias compran a precio
    preferencial en la tienda oficial, con un código por categoría, y Playmaker entrega los pedidos consolidados en el club.</p>
  <h2>CATEGORÍAS</h2>
  <div class="categorias">{cats}</div>
  <p class="nota">Damas y varones. Tallas infantiles y de adulto según la edad de cada categoría.</p>
  <h2>KITS SUGERIDOS</h2>
  <table class="tabla">
    <tr><th>KIT</th><th class="n">PRECIO FORMATIVAS</th><th class="n">PRECIO TIENDA</th></tr>
    {''.join(kits)}
  </table>
  <p class="nota">Precios por kit en pesos chilenos con IVA incluido. Cada prenda también se puede comprar por separado (ver catálogo).</p>
  <h2>CÓMO FUNCIONA</h2>
  <div class="pasos">
    <div><em>01</em><b>Código por categoría</b><p>Cada categoría recibe un código para comprar a precio preferencial.</p></div>
    <div><em>02</em><b>Compra en línea</b><p>Las familias eligen prendas y tallas en playmaker.cl y pagan en línea.</p></div>
    <div><em>03</em><b>Producción por lote</b><p>Al cierre de cada período de compra se fabrica todo lo vendido.</p></div>
    <div><em>04</em><b>Entrega en el club</b><p>Los pedidos llegan al club separados por categoría y jugador.</p></div>
  </div>
  {pie(6)}
</section>""")

    # 7. tienda oficial
    tramos = "".join(f"<tr><td>{t}</td><td class='n b'>{p}%</td></tr>" for t, p in TRAMOS)
    paginas.append(f"""<section class="page marfil">
  {cab("SECCIÓN 04", "TIENDA OFICIAL")}
  <h1>Tienda oficial Los Leones en playmaker.cl</h1>
  <p class="intro">Una vitrina propia del club en playmaker.cl, dentro de la sección de clubes e instituciones, donde socios,
    familias e hinchas compran la indumentaria oficial. Playmaker se encarga del cobro, la producción y la entrega; el club
    recibe un royalty por cada venta, sin invertir en stock.</p>
  <div class="banda"><small>PARA SOCIOS E HINCHAS</small><b>El {TRAMOS[0][1]}% de cada compra va directo a Los Leones</b></div>
  <div class="dos">
    <div><h2>ROYALTY PARA EL CLUB</h2>
      <table class="tabla"><tr><th>UNIDADES VENDIDAS EN LA TEMPORADA</th><th class="n">ROYALTY</th></tr>{tramos}</table>
      <ul class="puntos chica">
        <li>El porcentaje del tramo alcanzado se aplica a todas las unidades de la temporada.</li>
        <li>Se calcula sobre la venta neta: sin IVA y descontadas las devoluciones.</li>
        <li>Si el club lo recibe en productos, se suma un {BONO_CREDITO}% en crédito para indumentaria.</li></ul></div>
    <div><h2>TRANSPARENCIA Y PAGOS</h2><ul class="puntos">
      <li>Liquidación al cierre de cada preventa con el detalle de cada venta: producto, talla, monto neto y royalty.</li>
      <li>Respaldo con la exportación directa de la plataforma de pago.</li>
      <li>Pago en 15 días desde el cierre, por transferencia o en crédito con el bono.</li>
      <li>El club puede pedir el respaldo de cualquier venta en cualquier momento.</li>
      <li>Las compras de las formativas a precio preferencial no generan royalty: ese beneficio va directo a las familias.</li></ul></div>
  </div>
  {pie(7)}
</section>""")

    # 8. catálogo
    lineas = ["Juego", "Entrenamiento", "Presentación y viaje", "Socios e hinchas"]
    cat = []
    for linea in lineas:
        cat.append(f"<tr class='sec'><td colspan='3'>{linea.upper()}</td></tr>")
        for nombre, l, precio, adicional, _ in PRODUCTOS.values():
            if l != linea:
                continue
            marca = " <span class='tag'>NUEVA</span>" if adicional else ""
            cat.append(f"<tr><td>{nombre}{marca}</td><td class='n b'>{pesos(precio_formativas(precio))}</td><td class='n'>{pesos(precio)}</td></tr>")
    paginas.append(f"""<section class="page">
  {cab("SECCIÓN 05", "CATÁLOGO Y PRECIOS")}
  <h1>Catálogo y precios 2027</h1>
  <p class="intro">Toda la línea del club, con las prendas de la solicitud y otras que proponemos sumar (marcadas como nuevas).
    Precios por unidad en pesos chilenos con IVA incluido.</p>
  <table class="tabla detalle">
    <tr><th>PRENDA</th><th class="n">PRECIO FORMATIVAS</th><th class="n">PRECIO TIENDA OFICIAL</th></tr>
    {''.join(cat)}
  </table>
  <p class="nota">El precio formativas aplica a jugadores de las series del club con el código de su categoría. El precio de la tienda oficial aplica a socios, familias e hinchas.</p>
  {pie(8)}
</section>""")

    # 9. próximos pasos
    paginas.append(f"""<section class="page portada cierre">
  <div class="kicker">PRÓXIMOS PASOS</div>
  <h1>De la propuesta a la cancha</h1>
  <div class="pasos-cierre">
    <div><em>01</em><div><b>Revisión de la propuesta</b><p>El club revisa el canje, las condiciones y los precios, y define sus comentarios.</p></div></div>
    <div><em>02</em><div><b>Diseño de la línea 2027</b><p>Playmaker presenta los diseños de cada uniforme y prenda para su aprobación.</p></div></div>
    <div><em>03</em><div><b>Firma del convenio</b><p>Se acuerdan las bases del convenio por las temporadas 2027 y 2028.</p></div></div>
    <div><em>04</em><div><b>Producción y lanzamiento</b><p>Entrega del canje antes del inicio de la temporada y apertura de la tienda oficial.</p></div></div>
  </div>
  <p class="lema">"Un club, una familia."</p>
  <div class="firma"><b>Sean Duarte</b><span>Playmaker SpA</span><span>sduarte@playmaker.cl, +56 9 3928 3323, www.playmaker.cl</span></div>
  {pie(9)}
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

def excel(secciones):
    NAVY = "141E3C"
    f_tit = Font(name="Arial", size=14, bold=True, color=NAVY)
    f_nota = Font(name="Arial", size=9, italic=True, color="6E7280")
    f_cab = Font(name="Arial", size=9, bold=True, color="FFFFFF")
    f_norm = Font(name="Arial", size=10)
    f_input = Font(name="Arial", size=10, color="0000FF")
    f_total = Font(name="Arial", size=10, bold=True, color=NAVY)
    f_sec = Font(name="Arial", size=10, bold=True, color="B1A542")
    r_cab = PatternFill("solid", fgColor=NAVY)
    r_input = PatternFill("solid", fgColor="FFF2CC")
    r_total = PatternFill("solid", fgColor="EDEBE4")
    linea = Border(bottom=Side(style="thin", color="DCD8CB"))
    PESOS, PCT, NUM = '"$"#,##0;("$"#,##0);"-"', "0%", "#,##0"

    def cabecera(ws, fila, textos):
        for i, t in enumerate(textos, start=1):
            c = ws.cell(fila, i, t)
            c.font, c.fill = f_cab, r_cab
            c.alignment = Alignment(horizontal="left" if i == 1 else "center", vertical="center", wrap_text=True)
        ws.row_dimensions[fila].height = 30

    wb = openpyxl.Workbook()
    # Precios
    pr = wb.active
    pr.title = "Precios"
    pr["A1"], pr["A1"].font = "PRECIOS 2027 LOS LEONES DE QUILPUÉ", f_tit
    pr["A2"], pr["A2"].font = "Celdas amarillas editables. Precios por unidad con IVA incluido.", f_nota
    pr["A4"], pr["A4"].font = "IVA", f_norm
    pr["B4"], pr["B4"].font, pr["B4"].fill, pr["B4"].number_format = PARAMETROS["iva"], f_input, r_input, PCT
    pr["A5"], pr["A5"].font = "Costo de producción (% del precio neto)", f_norm
    pr["B5"], pr["B5"].font, pr["B5"].fill, pr["B5"].number_format = PARAMETROS["costo_produccion"], f_input, r_input, PCT
    pr["C5"], pr["C5"].font = "Supuesto: reemplazar por el costo real", f_nota
    cabecera(pr, 7, ["Producto", "Línea", "Precio tienda\ncon IVA", "Precio formativas\ncon IVA", "Costo unitario\nPlaymaker", "Referencia"])
    fila_producto = {}
    for i, (k, (nombre, l, precio, adicional, ref)) in enumerate(PRODUCTOS.items()):
        r = 8 + i
        fila_producto[k] = r
        valores = [nombre + (" (nueva)" if adicional else ""), l, precio, precio_formativas(precio),
                   f"=ROUND(C{r}/(1+$B$4)*$B$5,0)", ref]
        for col, v in enumerate(valores, start=1):
            c = pr.cell(r, col, v)
            c.font = f_input if col in (3, 4) else (f_nota if col == 6 else f_norm)
            if col in (3, 4):
                c.fill = r_input
            if col in (3, 4, 5):
                c.number_format = PESOS
            c.border = linea
    for col, ancho in zip("ABCDEF", (40, 22, 14, 16, 15, 40)):
        pr.column_dimensions[col].width = ancho

    # Canje
    cj = wb.create_sheet("Canje", 0)
    cj["A1"], cj["A1"].font = "CANJE 2027: PRIMEROS EQUIPOS Y CUERPO TÉCNICO", f_tit
    cj["A2"], cj["A2"].font = "Cantidades según la solicitud del club. Precios y costos desde la hoja Precios.", f_nota
    cabecera(cj, 4, ["Prenda", "Producto Playmaker", "LNB", "LNF", "Total", "Precio lista\ncon IVA", "Valor comercial", "Costo Playmaker"])
    r = 5
    filas_total = []
    for seccion, filas in secciones:
        c = cj.cell(r, 1, seccion.upper())
        c.font = f_sec
        r += 1
        for _, nombre, productos, lnb, lnf in filas:
            precio = "=" + "+".join(f"Precios!$C${fila_producto[p]}" for p in productos)
            costo = "=" + "+".join(f"Precios!$E${fila_producto[p]}" for p in productos)
            valores = [nombre, " y ".join(PRODUCTOS[p][0] for p in productos), lnb, lnf, f"=C{r}+D{r}", precio,
                       f"=E{r}*F{r}", f"=E{r}*({costo[1:]})"]
            for col, v in enumerate(valores, start=1):
                cc = cj.cell(r, col, v)
                cc.font = f_norm
                cc.border = linea
                if col in (3, 4, 5):
                    cc.number_format = NUM
                if col in (6, 7, 8):
                    cc.number_format = PESOS
            filas_total.append(r)
            r += 1
    cj.cell(r, 1, "TOTAL POR TEMPORADA").font = f_total
    for col, letra in ((3, "C"), (4, "D"), (5, "E"), (7, "G"), (8, "H")):
        cc = cj.cell(r, col, f"=SUM({letra}5:{letra}{r - 1})")
        cc.font, cc.fill = f_total, r_total
        cc.number_format = NUM if col <= 5 else PESOS
    for col in (1, 2, 6):
        cj.cell(r, col).fill = r_total
    total = r
    for col, ancho in zip("ABCDEFGH", (44, 44, 8, 8, 9, 14, 16, 16)):
        cj.column_dimensions[col].width = ancho

    # Resumen
    rs = wb.create_sheet("Resumen", 0)
    rs["A1"], rs["A1"].font = "LOS LEONES DE QUILPUÉ 2027: RESUMEN DEL CANJE", f_tit
    rs["A2"], rs["A2"].font = "Uso interno. Se calcula con las hojas Canje y Precios.", f_nota
    datos = [
        ("Unidades del canje por temporada", f"=Canje!E{total}", NUM),
        ("Valor comercial del canje (con IVA)", f"=Canje!G{total}", PESOS),
        ("Costo del canje para Playmaker", f"=Canje!H{total}", PESOS),
        ("Margen por kit de juego formativo (neto, sin IVA)",
         f"=ROUND((Precios!D{fila_producto['camiseta_juego']}+Precios!D{fila_producto['short_juego']})/(1+Precios!B4),0)"
         f"-Precios!E{fila_producto['camiseta_juego']}-Precios!E{fila_producto['short_juego']}", PESOS),
        ("Kits de juego formativos que cubren el costo del canje", "=IF(B7=0,0,ROUNDUP(B6/B7,0))", NUM),
    ]
    for i, (txt, f, fmt) in enumerate(datos):
        rr = 4 + i
        rs.cell(rr, 1, txt).font = f_total if i in (1, 2) else f_norm
        c = rs.cell(rr, 2, f)
        c.font, c.number_format = (f_total if i in (1, 2) else f_norm), fmt
        rs.cell(rr, 1).border = c.border = linea
    rs.column_dimensions["A"].width = 56
    rs.column_dimensions["B"].width = 18
    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
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
