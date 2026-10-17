"""Inglés 1° a 4° medio: 15 desafíos por OA (3 por nivel de dificultad, 1 a 5).
Lectura con textos breves originales; escritura con las funciones de cada curso; algunos desafíos con audio en inglés."""
from autor import Autor

V_F = ["True", "False", "Not mentioned"]


# ---------------- 1° medio ----------------
def in1m_oa9():
    b = Autor("ing", "1m", 9)
    T1 = "Valparaíso is famous for its colourful houses on the hills. Visitors ride old funiculars called «ascensores» to go up. Many artists paint murals on the walls, so the city looks like an open-air museum."
    b.om(1, "¿Por qué es famosa Valparaíso según el texto?", "por sus casas de colores en los cerros", ["por sus playas de arena blanca", "por sus edificios muy altos", "por su clima frío"], "Busca «famous for».", "«Famous for its colourful houses on the hills».", texto=T1)
    b.co(2, "Visitors use old ___ to go up the hills.", "funiculars", ["buses", "bicycles", "boats"], "Busca «ride».", "«Visitors ride old funiculars called ascensores».", texto=T1)
    b.om(3, "¿Por qué la ciudad parece «an open-air museum»?", "porque hay muchos murales en las paredes", ["porque tiene muchos museos cerrados", "porque las casas son antiguas", "porque no se permite pintar"], "Mira la palabra «so».", "Los artistas pintan murales; por eso parece un museo al aire libre.", texto=T1)
    T2 = "Hi Tomás! I'm in Puerto Natales with my family. Yesterday we visited Torres del Paine. It was windy and cold, but the mountains were amazing. Tomorrow we're taking a boat to see a glacier. See you next week! – Sofía"
    b.om(1, "¿Dónde está Sofía?", "en Puerto Natales", ["en Santiago", "en Valparaíso", "en Arica"], "Lee la segunda oración.", "«I'm in Puerto Natales with my family».", texto=T2)
    b.cat(2, "¿Verdadero, falso o no se menciona?", V_F, [("They visited Torres del Paine yesterday.", 0), ("The weather was hot.", 1), ("Sofía travelled by plane.", 2), ("They will see a glacier.", 0)],
          "Busca cada dato en el texto.", "Visitaron Torres del Paine y verán un glaciar; hacía frío (no calor); no dice cómo viajaron.", texto=T2)
    b.ord(3, "Ordena lo que hace Sofía.", ["visit Torres del Paine", "write to Tomás", "take a boat to a glacier", "see Tomás"],
          "Fíjate en yesterday, now, tomorrow y next week.", "Ayer el parque, hoy escribe, mañana el bote y la próxima semana ve a Tomás.", texto=T2)
    T3 = "Many teenagers sleep less than eight hours a night. Experts say this affects their memory and mood. Phones are part of the problem: the blue light from screens tells the brain that it is still daytime. A simple tip is to leave the phone outside the bedroom."
    b.om(4, "What is the main idea of the text?", "Teenagers don't sleep enough, and phones are part of the problem.", ["Phones help teenagers sleep better.", "Experts sleep more than eight hours.", "Blue light is good for memory."],
         "La idea principal resume todo el texto, no un detalle.", "El texto habla de que los adolescentes duermen poco y del papel de los celulares.", texto=T3)
    b.co(4, "Blue light tells the brain that it is still ___.", "daytime", ["night", "winter", "asleep"], "Busca «blue light».", "«Tells the brain that it is still daytime».", texto=T3)
    b.em(4, "Une cada parte del texto con su función.", [["Many teenagers sleep less than eight hours.", "problema"], ["It affects memory and mood.", "consecuencia"], ["Leave the phone outside the bedroom.", "solución"]],
         "Piensa en problema, consecuencia y solución.", "Primero el problema, luego su efecto y al final un consejo.", texto=T3)
    T4 = "The Atacama Desert is one of the driest places on Earth. Some areas haven't had rain for years. However, after a rare rainy winter, the desert can bloom with thousands of purple and pink flowers. People call this event «desierto florido»."
    b.om(5, "¿Qué palabra muestra un contraste en el texto?", "However", ["after", "people", "thousands"], "Busca un conector que cambie la idea.", "«However» contrasta la sequía con la floración.", texto=T4)
    b.om(5, "What can we infer about «desierto florido»?", "It doesn't happen every year.", ["It happens every summer.", "It only has white flowers.", "It happens in the south of Chile."],
         "«Rare rainy winter»: ¿es algo frecuente?", "Ocurre tras un invierno lluvioso poco común, así que no es todos los años.", texto=T4)
    b.om(5, "¿Cuál es el propósito del texto?", "informar sobre un fenómeno natural", ["vender un viaje", "dar una opinión sobre el clima", "contar un cuento"], "¿Qué hace el texto: informa, convence o narra?", "Explica qué es el desierto florido: informa.", texto=T4)
    b.om(1, "Escucha. ¿Qué día es el examen?", "el viernes", ["el lunes", "el miércoles", "el domingo"], "Escucha el día de la semana.", "Dice: «The English test is on Friday».", audio="Remember, the English test is on Friday.")
    b.om(2, "Escucha. ¿Qué necesita llevar el curso?", "un diccionario", ["un computador", "una calculadora", "un libro de cuentos"], "Escucha qué deben llevar.", "Dice: «bring a dictionary».", audio="For tomorrow's class, please bring a dictionary.")
    b.om(3, "Escucha el aviso. ¿Por qué se suspende la salida?", "por la lluvia", ["por un paro", "por el calor", "porque el bus está lleno"], "Escucha «because of».", "Dice: «because of the heavy rain».", audio="The school trip is cancelled because of the heavy rain.")
    return b.items


