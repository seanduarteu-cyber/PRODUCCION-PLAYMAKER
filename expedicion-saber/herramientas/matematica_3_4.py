"""Matemática 3° y 4° básico: 20 desafíos por OA (4 por nivel de dificultad, 1 a 5)."""
from comun import (opcion_multiple as om, completar as co, ordenar as orden, emparejar as em,
                   categoria as cat, numerica as nu, distractores_numericos as dn)
from matematica_1_2 import Banco


def miles(n):
    """Formato chileno: punto como separador de miles."""
    return f"{n:,}".replace(",", ".")


def _con_reserva_suma(r, da, db):
    while True:
        a = r.randint(10 ** (da - 1), 10 ** da - 1); c = r.randint(10 ** (db - 1), 10 ** db - 1)
        if a + c <= 1000 and any(int(x) + int(y) >= 10 for x, y in zip(str(a)[::-1], str(c)[::-1])):
            return a, c


def _sin_reserva(r, da, db, resta=False):
    while True:
        a = r.randint(10 ** (da - 1), 10 ** da - 1); c = r.randint(10 ** (db - 1), 10 ** db - 1)
        pares = list(zip(str(a)[::-1], str(c)[::-1]))
        if resta and c < a and all(int(x) >= int(y) for x, y in pares):
            return a, c
        if not resta and a + c < 1000 and all(int(x) + int(y) < 10 for x, y in pares):
            return a, c


def _con_reserva_resta(r, da, db):
    while True:
        a = r.randint(10 ** (da - 1), 10 ** da - 1); c = r.randint(10 ** (db - 1), 10 ** db - 1)
        if c < a and any(int(x) < int(y) for x, y in zip(str(a)[::-1], str(c)[::-1])):
            return a, c


# ---------------- 3° básico ----------------
def ma03_oa6():
    b = Banco(3, 6, 306); r = b.r
    a, c = 100 * r.randint(1, 5), 100 * r.randint(1, 4)
    b(nu(b.id(), 1, f"¿Cuánto es {a} + {c}?", a + c, "Suma las centenas.", f"{a // 100} centenas + {c // 100} centenas = {(a + c) // 100} centenas."))
    a, c = _sin_reserva(r, 3, 1)
    b(nu(b.id(), 1, f"¿Cuánto es {a} + {c}?", a + c, "Solo cambian las unidades.", f"{a} + {c} = {a + c}."))
    b(om(b.id(), 1, "¿Cuánto es 700 − 200?", 500, [900, 520, 400], "7 centenas menos 2 centenas.", "700 − 200 = 500.", r))
    a, c = _sin_reserva(r, 3, 1, resta=True)
    b(nu(b.id(), 1, f"¿Cuánto es {a} − {c}?", a - c, "Resta solo las unidades.", f"{a} − {c} = {a - c}."))
    for _ in range(2):
        a, c = _sin_reserva(r, 3, 2)
        b(nu(b.id(), 2, f"¿Cuánto es {a} + {c}?", a + c, "Suma por columnas: unidades, decenas y centenas.", f"{a} + {c} = {a + c}."))
    a, c = _sin_reserva(r, 3, 2, resta=True)
    b(co(b.id(), 2, f"{a} − {c} = ___", a - c, dn(a - c, [a - c + 10, a - c - 100, a + c]), "Resta por columnas.", f"{a} − {c} = {a - c}.", r))
    a, c = _sin_reserva(r, 3, 2, resta=True)
    b(nu(b.id(), 2, f"¿Cuánto es {a} − {c}?", a - c, "Resta por columnas.", f"{a} − {c} = {a - c}."))
    for _ in range(2):
        a, c = _con_reserva_suma(r, 3, 3 if _ else 2)
        b(nu(b.id(), 3, f"¿Cuánto es {a} + {c}?", a + c, "Si una columna suma 10 o más, llevas 1 a la columna siguiente.", f"{a} + {c} = {a + c}."))
    a, c = _con_reserva_suma(r, 3, 3)
    b(om(b.id(), 3, f"¿Cuánto es {a} + {c}?", a + c, dn(a + c, [a + c - 10, a + c - 100, a + c + 10]), "No olvides la reserva.", f"{a} + {c} = {a + c}.", r))
    a, c = _con_reserva_suma(r, 3, 2)
    b(co(b.id(), 3, f"{a} + {c} = ___", a + c, dn(a + c, [a + c - 10, a + c + 100, a + c - 1]), "Suma por columnas con reserva.", f"{a} + {c} = {a + c}.", r))
    a, c = _con_reserva_resta(r, 3, 3)
    b(nu(b.id(), 4, f"¿Cuánto es {a} − {c}?", a - c, "Si arriba hay menos, pide prestado a la columna de la izquierda.", f"{a} − {c} = {a - c}."))
    c = r.randint(111, 499)
    b(nu(b.id(), 4, f"¿Cuánto es 700 − {c}?", 700 - c, "Puedes descomponer: 700 = 600 + 90 + 10.", f"700 − {c} = {700 - c}."))
    a, c = _con_reserva_resta(r, 3, 3)
    b(nu(b.id(), 4, f"{{personaje}} tenía {a} {{objetos}} y usó {c} en {{la_construccion}}. ¿Cuántos le quedan?", a - c, "Usar es restar.", f"{a} − {c} = {a - c}."))
    pares = []
    while len(pares) < 4:
        a, c = _con_reserva_resta(r, 3, 2)
        if all(str(a - c) != p[1] for p in pares):
            pares.append([f"{a} − {c}", str(a - c)])
    b(em(b.id(), 4, "Une cada resta con su resultado.", pares, "Resuelve cada resta con reserva.", "; ".join(f"{p[0]} = {p[1]}" for p in pares) + "."))
    b(nu(b.id(), 5, "{personaje} tenía 350 {objetos}, juntó 275 más y después usó 180. ¿Cuántos tiene ahora?", 445, "Primero suma, después resta.", "350 + 275 = 625 y 625 − 180 = 445."))
    b(co(b.id(), 5, "___ + 245 = 600", 355, [455, 845, 345], "Piensa al revés: 600 − 245.", "600 − 245 = 355.", r))
    b(cat(b.id(), 5, "¿El resultado es mayor que 500?", ["500 o menos", "Mayor que 500"],
          [("250 + 180", 0), ("900 − 450", 0), ("610 − 125", 0), ("380 + 145", 1), ("999 − 400", 1), ("275 + 275", 1)],
          "Calcula cada operación.", "250 + 180 = 430, 900 − 450 = 450, 610 − 125 = 485; 380 + 145 = 525, 999 − 400 = 599, 275 + 275 = 550."))
    b(om(b.id(), 5, "En {lugar} hay 820 {objetos}. Se usan 315 y luego llegan 140. ¿Cuántos hay ahora?", 645, [365, 505, 1275], "Resta lo que se usa y suma lo que llega.", "820 − 315 = 505 y 505 + 140 = 645.", r))
    return b.items


