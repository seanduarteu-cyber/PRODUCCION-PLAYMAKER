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


GENERADORES = {
    "1_medio.lenguaje.OA3": le1m_oa3, "1_medio.lenguaje.OA4": le1m_oa4, "1_medio.lenguaje.OA9": le1m_oa9,
    "2_medio.lenguaje.OA3": le2m_oa3, "2_medio.lenguaje.OA9": le2m_oa9, "2_medio.lenguaje.OA18": le2m_oa18,
}
