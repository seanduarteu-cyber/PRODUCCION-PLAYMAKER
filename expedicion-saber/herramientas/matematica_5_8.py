"""Matemática 5° a 8° básico: 20 desafíos por OA (4 por nivel de dificultad, 1 a 5)."""
from comun import (opcion_multiple as om, completar as co, ordenar as orden, emparejar as em,
                   categoria as cat, numerica as nu, distractores_numericos as dn)
from matematica_1_2 import Banco
from matematica_3_4 import miles

M = miles


def ma05_oa3():
    b = Banco(5, 3, 503)
    b(nu(b.id(), 1, "¿Cuánto es 23 × 10?", 230, "Multiplicar por 10 agrega un cero.", "23 × 10 = 230."))
    b(nu(b.id(), 1, "¿Cuánto es 40 × 30?", 1200, "4 × 3 = 12 y luego agrega los dos ceros.", "40 × 30 = 1.200."))
    b(om(b.id(), 1, "¿Cuánto es 20 × 15?", 300, [35, 200, 3000], "Calcula 2 × 15 y agrega un cero.", "20 × 15 = 300."))
    b(nu(b.id(), 1, "¿Cuánto es 12 × 11?", 132, "12 × 10 + 12.", "12 × 11 = 120 + 12 = 132."))
    for a, c in [(14, 12), (21, 13)]:
        b(nu(b.id(), 2, f"¿Cuánto es {a} × {c}?", a * c, f"Descompón {c} en 10 + {c - 10}.", f"{a} × {c} = {a * 10} + {a * (c - 10)} = {a * c}."))
    b(co(b.id(), 2, "16 × 15 = ___", 240, [225, 160, 256], "16 × 10 + 16 × 5.", "160 + 80 = 240."))
    b(om(b.id(), 2, "¿Cuánto es 25 × 12?", 300, [250, 312, 275], "25 × 4 = 100.", "25 × 12 = 25 × 4 × 3 = 300."))
    for a, c in [(47, 36), (58, 24)]:
        b(nu(b.id(), 3, f"¿Cuánto es {a} × {c}?", a * c, "Multiplica por las unidades y por las decenas, y suma.", f"{a} × {c} = {M(a * c)}."))
    b(om(b.id(), 3, "¿Cuánto es 63 × 45?", 2835, [2735, 2825, 3150], "63 × 40 + 63 × 5.", "2.520 + 315 = 2.835."))
    b(co(b.id(), 3, "39 × 27 = ___", 1053, [1043, 1153, 954], "39 × 20 + 39 × 7.", "780 + 273 = 1.053."))
    b(nu(b.id(), 4, "Estima 48 × 32 redondeando a la decena. Basta con una buena estimación.", 1500, "48 ≈ 50 y 32 ≈ 30.", "50 × 30 = 1.500 (exacto: 1.536).", tolerancia=100))
    b(om(b.id(), 4, "¿Qué cálculo da una buena estimación de 29 × 41?", "30 × 40", ["20 × 40", "30 × 50", "29 + 41"], "Redondea cada factor a la decena más cercana.", "29 ≈ 30 y 41 ≈ 40."))
    b(co(b.id(), 4, "23 × 15 = 23 × 10 + 23 × ___", 5, [15, 3, 1], "15 = 10 + 5.", "23 × 15 = 230 + 115 = 345."))
    b(em(b.id(), 4, "Une cada multiplicación con su resultado.", [["15 × 15", "225"], ["24 × 25", "600"], ["32 × 21", "672"]], "Usa descomposiciones.", "15 × 15 = 225, 24 × 25 = 600 y 32 × 21 = 672."))
    b(nu(b.id(), 5, "{personaje} arma 24 filas de 16 {objetos}. ¿Cuántos {objetos} hay?", 384, "24 × 16.", "24 × 16 = 384."))
    b(nu(b.id(), 5, "Un curso de 36 estudiantes aporta $45 cada uno. ¿Cuánto juntan?", 1620, "36 × 45.", "36 × 45 = $1.620."))
    b(om(b.id(), 5, "Cada {contenedor} trae 48 {objetos}. ¿Cuántos hay en 25 {contenedores}?", 1200, [1000, 1240, 960], "48 × 25 = 48 × 100 ÷ 4.", "48 × 25 = 1.200."))
    b(cat(b.id(), 5, "¿El producto es mayor que 1.000?", ["1.000 o menos", "Mayor que 1.000"], [("31 × 32", 0), ("25 × 40", 0), ("19 × 52", 0), ("33 × 31", 1), ("26 × 40", 1), ("41 × 25", 1)],
          "Estima y luego calcula.", "31 × 32 = 992, 25 × 40 = 1.000, 19 × 52 = 988; 33 × 31 = 1.023, 26 × 40 = 1.040, 41 × 25 = 1.025."))
    return b.items


