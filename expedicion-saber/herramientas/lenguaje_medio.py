"""Lengua y Literatura 1° a 4° medio: 15 desafíos por OA (3 por nivel de dificultad, 1 a 5).
Todos los textos son originales; los versos se separan con « / »."""
from autor import Autor


# ---------------- 1° medio ----------------
def le1m_oa3():
    b = Autor("len", "1m", 3)
    T1 = "Desde que cerraron la mina, mi padre se sienta cada tarde frente a la ventana. No habla. Yo le llevo el té y él me da las gracias con un gesto. Mi madre dice que está pensando; yo creo que está esperando algo que ya no va a volver."
    b.om(1, "¿En qué persona está narrado el texto?", "primera persona", ["tercera persona", "segunda persona", "no tiene narrador"], "Fíjate en «mi padre», «yo le llevo».", "El narrador participa y dice «yo»: primera persona.", texto=T1)
    b.om(2, "¿Cuál es el conflicto principal?", "el padre no logra superar el cierre de la mina", ["la madre quiere mudarse", "el narrador no quiere llevar el té", "la ventana está rota"], "¿Qué cambió en la vida del padre?", "El cierre de la mina afecta profundamente al padre.", texto=T1)
    b.om(4, "¿Qué efecto produce narrar en primera persona en este relato?", "transmite la mirada íntima y la preocupación del hijo", ["hace el relato más objetivo", "permite conocer los pensamientos del padre", "elimina las emociones"], "El narrador interpreta lo que ve.", "La primera persona muestra la interpretación emocional del hijo.", texto=T1)
    T2 = "Clara y su hermana Inés no se hablaban desde el funeral de su abuela. Cuando el notario leyó el testamento, ambas descubrieron que la casa del lago quedaba para las dos, con una condición: debían pasar juntas un verano entero allí."
    b.om(1, "¿Quiénes son los personajes principales?", "Clara e Inés", ["el notario y la abuela", "Clara y el notario", "Inés y su madre"], "Busca a quienes vive el conflicto.", "Las hermanas Clara e Inés.", texto=T2)
    b.co(2, "La relación entre las hermanas al comienzo es de ___.", "distanciamiento", ["complicidad", "admiración", "alegría"], "«No se hablaban».", "No se hablaban: hay distanciamiento.", texto=T2)
    b.om(3, "¿Qué función cumple la condición del testamento en la historia?", "obliga a las hermanas a enfrentar su conflicto", ["resuelve el conflicto de inmediato", "presenta a un nuevo personaje", "describe el lago"], "¿Qué provocará pasar un verano juntas?", "La condición las obliga a convivir y enfrentar su distancia.", texto=T2)
    b.om(3, "¿Qué tipo de conflicto viven Clara e Inés?", "un conflicto entre personajes", ["un conflicto con la naturaleza", "un conflicto con la tecnología", "no hay conflicto"], "El problema está en la relación entre ellas.", "Es un conflicto interpersonal, entre las hermanas.", texto=T2)
    T3 = "El inspector Rojas observó la habitación: la ventana abierta, el reloj detenido a las tres y una taza de café todavía tibia. Nadie había entrado ni salido, según el portero. Rojas sonrió: el portero mentía."
    b.om(2, "¿Qué tipo de narrador tiene este fragmento?", "tercera persona", ["primera persona protagonista", "primera persona testigo", "segunda persona"], "El narrador habla de «Rojas».", "Narra desde fuera: tercera persona.", texto=T3)
    b.cat(3, "¿Es un indicio para el inspector o no?", ["Indicio", "Dato sin importancia aparente"], [("la taza de café tibia", 0), ("el reloj detenido a las tres", 0), ("la ventana abierta", 0), ("el nombre del inspector", 1)],
          "Los indicios ayudan a resolver el misterio.", "La taza tibia, el reloj y la ventana son indicios; el nombre no.", texto=T3)
    b.om(5, "¿Por qué Rojas concluye que el portero mentía?", "porque el café tibio muestra que alguien estuvo ahí hace poco", ["porque el reloj funcionaba", "porque el portero sonrió", "porque la ventana estaba cerrada"], "Relaciona la taza tibia con «nadie había entrado».", "Si el café seguía tibio, alguien había estado recién.", texto=T3)
    T4 = "Este fragmento pertenece al capítulo final de una novela. Tomás, el protagonista que había huido de su pueblo al comienzo, vuelve y encuentra la plaza vacía. «Todo es igual», piensa, «solo yo cambié»."
    b.om(4, "¿Qué revela la frase «solo yo cambié» en relación con la obra completa?", "la transformación del protagonista a lo largo de la novela", ["que el pueblo se modernizó", "que Tomás nunca salió", "que la novela empieza ahí"], "Relaciona el final con el comienzo (la huida).", "El fragmento final muestra cómo cambió Tomás desde su huida.", texto=T4)
    b.ord(4, "Ordena los momentos de la historia de Tomás.", ["Tomás huye de su pueblo.", "Vive fuera mucho tiempo.", "Vuelve al pueblo.", "Reconoce que él cambió."], "El fragmento alude al comienzo y al final.", "Huida, ausencia, regreso y reconocimiento.", texto=T4)
    b.em(5, "Une cada elemento narrativo con su ejemplo de los textos.", [["conflicto interno", "el padre que espera algo que no volverá"], ["conflicto entre personajes", "las hermanas que no se hablan"], ["indicio", "el café todavía tibio"]],
         "Repasa los tres primeros textos.", "Conflicto interno, entre personajes e indicio.")
    b.om(5, "Si el texto de la mina estuviera narrado por un narrador omnisciente, ¿qué podría agregar?", "lo que piensa y siente el padre por dentro", ["solo los diálogos", "nada, sería idéntico", "la opinión del lector"], "El omnisciente conoce los pensamientos de todos.", "Podría revelar la interioridad del padre.")
    b.co(1, "El narrador que cuenta la historia como uno de sus personajes es un narrador ___.", "protagonista", ["omnisciente", "objetivo", "ausente"], "Narra en primera persona su propia historia.", "Es narrador protagonista.")
    return b.items


