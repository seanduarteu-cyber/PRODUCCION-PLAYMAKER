"""Matemática 1° a 4° medio: 15 desafíos por OA (3 por nivel de dificultad, 1 a 5).
Las respuestas numéricas son enteras; fracciones, decimales, complejos y expresiones van como alternativas."""
from autor import Autor


# ---------------- 1° medio ----------------
def ma1m_oa1():
    b = Autor("mat", "1m", 1)
    b.om(1, "¿Cuánto es 1/2 + 1/4?", "3/4", ["2/6", "1/6", "2/4"], "Usa denominador común 4.", "1/2 = 2/4; 2/4 + 1/4 = 3/4.")
    b.om(1, "¿Cuánto es 0,5 · 4?", "2", ["0,2", "20", "4,5"], "La mitad de 4.", "0,5 · 4 = 2.")
    b.co(1, "2/3 · 3/4 = ___", "1/2", ["6/7", "5/7", "8/9"], "Multiplica numeradores y denominadores y simplifica.", "6/12 = 1/2.")
    b.om(2, "¿Cuánto es 3/5 − 1/10?", "1/2", ["2/5", "2/10", "1/5"], "Denominador común 10.", "6/10 − 1/10 = 5/10 = 1/2.")
    b.om(2, "¿Cuánto es (−2/3) · (9/4)?", "−3/2", ["3/2", "−6/7", "−2/3"], "Distintos signos: negativo. Simplifica.", "−18/12 = −3/2.")
    b.cat(2, "¿Resultado mayor o menor que 1?", ["Menor que 1", "Mayor que 1"], [("1/2 + 1/3", 0), ("0,4 · 2", 0), ("3/4 · 1/2", 0), ("1/2 + 3/4", 1), ("1,5 · 2", 1), ("5/4 ÷ 1/2", 1)],
          "Calcula o estima cada operación.", "5/6, 0,8 y 3/8 son menores que 1; 5/4, 3 y 5/2 son mayores.")
    b.om(3, "¿Cuánto es 3/4 ÷ 3/8?", "2", ["9/32", "1/2", "6/12"], "Dividir es multiplicar por el inverso.", "3/4 · 8/3 = 24/12 = 2.")
    b.nu(3, "Calcula 2 + 3 · (1/3).", 3, "Primero la multiplicación.", "3 · 1/3 = 1; 2 + 1 = 3.")
    b.om(3, "¿Cuánto es 1/2 + 1/2 · 1/2?", "3/4", ["1/2", "1", "1/8"], "Primero la multiplicación.", "1/2 · 1/2 = 1/4; 1/2 + 1/4 = 3/4.")
    b.nu(4, "Calcula (1/2 + 1/3) · 6.", 5, "Resuelve el paréntesis primero.", "1/2 + 1/3 = 5/6; 5/6 · 6 = 5.")
    b.ord(4, "Ordena de menor a mayor.", ["−3/4", "−0,5", "1/3", "0,4"], "Pasa todo a decimal.", "−0,75 < −0,5 < 0,33… < 0,4.")
    b.om(4, "¿Cuál es el valor de 0,2 + 1/5 · 2?", "0,6", ["0,8", "0,4", "1,2"], "1/5 = 0,2; primero multiplica.", "0,2 · 2 = 0,4; 0,2 + 0,4 = 0,6.")
    b.nu(5, "Una receta usa 3/4 de taza de harina por porción. ¿Cuántas tazas se necesitan para 8 porciones?", 6, "Multiplica 3/4 por 8.", "3/4 · 8 = 24/4 = 6 tazas.", unidad="tazas")
    b.om(5, "{personaje} gastó 1/3 de sus {objetos} el lunes y 1/4 del total el martes. ¿Qué fracción le queda?", "5/12", ["7/12", "1/12", "2/7"], "Suma lo gastado y réstalo de 1.", "1/3 + 1/4 = 7/12; 1 − 7/12 = 5/12.")
    b.nu(5, "Un estanque de 240 litros está lleno en sus 5/8. ¿Cuántos litros faltan para llenarlo?", 90, "Calcula los 3/8 que faltan.", "3/8 · 240 = 90 litros.", unidad="L")
    return b.items


def ma1m_oa4():
    b = Autor("mat", "1m", 4)
    b.om(1, "¿Qué par (x, y) es solución de x + y = 5 y x − y = 1?", "(3, 2)", ["(2, 3)", "(4, 1)", "(5, 0)"], "Reemplaza en ambas ecuaciones.", "3 + 2 = 5 y 3 − 2 = 1.")
    b.nu(1, "Si x + y = 10 e y = 4, ¿cuánto vale x?", 6, "Reemplaza y.", "x = 10 − 4 = 6.")
    b.co(1, "Un sistema 2x2 tiene ___ ecuaciones y dos incógnitas.", "dos", ["una", "tres", "cuatro"], "2x2: dos por dos.", "Tiene dos ecuaciones y dos incógnitas.")
    b.nu(2, "Resuelve: x + y = 12, x − y = 4. ¿Cuánto vale x?", 8, "Suma las ecuaciones: 2x = 16.", "2x = 16 → x = 8.")
    b.nu(2, "En el sistema y = 2x, x + y = 9, ¿cuánto vale x?", 3, "Sustituye y = 2x.", "x + 2x = 9 → x = 3.")
    b.em(2, "Une cada método con su idea.", [["sustitución", "despejar una incógnita y reemplazarla"], ["igualación", "despejar la misma incógnita en ambas e igualar"], ["reducción", "sumar o restar ecuaciones para eliminar una incógnita"]], "Recuerda los tres métodos.", "Sustitución, igualación y reducción.")
    b.nu(3, "Resuelve: 2x + y = 11, x − y = 1. ¿Cuánto vale y?", 3, "Suma: 3x = 12, x = 4.", "x = 4; y = 4 − 1 = 3.")
    b.om(3, "Gráficamente, la solución de un sistema 2x2 es…", "el punto donde se cortan las dos rectas", ["el origen siempre", "la pendiente de una recta", "el área entre las rectas"], "Cada ecuación es una recta.", "La solución es el punto de intersección.")
    b.ord(3, "Ordena los pasos del método de sustitución.", ["Despejar una incógnita en una ecuación.", "Reemplazarla en la otra ecuación.", "Resolver la ecuación con una incógnita.", "Calcular la otra incógnita."], "Despejar, reemplazar, resolver y completar.", "Así se aplica la sustitución.")
    b.cat(4, "¿Cuántas soluciones tiene el sistema?", ["Una solución", "Ninguna", "Infinitas"], [("x + y = 4 ; x − y = 2", 0), ("y = 2x ; y = x + 1", 0), ("x + y = 3 ; x + y = 5", 1), ("y = x + 1 ; y = x − 2", 1), ("x + y = 2 ; 2x + 2y = 4", 2), ("y = 3x ; 2y = 6x", 2)],
          "Rectas que se cortan, paralelas o iguales.", "Distinta pendiente: una solución; paralelas: ninguna; la misma recta: infinitas.")
    b.om(4, "Las rectas y = 2x + 1 e y = 2x − 3 son paralelas. El sistema…", "no tiene solución", ["tiene una solución", "tiene infinitas soluciones", "tiene dos soluciones"], "Misma pendiente, distinta posición.", "Las rectas paralelas no se cortan.")
    b.nu(4, "Entradas: adulto $3.000 y niño $2.000. Un grupo de 7 personas pagó $17.000. ¿Cuántos adultos había?", 3, "a + n = 7 ; 3.000a + 2.000n = 17.000.", "Si n = 7 − a: 3.000a + 14.000 − 2.000a = 17.000 → a = 3.")
    b.nu(5, "En un corral hay gallinas y conejos: 10 cabezas y 28 patas. ¿Cuántos conejos hay?", 4, "g + c = 10 ; 2g + 4c = 28.", "2(10 − c) + 4c = 28 → 2c = 8 → c = 4.", unidad="conejos")
    b.nu(5, "La suma de dos números es 50 y su diferencia es 14. ¿Cuál es el número mayor?", 32, "x + y = 50 ; x − y = 14.", "2x = 64 → x = 32.")
    b.om(5, "Un plan cobra $5.000 más $100 por minuto; otro, $8.000 más $50 por minuto. ¿Con cuántos minutos cuestan lo mismo?", "60", ["30", "50", "80"], "Iguala 5.000 + 100m = 8.000 + 50m.", "50m = 3.000 → m = 60 minutos.")
    return b.items


