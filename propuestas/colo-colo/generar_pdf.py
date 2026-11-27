"""PDF de la propuesta comercial 2027 para presentar al CSD Colo-Colo, armado desde la planilla de la propuesta.

Uso:
    python3 propuestas/colo-colo/generar_pdf.py

Lee Propuesta_Comercial_CSD_Colo_Colo_2027.xlsm (los valores que la planilla tiene calculados) y crea
propuesta_club.html y Propuesta_Comercial_CSD_Colo_Colo_2027.pdf: portada, resumen de la propuesta, calendario de
entregas, cronograma, canje proporcional a las compras, lista de precios
por disciplina, detalle del canje de los primeros equipos, de formativas y cuerpo técnico y del stock comercial, y
próximos pasos. No incluye costos ni márgenes (hojas COSTOS y RESUMEN NEGOCIO). Si se cambian precios, descuentos o
cantidades en la planilla, basta guardarla y volver a correr este script. Si la planilla no trae valores calculados,
se recalcula con LibreOffice.
"""

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import openpyxl

DIR = Path(__file__).parent
PLANILLA = DIR / "Propuesta_Comercial_CSD_Colo_Colo_2027.xlsm"
HTML = DIR / "propuesta_club.html"
PDF = DIR / "Propuesta_Comercial_CSD_Colo_Colo_2027.pdf"
RECALC = Path("/root/.claude/skills/synced/bc307280-4611-44d6-aa94-f2bad7ad32ae_766667a6-21fa-41c9-a3ab-adb5c42c724e/"
              "xlsx/scripts/recalc.py")
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre",
         "diciembre"]
HOJAS = {"canje": "CANJE PRIMEROS EQUIPOS", "formativas": "FORMATIVAS Y CT", "comercial": "COMERCIAL"}
HOJA_ENTREGAS = "ENTREGAS 2027"
SUFIJOS = r" (básquetbol|futsal|vóleibol|patín|Esperanza Alba|institucional)$"  # disciplina al final del producto
FILAS_PAGINA = 46  # filas de tabla que caben en una página de detalle (con título)


def pesos(n):
    return "$" + f"{round(n or 0):,}".replace(",", ".")


def num(n):
    return f"{round(n or 0):,}".replace(",", ".")


def pct(x):
    return f"{x * 100:.0f}%" if abs(x * 100 - round(x * 100)) < 0.05 else f"{x * 100:.1f}%".replace(".", ",")


def texto(v):
    return " ".join(str(v or "").split())


def libro():
    wb = openpyxl.load_workbook(PLANILLA, data_only=True)
    if wb["RESUMEN"]["D6"].value is None:  # sin valores calculados
        if not RECALC.exists():
            sys.exit("La planilla no tiene valores calculados: ábrela en Excel, guárdala y vuelve a correr el script.")
        subprocess.run([sys.executable, str(RECALC), str(PLANILLA), "120"], check=True, stdout=subprocess.DEVNULL)
        wb = openpyxl.load_workbook(PLANILLA, data_only=True)
    return wb


def leer(wb):
    pr = wb["PRECIOS"]
    descuentos = {}  # los descuentos son internos: no van en el PDF
    cab = next(r for r in range(1, 15) if texto(pr.cell(r, 2).value) == "PRODUCTO")
    disciplinas = []  # [(título, [producto])]
    for r in range(cab + 1, pr.max_row + 1):
        b = texto(pr.cell(r, 2).value)
        if not b:
            continue
        if pr.cell(r, 4).value is None:
            disciplinas.append((b, []))
        elif disciplinas:
            disciplinas[-1][1].append({"producto": re.sub(SUFIJOS, "", b), "linea": pr.cell(r, 3).value,
                                       "valor": pr.cell(r, 4).value or 0, "comercial": pr.cell(r, 5).value or 0})

    rs = wb["RESUMEN"]
    resumen, r = [], 6
    while r <= rs.max_row and texto(rs.cell(r, 2).value) != "TOTAL PROPUESTA":
        resumen.append([rs.cell(r, c).value for c in range(2, 9)])
        r += 1
    total = [rs.cell(r, c).value for c in range(2, 9)]

    detalle = {}
    for clave, hoja in HOJAS.items():
        ws = wb[hoja]
        ramas = []
        for r in range(6, ws.max_row + 1):
            b = texto(ws.cell(r, 2).value)
            if b == "TOTAL" or not b:
                if b == "TOTAL":
                    break
                continue
            if not ramas or ramas[-1][0] != b:
                ramas.append((b, []))
            ramas[-1][1].append({"tipo": texto(ws.cell(r, 3).value), "producto": re.sub(SUFIJOS, "", texto(ws.cell(r, 7).value)),
                                 "modelo": texto(ws.cell(r, 5).value), "color": texto(ws.cell(r, 6).value),
                                 "cantidad": ws.cell(r, 9).value or 0, "valor": ws.cell(r, 10).value or 0,
                                 "precio": ws.cell(r, 11).value or 0, "valor_total": ws.cell(r, 12).value or 0,
                                 "pagar": ws.cell(r, 13).value or 0, "canje": ws.cell(r, 14).value or 0})
        detalle[clave] = ramas
    return descuentos, disciplinas, resumen, total, detalle