def ma03_oa8():
    b = Banco(3, 8, 308); r = b.r
    for nivel, tablas in [(1, [2, 5, 10]), (2, [3, 4]), (3, [6, 7]), (4, [8, 9])]:
        t1 = tablas[0]; k = r.randint(3, 10)
        b(nu(b.id(), nivel, f"¿Cuánto es {k} × {t1}?", k * t1, f"Cuenta de {t1} en {t1}.", f"{k} × {t1} = {k * t1}."))
        t2 = tablas[-1]; k = r.randint(3, 10)
        b(co(b.id(), nivel, f"{k} × {t2} = ___", k * t2, dn(k * t2, [k * t2 + t2, k * t2 - t2, k + t2]), f"Usa la tabla del {t2}.", f"{k} × {t2} = {k * t2}.", r))
        if nivel < 4:
            ks = r.sample(range(2, 11), 3); t = r.choice(tablas)
            b(em(b.id(), nivel, "Une cada multiplicación con su resultado.", [[f"{k} × {t}", str(k * t)] for k in ks],
                 f"Usa la tabla del {t}.", ", ".join(f"{k} × {t} = {k * t}" for k in ks) + "."))
            t = r.choice(tablas); k = r.randint(4, 10)
            b(om(b.id(), nivel, f"¿Cuánto es {t} × {k}?", t * k, dn(t * k, [t * k + t, t * k - t, t + k]), "El orden de los factores no cambia el producto.", f"{t} × {k} = {t * k}.", r))
        else:
            b(nu(b.id(), 4, "{personaje} arma 8 filas de 6 {objetos}. ¿Cuántos {objetos} hay?", 48, "Son 8 veces 6.", "8 × 6 = 48."))
            b(nu(b.id(), 4, "Cada {contenedor} tiene 9 {objetos}. ¿Cuántos hay en 7 {contenedores}?", 63, "Son 7 veces 9.", "7 × 9 = 63."))
    b(co(b.id(), 5, "7 × 8 = 7 × 5 + 7 × ___", 3, [8, 5, 2], "8 se puede separar en 5 + 3.", "7 × 8 = 7 × 5 + 7 × 3 = 35 + 21 = 56."))
    b(co(b.id(), 5, "6 × ___ = 54", 9, [8, 7, 6], "Cuenta de 6 en 6 hasta 54.", "6 × 9 = 54.", r))
    b(em(b.id(), 5, "Une cada multiplicación con su resultado.", [["6 × 7", "42"], ["8 × 8", "64"], ["9 × 4", "36"], ["7 × 7", "49"]],
         "Usa las tablas.", "6 × 7 = 42, 8 × 8 = 64, 9 × 4 = 36 y 7 × 7 = 49."))
    b(cat(b.id(), 5, "¿El resultado es mayor que 50?", ["50 o menos", "Mayor que 50"],
          [("6 × 8", 0), ("7 × 7", 0), ("9 × 5", 0), ("8 × 7", 1), ("9 × 6", 1), ("8 × 9", 1)],
          "Calcula cada producto.", "6 × 8 = 48, 7 × 7 = 49, 9 × 5 = 45; 8 × 7 = 56, 9 × 6 = 54, 8 × 9 = 72."))
    return b.items