def ma05_oa4():
    b = Banco(5, 4, 504)
    b(nu(b.id(), 1, "¿Cuánto es 360 ÷ 6?", 60, "36 ÷ 6 = 6.", "360 ÷ 6 = 60."))
    b(nu(b.id(), 1, "¿Cuánto es 248 ÷ 2?", 124, "Divide cada cifra por 2.", "248 ÷ 2 = 124."))
    b(om(b.id(), 1, "¿Cuánto es 155 ÷ 5?", 31, [30, 35, 26], "150 ÷ 5 + 5 ÷ 5.", "30 + 1 = 31."))
    b(co(b.id(), 1, "426 ÷ 3 = ___", 142, [141, 124, 152], "Divide 4, 2 y 6 por 3 con cuidado.", "426 ÷ 3 = 142."))
    b(nu(b.id(), 2, "¿Cuánto es 432 ÷ 8?", 54, "8 × 50 = 400.", "432 = 400 + 32: 50 + 4 = 54."))
    b(nu(b.id(), 2, "¿Cuánto es 315 ÷ 7?", 45, "7 × 40 = 280.", "315 = 280 + 35: 40 + 5 = 45."))
    b(om(b.id(), 2, "¿Cuánto es 744 ÷ 6?", 124, [114, 134, 127], "6 × 100 = 600.", "744 = 600 + 144: 100 + 24 = 124."))
    b(co(b.id(), 2, "567 ÷ 9 = ___", 63, [62, 73, 57], "9 × 60 = 540.", "567 = 540 + 27: 60 + 3 = 63."))
    b(om(b.id(), 3, "¿Cuánto es 347 ÷ 5?", "cociente 69, resto 2", ["cociente 69, resto 0", "cociente 68, resto 7", "cociente 70, resto 3"], "5 × 69 = 345.", "347 = 5 × 69 + 2."))
    b(nu(b.id(), 3, "¿Cuál es el resto de 250 ÷ 7?", 5, "7 × 35 = 245.", "250 = 7 × 35 + 5: el resto es 5."))
    b(nu(b.id(), 3, "¿Cuál es el cociente de 500 ÷ 6?", 83, "6 × 80 = 480.", "500 = 6 × 83 + 2: el cociente es 83."))
    b(om(b.id(), 3, "¿Cuánto es 613 ÷ 4?", "cociente 153, resto 1", ["cociente 153, resto 0", "cociente 152, resto 5", "cociente 154, resto 1"], "4 × 150 = 600.", "613 = 4 × 153 + 1."))
    b(nu(b.id(), 4, "{personaje} reparte 365 {objetos} en 5 {contenedores} iguales. ¿Cuántos van en cada uno?", 73, "365 ÷ 5.", "365 ÷ 5 = 73."))
    b(nu(b.id(), 4, "Se arman grupos de 8 con 456 {objetos}. ¿Cuántos grupos se forman?", 57, "456 ÷ 8.", "456 ÷ 8 = 57."))
    b(om(b.id(), 4, "El cociente de 598 ÷ 3 está más cerca de…", 200, [100, 300, 150], "3 × 200 = 600.", "598 ÷ 3 ≈ 199."))
    b(em(b.id(), 4, "Une cada división con su cociente.", [["848 ÷ 4", "212"], ["936 ÷ 9", "104"], ["725 ÷ 5", "145"]], "Descompón el dividendo.", "848 ÷ 4 = 212, 936 ÷ 9 = 104 y 725 ÷ 5 = 145."))
    b(nu(b.id(), 5, "{personaje} guarda 250 {objetos} en {contenedores} donde caben 8. ¿Cuántos {contenedores} necesita para guardarlos todos?", 32,
         "250 ÷ 8 = 31 y sobran 2.", "31 se llenan y 1 más guarda los 2 que sobran: 32."))
    b(nu(b.id(), 5, "Con 250 {objetos} en {contenedores} de 8, ¿cuántos {contenedores} quedan completos?", 31, "8 × 31 = 248.", "250 = 8 × 31 + 2: 31 completos."))
    b(nu(b.id(), 5, "Un bus lleva 9 personas por fila. ¿Cuántas filas completas llena un grupo de 130?", 14, "9 × 14 = 126.", "130 = 9 × 14 + 4: 14 filas completas."))
    b(cat(b.id(), 5, "¿La división es exacta?", ["Exacta", "Con resto"], [("378 ÷ 6", 0), ("945 ÷ 9", 0), ("512 ÷ 8", 0), ("500 ÷ 3", 1), ("731 ÷ 4", 1), ("259 ÷ 5", 1)],
          "Es exacta si el resto es 0.", "378 ÷ 6 = 63, 945 ÷ 9 = 105 y 512 ÷ 8 = 64; las demás tienen resto."))
    return b.items