def fecha_txt(d):
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}" if hasattr(d, "day") else texto(d)


def fecha_corta(d):
    corto = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    return f"{d.day} {corto[d.month - 1]} {d.year}" if hasattr(d, "day") else texto(d)


def leer_entregas(wb):
    """Calendario de entregas y canje proporcional, de la hoja ENTREGAS 2027 (None si la planilla no la tiene)."""
    if HOJA_ENTREGAS not in wb.sheetnames:
        return None
    ws = wb[HOJA_ENTREGAS]
    e = {"ramas": [], "entregas": [], "adelanto": [], "hitos": [], "nombres_entrega": []}
    modo = None
    for r in range(1, ws.max_row + 1):
        v = [ws.cell(r, c).value for c in range(2, 13)]
        b, c = texto(v[0]), texto(v[1])
        if b == "RAMA":
            modo = "ramas"
        elif b == "ENTREGA" and c == "FECHA":
            modo = "entregas"
        elif b == "ENTREGA" and c.startswith("COMPRAS"):
            modo = "adelanto"
        elif b == "HITO":
            modo = "hitos"
            e["nombres_entrega"] = [texto(x) for x in v[1:] if texto(x) and texto(x) != "DETALLE"]
        elif b == "TOTAL" and modo:
            e["total_" + modo] = v
            modo = None
        elif b.startswith("Proporción canje"):
            e["proporcion"] = v[1] or 0
        elif b.startswith("Canje por cada"):
            e["por_millon"] = v[1] or 0
        elif b.startswith("Simulación"):
            e["sim_compra"] = v[1] or 0
        elif b.startswith("El canje que le corresponde"):
            e["sim_canje"] = v[1] or 0
        elif modo == "hitos" and (not b or not hasattr(v[1], "day")):  # fin del cronograma (filas con fecha)
            modo = None
        elif modo and b:
            e[modo].append(v)
    return e


def pie(n):
    return (f'<div class="pie"><span>CSD COLO-COLO, TEMPORADA 2027</span>'
            f'<img src="../_recursos/playmaker_logo_horizontal_navy.png" alt="Playmaker"><span class="num">{n:02d}</span></div>')


def cab(izq):
    return f'<div class="cab"><b>{izq}</b><span>PROPUESTA COMERCIAL 2027</span></div>'


def paginar(bloques, primera, resto=FILAS_PAGINA):
    """Reparte bloques de filas (cada uno: lista de filas html, la primera es el título de la rama) en páginas."""
    paginas, actual, libre = [], [], primera
    for bloque in bloques:
        while bloque:
            if len(bloque) > libre and actual and libre < 8:
                paginas.append(actual)
                actual, libre = [], resto
            toma = libre
            if len(bloque) > libre and len(bloque) - libre < 6:  # no dejar pocas filas solas en la página siguiente
                toma = len(bloque) - 6
                if toma < 5 and actual:
                    paginas.append(actual)
                    actual, libre = [], resto
                    toma = libre
            parte, bloque = bloque[:toma], bloque[toma:]
            if bloque:  # la rama sigue en la página siguiente: repite su título
                bloque = [parte[0].replace("</td>", " (CONTINUACIÓN)</td>", 1)] + bloque
            actual += parte
            libre -= len(parte)
    if actual:
        paginas.append(actual)
    return paginas


