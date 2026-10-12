"""Matemática 1° y 2° básico: 20 desafíos por OA (4 por nivel de dificultad, 1 a 5)."""
from comun import (opcion_multiple as om, completar as co, ordenar as orden, emparejar as em,
                   categoria as cat, numerica as nu, distractores_numericos as dn, rng_para)


class Banco:
    def __init__(self, curso, oa, semilla):
        self.curso, self.oa, self.k, self.r, self.items = curso, oa, 0, rng_para(semilla), []

    def id(self):
        self.k += 1
        return f"mat{self.curso}-oa{self.oa}-{self.k:03d}"

    def __call__(self, item):
        self.items.append(item)


def serie(inicio, paso, n):
    return [inicio + paso * i for i in range(n)]


def _sig(b, nivel, inicio, paso, n=3, enun=None):
    s = serie(inicio, paso, n + 1)
    txt = enun or (f"Cuenta de {abs(paso)} en {abs(paso)}" + (" hacia atrás" if paso < 0 else "") + ". ¿Qué número sigue?")
    b(nu(b.id(), nivel, f"{txt} {', '.join(map(str, s[:n]))}, ___", s[n],
         f"Mira cuánto cambia cada número: {'resta' if paso < 0 else 'suma'} {abs(paso)}.",
         f"Después de {s[n - 1]} viene {s[n]}: {'le restamos' if paso < 0 else 'le sumamos'} {abs(paso)}."))


# ---------------- 1° básico ----------------
def ma01_oa1():
    b = Banco(1, 1, 101); r = b.r
    # nivel 1: contar de 1 en 1 hasta 20
    _sig(b, 1, r.randint(1, 8), 1); _sig(b, 1, r.randint(9, 15), 1)
    s = r.randint(2, 14)
    b(orden(b.id(), 1, "Ordena los números como cuando cuentas de 1 en 1.", serie(s, 1, 4),
            "Empieza por el más pequeño.", f"Al contar de 1 en 1 el orden es {s}, {s + 1}, {s + 2}, {s + 3}."))
    n = r.randint(6, 19)
    b(om(b.id(), 1, f"¿Qué número va justo antes de {n}?", n - 1, [n + 1, n - 2, n + 2],
         "Antes significa uno menos.", f"Justo antes de {n} está {n - 1}.", r))
    # nivel 2: hasta 100, adelante y atrás, cruzando decenas
    a = r.choice([28, 38, 48, 58, 68, 78, 88]); _sig(b, 2, a, 1, 2)
    _sig(b, 2, r.randint(43, 99), -1)
    c = r.randint(52, 88)
    b(co(b.id(), 2, f"{{personaje}} cuenta {{objetos}}: {c}, {c + 1}, ___, {c + 3}.", c + 2, [c + 4, c - 1, c + 12],
         "Falta el número que va entre los dos de los lados.", f"Entre {c + 1} y {c + 3} va {c + 2}.", r))
    d = r.randint(35, 96)
    b(orden(b.id(), 2, "Ordena como cuando cuentas hacia atrás de 1 en 1.", serie(d, -1, 4),
            "Hacia atrás, cada número es uno menos.", f"Hacia atrás: {d}, {d - 1}, {d - 2}, {d - 3}."))
    # nivel 3: de 10 en 10 y de 5 en 5
    _sig(b, 3, 10 * r.randint(1, 5), 10); _sig(b, 3, 5 * r.randint(1, 12), 5)
    u = r.randint(1, 9)
    b(co(b.id(), 3, f"Cuenta de 10 en 10: {u}, {u + 10}, {u + 20}, ___", u + 30, [u + 21, 30, u + 40],
         "Contar de 10 en 10 cambia solo las decenas.", f"{u + 20} + 10 = {u + 30}.", r))
    s5 = 5 * r.randint(2, 14)
    b(orden(b.id(), 3, "Ordena los números como cuando cuentas de 5 en 5.", serie(s5, 5, 4),
            "Cada número es 5 más que el anterior.", f"De 5 en 5: {', '.join(map(str, serie(s5, 5, 4)))}."))
    # nivel 4: de 2 en 2 y hacia atrás de 10 en 10
    _sig(b, 4, 2 * r.randint(15, 40), 2); _sig(b, 4, 10 * r.randint(6, 10), -10)
    o = 2 * r.randint(10, 40) + 1
    b(co(b.id(), 4, f"Cuenta de 2 en 2: {o}, {o + 2}, ___, {o + 6}", o + 4, [o + 3, o + 5, o + 1],
         "Si empiezas en un número impar, contando de 2 en 2 sigues en impares.", f"{o + 2} + 2 = {o + 4}.", r))
    si = [5 * r.randint(1, 19) for _ in range(3)]
    si = sorted(set(si))
    while len(si) < 3:
        si = sorted(set(si + [5 * r.randint(1, 19)]))
    no = []
    while len(no) < 3:
        x = r.randint(11, 98)
        if x % 5 and x not in no:
            no.append(x)
    b(cat(b.id(), 4, "¿Aparece al contar de 5 en 5 desde 0?", ["Sí aparece", "No aparece"],
          [(x, 0) for x in si] + [(x, 1) for x in no],
          "Contando de 5 en 5 desde 0, los números terminan en 0 o en 5.",
          "Solo los números que terminan en 0 o en 5 aparecen al contar de 5 en 5."))
    # nivel 5: identificar el paso y contar hacia atrás de 5 y de 2
    pasos = ["de 1 en 1", "de 2 en 2", "de 5 en 5", "de 10 en 10"]
    for paso, txt in [(5, "de 5 en 5"), (2, "de 2 en 2")]:
        s = serie(paso * r.randint(6, 15), paso, 4)
        b(om(b.id(), 5, f"¿De cuánto en cuánto se cuenta? {', '.join(map(str, s))}", txt, [p for p in pasos if p != txt],
             "Resta dos números seguidos de la serie.", f"Cada número aumenta {paso}: se cuenta {txt}.", r))
    _sig(b, 5, 5 * r.randint(12, 20), -5); _sig(b, 5, 2 * r.randint(35, 50), -2)
    return b.items