def in1m_oa10():
    b = Autor("ing", "1m", 10)
    T1 = "LOST DOG – Have you seen Toby? He is a small brown dog with a red collar. He got lost near Plaza Ñuñoa on Saturday. If you find him, please call 9 1234 5678. Reward!"
    b.om(1, "What kind of text is this?", "a notice", ["a poem", "a recipe", "a biography"], "Mira el título en mayúsculas y el teléfono.", "Es un aviso (notice) de perro perdido.", texto=T1)
    b.co(1, "Toby has a red ___.", "collar", ["hat", "ball", "bed"], "Busca la descripción del perro.", "«A small brown dog with a red collar».", texto=T1)
    b.om(2, "¿Cuál es el propósito del aviso?", "pedir ayuda para encontrar al perro", ["vender un perro", "invitar a una fiesta", "informar el clima"], "¿Para qué se escribe un «LOST DOG»?", "Pide ayuda para encontrar a Toby.", texto=T1)
    T2 = "From: Diego  To: Ms. Rojas  Subject: Homework\nDear Ms. Rojas, I couldn't send my essay yesterday because the internet was down at home. I have attached it now. I'm sorry for the delay. Best regards, Diego"
    b.om(2, "Why did Diego write the email?", "to send his essay late and apologise", ["to ask for more homework", "to complain about the teacher", "to invite Ms. Rojas"], "Lee la razón y lo que adjunta.", "Envía su ensayo atrasado y se disculpa.", texto=T2)
    b.cat(2, "¿Verdadero, falso o no se menciona?", V_F, [("The internet was down.", 0), ("Diego sent the essay on time.", 1), ("The essay is about Chile.", 2), ("Diego apologises.", 0)],
          "Revisa cada dato.", "Se cayó internet y se disculpa; no lo envió a tiempo; no dice el tema.", texto=T2)
    b.em(3, "Une cada expresión con su función en el email.", [["Dear Ms. Rojas", "saludo"], ["because the internet was down", "causa"], ["I'm sorry for the delay", "disculpa"], ["Best regards", "despedida"]],
         "Piensa en la estructura de un email formal.", "Saludo, causa, disculpa y despedida.", texto=T2)
    T3 = "Plastic bags take hundreds of years to break down. In 2018, Chile became the first country in Latin America to ban plastic bags in shops. As a result, people now bring their own reusable bags. Some shoppers complained at first, but most got used to it."
    b.om(3, "What was the result of the ban?", "People bring reusable bags.", ["Shops sell more plastic bags.", "People stopped shopping.", "Plastic now breaks down fast."], "Busca «as a result».", "«As a result, people now bring their own reusable bags».", texto=T3)
    b.om(4, "¿Qué relación muestra «Some shoppers complained at first, but most got used to it»?", "contraste", ["causa", "ejemplo", "secuencia"], "Fíjate en «but».", "«But» opone dos ideas: contraste.", texto=T3)
    b.om(4, "In the text, «ban» means…", "prohibir", ["vender", "reciclar", "regalar"], "Si se prohíben, la gente trae sus propias bolsas.", "«Ban» es prohibir.", texto=T3)
    T4 = "Problem: many students arrive late because buses are full in the morning. Solution: our school will start classes 30 minutes later on Mondays, when traffic is worse. We will check the results in June."
    b.em(4, "Une cada parte con su contenido.", [["Problem", "buses are full in the morning"], ["Solution", "start 30 minutes later on Mondays"], ["Next step", "check the results in June"]],
         "El texto usa la estructura problema–solución.", "Problema: buses llenos; solución: empezar más tarde; después: revisar en junio.", texto=T4)
    b.om(5, "¿Por qué la solución se aplica solo los lunes?", "porque el tráfico es peor ese día", ["porque no hay clases los lunes", "porque los buses son gratis", "porque lo pidió el profesor"], "Busca «when traffic is worse».", "Los lunes el tráfico es peor.", texto=T4)
    b.om(5, "What can we infer about the plan?", "The school is not sure yet if it will work.", ["The plan has already failed.", "Students don't like buses.", "Classes will start earlier."], "¿Por qué revisarán los resultados?", "Si van a revisar los resultados, aún no saben si funciona.", texto=T4)
    T5 = "Violeta Parra (1917–1967) was a Chilean singer, composer and artist. She travelled around Chile collecting traditional songs. She also made colourful embroidered pictures called «arpilleras». Her song «Gracias a la vida» is known around the world."
    b.ord(1, "Ordena las palabras para formar la pregunta.", ["What", "did", "Violeta", "Parra", "collect?"], "Pregunta en pasado: What + did + sujeto + verbo.", "What did Violeta Parra collect?", texto=T5)
    b.co(3, "Violeta Parra was a singer, composer ___ artist.", "and", ["but", "because", "so"], "Es una lista.", "Las listas se unen con «and».", texto=T5)
    b.om(5, "What is the purpose of this text?", "to give basic facts about a person's life", ["to persuade people to sing", "to tell a funny story", "to explain how to make arpilleras"], "Es una biografía breve.", "Entrega datos de su vida: es una biografía.", texto=T5)
    return b.items


def in1m_oa16():
    b = Autor("ing", "1m", 16)
    b.co(1, "When I was a child, I ___ play in the park every day.", "used to", ["use to", "am used", "using to"], "Hábito pasado: used to + verbo.", "«I used to play» expresa un hábito pasado.")
    b.co(1, "She has ___ in Concepción since 2020.", "lived", ["live", "living", "lives"], "Present perfect: has + participio.", "«She has lived» (present perfect).")
    b.om(1, "¿Qué oración describe un hábito del pasado?", "My grandfather used to ride a horse to school.", ["My grandfather rides a horse now.", "My grandfather will ride a horse.", "My grandfather is riding a horse."], "Busca «used to».", "«Used to» indica algo que se hacía antes.")
    b.co(2, "The girl ___ won the contest is my cousin.", "who", ["which", "where", "when"], "Para personas se usa «who».", "«The girl who won…»: relativo para personas.")
    b.co(2, "This is the house ___ I was born.", "where", ["who", "which", "when"], "Para lugares se usa «where».", "«The house where I was born».")
    b.cat(2, "¿Present perfect o pasado simple?", ["Present perfect", "Past simple"], [("I have visited Chiloé.", 0), ("She has finished her homework.", 0), ("We went to Arica last year.", 1), ("They saw a whale yesterday.", 1)],
          "Las marcas de tiempo definido (yesterday, last year) van con pasado simple.", "Have/has + participio es present perfect; went y saw, pasado simple.")
    b.co(3, "Empanadas ___ in many Chilean homes on September 18th.", "are eaten", ["eat", "are eating", "ate"], "Voz pasiva: be + participio.", "«Empanadas are eaten»: voz pasiva en presente.")
    b.ord(3, "Ordena la oración en voz pasiva.", ["The", "bridge", "was", "built", "in", "1990."], "Sujeto + was + participio.", "The bridge was built in 1990.")
    b.em(3, "Une cada inicio con su final.", [["I have known Ana", "since we were six."], ["The book which you lent me", "was great."], ["Copper is exported", "to many countries."]],
         "Revisa el sentido y la gramática.", "since + punto de partida; relativo «which» para cosas; voz pasiva «is exported».")
    b.co(4, "___ it was raining, we went to the beach.", "Although", ["Because", "So that", "Unless"], "Une dos ideas opuestas.", "«Although» introduce un contraste: llovía, pero fuimos.")
    b.co(4, "I'm saving money so ___ I can buy a bike.", "that", ["what", "which", "because"], "Expresa propósito: so that.", "«So that» expresa finalidad.")
    b.om(4, "¿Qué oración está bien escrita?", "I haven't seen that film yet.", ["I didn't seen that film yet.", "I haven't saw that film yet.", "I not have seen that film yet."], "Present perfect negativo: haven't + participio.", "«Haven't seen» es la forma correcta.")
    b.om(5, "Elige la mejor forma de unir: «The museum is in Santiago. It has a famous painting.»", "The museum, which is in Santiago, has a famous painting.", ["The museum who is in Santiago has a famous painting.", "The museum where is in Santiago has a famous painting.", "The museum, it is in Santiago, has a famous painting."],
         "Para cosas se usa «which».", "«Which» introduce información adicional sobre el museo.")
    b.om(5, "Escucha y elige la oración que oíste.", "The new library was opened last month.", ["The new library opened me last month.", "The new library is opening next month.", "The new library has been closed."], "Fíjate en el tiempo verbal.", "Dice «was opened last month»: voz pasiva en pasado.", audio="The new library was opened last month.")
    b.cat(5, "¿Qué función cumple cada oración?", ["Hábito pasado", "Experiencia hasta hoy", "Proceso (voz pasiva)"],
          [("We used to live in Temuco.", 0), ("I used to hate vegetables.", 0), ("She has climbed a volcano.", 1), ("We have never seen snow.", 1), ("Wine is made from grapes.", 2), ("The letters were sent by post.", 2)],
          "used to / have + participio / be + participio.", "Used to: hábitos; present perfect: experiencias; be + participio: procesos.")
    return b.items


