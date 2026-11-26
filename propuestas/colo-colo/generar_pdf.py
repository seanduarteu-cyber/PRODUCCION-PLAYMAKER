"""PDF de la propuesta comercial 2027 para presentar al CSD Colo-Colo, armado desde la planilla de la propuesta.

Uso:
    python3 propuestas/colo-colo/generar_pdf.py

Lee Propuesta_Comercial_CSD_Colo_Colo_2027.xlsm (los valores que la planilla tiene calculados) y crea
propuesta_club.html y Propuesta_Comercial_CSD_Colo_Colo_2027.pdf: portada, resumen de la propuesta, lista de precios
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
    descuentos = {}
    for r in range(4, 9):
        etq = texto(pr.cell(r, 2).value).lower()
        for clave in HOJAS:
            if clave in etq:
                descuentos[clave] = pr.cell(r, 3).value or 0
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
                                       "publico": pr.cell(r, 4).value or 0, "formativas": pr.cell(r, 8).value or 0,
                                       "comercial": pr.cell(r, 10).value or 0})

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
                                 "cantidad": ws.cell(r, 9).value or 0, "publico": ws.cell(r, 10).value or 0,
                                 "precio": ws.cell(r, 11).value or 0, "valor_publico": ws.cell(r, 12).value or 0,
                                 "pagar": ws.cell(r, 13).value or 0, "canje": ws.cell(r, 14).value or 0})
        detalle[clave] = ramas
    return descuentos, disciplinas, resumen, total, detalle


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
    descuentos, disciplinas, resumen, total, detalle = leer(libro())
    unidades, canje, ventas, neto, iva = total[2], total[3], total[4], total[5], total[6]
    hoy = date.today()
    fecha = f"Santiago, {hoy.day} de {MESES[hoy.month - 1]} de {hoy.year}"
    tot_cat = {}
    for fila in resumen:
        if texto(fila[0]).startswith("Total "):
            clave = next(c for c in HOJAS if c in texto(fila[0]).lower() or (c == "canje" and "canje" in texto(fila[0]).lower()))
            tot_cat[clave] = fila
    ramas_dep = [r for r, _ in detalle["canje"]]
    d_fo, d_co = descuentos.get("formativas", 0), descuentos.get("comercial", 0)
    txt_fo = f"con un {pct(d_fo)} de descuento sobre el precio público" if d_fo else "a precio de lista"
    txt_co = f"con un {pct(d_co)} de descuento sobre el precio público" if d_co else "a precio de lista"
    paginas = []
    n = 1

    # 1. portada
    paginas.append(f"""<section class="page portada">
  <img class="logo" src="../_recursos/playmaker_logo_horizontal_blanco.png" alt="Playmaker">
  <div class="kicker">PROPUESTA COMERCIAL 2027</div>
  <h1>Ramas deportivas del<br>CSD Colo-Colo</h1>
  <p class="sub">Indumentaria de juego, entrenamiento y presentación para los primeros equipos, las series formativas, el cuerpo técnico y la tienda del club</p>
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
  <p class="intro">Playmaker propone vestir a las ramas deportivas del CSD Colo-Colo en 2027 en tres partes: los primeros equipos de {", ".join(r.lower() if r != "Esperanza Alba" else r for r in ramas_dep[:-1])} y {ramas_dep[-1] if ramas_dep[-1] == "Esperanza Alba" else ramas_dep[-1].lower()} reciben su indumentaria en canje (100% de descuento); las series formativas, el cuerpo técnico, el directorio y la oficina la compran {txt_fo}, y el club compra stock para su tienda {txt_co}. Las cantidades son las de la planilla de requerimientos del club.</p>
  <div class="cifras">
    <div><small>PRENDAS</small><b>{num(unidades)}</b><span>canje, formativas y comercial</span></div>
    <div><small>VALOR DEL CANJE</small><b>{pesos(canje)}</b><span>primeros equipos, a precio público</span></div>
    <div><small>FORMATIVAS Y CUERPO TÉCNICO</small><b>{pesos(fo[4])}</b><span>{num(fo[2])} prendas, IVA incluido</span></div>
    <div><small>STOCK PARA LA TIENDA</small><b>{pesos(co[4])}</b><span>{num(co[2])} prendas, IVA incluido</span></div>
  </div>
  <h2>VALOR POR CATEGORÍA Y RAMA</h2>
  <table class="tabla val res"><tr><th>CATEGORÍA</th><th>RAMA</th><th class="n">PRENDAS</th><th class="n">VALOR DEL CANJE</th><th class="n">VALOR A PAGAR</th></tr>{"".join(filas)}</table>
  <p class="leyenda">Valores en pesos chilenos con IVA incluido. El valor del canje se calcula a precio público. Las compras suman {pesos(neto)} neto más {pesos(iva)} de IVA.</p>
  {pie(n)}