def le1m_oa4():
    b = Autor("len", "1m", 4)
    P1 = "Mi casa es un barco / anclado en la ladera, / cuando sopla el viento / sueña que navega."
    b.om(1, "¿Qué figura literaria hay en «Mi casa es un barco»?", "metáfora", ["comparación", "hipérbole", "anáfora"], "Identifica dos cosas sin «como».", "Identifica casa y barco sin nexo: metáfora.", texto=P1)
    b.om(2, "«Sueña que navega» atribuye a la casa una acción humana. Es una…", "personificación", ["hipérbole", "aliteración", "antítesis"], "Soñar es propio de seres vivos.", "Dar cualidades humanas a un objeto es personificar.", texto=P1)
    b.om(4, "¿Qué actitud tiene el hablante hacia su casa?", "afectiva e imaginativa: la ve como algo vivo que desea viajar", ["indiferente", "de rechazo", "de miedo"], "Fíjate en cómo la describe.", "La personifica con cariño y fantasía.", texto=P1)
    P2 = "Cayó la última hoja / del aromo del patio, / y mi abuela, en silencio, / guardó su delantal."
    b.om(2, "¿Qué podría simbolizar «la última hoja» del árbol?", "el final de una etapa o de una vida", ["el comienzo de la primavera", "la alegría de una fiesta", "un día de sol"], "Piensa en el otoño y en la abuela.", "La última hoja sugiere un final, un cierre.", texto=P2)
    b.co(3, "El hablante lírico del poema observa a su ___.", "abuela", ["madre", "hermana", "vecina"], "Busca el personaje mencionado.", "El hablante observa a su abuela.", texto=P2)
    b.om(5, "¿Qué relación hay entre la hoja que cae y el gesto de la abuela?", "ambos sugieren un cierre o despedida silenciosa", ["no tienen relación", "la abuela barre la hoja", "la hoja cae sobre el delantal"], "Busca un paralelo entre naturaleza y persona.", "Los dos versos finales reflejan el mismo sentido de final.", texto=P2)
    P3 = "Ruge el río, ronco y rojo, / rompe rocas sin reposo."
    b.om(3, "¿Qué recurso sonoro predomina?", "aliteración (repetición del sonido r)", ["rima asonante en a", "anáfora", "pregunta retórica"], "Escucha qué sonido se repite.", "La repetición de la r imita la fuerza del río.", texto=P3)
    b.om(4, "¿Qué efecto produce ese recurso sonoro?", "imita el ruido fuerte y violento del río", ["hace el poema más silencioso", "crea humor", "describe colores suaves"], "Relaciona forma y significado.", "La r repetida suena áspera, como el río.", texto=P3)
    b.cat(1, "¿Comparación o metáfora?", ["Comparación", "Metáfora"], [("tus ojos son como luceros", 0), ("ligero como una pluma", 0), ("tus ojos son luceros", 1), ("la vida es un río", 1)],
          "La comparación usa «como».", "Con «como» es comparación; sin nexo, metáfora.")
    P4 = "No quiero tu oro, / no quiero tu plata, / quiero tu risa / cuando el día acaba."
    b.om(3, "¿Qué figura se repite al inicio de los versos «No quiero…»?", "anáfora", ["hipérbole", "metáfora", "onomatopeya"], "Repetición al comienzo de versos.", "Repetir al inicio de versos es anáfora.", texto=P4)
    b.om(5, "¿Qué valor expresa el hablante?", "valora más el afecto que la riqueza", ["prefiere el oro", "no quiere a nadie", "le gusta la noche"], "Contrasta lo que no quiere con lo que sí.", "Rechaza el oro y la plata y prefiere la risa del otro.", texto=P4)
    b.em(4, "Une cada elemento del poema con su función.", [["hablante lírico", "voz que expresa el poema"], ["objeto lírico", "aquello sobre lo que habla"], ["temple de ánimo", "estado emocional del hablante"]], "Conceptos de la poesía.", "Hablante, objeto y temple de ánimo.")
    b.ord(2, "Ordena los versos para reconstruir la estrofa.", ["Mi casa es un barco", "anclado en la ladera,", "cuando sopla el viento", "sueña que navega."], "Sigue el sentido del poema.", "Así se lee la estrofa original.")
    b.co(1, "La persona que «habla» en un poema se llama hablante ___.", "lírico", ["narrador", "dramático", "omnisciente"], "No es el autor.", "Es el hablante lírico.")
    b.om(5, "¿Por qué decimos que la forma de P3 («Ruge el río…») refuerza su significado?", "porque los sonidos repetidos imitan lo que describen", ["porque es muy largo", "porque no tiene verbos", "porque rima con el título"], "Forma = sonidos; significado = un río violento.", "Los sonidos ásperos reproducen la fuerza del río.")
    return b.items


def le1m_oa9():
    b = Autor("len", "1m", 9)
    T1 = "Los colegios deberían tener más áreas verdes. Diversos estudios muestran que el contacto con la naturaleza reduce el estrés y mejora la concentración. Además, los patios de cemento se calientan demasiado en verano. Invertir en árboles es invertir en aprendizaje."
    b.om(1, "¿Cuál es la tesis del texto?", "Los colegios deberían tener más áreas verdes.", ["Los patios de cemento son baratos.", "En verano hace calor.", "Los estudios son aburridos."], "La tesis es la postura que se defiende.", "La primera oración plantea la postura.", texto=T1)
    b.om(2, "¿Qué argumento usa el autor?", "el contacto con la naturaleza reduce el estrés", ["los árboles son caros", "a los alumnos les gusta el cemento", "los colegios son grandes"], "Busca las razones que apoyan la tesis.", "Cita estudios sobre el estrés y la concentración.", texto=T1)
    b.om(2, "¿Qué conector usa el autor para agregar un argumento?", "Además", ["Sin embargo", "Por lo tanto", "Aunque"], "Busca una palabra que sume ideas.", "«Además» agrega un nuevo argumento.", texto=T1)
    b.om(3, "¿Qué tipo de argumento es «diversos estudios muestran…»?", "de autoridad o evidencia científica", ["de experiencia personal", "emocional", "de analogía"], "Se apoya en investigaciones.", "Recurre a estudios como evidencia.", texto=T1)
    T2 = "Mi vecino dice que el reciclaje no sirve porque todo termina en el mismo camión. Yo lo vi una vez, así que debe ser verdad en todas las comunas."
    b.om(4, "¿Cuál es el problema de este razonamiento?", "generaliza a partir de un solo caso", ["usa demasiadas estadísticas", "cita a un experto", "no tiene opinión"], "¿Una sola observación prueba algo para todas las comunas?", "Es una generalización apresurada: un caso no basta.", texto=T2)
    b.om(5, "¿Qué evidencia haría más sólida la opinión del vecino?", "datos oficiales sobre el destino del reciclaje en varias comunas", ["que más vecinos opinen lo mismo", "una foto de un camión", "repetir la idea más fuerte"], "Busca evidencia suficiente y confiable.", "Se necesitan datos amplios y confiables.", texto=T2)
    b.cat(1, "¿Hecho u opinión?", ["Hecho", "Opinión"], [("Chile tiene 16 regiones.", 0), ("El agua hierve a 100 °C a nivel del mar.", 0), ("El invierno es la mejor estación.", 1), ("Las series de hoy son aburridas.", 1)],
          "Un hecho se puede comprobar.", "Las regiones y la ebullición se comprueban; lo demás es opinión.")
    b.co(1, "La idea que un texto argumentativo defiende se llama ___.", "tesis", ["conclusión", "título", "ejemplo"], "Es la postura del emisor.", "La postura central es la tesis.")
    b.em(3, "Une cada texto argumentativo con su característica.", [["columna de opinión", "texto firmado en un diario"], ["carta al director", "lector que opina en un medio"], ["discurso", "texto oral ante un público"]], "Géneros argumentativos.", "Columna, carta al director y discurso.")
    b.ord(3, "Ordena la estructura de un texto argumentativo.", ["Introducción con la tesis", "Argumentos que la sostienen", "Contraargumento y respuesta", "Conclusión"], "Primero la postura y al final el cierre.", "Introducción, argumentos, contraargumento y conclusión.")
    b.om(4, "¿Qué conector introduce un contraargumento?", "Sin embargo, algunos sostienen que…", ["Por lo tanto,", "Además,", "En primer lugar,"], "Busca un conector de oposición.", "«Sin embargo» introduce una idea contraria.")
    b.om(4, "¿Qué argumento es más suficiente para defender que «el uniforme reduce la discriminación»?", "un estudio en 50 colegios que compara casos antes y después del uniforme", ["mi amigo cree que es así", "los uniformes son azules", "a mí me gusta el uniforme"], "Busca evidencia amplia.", "Un estudio comparativo es evidencia más suficiente.")
    b.om(5, "En «Es evidente que todos los jóvenes prefieren las redes sociales a los libros», ¿qué palabra debilita el argumento?", "todos", ["jóvenes", "redes", "libros"], "Busca una generalización.", "«Todos» generaliza sin evidencia.")
    b.cat(5, "¿Argumento válido o falacia?", ["Argumento válido", "Falacia"], [("Según el INE, el desempleo bajó 2 puntos.", 0), ("La medida redujo los accidentes en un 30 %.", 0), ("No le creas: es muy joven.", 1), ("Si todos lo hacen, debe estar bien.", 1)],
          "Las falacias atacan a la persona o apelan a la mayoría.", "Los datos son argumentos; atacar al hablante o apelar a «todos» son falacias.")
    b.om(2, "¿Cuál es la conclusión del texto sobre las áreas verdes?", "Invertir en árboles es invertir en aprendizaje.", ["Los patios de cemento son útiles.", "Los estudios son caros.", "El verano es largo."], "Busca la última oración.", "Cierra relacionando árboles y aprendizaje.", texto=T1)
    return b.items


