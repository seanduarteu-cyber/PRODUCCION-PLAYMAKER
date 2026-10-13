"""Lenguaje y Comunicación / Lengua y Literatura 5° a 8° básico: 15 a 17 desafíos por OA (3 o 4 por nivel de dificultad, 1 a 5).

En los poemas, « / » separa los versos.
"""
from autor import Autor


def le05_oa4():
    b = Autor("len", 5, 4)
    A = ("El viento soplaba como un lobo hambriento entre los cerros de Chiloé. Las nubes corrían apuradas hacia el mar. "
         "En la casa de palafito, la abuela Rosa tejía un chaleco de lana junto al fogón, mientras Pedro escuchaba sus historias de barcos y tormentas.")
    b.om(1, "¿Qué comparación aparece en el texto?", "el viento soplaba como un lobo hambriento",
         ["las nubes corrían apuradas", "la abuela tejía un chaleco", "Pedro escuchaba historias"],
         "Una comparación une dos cosas con la palabra «como».", "«El viento soplaba como un lobo hambriento» compara el viento con un lobo usando «como».", texto=A)
    b.om(2, "«Las nubes corrían apuradas» es una personificación porque…", "da a las nubes una acción propia de las personas",
         ["compara las nubes con algo usando «como»", "describe el color de las nubes", "cuenta cuántas nubes había"],
         "¿Quiénes suelen correr apurados?", "Correr apurado es algo que hacen las personas: se le atribuye a las nubes, por eso es personificación.", texto=A)
    b.cat(2, "¿Qué lugares y costumbres muestra el texto?", ["Aparece en el texto", "No aparece"],
          [("casa de palafito", 0), ("tejer con lana junto al fogón", 0), ("contar historias de barcos", 0),
           ("volar volantines", 1), ("esquiar en la nieve", 1), ("bailar cueca en la plaza", 1)],
          "Relee qué hace la abuela y dónde viven.", "El texto muestra el palafito, el tejido junto al fogón y las historias de barcos; lo demás no aparece.", texto=A)

    B = ("Martina llegó corriendo al colegio, roja como un tomate. Había olvidado su disertación en la micro. "
         "Su profesora le sonrió y le dijo que podía presentarla al día siguiente. Martina respiró aliviada y se sentó.")
    b.om(1, "¿Con qué se compara a Martina?", "con un tomate", ["con una micro", "con su profesora", "con una disertación"],
         "Busca la palabra «como».", "Dice que llegó «roja como un tomate».", texto=B)
    b.om(2, "¿Cómo reaccionó Martina cuando la profesora le dio otro día?", "se sintió aliviada",
         ["se enojó con la profesora", "se puso a llorar", "salió corriendo de la sala"],
         "Lee la última oración.", "El texto dice que «respiró aliviada»: se le pasó la preocupación.", texto=B)
    b.om(3, "¿Qué consecuencia tuvo que Martina olvidara su disertación?", "la presentará al día siguiente",
         ["la profesora la retó", "se sacó un uno", "perdió la micro de vuelta"],
         "¿Qué decidió la profesora?", "Como no tenía su disertación, la profesora le permitió presentarla al día siguiente.", texto=B)

    C = ("Vicente rompió sin querer el macetero de su vecina, doña Elena. Pensó en esconderse, pero tocó el timbre y le contó lo ocurrido. "
         "Doña Elena, en vez de retarlo, le pidió ayuda para plantar el cardenal en otro macetero. "
         "Desde ese día, Vicente la visita cada sábado para regar juntos el jardín.")
    b.om(3, "¿Qué actitud muestra Vicente al tocar el timbre?", "honestidad", ["cobardía", "indiferencia", "orgullo"],
         "Pensó en esconderse, pero ¿qué hizo finalmente?", "En vez de esconderse, contó lo que pasó: actuó con honestidad.", texto=C)
    b.ord(3, "Ordena los hechos del relato.",
          ["Vicente rompe el macetero.", "Piensa en esconderse.", "Le cuenta a doña Elena.", "Plantan juntos el cardenal.", "La visita cada sábado."],
          "Sigue el orden en que aparecen en el texto.", "Rompe el macetero, piensa en esconderse, lo cuenta, plantan el cardenal y luego la visita los sábados.", texto=C)
    b.om(4, "¿Qué consecuencia tuvo la honestidad de Vicente?", "se hizo amigo de doña Elena",
         ["doña Elena lo retó", "tuvo que pagar el macetero", "dejó de visitar a su vecina"],
         "Fíjate en lo que pasa «desde ese día».", "Por contar la verdad, terminó visitando a doña Elena cada sábado: se hicieron amigos.", texto=C)

    D = ("En la pampa, el sol mordía la piel de los mineros. El viejo campamento dormía bajo el polvo, y solo la campana de la oficina salitrera "
         "despertaba a las familias al amanecer. Los domingos, todos se reunían en la plaza para escuchar a la banda del pueblo.")
    b.em(4, "Une cada expresión del texto con lo que quiere decir.",
         [["el sol mordía la piel", "el sol quemaba con fuerza"], ["el campamento dormía bajo el polvo", "el lugar estaba quieto y polvoriento"],
          ["la campana despertaba a las familias", "la campana marcaba el inicio del día"]],
         "Piensa qué significa cada expresión en la vida real.", "El sol «mordía» porque quemaba, el campamento «dormía» porque estaba quieto, y la campana anunciaba el día.", texto=D)
    b.cat(4, "¿Describe el ambiente físico o una costumbre?", ["Ambiente físico", "Costumbre"],
          [("el sol fuerte de la pampa", 0), ("el polvo sobre el campamento", 0), ("el paisaje de la pampa", 0),
           ("despertar con la campana", 1), ("reunirse los domingos en la plaza", 1), ("escuchar a la banda del pueblo", 1)],
          "Una costumbre es algo que la gente hace habitualmente.", "El sol, el polvo y la pampa son el ambiente; la campana, la plaza y la banda son costumbres.", texto=D)
    b.om(5, "¿Por qué se dice que el sol «mordía» la piel?", "para mostrar que el calor era intenso y dañino",
         ["porque el sol era un animal", "para indicar que era de noche", "para mostrar que los mineros tenían hambre"],
         "Piensa qué se siente cuando algo muerde.", "Es una personificación: el sol hace daño como una mordida, porque el calor era muy fuerte.", texto=D)

    E = ("Cuando anunciaron que Josefa iría al campeonato regional de ajedrez, Amanda dejó de hablarle. Toda la semana caminó sola en los recreos. "
         "El día del torneo, sin embargo, apareció con un cartel que decía: «¡Fuerza, Josefa!». Josefa ganó la primera partida y corrió a abrazarla.")
    b.om(5, "¿Qué sentía probablemente Amanda al comienzo?", "envidia", ["alegría", "miedo al ajedrez", "aburrimiento"],
         "¿Por qué dejaría de hablarle justo cuando Josefa fue elegida?", "Dejó de hablarle cuando eligieron a Josefa: sentía envidia.", texto=E)
    b.om(5, "¿Qué muestra el cartel sobre Amanda?", "que superó su envidia y decidió apoyar a su amiga",
         ["que seguía enojada con Josefa", "que quería jugar en lugar de Josefa", "que el profesor la obligó a llevarlo"],
         "Compara lo que hizo al inicio con lo que hizo el día del torneo.", "Al final apoya a Josefa con un cartel: cambió su actitud y dejó atrás la envidia.", texto=E)

    F = ("La casa de mis abuelos en Valparaíso es pequeña como una caja de fósforos, pero está pintada de colores. "
         "Desde la ventana, los cerros parecen escaleras gigantes que bajan hasta el mar, y los ascensores suben y bajan como hormigas trabajadoras.")
    b.co(1, "La casa de los abuelos es pequeña como ___.", "una caja de fósforos", ["una escalera gigante", "una hormiga", "un ascensor"],
         "Busca lo que viene después de «pequeña como».", "La casa es «pequeña como una caja de fósforos».", texto=F)
    b.em(2, "Une cada elemento con aquello con lo que se compara.",
         [["la casa", "una caja de fósforos"], ["los cerros", "escaleras gigantes"], ["los ascensores", "hormigas trabajadoras"]],
         "Busca «como» y «parecen».", "La casa es como una caja de fósforos, los cerros parecen escaleras y los ascensores son como hormigas.", texto=F)
    b.nu(3, "¿Cuántas comparaciones hay en el texto?", 3,
         "Busca «como» y también «parecen».", "Hay 3: la casa como una caja de fósforos, los cerros parecen escaleras y los ascensores como hormigas.",
         unidad="comparaciones", texto=F)
    return b.items