</section>""")
    n += 1

    # 3. lista de precios por disciplina
    bloques = []
    for titulo, productos in disciplinas:
        b = [f'<tr class="sec"><td colspan="5">{titulo}</td></tr>']
        for p in productos:
            b.append(f'<tr><td>{p["producto"]}</td><td class="suave">{p["linea"]}</td><td class="n">{pesos(p["publico"])}</td>'
                     f'<td class="n b">{pesos(p["formativas"])}</td><td class="n b">{pesos(p["comercial"])}</td></tr>')
        bloques.append(b)
    th = ('<tr><th>PRODUCTO</th><th>LÍNEA</th><th class="n">PRECIO PÚBLICO</th><th class="n">PRECIO FORMATIVAS Y CT</th>'
          '<th class="n">PRECIO COMERCIAL</th></tr>')
    for k, filas in enumerate(paginar(bloques, FILAS_PAGINA - 4)):
        entre = lambda d: f"({pct(d)} de descuento)" if d else "(precio de lista)"  # noqa: E731
        intro = (f'<p class="intro">Cada disciplina tiene sus propios productos y precios. El precio público valoriza el '
                 f'canje de los primeros equipos; el precio formativas y cuerpo técnico es el que paga el club por las series '
                 f'formativas y el cuerpo técnico {entre(d_fo)}, y el precio comercial, el del stock para su tienda '
                 f'{entre(d_co)}.</p>' if k == 0 else "")
        paginas.append(f"""<section class="page detalle">
  {cab("LISTA DE PRECIOS")}
  <h1>Precios por disciplina{" (continuación)" if k else ""}</h1>
  {intro}
  <table class="tabla val precios"><colgroup><col class="p"><col class="l"><col class="m"><col class="m"><col class="m"></colgroup>{th}{"".join(filas)}</table>
  <p class="leyenda">Precios unitarios en pesos chilenos con IVA incluido.</p>
  {pie(n)}
</section>""")
        n += 1

    # 4. detalle por categoría
    textos = {
        "canje": ("CANJE PRIMEROS EQUIPOS", "Canje de los primeros equipos",
                  "Indumentaria de juego, entrenamiento y presentación de los primeros equipos, en canje (100% de descuento). Se valoriza a precio público."),
        "formativas": ("FORMATIVAS Y CUERPO TÉCNICO", "Formativas y cuerpo técnico",
                       f"Compra del club para las series formativas, el cuerpo técnico, el directorio y la oficina, {txt_fo}."),
        "comercial": ("COMERCIAL", "Stock para la tienda del club",
                      f"Compra del club para vender en su tienda, {txt_co}."),
    }
    for clave, ramas in detalle.items():
        es_canje = clave == "canje"
        con_publico = es_canje or any(i["publico"] != i["precio"] for _, items in ramas for i in items)
        cols = 4 + (1 if con_publico else 0) + (0 if es_canje else 1) + 1  # prenda, modelo, color, cantidad, precios, valor
        bloques = []
        for rama, items in ramas:
            items = [i for i in items if i["cantidad"]]
            if not items:
                continue
            b = [f'<tr class="sec"><td colspan="{cols}">{rama.upper()}</td></tr>']
            for i in items:
                valor = i["canje"] if es_canje else i["pagar"]
                b.append(f'<tr><td>{i["producto"]}</td><td>{i["modelo"]}</td><td class="co">{i["color"].replace("/", "/&#8203;")}</td><td class="n">{num(i["cantidad"])}</td>'
                         + (f'<td class="n">{pesos(i["publico"])}</td>' if con_publico else "")
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
              + ('<th class="n">PRECIO PÚBLICO</th>' if con_publico else "")
              + ("" if es_canje else f'<th class="n">PRECIO {"FORMATIVAS Y CT" if clave == "formativas" else "COMERCIAL"}</th>')
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

    # 5. condiciones y próximos pasos
    paginas.append(f"""<section class="page portada cierre">
  <div class="kicker">CONDICIONES Y PRÓXIMOS PASOS</div>
  <h1>De la propuesta a la cancha</h1>
  <div class="pasos-cierre">
    <div><em>01</em><div><b>Revisión de la propuesta</b><p>El club confirma las prendas, las cantidades por rama y los precios de cada categoría. El valor final se ajusta a las cantidades confirmadas.</p></div></div>
    <div><em>02</em><div><b>Diseño de cada rama</b><p>Playmaker presenta los diseños de juego, entrenamiento y presentación, con la identidad del club, para su aprobación antes de producir.</p></div></div>
    <div><em>03</em><div><b>Tallas y firma del acuerdo</b><p>El club entrega la curva de tallas por rama y categoría, y se firman las condiciones del canje y de las compras.</p></div></div>
    <div><em>04</em><div><b>Producción y entrega</b><p>Confección en planta propia en Santiago, en 10 a 15 días hábiles desde la aprobación del diseño, con entrega por rama.</p></div></div>
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