def ma1m_oa14():
    b = Autor("mat", "1m", 14)
    b.om(1, "Al lanzar un dado, ¿cuál es la probabilidad de obtener un 6?", "1/6", ["1/2", "6", "1/3"], "Casos favorables ÷ casos posibles.", "1 caso favorable de 6.")
    b.om(1, "Al lanzar una moneda dos veces, ¿cuántos resultados posibles hay?", "4", ["2", "3", "6"], "CC, CS, SC, SS.", "Hay 4 resultados posibles.")
    b.co(1, "La probabilidad de un suceso imposible es ___.", "0", ["1", "1/2", "−1"], "No puede ocurrir nunca.", "Un suceso imposible tiene probabilidad 0.")
    b.om(2, "Al lanzar un dado, ¿cuál es la probabilidad de obtener un número par o un 5? (regla aditiva)", "2/3", ["1/2", "1/6", "5/6"], "Par: 3 casos; el 5: 1 caso. No se superponen.", "3/6 + 1/6 = 4/6 = 2/3.")
    b.om(2, "Se lanzan dos monedas. ¿Cuál es la probabilidad de obtener dos caras? (regla multiplicativa)", "1/4", ["1/2", "1/3", "2/4"], "Multiplica las probabilidades.", "1/2 · 1/2 = 1/4.")
    b.cat(2, "¿Se suman o se multiplican las probabilidades?", ["Se suman («o», excluyentes)", "Se multiplican («y», independientes)"], [("sacar un 1 o un 2 en un dado", 0), ("que salga rojo o azul en una ruleta", 0), ("cara en una moneda y 6 en un dado", 1), ("dos caras seguidas", 1)],
          "«O» con sucesos excluyentes suma; «y» con independientes multiplica.", "O excluyente: suma; y independiente: multiplica.")
    b.om(3, "Una bolsa tiene 3 bolitas rojas y 2 azules. Sacas una, la devuelves y sacas otra. ¿Cuál es la probabilidad de que ambas sean rojas?", "9/25", ["3/5", "6/25", "9/10"], "Con reposición: 3/5 · 3/5.", "3/5 · 3/5 = 9/25.")
    b.om(3, "Se lanza un dado y una moneda. ¿Probabilidad de obtener un número mayor que 4 y cara?", "1/6", ["1/3", "1/2", "2/3"], "Mayor que 4: {5, 6}.", "2/6 · 1/2 = 1/6.")
    b.ord(3, "Ordena de menor a mayor probabilidad (un dado).", ["sacar un 7", "sacar un 6", "sacar un par", "sacar un número menor que 7"], "Imposible, 1/6, 1/2 y seguro.", "0 < 1/6 < 1/2 < 1.")
    b.om(4, "Misma bolsa (3 rojas y 2 azules), sin devolver la primera. ¿Probabilidad de que ambas sean rojas?", "3/10", ["9/25", "6/25", "3/5"], "Sin reposición: 3/5 · 2/4.", "3/5 · 2/4 = 6/20 = 3/10.")
    b.om(4, "En un curso, 60% practica fútbol, 30% básquetbol y 10% ambos. ¿Probabilidad de que un estudiante practique fútbol o básquetbol?", "80%", ["90%", "100%", "70%"], "P(A o B) = P(A) + P(B) − P(A y B).", "60 + 30 − 10 = 80 %.")
    b.nu(4, "¿Cuántos caminos tiene un diagrama de árbol al lanzar 3 monedas?", 8, "2 · 2 · 2.", "2³ = 8 caminos.", unidad="caminos")
    b.om(5, "Se lanzan dos dados. ¿Cuál es la probabilidad de que la suma sea 7?", "1/6", ["1/12", "7/36", "1/7"], "Cuenta los pares que suman 7: (1,6), (2,5)… de 36.", "Hay 6 pares de 36: 6/36 = 1/6.")
    b.om(5, "La probabilidad de lluvia el sábado es 0,3 y el domingo 0,4, de forma independiente. ¿Probabilidad de que no llueva ningún día?", "0,42", ["0,12", "0,7", "0,58"], "No llueve: 0,7 y 0,6.", "0,7 · 0,6 = 0,42.")
    b.om(5, "En un diagrama de árbol de 2 lanzamientos de moneda, ¿qué probabilidad tiene obtener al menos una cara?", "3/4", ["1/4", "1/2", "1"], "Lo contrario de «al menos una cara» es «ninguna cara».", "1 − P(SS) = 1 − 1/4 = 3/4.")
    return b.items


