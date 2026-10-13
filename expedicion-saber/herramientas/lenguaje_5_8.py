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


def le05_oa22():
    b = Autor("len", 5, 22)
    b.co(1, "Un lápiz, dos ___.", "lápices", ["lápizes", "lápises", "lapices"],
         "Las palabras terminadas en z forman el plural con -ces.", "lápiz → lápices: la z cambia a c y conserva la tilde.")
    b.om(1, "¿Cuál está bien escrita?", "pingüino", ["pinguino", "pingüíno", "pinhuino"],
         "Se pronuncia la u entre la g y la i.", "Se escribe «pingüino»: la diéresis (ü) indica que la u suena.")
    b.om(1, "¿Qué signo indica, en un diálogo, que habla un personaje?", "la raya (—)", ["el punto (.)", "el paréntesis ( )", "el asterisco (*)"],
         "Es una línea horizontal larga al inicio de lo que dice el personaje.", "La raya (—) marca la intervención de cada personaje en un diálogo.")
    b.cat(2, "¿Bien escrita o mal escrita?", ["Bien escrita", "Mal escrita"],
          [("vergüenza", 0), ("paragüero", 0), ("guitarra", 0), ("pinguino", 1), ("cigueña", 1), ("güitarra", 1)],
          "La ü se usa solo cuando la u suena entre g y e o i.", "vergüenza, paragüero y guitarra están bien; se escribe pingüino, cigüeña y guitarra (sin diéresis, porque la u no suena).")
    b.co(2, "Ellas son muy ___ (capaz) de lograrlo.", "capaces", ["capazes", "capases", "capaz"],
         "Plural de una palabra terminada en z.", "capaz → capaces: la z cambia a c antes de -es.")
    b.co(2, "¿Quieres un ___ o un café?", "té", ["te", "tea", "tee"],
         "Es la bebida, no el pronombre.", "La bebida lleva tilde diacrítica: té. Sin tilde, «te» es pronombre (te quiero).")
    b.co(3, "La confi___ entre amigos es importante.", "anza", ["ansa", "asa", "ancia"],
         "Piensa en «esperanza» y «enseñanza».", "Los sustantivos con el sufijo -anza se escriben con z: confianza.")
    b.cat(3, "¿Bien escrita o mal escrita?", ["Bien escrita", "Mal escrita"],
          [("belleza", 0), ("rapidez", 0), ("tristeza", 0), ("niñes", 1), ("pobresa", 1), ("vejes", 1)],
          "Los sustantivos abstractos terminados en -ez y -eza se escriben con z.", "Se escribe niñez, pobreza y vejez, con z, como belleza, rapidez y tristeza.")
    b.co(3, "A ___ me gusta el pastel de choclo.", "mí", ["mi", "me", "mío"],
         "Después de «a», es el pronombre de la persona que habla.", "«Mí» con tilde es pronombre (a mí); «mi» sin tilde es posesivo (mi casa).")
    b.cat(4, "¿La palabra derivada termina en -ción o en -sión?", ["-ción", "-sión"],
          [("educado → educa…", 0), ("atento → aten…", 0), ("redactor → redac…", 0), ("confuso → confu…", 1), ("decisivo → deci…", 1), ("televisor → televi…", 1)],
          "Si la palabra base termina en -do, -to o -tor, usa -ción; si termina en -so, -sor o -sivo, usa -sión.",
          "educación, atención y redacción llevan -ción; confusión, decisión y televisión, -sión.")
    b.om(4, "¿Qué diálogo está bien escrito?", "—¿Vienes a jugar? —preguntó Diego.",
         ["¿Vienes a jugar? —preguntó Diego.", "—¿Vienes a jugar?, preguntó Diego.", "—¿Vienes a jugar? preguntó Diego—."],
         "Va una raya al inicio de lo que dice el personaje y otra antes de lo que aclara el narrador.", "Se abre con raya y el comentario del narrador también va tras una raya: —¿Vienes a jugar? —preguntó Diego.")
    b.om(4, "¿Qué oración usa bien las comas?", "Valparaíso, la ciudad de los cerros, está junto al mar.",
         ["Valparaíso la ciudad de los cerros, está junto al mar.", "Valparaíso, la ciudad de los cerros está junto al mar.", "Valparaíso la ciudad, de los cerros está junto al mar."],
         "Una frase explicativa va entre dos comas.", "«la ciudad de los cerros» explica qué es Valparaíso: va entre dos comas.")
    b.em(4, "Une cada palabra con su uso.",
         [["tú", "pronombre (tú cantas)"], ["tu", "posesivo (tu casa)"], ["sí", "afirmación (sí, quiero)"], ["si", "condición (si llueve…)"]],
         "La tilde diacrítica distingue palabras que se escriben igual.", "tú y sí con tilde son pronombre y afirmación; tu y si sin tilde son posesivo y condición.")
    b.co(5, "—Mañana iremos a Chiloé ___dijo mamá—. Lleven ropa de lluvia.", "—", [",", ":", "«"],
         "Lo que aclara el narrador dentro de un diálogo va entre rayas.", "El inciso del narrador se abre con raya: «—Mañana iremos a Chiloé —dijo mamá—».")
    b.om(5, "¿Qué oración está escrita sin errores?", "Si tú quieres, mañana te invito un té.",
         ["Sí tu quieres, mañana té invito un te.", "Si tu quieres, mañana te invito un té.", "Si tú quieres, mañana té invito un té."],
         "Revisa cada palabra: si, tú, te y té.", "«Si» es condición, «tú» pronombre, «te» pronombre y «té» la bebida.")
    b.nu(5, "¿Cuántas comas faltan? «El huemul animal de nuestro escudo vive en el sur.»", 2,
         "Busca la frase que explica qué es el huemul.", "Faltan 2: El huemul, animal de nuestro escudo, vive en el sur.", unidad="comas")
    b.cat(5, "¿Qué letra va en el espacio?", ["c", "s", "z"],
          [("lu_es (plural de luz)", 0), ("can_ión (de cantar)", 0), ("confu_ión (de confuso)", 1), ("pa_ito (de paso)", 1), ("rique_a", 2), ("timide_", 2)],
          "Piensa en la palabra de origen y en las terminaciones -eza y -ez.", "luces y canción con c; confusión y pasito con s (vienen de confuso y paso); riqueza y timidez con z.")
    return b.items