# ---------------- 2° medio ----------------
def in2m_oa10():
    b = Autor("ing", "2m", 10)
    T1 = "SUMMER JOB! The Valdivia Aquarium is looking for students aged 16–18 to help with school visits in January. You must be friendly and speak some English. Send your CV to jobs@aquarium.cl before December 1st."
    b.om(1, "What is the text about?", "a summer job for students", ["a new fish species", "a school trip to Valdivia", "a swimming class"], "Mira el título.", "Es un aviso de trabajo de verano.", texto=T1)
    b.co(1, "Applicants must be friendly and speak some ___.", "English", ["French", "Mapudungun", "Chinese"], "Busca «You must…».", "«Speak some English».", texto=T1)
    b.cat(2, "¿Verdadero, falso o no se menciona?", V_F, [("The job is in January.", 0), ("You must be over 20.", 1), ("The job pays very well.", 2), ("You send a CV by email.", 0)],
          "Revisa edad, fecha y sueldo.", "Enero y CV por email: verdadero; edad 16–18: falso; sueldo: no se menciona.", texto=T1)
    T2 = "Fast fashion means cheap clothes produced very quickly. The problem is that it creates huge amounts of waste: in the Atacama Desert there are mountains of old clothes from other countries. One solution is to buy second-hand clothes or to repair the ones we have."
    b.om(2, "What is the main problem described?", "Fast fashion creates a lot of waste.", ["Clothes are too expensive.", "The desert is too hot.", "People don't buy clothes."], "Busca «The problem is…».", "El problema es la enorme cantidad de desechos.", texto=T2)
    b.em(3, "Une cada parte con su función.", [["Fast fashion means cheap clothes…", "definición"], ["mountains of old clothes in Atacama", "ejemplo"], ["buy second-hand or repair", "solución"]],
         "Definición, ejemplo y solución.", "Primero define, luego da un ejemplo del problema y al final propone soluciones.", texto=T2)
    b.om(3, "In the text, «second-hand» clothes are…", "clothes that someone used before", ["clothes made by hand", "very expensive clothes", "clothes for sports"], "Piensa en «de segunda mano».", "«Second-hand» es usado, de segunda mano.", texto=T2)
    T3 = "Most important rule at the pool: always take a shower before swimming. Also, children under 12 must be with an adult. Running is not allowed, and food must stay outside the pool area."
    b.om(4, "According to the text, what is the MOST important rule?", "take a shower before swimming", ["don't run", "eat outside", "come with friends"], "Busca «most important».", "La regla más importante es ducharse antes de nadar.", texto=T3)
    b.cat(4, "¿Está permitido o prohibido?", ["Allowed / required", "Not allowed"], [("Showering before swimming", 0), ("A child of 8 with his mother", 0), ("Running near the pool", 1), ("Eating by the water", 1)],
          "Lee las reglas una por una.", "Ducharse y niños con adulto: sí; correr y comer en la piscina: no.", texto=T3)
    b.om(4, "¿Qué conector agrega una regla más?", "Also", ["but", "before", "under"], "Busca una palabra que sume información.", "«Also» agrega información.", texto=T3)
    T4 = "Some people think homework should be banned. They say students need time to rest and do sports. Others argue that homework helps students practise and become responsible. Perhaps the answer is less homework, but better homework."
    b.om(5, "What is the purpose of the last sentence?", "to suggest a middle position", ["to support banning homework", "to give an example", "to describe a sport"], "Compara la última oración con las dos posturas.", "Propone un punto intermedio: menos tareas, pero mejores.", texto=T4)
    b.om(5, "¿Qué conector introduce la postura contraria?", "Others argue that", ["Some people think", "They say", "Perhaps"], "Busca dónde cambia la opinión.", "«Others argue that» presenta la postura opuesta.", texto=T4)
    b.om(5, "Escucha. ¿Qué quiere decir la persona?", "Prefiere quedarse en casa porque está cansada.", ["Quiere salir a correr.", "Está enojada con su amiga.", "Tiene hambre."], "Escucha «I'd rather» y «tired».", "Dice que está cansada y prefiere quedarse en casa.", audio="Thanks for the invitation, but I'm really tired. I'd rather stay at home tonight.")
    b.om(1, "Escucha. ¿A qué hora parte el bus?", "a las 7:30", ["a las 7:00", "a las 8:30", "a las 6:30"], "Escucha la hora.", "Dice «at seven thirty».", audio="The bus leaves at seven thirty, so don't be late.")
    b.om(2, "Escucha el aviso. ¿Dónde es la reunión?", "en la biblioteca", ["en el gimnasio", "en la sala 12", "en el patio"], "Escucha el lugar.", "Dice «in the library».", audio="The student council meeting will be in the library after lunch.")
    b.om(3, "Escucha. ¿Cuál es el problema?", "Se le olvidó la clave del wifi.", ["El computador está roto.", "No tiene celular.", "Llegó tarde a clases."], "Escucha «forgot».", "Dice que olvidó la contraseña del wifi.", audio="I can't connect. I forgot the wifi password.")
    return b.items