def ma03_oa9():
    b = Banco(3, 9, 309); r = b.r
    for nivel, divs in [(1, [2, 5, 10]), (2, [3, 4]), (3, [6, 7, 8, 9])]:
        d = r.choice(divs); q = r.randint(2, 10)
        b(nu(b.id(), nivel, f"¿Cuánto es {d * q} ÷ {d}?", q, f"Piensa: ¿qué número por {d} da {d * q}?", f"{d} × {q} = {d * q}, entonces {d * q} ÷ {d} = {q}."))
        d = r.choice(divs); q = r.randint(2, 10)
        b(nu(b.id(), nivel, f"¿Cuánto es {d * q} ÷ {d}?", q, f"Usa la tabla del {d}.", f"{d * q} ÷ {d} = {q}."))
        d = r.choice(divs); q = r.randint(3, 10)
        b(om(b.id(), nivel, f"¿Cuánto es {d * q} ÷ {d}?", q, dn(q, [q + 1, q - 1, d * q - d]), "La división es la operación inversa de la multiplicación.", f"{d * q} ÷ {d} = {q}.", r))
        d = r.choice(divs); q = r.randint(3, 10)
        b(co(b.id(), nivel, f"{d * q} ÷ {d} = ___", q, dn(q, [q + 2, q - 2, d]), f"¿Cuántas veces cabe {d} en {d * q}?", f"{d * q} ÷ {d} = {q}.", r))
    b(nu(b.id(), 4, "{personaje} reparte 24 {objetos} en 6 grupos iguales. ¿Cuántos quedan en cada grupo?", 4, "Repartir en partes iguales es dividir.", "24 ÷ 6 = 4."))
    b(nu(b.id(), 4, "Hay 30 {objetos} y se ponen 5 en cada {contenedor}. ¿Cuántos {contenedores} se llenan?", 6, "¿Cuántas veces cabe 5 en 30?", "30 ÷ 5 = 6."))
    b(nu(b.id(), 4, "{personaje} tiene 56 {objetos} y los ordena en 8 filas iguales. ¿Cuántos hay en cada fila?", 7, "Divide 56 en 8 partes iguales.", "56 ÷ 8 = 7."))
    b(om(b.id(), 4, "Se reparten 45 {objetos} en partes iguales entre 9 amigos. ¿Cuántos recibe cada uno?", 5, [6, 9, 36], "Usa la tabla del 9.", "45 ÷ 9 = 5.", r))
    b(om(b.id(), 5, "Si 7 × 6 = 42, entonces 42 ÷ 6 = ?", 7, [6, 36, 48], "La división deshace la multiplicación.", "42 ÷ 6 = 7, porque 7 × 6 = 42.", r))
    b(co(b.id(), 5, "Si 8 × 9 = 72, entonces 72 ÷ 9 = ___", 8, [9, 63, 7], "Usa la multiplicación que te dan.", "72 ÷ 9 = 8.", r))
    b(em(b.id(), 5, "Une cada multiplicación con la división que le corresponde.", [["4 × 7 = 28", "28 ÷ 7 = 4"], ["6 × 9 = 54", "54 ÷ 9 = 6"], ["3 × 8 = 24", "24 ÷ 8 = 3"]],
         "Busca los mismos tres números.", "Cada división usa los mismos números que su multiplicación."))
    b(cat(b.id(), 5, "¿Cuál es el resultado de cada división?", ["Da 6", "Da 7"],
          [("36 ÷ 6", 0), ("54 ÷ 9", 0), ("48 ÷ 8", 0), ("49 ÷ 7", 1), ("63 ÷ 9", 1), ("56 ÷ 8", 1)],
          "Usa las tablas del 6, 7, 8 y 9.", "36 ÷ 6, 54 ÷ 9 y 48 ÷ 8 dan 6; 49 ÷ 7, 63 ÷ 9 y 56 ÷ 8 dan 7."))
    return b.items


