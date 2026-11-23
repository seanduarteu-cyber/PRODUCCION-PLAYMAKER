"""Valorización de la ropa de las selecciones de vóleibol (FEVOCHI) 2027, a partir de la proyección del cliente.

Uso:
    python3 propuestas/fevochi-2027/generar_valorizacion.py

Lee Proyeccion_Ropa_Selecciones_FEVOCHI_2027_original.xlsx (hojas SELECCIONES ROPA 2027 y CUERPO TÉCNICO 2027:
jugadores por categoría y prendas por jugador, con colores escritos junto a la cantidad, p. ej. "2 roja-azul")
y crea Valorizacion_Ropa_Selecciones_FEVOCHI_2027.xlsx:
  - RESUMEN: valor por selección y categoría a precio federación, canje, total a pagar, neto e IVA, y valor por
    prenda.
  - SELECCIONES ROPA 2027 y CUERPO TÉCNICO 2027: una fila por categoría y prenda: unidades por jugador, total de
    unidades, precio público (solo referencia), precio federación, canje (SÍ: 100% de descuento en esa prenda; viene
    marcado en los equipos adultos de todas las selecciones) y valor a pagar.
  - PRECIOS: por prenda, precio público general, descuento y precio federación (todos con IVA). El descuento
    general se aplica a las prendas sin descuento propio.
Si la planilla de valorización ya existe, se conservan los precios, jugadores y unidades que tenga cargados.
"""

import re
from pathlib import Path

import openpyxl
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

DIR = Path(__file__).parent
ORIGEN = DIR / "Proyeccion_Ropa_Selecciones_FEVOCHI_2027_original.xlsx"
SALIDA = DIR / "Valorizacion_Ropa_Selecciones_FEVOCHI_2027.xlsx"
IVA = 0.19

# prendas con precio propio, por grupo (el nombre es la llave entre hojas: no cambiarlo en una sola parte)
PRENDAS = [
    ("LÍNEA DE JUEGO PISO", ["Camiseta de juego piso", "Short de juego piso", "Calza de juego piso"]),
    ("LÍNEA DE JUEGO PLAYA", ["Camiseta de juego playa", "Short de juego playa", "Bikini de juego playa"]),
    ("ENTRENAMIENTO Y PRESENTACIÓN", ["Buzo completo (polerón y pantalón)", "Polera de entrenamiento",
                                      "Polera de presentación", "Short de presentación",
                                      "Short o calza de presentación"]),
]
# columna de la proyección del cliente -> prenda, según el encabezado y el tipo de selección
def prenda_de(encabezado, playa):
    e = encabezado.upper()
    if "CAMISETA" in e:
        return "Camiseta de juego playa" if playa else "Camiseta de juego piso"
    if "CALZA" in e and "SHORT" in e:
        return "Short o calza de presentación"
    if "CALZA" in e:
        return "Calza de juego piso"
    if "BIKINI" in e:
        return "Bikini de juego playa"
    if "SHORT" in e and "PRESENTACI" in e:
        return "Short de presentación"
    if "SHORT" in e:
        return "Short de juego playa" if playa else "Short de juego piso"
    if "BUZO" in e:
        return "Buzo completo (polerón y pantalón)"
    if "ENTRENAMIENTO" in e:
        return "Polera de entrenamiento"
    if "PRESENTACI" in e:
        return "Polera de presentación"
    raise SystemExit(f"Prenda sin precio definido: {encabezado}")


def unidades_y_colores(valor):
    """'2 roja-azul' -> (2, 'Rojo y azul'); '2 azul-1 rojo' -> (3, '2 azul y 1 rojo'); 2 -> (2, '')."""
    if isinstance(valor, (int, float)):
        return int(valor), ""
    partes = [p.strip() for p in str(valor).split("-") if p.strip()]
    con_numero = [re.match(r"(\d+)\s*(.*)", p) for p in partes]
    genero = {"roja": "rojo", "blanca": "blanco", "negra": "negro"}
    if sum(1 for m in con_numero if m) > 1:  # cantidades por color
        items = [(int(m.group(1)), genero.get(m.group(2).lower(), m.group(2).lower())) for m in con_numero if m]
        return sum(n for n, _ in items), lista([f"{n} {c}" for n, c in items])
    m = con_numero[0]
    if not m:
        raise SystemExit(f"Cantidad sin número: {valor}")
    colores = [m.group(2)] + partes[1:]
    colores = [genero.get(c.lower(), c.lower()) for c in colores if c]
    if colores and len(colores) != int(m.group(1)):
        raise SystemExit(f"La cantidad no calza con los colores: {valor}")
    return int(m.group(1)), lista(colores).capitalize()


