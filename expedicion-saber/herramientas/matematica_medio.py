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


GENERADORES = {
    "1_medio.matematica.OA1": ma1m_oa1, "1_medio.matematica.OA4": ma1m_oa4, "1_medio.matematica.OA14": ma1m_oa14,
    "2_medio.matematica.OA2": ma2m_oa2, "2_medio.matematica.OA4": ma2m_oa4, "2_medio.matematica.OA11": ma2m_oa11,
}