# ---------------- 2° medio ----------------
def ma2m_oa2():
    b = Autor("mat", "2m", 2)
    b.nu(1, "¿Cuánto es √49?", 7, "¿Qué número al cuadrado da 49?", "7² = 49.")
    b.nu(1, "¿Cuánto es ∛8?", 2, "¿Qué número al cubo da 8?", "2³ = 8.")
    b.nu(1, "¿Cuánto es log₂ 8?", 3, "¿A qué exponente hay que elevar 2 para obtener 8?", "2³ = 8, entonces log₂ 8 = 3.")
    b.om(2, "a^(1/2) es lo mismo que…", "√a", ["a/2", "2a", "a²"], "Exponente 1/2 es raíz cuadrada.", "a^(1/2) = √a.")
    b.nu(2, "¿Cuánto es 16^(1/2)?", 4, "Es √16.", "√16 = 4.")
    b.em(2, "Une cada logaritmo con su valor.", [["log₁₀ 100", "2"], ["log₃ 27", "3"], ["log₅ 1", "0"]], "Pregúntate a qué exponente hay que elevar la base.", "10² = 100, 3³ = 27, 5⁰ = 1.")
    b.co(3, "Si 2^x = 32, entonces x = log₂ 32 = ___", "5", ["16", "4", "6"], "2^5 = 32.", "2^5 = 32, entonces x = 5.")
    b.nu(3, "¿Cuánto es 8^(2/3)?", 4, "Primero la raíz cúbica, luego el cuadrado.", "∛8 = 2; 2² = 4.")
    b.om(3, "log_a P = x es equivalente a…", "a^x = P", ["x^a = P", "P^x = a", "a · x = P"], "Un logaritmo es un exponente.", "log_a P = x ⇔ a^x = P.")
    b.nu(4, "Calcula log₂ 4 + log₂ 8.", 5, "log₂ 4 = 2 y log₂ 8 = 3.", "2 + 3 = 5 (es igual a log₂ 32).")
    b.om(4, "¿Cuál es el valor de 27^(−1/3)?", "1/3", ["−3", "3", "−1/3"], "Exponente negativo: inverso. Exponente 1/3: raíz cúbica.", "27^(1/3) = 3; inverso: 1/3.")
    b.ord(4, "Ordena de menor a mayor.", ["log₂ 2", "√9", "log₁₀ 10.000", "2^3"], "Calcula cada valor.", "1 < 3 < 4 < 8.")
    b.nu(5, "Una bacteria se duplica cada hora. ¿Cuántas horas pasan para que 1 bacteria se convierta en 1.024? (2^x = 1.024)", 10, "x = log₂ 1.024.", "2^10 = 1.024: 10 horas.", unidad="horas")
    b.om(5, "¿Qué expresión es igual a √(a³)?", "a^(3/2)", ["a^(2/3)", "a^6", "3a/2"], "Raíz cuadrada: exponente 1/2.", "√(a³) = (a³)^(1/2) = a^(3/2).")
    b.nu(5, "La escala de Richter es logarítmica: cada punto más es 10 veces más amplitud. ¿Cuántas veces mayor es la amplitud de un sismo 8 que la de uno 6?", 100, "Diferencia de 2 puntos: 10².", "10² = 100 veces.", unidad="veces")
    return b.items


def ma2m_oa4():
    b = Autor("mat", "2m", 4)
    b.om(1, "¿Cuáles son las soluciones de x² = 25?", "x = 5 y x = −5", ["solo x = 5", "x = 25", "x = 12,5"], "Hay dos números que al cuadrado dan 25.", "5² = 25 y (−5)² = 25.")
    b.nu(1, "Resuelve 2x² = 18. ¿Cuál es la solución positiva?", 3, "x² = 9.", "x² = 9 → x = ±3; la positiva es 3.")
    b.co(1, "En x² + 5x + 6 = 0, el término independiente es ___.", "6", ["5", "1", "0"], "Es el número sin x.", "El término independiente es 6.")
    b.om(2, "¿Cuáles son las soluciones de x² − 4x = 0?", "x = 0 y x = 4", ["x = 4 solamente", "x = −4 y x = 0", "x = 2"], "Factoriza: x(x − 4) = 0.", "x = 0 o x − 4 = 0 → x = 4.")
    b.om(2, "Factoriza x² + 5x + 6.", "(x + 2)(x + 3)", ["(x + 1)(x + 6)", "(x − 2)(x − 3)", "(x + 5)(x + 1)"], "Busca dos números que sumen 5 y multipliquen 6.", "2 + 3 = 5 y 2 · 3 = 6.")
    b.cat(2, "¿Qué tipo de ecuación es?", ["Cuadrática", "No cuadrática"], [("x² − 9 = 0", 0), ("3x² + x = 2", 0), ("(x + 1)² = 4", 0), ("2x + 3 = 7", 1), ("x³ = 8", 1)],
          "Una ecuación cuadrática tiene grado 2.", "Las que tienen x² como mayor potencia son cuadráticas.")
    b.om(3, "¿Cuáles son las soluciones de x² − 5x + 6 = 0?", "x = 2 y x = 3", ["x = −2 y x = −3", "x = 1 y x = 6", "x = 5 y x = 6"], "Factoriza: (x − 2)(x − 3).", "x = 2 o x = 3.")
    b.om(3, "Resuelve (x − 1)² = 16.", "x = 5 y x = −3", ["x = 4 y x = −4", "x = 17", "x = 5 solamente"], "x − 1 = ±4.", "x − 1 = 4 → 5; x − 1 = −4 → −3.")
    b.em(3, "Une cada ecuación con sus soluciones.", [["x² = 36", "6 y −6"], ["x² − 7x = 0", "0 y 7"], ["x² − 1 = 0", "1 y −1"]], "Despeja o factoriza.", "x = ±6; x(x − 7) = 0; x = ±1.")
    b.om(4, "Con la fórmula general, ¿cuánto vale el discriminante de x² + 2x − 3 = 0?", "16", ["4", "−8", "8"], "Δ = b² − 4ac.", "4 − 4·1·(−3) = 4 + 12 = 16.")
    b.cat(4, "¿Cuántas soluciones reales tiene?", ["Dos soluciones", "Una solución", "Ninguna real"], [("x² − 9 = 0", 0), ("x² − 5x + 4 = 0", 0), ("x² − 6x + 9 = 0", 1), ("x² + 4x + 4 = 0", 1), ("x² + 1 = 0", 2), ("x² + x + 5 = 0", 2)],
          "Mira el discriminante Δ = b² − 4ac.", "Δ > 0: dos; Δ = 0: una; Δ < 0: ninguna real.")
    b.ord(4, "Ordena los pasos para completar el cuadrado en x² + 6x = 7.", ["Sumar 9 a ambos lados.", "Escribir (x + 3)² = 16.", "Sacar raíz: x + 3 = ±4.", "Obtener x = 1 o x = −7."], "La mitad de 6 es 3, y 3² = 9.", "x² + 6x + 9 = 16 → (x + 3)² = 16 → x = 1 o x = −7.")
    b.nu(5, "Un terreno rectangular mide x metros de ancho y (x + 3) de largo. Su área es 40 m². ¿Cuánto mide el ancho?", 5, "x(x + 3) = 40 → x² + 3x − 40 = 0.", "(x + 8)(x − 5) = 0 → x = 5 (el ancho no puede ser negativo).", unidad="m")
    b.nu(5, "Un número positivo multiplicado por sí mismo menos el doble del número da 15. ¿Cuál es el número?", 5, "x² − 2x = 15 → x² − 2x − 15 = 0.", "(x − 5)(x + 3) = 0 → x = 5.")
    b.om(5, "Una pelota se lanza y su altura es h = −t² + 6t. ¿En qué tiempos está en el suelo (h = 0)?", "t = 0 y t = 6", ["t = 3 solamente", "t = 6 solamente", "t = −6 y t = 0"], "Factoriza: −t(t − 6) = 0.", "Está en el suelo al lanzarla (t = 0) y al caer (t = 6).")
    return b.items