def in2m_oa11():
    b = Autor("ing", "2m", 11)
    T1 = "Every night, old Pedro walked to the lighthouse to turn on the light. One stormy night he was too ill to go. His granddaughter Ema, who was afraid of the dark, took his lantern and climbed the hill alone. The ships passed safely."
    b.om(1, "Who is the main character who solves the problem?", "Ema", ["Pedro", "a sailor", "a ship"], "¿Quién sube al faro?", "Ema toma la linterna y sube sola.", texto=T1)
    b.om(2, "What is the conflict of the story?", "Pedro is ill and can't turn on the light.", ["Ema loses her lantern.", "A ship sinks.", "Pedro is afraid of the dark."], "¿Qué problema aparece?", "El abuelo está enfermo y nadie enciende el faro.", texto=T1)
    b.om(4, "What does Ema's action show about her?", "She is brave.", ["She is lazy.", "She is rude.", "She is always calm."], "Ema tenía miedo a la oscuridad, pero igual fue.", "Vence su miedo para ayudar: es valiente.", texto=T1)
    T2 = "The wind sings / through the empty streets, / the moon is a silver coin / that nobody can spend."
    b.om(2, "¿Qué figura es «the moon is a silver coin»?", "metáfora", ["comparación con «like»", "rima", "pregunta"], "Dice que la luna ES una moneda, sin «like».", "Es una metáfora.", texto=T2)
    b.om(3, "«The wind sings» is an example of…", "personification", ["simile", "rhyme", "alliteration"], "El viento hace algo humano.", "Cantar es humano: personificación.", texto=T2)
    b.om(5, "What is the mood of the poem?", "quiet and lonely", ["happy and noisy", "angry and violent", "funny"], "Fíjate en «empty streets» y «nobody».", "Calles vacías y nadie: ambiente solitario y tranquilo.", texto=T2)
    T3 = "Long ago, the Mapuche say, two giant snakes fought: Kai Kai, who lived in the sea, made the water rise. Tren Tren, who lived in the mountains, raised the hills higher and higher to save the people. That is why Chile has so many mountains."
    b.co(1, "This text is a ___: it explains the origin of something with fantastic creatures.", "myth", ["news report", "recipe", "biography"], "Seres fantásticos que explican el origen de algo.", "Es un mito: explica el origen de las montañas.", texto=T3)
    b.em(3, "Une cada personaje con lo que hace.", [["Kai Kai", "makes the water rise"], ["Tren Tren", "raises the hills"], ["the people", "are saved"]],
         "Busca qué hace cada uno.", "Kai Kai sube el agua; Tren Tren eleva los cerros y salva a la gente.", texto=T3)
    b.om(4, "What does the myth explain?", "why Chile has many mountains", ["why snakes live in the sea", "how to build a house", "why it rains in winter"], "Lee la última oración.", "«That is why Chile has so many mountains».", texto=T3)
    T4 = "Sam's phone buzzed: «Meet me at the old station at midnight.» No name. Sam looked out of the window. The streets were dark and wet. He put on his jacket, then stopped. «What if it's a trap?» he whispered."
    b.ord(2, "Ordena lo que pasa en la historia.", ["Sam gets a message.", "He looks out of the window.", "He puts on his jacket.", "He stops and doubts."], "Sigue el orden del texto.", "Mensaje, ventana, chaqueta y duda.", texto=T4)
    b.om(3, "Where does the story take place?", "in a dark, rainy town at night", ["on a sunny beach", "in a school in the morning", "in the countryside at noon"], "Busca pistas del ambiente.", "Calles oscuras y mojadas, a medianoche.", texto=T4)
    b.om(5, "What is the effect of the ending?", "It creates suspense.", ["It solves the mystery.", "It makes the story funny.", "It describes the station."], "La historia termina con una pregunta.", "Termina sin resolver, con una duda: crea suspenso.", texto=T4)
    T5 = "In the song, the singer remembers summers at her grandmother's house in Chiloé: the smell of bread, the rain on the roof and the warmth of the fire. «Those days are gone,» she sings, «but they live in me.»"
    b.em(4, "Une cada imagen de la canción con el sentido que evoca.", [["the smell of bread", "olfato"], ["the rain on the roof", "oído"], ["the warmth of the fire", "tacto"]],
         "Piensa con qué sentido se percibe cada cosa.", "El pan se huele, la lluvia se escucha y el calor del fuego se siente.", texto=T5)
    b.om(5, "What is the theme of the song?", "memories of childhood and family", ["the dangers of rain", "how to bake bread", "a trip to the city"], "¿De qué trata en el fondo?", "Recuerda los veranos con su abuela: memoria y familia.", texto=T5)
    b.om(1, "Escucha. ¿Cómo empieza la historia?", "Había una vez un rey muy pobre.", ["Había una vez una reina muy rica.", "El rey era un niño.", "La historia termina bien."], "Escucha «poor king».", "Dice «a very poor king».", audio="Once upon a time, there was a very poor king.")
    return b.items


def in2m_oa16():
    b = Autor("ing", "2m", 16)
    b.co(1, "First, we packed our bags. ___, we drove to the coast.", "Then", ["Although", "Because", "Unless"], "Conector de secuencia.", "«Then» indica lo que pasó después.")
    b.co(1, "If I ___ you, I would study for the test.", "were", ["am", "will be", "being"], "Situación hipotética: If I were…", "Con situaciones hipotéticas se usa «If I were».")
    b.om(1, "¿Qué oración da un consejo?", "You should drink more water.", ["You drank more water.", "You are drinking water.", "You have drunk water."], "Los consejos usan «should».", "«You should…» da un consejo.")
    b.co(2, "She said that she ___ tired.", "was", ["is being", "be", "will"], "Estilo indirecto: el presente pasa a pasado.", "«I am tired» → «She said that she was tired».")
    b.ord(2, "Ordena el consejo.", ["You", "shouldn't", "stay", "up", "so", "late."], "Sujeto + shouldn't + verbo.", "You shouldn't stay up so late.")
    b.cat(2, "¿Qué expresa cada oración?", ["Consejo", "Situación hipotética"], [("You ought to see a doctor.", 0), ("Why don't you call her?", 0), ("If I won the lottery, I'd travel.", 1), ("If we lived by the sea, we'd surf.", 1)],
          "Should/ought to/why don't you dan consejos; if + pasado imagina.", "Los consejos sugieren; las hipotéticas imaginan algo irreal.")
    b.co(3, "He told me that he ___ the film the day before.", "had seen", ["has seen", "sees", "will see"], "Estilo indirecto: el pasado pasa a past perfect.", "«I saw the film yesterday» → «he had seen the film the day before».")
    b.co(3, "If it rains tomorrow, we ___ the match.", "will cancel", ["would cancel", "cancelled", "cancelling"], "Condicional real: if + presente, will + verbo.", "Es posible que llueva: «we will cancel».")
    b.em(3, "Une la frase directa con su versión indirecta.", [["«I'm hungry.»", "She said she was hungry."], ["«I can swim.»", "He said he could swim."], ["«We will help.»", "They said they would help."]],
         "Cada verbo retrocede un tiempo.", "am → was, can → could, will → would.")
    b.ord(4, "Ordena el relato en el tiempo.", ["We woke up early.", "After breakfast, we took the bus.", "When we arrived, it started to rain.", "Finally, we went back home."], "Busca los conectores de secuencia.", "Despertar, desayuno y bus, llegada con lluvia y regreso.")
    b.om(4, "¿Qué oración está bien escrita?", "If I had more time, I would learn to play the guitar.", ["If I have more time, I would learned the guitar.", "If I would have time, I learn the guitar.", "If I had more time, I will learning the guitar."], "Segundo condicional: if + pasado, would + verbo.", "«If I had…, I would learn…» es la estructura correcta.")
    b.co(4, "The teacher asked us ___ we had finished.", "if", ["that", "what", "so"], "Pregunta de sí o no en estilo indirecto.", "«Have you finished?» → «asked us if we had finished».")
    b.om(5, "Tu amigo dice: «I always feel tired in class.» ¿Qué consejo es más adecuado?", "Maybe you should go to bed earlier.", ["You went to bed earlier.", "If you go to bed, I am tired.", "You must to sleep in class."], "Busca un consejo amable y bien escrito.", "«Maybe you should…» es un consejo correcto y respetuoso.")
    b.om(5, "Escucha y elige lo que la persona dijo, en estilo indirecto.", "She said she would call me later.", ["She said she calls me now.", "She said she had called me yesterday.", "She says she will never call."], "«I'll call you later» → would call… later.", "«I'll call you later» pasa a «she would call me later».", audio="I'll call you later.")
    b.cat(5, "¿Qué conector usarías?", ["Secuencia", "Contraste", "Causa"], [("first / then / finally", 0), ("after that", 0), ("however", 1), ("although", 1), ("because", 2), ("since", 2)],
          "Piensa en la función de cada conector.", "Secuencia ordena, contraste opone y causa explica por qué.")
    return b.items