def le06_oa4():
    b = Autor("len", 6, 4)
    A = ("Diego miraba el mar desde el muelle de Caldera. Las olas eran caballos blancos que galopaban hacia la playa. "
         "Su papá, pescador, aún no regresaba, y el cielo se volvía gris como el plomo.")
    b.co(1, "El cielo se volvía gris como ___.", "el plomo", ["caballos blancos", "el mar", "la playa"],
         "Busca la comparación con «como» al final.", "El cielo se compara con el plomo: «gris como el plomo».", texto=A)
    b.om(2, "«Las olas eran caballos blancos» es una…", "metáfora", ["comparación", "personificación", "rima"],
         "Identifica las olas con caballos sin usar «como».", "Dice que las olas «eran» caballos, sin «como»: es una metáfora.", texto=A)
    b.om(3, "¿Qué sensación crea el ambiente del relato?", "preocupación, porque el papá no vuelve y el cielo se oscurece",
         ["alegría, porque es un día de playa", "aburrimiento, porque no pasa nada", "calma, porque el mar está quieto"],
         "Fíjate en el cielo gris y en que el papá no regresa.", "El cielo que se oscurece y el papá que no vuelve crean un ambiente de preocupación.", texto=A)

    B = ("Antonia quería ganar la feria científica. Durante semanas construyó un pequeño molino que generaba electricidad con el viento. "
         "El día de la feria, el molino no giró: no había viento en el gimnasio. "
         "Antonia pidió prestado un abanico, lo agitó frente a las aspas y la ampolleta se encendió entre aplausos.")
    b.ord(2, "Ordena las acciones principales.",
          ["Antonia quiere ganar la feria.", "Construye un molino de viento.", "El molino no gira en el gimnasio.", "Agita un abanico frente a las aspas.", "La ampolleta se enciende."],
          "Sigue el orden de la historia: meta, problema y solución.", "Primero la meta y el molino, luego el problema y al final la solución con el abanico.", texto=B)
    b.om(3, "¿Qué acción resuelve el problema de la historia?", "Antonia agita un abanico frente al molino",
         ["Antonia construye el molino", "el público aplaude", "Antonia decide participar en la feria"],
         "El problema era que no había viento.", "El abanico reemplaza al viento y hace girar el molino: esa acción resuelve el problema.", texto=B)
    b.om(4, "¿Qué muestra la reacción de Antonia ante el problema?", "que es ingeniosa y no se rinde",
         ["que es descuidada con su trabajo", "que prefiere que otros resuelvan sus problemas", "que no le importaba ganar"],
         "¿Qué hizo cuando el molino no giró?", "Buscó rápido una solución con el abanico: es ingeniosa y persistente.", texto=B)

    C = ("Benjamín guardaba cada moneda en un tarro. No compraba dulces ni láminas, aunque sus amigos se burlaban de él. "
         "En diciembre rompió el tarro y fue a la librería. Compró una caja de lápices de colores y la envolvió con cuidado: "
         "su hermana menor nunca había tenido una.")
    b.om(3, "¿Para qué ahorraba Benjamín?", "para hacerle un regalo a su hermana", ["para comprar dulces", "porque sus amigos se lo pidieron", "para comprarse láminas"],
         "Lee el final: ¿para quién eran los lápices?", "Envolvió los lápices para su hermana, que nunca había tenido una caja: ahorraba para regalárselos.", texto=C)
    b.om(4, "¿Por qué Benjamín soportaba las burlas de sus amigos?", "porque su meta de alegrar a su hermana era más importante para él",
         ["porque no escuchaba a sus amigos", "porque quería que lo admiraran", "porque no le gustaban los dulces"],
         "Piensa en su motivación.", "Su motivación, regalarle algo a su hermana, pesaba más que las burlas.", texto=C)
    b.om(5, "¿Qué enseñanza deja el relato?", "la generosidad a veces exige esfuerzo y sacrificio",
         ["hay que gastar el dinero apenas se tiene", "las burlas de los amigos siempre tienen razón", "los regalos caros son los mejores"],
         "¿Qué tuvo que dejar de lado Benjamín para lograr su regalo?", "Benjamín renunció a dulces y láminas y soportó burlas para regalar: ser generoso le costó esfuerzo.", texto=C)

    D = ("La niebla se tragó el camino del bosque. Los árboles estiraban sus ramas como brazos que querían atrapar a Clara. "
         "Ella apretó la linterna y siguió el ladrido de su perro, que la esperaba en la tranquera de la casa.")
    b.co(1, "En el texto, las ramas de los árboles se comparan con ___.", "brazos", ["linternas", "la niebla", "perros"],
         "Busca la palabra «como».", "«Estiraban sus ramas como brazos»: las ramas se comparan con brazos.", texto=D)
    b.cat(4, "Clasifica cada expresión.", ["Personificación", "Comparación", "Metáfora"],
          [("La niebla se tragó el camino.", 0), ("El viento silbaba enojado.", 0), ("Ramas como brazos.", 1), ("Rápido como un rayo.", 1),
           ("La luna era una moneda de plata.", 2), ("Sus ojos eran dos luceros.", 2)],
          "Comparación usa «como»; metáfora identifica sin «como»; personificación da rasgos humanos.",
          "Tragar y silbar enojado son acciones humanas; «como» marca comparaciones; «era/eran» sin «como» forma metáforas.", texto=D)
    b.om(5, "¿Cómo se relaciona el ambiente con lo que vive Clara?", "la niebla y el bosque oscuro hacen difícil el camino y aumentan su miedo",
         ["el bosque soleado la hace sentir tranquila", "el ambiente no tiene relación con lo que le pasa", "la niebla la ayuda a encontrar la casa"],
         "¿Qué siente alguien que no ve el camino y cree que los árboles lo quieren atrapar?", "La niebla tapa el camino y los árboles parecen amenazarla: el ambiente crea el problema y el miedo de Clara.", texto=D)

    E = ("Mi abuelo es un roble: lleva setenta inviernos en el campo de Curicó y nunca ha dejado de trabajar la tierra. "
         "Este año la sequía secó su huerto, pero él cavó un pozo con sus propias manos. "
         "«La tierra no abandona a quien la cuida», me dijo sonriendo.")
    b.em(4, "Une cada expresión del texto con su significado.",
         [["es un roble", "es fuerte y resistente"], ["setenta inviernos", "setenta años"], ["con sus propias manos", "con su propio esfuerzo"]],
         "Piensa en el sentido figurado de cada expresión.", "Roble: fortaleza; inviernos: años; con sus propias manos: con su propio esfuerzo.", texto=E)
    b.om(5, "¿Qué motiva al abuelo a cavar el pozo?", "su amor por la tierra y su decisión de no rendirse",
         ["el miedo a la sequía lo hizo vender el campo", "su nieto se lo ordenó", "quería buscar un tesoro"],
         "Relee la frase que dice al final.", "Él cree que «la tierra no abandona a quien la cuida»: lo mueve su amor por la tierra y su perseverancia.", texto=E)

    F = ("El reloj de la plaza de Talca tosía cada hora. Los vecinos decían que estaba viejo y cansado, pero nadie quería cambiarlo: "
         "sus campanadas eran parte del pueblo, como el olor a pan de la mañana.")
    b.om(1, "¿Qué recurso es «el reloj tosía cada hora»?", "personificación", ["comparación", "metáfora", "onomatopeya"],
         "¿Quiénes tosen normalmente?", "Toser es propio de seres vivos: se le atribuye al reloj, por eso es personificación.", texto=F)
    b.om(2, "¿Por qué los vecinos no querían cambiar el reloj?", "porque sus campanadas eran parte de la vida del pueblo",
         ["porque era nuevo", "porque no tenían dinero", "porque nunca se atrasaba"],
         "Lee lo que viene después de los dos puntos.", "Sus campanadas eran parte del pueblo, como el olor a pan: lo querían tal como era.", texto=F)
    return b.items


