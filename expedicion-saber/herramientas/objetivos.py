"""Registro de objetivos de aprendizaje (OA) incluidos en el banco.

Códigos según las Bases Curriculares de 1° a 6° básico (curriculumnacional.cl).
- verificacion.codigo = "verificado": el código y su tema se confirmaron en una página
  oficial de curriculumnacional.cl (la URL queda en verificacion.fuente).
- verificacion.codigo = "pendiente": el código existe en el eje, pero no se pudo confirmar
  su redacción. Revisar antes de usarlo en documentos oficiales.
- verificacion.texto = "resumen": objetivo_oficial es un resumen fiel, no la cita literal.
"""

CN = "https://www.curriculumnacional.cl"


def oa(nivel, asig, num, eje, resumen, dificultad, prereq, fuente, codigo="verificado"):
    return {
        "id_objetivo": f"{nivel}.{asig}.OA{num}",
        "nivel": nivel,
        "asignatura": asig,
        "eje": eje,
        "objetivo_oficial": f"OA {num}: {resumen}",
        "dificultad": dificultad,
        "prerequisitos": prereq,
        "verificacion": {"codigo": codigo, "texto": "resumen", "fuente": fuente},
    }


NUM = "Números y operaciones"
LEC = "Lectura"
ESC = "Escritura"