def ma01_oa4():
    b = Banco(1, 4, 104); r = b.r

    def distintos(n, lo, hi):
        return r.sample(range(lo, hi + 1), n)

    # nivel 1: hasta 10
    xs = distintos(4, 0, 10)
    b(om(b.id(), 1, "¿Cuál es el número mayor?", max(xs), [x for x in xs if x != max(xs)],
         "El mayor es el que está más lejos del 0 al contar.", f"{max(xs)} es el mayor de los cuatro.", r))
    xs = distintos(4, 0, 10)
    b(om(b.id(), 1, "¿Cuál es el número menor?", min(xs), [x for x in xs if x != min(xs)],
         "El menor es el que aparece primero al contar.", f"{min(xs)} es el menor de los cuatro.", r))
    m = r.randint(2, 8)
    b(om(b.id(), 1, f"¿Qué número está entre {m - 1} y {m + 1}?", m, [m - 2, m + 2, m + 3],
         "Cuenta desde el primero hasta el segundo.", f"Entre {m - 1} y {m + 1} está {m}.", r))
    xs = sorted(distintos(3, 0, 10))
    b(orden(b.id(), 1, "Ordena de menor a mayor.", xs, "Pon primero el más pequeño.", f"De menor a mayor: {', '.join(map(str, xs))}."))
    # nivel 2: hasta 20
    xs = distintos(4, 11, 20)
    b(om(b.id(), 2, "¿Cuál es el número mayor?", max(xs), [x for x in xs if x != max(xs)],
         "Todos tienen una decena: compara las unidades.", f"{max(xs)} es el mayor.", r))
    xs = distintos(4, 0, 20)
    b(om(b.id(), 2, "¿Cuál es el número menor?", min(xs), [x for x in xs if x != min(xs)],
         "Busca el que tiene menos.", f"{min(xs)} es el menor.", r))
    a = r.randint(8, 16); menor = r.randint(1, a - 1); mayores = r.sample(range(a, 21), 3)
    b(co(b.id(), 2, f"{a} es mayor que ___", menor, mayores, "Busca un número más pequeño.", f"{a} es mayor que {menor}.", r))
    xs = sorted(distintos(4, 0, 20))
    b(orden(b.id(), 2, "Ordena de menor a mayor.", xs, "Empieza por el más pequeño.", f"De menor a mayor: {', '.join(map(str, xs))}."))
    # nivel 3
    xs = sorted(distintos(4, 0, 20), reverse=True)
    b(orden(b.id(), 3, "Ordena de mayor a menor.", xs, "Empieza por el más grande.", f"De mayor a menor: {', '.join(map(str, xs))}."))
    xs = sorted(distintos(5, 0, 20))
    b(orden(b.id(), 3, "Ordena de menor a mayor.", xs, "Compara de a dos números.", f"De menor a mayor: {', '.join(map(str, xs))}."))
    men = distintos(3, 0, 9); may = distintos(3, 11, 20)
    b(cat(b.id(), 3, "Separa los números.", ["Menores que 10", "Mayores que 10"], [(x, 0) for x in men] + [(x, 1) for x in may],
          "Los números con una decena son mayores que 10.", "Del 0 al 9 son menores que 10; del 11 al 20, mayores."))
    p, q = r.sample(range(11, 20), 2)
    quien = "Lía" if q > p else "{personaje}"
    b(om(b.id(), 3, f"En {{el_contenedor}} de {{personaje}} hay {p} {{objetos}} y en el de Lía hay {q}. ¿Quién tiene más?", quien,
         [x for x in ["Lía", "{personaje}", "Tienen lo mismo", "No se puede saber"] if x != quien][:3],
         "Compara los dos números.", f"{max(p, q)} es mayor que {min(p, q)}.", r))
    # nivel 4: signos y rangos
    for a, c in [tuple(sorted(r.sample(range(10, 20), 2))), tuple(sorted(r.sample(range(10, 20), 2), reverse=True))]:
        sig = "<" if a < c else ">"
        b(co(b.id(), 4, f"{a} ___ {c}", sig, [s for s in ["<", ">", "=", "+"] if s != sig],
             "La boca del signo se abre hacia el número mayor.", f"{a} es {'menor' if a < c else 'mayor'} que {c}: se usa {sig}.", r))
    den = distintos(3, 5, 15); fue = distintos(2, 0, 4) + distintos(1, 16, 20)
    b(cat(b.id(), 4, "¿Está entre 5 y 15 (incluidos)?", ["Entre 5 y 15", "Fuera de ese rango"], [(x, 0) for x in den] + [(x, 1) for x in fue],
          "Revisa si cada número es al menos 5 y como máximo 15.", "Los números del 5 al 15 están en el rango; los demás, fuera."))
    xs = sorted(distintos(5, 0, 20), reverse=True)
    b(orden(b.id(), 4, "Ordena de mayor a menor.", xs, "Busca primero el mayor.", f"De mayor a menor: {', '.join(map(str, xs))}."))
    # nivel 5
    xs = [17, 12, 9, 14]
    b(om(b.id(), 5, "¿Cuál de estos números está más cerca de 20?", 17, [12, 9, 14], "Mira cuánto le falta a cada uno para llegar a 20.", "A 17 le faltan solo 3 para llegar a 20.", r))
    n = r.randint(11, 19)
    b(co(b.id(), 5, f"{n} ___ {n}", "=", ["<", ">", "+"], "Mira bien: ¿los dos números son iguales?", f"{n} es igual a {n}: se usa =.", r))
    xs = sorted(r.sample(range(11, 20), 5))
    b(orden(b.id(), 5, "Ordena de menor a mayor.", xs, "Todos tienen una decena: compara las unidades.", f"De menor a mayor: {', '.join(map(str, xs))}."))
    b(om(b.id(), 5, "¿Qué número es menor que 15 pero mayor que 12?", 13, [11, 16, 15],
         "Tiene que cumplir las dos condiciones.", "13 es mayor que 12 y menor que 15.", r))
    return b.items