def le06_oa21():
    b = Autor("len", 6, 21)
    b.co(1, "La ventana está ___ (romper).", "rota", ["rompida", "rompada", "roto"],
         "«Romper» tiene un participio irregular y debe concordar con «la ventana».", "El participio de romper es roto; con «la ventana», rota.")
    b.em(1, "Une cada verbo con su participio.", [["abrir", "abierto"], ["escribir", "escrito"], ["hacer", "hecho"], ["ver", "visto"]],
         "Ninguno termina en -ado ni en -ido.", "abrir → abierto, escribir → escrito, hacer → hecho, ver → visto.")
    b.om(1, "¿Cuál es el participio de «decir»?", "dicho", ["decido", "dicido", "decidido"],
         "Piensa en «lo dicho, dicho está».", "El participio de decir es dicho.")
    b.co(2, "Ya he ___ la tarea de Lenguaje.", "hecho", ["hacido", "echo", "hacho"],
         "Es el participio de «hacer» y lleva h.", "El participio de hacer es «hecho», con h; «echo» es del verbo echar.")
    b.cat(2, "¿Participio correcto o incorrecto?", ["Correcto", "Incorrecto"],
          [("vuelto", 0), ("puesto", 0), ("cubierto", 0), ("volvido", 1), ("ponido", 1), ("cubrido", 1)],
          "Volver, poner y cubrir tienen participios irregulares.", "Lo correcto es vuelto, puesto y cubierto; volvido, ponido y cubrido son errores.")
    b.co(2, "¿Has ___ mi cuaderno? Lo dejé sobre la mesa.", "visto", ["vido", "veído", "vito"],
         "Es el participio irregular de «ver».", "El participio de ver es visto: «¿Has visto…?».")
    b.co(3, "La carta fue ___ a mano.", "escrita", ["escribida", "escrito", "escribita"],
         "Usa el participio de «escribir» y concuerda con «la carta».", "Escribir → escrito; con «la carta», escrita.")
    b.co(3, "Me encantan las papas ___ (freír).", "fritas", ["frías", "fridas", "fritos"],
         "Concuerda con «las papas».", "Como adjetivo, el participio de freír es frito: las papas fritas.")
    b.cat(3, "¿Participio regular o irregular?", ["Regular (-ado, -ido)", "Irregular"],
          [("cantado", 0), ("comido", 0), ("vivido", 0), ("muerto", 1), ("resuelto", 1), ("puesto", 1)],
          "Los regulares terminan en -ado o -ido.", "cantado, comido y vivido son regulares; muerto, resuelto y puesto, irregulares.")
    b.co(3, "{personaje} ha ___ (volver) de {lugar} con {los_objetos}.", "vuelto", ["volvido", "vuelvido", "volvió"],
         "Después de «ha» va un participio.", "El participio de volver es vuelto: «ha vuelto».")
    b.co(4, "El profesor ha ___ (resolver) todas nuestras dudas.", "resuelto", ["resolvido", "resolvado", "resuelvido"],
         "Se parece a vuelto (de volver).", "El participio de resolver es resuelto.")
    b.co(4, "Las montañas estaban ___ (cubrir) de nieve.", "cubiertas", ["cubridas", "cubierto", "cubiertos"],
         "Participio irregular que concuerda con «las montañas».", "Cubrir → cubierto; con «las montañas», cubiertas.")
    b.om(4, "¿Qué oración tiene un error?", "Los niños han ponido la mesa.",
         ["Los niños han puesto la mesa.", "La mesa está puesta.", "Ya pusieron la mesa."],
         "Revisa el participio de «poner».", "El participio de poner es puesto: «han puesto», no «han ponido».")
    b.nu(4, "¿Cuántos participios irregulares hay? «He escrito una carta, he abierto la ventana y he cantado una canción.»", 2,
         "Los regulares terminan en -ado o -ido.", "escrito y abierto son irregulares; cantado es regular.", unidad="participios")
    b.om(5, "«Cuando llegué, el florero estaba rompido y nadie había dicho nada.» ¿Qué palabra está mal y cómo se corrige?", "rompido → roto",
         ["dicho → decido", "llegué → llegé", "estaba → estuvo"],
         "Busca un participio terminado en -ido que debería ser irregular.", "El participio de romper es roto: «estaba roto». «Dicho» está bien.")
    b.nu(5, "¿Cuántos participios están mal escritos? «Hemos hacido el mural, hemos escrito el título y hemos ponido la fecha.»", 2,
         "Revisa los participios de hacer, escribir y poner.", "Están mal hacido (hecho) y ponido (puesto); escrito está bien.", unidad="participios")
    b.cat(5, "¿Participio bien o mal usado?", ["Bien usado", "Mal usado"],
          [("La puerta está abierta.", 0), ("El cuento fue escrito por Josefa.", 0), ("Ya he impreso la guía.", 0),
           ("El pez está morido.", 1), ("Hemos devolvido los libros.", 1), ("La olla está descubrida.", 1)],
          "Los verbos derivados (devolver, descubrir) forman el participio como su verbo base.",
          "Lo correcto es muerto, devuelto (como vuelto) y descubierta (como cubierta).")
    return b.items