def le05_oa12():
    b = Autor("len", 5, 12)
    A = ("El pudú es un ciervo diminuto: mide apenas cuarenta centímetros de alto, menos que un perro mediano. "
         "Vive escondido en los bosques húmedos del sur de Chile.")
    b.om(1, "Según el texto, ¿qué significa «diminuto»?", "muy pequeño", ["muy rápido", "muy grande", "muy peludo"],
         "Lee lo que viene después de los dos puntos.", "Mide apenas cuarenta centímetros: «diminuto» significa muy pequeño.", texto=A)
    b.om(2, "¿Qué parte del texto es la clave para entender «diminuto»?", "«mide apenas cuarenta centímetros de alto»",
         ["«vive escondido»", "«en los bosques húmedos»", "«del sur de Chile»"],
         "Busca la parte que habla del tamaño.", "La medida del pudú explica la palabra: es una clave de contexto.", texto=A)

    B = ("Benjamín desarmó su bicicleta para limpiarla. Al terminar, intentó rearmarla, pero le sobraron dos tornillos. "
         "Le pareció increíble. Su hermana, que es ciclista, le explicó que eran del timbre.")
    b.co(1, "«Rearmar» significa armar ___.", "otra vez", ["antes", "mal", "sin ayuda"],
         "Piensa en «releer» o «rehacer».", "El prefijo re- significa «otra vez»: rearmar es volver a armar.", texto=B)
    b.em(2, "Une cada prefijo del texto con su significado.", [["des- (desarmar)", "acción contraria"], ["re- (rearmar)", "otra vez"], ["in- (increíble)", "no"]],
         "Piensa en «deshacer», «repetir» e «inútil».", "des- indica lo contrario, re- repetición e in- negación.", texto=B)
    b.om(3, "¿Qué significa «increíble» en el texto?", "que no se puede creer", ["que se cree otra vez", "que se cree antes", "que se cree con facilidad"],
         "Separa la palabra: in- + creíble.", "in- significa «no»: increíble es algo que no se puede creer.", texto=B)

    C = ("En la caleta de Tongoy, el panadero abre su local muy temprano. Saluda amablemente a los pescadores, que le compran pancitos calientes. "
         "Dice que su felicidad es verlos desayunar contentos.")
    b.em(3, "Une cada palabra del texto con lo que indica su sufijo.",
         [["panadero", "oficio: el que hace pan"], ["pancitos", "tamaño pequeño o cariño"], ["amablemente", "de manera amable"], ["felicidad", "cualidad de ser feliz"]],
         "Fíjate en el final de cada palabra: -ero, -ito, -mente, -dad.", "-ero indica oficio, -ito tamaño o cariño, -mente modo y -dad cualidad.", texto=C)
    b.om(3, "Si el panadero hace pan, ¿qué hace un «carpintero»?", "trabaja la madera", ["vende carpas", "arregla zapatos", "maneja camiones"],
         "El sufijo -ero indica oficio; ¿qué material usa?", "-ero indica oficio: el carpintero trabaja la madera.", texto=C)

    D = ("Al llegar a la cima del cerro, Sofía se sentó a descansar. El viento soplaba fuerte y la vista era espectacular: "
         "se veía todo Santiago y, al fondo, la cordillera nevada.")
    b.om(1, "¿Qué significa «cima» en el texto?", "la parte más alta", ["la parte más baja", "un camino de tierra", "una casa en el cerro"],
         "Sofía llegó y desde ahí veía toda la ciudad.", "Desde la cima se ve todo: es la parte más alta del cerro.", texto=D)
    b.om(3, "Sofía no conoce la palabra «cordillera» y el texto no da pistas. ¿Qué estrategia le dará el significado más preciso?",
         "buscarla en un diccionario", ["adivinarla por su primera letra", "contar sus sílabas", "saltarse la palabra"],
         "Cuando el contexto no ayuda, ¿dónde se explican las palabras?", "Si el contexto no basta, conviene consultar un diccionario (o preguntar a alguien que sepa).", texto=D)

    E = ("banco. 1. Asiento largo donde caben varias personas. 2. Empresa que guarda y presta dinero. "
         "3. Grupo grande de peces que nadan juntos.")
    b.co(2, "En «Nos sentamos en un banco de la plaza», «banco» tiene el significado número ___.", "1", ["2", "3", "4"],
         "¿Qué hay en una plaza para sentarse?", "En la plaza, el banco es un asiento: significado 1.", texto=E)
    b.nu(4, "¿Qué número de significado corresponde a «Desde el bote vimos un banco de jureles»?", 3,
         "Los jureles son peces.", "Un banco de jureles es un grupo de peces: significado 3.", texto=E)

    F = ("Después de tres días sin agua, las plantas del jardín estaban mustias: sus hojas colgaban sin fuerza y habían perdido su verde brillante. "
         "La abuela las regó con cuidado y, al día siguiente, lucían lozanas otra vez.")
    b.om(4, "¿Qué significa «mustias»?", "marchitas, sin fuerza", ["mojadas", "recién plantadas", "llenas de flores"],
         "Lee lo que viene después de los dos puntos.", "Las hojas colgaban sin fuerza y sin color: «mustias» significa marchitas.", texto=F)
    b.om(5, "Según el contexto, ¿qué significa «lozanas»?", "frescas y sanas", ["secas y débiles", "cortadas", "pequeñas"],
         "Es lo contrario de cómo estaban antes de regarlas.", "Después del riego se recuperaron: «lozanas» significa frescas y sanas, lo opuesto a mustias.", texto=F)
    b.cat(5, "¿Qué expresiones del texto ayudan a entender «mustias»?", ["Ayuda", "No ayuda"],
          [("tres días sin agua", 0), ("colgaban sin fuerza", 0), ("habían perdido su verde brillante", 0), ("la abuela", 1), ("con cuidado", 1)],
          "Busca las que describen cómo estaban las plantas.", "La falta de agua, las hojas sin fuerza y la pérdida de color son las claves de contexto.", texto=F)

    b.co(4, "Si «historia» es el tiempo con registros escritos, la «prehistoria» es el período ___ a la escritura.", "anterior", ["posterior", "igual", "contrario"],
         "¿Qué significa pre- en «prever» o «preparar»?", "pre- significa «antes»: la prehistoria es anterior a la escritura.")
    b.om(5, "«La deslealtad del capitán sorprendió a la tripulación». ¿Qué significa «deslealtad»?", "falta de lealtad",
         ["exceso de lealtad", "lealtad repetida", "persona muy leal"],
         "Separa: des- + leal + -tad. ¿Qué indica des-?", "des- indica lo contrario y -tad una cualidad: deslealtad es la falta de lealtad.")
    return b.items