def ma01_oa9():
    b = Banco(1, 9, 109); r = b.r
    # nivel 1: 0 a 5
    a, c = r.randint(1, 3), r.randint(1, 2)
    b(nu(b.id(), 1, f"¿Cuánto es {a} + {c}?", a + c, "Cuenta hacia adelante desde el número mayor.", f"{a} + {c} = {a + c}."))
    a = r.randint(3, 5); c = r.randint(1, a)
    b(nu(b.id(), 1, f"¿Cuánto es {a} − {c}?", a - c, "Quitar es contar hacia atrás.", f"{a} − {c} = {a - c}."))
    a, c = 1, 3
    b(om(b.id(), 1, f"¿Cuánto es {a} + {c}?", 4, [3, 5, 2], "Junta los dos grupos.", "1 + 3 = 4.", r))
    b(em(b.id(), 1, "Une cada operación con su resultado.", [["2 + 1", "3"], ["4 + 1", "5"], ["2 − 2", "0"]],
         "Resuelve cada operación antes de unir.", "2 + 1 = 3, 4 + 1 = 5 y 2 − 2 = 0."))
    # nivel 2: 6 a 10
    a = r.randint(3, 6); c = r.randint(2, 10 - a)
    b(nu(b.id(), 2, f"¿Cuánto es {a} + {c}?", a + c, "Parte del mayor y suma de a uno.", f"{a} + {c} = {a + c}."))
    a = r.randint(7, 10); c = r.randint(2, 6)
    b(nu(b.id(), 2, f"¿Cuánto es {a} − {c}?", a - c, "Cuenta hacia atrás desde el primer número.", f"{a} − {c} = {a - c}."))
    a = r.randint(7, 10); c = r.randint(1, 5)
    b(co(b.id(), 2, f"{a} − {c} = ___", a - c, dn(a - c, [a + c, a - c + 1, a - c - 1]), "Quita de a uno.", f"{a} − {c} = {a - c}.", r))
    a = r.randint(2, 5); c = r.randint(2, 5)
    b(nu(b.id(), 2, f"{{personaje}} {{junto}} {a} {{objetos}} y después {c} más. ¿Cuántos tiene ahora?", a + c,
         "Junta las dos cantidades.", f"{a} + {c} = {a + c}."))
    # nivel 3: 11 a 20
    a = r.randint(6, 9); c = r.randint(11 - a, 9)
    b(nu(b.id(), 3, f"¿Cuánto es {a} + {c}?", a + c, f"Completa 10 primero: {a} + {10 - a} = 10.", f"{a} + {c} = {a + c}."))
    a = r.randint(12, 18); c = r.randint(3, 9)
    b(nu(b.id(), 3, f"¿Cuánto es {a} − {c}?", a - c, "Puedes restar primero hasta llegar a 10.", f"{a} − {c} = {a - c}."))
    a = r.randint(9, 12); c = r.randint(5, 20 - a)
    b(nu(b.id(), 3, f"{{personaje}} {{junto}} {a} {{objetos}} y después {c} más. ¿Cuántos {{objetos}} tiene ahora?", a + c,
         "Juntar es sumar.", f"{a} + {c} = {a + c}."))
    a = r.randint(11, 15); c = r.randint(2, 5)
    b(om(b.id(), 3, f"¿Cuánto es {a} + {c}?", a + c, dn(a + c, [a + c + 1, a + c - 1, a + c + 10]), "Suma solo las unidades.", f"{a} + {c} = {a + c}.", r))
    # nivel 4: problemas
    a = r.randint(13, 19); c = r.randint(5, 9)
    b(nu(b.id(), 4, f"{{personaje}} tenía {a} {{objetos}} y usó {c} en {{la_construccion}}. ¿Cuántos le quedan?", a - c,
         "Usar es quitar: resta.", f"{a} − {c} = {a - c}."))
    ops = [(8, 7), (9, 5), (6, 6), (13, 4)]
    b(em(b.id(), 4, "Une cada suma con su resultado.", [[f"{x} + {y}", str(x + y)] for x, y in ops],
         "Resuelve cada suma.", "8 + 7 = 15, 9 + 5 = 14, 6 + 6 = 12 y 13 + 4 = 17."))
    b(cat(b.id(), 4, "¿El resultado es menor que 10 o es 10 o más?", ["Menor que 10", "10 o más"],
          [("3 + 4", 0), ("15 − 8", 0), ("12 − 5", 0), ("6 + 5", 1), ("9 + 3", 1), ("18 − 7", 1)],
          "Calcula primero cada operación.", "3 + 4 = 7, 15 − 8 = 7, 12 − 5 = 7; 6 + 5 = 11, 9 + 3 = 12, 18 − 7 = 11."))
    a = r.randint(4, 8); c = r.randint(4, 8)
    b(nu(b.id(), 4, f"En {{el_contenedor}} hay {a} {{objetos}}. {{personaje}} agrega {c}. ¿Cuántos hay ahora?", a + c,
         "Agregar es sumar.", f"{a} + {c} = {a + c}."))
    # nivel 5: términos que faltan y operaciones inversas
    a = r.randint(5, 9); t = r.randint(12, 18)
    b(co(b.id(), 5, f"{a} + ___ = {t}", t - a, dn(t - a, [t, t - a + 1, t + a]), f"¿Cuánto le falta a {a} para llegar a {t}?", f"{a} + {t - a} = {t}.", r))
    b(om(b.id(), 5, "Si 9 + 6 = 15, entonces 15 − 6 = ?", 9, [6, 15, 21], "La resta deshace la suma.", "Si 9 + 6 = 15, entonces 15 − 6 = 9.", r))
    t = r.randint(12, 15); c = r.randint(3, 5)
    b(nu(b.id(), 5, f"¿Qué número menos {c} da {t}?", t + c, "Piensa al revés: suma.", f"{t + c} − {c} = {t}."))
    a = r.randint(11, 16); c = r.randint(2, 4)
    b(nu(b.id(), 5, f"{{personaje}} tiene {a} {{objetos}} y Lía tiene {c} menos. ¿Cuántos tiene Lía?", a - c,
         "Tener menos significa restar.", f"{a} − {c} = {a - c}."))
    return b.items


