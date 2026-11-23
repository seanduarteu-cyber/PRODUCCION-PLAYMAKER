"""PDF para la federación con la valorización del convenio, armado desde la planilla de valorización.

Uso:
    python3 propuestas/fevochi-2027/generar_pdf.py

Lee Valorizacion_Ropa_Selecciones_FEVOCHI_2027.xlsx (los valores que la planilla tiene calculados) y crea
valorizacion_fevochi.html y Propuesta_Valorizacion_FEVOCHI_2027.pdf. Si se cambian precios, descuentos, canje o
cantidades en la planilla, basta guardarla y volver a correr este script. Si la planilla no trae valores
calculados (por ejemplo, recién generada con generar_valorizacion.py), se recalcula con LibreOffice.
"""

import subprocess
import sys
from pathlib import Path

import openpyxl

DIR = Path(__file__).parent
PLANILLA = DIR / "Valorizacion_Ropa_Selecciones_FEVOCHI_2027.xlsx"
HTML = DIR / "valorizacion_fevochi.html"
PDF = DIR / "Propuesta_Valorizacion_FEVOCHI_2027.pdf"
FECHA = "Santiago, 23 de noviembre de 2026"
RECALC = Path("/root/.claude/skills/synced/bc307280-4611-44d6-aa94-f2bad7ad32ae_766667a6-21fa-41c9-a3ab-adb5c42c724e/"
              "xlsx/scripts/recalc.py")


def pesos(n):
    return "$" + f"{round(n or 0):,}".replace(",", ".")


def num(n):
    return f"{round(n or 0):,}".replace(",", ".")


def pct(x):
    return f"{x * 100:.0f}%".replace(".", ",") if abs(x * 100 - round(x * 100)) < 0.05 else f"{x * 100:.1f}%".replace(".", ",")


def libro():
    wb = openpyxl.load_workbook(PLANILLA, data_only=True)
    if wb["RESUMEN"]["G6"].value is None:  # sin valores calculados
        if not RECALC.exists():
            sys.exit("La planilla no tiene valores calculados: ábrela en Excel, guárdala y vuelve a correr el script.")
        subprocess.run([sys.executable, str(RECALC), str(PLANILLA), "90"], check=True, stdout=subprocess.DEVNULL)
        wb = openpyxl.load_workbook(PLANILLA, data_only=True)
    return wb


def leer(wb):
    pr = wb["PRECIOS"]
    general = pr["C5"].value or 0
    precios = []
    for r in range(8, pr.max_row + 1):
        if pr.cell(r, 2).value and pr.cell(r, 5).value is not None:
            d = pr.cell(r, 4).value
            precios.append({"prenda": pr.cell(r, 2).value, "publico": pr.cell(r, 3).value or 0,
                            "descuento": general if d is None else d, "federacion": pr.cell(r, 5).value or 0})

    rs = wb["RESUMEN"]
    resumen, por_prenda, r = [], [], 6
    while r <= rs.max_row and rs.cell(r, 2).value != "TOTAL GENERAL":
        resumen.append([rs.cell(r, c).value for c in range(2, 10)])
        r += 1
    total = [rs.cell(r, c).value for c in range(2, 10)]
    while r <= rs.max_row and rs.cell(r, 2).value != "PRENDA":
        r += 1
    r += 1
    while r <= rs.max_row and rs.cell(r, 2).value != "TOTAL":
        if rs.cell(r, 2).value:
            por_prenda.append({"prenda": rs.cell(r, 2).value, "unidades": rs.cell(r, 7).value or 0,
                               "canje": rs.cell(r, 8).value or 0, "federacion": rs.cell(r, 9).value or 0})
        r += 1

    def bloques(ws, cols):
        """[(título, [(categoría, filas, subtotal)])] con filas: dict por prenda."""
        salida, actual, cat, filas = [], None, None, []
        for r in range(5, ws.max_row + 1):
            b = ws.cell(r, 2).value
            v = {k: ws.cell(r, c).value for k, c in cols.items()}
            if isinstance(b, str) and (b.startswith("SELECCIÓN") or b.startswith("CUERPO TÉCNICO")):
                actual = (b, [])
                salida.append(actual)
                cat, filas = (None if b.startswith("SELECCIÓN") else b), []
            elif isinstance(b, str) and b.startswith("Total "):
                actual[1].append((cat, filas, v))
                filas = []
            elif isinstance(b, str) and b.startswith("TOTAL ") and cat and not filas == []:
                actual[1].append((cat, filas, v))
                filas = []
            elif v.get("prenda") and isinstance(v.get("unidades"), (int, float)):
                if b and actual[0].startswith("SELECCIÓN"):
                    cat = b
                filas.append(v)
        return salida

    se = bloques(wb["SELECCIONES ROPA 2027"], {"prenda": 4, "colores": 5, "por": 6, "unidades": 7, "publico": 8,
                                               "federacion": 9, "canje": 10, "valor": 11})
    ct = bloques(wb["CUERPO TÉCNICO 2027"], {"prenda": 2, "personas": 3, "por": 4, "unidades": 5, "publico": 6,
                                             "federacion": 7, "canje": 8, "valor": 9})
    return precios, resumen, total, por_prenda, se, ct