def ma2m_oa11():
    b = Autor("mat", "2m", 11)
    b.nu(1, "¿Cuánto es 4! (4 factorial)?", 24, "4 · 3 · 2 · 1.", "4! = 24.")
    b.nu(1, "¿De cuántas formas se pueden ordenar 3 libros en una repisa?", 6, "3 · 2 · 1.", "3! = 6 formas.", unidad="formas")
    b.co(1, "0! = ___", "1", ["0", "−1", "no existe"], "Es una convención matemática.", "Por definición, 0! = 1.")
    b.nu(2, "Tienes 3 poleras y 4 pantalones. ¿Cuántas combinaciones de ropa puedes formar?", 12, "Principio multiplicativo.", "3 · 4 = 12 combinaciones.", unidad="combinaciones")
    b.nu(2, "¿De cuántas formas pueden llegar 5 corredores a la meta (sin empates)?", 120, "5!.", "5! = 120 formas.", unidad="formas")
    b.cat(2, "¿Importa el orden?", ["Importa (permutación)", "No importa (combinación)"], [("podio de oro, plata y bronce", 0), ("clave de 4 dígitos", 0), ("elegir 3 integrantes de un comité", 1), ("elegir 2 sabores de helado", 1)],
          "Si cambiar el orden cambia el resultado, importa.", "Podio y clave dependen del orden; comité y sabores no.")
    b.nu(3, "¿Cuántas claves de 3 dígitos distintos se forman con los dígitos 1, 2, 3, 4 y 5?", 60, "5 · 4 · 3.", "5 · 4 · 3 = 60 claves.", unidad="claves")
    b.nu(3, "¿De cuántas formas se elige un presidente y un secretario entre 6 personas?", 30, "6 opciones para el primer cargo y 5 para el segundo.", "6 · 5 = 30 formas.", unidad="formas")
    b.om(3, "¿Cuánto es 6!/4!?", "30", ["2", "720", "24"], "Simplifica: 6 · 5 · 4!/4!.", "6!/4! = 6 · 5 = 30.")
    b.nu(4, "¿Cuántos equipos de 2 personas se forman con 5 personas? (el orden no importa)", 10, "C(5, 2) = 5 · 4 / 2.", "20 ÷ 2 = 10 equipos.", unidad="equipos")
    b.om(4, "Se ordenan al azar las letras A, B y C. ¿Cuál es la probabilidad de obtener «ABC»?", "1/6", ["1/3", "1/2", "1/9"], "Hay 3! = 6 ordenamientos posibles.", "1 caso de 6.")
    b.ord(4, "Ordena de menor a mayor.", ["3!", "C(5, 2)", "4!", "5!"], "Calcula: 6, 10, 24 y 120.", "6 < 10 < 24 < 120.")
    b.nu(5, "¿Cuántas formas hay de elegir 3 estudiantes de un grupo de 6 para una delegación?", 20, "C(6, 3) = 6 · 5 · 4 / 3!.", "120 ÷ 6 = 20 formas.", unidad="formas")
    b.om(5, "En un sorteo eliges 2 números distintos del 1 al 10 (sin orden). ¿Probabilidad de acertar el par ganador?", "1/45", ["1/90", "1/10", "1/20"], "C(10, 2) = 45 pares posibles.", "Hay 45 pares: la probabilidad es 1/45.")
    b.om(5, "Se sientan 4 amigos en fila al azar. ¿Probabilidad de que Ana y Beto queden juntos?", "1/2", ["1/4", "1/6", "1/3"], "Trata a Ana y Beto como un bloque: 3! · 2 casos de 4!.", "12 de 24 casos: 1/2.")
    return b.items