# ---------------- 2° básico ----------------
def ma02_oa1():
    b = Banco(2, 1, 201); r = b.r
    _sig(b, 1, 10 * r.randint(2, 6), 10); _sig(b, 1, 10 * r.randint(10, 15), 10)
    s = 10 * r.randint(15, 60)
    b(orden(b.id(), 1, "Ordena como cuando cuentas de 10 en 10.", serie(s, 10, 4), "Cada número tiene una decena más.", f"De 10 en 10: {', '.join(map(str, serie(s, 10, 4)))}."))
    c = 10 * r.randint(20, 80)
    b(co(b.id(), 1, f"Cuenta de 10 en 10: {c}, ___, {c + 20}", c + 10, [c + 1, c + 100, c + 11], "Solo cambian las decenas.", f"{c} + 10 = {c + 10}.", r))
    _sig(b, 2, 100, 100); c = 100 * r.randint(2, 6)
    b(co(b.id(), 2, f"Cuenta de 100 en 100: {c}, ___, {c + 200}", c + 100, [c + 10, c + 1, c + 50], "Solo cambian las centenas.", f"{c} + 100 = {c + 100}.", r))
    _sig(b, 2, 100 * r.randint(7, 10), -100)
    s = 100 * r.randint(1, 5)
    b(orden(b.id(), 2, "Ordena como cuando cuentas de 100 en 100.", serie(s, 100, 4), "Mira las centenas.", f"De 100 en 100: {', '.join(map(str, serie(s, 100, 4)))}."))
    _sig(b, 3, 5 * r.randint(40, 180), 5); _sig(b, 3, 2 * r.randint(150, 400), 2)
    s = 5 * r.randint(50, 190)
    b(orden(b.id(), 3, "Ordena como cuando cuentas de 5 en 5.", serie(s, 5, 4), "Cada número es 5 más.", f"De 5 en 5: {', '.join(map(str, serie(s, 5, 4)))}."))
    c = 2 * r.randint(200, 450)
    b(co(b.id(), 3, f"Cuenta de 2 en 2: {c}, {c + 2}, ___", c + 4, [c + 3, c + 20, c + 5], "Suma 2 al último número.", f"{c + 2} + 2 = {c + 4}.", r))
    _sig(b, 4, 10 * r.randint(40, 95), -10); _sig(b, 4, 100 * r.randint(7, 10), -100)
    c = 2 * r.randint(150, 450)
    b(co(b.id(), 4, f"Cuenta hacia atrás de 2 en 2: {c}, {c - 2}, ___", c - 4, [c - 3, c - 20, c], "Resta 2 al último número.", f"{c - 2} − 2 = {c - 4}.", r))
    si = r.sample([100 * k for k in range(1, 11)], 3); no = r.sample([150, 220, 305, 470, 640, 990], 3)
    b(cat(b.id(), 4, "¿Aparece al contar de 100 en 100 desde 0?", ["Sí aparece", "No aparece"], [(x, 0) for x in si] + [(x, 1) for x in no],
          "Contando de 100 en 100 desde 0, los números terminan en 00.", "Solo aparecen los números que terminan en 00."))
    a = r.randint(101, 499)
    _sig(b, 5, a, 100, 3, "Cuenta de 100 en 100. ¿Qué número sigue?")
    pasos = ["de 2 en 2", "de 5 en 5", "de 10 en 10", "de 100 en 100"]
    s = serie(10 * r.randint(30, 90), 10, 4)
    b(om(b.id(), 5, f"¿De cuánto en cuánto se cuenta? {', '.join(map(str, s))}", "de 10 en 10", [p for p in pasos if p != "de 10 en 10"],
         "Resta dos números seguidos.", "Cada número aumenta 10.", r))
    _sig(b, 5, 5 * r.randint(150, 199), -5)
    b(nu(b.id(), 5, "Cuenta de 100 en 100 hacia atrás. ¿Qué número sigue? 1000, 900, ___", 800, "Resta 100.", "900 − 100 = 800."))
    return b.items