# ---------------- 2° medio ----------------
def le2m_oa3():
    b = Autor("len", "2m", 3)
    T1 = "El viejo marinero contaba cada noche la misma historia en el bar del puerto. Pero esa noche, mientras hablaba, recordó de pronto la tormenta de 1970: el mástil partido, el grito de su hermano, el agua helada. Entonces calló, y por primera vez nadie le pidió que siguiera."
    b.om(2, "¿Qué recurso narrativo aparece cuando el marinero recuerda la tormenta de 1970?", "un flashback o retrospección", ["un monólogo teatral", "una carta", "un diálogo"], "La historia salta al pasado.", "Recordar un hecho anterior es una retrospección.", texto=T1)
    b.om(4, "¿Qué efecto produce el silencio final?", "sugiere un dolor profundo que el marinero no puede contar", ["muestra que olvidó la historia", "crea humor", "indica que el bar cerró"], "Relaciona el recuerdo con el silencio.", "El recuerdo doloroso lo deja sin palabras.", texto=T1)
    b.co(1, "El lugar donde ocurre la historia es el bar del ___.", "puerto", ["campo", "colegio", "hospital"], "Lee la primera oración.", "Ocurre en un bar del puerto.", texto=T1)
    T2 = "En la novela, el personaje del abuelo sabio siempre tiene un consejo justo; la madrastra es cruel con la protagonista, y el príncipe llega a tiempo para salvarla."
    b.om(1, "¿Qué es un personaje tipo?", "un personaje con rasgos fijos y reconocibles en muchas obras", ["un personaje que cambia mucho", "el autor de la obra", "un personaje sin nombre"], "Piensa en la madrastra cruel o el príncipe salvador.", "Son modelos repetidos con rasgos predecibles.", texto=T2)
    b.cat(2, "¿Es un personaje tipo?", ["Personaje tipo", "No necesariamente"], [("la madrastra cruel", 0), ("el príncipe salvador", 0), ("el abuelo sabio", 0), ("una vecina con dudas y contradicciones", 1)],
          "Los personajes tipo son predecibles.", "Madrastra, príncipe y abuelo sabio son tipos; la vecina compleja no.", texto=T2)
    b.om(5, "¿Qué estereotipo de género podría cuestionarse en ese relato?", "que la protagonista necesite ser salvada por un príncipe", ["que el abuelo dé consejos", "que exista una novela", "que haya personajes"], "Piensa en roles fijos por género.", "La mujer pasiva salvada por un hombre es un estereotipo.", texto=T2)
    T3 = "Mientras esperaba el tren, Lucía abrió un libro. En él, un joven escribía cartas a una mujer que nunca respondía. Al final del libro, Lucía encontró una carta escrita a mano, con su propio nombre."
    b.om(3, "¿Qué recurso aparece en el cuento?", "una historia dentro de otra historia (relato enmarcado)", ["un poema", "una noticia", "una receta"], "Lucía lee una historia mientras vive la suya.", "La historia del libro está dentro de la de Lucía.", texto=T3)
    b.om(5, "¿Qué efecto produce el final?", "mezcla la historia leída con la vida de Lucía y genera misterio", ["explica todo el misterio", "aburre al lector", "cambia el tema a deportes"], "La carta tiene el nombre de Lucía.", "Las dos historias se cruzan y surge el misterio.", texto=T3)
    b.em(3, "Une cada tópico literario con su idea.", [["carpe diem", "aprovechar el momento presente"], ["tempus fugit", "el tiempo pasa rápido"], ["ubi sunt", "¿dónde están los que ya no están?"]], "Tópicos clásicos de la literatura.", "Carpe diem, tempus fugit y ubi sunt.")
    b.om(4, "En un cuento, una llave aparece siempre que la protagonista toma una decisión importante. La llave funciona como…", "símbolo de oportunidad o de cambio", ["personaje secundario", "narrador", "ambiente físico"], "Un objeto que representa una idea.", "La llave simboliza abrir nuevas posibilidades.")
    b.ord(4, "Ordena cronológicamente los hechos del marinero, aunque el relato no siga ese orden.", ["La tormenta de 1970.", "Cuenta historias en el bar durante años.", "Esa noche recuerda la tormenta.", "Calla y nadie le pide seguir."], "Distingue el orden del relato del orden de los hechos.", "Primero la tormenta; luego años de historias, el recuerdo y el silencio.")
    b.om(2, "En «el mástil partido, el grito de su hermano, el agua helada», ¿qué recurso se usa?", "enumeración de imágenes", ["pregunta retórica", "diálogo", "rima"], "Hay una serie de elementos separados por comas.", "Es una enumeración que reconstruye el recuerdo.")
    b.co(3, "Una creencia simplificada y generalizada sobre un grupo de personas es un ___.", "estereotipo", ["símbolo", "tópico", "flashback"], "Ej.: «todos los … son …».", "Es un estereotipo.")
    b.om(5, "¿Por qué el recuerdo de 1970 aparece justo mientras el marinero cuenta su historia de siempre?", "para revelar el origen de su dolor y cambiar el sentido de la escena", ["para describir el bar", "para presentar a un personaje nuevo", "para hacer reír a los oyentes"], "Compara la historia repetida con el recuerdo que lo silencia.", "El flashback muestra lo que la historia repetida ocultaba.", texto=T1)
    b.om(1, "¿Qué es un flashback?", "un salto al pasado dentro del relato", ["un salto al futuro", "el título de un cuento", "un tipo de narrador"], "Viene del inglés: destello hacia atrás.", "Es una retrospección.")
    return b.items


def le2m_oa9():
    b = Autor("len", "2m", 9)
    T1 = "Quizás algunos piensen que prohibir los celulares en clases es exagerado. Sin embargo, es indudable que su uso constante afecta la concentración. ¿Acaso queremos generaciones incapaces de prestar atención?"
    b.cat(2, "¿Es un modalizador?", ["Modalizador", "No es modalizador"], [("quizás", 0), ("es indudable que", 0), ("acaso", 0), ("celulares", 1), ("clases", 1)],
          "Los modalizadores muestran la actitud del emisor (certeza, duda).", "Quizás, es indudable y acaso muestran actitud; celulares y clases no.", texto=T1)
    b.om(3, "¿Qué recurso es «¿Acaso queremos generaciones incapaces de prestar atención?»?", "pregunta retórica con apelación emocional", ["dato estadístico", "cita de autoridad", "definición"], "No espera respuesta; busca conmover.", "Es una pregunta retórica que apela a la emoción.", texto=T1)
    b.om(4, "¿Qué expresa «es indudable que»?", "certeza fuerte del emisor", ["duda", "humor", "un dato comprobado"], "Es un modalizador.", "Muestra seguridad, aunque no aporta evidencia.", texto=T1)
    T2 = "El concejal propone más ciclovías. Pero claro, ¿qué va a saber de transporte alguien que nunca ha tomado una micro?"
    b.om(2, "¿Qué falacia aparece?", "ad hominem: ataca a la persona y no la propuesta", ["generalización apresurada", "apelación a la autoridad", "falso dilema"], "¿Se discuten las ciclovías o al concejal?", "Desacredita a la persona en vez de discutir la idea.", texto=T2)
    b.om(5, "¿Cómo se podría reformular para argumentar de manera válida?", "discutiendo datos sobre si las ciclovías mejoran el transporte", ["insultando al concejal con más fuerza", "cambiando de tema", "apoyando sin razones"], "Enfócate en la propuesta.", "Un argumento válido evalúa la propuesta con evidencia.", texto=T2)
    T3 = "O apoyamos el nuevo estadio, o la ciudad quedará estancada para siempre."
    b.om(3, "¿Qué falacia contiene?", "falso dilema", ["ad hominem", "apelación a la tradición", "pregunta retórica"], "Presenta solo dos opciones extremas.", "Reduce el problema a dos opciones cuando existen más.", texto=T3)
    b.cat(1, "¿Recurso racional o emocional?", ["Racional", "Emocional"], [("un dato estadístico", 0), ("una cita de un experto", 0), ("una historia conmovedora", 1), ("una imagen de un niño triste", 1)],
          "Los racionales apelan a la razón; los emocionales, a los sentimientos.", "Datos y expertos son racionales; historias e imágenes que conmueven, emocionales.")
    b.co(1, "Las palabras que muestran la actitud del emisor, como «quizás» o «sin duda», se llaman ___.", "modalizadores", ["sustantivos", "conectores temporales", "pronombres"], "Modalizan el enunciado.", "Son modalizadores.")
    b.em(2, "Une cada falacia con su ejemplo.", [["generalización apresurada", "Un taxista fue grosero: todos lo son."], ["apelación a la mayoría", "Millones lo compran: debe ser bueno."], ["ad hominem", "No le creas, es de otra ciudad."]], "Identifica el error de cada razonamiento.", "Generalizar, apelar a la mayoría y atacar a la persona.")
    b.ord(3, "Ordena los pasos para evaluar un texto argumentativo.", ["Identificar la tesis.", "Reconocer los argumentos.", "Evaluar si la evidencia es suficiente.", "Detectar falacias o recursos emocionales."], "De lo general a la evaluación crítica.", "Así se evalúa un texto argumentativo.")
    b.om(4, "«Todos los expertos coinciden en que…», sin nombrar a ninguno. ¿Qué problema tiene?", "apela a una autoridad vaga e imposible de verificar", ["es un dato preciso", "es una pregunta retórica", "no tiene ningún problema"], "¿Quiénes son esos expertos?", "Una autoridad sin identificar no se puede comprobar.")
    b.om(4, "¿Qué publicidad usa principalmente un recurso emocional?", "«Dale a tu familia la felicidad que merece»", ["«Contiene 30 % menos de azúcar»", "«Precio: $1.990»", "«Disponible desde el lunes»"], "Busca la que apela a sentimientos.", "Apela al cariño por la familia, no a datos.")
    b.om(5, "¿Qué modalizador expresa duda y deja abierta la discusión?", "Posiblemente", ["Sin duda", "Evidentemente", "Indiscutiblemente"], "Busca uno que no sea tajante.", "«Posiblemente» expresa duda.")
    b.cat(5, "¿Certeza o duda?", ["Certeza", "Duda"], [("es evidente que", 0), ("sin lugar a dudas", 0), ("tal vez", 1), ("podría ser que", 1)],
          "Fíjate en qué tan seguro está el emisor.", "Evidente y sin lugar a dudas expresan certeza; tal vez y podría, duda.")
    b.co(1, "Cuando se presentan solo dos opciones extremas habiendo más, se comete un falso ___.", "dilema", ["argumento", "símbolo", "hecho"], "«O esto, o aquello».", "Es un falso dilema.")
    return b.items