def ma03_oa11():
    b = Banco(3, 11, 311); r = b.r
    F = ["1/2", "1/3", "1/4", "2/3", "3/4"]

    def barra(n, d):
        return "🟩" * n + "⬜" * (d - n)

    for nivel, casos in [(1, [(1, 2), (1, 4), (1, 3)]), (2, [(2, 3), (3, 4), (1, 2)])]:
        for n, d in casos:
            f = f"{n}/{d}"
            b(om(b.id(), nivel, f"¿Qué fracción de la barra está pintada? {barra(n, d)}", f, [x for x in F if x != f][:3],
                 "Cuenta las partes pintadas (arriba) y las partes en total (abajo).", f"Hay {n} parte{'s' if n > 1 else ''} pintada{'s' if n > 1 else ''} de {d}: {f}."))
    b(em(b.id(), 1, "Une cada fracción con su nombre.", [["1/2", "un medio"], ["1/3", "un tercio"], ["1/4", "un cuarto"]],
         "El número de abajo dice en cuántas partes se dividió.", "1/2 es un medio, 1/3 un tercio y 1/4 un cuarto."))
    b(em(b.id(), 2, "Une cada fracción con su nombre.", [["2/3", "dos tercios"], ["3/4", "tres cuartos"], ["1/2", "un medio"], ["1/4", "un cuarto"]],
         "Lee primero el número de arriba y luego el de abajo.", "2/3 son dos tercios y 3/4 son tres cuartos."))
    b(om(b.id(), 3, "¿Cuál es mayor?", "2/3", ["1/3", "Son iguales", "No se puede saber"], "Con el mismo denominador, gana la que tiene más partes.", "2 partes de 3 es más que 1 parte de 3."))
    b(om(b.id(), 3, "¿Cuál es menor?", "1/4", ["3/4", "Son iguales", "No se puede saber"], "Mismo denominador: compara los numeradores.", "1 parte de 4 es menos que 3 partes de 4."))
    b(co(b.id(), 3, "1/4 ___ 3/4", "<", [">", "=", "+"], "Mismo denominador: compara los numeradores.", "1/4 es menor que 3/4."))
    b(orden(b.id(), 3, "Ordena de menor a mayor.", ["1/4", "2/4", "3/4"], "Todas tienen 4 partes: compara cuántas se toman.", "1/4 < 2/4 < 3/4."))
    b(om(b.id(), 4, "{personaje} divide {la_construccion} en 3 partes iguales y pinta 1. ¿Qué fracción pintó?", "1/3", ["1/2", "3/1", "2/3"], "Son 3 partes iguales y se pinta 1.", "1 de 3 partes es 1/3."))
    b(om(b.id(), 4, "Una torta se reparte en partes iguales entre 4 personas. ¿Qué fracción recibe cada una?", "1/4", ["1/2", "4/1", "3/4"], "Son 4 partes iguales.", "Cada persona recibe 1 de 4 partes: 1/4."))
    b(co(b.id(), 4, "La mitad de algo es ___", "1/2", ["1/3", "1/4", "2/3"], "Mitad significa dividir en 2 partes iguales.", "La mitad es 1/2."))
    b(cat(b.id(), 4, "¿Es más o menos de la mitad?", ["Menos de la mitad", "Más de la mitad"], [("1/4", 0), ("1/3", 0), ("3/4", 1), ("2/3", 1)],
          "Imagina una barra: ¿queda pintada más o menos de la mitad?", "1/4 y 1/3 son menos de la mitad; 3/4 y 2/3 son más."))
    for come, queda in [("1/4", "3/4"), ("2/3", "1/3"), ("1/2", "1/2")]:
        b(om(b.id(), 5, f"{{personaje}} usa {come} de una barra. ¿Qué fracción queda?", queda, [x for x in F if x != queda][:3],
             "Lo que se usa y lo que queda forman la barra completa.", f"Si se usa {come}, queda {queda}."))
    b(em(b.id(), 5, "Une lo que se come con lo que queda.", [["Comes 1/4", "Queda 3/4"], ["Comes 2/3", "Queda 1/3"], ["Comes 3/4", "Queda 1/4"], ["Comes 1/3", "Queda 2/3"]],
         "Las dos partes juntas forman el entero.", "1/4 + 3/4, 2/3 + 1/3, 3/4 + 1/4 y 1/3 + 2/3 forman un entero."))
    return b.items