def ma02_oa3():
    b = Banco(2, 3, 203); r = b.r

    def decenas_distintas(n):
        ds = r.sample(range(1, 10), n)
        return [10 * d + r.randint(0, 9) for d in ds]

    def misma_decena(n):
        d = r.randint(2, 9); us = r.sample(range(0, 10), n)
        return [10 * d + u for u in us]

    for nivel, gen in [(1, decenas_distintas), (2, misma_decena)]:
        xs = gen(4)
        b(om(b.id(), nivel, "¿Cuál es el número mayor?", max(xs), [x for x in xs if x != max(xs)],
             "Compara primero las decenas y después las unidades.", f"{max(xs)} es el mayor.", r))
        xs = gen(4)
        b(om(b.id(), nivel, "¿Cuál es el número menor?", min(xs), [x for x in xs if x != min(xs)],
             "Compara primero las decenas y después las unidades.", f"{min(xs)} es el menor.", r))
        a, c = gen(2)
        sig = "<" if a < c else ">"
        b(co(b.id(), nivel, f"{a} ___ {c}", sig, [s for s in ["<", ">", "=", "+"] if s != sig],
             "La boca del signo se abre hacia el número mayor.", f"{a} es {'menor' if a < c else 'mayor'} que {c}.", r))
        xs = sorted(gen(4))
        b(orden(b.id(), nivel, "Ordena de menor a mayor.", xs, "Mira las decenas primero.", f"De menor a mayor: {', '.join(map(str, xs))}."))
    xs = sorted(r.sample(range(10, 100), 4))
    b(orden(b.id(), 3, "Ordena de menor a mayor.", xs, "Compara decenas y luego unidades.", f"De menor a mayor: {', '.join(map(str, xs))}."))
    xs = sorted(r.sample(range(10, 100), 4), reverse=True)
    b(orden(b.id(), 3, "Ordena de mayor a menor.", xs, "Empieza por el mayor.", f"De mayor a menor: {', '.join(map(str, xs))}."))
    men = r.sample(range(10, 50), 3); may = r.sample(range(51, 100), 3)
    b(cat(b.id(), 3, "Separa los números.", ["Menores que 50", "Mayores que 50"], [(x, 0) for x in men] + [(x, 1) for x in may],
          "Mira si las decenas son menos o más que 5.", "Los que tienen 4 decenas o menos son menores que 50."))
    b(om(b.id(), 3, "¿Qué número está entre 56 y 60?", 58, [55, 61, 66], "Tiene que ser mayor que 56 y menor que 60.", "58 está entre 56 y 60.", r))
    a, c = r.sample(range(41, 99), 2)
    sig = "<" if a < c else ">"
    b(co(b.id(), 4, f"{a} ___ {c}", sig, [s for s in ["<", ">", "=", "+"] if s != sig], "Compara las decenas.", f"{a} es {'menor' if a < c else 'mayor'} que {c}.", r))
    p = r.randint(6, 9) * 10 + r.randint(1, 5); q = int(str(p)[::-1])
    quien = "{personaje}" if p > q else "Lía"
    b(om(b.id(), 4, f"{{personaje}} tiene {p} {{objetos}} y Lía tiene {q}. ¿Quién tiene más?", quien,
         [x for x in ["{personaje}", "Lía", "Tienen lo mismo", "No se puede saber"] if x != quien][:3],
         "Tienen los mismos dígitos, pero en distinto lugar: compara las decenas.", f"{max(p, q)} es mayor que {min(p, q)}.", r))
    b(om(b.id(), 4, "¿Cuál es el mayor número de dos cifras que puedes formar con 3 y 8, sin repetir?", 83, [38, 88, 11],
         "Pon la cifra más grande en las decenas.", "Con 8 decenas y 3 unidades se forma 83.", r))
    xs = sorted(misma_decena(3) + [r.randint(10, 19), r.randint(91, 99)])
    b(orden(b.id(), 4, "Ordena de menor a mayor.", xs, "Agrupa por decenas.", f"De menor a mayor: {', '.join(map(str, xs))}."))
    xs = sorted({47, 74, 70, 44, 77}, reverse=True)
    b(orden(b.id(), 5, "Ordena de mayor a menor.", xs, "47 y 74 se parecen, pero tienen distintas decenas.", "De mayor a menor: 77, 74, 70, 47, 44."))
    b(om(b.id(), 5, "¿Cuál de estos números está más cerca de 50?", 48, [41, 58, 62], "Calcula cuánto se aleja cada uno de 50.", "48 está a solo 2 de 50.", r))
    b(om(b.id(), 5, "¿Qué cantidad de dinero es mayor?", "$54", ["$45", "$50", "$49"], "Compara las decenas de pesos.", "$54 tiene 5 decenas y 4 unidades: es la mayor.", r))
    a, c = r.sample(range(60, 100), 2)
    sig = "<" if a < c else ">"
    b(co(b.id(), 5, f"{a} ___ {c}", sig, [s for s in ["<", ">", "=", "+"] if s != sig], "Compara decenas y luego unidades.", f"{a} es {'menor' if a < c else 'mayor'} que {c}.", r))
    return b.items