def pie(num_pag):
    return (f'<div class="pie"><span>UN CLUB, UNA FAMILIA.</span>'
            f'<img src="../_recursos/playmaker_logo_horizontal_navy.png" alt="Playmaker"><span class="num">{num_pag:02d}</span></div>')


def cab(izq, der="SELECCIONES NACIONALES DE VÓLEIBOL"):
    return f'<div class="cab"><b>{izq}</b><span>{der}</span></div>'


def tabla_detalle(categorias, persona="jugador", rotulos=True):
    filas = []
    for cat, items, sub in categorias:
        en_canje = all(i["canje"] == "SÍ" for i in items)
        titulo = f"{cat}{' (canje)' if en_canje else ''}"
        if rotulos:
            filas.append(f'<tr class="sec"><td colspan="7">{titulo.upper()}</td></tr>')
        for i in items:
            canje = i["canje"] == "SÍ"
            precio = i["publico"] if canje else i["federacion"]
            valor_canje = i["unidades"] * i["publico"] if canje else 0
            filas.append(
                f'<tr><td>{i["prenda"]}</td><td>{i.get("colores") or ""}</td><td class="n">{num(i["por"])}</td>'
                f'<td class="n">{num(i["unidades"])}</td><td class="n">{pesos(precio)}</td>'
                f'<td class="canje">{pesos(valor_canje) if canje else ""}</td>'
                f'<td class="n b">{"" if canje else pesos(i["valor"])}</td></tr>')
        canje_total = sum(i["unidades"] * i["publico"] for i in items if i["canje"] == "SÍ")
        filas.append(f'<tr class="sub"><td colspan="3">{"Total " + cat if rotulos else "Total"}</td><td class="n">{num(sub["unidades"])}</td><td></td>'
                     f'<td class="canje">{pesos(canje_total) if canje_total else ""}</td>'
                     f'<td class="n">{pesos(sub["valor"]) if sub["valor"] else ""}</td></tr>')
    return (f'<table class="tabla val det"><colgroup><col class="p"><col class="c"><col class="x"><col class="u">'
            f'<col class="m"><col class="m"><col class="m"></colgroup><tr><th>PRENDA</th><th>COLORES</th><th class="n">POR {persona.upper()}</th>'
            f'<th class="n">UNIDADES</th><th class="n">PRECIO UNITARIO</th><th class="n">VALOR CANJE</th>'
            f'<th class="n">VALOR FEDERACIÓN</th></tr>{"".join(filas)}</table>')