def le07_oa3():
    b = Autor("len", 7, 3)
    b.em(1, "Une cada tipo de narrador con su descripción.",
         [["protagonista", "cuenta su propia historia en primera persona"], ["testigo", "cuenta lo que vio que le pasó a otro"],
          ["omnisciente", "lo sabe todo, incluso lo que piensan los personajes"]],
         "Piensa en cuánto sabe cada narrador y de quién habla.", "El protagonista cuenta su historia; el testigo, la de otro; el omnisciente lo sabe todo.")
    b.co(1, "En un relato con orden ___, los hechos se cuentan en el mismo orden en que ocurrieron.", "lineal", ["retrospectivo", "inverso", "circular"],
         "Piensa en una línea recta del inicio al final.", "El orden lineal (o cronológico) sigue los hechos tal como ocurrieron.")

    A = ("Nunca olvidaré mi primer día en Punta Arenas. El viento me empujaba por la calle y yo, que venía de Iquique, "
         "no entendía cómo la gente caminaba tan tranquila. Esa tarde me compré mi primer gorro de lana.")
    b.om(1, "¿Qué tipo de narrador tiene este relato?", "protagonista", ["testigo", "omnisciente", "no tiene narrador"],
         "¿A quién le pasan los hechos que se cuentan?", "Quien narra cuenta lo que le pasó a sí mismo: es narrador protagonista.", texto=A)
    b.om(2, "¿Qué pista indica el tipo de narrador?", "cuenta en primera persona lo que le pasó a él mismo",
         ["usa la tercera persona", "conoce los pensamientos de todos los personajes", "cuenta lo que le pasó a un amigo"],
         "Fíjate en palabras como «me», «mi» y «yo».", "Usa la primera persona (me, mi, yo) para contar su propia experiencia: es protagonista.", texto=A)

    B = ("Yo estaba en la galería cuando Ignacio subió al escenario. Le temblaban las manos. Desde mi asiento vi cómo cerraba los ojos "
         "un segundo antes de tocar el violín. No sé qué pensó, pero cuando terminó, el teatro entero se puso de pie.")
    b.om(2, "¿Qué tipo de narrador tiene este relato?", "testigo", ["protagonista", "omnisciente", "Ignacio, en primera persona"],
         "¿El narrador cuenta su historia o la de otro?", "Narra en primera persona lo que vio que le pasó a Ignacio: es narrador testigo.", texto=B)
    b.om(3, "¿Qué frase demuestra que el narrador NO es omnisciente?", "«No sé qué pensó»",
         ["«Le temblaban las manos»", "«el teatro entero se puso de pie»", "«Ignacio subió al escenario»"],
         "Un narrador omnisciente conoce los pensamientos de los personajes.", "Si dice «No sé qué pensó», no conoce la mente de Ignacio: no es omnisciente.", texto=B)
    b.om(5, "Si Ignacio contara la historia como narrador protagonista, ¿qué frase podría aparecer?", "«Cerré los ojos y pensé en mi abuela.»",
         ["«No sé qué pensó Ignacio.»", "«Desde mi asiento vi a Ignacio.»", "«Ignacio subió al escenario.»"],
         "El protagonista cuenta en primera persona lo que él mismo hace y piensa.", "Solo Ignacio podría decir en primera persona lo que hizo y pensó: «Cerré los ojos y pensé…».", texto=B)

    C = ("Catalina sabía que su amiga Fernanda había copiado en la prueba. La profesora no lo sospechaba, y Fernanda, desde el banco de atrás, "
         "rezaba para que nadie hablara. Catalina se mordió el labio: si callaba, traicionaba lo que creía justo; si hablaba, perdía a su mejor amiga.")
    b.om(3, "¿Qué tipo de narrador tiene este relato?", "omnisciente", ["protagonista", "testigo", "Catalina, en primera persona"],
         "¿El narrador participa en la historia? ¿Qué sabe de los personajes?", "Narra en tercera persona y conoce lo que piensan varios personajes: es omnisciente.", texto=C)
    b.om(4, "¿Qué tipo de conflicto vive Catalina?", "consigo misma (conflicto interno)", ["con la naturaleza", "con la sociedad", "con la profesora"],
         "Su lucha ocurre dentro de ella: debe elegir entre dos cosas que valora.", "Catalina duda entre la justicia y la amistad: es un conflicto interno.", texto=C)
    b.om(4, "¿Qué muestra que el narrador es omnisciente?", "conoce lo que piensan y sienten Catalina y Fernanda",
         ["usa la primera persona", "solo describe lo que se ve desde afuera", "es un compañero de curso que observa"],
         "¿Cómo sabe el narrador lo que pasa por la mente de cada una?", "Sabe lo que sabe Catalina y lo que desea Fernanda: conoce el interior de los personajes.", texto=C)

    D = ("Al ver la vieja bicicleta en la bodega, don Héctor sonrió. Recordó aquel verano de 1975 en Pichilemu, cuando su padre le enseñó "
         "a pedalear por la costanera y él cayó tres veces antes de lograrlo. Ahora, con cuidado, infló las ruedas: era el turno de su nieta.")
    b.om(3, "¿Qué recurso temporal hay en «Recordó aquel verano de 1975…»?", "retrospección (flashback)",
         ["orden lineal", "anticipación de hechos futuros", "un diálogo entre personajes"],
         "La historia salta hacia atrás en el tiempo.", "Se interrumpe el presente para contar un hecho del pasado: es una retrospección.", texto=D)
    b.ord(5, "Ordena los hechos según cuándo ocurrieron (no según el orden del texto).",
          ["El padre le enseña a pedalear.", "Héctor se cae tres veces.", "Héctor logra pedalear.", "Héctor ve la bicicleta en la bodega.", "Infla las ruedas para su nieta."],
          "Lo que se recuerda ocurrió antes que lo que pasa en la bodega.", "Primero ocurre el verano de 1975 (enseñanza, caídas, logro) y después, años más tarde, la escena de la bodega.", texto=D)

    E = ("La lluvia caía sin parar sobre el campamento. —¡Hay que subir al cerro! —gritó Rodrigo. —Exageras, es solo un chubasco —respondió Matías. "
         "Nadie se movió. Una hora después, el río creció, cubrió las carpas y todos corrieron cuesta arriba.")
    b.om(2, "¿Qué signo marca en el texto que comienza a hablar un personaje?", "la raya (—)", ["el punto y coma (;)", "los paréntesis ( )", "los dos puntos (:)"],
         "Mira lo que aparece justo antes de «¡Hay que subir…».", "La raya introduce las palabras de cada personaje en el diálogo.", texto=E)
    b.om(3, "¿Qué conflicto principal enfrentan todos en el campamento?", "con la naturaleza: la crecida del río",
         ["consigo mismos: el miedo a la oscuridad", "con la sociedad: una ley injusta", "con un animal salvaje"],
         "¿Qué amenaza a todo el campamento?", "La lluvia y el río que crece amenazan a todos: es un conflicto con la naturaleza.", texto=E)
    b.cat(4, "¿Habla el narrador o un personaje?", ["Narrador", "Personaje"],
          [("La lluvia caía sin parar sobre el campamento.", 0), ("gritó Rodrigo", 0), ("respondió Matías", 0), ("Nadie se movió.", 0),
           ("¡Hay que subir al cerro!", 1), ("Exageras, es solo un chubasco", 1)],
          "Las palabras de los personajes van después de la raya; el narrador cuenta y aclara quién habla.",
          "El narrador cuenta los hechos y dice «gritó Rodrigo» y «respondió Matías»; los personajes dicen lo que va entre rayas.", texto=E)

    F = ("En el pueblo de Las Quilas, una vieja regla prohibía que las niñas jugaran fútbol en la cancha. Elena entrenaba sola al amanecer. "
         "Un día juntó firmas, habló en el consejo del pueblo y logró que la cancha fuera para todos.")
    b.om(4, "¿Qué tipo de conflicto enfrenta Elena?", "con la sociedad: una regla injusta del pueblo",
         ["con la naturaleza: el frío del amanecer", "consigo misma: su miedo a jugar", "con otro personaje: una rival del equipo"],
         "¿Qué le impide jugar en la cancha?", "Lo que se opone a Elena es una regla del pueblo: es un conflicto con la sociedad.", texto=F)
    b.om(5, "¿Cómo se resuelve el conflicto y qué muestra eso de Elena?", "se organiza y argumenta hasta cambiar la regla: es perseverante",
         ["se resuelve solo con el tiempo: Elena es pasiva", "abandona el fútbol: Elena es insegura", "el consejo la castiga: Elena es rebelde"],
         "Fíjate en lo que hizo «un día».", "Juntó firmas y habló en el consejo hasta lograr el cambio: es perseverante y luchadora.", texto=F)
    return b.items