# ---------------- 3° medio (FG-MATE-3M) ----------------
def ma3m_oac1():
    b = Autor("mat", "3m", 1)
    b.om(1, "¿Cuánto es i², donde i es la unidad imaginaria?", "−1", ["1", "i", "0"], "Por definición, i = √−1.", "i² = −1.")
    b.co(1, "En el complejo 3 + 4i, la parte real es ___.", "3", ["4", "4i", "7"], "La parte real no lleva i.", "Parte real 3, parte imaginaria 4.")
    b.om(1, "¿Cuánto es (2 + 3i) + (1 + 2i)?", "3 + 5i", ["3 + 6i", "2 + 6i", "5 + 3i"], "Suma reales con reales e imaginarios con imaginarios.", "(2 + 1) + (3 + 2)i = 3 + 5i.")
    b.om(2, "¿Cuánto es (5 + 2i) − (3 + 6i)?", "2 − 4i", ["2 + 4i", "8 − 4i", "2 + 8i"], "Resta parte por parte.", "(5 − 3) + (2 − 6)i = 2 − 4i.")
    b.om(2, "¿Cuánto es √−9?", "3i", ["−3", "9i", "3"], "√−9 = √9 · √−1.", "√−9 = 3i.")
    b.em(2, "Une cada complejo con su conjugado.", [["2 + 3i", "2 − 3i"], ["−1 − i", "−1 + i"], ["4i", "−4i"]], "El conjugado cambia el signo de la parte imaginaria.", "Se cambia el signo de la parte imaginaria.")
    b.om(3, "¿Cuánto es (1 + i)(1 − i)?", "2", ["0", "1 − i²", "2i"], "Usa (a + b)(a − b) = a² − b².", "1 − i² = 1 − (−1) = 2.")
    b.om(3, "¿Cuánto es 2i · 3i?", "−6", ["6", "6i", "5i"], "i · i = i² = −1.", "6i² = −6.")
    b.cat(3, "¿Número real o imaginario puro?", ["Real", "Imaginario puro"], [("i²", 0), ("(1 + i)(1 − i)", 0), ("√16", 0), ("5i", 1), ("√−4", 1), ("i³ · i⁻²", 1)],
          "Calcula cada expresión.", "i² = −1, (1 + i)(1 − i) = 2 y √16 = 4 son reales; 5i, 2i e i son imaginarios puros.")
    b.om(4, "¿Cuánto es (2 + i)²?", "3 + 4i", ["4 + i²", "5 + 4i", "4 + 4i"], "(a + b)² = a² + 2ab + b².", "4 + 4i + i² = 4 + 4i − 1 = 3 + 4i.")
    b.ord(4, "Ordena las potencias de i según su valor, empezando por i¹.", ["i", "−1", "−i", "1"], "i¹, i², i³, i⁴.", "i¹ = i, i² = −1, i³ = −i, i⁴ = 1.")
    b.nu(4, "¿Cuál es el módulo de 3 + 4i? (|a + bi| = √(a² + b²))", 5, "√(9 + 16).", "√25 = 5.")
    b.om(5, "¿Cuánto es (4 + 2i) ÷ (1 + i)? (multiplica por el conjugado)", "3 − i", ["4 + 2i", "2 + i", "3 + i"], "Multiplica arriba y abajo por (1 − i).", "(4 + 2i)(1 − i) = 4 − 4i + 2i − 2i² = 6 − 2i; ÷ 2 = 3 − i.")
    b.om(5, "¿Cuánto es i^23?", "−i", ["i", "1", "−1"], "Las potencias de i se repiten cada 4.", "23 = 4 · 5 + 3, así que i^23 = i³ = −i.")
    b.om(5, "En el plano complejo, ¿dónde se ubica el punto que representa −2 + 3i?", "en el segundo cuadrante", ["en el primer cuadrante", "en el tercer cuadrante", "en el eje real"], "Parte real negativa, parte imaginaria positiva.", "x = −2 e y = 3: segundo cuadrante.")
    return b.items


def ma3m_oac2():
    b = Autor("mat", "3m", 2)
    b.nu(1, "¿Cuál es el rango de los datos 4, 9, 2, 7, 5?", 7, "Rango = máximo − mínimo.", "9 − 2 = 7.")
    b.om(1, "¿Qué mide la desviación estándar?", "qué tan dispersos están los datos respecto de la media", ["el dato más repetido", "el valor central", "la cantidad de datos"], "Es una medida de dispersión.", "Indica cuánto se alejan los datos del promedio.")
    b.co(1, "La probabilidad de A dado B se escribe P(A ___ B).", "|", ["+", "·", "−"], "Se lee «A dado B».", "Se escribe P(A | B).")
    b.om(2, "Dos cursos tienen promedio 5,5. El curso A tiene notas entre 5,0 y 6,0; el B, entre 3,0 y 7,0. ¿Cuál tiene mayor dispersión?", "el curso B", ["el curso A", "son iguales", "no se puede saber nada"], "Compara el rango de cada curso.", "El curso B tiene un rango mayor: más dispersión.")
    b.nu(2, "La media de 2, 4, 6, 8 es 5. ¿Cuál es la suma de las distancias absolutas de cada dato a la media?", 8, "|2 − 5| + |4 − 5| + |6 − 5| + |8 − 5|.", "3 + 1 + 1 + 3 = 8.")
    b.em(2, "Une cada medida con lo que describe.", [["media", "tendencia central"], ["rango", "dispersión"], ["P(A | B)", "probabilidad condicional"]], "Separa centro, dispersión y probabilidad.", "La media es centro; el rango, dispersión; P(A|B), probabilidad condicional.")
    b.om(3, "En un curso de 30 estudiantes, 12 son mujeres y 6 de ellas usan lentes. ¿Cuál es P(lentes | mujer)?", "1/2", ["1/5", "6/30", "12/30"], "Solo se consideran las mujeres.", "6 de 12 = 1/2.")
    b.om(3, "Se saca una carta de un naipe de 52. Sabiendo que es roja, ¿cuál es la probabilidad de que sea corazón?", "1/2", ["1/4", "1/13", "1/26"], "Hay 26 rojas: 13 corazones y 13 diamantes.", "13 de 26 = 1/2.")
    b.cat(3, "¿Mayor o menor dispersión?", ["Menor dispersión", "Mayor dispersión"], [("10, 10, 11, 9, 10", 0), ("50, 51, 49, 50", 0), ("1, 20, 5, 40", 1), ("3, 15, 30, 8", 1)],
          "Compara qué tan separados están los datos.", "Los primeros grupos están muy juntos; los otros, muy separados.")
    b.om(4, "Tabla: de 100 personas, 40 hacen deporte; de ellas, 30 duermen bien. De las 60 que no hacen deporte, 24 duermen bien. ¿P(duerme bien | hace deporte)?", "3/4", ["3/10", "2/5", "54/100"], "Divide por quienes hacen deporte.", "30 de 40 = 3/4.")
    b.om(4, "Con la misma tabla, ¿P(duerme bien | no hace deporte)?", "2/5", ["24/100", "3/4", "1/2"], "Divide por quienes no hacen deporte.", "24 de 60 = 2/5.")
    b.ord(4, "Ordena los pasos para calcular P(A | B) desde una tabla.", ["Identificar el grupo B.", "Contar los casos de B.", "Contar los casos que son A y B.", "Dividir los casos de A y B por los casos de B."], "La condición reduce el espacio muestral.", "P(A | B) = casos (A y B) ÷ casos de B.")
    b.om(5, "Un test detecta una enfermedad. ¿Por qué no basta con mirar el porcentaje de aciertos para decidir?", "porque si la enfermedad es rara, muchos positivos pueden ser falsos", ["porque los tests nunca fallan", "porque la media siempre es 50%", "porque la probabilidad no se usa en salud"], "Piensa en la probabilidad condicional y en lo poco frecuente.", "Con enfermedades raras, P(enfermo | positivo) puede ser baja.")
    b.om(5, "Dos inversiones tienen la misma ganancia promedio; A varía poco y B varía mucho. ¿Qué decisión es razonable para alguien que no quiere arriesgar?", "elegir A, por su menor dispersión", ["elegir B, por su mayor dispersión", "da lo mismo siempre", "no invertir nunca en nada"], "Más dispersión significa más incertidumbre.", "Menor dispersión es menor riesgo.")
    b.nu(5, "En una urna hay 5 bolitas rojas y 3 azules. Se saca una roja y no se devuelve. ¿Cuántas bolitas rojas quedan para la segunda extracción?", 4, "Se sacó una roja.", "5 − 1 = 4 rojas de 7 bolitas en total.")
    return b.items