def main():
    precios, resumen, total, por_prenda, se, ct = leer(libro())
    unidades, canje, federacion, neto, iva = total[3], total[4], total[5], total[6], total[7]
    descuentos = {round(p["descuento"], 4) for p in precios if p["publico"]}
    desc_txt = pct(descuentos.pop()) if len(descuentos) == 1 else "variable"
    publico_pagado = sum(p["publico"] * x["unidades"] for p in precios for x in por_prenda if x["prenda"] == p["prenda"]) \
        - sum(x["canje"] for x in por_prenda)
    beneficio = canje + max(publico_pagado - federacion, 0)
    paginas = []

    # 1. portada
    paginas.append(f"""<section class="page portada">
  <div class="logos"><img class="pm" src="../_recursos/playmaker_logo_horizontal_blanco.png" alt="Playmaker"><i></i>
    <img class="fev" src="logo_fevochi.png" alt="Federación de Vóleibol de Chile"></div>
  <div class="kicker">PROPUESTA DE INDUMENTARIA 2027</div>
  <h1>Selecciones Nacionales<br>de Vóleibol</h1>
  <p class="sub">Valorización del convenio con la Federación de Vóleibol de Chile: selecciones de piso y playa, masculinas y femeninas, y sus cuerpos técnicos</p>
  <div class="regla"></div>
  <div class="ligas"><div><b>{num(unidades)}</b><span>prendas en total</span></div><div><b>4</b><span>selecciones nacionales</span></div><div><b>{desc_txt}</b><span>descuento federación</span></div></div>
  <div class="firma"><small>PRESENTADA POR</small><b>Sean Duarte</b><span>Playmaker SpA, sduarte@playmaker.cl, +56 9 3928 3323</span><span>{FECHA}</span></div>
  {pie(1)}
</section>""")

    # 2. resumen del convenio
    filas = []
    for sel, cat, jug, unid, cj, fed, nt, iv in resumen:
        clase = ' class="sub"' if sel and str(sel).startswith("Total") else ""
        filas.append(f'<tr{clase}><td>{sel or ""}</td><td>{cat or ""}</td><td class="n">{num(jug)}</td><td class="n">{num(unid)}</td>'
                     f'<td class="canje">{pesos(cj) if cj else ""}</td><td class="n b">{pesos(fed) if fed else ""}</td></tr>')
    filas.append(f'<tr class="total"><td colspan="2">TOTAL DEL CONVENIO</td><td class="n">{num(total[2])}</td>'
                 f'<td class="n">{num(unidades)}</td><td class="n">{pesos(canje)}</td><td class="n">{pesos(federacion)}</td></tr>')
    paginas.append(f"""<section class="page">
  {cab("RESUMEN DEL CONVENIO")}
  <h1>Valorización del convenio</h1>
  <p class="intro">Playmaker propone vestir a las selecciones nacionales de vóleibol en 2027 con un modelo mixto: los equipos adultos de las cuatro selecciones reciben su indumentaria en canje, y las categorías menores y los cuerpos técnicos la compran a precio federación, con un {desc_txt} de descuento sobre el precio público general. Las cantidades corresponden a la proyección de la federación.</p>
  <div class="cifras">
    <div><small>PRENDAS</small><b>{num(unidades)}</b><span>en 4 selecciones y 3 cuerpos técnicos</span></div>
    <div><small>VALOR DEL CANJE</small><b>{pesos(canje)}</b><span>equipos adultos, a precio público general</span></div>
    <div><small>COMPRA FEDERACIÓN</small><b>{pesos(federacion)}</b><span>a precio federación, IVA incluido</span></div>
    <div><small>BENEFICIO TOTAL</small><b>{pesos(beneficio)}</b><span>canje más descuento sobre las compras</span></div>
  </div>
  <h2>VALOR POR SELECCIÓN Y CATEGORÍA</h2>
  <table class="tabla val res"><tr><th>SELECCIÓN</th><th>CATEGORÍA</th><th class="n">JUGADORES</th><th class="n">UNIDADES</th><th class="n">VALOR CANJE</th><th class="n">VALOR FEDERACIÓN</th></tr>{"".join(filas)}</table>
  <p class="leyenda">Valores en pesos chilenos con IVA incluido. El valor del canje se calcula a precio público general. La compra a precio federación suma {pesos(neto)} neto más {pesos(iva)} de IVA.</p>
  {pie(2)}
</section>""")

    # 3. precios y valor por prenda
    fp = {x["prenda"]: x for x in por_prenda}
    filas = []
    for p in precios:
        x = fp.get(p["prenda"], {"unidades": 0, "canje": 0, "federacion": 0})
        if not x["unidades"]:
            continue
        filas.append(f'<tr><td>{p["prenda"]}</td><td class="n">{pesos(p["publico"])}</td><td class="n">{pct(p["descuento"])}</td>'
                     f'<td class="n b">{pesos(p["federacion"])}</td><td class="n">{num(x["unidades"])}</td>'
                     f'<td class="canje">{pesos(x["canje"]) if x["canje"] else ""}</td><td class="n b">{pesos(x["federacion"])}</td></tr>')
    filas.append(f'<tr class="total"><td colspan="4">TOTAL</td><td class="n">{num(unidades)}</td><td class="n">{pesos(canje)}</td>'
                 f'<td class="n">{pesos(federacion)}</td></tr>')
    paginas.append(f"""<section class="page">
  {cab("PRECIOS Y VALOR POR PRENDA")}
  <h1>Precios por prenda</h1>
  <p class="intro">Cada prenda tiene un precio público general y un precio federación, que es el que paga la federación por las categorías menores y los cuerpos técnicos. Las prendas de los equipos adultos van en canje y se valorizan a precio público general.</p>
  <table class="tabla val"><tr><th>PRENDA</th><th class="n">PRECIO PÚBLICO</th><th class="n">DESCUENTO</th><th class="n">PRECIO FEDERACIÓN</th><th class="n">UNIDADES</th><th class="n">VALOR CANJE</th><th class="n">VALOR FEDERACIÓN</th></tr>{"".join(filas)}</table>
  <p class="leyenda">Precios unitarios en pesos chilenos con IVA incluido.</p>
  <div class="nota-caja"><b>CONDICIONES DE LA PROPUESTA</b>El canje cubre el 100% de las prendas indicadas para los equipos adultos de las selecciones de piso y playa, masculinas y femeninas. Las categorías menores y los cuerpos técnicos se facturan a precio federación. Las cantidades, colores y diseños se confirman con la federación antes de producir, y el valor final se ajusta a las cantidades confirmadas.</div>
  {pie(3)}
</section>""")

    # 4 en adelante: detalle por selección (piso: una por página; playa: las dos juntas; cuerpos técnicos)
    n = 4
    piso = [b for b in se if "PLAYA" not in b[0]]
    playa = [b for b in se if "PLAYA" in b[0]]
    for titulo, cats in piso:
        persona = "jugador" if "MASCULINA" in titulo else "jugadora"
        paginas.append(f"""<section class="page detalle">
  {cab("DETALLE POR SELECCIÓN")}
  <h1>{titulo.replace("SELECCIÓN", "Selección").replace("MASCULINA", "masculina").replace("FEMENINA", "femenina").replace("PISO", "de piso")}</h1>
  {tabla_detalle(cats, persona)}
  <p class="leyenda">En las categorías en canje el precio unitario es el precio público general; en las demás, el precio federación. Valores con IVA incluido.</p>
  {pie(n)}
</section>""")
        n += 1
    for titulo, cats in playa:
        persona = "jugador" if "MASCULINA" in titulo else "jugadora"
        nombre = "masculina" if "MASCULINA" in titulo else "femenina"
        paginas.append(f"""<section class="page detalle">
  {cab("DETALLE POR SELECCIÓN")}
  <h1>Selección {nombre} de vóleibol playa</h1>
  {tabla_detalle(cats, persona)}
  <p class="leyenda">En las categorías en canje el precio unitario es el precio público general; en las demás, el precio federación. Valores con IVA incluido.</p>
  {pie(n)}
</section>""")
        n += 1
    cuerpo = []
    for titulo, cats in ct:
        personas = cats[0][1][0]["personas"] if cats and cats[0][1] else 0
        nombre = titulo.replace("CUERPO TÉCNICO ", "").lower()
        cuerpo.append(f'<h2>CUERPO TÉCNICO {nombre.upper()} ({num(personas)} PERSONAS)</h2>'
                      + tabla_detalle(cats, "persona", rotulos=False))
    paginas.append(f"""<section class="page detalle">
  {cab("DETALLE POR SELECCIÓN")}
  <h1>Cuerpos técnicos</h1>
  {"".join(cuerpo)}
  <p class="leyenda">Valores con IVA incluido.</p>
  {pie(n)}
</section>""")
    n += 1

    # cierre
    paginas.append(f"""<section class="page portada cierre">
  <div class="kicker">PRÓXIMOS PASOS</div>
  <h1>De la propuesta a la cancha</h1>
  <div class="pasos-cierre">
    <div><em>01</em><div><b>Revisión de la valorización</b><p>La federación confirma las cantidades por categoría y las prendas de cada selección.</p></div></div>
    <div><em>02</em><div><b>Diseño de las selecciones</b><p>Playmaker presenta los diseños y colores de cada uniforme para su aprobación.</p></div></div>
    <div><em>03</em><div><b>Tallas y firma del convenio</b><p>La federación entrega la curva de tallas por categoría y se firman las condiciones.</p></div></div>
    <div><em>04</em><div><b>Producción y entrega</b><p>Confección en planta propia en Santiago y entrega por selección, según el calendario de competencias.</p></div></div>
  </div>
  <p class="lema">"Un club, una familia."</p>
  <div class="firma"><b>Sean Duarte</b><span>Playmaker SpA</span><span>sduarte@playmaker.cl, +56 9 3928 3323, www.playmaker.cl</span></div>
  {pie(n)}
</section>""")

    css = (DIR / "estilo_valorizacion.css").read_text(encoding="utf-8")
    HTML.write_text(f"""<!doctype html>
<!-- Generado por generar_pdf.py desde la planilla de valorización: no editar a mano. -->
<html lang="es"><head><meta charset="utf-8"><title>Valorización convenio FEVOCHI 2027</title>
<style>
{css}</style></head><body>
{chr(10).join(paginas)}
</body></html>
""", encoding="utf-8")
    subprocess.run(["bash", str(DIR.parent / "html_a_pdf.sh"), str(HTML), str(PDF)], check=True, stdout=subprocess.DEVNULL)
    print(f"OK  {PDF.name}  ({n} páginas; canje {pesos(canje)}, compra federación {pesos(federacion)})")


if __name__ == "__main__":
    main()