def ma05_oa7():
    b = Banco(5, 7, 507)
    b(om(b.id(), 1, "Si amplificas 2/3 por 4, ¿qué fracción obtienes?", "8/12", ["6/7", "2/12", "8/3"], "Multiplica numerador y denominador por 4.", "2 × 4 = 8 y 3 × 4 = 12."))
    b(om(b.id(), 1, "¿Qué fracción es equivalente a 3/5?", "6/10", ["3/10", "5/3", "6/5"], "Amplifica por 2.", "3/5 = 6/10."))
    b(co(b.id(), 1, "1/4 = ___/12", 3, [4, 2, 6], "¿Por cuánto se multiplicó el denominador?", "4 × 3 = 12, entonces 1 × 3 = 3."))
    b(em(b.id(), 1, "Une cada fracción con su amplificada por 2.", [["1/3", "2/6"], ["3/4", "6/8"], ["2/5", "4/10"]], "Multiplica arriba y abajo por 2.", "1/3 = 2/6, 3/4 = 6/8 y 2/5 = 4/10."))
    for f, s, ds in [("6/8", "3/4", ["2/4", "6/4", "3/8"]), ("10/15", "2/3", ["1/3", "5/3", "10/5"]), ("12/16", "3/4", ["6/16", "4/3", "2/4"])]:
        b(om(b.id(), 2, f"Simplifica {f} lo más posible.", s, ds, "Divide arriba y abajo por el mismo número.", f"{f} = {s}."))
    b(co(b.id(), 2, "9/12 = 3/___", 4, [3, 6, 9], "Divide por 3.", "9/12 = 3/4."))
    b(om(b.id(), 3, "¿Cuál es mayor?", "5/9", ["4/9", "Son iguales", "No se puede saber"], "Mismo denominador: compara numeradores.", "5/9 > 4/9."))
    b(om(b.id(), 3, "¿Cuál es mayor?", "3/5", ["3/8", "Son iguales", "No se puede saber"], "Mismo numerador: menos partes = partes más grandes.", "3/5 > 3/8."))
    b(co(b.id(), 3, "7/10 ___ 9/10", "<", [">", "=", "+"], "Compara numeradores.", "7/10 < 9/10."))
    b(orden(b.id(), 3, "Ordena de menor a mayor.", ["2/7", "3/7", "5/7", "6/7"], "Mismo denominador.", "2/7 < 3/7 < 5/7 < 6/7."))
    b(om(b.id(), 4, "¿Cuál es mayor, 2/3 o 3/4?", "3/4", ["2/3", "Son iguales", "No se puede saber"], "Iguala denominadores: 8/12 y 9/12.", "2/3 = 8/12 y 3/4 = 9/12: gana 3/4."))
    b(om(b.id(), 4, "¿Cuál es mayor, 3/5 o 4/7?", "3/5", ["4/7", "Son iguales", "No se puede saber"], "Denominador común 35.", "3/5 = 21/35 y 4/7 = 20/35."))
    b(co(b.id(), 4, "5/6 ___ 7/9", ">", ["<", "=", "+"], "Denominador común 18.", "5/6 = 15/18 y 7/9 = 14/18."))
    b(orden(b.id(), 4, "Ordena de menor a mayor.", ["1/2", "2/3", "3/4"], "Usa denominador 12.", "6/12 < 8/12 < 9/12."))
    b(om(b.id(), 5, "{personaje} usó 3/8 de {los_objetos} y Lía usó 1/4. ¿Quién usó más?", "{personaje}", ["Lía", "Usaron lo mismo", "No se puede saber"], "1/4 = 2/8.", "3/8 > 2/8."))
    b(cat(b.id(), 5, "¿Es mayor o menor que 1/2?", ["Menor que 1/2", "Mayor que 1/2"], [("2/5", 0), ("3/8", 0), ("4/9", 0), ("4/7", 1), ("5/8", 1), ("7/12", 1)],
          "Compara el numerador con la mitad del denominador.", "2/5, 3/8 y 4/9 son menores que 1/2; 4/7, 5/8 y 7/12, mayores."))
    b(em(b.id(), 5, "Une cada fracción con su forma más simple.", [["8/12", "2/3"], ["15/20", "3/4"], ["10/25", "2/5"], ["9/27", "1/3"]],
         "Divide por el máximo factor común.", "8/12 = 2/3, 15/20 = 3/4, 10/25 = 2/5 y 9/27 = 1/3."))
    b(om(b.id(), 5, "Una pizza se dividió en 12 partes y quedan 8. ¿Qué fracción queda, simplificada?", "2/3", ["8/12", "4/3", "3/4"], "Simplifica 8/12.", "8/12 = 2/3."))
    return b.items


def ma06_oa1():
    b = Banco(6, 1, 601)
    b(om(b.id(), 1, "¿Cuál de estos números es múltiplo de 6?", 42, [32, 45, 26], "Un múltiplo de 6 se obtiene al multiplicar 6 por un natural.", "6 × 7 = 42."))
    b(om(b.id(), 1, "¿Cuál de estos números es factor de 24?", 8, [5, 7, 9], "Un factor divide a 24 sin resto.", "24 ÷ 8 = 3."))
    b(nu(b.id(), 1, "¿Cuál es el quinto múltiplo de 7 (7, 14, …)?", 35, "Cuenta de 7 en 7.", "7 × 5 = 35."))
    b(co(b.id(), 1, "Los primeros múltiplos de 4 son 4, 8, 12, ___", 16, [14, 18, 20], "Suma 4.", "12 + 4 = 16."))
    b(nu(b.id(), 2, "¿Cuántos factores tiene el número 12?", 6, "Busca pares que multiplicados den 12.", "1, 2, 3, 4, 6 y 12: 6 factores."))
    b(orden(b.id(), 2, "Ordena de menor a mayor los factores de 18.", ["1", "2", "3", "6", "9", "18"], "Busca los pares: 1 × 18, 2 × 9, 3 × 6.", "1, 2, 3, 6, 9 y 18."))
    b(om(b.id(), 2, "¿Qué número NO es factor de 30?", 4, [5, 6, 10], "Divide 30 por cada uno.", "30 ÷ 4 no es exacto."))
    b(nu(b.id(), 2, "¿Cuál es el mayor factor de 45 que es menor que 45?", 15, "45 = 3 × 15.", "Los factores de 45 son 1, 3, 5, 9, 15 y 45."))
    b(cat(b.id(), 3, "¿Primo o compuesto?", ["Primo", "Compuesto"], [(13, 0), (29, 0), (41, 0), (21, 1), (27, 1), (51, 1)],
          "Un primo solo tiene dos factores: 1 y él mismo.", "13, 29 y 41 son primos; 21 = 3 × 7, 27 = 3 × 9 y 51 = 3 × 17."))
    b(om(b.id(), 3, "¿Cuál de estos números es primo?", 37, [39, 49, 57], "Prueba dividir por 2, 3, 5 y 7.", "37 solo es divisible por 1 y por 37."))
    b(nu(b.id(), 3, "¿Cuál es el menor número primo mayor que 20?", 23, "21 y 22 no son primos.", "21 = 3 × 7, 22 = 2 × 11 y 23 es primo."))
    b(om(b.id(), 3, "¿Por qué el 1 no es primo?", "porque tiene un solo factor", ["porque es impar", "porque es muy pequeño", "porque es par"], "Un primo tiene exactamente dos factores.", "El 1 solo tiene un factor: él mismo."))
    b(nu(b.id(), 4, "Un bus pasa cada 6 minutos y otro cada 8. Si salen juntos, ¿en cuántos minutos vuelven a coincidir?", 24, "Busca el menor múltiplo común.", "Múltiplos de 6: 6, 12, 18, 24. De 8: 8, 16, 24."))
    b(nu(b.id(), 4, "¿Cuál es el mayor factor común de 18 y 24?", 6, "Lista los factores de cada uno.", "18: 1, 2, 3, 6, 9, 18. 24: 1, 2, 3, 4, 6, 8, 12, 24."))
    b(om(b.id(), 4, "¿Cuál es el menor múltiplo común de 4 y 10?", 20, [40, 14, 10], "Múltiplos de 10: 10, 20…", "20 es múltiplo de 4 y de 10."))
    b(em(b.id(), 4, "Une cada número con su descomposición.", [["12", "2 × 2 × 3"], ["18", "2 × 3 × 3"], ["20", "2 × 2 × 5"]], "Divide por primos.", "12 = 2 × 2 × 3, 18 = 2 × 3 × 3 y 20 = 2 × 2 × 5."))
    b(nu(b.id(), 5, "{personaje} tiene 36 {objetos} rojos y 48 azules. Quiere armar grupos iguales con ambos colores, sin que sobre ninguno. ¿Cuántos grupos puede armar como máximo?", 12,
         "Busca el mayor factor común de 36 y 48.", "12 divide a 36 y a 48: 12 grupos."))
    b(nu(b.id(), 5, "Una luz parpadea cada 9 segundos y otra cada 12. ¿Cada cuántos segundos parpadean juntas?", 36, "Menor múltiplo común de 9 y 12.", "9, 18, 27, 36 y 12, 24, 36."))
    b(cat(b.id(), 5, "¿Es múltiplo de 3 y de 4 a la vez?", ["Múltiplo de 3 y de 4", "No"], [(12, 0), (36, 0), (60, 0), (18, 1), (20, 1), (30, 1)],
          "Debe dividirse por 3 y por 4 sin resto.", "12, 36 y 60 son múltiplos de 12."))
    b(om(b.id(), 5, "¿Cuántos números primos hay entre 30 y 40?", 2, [1, 3, 4], "Revisa 31, 33, 35, 37 y 39.", "Solo 31 y 37 son primos."))
    return b.items