# ---------------- 3° medio ----------------
def in3m_oa1():
    b = Autor("ing", "3m", 1)
    T1 = "In Japan, students clean their classrooms every day. There are no cleaning staff in many schools. Teachers say this teaches responsibility and respect for shared spaces. Some foreign visitors are surprised, but students see it as normal."
    b.om(1, "What do Japanese students do every day, according to the text?", "clean their classrooms", ["cook lunch for teachers", "work in shops", "paint the school"], "Lee la primera oración.", "«Students clean their classrooms every day».", texto=T1)
    b.om(3, "Why do teachers support this practice?", "It teaches responsibility and respect.", ["It saves time for lessons.", "Students enjoy it a lot.", "It is a new law."], "Busca «Teachers say…».", "Dicen que enseña responsabilidad y respeto por los espacios compartidos.", texto=T1)
    b.om(5, "¿Qué muestra el texto sobre otras culturas?", "que una costumbre normal en un país puede sorprender en otro", ["que en Japón no hay profesores", "que los visitantes deben limpiar", "que todas las escuelas son iguales"], "Mira la última oración.", "A los visitantes les sorprende lo que para los estudiantes es normal.", texto=T1)
    T2 = "In Finland, many families leave babies to nap outside in their prams, even in winter. Parents believe fresh air helps children sleep better and stay healthy. For many people from warmer countries, this looks dangerous, but Finnish doctors say it is safe if the baby is dressed properly."
    b.cat(2, "¿Verdadero, falso o no se menciona?", V_F, [("Babies nap outside in winter.", 0), ("Finnish doctors say it is always dangerous.", 1), ("Parents believe fresh air helps sleep.", 0), ("Most Finnish babies are born in summer.", 2)],
          "Revisa cada afirmación.", "Duermen afuera y los padres creen que ayuda: verdadero; los médicos dicen que es seguro: falso; los nacimientos: no se mencionan.", texto=T2)
    b.co(2, "Finnish doctors say it is safe if the baby is ___ properly.", "dressed", ["fed", "washed", "carried"], "Busca la condición al final.", "«If the baby is dressed properly».", texto=T2)
    b.om(4, "What is the writer's attitude?", "neutral: the writer explains different views", ["angry with Finnish parents", "worried about babies", "funny and sarcastic"], "¿El autor critica o explica?", "Presenta la costumbre y las distintas miradas sin juzgar.", texto=T2)
    T3 = "Podcast transcript: «Hi, I'm Marta from Colombia. Here we say 'ahorita' a lot. It can mean 'right now', but sometimes it means 'later' or even 'maybe never'! Foreigners get confused, so ask: 'ahorita ahorita?'»"
    b.om(3, "Why do foreigners get confused?", "because «ahorita» can mean different times", ["because Marta speaks too fast", "because Colombia has many languages", "because «ahorita» is a rude word"], "Busca «It can mean…, but sometimes…».", "La palabra puede significar ahora, más tarde o nunca.", texto=T3)
    b.om(4, "What is Marta's advice?", "to ask again to check the meaning", ["to stop using the word", "to learn Spanish in a week", "to wait patiently forever"], "Lee el final.", "Recomienda preguntar «¿ahorita ahorita?» para confirmar.", texto=T3)
    b.om(5, "What is the main purpose of the podcast segment?", "to explain a cultural use of language", ["to sell a Spanish course", "to complain about foreigners", "to describe Colombian food"], "¿Qué enseña Marta?", "Explica cómo se usa una palabra en su cultura.", texto=T3)
    T4 = "Around the world, people greet each other differently. In Chile, friends often kiss on one cheek. In Japan, people usually bow. In Thailand, they press their hands together. In the United States, a handshake or a hug is common."
    b.em(1, "Une cada país con su saludo.", [["Chile", "one kiss on the cheek"], ["Japan", "a bow"], ["Thailand", "hands pressed together"]], "Busca cada país en el texto.", "Chile: un beso; Japón: reverencia; Tailandia: manos juntas.", texto=T4)
    b.om(2, "What is the text mainly about?", "different ways of greeting around the world", ["how to travel to Japan", "the history of handshakes", "why Chileans kiss"], "¿Qué tienen en común todos los ejemplos?", "Compara saludos en distintos países.", texto=T4)
    b.om(5, "A Chilean student greets a Japanese host with a kiss on the cheek. Why might the host feel uncomfortable?", "because in Japan people usually bow instead", ["because Japanese people never greet", "because kisses are only for children in Chile", "because handshakes are illegal in Japan"],
         "Compara las costumbres de ambos países.", "En Japón se saluda con una reverencia; un beso puede resultar inesperado.", texto=T4)
    b.om(1, "Escucha. ¿Qué celebra la persona?", "el Año Nuevo Lunar", ["Navidad", "Fiestas Patrias", "su cumpleaños"], "Escucha «Lunar New Year».", "Dice «we celebrate the Lunar New Year».", audio="In my family we celebrate the Lunar New Year with a big dinner.")
    b.om(4, "Escucha. ¿Qué no se debe hacer en ese país?", "dejar propina", ["sacar fotos", "saludar con la mano", "comer con palillos"], "Escucha «tip».", "Dice que dejar propina puede ser mal visto.", audio="In Japan, leaving a tip can be seen as rude.")
    b.om(3, "Escucha la opinión. ¿Qué piensa la persona del intercambio?", "Le cambió la forma de ver el mundo.", ["Fue aburrido.", "Fue muy caro.", "No aprendió nada."], "Escucha «changed the way I see».", "Dice que el intercambio cambió su forma de ver el mundo.", audio="My exchange year in Canada changed the way I see the world.")
    return b.items