def lista(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " y " + xs[-1]


def texto(v):
    return " ".join(str(v or "").split())


def leer_proyeccion():
    wb = openpyxl.load_workbook(ORIGEN)
    selecciones = []  # (título, [(categoría, jugadores, [(prenda, unidades, colores)])])
    ws = wb["SELECCIONES ROPA 2027"]
    r = 1
    while r <= ws.max_row:
        b = texto(ws.cell(r, 2).value)
        if b.upper().startswith("SELECCIÓN"):
            playa = "PLAYA" in b.upper()
            cab = [texto(ws.cell(r + 1, c).value) for c in range(4, 9)]
            prendas = [prenda_de(h, playa) for h in cab]
            cats, f = [], r + 2
            while f <= ws.max_row and ws.cell(f, 2).value:
                items = [(p, *unidades_y_colores(ws.cell(f, 4 + k).value)) for k, p in enumerate(prendas)]
                cats.append((texto(ws.cell(f, 2).value), ws.cell(f, 3).value, items))
                f += 1
            selecciones.append((b, cats))
            r = f
        r += 1
    tecnicos = []  # (título, personas, [(prenda, unidades)])
    ws = wb["CUERPO TÉCNICO 2027"]
    for r in range(1, ws.max_row + 1):
        b = texto(ws.cell(r, 2).value)
        m = re.match(r"(CUERPO TÉCNICO.*?)\s*\(\s*(\d+)\s*PERSONAS\s*\)", b.upper())
        if m:
            titulo = re.sub(r"\s*\(.*", "", b).strip()
            items, f = [], r + 2
            while f <= ws.max_row and ws.cell(f, 2).value:
                items.append((prenda_de(texto(ws.cell(f, 2).value), "PLAYA" in b.upper()), int(ws.cell(f, 3).value)))
                f += 1
            tecnicos.append((titulo, int(m.group(2)), items))
    return selecciones, tecnicos


def leer_previo():
    """Valores ya cargados en la valorización (precios, jugadores, unidades), para no perderlos."""
    if not SALIDA.exists():
        return None
    wb = openpyxl.load_workbook(SALIDA)
    previo = {"precios": {}, "iva": None, "descuento": None, "celdas": {}}
    pr = wb["PRECIOS"]
    for r in range(8, pr.max_row + 1):
        if pr.cell(r, 2).value:  # público, descuento propio, observaciones
            previo["precios"][texto(pr.cell(r, 2).value)] = (pr.cell(r, 3).value, pr.cell(r, 4).value,
                                                             pr.cell(r, 7).value)
    previo["iva"], previo["descuento"] = pr["C4"].value, pr["C5"].value
    for hoja in ("SELECCIONES ROPA 2027", "CUERPO TÉCNICO 2027"):
        ws = wb[hoja]
        for row in ws.iter_rows():
            for c in row:
                if c.font and c.font.color is not None and c.font.color.rgb == "FF0000FF" and c.value is not None:
                    previo["celdas"][(hoja, c.coordinate)] = c.value
    return previo


def main():
    selecciones, tecnicos = leer_proyeccion()
    previo = leer_previo()

    NAVY = "002060"
    f_tit = Font(name="Calibri", size=14, bold=True, color=NAVY)
    f_sec = Font(name="Calibri", size=12, bold=True, color=NAVY)
    f_cab = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    f_norm = Font(name="Calibri", size=11)
    f_gris = Font(name="Calibri", size=10, color="595959")
    f_input = Font(name="Calibri", size=11, color="0000FF")
    f_tot = Font(name="Calibri", size=11, bold=True)
    f_gran = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    f_nota = Font(name="Calibri", size=10, italic=True, color="595959")
    r_cab = PatternFill("solid", fgColor=NAVY)
    r_input = PatternFill("solid", fgColor="FFF2CC")
    r_sub = PatternFill("solid", fgColor="D9E1F2")
    r_gran = PatternFill("solid", fgColor=NAVY)
    fino = Side(style="thin", color="A6A6A6")
    caja = Border(left=fino, right=fino, top=fino, bottom=fino)
    PESOS = '"$"#,##0;-"$"#,##0;"-"'
    NUM = '#,##0;-#,##0;"-"'
    centro = Alignment(horizontal="center", vertical="center", wrap_text=True)
    izq = Alignment(horizontal="left", vertical="center", wrap_text=True)

    wb = openpyxl.Workbook()

    def celda(ws, ref, valor, fuente=f_norm, formato=None, relleno=None, alinear=centro, borde=True):
        c = ws[ref]
        c.value, c.font, c.alignment = valor, fuente, alinear
        if formato:
            c.number_format = formato
        if relleno:
            c.fill = relleno
        if borde:
            c.border = caja
        return c

    def entrada(ws, ref, valor, formato=None, alinear=centro):
        v = previo["celdas"].get((ws.title, ref), valor) if previo else valor
        return celda(ws, ref, v, f_input, formato, r_input, alinear)

    def cabecera(ws, fila, col0, textos, alto=34):
        for k, t in enumerate(textos):
            celda(ws, ws.cell(fila, col0 + k).coordinate, t, f_cab, relleno=r_cab)
        ws.row_dimensions[fila].height = alto

    def logo(ws, archivo):
        ruta = DIR / archivo
        if ruta.exists():
            im = XLImage(str(ruta))
            im.width, im.height = 72, 64
            ws.add_image(im, "A1")

    def encabezado(ws, titulo, bajada):
        celda(ws, "C2", titulo, f_tit, alinear=Alignment(vertical="center"), borde=False)
        celda(ws, "C3", bajada, f_nota, alinear=Alignment(vertical="center"), borde=False)
        ws.row_dimensions[1].height = 22
        ws.column_dimensions["A"].width = 11

    # ---------------------------------------------------------------- PRECIOS
    pr = wb.active
    pr.title = "PRECIOS"
    logo(pr, "logo_fevochi.png")
    encabezado(pr, "PRECIOS POR PRENDA", "Celdas amarillas: precio público general (con IVA) y descuento. El precio "
                                         "federación se calcula solo y se aplica a todas las categorías.")
    celda(pr, "B4", "IVA", f_tot, alinear=izq)
    celda(pr, "C4", previo["iva"] if previo and previo["iva"] is not None else IVA, f_input, "0%", r_input)
    celda(pr, "B5", "Descuento general para la federación", f_tot, alinear=izq)
    celda(pr, "C5", previo["descuento"] if previo and previo["descuento"] is not None else 0, f_input, "0%", r_input)
    celda(pr, "D5", "Se aplica a las prendas que no tienen un descuento propio en la columna DESCUENTO.", f_nota,
          alinear=Alignment(vertical="center"), borde=False)
    cabecera(pr, 7, 2, ["PRENDA", "PRECIO PÚBLICO GENERAL (CON IVA)", "DESCUENTO FEDERACIÓN",
                        "PRECIO FEDERACIÓN (CON IVA)", "PRECIO FEDERACIÓN NETO", "OBSERVACIONES"], alto=36)
    fila_precio = {}
    r = 8
    for grupo, prendas in PRENDAS:
        celda(pr, f"B{r}", grupo, Font(name="Calibri", size=10, bold=True, color=NAVY), relleno=r_sub, alinear=izq)
        for col in "CDEFG":
            celda(pr, f"{col}{r}", None, relleno=r_sub)
        r += 1
        for p in prendas:
            fila_precio[p] = r
            publico, desc, obs = previo["precios"].get(p, (None, None, None)) if previo else (None, None, None)
            celda(pr, f"B{r}", p, alinear=izq)
            celda(pr, f"C{r}", publico, f_input, PESOS, r_input)
            celda(pr, f"D{r}", desc, f_input, "0%", r_input)
            celda(pr, f"E{r}", f'=ROUND(N(C{r})*(1-IF(D{r}="",$C$5,D{r})),0)', f_tot, PESOS)
            celda(pr, f"F{r}", f"=ROUND(E{r}/(1+$C$4),0)", formato=PESOS)
            celda(pr, f"G{r}", obs, f_input, relleno=r_input, alinear=izq)
            r += 1
    ultima_precio = r - 1
    for col, ancho in zip("BCDEFG", (40, 18, 14, 18, 16, 40)):
        pr.column_dimensions[col].width = ancho
    dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                        errorTitle="Precio", error="Ingresa un precio en pesos (0 o más).")
    pr.add_data_validation(dv)
    dv.add(f"C8:C{ultima_precio}")
    dvp = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True,
                         errorTitle="Descuento", error="Ingresa un porcentaje entre 0% y 100%.")
    pr.add_data_validation(dvp)
    dvp.add("C5")
    dvp.add(f"D8:D{ultima_precio}")

    def precio_de(prenda, col="E"):  # E: precio federación; C: precio público
        return (f"N(INDEX(PRECIOS!${col}$8:${col}${ultima_precio},"
                f"MATCH(\"{prenda}\",PRECIOS!$B$8:$B${ultima_precio},0)))")

    # ---------------------------------------------------------------- SELECCIONES ROPA 2027
    se = wb.create_sheet("SELECCIONES ROPA 2027")
    logo(se, "logo_fevochi.png")
    encabezado(se, "SELECCIONES 2027: ROPA VALORIZADA POR CATEGORÍA",
               "Celdas amarillas: jugadores, unidades por jugador y canje (editables). CANJE SÍ = 100% de descuento en esa "
               "prenda. El precio público es solo referencia.")
    dv_canje = DataValidation(type="list", formula1='"SÍ,NO"', allow_blank=True, errorTitle="Canje",
                              error="Elige SÍ (canje, 100% de descuento) o NO.")
    r = 5
    totales_sel = []  # (título, [(categoría, primera fila, fila subtotal)], fila total)
    for titulo, cats in selecciones:
        celda(se, f"B{r}", titulo, f_sec, alinear=Alignment(vertical="center"), borde=False)
        se.row_dimensions[r].height = 20
        r += 1
        cabecera(se, r, 2, ["CATEGORÍA", "CANTIDAD DE JUGADORES" if "MASCULINA" in titulo else "CANTIDAD DE JUGADORAS",
                            "PRENDA", "COLORES", "UNIDADES POR JUGADOR" if "MASCULINA" in titulo else
                            "UNIDADES POR JUGADORA", "TOTAL UNIDADES", "PRECIO PÚBLICO (REFERENCIA)",
                            "PRECIO FEDERACIÓN", "CANJE", "VALOR A PAGAR"])
        r += 1
        filas_cat = []
        for cat, jugadores, items in cats:
            f0 = r
            canje = "SÍ" if cat.upper().startswith("ADULTO") else "NO"  # canje: equipos adultos
            for k, (prenda, unid, colores) in enumerate(items):
                if k == 0:
                    celda(se, f"B{r}", cat, f_tot)
                    entrada(se, f"C{r}", jugadores, NUM)
                else:
                    celda(se, f"B{r}", None)
                    celda(se, f"C{r}", f"=C{f0}", f_gris, NUM)
                celda(se, f"D{r}", prenda, alinear=izq)
                entrada(se, f"E{r}", colores or None, alinear=izq)
                entrada(se, f"F{r}", unid, NUM)
                celda(se, f"G{r}", f"=C{r}*F{r}", formato=NUM)
                celda(se, f"H{r}", "=" + precio_de(prenda, "C"), f_gris, PESOS)
                celda(se, f"I{r}", "=" + precio_de(prenda), formato=PESOS)
                entrada(se, f"J{r}", canje)
                celda(se, f"K{r}", f'=IF(J{r}="SÍ",0,G{r}*I{r})', f_tot, PESOS)
                r += 1
            dv_canje.add(f"J{f0}:J{r - 1}")
            celda(se, f"B{r}", f"Total {cat}", f_tot, relleno=r_sub)
            for col in "DEFHIJ":
                celda(se, f"{col}{r}", None, relleno=r_sub)
            celda(se, f"C{r}", f"=C{f0}", f_tot, NUM, r_sub)
            celda(se, f"G{r}", f"=SUM(G{f0}:G{r - 1})", f_tot, NUM, r_sub)
            celda(se, f"K{r}", f"=SUM(K{f0}:K{r - 1})", f_tot, PESOS, r_sub)
            filas_cat.append((cat, f0, r))
            r += 1
        celda(se, f"B{r}", f"TOTAL {titulo}", f_gran, relleno=r_gran, alinear=izq)
        for col in "CDEFGHIJK":
            celda(se, f"{col}{r}", None, f_gran, relleno=r_gran)
        celda(se, f"C{r}", "=" + "+".join(f"C{s}" for _, _, s in filas_cat), f_gran, NUM, r_gran)
        celda(se, f"G{r}", "=" + "+".join(f"G{s}" for _, _, s in filas_cat), f_gran, NUM, r_gran)
        celda(se, f"K{r}", "=" + "+".join(f"K{s}" for _, _, s in filas_cat), f_gran, PESOS, r_gran)
        se.row_dimensions[r].height = 20
        totales_sel.append((titulo, filas_cat, r))
        r += 3
    se.add_data_validation(dv_canje)
    for col, ancho in zip("BCDEFGHIJK", (20, 14, 33, 22, 13, 12, 15, 13, 10, 16)):
        se.column_dimensions[col].width = ancho
    dv2 = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                         errorTitle="Cantidad", error="Ingresa un número entero (0 o más).")
    se.add_data_validation(dv2)
    for _, filas_cat, _ in totales_sel:
        for _, f0, s in filas_cat:
            dv2.add(f"C{f0}")
            dv2.add(f"F{f0}:F{s - 1}")

    # ---------------------------------------------------------------- CUERPO TÉCNICO 2027
    ct = wb.create_sheet("CUERPO TÉCNICO 2027")
    logo(ct, "logo_fevochi_2.png")
    encabezado(ct, "CUERPOS TÉCNICOS 2027: ROPA VALORIZADA",
               "Celdas amarillas: personas, cantidad por técnico y canje (editables). CANJE SÍ = 100% de descuento en esa "
               "prenda. El precio público es solo referencia.")
    dv_canje_ct = DataValidation(type="list", formula1='"SÍ,NO"', allow_blank=True, errorTitle="Canje",
                                 error="Elige SÍ (canje, 100% de descuento) o NO.")
    r = 5
    totales_ct = []  # (título, primera fila, fila total)
    for titulo, personas, items in tecnicos:
        celda(ct, f"B{r}", titulo, f_sec, alinear=Alignment(vertical="center"), borde=False)
        ct.row_dimensions[r].height = 20
        r += 1
        cabecera(ct, r, 2, ["INDUMENTARIA COMPETENCIAS", "PERSONAS", "CANTIDAD POR TÉCNICO", "TOTAL UNIDADES",
                            "PRECIO PÚBLICO (REFERENCIA)", "PRECIO FEDERACIÓN", "CANJE", "VALOR A PAGAR"])
        r += 1
        f0 = r
        for k, (prenda, unid) in enumerate(items):
            celda(ct, f"B{r}", prenda, alinear=izq)
            if k == 0:
                entrada(ct, f"C{r}", personas, NUM)
            else:
                celda(ct, f"C{r}", f"=C{f0}", f_gris, NUM)
            entrada(ct, f"D{r}", unid, NUM)
            celda(ct, f"E{r}", f"=C{r}*D{r}", formato=NUM)
            celda(ct, f"F{r}", "=" + precio_de(prenda, "C"), f_gris, PESOS)
            celda(ct, f"G{r}", "=" + precio_de(prenda), formato=PESOS)
            entrada(ct, f"H{r}", "NO")
            celda(ct, f"I{r}", f'=IF(H{r}="SÍ",0,E{r}*G{r})', f_tot, PESOS)
            r += 1
        dv_canje_ct.add(f"H{f0}:H{r - 1}")
        celda(ct, f"B{r}", f"TOTAL {titulo}", f_gran, relleno=r_gran, alinear=izq)
        for col in "CDEFGHI":
            celda(ct, f"{col}{r}", None, f_gran, relleno=r_gran)
        celda(ct, f"C{r}", f"=C{f0}", f_gran, NUM, r_gran)
        celda(ct, f"E{r}", f"=SUM(E{f0}:E{r - 1})", f_gran, NUM, r_gran)
        celda(ct, f"I{r}", f"=SUM(I{f0}:I{r - 1})", f_gran, PESOS, r_gran)
        ct.row_dimensions[r].height = 20
        totales_ct.append((titulo, f0, r))
        ct.add_data_validation(dv3 := DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0",
                                                     allow_blank=True, errorTitle="Cantidad",
                                                     error="Ingresa un número entero (0 o más)."))
        dv3.add(f"C{f0}")
        dv3.add(f"D{f0}:D{r - 1}")
        r += 3
    ct.add_data_validation(dv_canje_ct)
    for col, ancho in zip("BCDEFGHI", (36, 11, 13, 12, 15, 13, 10, 16)):
        ct.column_dimensions[col].width = ancho

    # ---------------------------------------------------------------- RESUMEN
    rs = wb.create_sheet("RESUMEN", 0)
    logo(rs, "logo_fevochi.png")
    encabezado(rs, "VALORIZACIÓN ROPA SELECCIONES FEVOCHI 2027",
               "Valores con IVA a precio federación. El canje (100% de descuento en las prendas marcadas SÍ) se descuenta "
               "antes del neto y el IVA. El precio público general es solo referencia.")
    cabecera(rs, 5, 2, ["SELECCIÓN", "CATEGORÍA", "JUGADORES O PERSONAS", "TOTAL UNIDADES", "VALOR PRECIO FEDERACIÓN",
                        "CANJE", "TOTAL A PAGAR", "NETO", "IVA"], alto=36)
    S, T = "'SELECCIONES ROPA 2027'", "'CUERPO TÉCNICO 2027'"
    r = 6
    filas_total = []

    def fila_resumen(r, sel, cat, jug, unid, bruto, canje, pagar, fuente=f_norm, relleno=None):
        celda(rs, f"B{r}", sel, fuente, relleno=relleno, alinear=izq)
        celda(rs, f"C{r}", cat, fuente, relleno=relleno, alinear=izq)
        celda(rs, f"D{r}", jug, fuente, NUM, relleno)
        celda(rs, f"E{r}", unid, fuente, NUM, relleno)
        celda(rs, f"F{r}", bruto, fuente, PESOS, relleno)
        celda(rs, f"G{r}", canje, fuente, PESOS, relleno)
        celda(rs, f"H{r}", pagar, fuente if relleno else f_tot, PESOS, relleno)
        celda(rs, f"I{r}", f"=ROUND(H{r}/(1+PRECIOS!$C$4),0)", fuente, PESOS, relleno)
        celda(rs, f"J{r}", f"=H{r}-I{r}", fuente, PESOS, relleno)

    def rango(hoja, col, a, b):
        return f"{hoja}!{col}{a}:{col}{b}"

    for titulo, filas_cat, ft in totales_sel:
        nombre = titulo.replace("SELECCIÓN ", "").capitalize()
        r0 = r
        for k, (cat, f0, s) in enumerate(filas_cat):
            g, i, j = rango(S, "G", f0, s - 1), rango(S, "I", f0, s - 1), rango(S, "J", f0, s - 1)
            fila_resumen(r, nombre if k == 0 else None, cat, f"={S}!C{s}", f"={S}!G{s}", f"=SUMPRODUCT({g},{i})",
                         f'=SUMPRODUCT(({j}="SÍ")*{g}*{i})', f"={S}!K{s}")
            r += 1
        fila_resumen(r, f"Total {nombre.lower()}", None, *[f"=SUM({c}{r0}:{c}{r - 1})" for c in "DEFGH"], f_tot, r_sub)
        filas_total.append(r)
        r += 1
    fct0 = r
    for k, (titulo, f0, ft) in enumerate(totales_ct):
        nombre = titulo.replace("CUERPO TÉCNICO ", "").capitalize()
        e, g, h = rango(T, "E", f0, ft - 1), rango(T, "G", f0, ft - 1), rango(T, "H", f0, ft - 1)
        fila_resumen(r, "Cuerpos técnicos" if k == 0 else None, nombre, f"={T}!C{ft}", f"={T}!E{ft}",
                     f"=SUMPRODUCT({e},{g})", f'=SUMPRODUCT(({h}="SÍ")*{e}*{g})', f"={T}!I{ft}")
        r += 1
    fila_resumen(r, "Total cuerpos técnicos", None, *[f"=SUM({c}{fct0}:{c}{r - 1})" for c in "DEFGH"], f_tot, r_sub)
    filas_total.append(r)
    r += 1
    fila_resumen(r, "TOTAL GENERAL", None, *["=" + "+".join(f"{col}{x}" for x in filas_total) for col in "DEFGH"],
                 f_gran, r_gran)
    rs.row_dimensions[r].height = 22
    total_general = r
    celda(rs, f"B{r + 1}", f'=IF(ROUND(F{r}-G{r}-H{r},0)=0,"Control: valor federación menos canje es igual al total '
                           f'a pagar.","Revisar: el canje no cuadra con el total a pagar.")', f_nota,
          alinear=Alignment(vertical="center"), borde=False)

    r += 4
    celda(rs, f"B{r}", "VALOR POR PRENDA", f_sec, alinear=Alignment(vertical="center"), borde=False)
    r += 1
    cabecera(rs, r, 2, ["PRENDA", None, "PRECIO PÚBLICO (REFERENCIA)", "DESCUENTO", "PRECIO FEDERACIÓN",
                        "TOTAL UNIDADES", "VALOR PRECIO FEDERACIÓN", "CANJE", "TOTAL A PAGAR"], alto=36)
    rs.merge_cells(f"B{r}:C{r}")
    r += 1
    p0 = r
    for _, prendas in PRENDAS:
        for p in prendas:
            fp = fila_precio[p]
            celda(rs, f"B{r}", p, alinear=izq)
            celda(rs, f"C{r}", None)
            rs.merge_cells(f"B{r}:C{r}")
            celda(rs, f"D{r}", f"=PRECIOS!C{fp}", f_gris, PESOS)
            celda(rs, f"E{r}", f"=IF(N(D{r})=0,0,1-F{r}/D{r})", formato='0.0%;-0.0%;"-"')
            celda(rs, f"F{r}", f"=PRECIOS!E{fp}", formato=PESOS)
            celda(rs, f"G{r}", f'=SUMIF({S}!$D:$D,"{p}",{S}!$G:$G)+SUMIF({T}!$B:$B,"{p}",{T}!$E:$E)', formato=NUM)
            celda(rs, f"H{r}", f"=G{r}*F{r}", formato=PESOS)
            celda(rs, f"I{r}", f'=(SUMIFS({S}!$G:$G,{S}!$D:$D,"{p}",{S}!$J:$J,"SÍ")'
                               f'+SUMIFS({T}!$E:$E,{T}!$B:$B,"{p}",{T}!$H:$H,"SÍ"))*F{r}', formato=PESOS)
            celda(rs, f"J{r}", f'=SUMIF({S}!$D:$D,"{p}",{S}!$K:$K)+SUMIF({T}!$B:$B,"{p}",{T}!$I:$I)', f_tot, PESOS)
            r += 1
    celda(rs, f"B{r}", "TOTAL", f_gran, relleno=r_gran, alinear=izq)
    for col in "CDEF":
        celda(rs, f"{col}{r}", None, f_gran, relleno=r_gran)
    rs.merge_cells(f"B{r}:C{r}")
    for col, fmt in (("G", NUM), ("H", PESOS), ("I", PESOS), ("J", PESOS)):
        celda(rs, f"{col}{r}", f"=SUM({col}{p0}:{col}{r - 1})", f_gran, fmt, r_gran)
    celda(rs, f"B{r + 1}", f'=IF(AND(J{r}=H{total_general},I{r}=G{total_general}),"Control: la suma por prenda '
                           f'coincide con el total general.","Revisar: la suma por prenda no coincide con el total '
                           f'general.")', f_nota, alinear=Alignment(vertical="center"), borde=False)
    for col, ancho in zip("BCDEFGHIJ", (31, 18, 15, 13, 17, 14, 17, 15, 15)):
        rs.column_dimensions[col].width = ancho

    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
        ws.page_setup.orientation = "landscape" if ws.title != "PRECIOS" else "portrait"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    se.freeze_panes = "B5"
    wb.save(SALIDA)
    n_filas = sum(len(items) for _, cats in selecciones for _, _, items in cats)
    print(f"OK  {SALIDA.name}  ({len(selecciones)} selecciones, {n_filas} filas de prendas, {len(tecnicos)} cuerpos técnicos)")


if __name__ == "__main__":
    main()