def _sin_reserva_suma(r, da, db):
    """Dos números de da y db cifras cuya suma no lleva reserva."""
    while True:
        a = r.randint(10 ** (da - 1), 10 ** da - 1); c = r.randint(10 ** (db - 1) if db > 1 else 1, 10 ** db - 1)
        if all(int(x) + int(y) < 10 for x, y in zip(str(a)[::-1], str(c)[::-1])) and a + c < 100:
            return a, c


def _sin_reserva_resta(r, da, db):
    while True:
        a = r.randint(10 ** (da - 1), 10 ** da - 1); c = r.randint(10 ** (db - 1) if db > 1 else 1, 10 ** db - 1)
        if c < a and all(int(x) >= int(y) for x, y in zip(str(a)[::-1], str(c)[::-1])):
            return a, c


def ma02_oa9():
    b = Banco(2, 9, 209); r = b.r
    a, c = 10 * r.randint(1, 6), 10 * r.randint(1, 3)
    b(nu(b.id(), 1, f"¿Cuánto es {a} + {c}?", a + c, "Suma las decenas.", f"{a // 10} decenas + {c // 10} decenas = {(a + c) // 10} decenas."))
    a, c = 10 * r.randint(5, 9), 10 * r.randint(1, 4)
    b(nu(b.id(), 1, f"¿Cuánto es {a} − {c}?", a - c, "Resta las decenas.", f"{a} − {c} = {a - c}."))
    b(om(b.id(), 1, "¿Cuánto es 50 + 30?", 80, [53, 70, 90], "5 decenas más 3 decenas.", "50 + 30 = 80.", r))
    b(em(b.id(), 1, "Une cada operación con su resultado.", [["20 + 40", "60"], ["90 − 40", "50"], ["30 + 40", "70"]], "Trabaja con las decenas.", "20 + 40 = 60, 90 − 40 = 50 y 30 + 40 = 70."))
    for nivel, da, db in [(2, 2, 1), (3, 2, 2)]:
        a, c = _sin_reserva_suma(r, da, db)
        b(nu(b.id(), nivel, f"¿Cuánto es {a} + {c}?", a + c, "Suma unidades con unidades y decenas con decenas.", f"{a} + {c} = {a + c}."))
        a, c = _sin_reserva_resta(r, da, db)
        b(nu(b.id(), nivel, f"¿Cuánto es {a} − {c}?", a - c, "Resta unidades con unidades y decenas con decenas.", f"{a} − {c} = {a - c}."))
        a, c = _sin_reserva_suma(r, da, db)
        b(co(b.id(), nivel, f"{a} + {c} = ___", a + c, dn(a + c, [a + c + 10, a + c - 1, a + c + 1]), "Suma por columnas.", f"{a} + {c} = {a + c}.", r))
        a, c = _sin_reserva_resta(r, da, db)
        b(om(b.id(), nivel, f"¿Cuánto es {a} − {c}?", a - c, dn(a - c, [a - c + 10, a - c - 10, a + c]), "Resta por columnas.", f"{a} − {c} = {a - c}.", r))
    a, c = _sin_reserva_suma(r, 2, 2)
    b(nu(b.id(), 4, f"{{personaje}} {{junto}} {a} {{objetos}} en la mañana y {c} en la tarde. ¿Cuántos {{objetos}} juntó en total?", a + c, "En total significa sumar.", f"{a} + {c} = {a + c}."))
    a, c = _sin_reserva_resta(r, 2, 2)
    b(nu(b.id(), 4, f"En {{el_contenedor}} había {a} {{objetos}}. {{personaje}} sacó {c}. ¿Cuántos quedan?", a - c, "Sacar es restar.", f"{a} − {c} = {a - c}."))
    pares = []
    while len(pares) < 4:
        a, c = _sin_reserva_suma(r, 2, 2)
        if all(str(a + c) != p[1] for p in pares):
            pares.append([f"{a} + {c}", str(a + c)])
    b(em(b.id(), 4, "Une cada suma con su resultado.", pares, "Resuelve cada suma por columnas.", "; ".join(f"{p[0]} = {p[1]}" for p in pares) + "."))
    els = []
    while len(els) < 6:
        a, c = _sin_reserva_suma(r, 2, 2) if len(els) % 2 else _sin_reserva_resta(r, 2, 2)
        txt = f"{a} + {c}" if len(els) % 2 else f"{a} − {c}"
        res = a + c if len(els) % 2 else a - c
        if res != 50 and txt not in [e[0] for e in els]:
            els.append((txt, 1 if res > 50 else 0))
    if len({e[1] for e in els}) < 2:
        els[-1] = ("80 − 10", 1); els[-2] = ("20 + 10", 0)
    b(cat(b.id(), 4, "¿El resultado es mayor que 50?", ["50 o menos", "Mayor que 50"], els, "Calcula cada operación.", "Calcula cada resultado y compáralo con 50."))
    a, t = _sin_reserva_suma(r, 2, 2)
    b(co(b.id(), 5, f"{a} + ___ = {a + t}", t, dn(t, [a + t, t + 10, t - 10]), f"¿Cuánto le falta a {a} para llegar a {a + t}?", f"{a} + {t} = {a + t}.", r))
    a, c = _sin_reserva_resta(r, 2, 2)
    b(nu(b.id(), 5, f"¿Qué número menos {c} da {a - c}?", a, "Piensa al revés: suma.", f"{a - c} + {c} = {a}."))
    a, c = _sin_reserva_suma(r, 2, 2)
    b(om(b.id(), 5, f"Si {a} + {c} = {a + c}, entonces {a + c} − {c} = ?", a, dn(a, [c, a + c, a + 10]), "La resta deshace la suma.", f"{a + c} − {c} = {a}.", r))
    b(nu(b.id(), 5, "{personaje} tenía 20 {objetos}, ganó 35 y después usó 14. ¿Cuántos tiene ahora?", 41, "Primero suma lo que ganó y después resta lo que usó.", "20 + 35 = 55 y 55 − 14 = 41."))
    return b.items