def le07_oa4():
    b = Autor("len", 7, 4)
    A = ("Huele a sal la mañana en la caleta, / chillan las gaviotas sobre el muelle gris, / "
         "la arena tibia me acaricia los pies / y la tarde sabe a mote con huesillo.")
    b.om(1, "¿A qué sentido apela «chillan las gaviotas»?", "al oído", ["a la vista", "al olfato", "al gusto"],
         "¿Cómo percibes un chillido?", "Un chillido se escucha: es una imagen auditiva.", texto=A)
    b.em(2, "Une cada expresión con el sentido al que apela.",
         [["huele a sal la mañana", "olfato"], ["el muelle gris", "vista"], ["la arena tibia", "tacto"], ["sabe a mote con huesillo", "gusto"]],
         "Piensa con qué parte del cuerpo percibes cada cosa.", "Oler: olfato; un color: vista; la temperatura: tacto; un sabor: gusto.", texto=A)
    b.om(3, "Además de una imagen táctil, «la arena tibia me acaricia los pies» contiene una…", "personificación",
         ["hipérbole", "comparación", "aliteración"],
         "¿Quién suele acariciar?", "Acariciar es una acción humana atribuida a la arena: es una personificación.", texto=A)

    B = ("Tu risa es un cascabel de plata, / tus ojos, dos lagunas del sur; / "
         "caminas liviana como el humo / bajo un cielo de terciopelo azul.")
    b.om(1, "¿Qué recurso hay en «caminas liviana como el humo»?", "comparación", ["metáfora", "hipérbole", "aliteración"],
         "Busca la palabra que une los dos elementos.", "Usa «como» para relacionar a la persona con el humo: es una comparación.", texto=B)
    b.co(2, "«Tus ojos, dos lagunas del sur» es una ___, porque identifica los ojos con lagunas sin usar «como».", "metáfora",
         ["comparación", "personificación", "hipérbole"],
         "Es como una comparación, pero sin nexo.", "Identificar una cosa con otra sin «como» es una metáfora.", texto=B)

    C = ("Te esperé mil años en la estación, / lloré un río entero de pena, / "
         "y cuando al fin bajaste del tren / el mundo entero se puso a cantar.")
    b.om(2, "¿Qué recurso hay en «Te esperé mil años»?", "hipérbole", ["comparación", "metáfora", "personificación"],
         "¿Es posible esperar mil años?", "Es una exageración evidente: una hipérbole.", texto=C)
    b.om(3, "¿Qué efecto producen las exageraciones del poema?", "intensifican la emoción de la espera y del reencuentro",
         ["indican cuántos años pasaron exactamente", "describen el paisaje de la estación", "hacen que los versos rimen"],
         "¿Para qué exagera alguien al hablar de sus sentimientos?", "Las hipérboles agrandan los sentimientos: muestran cuánto sufrió y cuánto se alegró.", texto=C)
    b.nu(4, "¿Cuántas hipérboles hay en los dos primeros versos?", 2,
         "Busca exageraciones de tiempo y de cantidad.", "Hay 2: «mil años» y «un río entero de pena».", unidad="hipérboles", texto=C)

    D = "La lluvia golpea el tejado, / canta en la noche su canción; / el perro duerme a mi lado / y late lento mi corazón."
    b.co(1, "En el poema, «canción» rima con ___.", "corazón", ["tejado", "lado", "noche"],
         "Busca otra palabra al final de un verso que termine en -ón.", "canción y corazón terminan igual (-ón): riman.", texto=D)
    b.om(3, "¿Qué tipo de rima hay entre «tejado» y «lado»?", "consonante", ["asonante", "no riman", "aliteración"],
         "Compara vocales y consonantes desde la última vocal acentuada.", "Coinciden vocales y consonantes (-ado): es rima consonante.", texto=D)
    b.om(4, "¿Qué esquema de rima tiene la estrofa?", "ABAB", ["AABB", "ABBA", "AAAA"],
         "Marca con la misma letra los versos que riman entre sí.", "tejado (A), canción (B), lado (A), corazón (B): ABAB.", texto=D)

    E = "Bajo el cielo de Atacama / la noche se viste de luz; / brillan estrellas sin calma / sobre el silencio azul."
    b.om(4, "¿Qué tipo de rima tienen «Atacama» y «calma»?", "asonante", ["consonante", "no tienen rima", "aliteración"],
         "Desde la vocal acentuada, ¿coinciden las vocales, las consonantes o ambas?", "Coinciden solo las vocales (a-a), no las consonantes: es rima asonante.", texto=E)
    b.om(5, "¿Qué tipo de imagen predomina y qué efecto logra?", "visual: hace ver un cielo nocturno lleno de luz",
         ["auditiva: hace oír el ruido del desierto", "táctil: hace sentir el frío de la noche", "olfativa: hace oler las flores del desierto"],
         "Fíjate en cielo, luz, estrellas y azul.", "Cielo, luz, estrellas que brillan y color azul son imágenes visuales: pintan una noche luminosa.", texto=E)

    F = ("Suena el silbido suave del viento / sobre la sierra serena y sola; / "
         "rueda la roca, ruge el río, / y el rumor regresa en cada ola.")
    b.om(4, "¿Qué recurso sonoro predomina en los dos primeros versos?", "aliteración de la «s»", ["rima asonante", "hipérbole", "comparación"],
         "Lee en voz alta y fíjate qué sonido se repite.", "Se repite el sonido «s» (suena, silbido, suave, sierra, serena, sola): aliteración.", texto=F)
    b.om(5, "¿Qué efecto produce la repetición de la «r» en «rueda la roca, ruge el río»?", "imita el ruido fuerte del agua y las piedras",
         ["hace que el verso sea más largo", "imita el silencio de la sierra", "indica que es de noche"],
         "Pronuncia la «r» fuerte: ¿a qué sonido se parece?", "La «r» vibrante imita el estruendo del río y de las rocas que ruedan.", texto=F)

    b.cat(5, "¿Qué recurso usa cada verso?", ["Aliteración", "Hipérbole", "Comparación"],
          [("Susurra el sauce su secreto.", 0), ("Mece el mar su manto marino.", 0), ("Te lo he dicho un millón de veces.", 1),
           ("Lloré mares por ti.", 1), ("Blanca como la nieve.", 2), ("Fuerte como un roble.", 2)],
          "Aliteración repite sonidos; hipérbole exagera; comparación usa «como».",
          "Se repiten la s y la m; «un millón de veces» y «mares» exageran; «como» marca las comparaciones.")
    return b.items