def in3m_oa2():
    b = Autor("ing", "3m", 2)
    b.co(1, "In my ___, social media can be harmful for teenagers.", "opinion", ["opinions", "opine", "opinionated"], "Expresión fija para opinar: In my…", "«In my opinion» introduce una opinión.")
    b.co(1, "I ___ that cities should have more bike lanes.", "believe", ["believes", "believing", "am believe"], "Sujeto I + verbo en presente.", "«I believe that…».")
    b.om(1, "¿Qué frase introduce una opinión personal?", "From my point of view,", ["According to the data,", "In 1990,", "First of all, the map shows"], "Busca la que expresa tu punto de vista.", "«From my point of view» introduce una opinión.")
    b.co(2, "I see your point, ___ I don't completely agree.", "but", ["so", "because", "and then"], "Expresa contraste respetuoso.", "«I see your point, but…» discrepa con respeto.")
    b.cat(2, "¿Opinión o hecho?", ["Opinion", "Fact"], [("Online classes are boring.", 0), ("Football is the best sport.", 0), ("Chile has 16 regions.", 1), ("Water boils at 100 °C at sea level.", 1)],
          "Un hecho se puede comprobar; una opinión no.", "Aburrido y el mejor son opiniones; las regiones y la ebullición se comprueban.")
    b.ord(2, "Ordena la oración.", ["I", "strongly", "agree", "with", "this", "idea."], "Sujeto + adverbio + verbo.", "I strongly agree with this idea.")
    b.om(3, "¿Qué respuesta expresa desacuerdo respetuoso?", "That's an interesting point, but I see it differently.", ["You're wrong and that's stupid.", "Whatever.", "Nobody cares about your opinion."], "Respetar otras posturas también es parte del objetivo.", "Reconoce la idea del otro y luego discrepa con respeto.")
    b.co(3, "Uniforms are useful ___ they reduce pressure about clothes.", "because", ["although", "unless", "however"], "Justifica la opinión.", "«Because» introduce la razón.")
    b.em(3, "Une cada función con su expresión.", [["Dar una opinión", "I think that…"], ["Agregar un argumento", "Moreover,…"], ["Conceder", "It is true that…, but…"], ["Concluir", "To sum up,…"]],
         "Piensa en la estructura de un texto de opinión.", "Opinar, agregar, conceder y concluir.")
    b.ord(4, "Ordena el párrafo de opinión.", ["In my opinion, schools should start later.", "Firstly, teenagers need more sleep.", "Moreover, students would concentrate better.", "To sum up, a later start would help everyone."], "Opinión, argumentos y conclusión.", "Primero la postura, luego los argumentos y al final la conclusión.")
    b.om(4, "¿Qué oración tiene mejor argumento para «We should reduce plastic»?", "Plastic takes hundreds of years to break down and pollutes the ocean.", ["Plastic is ugly.", "I don't like plastic.", "Everybody says so."], "Un buen argumento entrega una razón o evidencia.", "Da una razón comprobable, no solo un gusto.")
    b.co(4, "___ some people prefer cars, public transport is better for the environment.", "Although", ["Because", "So", "Moreover"], "Concede una idea opuesta.", "«Although» introduce una concesión.")
    b.om(5, "Elige la mejor conclusión para un texto a favor de prohibir celulares en clases.", "To conclude, limiting phones in class can help students focus, while allowing them in emergencies.", ["To conclude, phones are bad and teachers are always right.", "To conclude, I have a new phone.", "To conclude, some students like music."],
         "Una buena conclusión resume la postura y considera matices.", "Resume la postura y considera una excepción razonable.")
    b.om(5, "Escucha la opinión. ¿Qué postura tiene la persona?", "Está a favor de los autos eléctricos, con reparos.", ["Está totalmente en contra.", "No tiene opinión.", "Habla de otro tema."], "Escucha «I support… but…».", "Apoya los autos eléctricos, pero menciona el problema del precio.", audio="I support electric cars, but they are still too expensive for most families.")
    b.cat(5, "¿El conector agrega, contrasta o concluye?", ["Agregar", "Contrastar", "Concluir"], [("Furthermore", 0), ("In addition", 0), ("On the other hand", 1), ("Nevertheless", 1), ("In conclusion", 2), ("All in all", 2)],
          "Piensa en la función de cada conector.", "Furthermore e in addition suman; on the other hand y nevertheless contrastan; in conclusion y all in all cierran.")
    return b.items


def in3m_oa3():
    b = Autor("ing", "3m", 3)
    T1 = "Should video games be considered a sport? Supporters say e-sports require strategy, teamwork and quick reflexes, just like football. Critics argue that sports must involve physical effort. Personally, I think e-sports are a different kind of competition, and they deserve respect, even if they are not 'sports'."
    b.om(1, "What is the topic of the text?", "whether video games are a sport", ["how to play football", "the history of video games", "why reflexes are important"], "Lee la pregunta inicial.", "Discute si los videojuegos son un deporte.", texto=T1)
    b.om(2, "What do critics think?", "Sports must involve physical effort.", ["E-sports need teamwork.", "Video games are better than football.", "Players should get paid more."], "Busca «Critics argue…».", "Los críticos dicen que el deporte requiere esfuerzo físico.", texto=T1)
    b.om(4, "What is the writer's personal position?", "E-sports deserve respect, even if they are not sports.", ["E-sports are exactly like football.", "Video games should be banned.", "The writer has no opinion."], "Busca «Personally, I think…».", "Cree que merecen respeto aunque no sean un deporte.", texto=T1)
    T2 = "Many people share news on social media without checking it. A false story can reach millions of people in hours. Before sharing, ask yourself: Who wrote this? Is there a reliable source? Does the headline sound too shocking to be true?"
    b.om(2, "What is the main advice of the text?", "Check information before sharing it.", ["Never use social media.", "Share news quickly.", "Only read headlines."], "Busca el consejo «Before sharing…».", "Recomienda verificar antes de compartir.", texto=T2)
    b.cat(3, "¿Es una buena pregunta para verificar una noticia?", ["Useful question", "Not useful"], [("Who wrote this?", 0), ("Is there a reliable source?", 0), ("Does it have many likes?", 1), ("Is the picture pretty?", 1)],
          "Piensa en qué ayuda a saber si algo es verdad.", "Autor y fuente ayudan a verificar; los likes y la foto no.", texto=T2)
    b.om(5, "Which sentence best expresses a critical but respectful reply to a friend who shared fake news?", "I think this might not be true; I couldn't find it on any reliable site.", ["You're so stupid for sharing this.", "Thanks, I'll share it too!", "Fake news is always funny."],
         "Crítica con respeto: da una razón y no ofende.", "Duda con un argumento y sin insultar.", texto=T2)
    b.co(1, "A ___ source is one you can trust.", "reliable", ["shocking", "fake", "funny"], "Fuente confiable.", "«Reliable» significa confiable.")
    b.co(3, "The story spread quickly; ___, many people believed it.", "as a result", ["although", "unless", "in contrast"], "Conector de consecuencia.", "«As a result» introduce una consecuencia.")
    b.em(3, "Une cada expresión con su significado.", [["to go viral", "difundirse muy rápido"], ["a headline", "titular"], ["to fact-check", "verificar datos"]], "Vocabulario de medios.", "Viral, titular y verificar datos.")
    b.ord(4, "Ordena la respuesta de opinión.", ["I partly agree with the article.", "It's true that games can be addictive.", "However, they can also teach teamwork.", "So, the key is balance."], "Postura, concesión, contraste y conclusión.", "Primero la postura, luego concede, contrasta y concluye.")
    b.om(4, "¿Qué oración usa correctamente un conector de concesión?", "Even though I enjoy social media, I try to limit my screen time.", ["Even though I enjoy social media, so I use it.", "Even though because I enjoy social media.", "I enjoy even though social media."], "Even though + idea, idea opuesta.", "La primera concede algo y luego presenta lo contrario.")
    b.om(5, "Escucha. ¿Qué opina la persona sobre trabajar desde casa?", "Ve ventajas, pero extraña a sus compañeros.", ["Lo odia completamente.", "Prefiere trabajar de noche.", "No ha trabajado nunca."], "Escucha «but I miss».", "Menciona ventajas, pero extraña a sus compañeros.", audio="Working from home saves me time, but I really miss my colleagues.")
    b.om(5, "¿Qué título resume mejor un texto que compara ventajas y desventajas de la inteligencia artificial en la escuela?", "AI in the Classroom: Helpful Tool or Shortcut?", ["AI Is Always Bad", "My Favourite Teacher", "How to Build a Robot"], "Busca un título que muestre ambas caras.", "La pregunta del título refleja ventajas y desventajas.")
    b.om(1, "Escucha. ¿De qué tema habla?", "del cambio climático", ["de un partido de fútbol", "de una receta", "de un viaje a la playa"], "Escucha «climate change».", "Dice «climate change».", audio="Climate change is the biggest challenge of our generation.")
    b.om(2, "Escucha. ¿Qué propone la persona?", "usar más transporte público", ["comprar más autos", "viajar en avión", "no salir de casa"], "Escucha «public transport».", "Propone usar más transporte público.", audio="I think we should use public transport more often.")
    return b.items