def le2m_oa18():
    b = Autor("len", "2m", 18)
    b.co(1, "___ vienes a la fiesta?", "¿Cuándo", ["¿Cuando", "Cuándo", "Cuando"], "Las palabras interrogativas llevan tilde y signos de apertura.", "Se escribe «¿Cuándo vienes…?».")
    b.om(1, "¿Qué oración usa bien la coma vocativa?", "Martina, ven a almorzar.", ["Martina ven, a almorzar.", "Martina ven a, almorzar.", "Martina ven a almorzar,"], "El vocativo se separa con coma.", "«Martina» es vocativo: va separado por coma.")
    b.cat(1, "¿Lleva tilde?", ["Lleva tilde", "No lleva tilde"], [("canción", 0), ("árbol", 0), ("lápiz", 0), ("examen", 1), ("reloj", 1), ("ciudad", 1)],
          "Aguda en n, s o vocal; grave en otra consonante.", "Canción (aguda en n), árbol y lápiz (graves en l/z) llevan; examen, reloj y ciudad no.")
    b.co(2, "Compré tres cosas___ pan, leche y huevos.", ":", [";", ",", "."], "Antes de una enumeración anunciada.", "Los dos puntos anuncian la enumeración.")
    b.om(2, "¿Dónde corresponde el punto y coma?", "Llovía mucho; sin embargo, salimos.", ["Llovía; mucho sin embargo, salimos.", "Llovía mucho sin embargo; salimos.", "Llovía mucho sin; embargo salimos."], "Va antes de conectores como «sin embargo» entre oraciones.", "Punto y coma antes de «sin embargo» y coma después.")
    b.em(2, "Une cada signo con su uso.", [["comillas", "citar palabras textuales"], ["paréntesis", "agregar información aclaratoria"], ["puntos suspensivos", "dejar una idea incompleta o en suspenso"]], "Repasa los signos de puntuación.", "Comillas, paréntesis y puntos suspensivos.")
    b.om(3, "¿Qué oración cita correctamente las palabras de Ana?", "Ana dijo: «Mañana llego temprano».", ["Ana dijo (Mañana llego temprano).", "Ana dijo; Mañana llego temprano.", "Ana dijo, mañana llego temprano»."], "Las palabras textuales van entre comillas, tras dos puntos.", "Se usan dos puntos y comillas para citar textualmente.")
    b.cat(3, "¿Correcta o incorrecta?", ["Correcta", "Incorrecta"], [("Ojalá venga mañana.", 0), ("Él compró té para mí.", 0), ("El llegó tarde.", 1), ("Quiero un te caliente.", 1)],
          "Revisa las tildes diacríticas.", "«Él» (pronombre) y «té» (bebida) llevan tilde.")
    b.om(3, "¿Qué oración tiene la puntuación correcta?", "Santiago, la capital de Chile, tiene muchos cerros.", ["Santiago la capital de Chile, tiene muchos cerros.", "Santiago, la capital de Chile tiene, muchos cerros.", "Santiago la capital, de Chile tiene muchos cerros."], "La aposición explicativa va entre comas.", "«La capital de Chile» explica a Santiago: va entre comas.")
    b.co(4, "—¿Vienes? ___preguntó Ana.", "—", ["«", "(", ";"], "En los diálogos, la raya introduce el comentario del narrador.", "Se usa raya: «—¿Vienes? —preguntó Ana.».")
    b.om(4, "¿Qué palabra está mal escrita?", "exhuberante", ["exuberante", "hierba", "exhibición"], "Una de ellas lleva una h que no corresponde.", "Lo correcto es «exuberante», sin h.")
    b.ord(4, "Ordena las palabras para formar una oración con buena puntuación.", ["Sin embargo,", "decidimos", "seguir", "caminando."], "El conector va al inicio, seguido de coma.", "«Sin embargo, decidimos seguir caminando.»")
    b.om(5, "¿Por qué lleva tilde «río» si es una palabra grave terminada en vocal?", "por el hiato: la vocal cerrada tónica lleva tilde", ["porque es aguda", "porque es esdrújula", "no debería llevarla"], "Piensa en las vocales i/o separadas.", "Ri-o: hiato con vocal cerrada tónica, lleva tilde.")
    b.om(5, "¿Cambia el sentido «No, espera» frente a «No espera»?", "sí: con coma es una negación seguida de una orden; sin coma dice que alguien no espera", ["no, significan lo mismo", "solo cambia el tono", "ninguna es correcta"], "La coma puede cambiar el significado.", "La coma separa la negación de la orden y cambia el sentido.")
    b.cat(5, "¿Aguda, grave o esdrújula?", ["Aguda", "Grave", "Esdrújula"], [("canción", 0), ("reloj", 0), ("lápiz", 1), ("casa", 1), ("rápido", 2), ("música", 2)],
          "Busca la sílaba tónica.", "Canción y reloj son agudas; lápiz y casa, graves; rápido y música, esdrújulas.")
    return b.items