def le08_oa3():
    b = Autor("len", 8, 3)
    b.em(1, "Une cada concepto con su definición.",
         [["autor", "persona real que escribe la obra"], ["narrador", "voz ficticia que cuenta la historia"], ["personaje", "ser que participa en los hechos"]],
         "Solo uno de ellos existe fuera del libro.", "El autor es real; el narrador es una voz creada por él; los personajes viven los hechos.")
    b.co(1, "Los ___ son ideas simplificadas sobre un grupo de personas, como «todos los abuelos son lentos».", "estereotipos",
         ["conflictos", "narradores", "desenlaces"],
         "Son generalizaciones que no consideran a cada persona.", "Un estereotipo atribuye una misma característica a todo un grupo.")

    A = ("«Soy una anciana de ochenta años y he visto crecer este puerto desde mi ventana. Vi llegar los primeros contenedores "
         "y vi irse a mis hijos en los barcos.» (Inicio del cuento «La ventana», de la escritora Javiera Muñoz, de 28 años).")
    b.om(1, "¿Quién narra el cuento?", "una anciana de ochenta años", ["Javiera Muñoz", "uno de sus hijos", "el capitán de un barco"],
         "¿Quién dice «yo» dentro del relato?", "La voz que cuenta es la de una anciana de ochenta años.", texto=A)
    b.om(2, "¿Quién eligió las palabras con que se describe el puerto?", "la escritora Javiera Muñoz",
         ["la anciana de la ventana", "los hijos de la anciana", "los marineros del puerto"],
         "¿Quién escribió el cuento en la realidad?", "La autora real, Javiera Muñoz, escribió todo el cuento, incluidas las palabras de la narradora.", texto=A)
    b.om(3, "¿Por qué la narradora y la autora no son la misma persona?", "la autora es una persona real que inventó una narradora ficticia",
         ["porque la narradora escribió el cuento", "porque la autora no puede usar la primera persona", "sí son la misma, porque el texto usa «yo»"],
         "Compara la edad de la autora con la de la narradora.", "La autora, de 28 años, creó una voz ficticia de 80 años: narrador y autor son distintos.", texto=A)

    B = ("Al comienzo del año, Maximiliano se burlaba de los que leían en el recreo. Un día lo castigaron en la biblioteca y, "
         "por aburrimiento, abrió una novela de piratas. Hoy dirige el club de lectura del colegio y presta sus libros a quien se los pida.")
    b.ord(2, "Ordena la transformación de Maximiliano.",
          ["Se burla de los lectores.", "Lo castigan en la biblioteca.", "Lee una novela por aburrimiento.", "Dirige el club de lectura."],
          "Sigue el camino desde cómo era hasta cómo es.", "Se burlaba, lo castigaron, leyó la novela y terminó dirigiendo el club.", texto=B)
    b.om(3, "¿Qué hecho provoca el cambio del personaje?", "leer una novela durante su castigo",
         ["burlarse de sus compañeros", "dirigir el club de lectura", "prestar sus libros"],
         "Busca lo que ocurre entre el inicio y el final.", "Leer la novela de piratas en la biblioteca es lo que lo transforma.", texto=B)
    b.cat(4, "¿Cómo era Maximiliano al inicio y cómo es al final?", ["Al inicio", "Al final"],
          [("burlón", 0), ("indiferente a los libros", 0), ("lector entusiasta", 1), ("generoso con sus libros", 1), ("líder del club de lectura", 1)],
          "Compara el comienzo del año con el «hoy».", "Al inicio era burlón e indiferente; al final lee, presta libros y lidera el club.", texto=B)

    C = ("Cuando llegó la nueva profesora de mecánica automotriz, varios apoderados reclamaron: «¿Una mujer enseñando a arreglar motores?». "
         "Al terminar el semestre, su curso ganó el concurso regional de autos solares.")
    b.om(2, "¿Quiénes expresan un prejuicio en el relato?", "los apoderados", ["la profesora", "los estudiantes del curso", "el jurado del concurso"],
         "¿Quién reclama sin conocer el trabajo de la profesora?", "Los apoderados juzgan a la profesora antes de verla trabajar.", texto=C)
    b.om(3, "¿Qué estereotipo muestran los apoderados?", "que la mecánica es un oficio solo para hombres",
         ["que los profesores nuevos son mejores", "que los autos solares son caros", "que los concursos son injustos"],
         "Fíjate en la pregunta que hacen los apoderados.", "Dudan porque es mujer: creen que la mecánica es cosa de hombres.", texto=C)
    b.om(4, "¿Cómo desmiente el relato ese estereotipo?", "muestra que el curso de la profesora gana el concurso regional",
         ["los apoderados la despiden", "la profesora deja el colegio", "el narrador da la razón a los apoderados"],
         "¿Qué ocurre al final del semestre?", "El éxito del curso demuestra que el estereotipo era falso.", texto=C)

    D = ("En el pueblo decían que los Rivas, recién llegados del norte, eran desconfiados, aunque nadie había hablado con ellos. "
         "Una noche de temporal se cayó el puente, y fue el señor Rivas quien, con sus hijos, cruzó el río para rescatar a los vecinos aislados. "
         "Al día siguiente, nadie repitió aquel comentario.")
    b.om(4, "¿Por qué la opinión del pueblo sobre los Rivas es un prejuicio?", "porque juzgaban a la familia sin conocerla",
         ["porque los Rivas eran realmente desconfiados", "porque venían del norte", "porque el puente se cayó"],
         "Fíjate en la frase «aunque nadie había hablado con ellos».", "Un prejuicio es juzgar antes de conocer: nadie había hablado con los Rivas.", texto=D)
    b.om(4, "¿Qué conflicto plantea el inicio del relato?", "una familia enfrenta los prejuicios de la comunidad",
         ["un personaje lucha contra sus propios miedos", "dos hermanos se pelean una herencia", "una persona enfrenta a un animal salvaje"],
         "¿Qué problema tienen los Rivas antes del temporal?", "Los Rivas son mal juzgados por el pueblo: un conflicto con la sociedad.", texto=D)
    b.om(5, "¿Qué transformación vive el pueblo?", "abandona su prejuicio al ver la valentía de los Rivas",
         ["sigue desconfiando de los Rivas", "decide construir un puente nuevo", "expulsa a la familia Rivas"],
         "¿Qué significa que «nadie repitió aquel comentario»?", "Tras el rescate, el pueblo dejó de decir que los Rivas eran desconfiados: cambió su opinión.", texto=D)

    E = ("Ana siempre había callado en clases por miedo a equivocarse. El día del debate, su equipo quedó sin vocero. "
         "Con la voz temblorosa, se levantó y defendió el reciclaje en su comuna. "
         "Perdieron por un punto, pero al salir, Ana sintió que había ganado algo más importante.")
    b.om(3, "¿Qué conflicto vive Ana al inicio?", "interno: su miedo a equivocarse", ["con su equipo", "con la naturaleza", "con el profesor"],
         "Lee la primera oración.", "Ana lucha contra su propio miedo: es un conflicto interno.", texto=E)
    b.om(5, "¿Cómo evoluciona Ana en el relato?", "pasa de callar por miedo a atreverse a hablar en público",
         ["pasa de hablar mucho a quedarse callada", "no cambia en nada", "pasa de ganar debates a perderlos"],
         "Compara cómo era en clases con lo que hizo en el debate.", "Al inicio callaba por miedo; en el debate se atrevió a hablar: se transformó.", texto=E)
    b.om(5, "¿Qué «ganó» Ana, aunque su equipo perdió?", "confianza para expresarse en público",
         ["el premio del debate", "un punto extra en la nota", "la amistad del equipo rival"],
         "Piensa en el miedo que tenía al comienzo.", "Superó su miedo a hablar: ganó confianza en sí misma, algo más importante que el resultado.", texto=E)
    return b.items