def main():
    wb = libro()
    descuentos, disciplinas, resumen, total, detalle = leer(wb)
    ent = leer_entregas(wb)
    unidades, canje, ventas, neto, iva = total[2], total[3], total[4], total[5], total[6]
    hoy = date.today()
    fecha = f"Santiago, {hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}"
    tot_cat = {}
    for fila in resumen:
        if texto(fila[0]).startswith("Total "):
            clave = next(c for c in HOJAS if c in texto(fila[0]).lower() or (c == "canje" and "canje" in texto(fila[0]).lower()))
            tot_cat[clave] = fila
    ramas_dep = [r for r, _ in detalle["canje"]]
    paginas = []
    n = 1

    # 1. portada
    paginas.append(f"""<section class="page portada">
  <img class="logo" src="../_recursos/playmaker_logo_horizontal_blanco.png" alt="Playmaker">
  <div class="kicker">PROPUESTA COMERCIAL 2027</div>
  <h1>Ramas deportivas del<br>CSD Colo-Colo</h1>
  <p class="sub">Indumentaria de juego, entrenamiento y presentación para los primeros equipos, las escuelas formativas, el cuerpo técnico y la tienda del club</p>
  <div class="regla"></div>
  <div class="cifras-portada"><div><b>{num(unidades)}</b><span>prendas en total</span></div><div><b>{len(ramas_dep)}</b><span>ramas deportivas</span></div><div><b>{pesos(canje)}</b><span>en canje para los primeros equipos</span></div></div>
  <div class="firma"><small>PRESENTADA POR</small><b>Sean Duarte</b><span>Playmaker SpA, sduarte@playmaker.cl, +56 9 3928 3323</span><span>{fecha}</span></div>
  {pie(n)}
</section>""")
    n += 1

    # 2. resumen de la propuesta
    filas = []
    for cat, rama, unid, cj, vt, _nt, _iv in resumen:
        es_total = texto(cat).startswith("Total")
        clase = ' class="sub"' if es_total else (' class="cat"' if cat else "")
        filas.append(f'<tr{clase}><td>{texto(cat)}</td><td>{texto(rama)}</td><td class="n">{num(unid)}</td>'
                     f'<td class="canje">{pesos(cj) if cj else ""}</td><td class="n b">{pesos(vt) if vt else ""}</td></tr>')
    filas.append(f'<tr class="total"><td colspan="2">TOTAL DE LA PROPUESTA</td><td class="n">{num(unidades)}</td>'
                 f'<td class="n">{pesos(canje)}</td><td class="n">{pesos(ventas)}</td></tr>')
    fo, co = tot_cat.get("formativas", [0] * 7), tot_cat.get("comercial", [0] * 7)
    paginas.append(f"""<section class="page">
  {cab("RESUMEN DE LA PROPUESTA")}
  <h1>Resumen de la propuesta</h1>
  <p class="intro">Playmaker propone vestir a las ramas deportivas del CSD Colo-Colo en 2027 en tres partes: los primeros equipos de {", ".join(r.lower() if r != "Esperanza Alba" else r for r in ramas_dep[:-1])} y {ramas_dep[-1] if ramas_dep[-1] == "Esperanza Alba" else ramas_dep[-1].lower()} reciben su indumentaria en canje; las escuelas formativas, el cuerpo técnico, el directorio y la oficina la compran a valor formativas y cuerpo técnico, y el club compra stock para su tienda a precio comercial. Las cantidades son las de la planilla de requerimientos del club.</p>
  <div class="cifras">
    <div><small>PRENDAS</small><b>{num(unidades)}</b><span>canje, formativas y comercial</span></div>
    <div><small>VALOR DEL CANJE</small><b>{pesos(canje)}</b><span>primeros equipos, a valor formativas y cuerpo técnico</span></div>
    <div><small>FORMATIVAS Y CUERPO TÉCNICO</small><b>{pesos(fo[4])}</b><span>{num(fo[2])} prendas, IVA incluido</span></div>
    <div><small>STOCK PARA LA TIENDA</small><b>{pesos(co[4])}</b><span>{num(co[2])} prendas, IVA incluido</span></div>
  </div>
  <h2>VALOR POR CATEGORÍA Y RAMA</h2>
  <table class="tabla val res"><tr><th>CATEGORÍA</th><th>RAMA</th><th class="n">PRENDAS</th><th class="n">VALOR DEL CANJE</th><th class="n">VALOR A PAGAR</th></tr>{"".join(filas)}</table>
  <p class="leyenda">Valores en pesos chilenos con IVA incluido. El canje se valoriza a valor formativas y cuerpo técnico. Las compras suman {pesos(neto)} neto más {pesos(iva)} de IVA.</p>
  {pie(n)}
</section>""")
    n += 1

    # 3. calendario de entregas, cronograma y canje proporcional a las compras
    if ent and ent["entregas"]:
        categorias = [("primer equipo", 1, 4), ("formativas y cuerpo técnico", 2, 5), ("stock para la tienda", 3, 6)]
        tarjetas, filas = [], []
        for i, fila in enumerate(ent["entregas"]):
            nombre = texto(fila[0]).split(": ", 1)[-1].upper()
            ramas_e = [texto(x[0]) for x in ent["ramas"]
                       if any(texto(x[ce]).upper() == nombre and (x[cu] or 0) > 0 for _t, ce, cu in categorias)]
            partes = [f"{num(fila[2 + j])} {t}" for j, (t, _ce, _cu) in enumerate(categorias) if fila[2 + j]]
            tarjetas.append(f'<div><small>ENTREGA {i + 1}</small><b>{fecha_txt(fila[1])}</b>'
                            f'<p>{", ".join(ramas_e)}</p><span>{num(fila[5])} prendas: {", ".join(partes)}</span></div>')
            filas.append(f'<tr class="sec"><td colspan="5">ENTREGA {i + 1}: {fecha_txt(fila[1]).upper()}</td></tr>')
            for x in ent["ramas"]:
                u = [(x[cu] or 0) if texto(x[ce]).upper() == nombre else 0 for _t, ce, cu in categorias]
                if sum(u):
                    filas.append(f'<tr><td>{texto(x[0])}</td>' + "".join(f'<td class="n">{num(v) if v else ""}</td>' for v in u)
                                 + f'<td class="n b">{num(sum(u))}</td></tr>')
            filas.append(f'<tr class="sub"><td>Total entrega {i + 1}</td>'
                         + "".join(f'<td class="n">{num(fila[2 + j]) if fila[2 + j] else ""}</td>' for j in range(3))
                         + f'<td class="n">{num(fila[5])}</td></tr>')
        t = ent.get("total_entregas") or [None] * 9
        filas.append(f'<tr class="total"><td>TOTAL</td><td class="n">{num(t[2])}</td><td class="n">{num(t[3])}</td>'
                     f'<td class="n">{num(t[4])}</td><td class="n">{num(t[5])}</td></tr>')
        paginas.append(f"""<section class="page">
  {cab("CALENDARIO DE ENTREGAS")}
  <h1>Calendario de entregas</h1>
  <p class="intro">La indumentaria se entrega en {["una", "dos", "tres", "cuatro", "cinco"][len(ent["entregas"]) - 1]} fechas, según el inicio de temporada de cada rama y el volumen de producción: primero la de los primeros equipos, las escuelas formativas, el cuerpo técnico y los directivos de las ramas que comienzan en marzo; después el stock para la tienda, y en el segundo semestre la de vóleibol y patín.</p>
  <div class="entregas tres">{"".join(tarjetas)}</div>
  <h2>PRENDAS POR ENTREGA</h2>
  <table class="tabla val res"><tr><th>RAMA</th><th class="n">PRIMER EQUIPO (CANJE)</th><th class="n">FORMATIVAS Y CT</th><th class="n">TIENDA</th><th class="n">TOTAL PRENDAS</th></tr>{"".join(filas)}</table>
  {pie(n)}
</section>""")
        n += 1

        cols_e = len(ent["nombres_entrega"])
        hitos = "".join(f'<tr{" class=sub" if k == len(ent["hitos"]) - 1 else ""}><td>{texto(h[0])}</td>'
                        + "".join(f'<td class="n">{fecha_corta(h[1 + j])}</td>' for j in range(cols_e))
                        + f'<td class="suave">{texto(h[1 + cols_e])}</td></tr>' for k, h in enumerate(ent["hitos"]))
        th_h = ("<tr><th>HITO</th>" + "".join(f'<th class="n">{x.replace(": ", "<br>")}</th>' for x in ent["nombres_entrega"])
                + "<th>DETALLE</th></tr>")
        paginas.append(f"""<section class="page">
  {cab("CRONOGRAMA")}
  <h1>Cronograma</h1>
  <p class="intro">Una vez aprobado el presupuesto, lo primero es firmar el contrato y emitir la orden de compra con el abono de la primera parte del pedido. Con eso acordado se trabajan los diseños, las muestras y las tallas, que quedan listos antes de fin de año para producir en enero y febrero.</p>
  <table class="tabla val crono c{cols_e}"><colgroup><col class="h">{'<col class="f">' * cols_e}<col class="d"></colgroup>{th_h}{hitos}</table>
  <p class="leyenda">La producción se fabrica según las muestras aprobadas, con supervisión y control de calidad de Playmaker. Cumplir estas fechas asegura cada entrega a tiempo.</p>
  {pie(n)}
</section>""")
        n += 1

        prop, por_millon = ent.get("proporcion", 0), ent.get("por_millon", 0)
        filas = []
        for x in ent["adelanto"]:  # entrega, compras, canje que se entrega, canje según las compras, diferencia
            filas.append(f'<tr><td>{texto(x[0])}</td><td class="n b">{pesos(x[1])}</td><td class="canje">{pesos(x[2])}</td></tr>')
        t = ent.get("total_adelanto") or [None] * 9
        filas.append(f'<tr class="total"><td>TOTAL</td><td class="n">{pesos(t[1])}</td><td class="n">{pesos(t[2])}</td></tr>')
        dif = ent["adelanto"][0][4] if ent["adelanto"] else 0
        f1 = fecha_txt(ent["entregas"][0][1]) if ent["entregas"] else ""
        cuadre = (f"La entrega del {f1} lleva más canje que el {pct(prop)} de sus compras, porque incluye a Esperanza "
                  f"Alba, que recibe solo canje, y el stock para la tienda llega en la entrega siguiente; las entregas "
                  f"siguientes llevan menos. En el total del año el canje queda exactamente en el {pct(prop)} de las "
                  f"compras. " if dif and dif > 0 else "")
        paginas.append(f"""<section class="page">
  {cab("CANJE PROPORCIONAL A LAS COMPRAS")}
  <h1>Canje proporcional a las compras</h1>
  <p class="intro">El canje de los primeros equipos es proporcional a lo que compra el club. En esta propuesta, el canje ({pesos(canje)}) equivale al {pct(prop)} de las compras ({pesos(ventas)}): por cada $1.000.000 que el club compra, recibe {pesos(por_millon)} en indumentaria en canje. Si el club compra menos, el canje baja en la misma proporción; si compra más, sube.</p>
  <div class="cifras tres">
    <div><small>PROPORCIÓN CANJE / COMPRAS</small><b>{pct(prop)}</b><span>del valor de las compras, con IVA</span></div>
    <div><small>POR CADA $1.000.000 EN COMPRAS</small><b>{pesos(por_millon)}</b><span>en canje, a valor formativas y cuerpo técnico</span></div>
    <div><small>EJEMPLO</small><b>{pesos(ent.get("sim_canje", 0))}</b><span>de canje si el club compra {pesos(ent.get("sim_compra", 0))}</span></div>
  </div>
  <h2>COMPRAS Y CANJE POR ENTREGA</h2>
  <table class="tabla val"><tr><th>ENTREGA</th><th class="n">COMPRAS DEL CLUB</th><th class="n">CANJE QUE SE ENTREGA</th></tr>{"".join(filas)}</table>
  <p class="leyenda">Valores con IVA incluido.</p>
  <div class="nota-caja"><b>CÓMO SE CUADRA EN EL AÑO</b>{cuadre}Si al cierre de la temporada las compras realizadas son menores a las de esta propuesta, el canje se ajusta a la misma proporción y la diferencia se liquida en ese momento.</div>
  {pie(n)}
</section>""")
        n += 1

    # 4. lista de precios por disciplina
    bloques = []
    for titulo, productos in disciplinas:
        b = [f'<tr class="sec"><td colspan="4">{titulo}</td></tr>']
        for p in productos:
            b.append(f'<tr><td>{p["producto"]}</td><td class="suave">{p["linea"]}</td>'
                     f'<td class="n b">{pesos(p["valor"])}</td><td class="n b">{pesos(p["comercial"])}</td></tr>')
        bloques.append(b)
    th = ('<tr><th>PRODUCTO</th><th>LÍNEA</th><th class="n">VALOR FORMATIVAS Y CUERPO TÉCNICO</th>'
          '<th class="n">PRECIO COMERCIAL TIENDA</th></tr>')
    for k, filas in enumerate(paginar(bloques, FILAS_PAGINA - 4)):
        intro = ('<p class="intro">Cada disciplina tiene sus propios productos y precios. El valor formativas y cuerpo '
                 'técnico es lo que paga el club por las escuelas formativas y el cuerpo técnico, y con él se calcula el '
                 'canje. El precio comercial es el del stock para la tienda del club.</p>' if k == 0 else "")
        paginas.append(f"""<section class="page detalle">
  {cab("LISTA DE PRECIOS")}
  <h1>Precios por disciplina{" (continuación)" if k else ""}</h1>
  {intro}
  <table class="tabla val precios"><colgroup><col class="p"><col class="l"><col class="m"><col class="m"></colgroup>{th}{"".join(filas)}</table>
  <p class="leyenda">Precios unitarios en pesos chilenos con IVA incluido.</p>
  {pie(n)}
</section>""")
        n += 1

    # 5. detalle por categoría
    textos = {
        "canje": ("CANJE PRIMEROS EQUIPOS", "Canje de los primeros equipos",
                  "Indumentaria de juego, entrenamiento y presentación de los primeros equipos, en canje. Se valoriza a valor formativas y cuerpo técnico."),
        "formativas": ("FORMATIVAS Y CUERPO TÉCNICO", "Formativas y cuerpo técnico",
                       "Compra del club para las escuelas formativas, el cuerpo técnico, el directorio y la oficina, a valor formativas y cuerpo técnico."),
        "comercial": ("COMERCIAL", "Stock para la tienda del club",
                      "Compra del club para vender en su tienda, a precio comercial."),
    }
    for clave, ramas in detalle.items():
        es_canje = clave == "canje"
        con_valor = es_canje  # el canje muestra el valor formativas y CT con que se valoriza
        cols = 4 + (1 if con_valor else 0) + (0 if es_canje else 1) + 1  # prenda, modelo, color, cantidad, precios, valor
        bloques = []
        for rama, items in ramas:
            items = [i for i in items if i["cantidad"]]
            if not items:
                continue
            b = [f'<tr class="sec"><td colspan="{cols}">{rama.upper()}</td></tr>']
            for i in items:
                valor = i["canje"] if es_canje else i["pagar"]
                b.append(f'<tr><td>{i["producto"]}</td><td>{i["modelo"]}</td><td class="co">{i["color"].replace("/", "/&#8203;")}</td><td class="n">{num(i["cantidad"])}</td>'
                         + (f'<td class="n">{pesos(i["valor"])}</td>' if con_valor else "")
                         + ("" if es_canje else f'<td class="n">{pesos(i["precio"])}</td>')
                         + (f'<td class="canje">{pesos(valor)}</td>' if es_canje else f'<td class="n b">{pesos(valor)}</td>') + "</tr>")
            st_u = sum(i["cantidad"] for i in items)
            st_v = sum(i["canje"] if es_canje else i["pagar"] for i in items)
            b.append(f'<tr class="sub"><td colspan="3">Total {rama.lower() if rama != "Esperanza Alba" else rama}</td><td class="n">{num(st_u)}</td>'
                     f'<td colspan="{cols - 5}"></td><td class="n">{pesos(st_v)}</td></tr>')
            bloques.append(b)
        tot_u = sum(i["cantidad"] for _, items in ramas for i in items)
        tot_v = sum(i["canje"] if es_canje else i["pagar"] for _, items in ramas for i in items)
        bloques.append([f'<tr class="total"><td colspan="3">TOTAL</td><td class="n">{num(tot_u)}</td><td colspan="{cols - 5}"></td>'
                        f'<td class="n">{pesos(tot_v)}</td></tr>'])
        th = ('<tr><th>PRENDA</th><th>MODELO</th><th>COLOR</th><th class="n">CANTIDAD</th>'
              + ('<th class="n">VALOR FORMATIVAS Y CT</th>' if con_valor else "")
              + ("" if es_canje else f'<th class="n">{"VALOR FORMATIVAS Y CT" if clave == "formativas" else "PRECIO COMERCIAL"}</th>')
              + ('<th class="n">VALOR DEL CANJE</th>' if es_canje else '<th class="n">VALOR A PAGAR</th>') + "</tr>")
        colg = ('<colgroup><col class="p"><col class="mo"><col class="co"><col class="u">'
                + '<col class="m">' * (cols - 4) + "</colgroup>")
        kick, titulo, intro = textos[clave]
        for k, filas in enumerate(paginar(bloques, FILAS_PAGINA - 3)):
            paginas.append(f"""<section class="page detalle">
  {cab(kick)}
  <h1>{titulo}{" (continuación)" if k else ""}</h1>
  {f'<p class="intro corta">{intro}</p>' if k == 0 else ""}
  <table class="tabla val det c{cols}">{colg}{th}{"".join(filas)}</table>
  <p class="leyenda">Valores en pesos chilenos con IVA incluido.{" Se incluyen las prendas con cantidad en la planilla de requerimientos del club." if not es_canje else ""}</p>
  {pie(n)}
</section>""")
            n += 1

    # 6. condiciones y próximos pasos
    def hito(nombre, i=0):
        h = next((x for x in (ent or {}).get("hitos", []) if texto(x[0]).startswith(nombre)), None)
        return fecha_txt(h[1 + i]) if h and h[1 + i] else None
    f_con, f_dis, f_vb = hito("Contrato"), hito("Aprobación de diseños"), hito("Visto bueno")
    fechas_ent = [fecha_txt(x[1]) for x in (ent or {}).get("entregas", [])]
    txt_ent = (", ".join(fechas_ent[:-1]) + " y el " + fechas_ent[-1]) if len(fechas_ent) > 1 else "".join(fechas_ent)
    paginas.append(f"""<section class="page portada cierre">
  <div class="kicker">CONDICIONES Y PRÓXIMOS PASOS</div>
  <h1>De la propuesta a la cancha</h1>
  <div class="pasos-cierre">
    <div><em>01</em><div><b>Contrato y orden de compra</b><p>Una vez aprobado el presupuesto, se firma el contrato y se emite la orden de compra con el abono de la primera parte del pedido{f", a más tardar el {f_con}" if f_con else ""}.</p></div></div>
    <div><em>02</em><div><b>Aprobación de diseños</b><p>El club aprueba los diseños de juego, entrenamiento y presentación de cada rama{f", a más tardar el {f_dis}" if f_dis else ""}.</p></div></div>
    <div><em>03</em><div><b>Muestras y tallas</b><p>Playmaker entrega muestras de cada prenda. Con el visto bueno del club y la curva de tallas{f" ({f_vb})" if f_vb else ""}, la producción se fabrica según las muestras aprobadas.</p></div></div>
    <div><em>04</em><div><b>Producción y entregas</b><p>Producción con supervisión y control de calidad de Playmaker{f"; entregas el {txt_ent}" if txt_ent else ""}. El valor final se ajusta a las cantidades confirmadas.</p></div></div>
  </div>
  <p class="lema">Volver a vestir a las ramas del Colo-Colo.</p>
  <div class="firma"><b>Sean Duarte</b><span>Dueño y CEO de Playmaker SpA</span><span>sduarte@playmaker.cl, +56 9 3928 3323, www.playmaker.cl</span></div>
  {pie(n)}
</section>""")

    css = (DIR / "estilo_propuesta.css").read_text(encoding="utf-8")
    HTML.write_text(f"""<!doctype html>
<!-- Generado por generar_pdf.py desde la planilla de la propuesta: no editar a mano. -->
<html lang="es"><head><meta charset="utf-8"><title>Propuesta comercial CSD Colo-Colo 2027</title>
<style>
{css}</style></head><body>
{chr(10).join(paginas)}
</body></html>
""", encoding="utf-8")
    subprocess.run(["bash", str(DIR.parent / "html_a_pdf.sh"), str(HTML), str(PDF)], check=True, stdout=subprocess.DEVNULL)
    print(f"OK  {PDF.name}  ({n} páginas; canje {pesos(canje)}, compras {pesos(ventas)})")


if __name__ == "__main__":
    main()