# ---------------- 3° medio (FG-LELI-3M) ----------------
def le3m_oac1():
    b = Autor("len", "3m", 1)
    T1 = "Cada noche, la tejedora deshacía lo que había tejido durante el día. Los pretendientes esperaban en el salón, impacientes. Ella sonreía: mientras el manto no estuviera terminado, nadie podría obligarla a elegir."
    b.om(1, "¿Qué hace la tejedora cada noche?", "deshace lo que tejió durante el día", ["teje más rápido", "vende el manto", "invita a los pretendientes"], "Lee la primera oración.", "Deshace su tejido cada noche.", texto=T1)
    b.om(3, "¿Con qué obra clásica dialoga este relato (intertextualidad)?", "la Odisea, por Penélope que teje y desteje esperando a Ulises", ["el Quijote", "Caperucita Roja", "Romeo y Julieta"], "Piensa en una esposa que espera y engaña a sus pretendientes.", "Retoma el episodio de Penélope en la Odisea.", texto=T1)
    b.om(5, "¿Qué interpretación sostiene mejor el texto?", "el tejido es una estrategia de resistencia para conservar su libertad de decidir", ["la tejedora no sabe tejer", "a la tejedora le gustan los pretendientes", "el manto es un regalo para el rey"], "¿Para qué deshace el tejido?", "Deshacer el manto le permite no ser obligada a elegir.", texto=T1)
    T2 = "El reloj de la estación marcaba siempre las seis y diez. Nadie lo arreglaba. Los viajeros lo miraban por costumbre y luego miraban sus teléfonos. Solo el viejo jefe de estación seguía creyendo que, algún día, la hora volvería a ser verdad."
    b.om(1, "¿Qué hora marca siempre el reloj?", "las seis y diez", ["las doce", "las tres y media", "ninguna"], "Busca la primera oración.", "Marca las seis y diez.", texto=T2)
    b.om(3, "¿Qué podría simbolizar el reloj detenido?", "un tiempo pasado que se resiste a desaparecer", ["la puntualidad de los trenes", "la modernidad", "la alegría de viajar"], "Relaciona el reloj con el jefe de estación.", "El reloj simboliza un pasado detenido que el jefe aún espera.", texto=T2)
    b.om(4, "¿Qué contraste construye el texto?", "entre los viajeros que viven en el presente y el jefe que se aferra al pasado", ["entre el día y la noche", "entre el campo y la ciudad", "entre dos relojes"], "Compara a los viajeros con el jefe de estación.", "Los teléfonos representan el presente; el jefe, la nostalgia.", texto=T2)
    b.cat(2, "¿Recurso narrativo o recurso lírico?", ["Narrativo", "Lírico"], [("narrador", 0), ("personajes", 0), ("tiempo del relato", 0), ("hablante lírico", 1), ("verso y rima", 1)],
          "Narrativa: narrador y personajes; lírica: hablante y verso.", "Narrador, personajes y tiempo son narrativos; hablante y verso, líricos.")
    b.co(2, "La relación de un texto con otros textos se llama ___.", "intertextualidad", ["polisemia", "narración", "rima"], "Inter-texto.", "Es la intertextualidad.")
    b.em(2, "Une cada tópico literario con un ejemplo.", [["amor imposible", "dos amantes de familias enemigas"], ["viaje del héroe", "un joven que sale de casa y vuelve transformado"], ["locus amoenus", "un paisaje idealizado y tranquilo"]], "Tópicos frecuentes de la literatura.", "Amor imposible, viaje del héroe y lugar ameno.")
    b.ord(4, "Ordena los pasos para formular una interpretación literaria.", ["Leer y comprender el sentido literal.", "Identificar recursos (narrador, símbolos, figuras).", "Proponer una interpretación.", "Fundamentarla con citas del texto."], "De la comprensión a la argumentación.", "Comprender, analizar, interpretar y fundamentar.")
    b.om(4, "¿Qué cita del texto del reloj apoya mejor la idea de nostalgia?", "«la hora volvería a ser verdad»", ["«miraban sus teléfonos»", "«Nadie lo arreglaba»", "«de la estación»"], "Busca la expresión de esperanza en el pasado.", "Esa frase muestra el deseo de que vuelva el tiempo pasado.", texto=T2)
    P = "Volveré, dijo el mar a la orilla, / y la orilla aprendió a esperar / con la paciencia de la arena."
    b.om(5, "¿Qué figura predomina en el poema?", "personificación del mar y de la orilla", ["hipérbole", "aliteración en r", "pregunta retórica"], "El mar habla y la orilla aprende.", "Mar y orilla actúan como personas.", texto=P)
    b.om(5, "¿Qué tema desarrolla el poema?", "la espera paciente de un regreso", ["la contaminación del mar", "la pesca", "la construcción de puertos"], "Fíjate en «volveré» y «esperar».", "El poema trata la espera de un regreso.", texto=P)
    b.om(1, "¿Qué es un símbolo en literatura?", "un elemento concreto que representa una idea abstracta", ["el título de un libro", "un tipo de rima", "el nombre del autor"], "Ej.: una paloma representa la paz.", "Un símbolo representa una idea.")
    b.om(3, "Si una novela retoma el mito de Ícaro (quien vuela demasiado alto y cae), ¿qué idea podría querer transmitir?", "los riesgos de la ambición desmedida", ["la importancia del deporte", "la vida en el campo", "las ventajas de volar en avión"], "Recuerda qué le pasó a Ícaro.", "El mito de Ícaro advierte sobre la ambición excesiva.")
    return b.items


def le3m_oac3():
    b = Autor("len", "3m", 3)
    T1 = "AVISO PAGADO. ¡El nuevo yogur NutriMax fortalece tus defensas! Recomendado por miles de familias chilenas. Cómpralo hoy con 30 % de descuento."
    b.om(1, "¿Cuál es el propósito principal del texto?", "persuadir para comprar un producto", ["informar una noticia", "narrar una historia", "explicar un experimento"], "Mira «AVISO PAGADO» y «Cómpralo hoy».", "Es publicidad: busca vender.", texto=T1)
    b.om(3, "¿Qué afirmación del aviso requiere más evidencia?", "que fortalece tus defensas", ["que tiene 30 % de descuento", "que es un yogur", "que es un aviso pagado"], "¿Qué dato no se puede comprobar con el aviso?", "La afirmación sobre la salud necesita respaldo científico.", texto=T1)
    b.om(5, "«Recomendado por miles de familias» es un argumento…", "de apelación a la mayoría, que no prueba que el producto funcione", ["científico muy sólido", "de autoridad médica", "estadístico preciso"], "Que muchos lo usen no prueba su efecto.", "Apelar a la mayoría no demuestra eficacia.", texto=T1)
    T2 = "Estimados vecinos: la Junta de Vecinos informa que el corte de agua será el martes de 9:00 a 14:00 por trabajos de mantención. Les pedimos guardar agua el día anterior."
    b.om(1, "¿Quién es el enunciador del texto?", "la Junta de Vecinos", ["los vecinos", "la empresa de agua", "el alcalde"], "Busca quién informa.", "Escribe la Junta de Vecinos.", texto=T2)
    b.om(2, "¿Quién es la audiencia del texto?", "los vecinos del sector", ["los turistas", "los estudiantes de un colegio", "los periodistas"], "Busca a quién se dirige.", "Se dirige a los vecinos.", texto=T2)
    b.cat(2, "¿Texto literario o no literario?", ["No literario", "Literario"], [("aviso de corte de agua", 0), ("noticia", 0), ("columna de opinión", 0), ("cuento", 1), ("poema", 1)],
          "Los no literarios cumplen funciones prácticas.", "Aviso, noticia y columna son no literarios; cuento y poema, literarios.")
    T3 = "Un estudio de una universidad chilena con 1.200 estudiantes encontró que quienes duermen menos de 6 horas obtienen, en promedio, notas más bajas. Los autores advierten que se necesitan más estudios para afirmar que una cosa causa la otra."
    b.om(3, "¿Por qué este texto es más confiable que un rumor en redes?", "porque indica la fuente, el tamaño de la muestra y los límites del estudio", ["porque es más largo", "porque usa muchas exclamaciones", "porque tiene una foto"], "Busca fuente, datos y prudencia.", "Entrega fuente, muestra y advertencias.", texto=T3)
    b.om(4, "¿Qué conclusión NO se puede sacar del estudio?", "Dormir poco causa con certeza las malas notas.", ["Hay una relación entre dormir poco y notas más bajas.", "El estudio tuvo 1.200 participantes.", "Se necesitan más estudios."], "Los autores distinguen relación de causa.", "Una correlación no prueba causalidad.", texto=T3)
    b.em(4, "Une cada género discursivo con su propósito.", [["noticia", "informar hechos recientes"], ["editorial", "expresar la opinión del medio"], ["infografía", "explicar datos de manera visual"]], "Géneros del discurso periodístico.", "Noticia, editorial e infografía.")
    b.ord(4, "Ordena los pasos para verificar una información.", ["Identificar quién la publica.", "Buscar la fuente original.", "Contrastar con otros medios confiables.", "Decidir si es verosímil."], "De la fuente a la evaluación.", "Así se verifica una información.")
    b.om(5, "¿Qué pregunta ayuda más a evaluar la veracidad de un titular impactante?", "¿Qué fuente respalda el dato y qué dicen otros medios?", ["¿Cuántos likes tiene?", "¿Me gusta el titular?", "¿Es corto?"], "La veracidad se verifica con fuentes.", "Contrastar fuentes permite evaluar la veracidad.")
    b.om(5, "Un video viral muestra a una autoridad diciendo algo polémico, pero el audio no coincide con el movimiento de los labios. ¿Qué es lo más razonable?", "sospechar que puede estar manipulado y buscar la fuente original", ["compartirlo de inmediato", "creerlo porque es un video", "ignorar todos los videos para siempre"], "Los videos también se pueden manipular.", "Las inconsistencias indican posible manipulación: hay que verificar.")
    b.co(1, "Quien emite un texto se llama ___.", "enunciador", ["audiencia", "receptor", "referente"], "Es quien produce el discurso.", "Es el enunciador (emisor).")
    b.co(3, "Un texto que relaciona causa y consecuencia usa conectores como ___.", "por lo tanto", ["sin embargo", "por ejemplo", "en cambio"], "Indica consecuencia.", "«Por lo tanto» introduce una consecuencia.")
    b.om(2, "¿Qué tipo de texto es una carta al director?", "un texto de opinión de un lector en un medio", ["un cuento", "un manual de instrucciones", "una receta"], "Se publica en diarios.", "Un lector opina en un medio de comunicación.")
    return b.items