# ---------------- 4° básico ----------------
def ma04_oa3():
    b = Banco(4, 3, 403); r = b.r
    a, c = _sin_reserva(r, 3, 3)
    b(nu(b.id(), 1, f"¿Cuánto es {a} + {c}?", a + c, "Suma por columnas.", f"{a} + {c} = {a + c}."))
    a, c = _sin_reserva(r, 3, 3, resta=True)
    b(nu(b.id(), 1, f"¿Cuánto es {a} − {c}?", a - c, "Resta por columnas.", f"{a} − {c} = {a - c}."))
    a, c = _sin_reserva(r, 3, 3)
    b(om(b.id(), 1, f"¿Cuánto es {a} + {c}?", a + c, dn(a + c, [a + c + 100, a + c - 10, a + c + 1]), "Suma unidades, decenas y centenas.", f"{a} + {c} = {a + c}.", r))
    a, c = _sin_reserva(r, 3, 3, resta=True)
    b(co(b.id(), 1, f"{a} − {c} = ___", a - c, dn(a - c, [a - c + 100, a - c - 10, a + c]), "Resta por columnas.", f"{a} − {c} = {a - c}.", r))
    a, c = _con_reserva_suma(r, 3, 3)
    b(nu(b.id(), 2, f"¿Cuánto es {a} + {c}?", a + c, "Lleva la reserva a la columna siguiente.", f"{a} + {c} = {a + c}."))
    c = r.randint(123, 389)
    b(nu(b.id(), 2, f"¿Cuánto es 803 − {c}?", 803 - c, "Con un 0 en las decenas, pide prestado a las centenas.", f"803 − {c} = {803 - c}."))
    a, c = _con_reserva_resta(r, 3, 3)
    b(co(b.id(), 2, f"{a} − {c} = ___", a - c, dn(a - c, [a - c + 10, a - c + 100, a - c - 1]), "Si arriba hay menos, pide prestado.", f"{a} − {c} = {a - c}.", r))
    a, c = _con_reserva_suma(r, 3, 3)
    b(om(b.id(), 2, f"¿Cuánto es {a} + {c}?", a + c, dn(a + c, [a + c - 10, a + c - 100, a + c + 1]), "No olvides lo que llevas.", f"{a} + {c} = {a + c}.", r))
    b(om(b.id(), 3, "Estima 398 + 205 redondeando cada número a la centena más cercana.", 600, [500, 700, 603], "398 está cerca de 400 y 205 cerca de 200.", "400 + 200 = 600. (El resultado exacto es 603.)", r))
    b(nu(b.id(), 3, "Estima 512 + 289. No necesitas el número exacto: basta con una buena estimación.", 800,
         "Redondea a la centena: 500 + 300.", "512 + 289 es aproximadamente 500 + 300 = 800 (exacto: 801).", tolerancia=50))
    b(nu(b.id(), 3, "Estima 712 − 395. Basta con una buena estimación.", 300, "Redondea: 700 − 400.", "712 − 395 es aproximadamente 700 − 400 = 300 (exacto: 317).", tolerancia=50))
    b(om(b.id(), 3, "¿Cuál es la mejor estimación de 489 + 312?", 800, [700, 900, 1000], "489 está cerca de 500 y 312 cerca de 300.", "500 + 300 = 800 (exacto: 801).", r))
    b(nu(b.id(), 4, "En {lugar} hay 734 {objetos}. {personaje} usa 458 para {la_construccion}. ¿Cuántos quedan?", 276, "Usar es restar.", "734 − 458 = 276."))
    b(nu(b.id(), 4, "{personaje} junta 385 {objetos} el lunes y 467 el martes. ¿Cuántos juntó en total?", 852, "En total: suma.", "385 + 467 = 852."))
    b(nu(b.id(), 4, "{personaje} necesita 1000 {objetos}. Ya tiene 628. ¿Cuántos le faltan?", 372, "Lo que falta es la diferencia.", "1000 − 628 = 372."))
    b(em(b.id(), 4, "Une cada operación con su resultado.", [["456 + 278", "734"], ["900 − 365", "535"], ["619 + 183", "802"]],
         "Resuelve cada una con cuidado con la reserva.", "456 + 278 = 734, 900 − 365 = 535 y 619 + 183 = 802."))
    b(co(b.id(), 5, "___ − 247 = 389", 636, [142, 626, 536], "Piensa al revés: 389 + 247.", "389 + 247 = 636.", r))
    b(nu(b.id(), 5, "{personaje} tenía 540 {objetos}. Ganó 275 y luego regaló 390. ¿Cuántos tiene ahora?", 425, "Primero suma y después resta.", "540 + 275 = 815 y 815 − 390 = 425."))
    b(cat(b.id(), 5, "¿El resultado es mayor que 500?", ["500 o menos", "Mayor que 500"],
          [("845 − 367", 0), ("238 + 259", 0), ("700 − 215", 0), ("264 + 248", 1), ("901 − 388", 1), ("199 + 302", 1)],
          "Calcula cada operación.", "845 − 367 = 478, 238 + 259 = 497, 700 − 215 = 485; 264 + 248 = 512, 901 − 388 = 513, 199 + 302 = 501."))
    b(om(b.id(), 5, "Para comprobar que 925 − 478 = 447, ¿qué cálculo sirve?", "447 + 478", ["925 + 478", "447 − 478", "925 − 447 − 478"], "La suma comprueba la resta.", "Si 447 + 478 = 925, la resta está bien.", r))
    return b.items