def ma3m_oac3():
    b = Autor("mat", "3m", 3)
    b.om(1, "¿Qué función modela algo que se duplica cada período?", "exponencial", ["lineal", "constante", "cuadrática"], "Multiplica por 2 cada vez.", "Duplicar es crecer en forma exponencial.")
    b.nu(1, "Si f(x) = 2^x, ¿cuánto es f(4)?", 16, "2 · 2 · 2 · 2.", "2^4 = 16.")
    b.co(1, "En f(x) = 3 · 2^x, el valor inicial f(0) es ___.", "3", ["2", "6", "1"], "2^0 = 1.", "3 · 1 = 3.")
    b.om(2, "¿Cuál de estas funciones es decreciente?", "f(x) = (1/2)^x", ["f(x) = 2^x", "f(x) = 3^x", "f(x) = x + 5"], "Base entre 0 y 1: decrece.", "Con base 1/2 la función decrece.")
    b.nu(2, "Una población de 100 bacterias se triplica cada hora. ¿Cuántas habrá en 2 horas?", 900, "100 · 3².", "100 · 9 = 900.", unidad="bacterias")
    b.em(2, "Une cada situación con su modelo.", [["un ahorro que gana 5 % anual compuesto", "exponencial creciente"], ["un medicamento que se elimina a la mitad cada 6 horas", "exponencial decreciente"], ["un taxi: $500 fijo más $300 por km", "lineal"]], "¿Se multiplica o se suma en cada paso?", "Multiplicar: exponencial; sumar: lineal.")
    b.nu(3, "Un auto de $10.000.000 pierde la mitad de su valor cada 5 años. ¿Cuánto vale en millones después de 10 años?", 2, "Dos períodos de 5 años: se divide por 2 dos veces. Hay un decimal en el camino.", "10 → 5 → 2,5 millones; la respuesta más cercana como entero es 2 (2,5 millones).", tol=1, unidad="millones")
    b.nu(3, "¿Cuántos años tarda en duplicarse un capital que crece según 2^(t/7)?", 7, "2^(t/7) = 2 cuando t/7 = 1.", "t = 7 años.", unidad="años")
    b.om(3, "La función inversa de f(x) = 10^x es…", "log₁₀ x", ["x/10", "x^10", "10x"], "El logaritmo deshace la potencia.", "log₁₀(10^x) = x.")
    b.om(4, "Se usa la función logarítmica para medir…", "la intensidad de los sismos (Richter) y del sonido (decibeles)", ["el área de un rectángulo", "la velocidad de un auto", "el número de alumnos"], "Son escalas que crecen por potencias de 10.", "Richter y decibeles son escalas logarítmicas.")
    b.nu(4, "Un sonido de 60 dB y otro de 80 dB: cada 10 dB la intensidad se multiplica por 10. ¿Cuántas veces más intenso es el de 80 dB?", 100, "Son 20 dB más: dos veces ×10.", "10 · 10 = 100 veces.", unidad="veces")
    b.ord(4, "Ordena de menor a mayor para x = 3.", ["log₂ x · 0 + 1", "2x", "x²", "2^x"], "Calcula: 1, 6, 9 y 8… revisa con cuidado.", "Para x = 3: 1, 6, 8 (2³) y 9 (3²). Ojo: 2^x = 8 < x² = 9.")
    b.nu(5, "Si la población de una ciudad crece 10 % al año, partiendo de 1.000 personas, ¿cuántas habrá en 2 años?", 1210, "1.000 · 1,1².", "1.000 · 1,21 = 1.210 personas.", unidad="personas")
    b.om(5, "El carbono-14 se reduce a la mitad cada 5.730 años. Un fósil tiene 1/4 del C-14 original. ¿Qué edad aproximada tiene?", "11.460 años", ["5.730 años", "2.865 años", "22.920 años"], "1/4 = dos semividas.", "2 · 5.730 = 11.460 años.")
    b.om(5, "¿Cuál es la solución de 2^x = 50?", "x = log₂ 50 (entre 5 y 6)", ["x = 25", "x = 50/2", "x = 7"], "2^5 = 32 y 2^6 = 64.", "x = log₂ 50, un valor entre 5 y 6.")
    return b.items