def ma06_oa4():
    b = Banco(6, 4, 604)
    b(om(b.id(), 1, "¿Qué porcentaje de la barra está pintado? 🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜", "50%", ["5%", "10%", "25%"], "Son 10 partes iguales; cada una es 10%.", "5 de 10 partes = 50%."))
    b(om(b.id(), 1, "25 de cada 100 es…", "25%", ["2,5%", "75%", "4%"], "Por ciento significa «de cada 100».", "25 de 100 = 25%."))
    b(em(b.id(), 1, "Une cada porcentaje con su fracción.", [["50%", "1/2"], ["25%", "1/4"], ["10%", "1/10"], ["75%", "3/4"]], "Piensa en partes de 100.", "50% = 1/2, 25% = 1/4, 10% = 1/10 y 75% = 3/4."))
    b(om(b.id(), 1, "¿Qué porcentaje de la barra está pintado? 🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜", "20%", ["2%", "80%", "12%"], "Cada parte es 10%.", "2 de 10 = 20%."))
    b(nu(b.id(), 2, "¿Cuánto es el 30% de 100?", 30, "30 de cada 100.", "30% de 100 = 30."))
    b(nu(b.id(), 2, "¿Cuánto es el 50% de 80?", 40, "50% es la mitad.", "80 ÷ 2 = 40."))
    b(nu(b.id(), 2, "¿Cuánto es el 10% de 70?", 7, "10% es dividir por 10.", "70 ÷ 10 = 7."))
    b(om(b.id(), 2, "¿Cuánto es el 100% de 45?", 45, [100, 4.5, 145], "100% es el total.", "100% de 45 = 45."))
    b(nu(b.id(), 3, "¿Cuánto es el 25% de 60?", 15, "25% es dividir por 4.", "60 ÷ 4 = 15."))
    b(nu(b.id(), 3, "¿Cuánto es el 20% de 45?", 9, "20% es dividir por 5.", "45 ÷ 5 = 9."))
    b(nu(b.id(), 3, "¿Cuánto es el 75% de 40?", 30, "75% = 3 veces el 25%.", "25% de 40 = 10; 75% = 30."))
    b(om(b.id(), 3, "¿Cuánto es el 5% de 200?", 10, [5, 20, 40], "5% es la mitad del 10%.", "10% de 200 = 20; 5% = 10."))
    b(om(b.id(), 4, "0,4 expresado como porcentaje es…", "40%", ["4%", "0,4%", "400%"], "Multiplica por 100.", "0,4 × 100 = 40%."))
    b(cat(b.id(), 4, "¿Es más o menos de la mitad?", ["Menos de 50%", "Más de 50%"], [("1/4", 0), ("0,3", 0), ("45%", 0), ("3/4", 1), ("0,6", 1), ("55%", 1)],
          "La mitad es 50% = 0,5 = 1/2.", "1/4 = 25%, 0,3 = 30% y 45% son menos; 3/4 = 75%, 0,6 = 60% y 55% son más."))
    b(orden(b.id(), 4, "Ordena de menor a mayor.", ["1/4", "30%", "0,5"], "Pasa todo a porcentaje.", "25% < 30% < 50%."))
    b(om(b.id(), 4, "¿Qué fracción equivale a 20%?", "1/5", ["1/2", "1/20", "2/5"], "20 de 100, simplificado.", "20/100 = 1/5."))
    b(nu(b.id(), 5, "Hay 200 {objetos} y el 15% son nuevos. ¿Cuántos son nuevos?", 30, "10% = 20 y 5% = 10.", "15% de 200 = 30."))
    b(nu(b.id(), 5, "{personaje} tiene 40 {objetos} y usa el 25%. ¿Cuántos usa?", 10, "25% es la cuarta parte.", "40 ÷ 4 = 10."))
    b(nu(b.id(), 5, "Un juego cuesta $8.000 y tiene 25% de descuento. ¿Cuántos pesos te descuentan?", 2000, "La cuarta parte de 8.000.", "25% de 8.000 = $2.000."))
    b(om(b.id(), 5, "En un curso, 18 de 30 estudiantes prefieren fútbol. ¿Qué porcentaje es?", "60%", ["18%", "30%", "50%"], "18/30 = 6/10.", "6/10 = 60%."))
    return b.items