def ma04_oa5():
    b = Banco(4, 5, 405); r = b.r
    for a, c in [(300, 3), (200, 4)]:
        b(nu(b.id(), 1, f"¿Cuánto es {a} × {c}?", a * c, f"{a // 100} centenas × {c}.", f"{a} × {c} = {miles(a * c)}."))
    b(om(b.id(), 1, "¿Cuánto es 400 × 2?", 800, [600, 420, 80], "4 centenas × 2.", "400 × 2 = 800.", r))
    b(nu(b.id(), 1, "¿Cuánto es 120 × 3?", 360, "12 decenas × 3 = 36 decenas.", "120 × 3 = 360."))
    for a, c in [(213, 3), (132, 2)]:
        b(nu(b.id(), 2, f"¿Cuánto es {a} × {c}?", a * c, "Multiplica unidades, decenas y centenas.", f"{a} × {c} = {a * c}."))
    b(co(b.id(), 2, "321 × 3 = ___", 963, [933, 663, 324], "Multiplica cada cifra por 3.", "321 × 3 = 963.", r))
    b(nu(b.id(), 2, "¿Cuánto es 111 × 7?", 777, "Cada cifra 1 se multiplica por 7.", "111 × 7 = 777."))
    for a, c in [(254, 3), (467, 2)]:
        b(nu(b.id(), 3, f"¿Cuánto es {a} × {c}?", a * c, "Si un producto pasa de 9, llevas la reserva.", f"{a} × {c} = {miles(a * c)}."))
    b(om(b.id(), 3, "¿Cuánto es 315 × 4?", 1260, [1240, 1200, 319], "Multiplica por 4 cada cifra y suma las reservas.", "315 × 4 = 1.260.", r))
    b(nu(b.id(), 3, "¿Cuánto es 128 × 6?", 768, "8 × 6 = 48: escribe 8 y llevas 4.", "128 × 6 = 768."))
    b(co(b.id(), 4, "4 × 253 = 4 × 200 + 4 × 50 + 4 × ___", 3, [5, 25, 53], "253 = 200 + 50 + 3.", "4 × 253 = 800 + 200 + 12 = 1.012.", r))
    b(nu(b.id(), 4, "Estima 298 × 4. Basta con una buena estimación.", 1200, "298 está cerca de 300.", "300 × 4 = 1.200 (exacto: 1.192).", tolerancia=50))
    b(om(b.id(), 4, "¿Qué cálculo sirve para resolver 5 × 312?", "5 × 300 + 5 × 12", ["5 × 300 + 12", "5 + 312", "5 × 3 + 5 × 12"], "Descompón 312 en 300 + 12.", "5 × 312 = 5 × 300 + 5 × 12 = 1.500 + 60 = 1.560.", r))
    b(em(b.id(), 4, "Une cada multiplicación con su resultado.", [["150 × 4", "600"], ["205 × 3", "615"], ["122 × 5", "610"]],
         "Usa la descomposición.", "150 × 4 = 600, 205 × 3 = 615 y 122 × 5 = 610."))
    b(nu(b.id(), 5, "{personaje} pone 125 {objetos} en cada {contenedor}. Tiene 6 {contenedores}. ¿Cuántos {objetos} guarda?", 750, "Son 6 veces 125.", "125 × 6 = 750."))
    b(nu(b.id(), 5, "Cada día {personaje} junta 175 {objetos}. ¿Cuántos junta en una semana (7 días)?", 1225, "Multiplica 175 por 7.", "175 × 7 = 1.225."))
    b(om(b.id(), 5, "En {lugar} hay 4 grupos de 236 {objetos}. ¿Cuántos hay en total?", 944, [924, 240, 836], "4 × 236.", "4 × 236 = 944.", r))
    b(cat(b.id(), 5, "¿El producto es mayor que 1.000?", ["1.000 o menos", "Mayor que 1.000"],
          [("245 × 4", 0), ("199 × 5", 0), ("320 × 3", 0), ("251 × 4", 1), ("170 × 6", 1), ("505 × 2", 1)],
          "Estima primero cada producto.", "245 × 4 = 980, 199 × 5 = 995, 320 × 3 = 960; 251 × 4 = 1.004, 170 × 6 = 1.020, 505 × 2 = 1.010."))
    return b.items