OBJETIVOS = [
    # ---------- Matemática ----------
    oa("1_basico", "matematica", 1, NUM, "Contar números del 0 al 100 de 1 en 1, de 2 en 2, de 5 en 5 y de 10 en 10, hacia adelante y hacia atrás, empezando por cualquier número menor que 100.",
       1, [], f"{CN}/614/w3-article-17473.html"),
    oa("1_basico", "matematica", 4, NUM, "Comparar y ordenar números del 0 al 20 de menor a mayor y/o viceversa, utilizando material concreto y/o software educativo.",
       1, ["1_basico.matematica.OA1"], "https://curriculumnacional.mineduc.cl/614/w3-propertyvalue-53688.html"),
    oa("1_basico", "matematica", 9, NUM, "Demostrar que comprende la adición y la sustracción de números del 0 al 20 progresivamente (0 a 5, 6 a 10, 11 a 20), con dos sumandos.",
       2, ["1_basico.matematica.OA1"], f"{CN}/portal/Ejes/Matematica/Numeros-y-operaciones/17481:MA01-OA-09"),
    oa("2_basico", "matematica", 1, NUM, "Contar números del 0 al 1 000 de 2 en 2, de 5 en 5, de 10 en 10 y de 100 en 100, hacia adelante y hacia atrás.",
       2, ["1_basico.matematica.OA1"], f"{CN}/614/w3-article-17509.html"),
    oa("2_basico", "matematica", 3, NUM, "Comparar y ordenar números del 0 al 100 de menor a mayor y viceversa, usando material concreto y monedas nacionales.",
       2, ["1_basico.matematica.OA4"], f"{CN}/portal/Ejes/Matematica/Numeros-y-operaciones/17511:MA02-OA-03"),
    oa("2_basico", "matematica", 9, NUM, "Demostrar que comprende la adición y la sustracción en el ámbito del 0 al 100, resolviendo problemas y aplicando el algoritmo sin reserva.",
       3, ["1_basico.matematica.OA9"], f"{CN}/curriculum/1o-6o-basico/matematica/2-basico/ma02-oa-09"),
    oa("2_basico", "matematica", 11, NUM, "Demostrar que comprende la multiplicación como adición de sumandos iguales, usando las tablas del 2, del 5 y del 10 para resolver problemas.",
       3, ["2_basico.matematica.OA1", "2_basico.matematica.OA9"], f"{CN}/portal/Ejes/Matematica/Numeros-y-operaciones/17519:MA02-OA-11"),
    oa("3_basico", "matematica", 6, NUM, "Demostrar que comprende la adición y la sustracción de números del 0 al 1 000, con estrategias personales, algoritmos con y sin reserva y problemas con operaciones combinadas.",
       3, ["2_basico.matematica.OA9"], f"{CN}/portal/Ejes/Matematica/Numeros-y-operaciones/17551:MA03-OA-06"),
    oa("3_basico", "matematica", 8, NUM, "Demostrar que comprende las tablas de multiplicar hasta 10 de manera progresiva, usando representaciones y la distributividad como estrategia.",
       3, ["2_basico.matematica.OA11"], f"{CN}/docente/629/w3-article-17553.html"),
    oa("3_basico", "matematica", 9, NUM, "Demostrar que comprende la división en el contexto de las tablas de hasta 10 × 10, relacionándola con la multiplicación.",
       4, ["3_basico.matematica.OA8"], f"{CN}/portal/Ejes/Matematica/Numeros-y-operaciones/17554:MA03-OA-09"),
    oa("3_basico", "matematica", 11, NUM, "Demostrar que comprende las fracciones de uso común (1/4, 1/3, 1/2, 2/3, 3/4): parte de un todo, situaciones de uso y comparación con igual denominador.",
       4, ["3_basico.matematica.OA9"], f"{CN}/portal/Ejes/Matematica/Numeros-y-operaciones/17556:MA03-OA-11"),
    oa("4_basico", "matematica", 3, NUM, "Demostrar que comprende la adición y la sustracción de números hasta 1 000, usando estrategias personales, estimación y algoritmos.",
       4, ["3_basico.matematica.OA6"], f"{CN}/portal/Ejes/Matematica/Numeros-y-operaciones/17594:MA04-OA-03"),
    oa("4_basico", "matematica", 5, NUM, "Demostrar que comprende la multiplicación de números de tres dígitos por números de un dígito, usando la distributividad, la estimación y el algoritmo.",
       4, ["3_basico.matematica.OA8"], f"{CN}/portal/Ejes/Matematica/Numeros-y-operaciones/17596:MA04-OA-05"),
    oa("4_basico", "matematica", 6, NUM, "Demostrar que comprende la división con dividendos de dos dígitos y divisores de un dígito, usando su relación con la multiplicación y la estimación del cociente.",
       5, ["3_basico.matematica.OA9"], f"{CN}/614/w3-article-17597.html"),
    oa("4_basico", "matematica", 8, NUM, "Demostrar que comprende las fracciones: parte de un todo o de un grupo, ubicación en la recta numérica, fracciones equivalentes, y comparar y ordenar fracciones.",
       5, ["3_basico.matematica.OA11"], f"{CN}/docentes/Educacion-General/Matematica-4-basico/MA04-OA-08/17599:MA04-OA-08"),

    # ---------- Lenguaje y Comunicación ----------
    oa("1_basico", "lenguaje", 3, LEC, "Identificar los sonidos que componen las palabras (conciencia fonológica), separando y combinando fonemas y sílabas.",
       1, [], f"{CN}/614/w3-article-17116.html"),
    oa("1_basico", "lenguaje", 4, LEC, "Leer palabras aisladas y en contexto, aplicando la correspondencia letra-sonido en sílabas directas, indirectas, complejas y dígrafos.",
       1, ["1_basico.lenguaje.OA3"], f"{CN}/recursos/leo-1-basico-texto-estudiante-tomo-1", codigo="pendiente"),
    oa("1_basico", "lenguaje", 8, LEC, "Demostrar comprensión de narraciones: información explícita, secuencia de acciones y personajes.",
       2, ["1_basico.lenguaje.OA4"], f"{CN}/recursos/leo-1-basico-texto-estudiante-tomo-1", codigo="pendiente"),
    oa("2_basico", "lenguaje", 5, LEC, "Demostrar comprensión de las narraciones leídas: información explícita e implícita, secuencia de acciones, características y sentimientos de los personajes, ambiente y opinión.",
       2, ["1_basico.lenguaje.OA8"], f"{CN}/portal/Ejes/Lenguaje-y-Comunicacion/Lectura-Comprension/17151:LE02-OA-05"),
    oa("2_basico", "lenguaje", 21, ESC, "Escribir correctamente para facilitar la comprensión del lector: ce-ci, que-qui, ge-gi, gue-gui, güe-güi, r-rr-nr, mayúsculas y punto final.",
       2, ["1_basico.lenguaje.OA4"], f"{CN}/portal/Educacion-General/Lenguaje-y-comunicacion-2-basico/LE02-OA-01/131696:Programa-de-apoyo-compartido-Lenguaje-y-Comunicacion-2-basico-Periodo-2", codigo="pendiente"),
    oa("3_basico", "lenguaje", 4, LEC, "Profundizar la comprensión de las narraciones leídas: información explícita e implícita, secuencia, personajes, ambiente y opinión fundamentada.",
       3, ["2_basico.lenguaje.OA5"], f"{CN}/curriculum/1o-6o-basico/lenguaje-comunicacion/3-basico"),
    oa("3_basico", "lenguaje", 20, ESC, "Comprender la función de los artículos, sustantivos y adjetivos, y reemplazarlos o combinarlos para enriquecer y precisar lo que se escribe.",
       3, ["1_basico.lenguaje.OA4"], f"{CN}/614/w3-article-17203.html"),
    oa("3_basico", "lenguaje", 22, ESC, "Escribir correctamente: mayúsculas, punto seguido y aparte, plurales de palabras terminadas en z, ge-gi y je-ji, terminaciones cito-cita y coma en enumeraciones.",
       3, ["2_basico.lenguaje.OA21"], f"{CN}/portal/Ejes/Lenguaje-y-Comunicacion/Escritura-Produccion/17205:LE03-OA-22"),
    oa("4_basico", "lenguaje", 4, LEC, "Profundizar la comprensión de las narraciones leídas: ambiente, causas y consecuencias, personajes y postura fundamentada con ejemplos del texto.",
       4, ["3_basico.lenguaje.OA4"], f"{CN}/portal/Ejes/Lenguaje-y-Comunicacion/Lectura-Comprension/17225:LE04-OA-04"),
    oa("4_basico", "lenguaje", 10, LEC, "Aplicar estrategias para determinar el significado de palabras nuevas: claves del contexto, raíces y afijos, y orden alfabético para usar el diccionario.",
       4, ["3_basico.lenguaje.OA4"], f"{CN}/portal/Ejes/Lectura/Vocabulario/17231:LE04-OA-10"),
    oa("4_basico", "lenguaje", 21, ESC, "Escribir correctamente: b-v, h de uso frecuente, ay-hay-ahí y acentuación de palabras agudas, graves, esdrújulas y sobresdrújulas.",
       4, ["3_basico.lenguaje.OA22"], f"{CN}/614/w3-article-17242.html"),
]

POR_ID = {o["id_objetivo"]: o for o in OBJETIVOS}