def ma07_oa1():
    b = Banco(7, 1, 701)
    b(nu(b.id(), 1, "La temperatura era −3 °C y subió 5 °C. ¿Qué temperatura hay ahora?", 2, "Avanza 5 desde −3 en la recta numérica.", "−3 + 5 = 2.", unidad="°C"))
    b(nu(b.id(), 1, "¿Cuánto es (−4) + 6?", 2, "Imagina la recta numérica.", "−4 + 6 = 2."))
    b(om(b.id(), 1, "¿Qué número es mayor?", "−2", ["−5", "−9", "−7"], "En la recta, el mayor está más a la derecha.", "−2 está más cerca del 0."))
    b(co(b.id(), 1, "(−1) + 4 = ___", 3, [5, -3, -5], "Avanza 4 desde −1.", "−1 + 4 = 3."))
    b(nu(b.id(), 2, "¿Cuánto es (−7) + (−5)?", -12, "Dos negativos se acumulan.", "−7 + −5 = −12."))
    b(nu(b.id(), 2, "¿Cuánto es 3 − 8?", -5, "Te pasas del 0.", "3 − 8 = −5."))
    b(om(b.id(), 2, "¿Cuánto es (−9) + 4?", "−5", ["5", "−13", "13"], "Avanza 4 desde −9 en la recta numérica.", "−9 + 4 = −5."))
    b(co(b.id(), 2, "(−2) + (−6) = ___", "−8", ["8", "−4", "4"], "Suma las distancias y conserva el signo.", "−2 + −6 = −8."))
    b(nu(b.id(), 3, "¿Cuánto es (−6) − (−9)?", 3, "Restar un negativo es sumar su opuesto.", "−6 + 9 = 3."))
    b(nu(b.id(), 3, "¿Cuánto es 5 − (−4)?", 9, "Restar −4 es sumar 4.", "5 + 4 = 9."))
    b(om(b.id(), 3, "¿Cuánto es (−3) − 7?", "−10", ["10", "4", "−4"], "Restar 7 es retroceder 7.", "−3 − 7 = −10."))
    b(co(b.id(), 3, "(−8) − (−8) = ___", 0, [-16, 16, 8], "Un número menos sí mismo.", "−8 + 8 = 0."))
    b(orden(b.id(), 4, "Ordena de menor a mayor.", ["−5", "−2", "0", "3"], "Los negativos más lejanos del 0 son menores.", "−5 < −2 < 0 < 3."))
    b(cat(b.id(), 4, "¿El resultado es positivo o negativo?", ["Negativo", "Positivo"], [("4 − 9", 0), ("(−3) + (−2)", 0), ("(−10) + 6", 0), ("(−2) + 7", 1), ("5 − (−1)", 1), ("(−4) − (−6)", 1)],
          "Calcula cada operación.", "−5, −5 y −4 son negativos; 5, 6 y 2 son positivos."))
    b(nu(b.id(), 4, "Un buzo está a −12 m y sube 5 m. ¿A qué profundidad queda?", -7, "Subir es sumar.", "−12 + 5 = −7.", unidad="m"))
    b(nu(b.id(), 4, "En Punta Arenas hay −2 °C y en Arica 21 °C. ¿Cuántos grados de diferencia hay?", 23, "Resta: 21 − (−2).", "21 + 2 = 23.", unidad="°C"))
    b(nu(b.id(), 5, "Tienes $2.000 en una cuenta, gastas $3.500 y luego depositas $1.000. ¿Cuál es el saldo?", -500, "2.000 − 3.500 + 1.000.", "−1.500 + 1.000 = −500."))
    b(co(b.id(), 5, "(−4) + ___ = 3", 7, [-7, 1, -1], "¿Cuánto hay que avanzar desde −4 hasta 3?", "−4 + 7 = 3."))
    b(nu(b.id(), 5, "Un ascensor está en el piso −3, sube 8 pisos y baja 2. ¿En qué piso queda?", 3, "−3 + 8 − 2.", "−3 + 8 = 5 y 5 − 2 = 3."))
    b(om(b.id(), 5, "¿Qué operación da −6?", "(−10) + 4", ["10 − 4", "(−10) − (−4) − (−10)", "6 − (−6)"], "Calcula cada una.", "−10 + 4 = −6."))
    return b.items