def le3m_oac5():
    b = Autor("len", "3m", 5)
    b.om(1, "¿Qué palabra tiene léxico valorativo (expresa juicio)?", "vergonzoso", ["edificio", "martes", "kilómetro"], "Busca una que evalúe.", "«Vergonzoso» expresa una valoración negativa.")
    b.co(1, "Las palabras como «aquí», «ahora» o «yo», que dependen del contexto, se llaman ___.", "deícticos", ["sinónimos", "conectores", "adjetivos calificativos"], "Señalan persona, lugar o tiempo.", "Son deícticos.")
    b.cat(1, "¿Léxico valorativo o neutro?", ["Valorativo", "Neutro"], [("brillante", 0), ("lamentable", 0), ("heroico", 0), ("mesa", 1), ("año", 1)], "Valorativo: expresa juicio o emoción.", "Brillante, lamentable y heroico valoran; mesa y año son neutros.")
    T1 = "Ayer, el alcalde inauguró con bombos y platillos una plaza a medio terminar. Los vecinos, cansados de promesas, observaron en silencio."
    b.om(2, "¿Qué expresión muestra una postura crítica del enunciador?", "«con bombos y platillos» y «a medio terminar»", ["«Ayer»", "«una plaza»", "«los vecinos»"], "Busca palabras que evalúan.", "Esas expresiones ironizan sobre la inauguración.", texto=T1)
    b.om(2, "En el texto, «ayer» es un deíctico de…", "tiempo", ["lugar", "persona", "cantidad"], "Señala cuándo.", "«Ayer» depende del momento en que se habla: tiempo.", texto=T1)
    b.om(3, "¿Qué efecto busca «cansados de promesas»?", "que la audiencia simpatice con los vecinos y desconfíe del alcalde", ["informar con neutralidad", "elogiar al alcalde", "describir la plaza"], "Piensa en la emoción que transmite.", "Genera empatía con los vecinos.", texto=T1)
    b.em(3, "Une cada verbo con la actitud que comunica.", [["afirmó", "neutral"], ["admitió", "reconoce algo a regañadientes"], ["denunció", "acusa algo grave"]], "Los verbos de habla no son neutros.", "Afirmar es neutro; admitir implica reconocer; denunciar, acusar.")
    b.om(3, "¿Qué oración usa la voz pasiva para ocultar a quien realizó la acción?", "Se cometieron errores en el proceso.", ["El ministro cometió errores.", "Los errores los cometió el equipo.", "Yo cometí un error."], "La pasiva con «se» omite al agente.", "No dice quién cometió los errores.")
    b.ord(4, "Ordena de más neutral a más valorativo.", ["La medida fue aprobada.", "La medida fue cuestionada.", "La medida fue duramente criticada.", "La medida fue un escándalo vergonzoso."], "Observa la carga de cada expresión.", "La valoración aumenta en cada oración.")
    b.om(4, "¿Qué efecto tienen los signos de exclamación en «¡Esto no puede seguir así!»?", "intensifican la emoción y la urgencia", ["indican una pregunta", "suavizan la crítica", "citan a otra persona"], "Piensa en el tono.", "La exclamación refuerza la intensidad.")
    b.cat(4, "¿Recurso lingüístico o no lingüístico?", ["Lingüístico", "No lingüístico"], [("adjetivos valorativos", 0), ("verbos de habla", 0), ("una fotografía impactante", 1), ("colores llamativos", 1), ("tipografía grande", 1)],
          "Los lingüísticos son palabras; los no lingüísticos, imágenes y diseño.", "Adjetivos y verbos son lingüísticos; foto, colores y tipografía, no lingüísticos.")
    b.om(5, "Compara: «Estudiantes protestaron» vs. «Vándalos desordenaron». ¿Qué cambia?", "la valoración: la segunda descalifica a los participantes", ["nada, significan lo mismo", "la cantidad de personas", "el lugar de los hechos"], "Mira la elección de palabras.", "«Vándalos» carga negativamente el mismo hecho.")
    b.om(5, "¿Por qué un medio podría usar «nosotros» en una columna («nosotros los chilenos»)?", "para crear cercanía e incluir a la audiencia en su postura", ["para excluir a los lectores", "para hablar solo del autor", "por error gramatical"], "Es un deíctico de persona inclusivo.", "El «nosotros» inclusivo busca adhesión.")
    b.om(5, "En una infografía, ¿qué recurso no lingüístico puede influir en la interpretación de los datos?", "un gráfico con el eje cortado que exagera las diferencias", ["el uso de tildes", "un título con sustantivos", "un punto final"], "Piensa en cómo se presentan visualmente los datos.", "Un eje manipulado puede exagerar diferencias.")
    b.co(2, "En «Lamentablemente, el proyecto fracasó», la palabra «lamentablemente» es un ___.", "modalizador", ["deíctico", "sustantivo", "conector temporal"], "Muestra la actitud del enunciador.", "Expresa la valoración del enunciador.")
    return b.items