def ma02_oa11():
    b = Banco(2, 11, 211); r = b.r
    b(om(b.id(), 1, "2 + 2 + 2 + 2 es lo mismo que…", "4 × 2", ["2 × 2", "4 + 2", "8 × 2"], "Cuenta cuántas veces se suma el 2.", "Se suma 4 veces el 2: 4 × 2.", r))
    b(om(b.id(), 1, "5 + 5 + 5 es lo mismo que…", "3 × 5", ["5 × 5", "3 + 5", "15 × 3"], "Cuenta cuántas veces se suma el 5.", "Se suma 3 veces el 5: 3 × 5.", r))
    b(nu(b.id(), 1, "{personaje} hace 3 montones de 2 {objetos}. ¿Cuántos {objetos} hay?", 6, "Suma 2 + 2 + 2.", "3 veces 2 es 6."))
    b(nu(b.id(), 1, "¿Cuánto es 10 + 10 + 10 + 10?", 40, "Son 4 veces 10.", "4 × 10 = 40."))
    for nivel, tablas in [(2, [2, 10]), (3, [5])]:
        for t in (tablas * 2)[:2]:
            k = r.randint(3, 10)
            b(nu(b.id(), nivel, f"¿Cuánto es {k} × {t}?", k * t, f"Cuenta de {t} en {t}, {k} veces.", f"{k} × {t} = {k * t}."))
        t = tablas[0]; k = r.randint(4, 9)
        b(co(b.id(), nivel, f"{k} × {t} = ___", k * t, dn(k * t, [k * t + t, k * t - t, k + t]), f"Cuenta de {t} en {t}.", f"{k} × {t} = {k * t}.", r))
        ks = r.sample(range(2, 11), 3)
        b(em(b.id(), nivel, f"Une cada multiplicación con su resultado.", [[f"{k} × {tablas[-1]}", str(k * tablas[-1])] for k in ks],
             f"Usa la tabla del {tablas[-1]}.", ", ".join(f"{k} × {tablas[-1]} = {k * tablas[-1]}" for k in ks) + "."))
    b(nu(b.id(), 4, "{personaje} arma 4 grupos de 5 {objetos}. ¿Cuántos {objetos} hay?", 20, "Son 4 veces 5.", "4 × 5 = 20."))
    b(nu(b.id(), 4, "Hay 6 montones de 2 {objetos}. ¿Cuántos {objetos} hay en total?", 12, "Son 6 veces 2.", "6 × 2 = 12."))
    b(nu(b.id(), 4, "¿Cuántas patas tienen 7 gallinas?", 14, "Cada gallina tiene 2 patas.", "7 × 2 = 14."))
    b(cat(b.id(), 4, "¿Está en la tabla del 5?", ["Sí está", "No está"], [(15, 0), (35, 0), (50, 0), (25, 0), (12, 1), (18, 1), (33, 1), (44, 1)],
          "Los resultados de la tabla del 5 terminan en 0 o en 5.", "15, 25, 35 y 50 están en la tabla del 5."))
    for t, k in [(5, 7), (10, 8), (2, 8)]:
        b(co(b.id(), 5, f"{t} × ___ = {t * k}", k, dn(k, [k + 1, k - 1, t * k - t]), f"Cuenta de {t} en {t} hasta llegar a {t * k}.", f"{t} × {k} = {t * k}.", r))
    b(om(b.id(), 5, "¿Qué multiplicación da 30?", "3 × 10", ["3 × 5", "2 × 10", "5 × 5"], "Calcula cada una.", "3 × 10 = 30.", r))
    return b.items


GENERADORES = {
    "1_basico.matematica.OA1": ma01_oa1, "1_basico.matematica.OA4": ma01_oa4, "1_basico.matematica.OA9": ma01_oa9,
    "2_basico.matematica.OA1": ma02_oa1, "2_basico.matematica.OA3": ma02_oa3, "2_basico.matematica.OA9": ma02_oa9,
    "2_basico.matematica.OA11": ma02_oa11,
}