# ---------------- 4° medio (FG-MATE-4M) ----------------
def ma4m_oac1():
    b = Autor("mat", "4m", 1)
    b.nu(1, "¿Cuánto es el 15 % de $20.000?", 3000, "10 % = 2.000 y 5 % = 1.000.", "2.000 + 1.000 = $3.000.", unidad="$")
    b.om(1, "¿Qué es la tasa de interés?", "el porcentaje que se paga o se gana por un dinero en un período", ["el precio de un producto", "el sueldo mínimo", "un impuesto fijo"], "Se aplica a créditos y ahorros.", "Es el costo o la ganancia por usar dinero en el tiempo.")
    b.co(1, "El IPC mide la variación de los ___ de una canasta de bienes y servicios.", "precios", ["sueldos", "impuestos", "intereses"], "Se usa para medir la inflación.", "El IPC mide cómo cambian los precios.")
    b.nu(2, "Ahorras $100.000 al 5 % de interés simple anual. ¿Cuánto interés ganas en 1 año?", 5000, "5 % de 100.000.", "$5.000.", unidad="$")
    b.nu(2, "Un producto de $40.000 sube 10 %. ¿Cuál es su nuevo precio?", 44000, "Calcula el 10 % y súmalo.", "40.000 + 4.000 = $44.000.", unidad="$")
    b.em(2, "Une cada concepto con su definición.", [["inflación", "aumento general de los precios"], ["crédito", "dinero prestado que se devuelve con interés"], ["UF", "unidad que se reajusta según la inflación"]], "Vocabulario financiero chileno.", "Inflación, crédito y UF.")
    b.nu(3, "Con interés compuesto del 10 % anual, ¿cuánto tendrás al cabo de 2 años si depositas $100.000?", 121000, "100.000 · 1,1².", "100.000 · 1,21 = $121.000.", unidad="$")
    b.om(3, "¿Por qué un crédito con CAE más baja suele ser mejor?", "porque refleja un costo total menor del crédito", ["porque te prestan más dinero siempre", "porque no hay que pagarlo", "porque dura menos días"], "La CAE incluye intereses y gastos.", "La Carga Anual Equivalente resume el costo total: menor es más barato.")
    b.cat(3, "¿Interés simple o compuesto?", ["Simple", "Compuesto"], [("el interés se calcula siempre sobre el capital inicial", 0), ("se gana lo mismo cada año", 0), ("el interés se suma al capital y genera más interés", 1), ("el crecimiento es exponencial", 1)],
          "En el compuesto, los intereses generan intereses.", "Simple: siempre sobre el capital inicial; compuesto: interés sobre interés.")
    b.om(4, "Una tienda ofrece pagar $120.000 en 12 cuotas de $12.000. ¿Cuánto pagas de más?", "$24.000", ["$12.000", "$0", "$144.000"], "12 · 12.000 = 144.000.", "144.000 − 120.000 = $24.000 extra.")
    b.nu(4, "Si la inflación anual es 4 % y tu sueldo de $500.000 sube 4 %, ¿cuál es tu nuevo sueldo?", 520000, "4 % de 500.000.", "500.000 + 20.000 = $520.000 (mantiene el poder de compra).", unidad="$")
    b.ord(4, "Ordena los pasos para comparar dos créditos.", ["Revisar el monto y el plazo.", "Comparar la CAE de cada uno.", "Calcular el costo total (cuota × número de cuotas).", "Elegir el de menor costo total que puedas pagar."], "Monto, CAE, costo total y decisión.", "Así se toma una decisión financiera informada.")
    b.om(5, "Un precio baja 20 % y luego sube 20 %. Respecto del precio original, queda…", "4 % más bajo", ["igual", "4 % más alto", "20 % más bajo"], "Prueba con $100.", "100 → 80 → 96: queda 4 % más bajo.")
    b.om(5, "La UF subió de 36.000 a 37.800 pesos en un año. ¿Cuál fue su variación porcentual?", "5 %", ["1,8 %", "18 %", "50 %"], "(37.800 − 36.000) ÷ 36.000.", "1.800 ÷ 36.000 = 0,05 = 5 %.")
    b.om(5, "¿Qué opción conviene más para un ahorro a 3 años?", "interés compuesto del 6 % anual", ["interés simple del 6 % anual", "guardar el dinero en casa", "un crédito del 6 %"], "El compuesto genera interés sobre interés.", "Con la misma tasa, el compuesto da más que el simple.")
    return b.items


def ma4m_oac2():
    b = Autor("mat", "4m", 2)
    b.om(1, "¿Qué forma tiene la curva de la distribución normal?", "de campana, simétrica", ["una recta creciente", "una U", "escalones"], "Se la conoce como campana de Gauss.", "Es una campana simétrica alrededor de la media.")
    b.co(1, "En la distribución normal, la media, la mediana y la moda son ___.", "iguales", ["distintas siempre", "cero", "negativas"], "La curva es simétrica.", "En una normal coinciden las tres.")
    b.om(1, "Un experimento binomial tiene…", "dos resultados posibles en cada intento (éxito o fracaso)", ["infinitos resultados", "resultados que dependen unos de otros", "un solo intento siempre"], "Por ejemplo, cara o sello.", "Cada intento es éxito o fracaso, con probabilidad constante.")
    b.om(2, "Se lanza una moneda 3 veces. ¿Probabilidad de obtener exactamente 3 caras?", "1/8", ["1/3", "3/8", "1/2"], "(1/2)³.", "(1/2)³ = 1/8.")
    b.nu(2, "Un jugador encesta 80 % de sus tiros. En 10 tiros, ¿cuántos encestes se esperan? (n · p)", 8, "Esperanza = n · p.", "10 · 0,8 = 8 encestes.", unidad="encestes")
    b.em(2, "Une cada intervalo de la normal con su porcentaje aproximado.", [["media ± 1 desviación estándar", "68 %"], ["media ± 2 desviaciones estándar", "95 %"], ["media ± 3 desviaciones estándar", "99,7 %"]], "Es la regla empírica.", "68 %, 95 % y 99,7 %.")
    b.om(3, "Se lanza una moneda 3 veces. ¿Probabilidad de obtener exactamente 2 caras?", "3/8", ["1/8", "2/3", "1/2"], "Hay 3 formas: CCS, CSC, SCC.", "3 · (1/2)³ = 3/8.")
    b.om(3, "Estaturas con media 160 cm y desviación estándar 10 cm (distribución normal). ¿Qué porcentaje mide entre 150 y 170 cm?", "aproximadamente 68 %", ["50 %", "95 %", "100 %"], "Es la media ± 1 desviación estándar.", "Entre 150 y 170 está el 68 % aproximado.")
    b.cat(3, "¿Sigue un modelo binomial?", ["Binomial", "No binomial"], [("número de caras en 10 lanzamientos", 0), ("número de penales convertidos de 5", 0), ("la estatura de un estudiante", 1), ("el tiempo que tarda un bus", 1)],
          "Binomial: contar éxitos en n intentos independientes.", "Contar caras o penales es binomial; estatura y tiempo son variables continuas.")
    b.om(4, "Puntajes con media 500 y desviación estándar 100. ¿Qué porcentaje aproximado obtiene más de 700?", "2,5 %", ["5 %", "16 %", "0,15 %"], "700 es media + 2 desviaciones; fuera del 95 % central, la mitad está arriba.", "(100 − 95) ÷ 2 = 2,5 %.")
    b.nu(4, "En un examen de 20 preguntas de verdadero o falso respondidas al azar, ¿cuántas correctas se esperan?", 10, "n · p con p = 1/2.", "20 · 0,5 = 10.")
    b.ord(4, "Ordena de menor a mayor probabilidad (moneda lanzada 4 veces).", ["4 caras", "3 caras", "2 caras"], "Cuenta cuántas formas hay de cada resultado: 1, 4 y 6.", "P(4) = 1/16 < P(3) = 4/16 < P(2) = 6/16.")
    b.om(5, "Un medio dice: «Un estudiante sacó 750 puntos (media 500, desviación 100), un resultado imposible». ¿Qué responderías?", "Es poco frecuente (2,5 desviaciones sobre la media), pero no imposible.", ["Tiene razón: es imposible.", "Es el resultado más común.", "La normal no tiene valores altos."], "En la normal, los valores extremos son raros, no imposibles.", "Está fuera del 95 % central: es poco frecuente, pero posible.")
    b.om(5, "Una fábrica dice que solo 2 % de sus ampolletas fallan. En una caja de 50, ¿cuántas se espera que fallen?", "1", ["2", "5", "10"], "n · p = 50 · 0,02.", "50 · 0,02 = 1 ampolleta.")
    b.om(5, "¿Por qué un estudio con 10 personas es menos confiable que uno con 1.000 para estimar un promedio?", "porque con más datos la estimación varía menos", ["porque 10 es un número impar", "porque las muestras grandes siempre mienten", "porque el promedio no cambia nunca"], "Piensa en la variabilidad de las muestras.", "Las muestras grandes dan estimaciones más estables.")
    return b.items