# ---------------- 4° medio ----------------
def in4m_oa1():
    b = Autor("ing", "4m", 1)
    T1 = "JOB OFFER – Junior Graphic Designer. Remote work, 30 hours a week. Requirements: portfolio with at least five projects, intermediate English, knowledge of design software. Applications close on March 15th. Interviews will be online."
    b.om(1, "How many hours a week is the job?", "30", ["15", "40", "5"], "Busca «hours a week».", "«30 hours a week».", texto=T1)
    b.cat(2, "¿Es un requisito del trabajo?", ["Required", "Not mentioned"], [("a portfolio with five projects", 0), ("intermediate English", 0), ("a driving licence", 1), ("a university degree", 1)],
          "Lee la lista de «Requirements».", "Portafolio e inglés intermedio se piden; licencia y título no se mencionan.", texto=T1)
    b.om(3, "You want to apply. What do you need to do first, according to the ad?", "prepare a portfolio with at least five projects", ["travel to the office", "buy design software", "wait until April"], "Piensa en el propósito: postular.", "Necesitas un portafolio antes del 15 de marzo.", texto=T1)
    T2 = "Hostel Patagonia: Breakfast 7–10 a.m. Kitchen open until 10 p.m. Quiet hours from 11 p.m. Lockers available at reception (bring your own padlock). Free bikes for guests; return them before sunset."
    b.om(1, "Until what time can guests use the kitchen?", "10 p.m.", ["11 p.m.", "7 a.m.", "sunset"], "Busca «Kitchen».", "«Kitchen open until 10 p.m.».", texto=T2)
    b.om(3, "You want to keep your passport safe. What should you bring?", "a padlock", ["a bike", "a key card", "breakfast"], "Busca «Lockers».", "Hay casilleros, pero debes traer tu propio candado.", texto=T2)
    b.om(4, "A guest borrows a bike at 6 p.m. in winter. What could be a problem?", "Sunset is early, so there is little time to return it.", ["Bikes are not free.", "Breakfast ends at 10.", "The kitchen is closed."], "Relaciona «before sunset» con el invierno.", "En invierno oscurece temprano y hay que devolverla antes.", texto=T2)
    T3 = "A recent survey of 2,000 Chilean teenagers found that 68% use their phones for more than five hours a day. However, 54% said they would like to spend less time online. Researchers recommend digital breaks and offline hobbies."
    b.nu(2, "What percentage of teenagers would like to spend less time online?", 54, "Busca «would like to spend less».", "«54% said they would like to spend less time online».", unidad="%", texto=T3)
    b.om(4, "Which sentence best summarises the survey?", "Most teens use phones a lot, but many want to use them less.", ["Teens never use their phones.", "Researchers want teens online more.", "Only 54 teens answered."], "Une los dos datos principales.", "Muchos lo usan bastante, pero más de la mitad quiere usarlo menos.", texto=T3)
    b.om(5, "What can we infer from the survey?", "Many teens are aware that they use their phones too much.", ["Teens don't care about screen time.", "Phones are banned in Chile.", "Researchers use phones five hours a day."],
         "Relaciona el 68% con el 54%.", "Más de la mitad quiere usarlo menos: muchos reconocen que lo usan demasiado.", texto=T3)
    b.om(5, "What is the purpose of the last sentence?", "to suggest solutions", ["to give more statistics", "to criticise researchers", "to describe a hobby in detail"], "¿Qué hacen los investigadores?", "Recomiendan pausas digitales: proponen soluciones.", texto=T3)
    b.co(2, "The interviews will be ___, so you don't need to travel.", "online", ["in person", "outdoors", "cancelled"], "Relee el aviso de trabajo.", "«Interviews will be online».", texto=T1)
    b.em(3, "Une cada necesidad con el texto donde buscarías.", [["find a job", "a job offer"], ["book a bed", "a hostel website"], ["learn about teen habits", "a survey report"]], "Piensa en el propósito de cada texto.", "Cada propósito se resuelve con un tipo de texto.")
    b.om(5, "Escucha el mensaje. ¿Qué debe hacer el pasajero?", "ir a la puerta 12 porque cambió", ["esperar en la puerta 4", "salir del aeropuerto", "comprar otro pasaje"], "Escucha «now departing from gate 12».", "El vuelo ahora sale por la puerta 12.", audio="Attention, passengers on flight LA 800 to Lima: your flight is now departing from gate 12.")
    b.om(1, "Escucha. ¿Cuánto cuesta la entrada?", "5 dólares", ["15 dólares", "50 dólares", "es gratis"], "Escucha el precio.", "Dice «five dollars».", audio="Entrance to the museum is five dollars for students.")
    b.om(4, "Escucha el pronóstico. ¿Qué conviene llevar el sábado?", "paraguas", ["traje de baño", "lentes de sol", "nada especial"], "Escucha «heavy rain on Saturday».", "Anuncia lluvia intensa el sábado.", audio="Expect sunny skies on Friday, but heavy rain on Saturday.")
    return b.items


def in4m_oa2():
    b = Autor("ing", "4m", 2)
    b.co(1, "I'm ___ favour of a four-day school week.", "in", ["on", "at", "for"], "Expresión fija: in favour of.", "«In favour of» = a favor de.")
    b.co(1, "I'm against this idea ___ it could increase inequality.", "because", ["although", "unless", "whereas"], "Justifica la postura.", "«Because» introduce la razón.")
    b.om(1, "¿Qué expresión muestra acuerdo total?", "I couldn't agree more.", ["I'm not so sure.", "I totally disagree.", "That's not the point."], "«No podría estar más de acuerdo».", "«I couldn't agree more» expresa acuerdo total.")
    b.cat(2, "¿Acuerdo o desacuerdo?", ["Agree", "Disagree"], [("Absolutely.", 0), ("That's exactly what I think.", 0), ("I'm afraid I don't share that view.", 1), ("I see it quite differently.", 1)],
          "Fíjate en el sentido de cada frase.", "Absolutely y exactly expresan acuerdo; las otras, desacuerdo cortés.")
    b.co(2, "___ is no doubt that recycling helps the environment.", "There", ["It", "This", "They"], "Expresión fija: There is no doubt that…", "«There is no doubt that…».")
    b.ord(2, "Ordena la oración.", ["It", "is", "widely", "believed", "that", "exercise helps."], "Expresión impersonal: It is believed that…", "It is widely believed that exercise helps.")
    b.om(3, "¿Qué oración presenta una postura con matices?", "While tourism brings jobs, it can also damage fragile ecosystems.", ["Tourism is perfect.", "Tourism is the worst thing ever.", "I went on holiday last year."], "Busca la que considera dos lados.", "«While…, it can also…» reconoce ventajas y riesgos.")
    b.co(3, "Some people say the law is unfair. ___, others believe it protects consumers.", "On the other hand", ["As a result", "For example", "Firstly"], "Presenta la otra postura.", "«On the other hand» introduce la postura contraria.")
    b.em(3, "Une cada tipo de argumento con su ejemplo.", [["Dato", "70% of students support the change."], ["Ejemplo", "In Iceland, a similar plan worked."], ["Experiencia", "When I tried it, I slept better."]],
         "Un buen texto usa distintos tipos de evidencia.", "Datos, ejemplos y experiencia personal apoyan una postura.")
    b.ord(4, "Ordena el párrafo argumentativo.", ["Public transport should be free for students.", "This would reduce costs for families.", "It could also reduce traffic and pollution.", "Therefore, the government should fund it."], "Tesis, argumentos y conclusión.", "Postura, dos argumentos y una conclusión con «Therefore».")
    b.om(4, "¿Qué oración contiene una generalización que debilita el argumento?", "All teenagers are addicted to their phones.", ["Many teenagers spend over five hours online.", "A survey shows phone use is increasing.", "Some students use apps to study."], "Busca palabras absolutas como «all».", "«All» exagera: no todos los adolescentes son adictos.")
    b.co(4, "We need stricter rules; ___, accidents will keep happening.", "otherwise", ["moreover", "although", "because"], "«De lo contrario».", "«Otherwise» expresa lo que pasaría si no.")
    b.om(5, "Elige la respuesta más crítica y respetuosa a: «Climate change is not real.»", "I understand doubts exist, but most scientific studies show clear evidence of it.", ["That's ridiculous, you know nothing.", "OK, whatever you say.", "Climate change is boring."], "Debe dar evidencia y no ofender.", "Reconoce la duda y responde con evidencia, sin descalificar.")
    b.om(5, "Escucha. ¿Qué postura defiende la persona?", "A favor de las clases en línea como complemento.", ["Contra toda clase en línea.", "A favor de cerrar los colegios.", "Indiferente."], "Escucha «as a complement».", "Defiende las clases en línea como complemento, no como reemplazo.", audio="Online classes shouldn't replace school, but they work well as a complement.")
    b.cat(5, "¿Es un argumento sólido o una falacia?", ["Argumento sólido", "Falacia"], [("Studies show sleep improves memory.", 0), ("Our city reduced traffic by 20% with bike lanes.", 0), ("He's wrong because he's young.", 1), ("Everyone does it, so it must be right.", 1)],
          "Las falacias atacan a la persona o apelan a «todos lo hacen».", "Los datos son argumentos; atacar a la persona y el «todos lo hacen» son falacias.")
    return b.items