def le08_oa4():
    b = Autor("len", 8, 4)
    b.em(1, "Une cada recurso con su ejemplo.",
         [["metáfora", "Tus manos son palomas."], ["comparación", "Blanca como la espuma."],
          ["personificación", "La luna llora en silencio."], ["hipérbole", "Te llamé un millón de veces."]],
         "Comparación usa «como»; metáfora identifica; personificación humaniza; hipérbole exagera.",
         "Manos = palomas es metáfora; «como la espuma», comparación; la luna que llora, personificación; un millón de veces, hipérbole.")
    b.cat(3, "¿Lenguaje literal o figurado?", ["Literal", "Figurado"],
          [("Llueve sobre Valdivia.", 0), ("La tetera está en la mesa.", 0), ("El tren pasa por el pueblo.", 0),
           ("Llueve adentro, en el corazón.", 1), ("Tus ojos son dos lagunas.", 1), ("El viento te dio su voz.", 1)],
          "El lenguaje figurado no se entiende al pie de la letra.", "Las tres primeras dicen exactamente lo que pasa; las otras expresan sentimientos o imágenes con sentido figurado.")

    A = "Vuelvo al sur por sus lluvias, / vuelvo al sur por su pan, / vuelvo al sur por mi madre / que me espera en el umbral."
    b.om(1, "¿Qué recurso consiste en repetir palabras al comienzo de varios versos, como aquí?", "anáfora",
         ["hipérbole", "comparación", "personificación"],
         "Fíjate en cómo empiezan los tres primeros versos.", "Repetir «vuelvo al sur» al inicio de los versos es una anáfora.", texto=A)
    b.co(2, "La expresión que se repite al comienzo de los versos es «___».", "vuelvo al sur", ["por sus lluvias", "mi madre", "en el umbral"],
         "Lee solo el inicio de cada verso.", "Los tres primeros versos comienzan con «vuelvo al sur».", texto=A)
    b.om(3, "¿Qué efecto produce la anáfora en este poema?", "enfatiza el deseo intenso del hablante de regresar",
         ["indica que el hablante nunca se fue", "describe el clima del norte", "hace que el poema sea más corto"],
         "¿Qué idea queda más fuerte al repetirse tres veces?", "Repetir «vuelvo al sur» insiste en las ganas de volver y en todo lo que lo atrae.", texto=A)

    B = "El mar te dio su azul, / el bosque te dio su sombra, / el viento te dio su voz, / y yo te di mi nombre."
    b.om(2, "¿Qué recurso hay en los tres primeros versos, que repiten la misma estructura?", "paralelismo",
         ["aliteración", "hipérbole", "rima consonante"],
         "Compara cómo están construidos los versos: «el ___ te dio su ___».", "Repetir la misma construcción en varios versos es un paralelismo.", texto=B)
    b.om(4, "¿Qué efecto tiene que el último verso rompa la estructura con «y yo te di mi nombre»?", "destaca el regalo del hablante como el más personal",
         ["muestra que el hablante olvidó el patrón", "indica que el poema no tiene ritmo", "explica de qué color es el mar"],
         "¿Qué cambia en el último verso y quién aparece?", "Al cambiar la estructura, el último verso llama la atención: el hablante entrega algo propio, su nombre.", texto=B)
    b.om(5, "¿Qué idea une todo el poema?", "la persona amada recibe lo mejor de la naturaleza y del hablante",
         ["el hablante critica a la naturaleza", "el poema describe un paisaje vacío", "el mar y el viento compiten entre sí"],
         "¿Qué tienen en común todos los versos?", "En cada verso alguien le da algo valioso a «ti»: el poema celebra a la persona amada.", texto=B)

    C = ("Caperucita ya no teme al bosque: / ahora el lobo vive en la ciudad, / "
         "tiene auto, corbata y oficina, / y sonríe en la televisión.")
    b.om(3, "¿Con qué texto conocido se relaciona este poema?", "el cuento de Caperucita Roja",
         ["la fábula de la cigarra y la hormiga", "la leyenda del Caleuche", "el cuento de los tres cerditos"],
         "¿Qué personaje se nombra en el primer verso?", "Menciona a Caperucita, al lobo y al bosque: dialoga con el cuento de Caperucita Roja.", texto=C)
    b.om(4, "¿Qué elementos del cuento tradicional conserva el poema?", "los personajes de Caperucita y el lobo",
         ["el cazador y la abuela", "la canasta con pasteles", "la casita de la abuela"],
         "Fíjate en qué personajes del cuento aparecen.", "El poema toma a Caperucita y al lobo del cuento, pero los sitúa en el mundo actual.", texto=C)
    b.om(5, "¿Qué sentido nuevo le da el poema al lobo?", "representa peligros disfrazados de la vida moderna",
         ["es un animal real que escapó del zoológico", "es el abuelo de Caperucita", "es un personaje bueno que ayuda a todos"],
         "En el cuento el lobo engaña disfrazado. ¿Cómo se «disfraza» ahora?", "El lobo con corbata que sonríe en televisión simboliza amenazas que hoy se ven confiables.", texto=C)

    D = "Llueve, llueve sobre Valdivia, / llueve en el río y en el portón, / llueve en los ojos de mi abuela / y llueve adentro, en el corazón."
    b.nu(2, "¿Cuántas veces se repite la palabra «llueve» en el poema?", 5,
         "Cuenta con cuidado: el primer verso tiene más de una.", "Aparece 5 veces: dos en el primer verso y una en cada uno de los otros tres.", unidad="veces", texto=D)
    b.om(3, "¿Qué efecto produce repetir «llueve»?", "transmite la sensación de una lluvia constante que lo invade todo",
         ["indica que la lluvia ya terminó", "hace que el poema tenga menos versos", "muestra que la lluvia le da risa al hablante"],
         "¿Cómo es una lluvia que se nombra una y otra vez?", "La repetición imita una lluvia que no para y que llega a todas partes, incluso adentro.", texto=D)
    b.om(4, "¿Qué sugieren «llueve en los ojos de mi abuela» y «llueve adentro, en el corazón»?", "que hay tristeza y llanto",
         ["que hay goteras en la casa", "que al hablante le gusta la lluvia", "que la abuela quedó mojada"],
         "No los leas al pie de la letra: ¿qué «lluvia» sale de los ojos?", "Son metáforas: la lluvia en los ojos es llanto y la lluvia en el corazón, tristeza.", texto=D)

    E = ("Tic, tac, tic, tac, la tarde se va, / tiembla la taza, la tetera también; / "
         "tras la ventana trota el tren / y tú, tan lejos, no vuelves ya.")
    b.co(1, "En el primer verso, «___» imita el sonido de un reloj.", "tic, tac", ["la tarde", "se va", "la taza"],
         "Busca palabras que suenan como lo que nombran.", "«Tic, tac» es una onomatopeya: imita el sonido del reloj.", texto=E)
    b.om(4, "¿Qué sonido se repite en todo el poema y qué imita?", "la «t», que imita el tictac del reloj",
         ["la «m», que imita el mar", "la «s», que imita el viento", "la «r», que imita un motor"],
         "Lee en voz alta: tarde, tiembla, taza, tetera, tras, trota, tren…", "La «t» repetida (aliteración) imita el golpeteo del reloj.", texto=E)
    b.om(5, "¿Qué relación hay entre el tictac y el último verso?", "el tictac marca el tiempo que pasa mientras el hablante espera a alguien que no vuelve",
         ["el reloj está roto y por eso nadie vuelve", "el tren hace tictac al pasar", "no hay ninguna relación entre ambos"],
         "¿Qué mide un reloj y qué le pasa al hablante?", "El reloj hace sentir el paso del tiempo y la espera inútil de quien está «tan lejos».", texto=E)
    return b.items


GENERADORES = {
    "5_basico.lenguaje.OA4": le05_oa4,
    "5_basico.lenguaje.OA12": le05_oa12,
    "5_basico.lenguaje.OA21": le05_oa21,
    "5_basico.lenguaje.OA22": le05_oa22,
    "6_basico.lenguaje.OA4": le06_oa4,
    "6_basico.lenguaje.OA21": le06_oa21,
    "7_basico.lenguaje.OA3": le07_oa3,
    "7_basico.lenguaje.OA4": le07_oa4,
    "8_basico.lenguaje.OA3": le08_oa3,
    "8_basico.lenguaje.OA4": le08_oa4,
}