def ma04_oa6():
    b = Banco(4, 6, 406); r = b.r
    for d, q in [(4, 9), (5, 9)]:
        b(nu(b.id(), 1, f"¿Cuánto es {d * q} ÷ {d}?", q, f"Usa la tabla del {d}.", f"{d * q} ÷ {d} = {q}."))
    b(om(b.id(), 1, "¿Cuánto es 63 ÷ 7?", 9, [8, 7, 56], "7 × ? = 63.", "63 ÷ 7 = 9.", r))
    b(co(b.id(), 1, "48 ÷ 6 = ___", 8, [6, 7, 9], "6 × ? = 48.", "48 ÷ 6 = 8.", r))
    for d, q in [(4, 21), (3, 32)]:
        b(nu(b.id(), 2, f"¿Cuánto es {d * q} ÷ {d}?", q, f"Descompón: {d * q} = {d * (q // 10 * 10)} + {d * (q % 10)}.", f"{d * q} ÷ {d} = {q}."))
    b(om(b.id(), 2, "¿Cuánto es 75 ÷ 5?", 15, [13, 25, 17], "75 = 50 + 25.", "50 ÷ 5 + 25 ÷ 5 = 10 + 5 = 15.", r))
    b(nu(b.id(), 2, "¿Cuánto es 91 ÷ 7?", 13, "91 = 70 + 21.", "70 ÷ 7 + 21 ÷ 7 = 10 + 3 = 13."))
    b(om(b.id(), 3, "¿Cuánto es 47 ÷ 5?", "cociente 9, resto 2", ["cociente 8, resto 7", "cociente 9, resto 0", "cociente 7, resto 2"], "5 × 9 = 45. ¿Cuánto falta para 47?", "47 = 5 × 9 + 2: cociente 9, resto 2.", r))
    b(nu(b.id(), 3, "¿Cuál es el resto de 38 ÷ 6?", 2, "6 × 6 = 36.", "38 = 6 × 6 + 2: el resto es 2."))
    b(nu(b.id(), 3, "¿Cuál es el cociente de 59 ÷ 8?", 7, "8 × 7 = 56 y 8 × 8 = 64.", "59 = 8 × 7 + 3: el cociente es 7."))
    b(om(b.id(), 3, "¿Cuánto es 29 ÷ 4?", "cociente 7, resto 1", ["cociente 6, resto 5", "cociente 7, resto 0", "cociente 8, resto 1"], "4 × 7 = 28.", "29 = 4 × 7 + 1.", r))
    b(om(b.id(), 4, "El cociente de 78 ÷ 4 está más cerca de…", 20, [10, 30, 40], "4 × 20 = 80, muy cerca de 78.", "78 ÷ 4 = 19,5, cerca de 20.", r))
    b(nu(b.id(), 4, "{personaje} reparte 72 {objetos} en partes iguales entre 6 amigos. ¿Cuántos recibe cada uno?", 12, "72 = 60 + 12.", "72 ÷ 6 = 12."))
    b(nu(b.id(), 4, "Hay 84 {objetos} y se guardan 7 en cada {contenedor}. ¿Cuántos {contenedores} se llenan?", 12, "¿Cuántas veces cabe 7 en 84?", "84 ÷ 7 = 12."))
    b(em(b.id(), 4, "Une cada división con su cociente.", [["96 ÷ 8", "12"], ["65 ÷ 5", "13"], ["88 ÷ 4", "22"]], "Descompón el dividendo.", "96 ÷ 8 = 12, 65 ÷ 5 = 13 y 88 ÷ 4 = 22."))
    b(nu(b.id(), 5, "{personaje} quiere guardar 52 {objetos} en {contenedores} donde caben 5. ¿Cuántos {contenedores} necesita para guardarlos todos?", 11,
         "52 ÷ 5 = 10 y sobran 2: esos 2 también necesitan lugar.", "Con 10 se guardan 50; para los 2 que sobran hace falta 1 más: 11."))
    b(nu(b.id(), 5, "{personaje} tiene 45 {objetos} y arma grupos de 7. ¿Cuántos grupos completos arma?", 6, "7 × 6 = 42.", "45 = 7 × 6 + 3: arma 6 grupos completos."))
    b(nu(b.id(), 5, "Con 45 {objetos} en grupos de 7, ¿cuántos {objetos} sobran?", 3, "7 × 6 = 42.", "45 − 42 = 3."))
    b(cat(b.id(), 5, "¿La división es exacta o tiene resto?", ["Exacta", "Con resto"],
          [("56 ÷ 7", 0), ("81 ÷ 9", 0), ("64 ÷ 4", 0), ("50 ÷ 6", 1), ("73 ÷ 8", 1), ("38 ÷ 5", 1)],
          "Una división es exacta si el resto es 0.", "56 ÷ 7 = 8, 81 ÷ 9 = 9 y 64 ÷ 4 = 16 son exactas; las otras tienen resto."))
    return b.items