def ma07_oa4():
    b = Banco(7, 4, 704)
    b(om(b.id(), 1, "Calcular el 25% de un número es lo mismo que dividirlo por…", 4, [25, 2, 5], "25% = 1/4.", "25% = 1/4: se divide por 4."))
    b(nu(b.id(), 1, "¿Cuánto es el 50% de 90?", 45, "La mitad.", "90 ÷ 2 = 45."))
    b(nu(b.id(), 1, "¿Cuánto es el 10% de 230?", 23, "Divide por 10.", "230 ÷ 10 = 23."))
    b(om(b.id(), 1, "Calcular el 20% es lo mismo que dividir por…", 5, [20, 2, 4], "20% = 1/5.", "20% = 1/5."))
    b(nu(b.id(), 2, "¿Cuánto es el 35% de 200?", 70, "10% = 20; 35% = 3,5 veces.", "35% de 200 = 70."))
    b(nu(b.id(), 2, "¿Cuánto es el 12% de 50?", 6, "1% de 50 = 0,5.", "12 × 0,5 = 6."))
    b(co(b.id(), 2, "El 40% de 150 es ___", 60, [40, 15, 90], "10% de 150 = 15.", "4 × 15 = 60."))
    b(om(b.id(), 2, "¿Cuánto es el 1% de 3.500?", 35, [350, 3.5, 135], "Divide por 100.", "3.500 ÷ 100 = 35."))
    b(nu(b.id(), 3, "¿Qué porcentaje es 18 de 60?", 30, "18/60 = 3/10.", "3/10 = 30%.", unidad="%"))
    b(nu(b.id(), 3, "¿Qué porcentaje es 15 de 75?", 20, "15/75 = 1/5.", "1/5 = 20%.", unidad="%"))
    b(om(b.id(), 3, "¿Qué porcentaje es 9 de 12?", "75%", ["9%", "12%", "25%"], "9/12 = 3/4.", "3/4 = 75%."))
    b(co(b.id(), 3, "7 de 20 es el ___", "35%", ["7%", "20%", "70%"], "Amplifica a denominador 100.", "7/20 = 35/100 = 35%."))
    b(nu(b.id(), 4, "Una polera de $12.000 tiene 20% de descuento. ¿Cuánto pagas?", 9600, "Descuento: 20% de 12.000 = 2.400.", "12.000 − 2.400 = $9.600."))
    b(nu(b.id(), 4, "Un pasaje de $5.000 sube un 10%. ¿Cuál es el nuevo precio?", 5500, "10% de 5.000 = 500.", "5.000 + 500 = $5.500."))
    b(om(b.id(), 4, "Un precio sube 50% y queda en $1.500. ¿Cuál era el precio original?", "$1.000", ["$750", "$1.450", "$3.000"], "1.500 es el 150% del original.", "1.500 ÷ 1,5 = 1.000."))
    b(em(b.id(), 4, "Une cada cálculo con su resultado.", [["15% de 80", "12"], ["60% de 45", "27"], ["5% de 300", "15"]], "Usa el 10% y el 5% como ayuda.", "15% de 80 = 12, 60% de 45 = 27 y 5% de 300 = 15."))
    b(nu(b.id(), 5, "En un curso de 40 estudiantes, el 35% prefiere básquetbol. ¿Cuántos son?", 14, "10% = 4.", "35% de 40 = 14."))
    b(nu(b.id(), 5, "Si el 30% de un grupo son 12 personas, ¿cuántas personas hay en total?", 40, "10% = 4.", "100% = 40."))
    b(om(b.id(), 5, "{personaje} tenía 80 {objetos} y regaló 20. ¿Qué porcentaje regaló?", "25%", ["20%", "60%", "75%"], "20/80 = 1/4.", "1/4 = 25%."))
    b(cat(b.id(), 5, "Hay dos ofertas. Lleva cada dato a la oferta que le corresponde.", ["$10.000 con 30% de descuento", "$9.000 con 20% de descuento"], [("Pagas $7.000", 0), ("Ahorras $3.000", 0), ("Pagas $7.200", 1), ("Ahorras $1.800", 1)],
          "Calcula el descuento de cada oferta.", "30% de 10.000 = 3.000 → pagas $7.000. 20% de 9.000 = 1.800 → pagas $7.200: conviene la primera."))
    return b.items


def ma08_oa1():
    b = Banco(8, 1, 801)
    b(om(b.id(), 1, "Un número negativo multiplicado por otro negativo da un resultado…", "positivo", ["negativo", "cero", "depende"], "Regla de los signos.", "(−) × (−) = (+)."))
    b(nu(b.id(), 1, "¿Cuánto es (−3) × 4?", -12, "Distintos signos: negativo.", "(−3) × 4 = −12."))
    b(om(b.id(), 1, "Un número positivo dividido por uno negativo da un resultado…", "negativo", ["positivo", "cero", "depende"], "Distintos signos: negativo.", "(+) ÷ (−) = (−)."))
    b(co(b.id(), 1, "(−2) × (−5) = ___", 10, [-10, 7, -7], "Mismo signo: positivo.", "(−2) × (−5) = 10."))
    b(nu(b.id(), 2, "¿Cuánto es (−6) × (−7)?", 42, "Mismo signo: positivo.", "(−6) × (−7) = 42."))
    b(nu(b.id(), 2, "¿Cuánto es (−48) ÷ 6?", -8, "Distintos signos.", "(−48) ÷ 6 = −8."))
    b(om(b.id(), 2, "¿Cuánto es 9 × (−3)?", "−27", ["27", "−12", "6"], "Distintos signos.", "9 × (−3) = −27."))
    b(co(b.id(), 2, "(−35) ÷ (−5) = ___", 7, [-7, 30, -30], "Mismo signo.", "(−35) ÷ (−5) = 7."))
    b(nu(b.id(), 3, "¿Cuánto es (−72) ÷ (−9)?", 8, "Mismo signo.", "(−72) ÷ (−9) = 8."))
    b(nu(b.id(), 3, "¿Cuánto es 5 × (−9)?", -45, "Distintos signos.", "5 × (−9) = −45."))
    b(om(b.id(), 3, "¿Cuánto es 64 ÷ (−8)?", "−8", ["8", "−56", "72"], "Distintos signos.", "64 ÷ (−8) = −8."))
    b(co(b.id(), 3, "(−11) × (−4) = ___", 44, [-44, 15, -15], "Mismo signo.", "(−11) × (−4) = 44."))
    b(nu(b.id(), 4, "¿Cuánto es (−2) × 3 × (−4)?", 24, "Cuenta los signos negativos: dos.", "(−2) × 3 = −6 y (−6) × (−4) = 24."))
    b(cat(b.id(), 4, "¿El resultado es positivo o negativo?", ["Negativo", "Positivo"], [("(−3) × 5", 0), ("(−2) × (−2) × (−2)", 0), ("40 ÷ (−8)", 0), ("(−6) × (−6)", 1), ("(−20) ÷ (−4)", 1), ("(−1) × (−1) × 5", 1)],
          "Un número par de signos negativos da positivo.", "−15, −8 y −5 son negativos; 36, 5 y 5 son positivos."))
    b(nu(b.id(), 4, "¿Cuánto es (−36) ÷ 4 × (−2)?", 18, "Resuelve de izquierda a derecha.", "(−36) ÷ 4 = −9 y (−9) × (−2) = 18."))
    b(em(b.id(), 4, "Une cada operación con su resultado.", [["(−4) × 6", "−24"], ["(−4) × (−6)", "24"], ["(−24) ÷ (−6)", "4"]], "Aplica la regla de los signos.", "−24, 24 y 4."))
    b(nu(b.id(), 5, "La temperatura baja 3 °C cada hora durante 5 horas. ¿Cuánto cambió en total?", -15, "Bajar es negativo: 5 × (−3).", "5 × (−3) = −15.", unidad="°C"))
    b(co(b.id(), 5, "(−36) ÷ ___ = 4", -9, [9, -4, 32], "¿Qué número por 4 da −36?", "(−36) ÷ (−9) = 4."))
    b(nu(b.id(), 5, "Un submarino desciende 25 m por minuto. ¿A qué profundidad estará tras 4 minutos, si partió en la superficie?", -100, "4 × (−25).", "4 × (−25) = −100.", unidad="m"))
    b(om(b.id(), 5, "Una deuda de $12.000 se reparte en partes iguales entre 4 personas. Como entero, ¿cuánto le toca a cada una?", "−3.000", ["3.000", "−48.000", "−4.000"], "(−12.000) ÷ 4.", "(−12.000) ÷ 4 = −3.000."))
    return b.items