def ma4m_oac3():
    b = Autor("mat", "4m", 3)
    b.nu(1, "Si f(x) = x³, ¿cuánto es f(2)?", 8, "2 · 2 · 2.", "2³ = 8.")
    b.nu(1, "¿Cuánto es sen(90°)?", 1, "En el círculo unitario, 90° está arriba.", "sen 90° = 1.")
    b.co(1, "La función cos(x) es ___, porque sus valores se repiten cada 360°.", "periódica", ["lineal", "constante", "creciente siempre"], "Se repite en ciclos.", "Seno y coseno son periódicas.")
    b.om(2, "¿Cuál es el valor máximo de f(x) = sen(x)?", "1", ["0", "360", "−1"], "Oscila entre −1 y 1.", "El máximo de sen x es 1.")
    b.nu(2, "¿Cuánto es cos(0°)?", 1, "En 0° el punto del círculo unitario es (1, 0).", "cos 0° = 1.")
    b.em(2, "Une cada función con su gráfico típico.", [["f(x) = x²", "parábola en forma de U"], ["f(x) = x³", "curva creciente en forma de S"], ["f(x) = sen x", "onda que se repite"]], "Piensa en la forma de cada curva.", "Parábola, cúbica y onda periódica.")
    b.om(3, "¿Cuál es el período de f(x) = sen(x), en grados?", "360°", ["90°", "180°", "720°"], "Una vuelta completa.", "Seno se repite cada 360°.")
    b.om(3, "¿Qué función tiene simetría respecto del eje y (es par)?", "f(x) = x²", ["f(x) = x³", "f(x) = sen x", "f(x) = x"], "f(−x) = f(x).", "(−x)² = x²: es par.")
    b.cat(3, "¿Crece siempre o no?", ["Crece siempre", "No crece siempre"], [("f(x) = x³", 0), ("f(x) = x", 0), ("f(x) = x²", 1), ("f(x) = sen x", 1)],
          "Piensa en todo el dominio de los números reales.", "x³ y x crecen siempre; x² baja y luego sube; sen x oscila.")
    b.om(4, "La marea en un puerto sube y baja cada 12 horas aproximadamente. ¿Qué función la modela mejor?", "una función seno o coseno", ["una función lineal", "una función cúbica", "una función constante"], "Es un fenómeno periódico.", "Lo periódico se modela con seno o coseno.")
    b.om(4, "¿Qué amplitud tiene f(x) = 3 sen(x)?", "3", ["1", "6", "1/3"], "La amplitud multiplica la altura de la onda.", "Oscila entre −3 y 3: amplitud 3.")
    b.ord(4, "Ordena de menor a mayor para x = 2.", ["x", "x²", "x³", "x⁴"], "Calcula 2, 4, 8 y 16.", "2 < 4 < 8 < 16.")
    b.om(5, "El volumen de un cubo de arista a es V = a³. Si la arista se duplica, el volumen…", "se multiplica por 8", ["se duplica", "se multiplica por 4", "se triplica"], "(2a)³ = 8a³.", "Al duplicar la arista, el volumen se multiplica por 2³ = 8.")
    b.om(5, "Una rueda de la fortuna tiene la altura h(t) = 20 + 15 sen(t). ¿Cuál es la altura máxima?", "35 m", ["20 m", "15 m", "5 m"], "sen(t) vale como máximo 1.", "20 + 15 · 1 = 35 m.")
    b.om(5, "¿Cuál es la altura mínima de esa misma rueda?", "5 m", ["0 m", "15 m", "20 m"], "sen(t) vale como mínimo −1.", "20 + 15 · (−1) = 5 m.")
    return b.items


GENERADORES = {
    "1_medio.matematica.OA1": ma1m_oa1, "1_medio.matematica.OA4": ma1m_oa4, "1_medio.matematica.OA14": ma1m_oa14,
    "2_medio.matematica.OA2": ma2m_oa2, "2_medio.matematica.OA4": ma2m_oa4, "2_medio.matematica.OA11": ma2m_oa11,
    "3_medio.matematica.OA1": ma3m_oac1, "3_medio.matematica.OA2": ma3m_oac2, "3_medio.matematica.OA3": ma3m_oac3,
    "4_medio.matematica.OA1": ma4m_oac1, "4_medio.matematica.OA2": ma4m_oac2, "4_medio.matematica.OA3": ma4m_oac3,
}