# ---------------- 4° medio (FG-LELI-4M) ----------------
def le4m_oac1():
    b = Autor("len", "4m", 1)
    T1 = "Dos poemas hablan del mar. El primero, escrito en 1890 por un poeta romántico, lo describe como un dios furioso que castiga a los hombres. El segundo, escrito en 2020, lo describe como un enfermo lleno de plástico."
    b.om(1, "¿Qué tema comparten los dos poemas?", "el mar", ["la guerra", "el amor", "la ciudad"], "Lee la primera oración.", "Ambos hablan del mar.", texto=T1)
    b.om(3, "¿Qué explica mejor la diferencia entre ambas miradas?", "el contexto de producción: la naturaleza poderosa en el siglo XIX y la crisis ambiental hoy", ["que los poetas no conocían el mar", "que el mar cambió de color", "que uno es más largo"], "Piensa en la época de cada poema.", "Cada época ve el mar desde sus preocupaciones.", texto=T1)
    b.om(5, "¿Qué efecto estético produce describir el mar como «un enfermo»?", "invierte la imagen del mar poderoso y genera compasión y conciencia", ["hace reír al lector", "describe técnicamente el agua", "no produce ningún efecto"], "Compara con «dios furioso».", "De dios temible pasa a víctima vulnerable: conmueve y alerta.", texto=T1)
    b.cat(2, "¿Contexto de producción o de recepción?", ["Producción", "Recepción"], [("la época en que vivió el autor", 0), ("los hechos históricos cuando se escribió", 0), ("cómo lo lee un estudiante hoy", 1), ("las preocupaciones del lector actual", 1)],
          "Producción: cuando se escribió; recepción: cuando se lee.", "La época del autor es producción; la lectura actual, recepción.")
    b.co(2, "El punto de vista desde el cual una obra presenta un tema se llama ___.", "perspectiva", ["rima", "estrofa", "título"], "También se le dice enfoque.", "Es la perspectiva.")
    b.em(2, "Une cada movimiento con un rasgo típico.", [["Romanticismo", "exaltación de la emoción y la naturaleza"], ["Realismo", "retrato fiel de la sociedad"], ["Vanguardias", "experimentación con la forma"]], "Movimientos literarios.", "Romanticismo, Realismo y Vanguardias.")
    T2 = "Una novela de 1950 presenta a la protagonista como una esposa feliz que solo espera a su marido. Una lectora de hoy la critica por mostrar a la mujer sin proyectos propios."
    b.om(3, "¿Qué muestra la crítica de la lectora actual?", "que el contexto de recepción cambia la interpretación de una obra", ["que la novela está mal escrita", "que en 1950 no había novelas", "que la lectora no leyó el libro"], "Compara la época de la novela con la de la lectora.", "Los valores de hoy permiten otra lectura.", texto=T2)
    b.om(4, "¿Qué interpretación es más fundamentada?", "la novela refleja los roles de género de su época, que hoy se cuestionan", ["la novela es actual y no tiene época", "la protagonista es una heroína moderna", "la novela trata de deportes"], "Considera ambos contextos.", "Relaciona la obra con su contexto y con la lectura actual.", texto=T2)
    b.ord(4, "Ordena los pasos para comparar dos obras sobre un mismo tema.", ["Identificar el tema común.", "Analizar la perspectiva de cada obra.", "Relacionar cada una con su contexto.", "Concluir sobre semejanzas y diferencias."], "De lo común al análisis y la conclusión.", "Así se construye una interpretación comparada.")
    b.om(4, "Dos canciones hablan de migrar: una con nostalgia por la tierra dejada y otra con esperanza por el nuevo lugar. ¿Qué las diferencia?", "la perspectiva sobre la experiencia de migrar", ["el tema", "el idioma obligatoriamente", "que una no es canción"], "Mismo tema, distinta mirada.", "Difieren en la perspectiva: nostalgia y esperanza.")
    b.om(5, "¿Por qué una obra antigua puede seguir siendo valiosa hoy?", "porque plantea preguntas humanas que siguen vigentes en otros contextos", ["porque es antigua", "porque es corta", "porque todos la conocen"], "Piensa en los temas universales.", "Sus temas universales dialogan con lectores de distintas épocas.")
    b.om(5, "Un cuento distópico de 1960 imaginó pantallas que vigilan a las personas. ¿Cómo podría leerse hoy?", "como una advertencia que dialoga con debates actuales sobre privacidad y tecnología", ["como una receta de cocina", "como un texto sin relación con el presente", "como una noticia real de 1960"], "Relaciona el tema con el presente.", "El contexto de recepción actual le da nuevos sentidos.")
    b.om(1, "¿Qué es el contexto de producción de una obra?", "las circunstancias históricas, sociales y culturales en que fue creada", ["el lugar donde se vende", "la opinión de los lectores hoy", "el número de páginas"], "Piensa en la época del autor.", "Es el momento y las condiciones en que se escribió.")
    b.om(1, "¿Qué es el «efecto estético» de una obra?", "la impresión o experiencia que produce en el lector por su forma y contenido", ["el precio del libro", "la cantidad de capítulos", "la editorial"], "Se relaciona con la belleza y la emoción.", "Es la experiencia que la obra provoca.")
    b.co(3, "Cuando una obra se lee de forma distinta según la época, decimos que cambia su contexto de ___.", "recepción", ["producción", "impresión", "edición"], "Se refiere a quien lee.", "Cambia el contexto de recepción.")
    return b.items


def le4m_oac3():
    b = Autor("len", "4m", 3)
    T1 = "Columna: «El país necesita más autopistas. Quien se oponga, simplemente no quiere que Chile progrese». Firma: presidente de la Asociación de Concesionarias Viales."
    b.om(1, "¿Cuál es la tesis de la columna?", "el país necesita más autopistas", ["las autopistas contaminan", "el transporte público es mejor", "Chile no debe progresar"], "Busca la postura que se defiende.", "Defiende la construcción de más autopistas.", texto=T1)
    b.om(3, "¿Qué intención implícita podría tener el enunciador?", "beneficiar a las empresas que construyen y administran autopistas", ["defender a los ciclistas", "reducir el uso del auto", "proteger el medio ambiente"], "Mira quién firma.", "El autor representa a las concesionarias: tiene un interés económico.", texto=T1)
    b.om(5, "¿Qué problema argumentativo tiene «quien se oponga no quiere que Chile progrese»?", "descalifica a quienes opinan distinto en lugar de responder sus argumentos", ["es un dato estadístico", "es una cita de autoridad", "es una pregunta abierta"], "¿Discute ideas o descalifica personas?", "Es una falacia que descalifica a los opositores.", texto=T1)
    T2 = "Titular A: «Gobierno reduce el desempleo a 8 %». Titular B: «Medio millón de chilenos sigue sin trabajo»."
    b.om(2, "¿Qué muestran estos dos titulares sobre el mismo dato?", "que se puede destacar un aspecto u otro según la postura del medio", ["que uno de ellos es falso", "que hablan de países distintos", "que no tienen relación"], "Mismo hecho, distinto énfasis.", "El encuadre cambia la impresión del lector.", texto=T2)
    b.om(4, "¿Qué titular tiene un encuadre más favorable al gobierno?", "el titular A", ["el titular B", "ambos por igual", "ninguno"], "¿Cuál destaca un logro?", "A destaca la reducción como un logro del gobierno.", texto=T2)
    b.cat(2, "¿Intención explícita o implícita?", ["Explícita", "Implícita"], [("«Te invitamos a votar por el candidato X»", 0), ("«Compra hoy con descuento»", 0), ("una noticia que solo entrevista a un sector", 1), ("una foto elegida para que alguien se vea mal", 1)],
          "Explícita: se dice directamente; implícita: se sugiere.", "Invitar o vender abiertamente es explícito; elegir fuentes o fotos sesgadas, implícito.")
    b.co(1, "Un conjunto de ideas y creencias que orienta la manera de ver la sociedad se llama ___.", "ideología", ["tipografía", "metáfora", "gramática"], "Influye en cómo se presentan los hechos.", "Es una ideología.")
    b.em(3, "Une cada estrategia con su efecto.", [["omitir datos que contradicen la postura", "dar una visión parcial"], ["usar solo fuentes de un sector", "sesgar la información"], ["incluir voces diversas", "dar una visión más equilibrada"]], "Piensa en la selección de información.", "Omitir y elegir fuentes sesga; incluir voces diversas equilibra.")
    b.ord(4, "Ordena los pasos para evaluar críticamente una noticia.", ["Identificar al enunciador y su posible interés.", "Distinguir hechos de opiniones.", "Revisar las fuentes citadas.", "Contrastar con otros medios."], "Del autor a la comparación.", "Así se evalúa críticamente una noticia.")
    b.om(3, "¿Qué es el «posicionamiento» del enunciador?", "la postura que adopta frente al tema", ["el lugar donde vive", "la cantidad de lectores", "la fecha del texto"], "Se refiere a su postura.", "Es la postura del enunciador ante el tema.")
    b.om(4, "Un reportaje sobre la minería solo entrevista a gerentes de empresas. ¿Qué falta?", "las voces de comunidades, trabajadores y especialistas ambientales", ["más publicidad", "un título más largo", "fotos de los gerentes"], "¿Qué perspectivas no aparecen?", "Faltan voces diversas para una visión equilibrada.")
    b.om(5, "¿Qué lectura es más crítica frente a un reportaje patrocinado por una empresa?", "considerar quién financia el contenido y contrastarlo con otras fuentes", ["creerle todo porque es largo", "rechazarlo sin leerlo", "compartirlo sin revisar"], "La crítica no es aceptar ni rechazar a ciegas.", "Hay que considerar el interés del patrocinador y contrastar.")
    b.om(5, "¿Cuál de estas afirmaciones es verificable?", "La tasa de desempleo fue de 8 % según el INE en marzo.", ["Este gobierno es el peor de la historia.", "La gente está harta.", "Todos saben que esto es así."], "Una afirmación verificable se puede comprobar con datos.", "Tiene fuente, cifra y fecha: se puede verificar.")
    b.co(2, "Cuando un medio enfoca un hecho desde un ángulo particular, se habla de ___.", "encuadre", ["rima", "estrofa", "prólogo"], "En inglés se dice «framing».", "Es el encuadre de la noticia.")
    b.om(1, "¿Qué es una intención implícita?", "un propósito que no se dice directamente, pero se puede inferir", ["un propósito que se dice claramente", "el título del texto", "la firma del autor"], "Se infiere del texto y su contexto.", "No se declara, pero se deduce.")
    return b.items