def ma08_oa3():
    b = Banco(8, 3, 803)
    b(nu(b.id(), 1, "¿Cuánto es 2³?", 8, "2 × 2 × 2.", "2³ = 8."))
    b(nu(b.id(), 1, "¿Cuánto es 5²?", 25, "5 × 5.", "5² = 25."))
    b(om(b.id(), 1, "¿Cuánto es 10³?", "1.000", ["30", "100", "10.000"], "10 × 10 × 10.", "10³ = 1.000."))
    b(co(b.id(), 1, "4² = ___", 16, [8, 6, 64], "4 × 4.", "4² = 16."))
    b(co(b.id(), 2, "2² · 2³ = 2^___", 5, [6, 1, 8], "Al multiplicar potencias de igual base, se suman los exponentes.", "2² · 2³ = 2⁵."))
    b(nu(b.id(), 2, "¿Cuánto es 3² · 3?", 27, "3² · 3¹ = 3³.", "3³ = 27."))
    b(om(b.id(), 2, "a² · a³ es igual a…", "a⁵", ["a⁶", "2a⁵", "a¹"], "Igual base: suma los exponentes.", "a² · a³ = a⁵."))
    b(nu(b.id(), 2, "¿Cuánto es 2³ · 2²?", 32, "2⁵.", "2⁵ = 32."))
    b(nu(b.id(), 3, "¿Cuánto es 5³ : 5²?", 5, "Al dividir potencias de igual base, se restan los exponentes.", "5³ : 5² = 5¹ = 5."))
    b(co(b.id(), 3, "3³ : 3 = 3^___", 2, [3, 4, 1], "3³ : 3¹ = 3^(3−1).", "3³ : 3 = 3²."))
    b(om(b.id(), 3, "a³ : a² es igual a…", "a", ["a⁵", "a⁶", "1"], "Resta los exponentes.", "a³ : a² = a¹ = a."))
    b(nu(b.id(), 3, "¿Cuánto es 10³ : 10²?", 10, "10^(3−2).", "10¹ = 10."))
    b(co(b.id(), 4, "(2²)³ = 2^___", 6, [5, 8, 9], "En una potencia de potencia, se multiplican los exponentes.", "(2²)³ = 2⁶."))
    b(nu(b.id(), 4, "¿Cuánto es (3²)²?", 81, "3⁴.", "(3²)² = 3⁴ = 81."))
    b(om(b.id(), 4, "(a³)² es igual a…", "a⁶", ["a⁵", "a⁹", "2a³"], "Multiplica los exponentes.", "(a³)² = a⁶."))
    b(nu(b.id(), 4, "¿Cuánto es (2³)²?", 64, "2⁶.", "(2³)² = 2⁶ = 64."))
    b(cat(b.id(), 5, "¿Es igual a 2⁶?", ["Igual a 2⁶", "Distinto"], [("2³ · 2³", 0), ("(2²)³", 0), ("64", 0), ("2³ · 2²", 1), ("(2³)³", 1), ("12", 1)],
          "2⁶ = 64.", "2³ · 2³ = 2⁶, (2²)³ = 2⁶ y 64 = 2⁶."))
    b(em(b.id(), 5, "Une cada expresión con su valor.", [["3² · 3", "27"], ["4³ : 4", "16"], ["(5²)¹", "25"]], "Aplica las propiedades y calcula.", "3³ = 27, 4² = 16 y 5² = 25."))
    b(nu(b.id(), 5, "¿Cuál es el volumen, en cm³, de un cubo de 4 cm de arista? (4³)", 64, "4 × 4 × 4.", "4³ = 64.", unidad="cm³"))
    b(om(b.id(), 5, "Una bacteria se duplica cada hora. Partiendo de 1, ¿cuántas hay después de 3 horas, como potencia?", "2³", ["3²", "2 · 3", "3³"], "1 → 2 → 4 → 8.", "8 = 2³."))
    return b.items