def ma04_oa8():
    b = Banco(4, 8, 408); r = b.r
    for tot, part in [(8, 3), (6, 5), (10, 7)]:
        f = f"{part}/{tot}"
        b(om(b.id(), 1, f"De {tot} {{objetos}}, {part} son nuevos. ¿Qué fracción de {{los_objetos}} son nuevos?", f, [f"{tot}/{part}", f"{tot - part}/{tot}", f"{part}/{tot + part}"],
             "Arriba va la parte; abajo, el total.", f"{part} de {tot} es {f}."))
    b(co(b.id(), 1, "Si una barra se divide en 5 partes iguales y se pintan 2, se pintó ___ de la barra.", "2/5", ["5/2", "3/5", "2/7"], "Arriba: partes pintadas. Abajo: partes totales.", "2 de 5 partes es 2/5.", r))
    for f, eq, ds in [("1/2", "2/4", ["1/4", "2/3", "3/4"]), ("1/3", "2/6", ["2/3", "1/6", "3/6"]), ("3/4", "6/8", ["3/8", "4/6", "6/4"])]:
        b(om(b.id(), 2, f"¿Qué fracción es equivalente a {f}?", eq, ds, "Multiplica arriba y abajo por el mismo número.", f"{f} = {eq}: se multiplicó arriba y abajo por 2."))
    b(em(b.id(), 2, "Une cada fracción con su equivalente.", [["1/2", "4/8"], ["1/5", "2/10"], ["2/3", "4/6"]], "Multiplica arriba y abajo por el mismo número.", "1/2 = 4/8, 1/5 = 2/10 y 2/3 = 4/6."))
    b(om(b.id(), 3, "¿Cuál es mayor?", "5/8", ["3/8", "Son iguales", "No se puede saber"], "Mismo denominador: compara los numeradores.", "5 octavos es más que 3 octavos."))
    b(om(b.id(), 3, "¿Cuál es mayor?", "1/3", ["1/5", "Son iguales", "No se puede saber"], "Mismo numerador: con menos partes, cada parte es más grande.", "Un tercio es más grande que un quinto."))
    b(co(b.id(), 3, "2/7 ___ 5/7", "<", [">", "=", "+"], "Mismo denominador: compara los numeradores.", "2/7 es menor que 5/7."))
    b(orden(b.id(), 3, "Ordena de menor a mayor.", ["1/6", "3/6", "4/6", "5/6"], "Mismo denominador: ordena por el numerador.", "1/6 < 3/6 < 4/6 < 5/6."))
    b(om(b.id(), 4, "Una recta de 0 a 1 está dividida en 4 partes iguales. ¿Qué fracción marca la tercera división?", "3/4", ["1/3", "4/3", "1/4"], "Cuenta los saltos desde el 0.", "3 saltos de 1/4 llegan a 3/4."))
    b(om(b.id(), 4, "Una recta de 0 a 1 está dividida en 5 partes iguales. ¿Qué fracción marca la segunda división?", "2/5", ["1/2", "5/2", "2/3"], "Cada salto vale 1/5.", "2 saltos de 1/5 llegan a 2/5."))
    b(om(b.id(), 4, "¿Qué fracción está justo a la mitad entre 0 y 1?", "1/2", ["1/4", "1/3", "2/3"], "Mitad del camino.", "La mitad entre 0 y 1 es 1/2."))
    b(orden(b.id(), 4, "Ordena de menor a mayor.", ["1/8", "1/4", "1/2"], "Mismo numerador: más partes significa partes más pequeñas.", "1/8 < 1/4 < 1/2."))
    b(cat(b.id(), 5, "¿Es equivalente a 1/2?", ["Equivale a 1/2", "No equivale"], [("2/4", 0), ("3/6", 0), ("4/8", 0), ("5/10", 0), ("2/3", 1), ("3/5", 1), ("1/4", 1)],
          "Una fracción equivale a 1/2 si el numerador es la mitad del denominador.", "2/4, 3/6, 4/8 y 5/10 son iguales a 1/2."))
    b(em(b.id(), 5, "Une las fracciones equivalentes.", [["2/6", "1/3"], ["6/8", "3/4"], ["4/10", "2/5"], ["8/12", "2/3"]],
         "Simplifica: divide arriba y abajo por el mismo número.", "2/6 = 1/3, 6/8 = 3/4, 4/10 = 2/5 y 8/12 = 2/3."))
    b(om(b.id(), 5, "{personaje} usó 2/6 de {los_objetos} y Lía usó 1/3. ¿Quién usó más?", "Usaron lo mismo", ["{personaje}", "Lía", "No se puede saber"], "Simplifica 2/6.", "2/6 = 1/3: usaron lo mismo."))
    b(co(b.id(), 5, "4/8 = 1/___", 2, [4, 8, 3], "Divide arriba y abajo por 4.", "4/8 = 1/2.", r))
    return b.items


GENERADORES = {
    "3_basico.matematica.OA6": ma03_oa6, "3_basico.matematica.OA8": ma03_oa8, "3_basico.matematica.OA9": ma03_oa9,
    "3_basico.matematica.OA11": ma03_oa11, "4_basico.matematica.OA3": ma04_oa3, "4_basico.matematica.OA5": ma04_oa5,
    "4_basico.matematica.OA6": ma04_oa6, "4_basico.matematica.OA8": ma04_oa8,
}