def le4m_oac4():
    b = Autor("len", "4m", 4)
    b.om(1, "¿Qué rol asume un enunciador que escribe «Como médico, les recomiendo…»?", "el de experto que aconseja", ["el de víctima", "el de vendedor", "el de humorista"], "Fíjate en «como médico».", "Se presenta como autoridad experta.")
    b.co(1, "Los recursos como imágenes, colores o tipografía son recursos ___.", "no lingüísticos", ["lingüísticos", "gramaticales", "fonéticos"], "No son palabras.", "Son recursos no lingüísticos.")
    b.cat(1, "¿Lingüístico o no lingüístico?", ["Lingüístico", "No lingüístico"], [("pronombre «nosotros»", 0), ("adjetivo «increíble»", 0), ("una foto de un niño", 1), ("música de fondo", 1), ("un logo", 1)],
          "Lingüístico = palabras.", "Pronombre y adjetivo son lingüísticos; foto, música y logo, no lingüísticos.")
    T1 = "Querida comunidad: hoy, juntos, podemos cambiar nuestro barrio. No necesitamos esperar a nadie. Los invito a la plaza este sábado: traigan guantes, ganas y a sus vecinos."
    b.om(2, "¿Qué efecto tiene el uso de «juntos» y «podemos»?", "incluir a la audiencia y motivarla a actuar", ["alejar a los vecinos", "informar con neutralidad", "criticar al municipio"], "Es un «nosotros» inclusivo.", "Integra al lector en la acción colectiva.", texto=T1)
    b.om(2, "¿Qué rol asume el enunciador ante su audiencia?", "el de un vecino que convoca y motiva", ["el de un juez", "el de un científico", "el de un vendedor"], "Mira «Querida comunidad» y «Los invito».", "Se presenta como par que convoca.", texto=T1)
    b.om(3, "¿Qué recurso aparece en «traigan guantes, ganas y a sus vecinos»?", "una enumeración que mezcla objetos y actitudes para dar cercanía", ["una pregunta retórica", "un dato estadístico", "una cita"], "Une cosas concretas y abstractas.", "La enumeración humaniza y da tono cercano.", texto=T1)
    b.em(3, "Une cada recurso con su efecto en la audiencia.", [["pregunta retórica", "invita a reflexionar"], ["dato estadístico", "da credibilidad"], ["anécdota personal", "genera empatía"]], "Cada recurso busca algo distinto.", "Reflexión, credibilidad y empatía.")
    b.om(3, "En un afiche contra el bullying, ¿qué recurso no lingüístico refuerza el mensaje?", "una imagen de un estudiante solo en un rincón", ["un código postal", "el número de página", "una tabla de precios"], "Busca uno que conmueva.", "La imagen genera empatía con la víctima.")
    b.ord(4, "Ordena de menor a mayor implicación del enunciador.", ["Se informa que la plaza será remodelada.", "La municipalidad informa la remodelación.", "Creemos que la remodelación es necesaria.", "Yo mismo lucharé para que la plaza se remodele."], "De lo impersonal a lo personal.", "La implicación aumenta del «se» al «yo».")
    b.om(4, "¿Qué cambia entre «Se tomó la decisión» y «Yo tomé la decisión»?", "en la segunda el enunciador asume la responsabilidad", ["nada, es idéntico", "la primera es más personal", "la segunda oculta al responsable"], "La construcción impersonal oculta al agente.", "Con «yo» el enunciador se hace responsable.")
    b.cat(4, "¿Busca cercanía o distancia con la audiencia?", ["Cercanía", "Distancia"], [("«Querida comunidad»", 0), ("tutear al lector", 0), ("«Se informa a los usuarios»", 1), ("lenguaje técnico y formal", 1)],
          "Piensa en el tono.", "Saludos afectuosos y el tuteo acercan; lo impersonal y técnico distancia.")
    b.om(5, "Un candidato dice «yo, como ustedes, tomo micro todos los días». ¿Qué busca?", "identificarse con la audiencia para ganar su confianza", ["informar el horario de las micros", "criticar el transporte", "presentarse como experto en buses"], "Fíjate en «como ustedes».", "Construye un rol de igual para generar adhesión.")
    b.om(5, "¿Por qué el mismo dato puede presentarse con un gráfico de barras grande y rojo, o pequeño y gris?", "porque el diseño influye en la importancia y la emoción que el lector le asigna", ["porque los datos cambian", "porque el rojo es obligatorio", "porque el gris es más preciso"], "El diseño también comunica.", "Los recursos visuales orientan la interpretación.")
    b.om(5, "¿Qué combinación de recursos construye mejor una postura de autoridad en un texto sobre salud?", "datos de fuentes oficiales, léxico técnico preciso y el rol de especialista", ["muchos signos de exclamación", "emojis y abreviaturas", "insultos a quienes opinan distinto"], "La autoridad se construye con credibilidad.", "Datos, precisión y experticia construyen autoridad.")
    b.co(2, "El enunciador que usa «nosotros» para incluir al lector emplea un nosotros ___.", "inclusivo", ["exclusivo", "formal", "plural mayestático"], "Incluye a quien lee.", "Es un nosotros inclusivo.")
    b.om(1, "¿Qué es la audiencia de un texto?", "las personas a quienes se dirige", ["el autor", "el título", "la imprenta"], "Es el destinatario.", "Es el público destinatario.")
    b.om(4, "¿Qué efecto tiene que un aviso de salud use el tuteo («Cuida tu corazón»)?", "acerca el mensaje y lo hace más personal", ["lo vuelve más técnico", "lo hace más distante", "no tiene efecto"], "Piensa en cómo se siente el lector.", "El tuteo genera cercanía.")
    return b.items


GENERADORES = {
    "1_medio.lenguaje.OA3": le1m_oa3, "1_medio.lenguaje.OA4": le1m_oa4, "1_medio.lenguaje.OA9": le1m_oa9,
    "2_medio.lenguaje.OA3": le2m_oa3, "2_medio.lenguaje.OA9": le2m_oa9, "2_medio.lenguaje.OA18": le2m_oa18,
    "3_medio.lenguaje.OA1": le3m_oac1, "3_medio.lenguaje.OA3": le3m_oac3, "3_medio.lenguaje.OA5": le3m_oac5,
    "4_medio.lenguaje.OA1": le4m_oac1, "4_medio.lenguaje.OA3": le4m_oac3, "4_medio.lenguaje.OA4": le4m_oac4,
}