def ma08_oa7():
    b = Banco(8, 7, 807)
    b(nu(b.id(), 1, "Si y = 2x, ¿cuánto vale y cuando x = 4?", 8, "Reemplaza x por 4.", "y = 2 · 4 = 8."))
    b(nu(b.id(), 1, "Si f(x) = x + 3, ¿cuánto es f(5)?", 8, "Reemplaza x por 5.", "f(5) = 5 + 3 = 8."))
    b(om(b.id(), 1, "Una máquina recibe un número y le suma 4. Si entra 6, ¿qué sale?", 10, [24, 2, 64], "6 + 4.", "Sale 10."))
    b(co(b.id(), 1, "Si y = 5x y x = 3, entonces y = ___", 15, [8, 53, 2], "5 · 3.", "y = 15."))
    b(om(b.id(), 2, "¿Qué regla cumple la tabla? x: 1, 2, 3 → y: 3, 6, 9", "y = 3x", ["y = x + 2", "y = x + 3", "y = 2x + 1"], "Prueba con todos los pares.", "3 · 1 = 3, 3 · 2 = 6, 3 · 3 = 9."))
    b(om(b.id(), 2, "¿Qué regla cumple la tabla? x: 0, 1, 2 → y: 5, 6, 7", "y = x + 5", ["y = 5x", "y = 6x", "y = x + 6"], "Cuando x = 0, y = 5.", "Cada y es x + 5."))
    b(nu(b.id(), 2, "Si y = 4x − 1, ¿cuánto vale y cuando x = 3?", 11, "4 · 3 − 1.", "12 − 1 = 11."))
    b(co(b.id(), 2, "En y = 2x + 3, si x = 0 entonces y = ___", 3, [0, 5, 2], "2 · 0 + 3.", "y = 3."))
    b(nu(b.id(), 3, "Si f(x) = 2x + 1, ¿cuánto es f(−3)?", -5, "2 · (−3) + 1.", "−6 + 1 = −5."))
    b(nu(b.id(), 3, "En y = 2x + 1, ¿qué valor de x da y = 11?", 5, "2x = 10.", "x = 5."))
    b(om(b.id(), 3, "Si f(x) = 3x − 2, ¿cuánto es f(4)?", 10, [14, 12, 5], "3 · 4 − 2.", "12 − 2 = 10."))
    b(co(b.id(), 3, "Si y = x − 7 y x = 2, entonces y = ___", -5, [5, 9, -9], "2 − 7.", "y = −5."))
    b(om(b.id(), 4, "¿Qué punto pertenece a la recta y = x + 2?", "(1, 3)", ["(3, 1)", "(2, 2)", "(0, 1)"], "Reemplaza x y revisa si da la y.", "1 + 2 = 3."))
    b(om(b.id(), 4, "Un estanque tiene 10 litros y recibe 4 litros por hora. ¿Qué función da los litros y después de x horas?", "y = 4x + 10", ["y = 10x + 4", "y = 14x", "y = 4x"], "Parte en 10 y suma 4 cada hora.", "y = 4x + 10."))
    b(nu(b.id(), 4, "En y = 3x, ¿cuánto aumenta y cada vez que x aumenta en 1?", 3, "Compara y(1) con y(2).", "Aumenta 3."))
    b(em(b.id(), 4, "Une cada función con el valor de y cuando x = 2.", [["y = 3x", "6"], ["y = x + 5", "7"], ["y = 4x − 3", "5"]], "Reemplaza x = 2.", "6, 7 y 5."))
    b(nu(b.id(), 5, "Un taxi cobra $500 fijos más $300 por kilómetro. ¿Cuánto cuesta un viaje de 6 km?", 2300, "500 + 300 · 6.", "500 + 1.800 = $2.300."))
    b(nu(b.id(), 5, "Con la misma tarifa ($500 + $300 por km), un viaje costó $3.500. ¿Cuántos km fueron?", 10, "3.500 − 500 = 3.000.", "3.000 ÷ 300 = 10 km.", unidad="km"))
    b(cat(b.id(), 5, "¿La tabla es una relación lineal (cambio constante)?", ["Lineal", "No lineal"],
          [("x: 1, 2, 3 → y: 2, 4, 6", 0), ("x: 1, 2, 3 → y: 5, 8, 11", 0), ("x: 0, 1, 2 → y: 1, 1, 1", 0), ("x: 1, 2, 3 → y: 1, 4, 9", 1), ("x: 1, 2, 3 → y: 2, 4, 8", 1)],
          "Revisa si y cambia siempre lo mismo cuando x aumenta en 1.", "Las tres primeras cambian de forma constante; 1, 4, 9 y 2, 4, 8 no."))
    b(om(b.id(), 5, "{personaje} junta 7 {objetos} por día y ya tiene 20. ¿Cuántos tendrá en 5 días?", 55, [35, 27, 140], "y = 7x + 20 con x = 5.", "35 + 20 = 55."))
    return b.items


GENERADORES = {
    "5_basico.matematica.OA3": ma05_oa3, "5_basico.matematica.OA4": ma05_oa4, "5_basico.matematica.OA7": ma05_oa7,
    "6_basico.matematica.OA1": ma06_oa1, "6_basico.matematica.OA4": ma06_oa4, "7_basico.matematica.OA1": ma07_oa1,
    "7_basico.matematica.OA4": ma07_oa4, "8_basico.matematica.OA1": ma08_oa1, "8_basico.matematica.OA3": ma08_oa3,
    "8_basico.matematica.OA7": ma08_oa7,
}