def in4m_oa3():
    b = Autor("ing", "4m", 3)
    T1 = "Fast delivery apps have changed how we shop. You can get food or groceries in minutes. However, many delivery riders work long hours without health insurance. As consumers, we could choose apps that treat workers fairly and tip when possible."
    b.om(1, "What has changed, according to the text?", "how we shop", ["how we cook", "how we travel", "how we study"], "Lee la primera oración.", "«Delivery apps have changed how we shop».", texto=T1)
    b.om(3, "What problem does the writer point out?", "Riders often work long hours without insurance.", ["Food arrives cold.", "Apps are too expensive.", "There are not enough restaurants."], "Busca «However…».", "Muchos repartidores trabajan muchas horas sin seguro de salud.", texto=T1)
    b.om(5, "What kind of action does the writer suggest?", "responsible choices as consumers", ["banning all apps", "never ordering food", "working as a rider"], "Lee la última oración.", "Propone elegir apps justas y dar propina: consumo responsable.", texto=T1)
    T2 = "Some argue that tourists should pay a fee to visit Easter Island (Rapa Nui), because the island's ecosystem and archaeological sites are fragile. Others fear that a high fee would make it a destination only for the rich. A possible compromise is a fee that funds conservation, with discounts for students."
    b.cat(2, "¿Qué postura apoya cada idea?", ["A favor de la tarifa", "En contra de una tarifa alta"], [("protects fragile sites", 0), ("funds conservation", 0), ("only rich people could go", 1), ("excludes students and families", 1)],
          "Separa los argumentos de cada lado.", "Proteger y financiar apoyan la tarifa; excluir a quienes tienen menos dinero va en contra.", texto=T2)
    b.om(4, "What is the «compromise» proposed?", "a fee that funds conservation, with student discounts", ["no fee at all", "closing the island", "a very high fee for everyone"], "Busca «A possible compromise is…».", "Una tarifa para conservar, con descuento para estudiantes.", texto=T2)
    b.co(3, "A «compromise» is a solution where both sides ___ something.", "give up", ["win", "destroy", "ignore"], "Piensa en un acuerdo intermedio.", "En un compromiso ambas partes ceden algo.", texto=T2)
    b.co(1, "Recycling is important. ___, it is not enough to solve pollution.", "However", ["Therefore", "Because", "For instance"], "Contraste entre dos ideas.", "«However» introduce un contraste.")
    b.ord(2, "Ordena la oración.", ["I", "would", "rather", "walk", "than", "drive."], "I would rather + verbo + than + verbo.", "I would rather walk than drive.")
    b.em(2, "Une cada inicio con su final.", [["If more people cycled,", "there would be less traffic."], ["Unless we act now,", "it will be too late."], ["Not only is it cheap,", "but it is also healthy."]], "Revisa la estructura de cada oración.", "Segundo condicional, unless y not only… but also.")
    b.om(3, "¿Qué oración expresa una postura crítica con evidencia?", "Bottled water is unnecessary in Chile's cities, since tap water is safe and much cheaper.", ["Bottled water is nice.", "I like my bottle.", "Water is wet."], "Busca opinión + razón.", "Da una postura y la justifica con evidencia.")
    b.om(4, "Escucha. ¿Qué piensa la persona de la inteligencia artificial?", "Que es útil, pero hay que usarla con responsabilidad.", ["Que es peligrosa y hay que prohibirla.", "Que no sirve para nada.", "Que reemplazará a todos los profesores."], "Escucha «useful» y «responsibly».", "Dice que es útil si se usa con responsabilidad.", audio="Artificial intelligence can be very useful if we use it responsibly.")
    b.om(4, "¿Qué conector usarías para dar un ejemplo?", "For instance,", ["Nevertheless,", "In conclusion,", "Otherwise,"], "«Por ejemplo».", "«For instance» introduce un ejemplo.")
    b.om(5, "Elige el mejor resumen de tu postura sobre el trabajo remoto.", "Remote work offers flexibility, but companies should make sure employees don't feel isolated.", ["Remote work is the best and has no problems.", "I don't know what remote work is.", "Everyone hates remote work."], "Un buen resumen es claro y considera matices.", "Presenta una ventaja y una condición razonable.")
    b.om(5, "Escucha y elige la respuesta más respetuosa.", "I respect your view, although I think there's another side to consider.", ["You're totally wrong.", "Stop talking.", "That's a silly idea."], "Responde a una opinión con la que no estás de acuerdo.", "Respeta la opinión y ofrece otra mirada.", audio="In my opinion, homework should be completely banned.")
    b.om(1, "Escucha. ¿Qué tema se discute?", "si los celulares deberían permitirse en clases", ["el precio de los celulares", "cómo reparar un celular", "la historia del teléfono"], "Escucha «phones in class».", "Pregunta si los celulares deberían permitirse en clases.", audio="Today's debate: should phones be allowed in class?")
    return b.items


GENERADORES = {
    "1_medio.ingles.OA9": in1m_oa9, "1_medio.ingles.OA10": in1m_oa10, "1_medio.ingles.OA16": in1m_oa16,
    "2_medio.ingles.OA10": in2m_oa10, "2_medio.ingles.OA11": in2m_oa11, "2_medio.ingles.OA16": in2m_oa16,
    "3_medio.ingles.OA1": in3m_oa1, "3_medio.ingles.OA2": in3m_oa2, "3_medio.ingles.OA3": in3m_oa3,
    "4_medio.ingles.OA1": in4m_oa1, "4_medio.ingles.OA2": in4m_oa2, "4_medio.ingles.OA3": in4m_oa3,
}
