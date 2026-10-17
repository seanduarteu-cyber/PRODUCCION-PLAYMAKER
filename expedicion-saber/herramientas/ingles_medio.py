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


GENERADORES = {
    "1_medio.ingles.OA9": in1m_oa9, "1_medio.ingles.OA10": in1m_oa10, "1_medio.ingles.OA16": in1m_oa16,
    "2_medio.ingles.OA10": in2m_oa10, "2_medio.ingles.OA11": in2m_oa11, "2_medio.ingles.OA16": in2m_oa16,
}