def le05_oa21():
    b = Autor("len", 5, 21)
    b.co(1, "Presente. Yo ___ (cantar) en el coro del colegio.", "canto", ["canté", "cantaba", "cantaré"],
         "El presente indica lo que ocurre ahora o habitualmente.", "Presente de «cantar» con yo: canto.")
    b.om(1, "¿En qué tiempo está «comeremos»?", "futuro", ["presente", "pretérito", "copretérito"],
         "Piensa si la acción ya pasó, pasa o pasará.", "«Comeremos» es una acción que aún no ocurre: futuro.")
    b.cat(1, "¿En qué termina cada verbo en infinitivo?", ["-ar", "-er", "-ir"],
          [("saltar", 0), ("bailar", 0), ("correr", 1), ("beber", 1), ("vivir", 2), ("escribir", 2)],
          "Mira las dos últimas letras.", "saltar y bailar terminan en -ar; correr y beber en -er; vivir y escribir en -ir.")
    b.co(2, "Pretérito. Ayer nosotros ___ (correr) en el parque.", "corrimos", ["corremos", "corríamos", "correremos"],
         "El pretérito cuenta una acción terminada en el pasado.", "Pretérito de «correr» con nosotros: corrimos.")
    b.em(2, "Une cada forma de «bailar» con su tiempo.", [["bailo", "presente"], ["bailé", "pretérito"], ["bailaba", "copretérito"], ["bailaré", "futuro"]],
         "-é es una acción terminada; -aba, una acción que duraba en el pasado.", "bailo: presente; bailé: pretérito; bailaba: copretérito; bailaré: futuro.")
    b.co(2, "Futuro. Mañana tú ___ (escribir) la carta.", "escribirás", ["escribiste", "escribías", "escribes"],
         "El futuro de tú termina en -ás.", "Futuro de «escribir» con tú: escribirás.")
    b.co(3, "Cuando era pequeña, Sofía ___ (vivir) en Arica.", "vivía", ["vive", "vivirá", "vivo"],
         "«Cuando era pequeña» habla de algo que duraba en el pasado.", "Para una situación que duraba en el pasado se usa el copretérito: vivía.")
    b.cat(3, "¿Pasado, presente o futuro?", ["Pasado", "Presente", "Futuro"],
          [("aprendí", 0), ("leían", 0), ("subes", 1), ("comprendemos", 1), ("abrirán", 2), ("venderé", 2)],
          "Fíjate en las terminaciones: -í, -ían, -rán, -ré…", "aprendí y leían son pasado; subes y comprendemos, presente; abrirán y venderé, futuro.")
    b.om(3, "¿Qué oración tiene el verbo bien conjugado?", "Ellos bebieron jugo en el almuerzo.",
         ["Ellos bebimos jugo en el almuerzo.", "Ellos bebió jugo en el almuerzo.", "Ellos bebiste jugo en el almuerzo."],
         "El verbo debe concordar con «ellos».", "Con ellos, el pretérito de «beber» es bebieron.")
    b.co(3, "Ayer {personaje} ___ (guardar) {los_objetos} en {el_contenedor}.", "guardó", ["guarda", "guardará", "guardé"],
         "«Ayer» indica una acción terminada; el sujeto es una sola persona que no eres tú.", "Pretérito de «guardar» con él o ella: guardó.")
    b.co(4, "El año pasado mis primos ___ (viajar) a Chiloé.", "viajaron", ["viajan", "viajarán", "viajamos"],
         "Revisa el tiempo («el año pasado») y quién viaja.", "Acción terminada y sujeto «mis primos» (ellos): viajaron.")
    b.co(4, "Mientras mamá ___ (barrer) el patio, yo regaba las plantas.", "barría", ["barrerá", "barremos", "barrieron"],
         "Las dos acciones ocurrían al mismo tiempo en el pasado.", "Con «regaba», la otra acción simultánea va en copretérito: barría.")
    b.em(4, "Une cada persona con la forma de «partir» en pretérito.",
         [["yo", "partí"], ["tú", "partiste"], ["ella", "partió"], ["nosotros", "partimos"], ["ellos", "partieron"]],
         "Piensa en «viví, viviste, vivió…».", "partí, partiste, partió, partimos, partieron.")
    b.om(5, "¿Qué oración tiene un verbo mal conjugado?", "Ayer tú comistes empanadas en la once.",
         ["Ayer comimos empanadas en la once.", "Mañana comeremos empanadas en la once.", "Antes comíamos empanadas en la once."],
         "Revisa la forma de tú en pretérito.", "Con tú, el pretérito es «comiste», sin s final: «comistes» es un error.")
    b.co(5, "El próximo verano, Tomás y Amanda ___ (recorrer) el desierto de Atacama.", "recorrerán", ["recorrieron", "recorrerá", "recorrían"],
         "Fíjate en cuándo ocurre y en cuántas personas lo hacen.", "Es futuro y el sujeto es plural (ellos): recorrerán.")
    b.nu(5, "¿Cuántos verbos en copretérito hay? «Cuando vivía en Valdivia, caminaba por la costanera y miraba los botes. Un día subí a uno.»", 3,
         "El copretérito de -ar termina en -aba; el de -er e -ir, en -ía.", "vivía, caminaba y miraba están en copretérito; «subí» está en pretérito.", unidad="verbos")
    b.co(5, "Si mañana llueve, nosotros ___ (suspender) el paseo.", "suspenderemos", ["suspendimos", "suspendíamos", "suspendieron"],
         "La acción depende de algo que pasará mañana.", "Es una acción futura con nosotros: suspenderemos.")
    return b.items


GENERADORES = {
    "5_basico.lenguaje.OA4": le05_oa4,
    "5_basico.lenguaje.OA12": le05_oa12,
    "5_basico.lenguaje.OA21": le05_oa21,
}
