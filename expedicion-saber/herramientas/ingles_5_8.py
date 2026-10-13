"""Inglés 5° a 8° básico: 15 a 17 desafíos por OA (3 o 4 por nivel de dificultad, 1 a 5).

OA de comprensión de lectura (5° y 6° OA5, 7° y 8° OA9): cada desafío lleva "texto", una lectura breve
en inglés que se muestra arriba; cada texto se usa en 2 o 3 preguntas. Niveles 1–2: información explícita;
3–4: vocabulario en contexto y relaciones; 5: idea principal, propósito o inferencia simple.
OA de expresión escrita (5° OA14, 6° OA15, 7° y 8° OA16): completar, ordenar palabras, emparejar,
clasificar y elegir la oración bien escrita; algunos llevan audio como modelo.
En 5° y 6° los enunciados van en español; en 7° y 8° algunas preguntas van en inglés simple.
La pista y la explicación siempre van en español."""
from autor import Autor


# ---------------------------------------------------------------- 5° básico
def in05_oa5():
    b = Autor("ing", 5, 5)
    sofia = ("Hi! My name is Sofía and I'm ten years old. I live in La Serena with my mom, my dad and "
             "my little brother, Tomás. I have long black hair and brown eyes. I like music, but I don't like soccer.")
    clase = ("Good morning, class! Please open your books to page 12. Read the text and answer the questions. "
             "Use your pencil, not your pen. Work in pairs, please.")
    casa = ("This is my house. It has two bedrooms, a kitchen, a living room and a small garden. "
            "My favorite room is the kitchen because my grandma cooks there. My dog sleeps in the garden.")
    diego = ("Diego lives in Valparaíso. Near his house there is a park, a supermarket and a big school. "
             "There isn't a hospital or a bank in his street. On Saturdays, Diego goes to the park with his cousins.")
    martina = ("Martina loves fruit. She likes apples, bananas and grapes. She doesn't like fish, but her brother "
               "Vicente loves it. On Sundays, they eat empanadas with their grandparents.")
    familia = ("My family is big. My grandpa is old and tall, and he has white hair. My aunt Josefa is short "
               "and she has curly red hair. My cousins are twins: they are eight years old.")
    # Nivel 1: información explícita y muy visible
    b.nu(1, "Lee el texto. ¿Cuántos años tiene Sofía?", 10,
         "Busca la palabra «years».",
         "Sofía dice «I'm ten years old»: tiene 10 años (ten = diez).", unidad="años", texto=sofia)
    b.nu(1, "¿En qué página deben abrir el libro?", 12,
         "Busca la palabra «page».",
         "La profesora dice «open your books to page 12»: deben abrirlo en la página 12.", texto=clase)
    b.om(1, "¿En qué ciudad vive Diego?", "Valparaíso", ["Santiago", "Temuco", "Arica"],
         "Lee la primera oración.",
         "El texto dice «Diego lives in Valparaíso»: Diego vive en Valparaíso.", texto=diego)
    # Nivel 2: información explícita
    b.ord(2, "Ordena las instrucciones en el orden en que las da la profesora.",
          ["open your books", "read the text", "answer the questions", "use your pencil", "work in pairs"],
          "Vuelve a leer el texto de principio a fin.",
          "El orden es: open your books, read the text, answer the questions, use your pencil y work in pairs.",
          texto=clase)
    b.nu(2, "¿Cuántos dormitorios tiene la casa?", 2,
         "Busca la palabra «bedrooms».",
         "El texto dice «two bedrooms»: la casa tiene 2 dormitorios.", unidad="dormitorios", texto=casa)
    b.cat(2, "¿A Martina le gusta o no le gusta?", ["Le gusta", "No le gusta"],
          [("apples", 0), ("bananas", 0), ("grapes", 0), ("fish", 1)],
          "«She likes» significa le gusta; «she doesn't like», no le gusta.",
          "A Martina le gustan las manzanas, los plátanos y las uvas; no le gusta el pescado (fish).", texto=martina)
    b.co(2, "Completa según el texto: «Aunt Josefa has curly ___ hair.»", "red", ["white", "black", "brown"],
         "Busca la oración que habla de la tía Josefa.",
         "El texto dice «she has curly red hair»: la tía Josefa tiene el pelo crespo y colorín (rojo).", texto=familia)
    # Nivel 3: vocabulario en contexto y relaciones
    b.em(3, "Une cada palabra del texto con su significado.",
         [["long", "largo"], ["black", "negro"], ["brown", "café"], ["little brother", "hermano menor"]],
         "Piensa en cómo describe Sofía su pelo, sus ojos y a Tomás.",
         "long = largo, black = negro, brown = café y little brother = hermano menor (Tomás).", texto=sofia)
    b.cat(3, "Según el texto, ¿qué hay y qué no hay cerca de la casa de Diego?", ["Hay", "No hay"],
          [("park", 0), ("supermarket", 0), ("school", 0), ("hospital", 1), ("bank", 1)],
          "«There is» significa hay; «there isn't» significa no hay.",
          "Hay un parque, un supermercado y una escuela (there is); no hay hospital ni banco (there isn't).", texto=diego)
    b.em(3, "Une cada persona con su descripción.",
         [["grandpa", "old and tall"], ["aunt Josefa", "short"], ["cousins", "eight years old"]],
         "Busca a cada persona en el texto.",
         "El abuelo es old and tall (viejo y alto), la tía Josefa es short (baja) y los primos tienen ocho años (eight years old).",
         texto=familia)
    # Nivel 4: vocabulario en contexto y relaciones entre ideas
    b.om(4, "En el texto, «work in pairs» significa…", "trabajar en parejas",
         ["trabajar solo", "trabajar en casa", "trabajar en silencio"],
         "«Pair» se usa para cosas que vienen de a dos, como «a pair of shoes».",
         "«Work in pairs» significa trabajar en parejas, es decir, de a dos.", texto=clase)
    b.om(4, "¿Por qué la cocina es el lugar favorito de la casa?", "porque ahí cocina su abuela",
         ["porque es muy grande", "porque ahí duerme su perro", "porque está al lado del jardín"],
         "Busca la palabra «because», que significa porque.",
         "El texto dice «because my grandma cooks there»: porque ahí cocina su abuela.", texto=casa)
    b.om(4, "¿Qué muestra la palabra «but» en el texto?", "que a Vicente le gusta algo que a Martina no",
         ["que a los dos les gusta el pescado", "que Martina come pescado los domingos",
          "que a Martina le encanta el pescado"],
         "«But» significa pero: une dos ideas diferentes.",
         "«But» (pero) muestra un contraste: a Martina no le gusta el pescado, pero a Vicente le encanta.", texto=martina)
    b.om(4, "En el texto, «twins» significa…", "gemelos o mellizos",
         ["primos lejanos", "hermanos mayores", "bebés recién nacidos"],
         "Fíjate: los dos primos tienen la misma edad.",
         "«Twins» son gemelos o mellizos: hermanos que nacieron el mismo día; por eso tienen la misma edad.",
         texto=familia)
    # Nivel 5: propósito, idea principal e inferencia simple
    b.om(5, "¿Para qué escribió Sofía este texto?", "para presentarse",
         ["para invitar a una fiesta", "para dar instrucciones", "para describir su ciudad"],
         "Fíjate en cómo empieza: «Hi! My name is…».",
         "Sofía cuenta su nombre, su edad, su familia y sus gustos: escribió el texto para presentarse.", texto=sofia)
    b.om(5, "¿Cuál es la idea principal del texto?", "Describe el barrio donde vive Diego.",
         ["Cuenta un viaje de Diego a la playa.", "Explica cómo llegar al hospital.", "Describe a los primos de Diego."],
         "Piensa de qué habla casi todo el texto.",
         "Casi todo el texto cuenta qué hay y qué no hay cerca de la casa de Diego: describe su barrio.", texto=diego)
    b.om(5, "¿Qué colación le gustaría más a Martina?", "una ensalada de frutas",
         ["un sándwich de atún", "pescado frito", "una sopa de pescado"],
         "Revisa qué le encanta y qué no le gusta a Martina.",
         "A Martina le encanta la fruta (loves fruit) y no le gusta el pescado; el atún también es pescado.",
         texto=martina)
    return b.items


def in05_oa14():
    b = Autor("ing", 5, 14)
    # Nivel 1: copiar y completar con modelo
    b.co(1, "Escucha el modelo y completa: «I ___ ten years old.»", "am", ["is", "are", "be"],
         "Con «I» se usa una forma especial del verbo to be.",
         "Con «I» se usa «am»: «I am ten years old» significa tengo diez años.", audio="I am ten years old.")
    b.em(1, "Une cada pronombre con su adjetivo posesivo.",
         [["I", "my"], ["you", "your"], ["he", "his"], ["she", "her"], ["we", "our"]],
         "«My» significa mi; piensa en los demás.",
         "I → my (mi), you → your (tu), he → his (su, de él), she → her (su, de ella) y we → our (nuestro).")
    b.co(1, "Escucha el modelo y completa la invitación: «Come to my birthday ___!» 🎂", "party",
         ["part", "partie", "play"],
         "Es la palabra «fiesta». Revisa bien sus letras.",
         "Fiesta se escribe «party»: «Come to my birthday party!» significa ¡ven a mi fiesta de cumpleaños!",
         audio="Come to my birthday party!")
    # Nivel 2: completar y ordenar oraciones simples
    b.co(2, "Completa: «She ___ got a cat.» 🐱", "has", ["have", "is", "haves"],
         "Con he, she o it se usa la forma que termina en -s.",
         "Con «she» se usa «has got»: «She has got a cat» significa ella tiene un gato.")
    b.cat(2, "Ayuda a {personaje} a describir su pieza. ¿Va con «There is» o con «There are»?",
          ["There is", "There are"],
          [("a bed", 0), ("a lamp", 0), ("an old sofa", 0), ("two chairs", 1), ("three windows", 1), ("some books", 1)],
          "«There is» va con una sola cosa; «there are», con varias.",
          "There is a bed, a lamp y an old sofa (una cosa); there are two chairs, three windows y some books (varias).")
    b.ord(2, "Escucha el modelo y ordena: «Mi hermano tiene el pelo corto.»",
          ["My brother", "has got", "short", "hair."],
          "En inglés, el adjetivo (short) va antes de la palabra hair.",
          "«My brother has got short hair.» significa mi hermano tiene el pelo corto.",
          audio="My brother has got short hair.")
    b.co(2, "Completa la descripción: «This is my sister. ___ name is Amanda.»", "Her", ["His", "She", "Your"],
         "Hablas de una niña: ¿cómo se dice «su nombre» (de ella)?",
         "Para una mujer se usa «her»: «Her name is Amanda» significa su nombre es Amanda.")
    # Nivel 3: aplicar la gramática del año
    b.co(3, "Completa: «We have got a dog. ___ dog is very friendly.»", "Our", ["We", "Us", "Their"],
         "Busca el posesivo de «we» (nosotros).",
         "El posesivo de «we» es «our»: «Our dog is very friendly» significa nuestro perro es muy amistoso.")
    b.ord(3, "Ordena la pregunta: «¿Hay un baño en tu casa?»", ["Is there", "a bathroom", "in", "your house?"],
          "En las preguntas, «is» va antes de «there».",
          "«Is there a bathroom in your house?» significa ¿hay un baño en tu casa?")
    b.om(3, "¿Qué oración está bien escrita?", "There are two bedrooms in my house.",
         ["There is two bedrooms in my house.", "There are two bedroom in my house.",
          "There two bedrooms are in my house."],
         "Son dos dormitorios: revisa el verbo y el plural.",
         "Con dos o más cosas se usa «there are» y el sustantivo en plural: «There are two bedrooms in my house.»")
    b.em(3, "Une cada parte de la postal con su función.",
         [["Dear Grandma,", "saludo"], ["I'm in Arica with my family.", "dónde estás"],
          ["It's hot and sunny here.", "cómo está el tiempo"], ["Love, Josefa", "despedida y firma"]],
         "Una postal empieza con un saludo y termina con una despedida y tu nombre.",
         "«Dear Grandma,» es el saludo; «I'm in Arica…» dice dónde estás; «It's hot and sunny» cuenta el tiempo y «Love, Josefa» es la despedida y firma.")
    # Nivel 4: textos breves con modelo
    b.co(4, "Completa la postal: «Dear Vicente, I'm in Torres del Paine. There ___ a lot of mountains here!»", "are",
         ["is", "has", "have"],
         "«A lot of mountains» son muchas montañas.",
         "Con varias cosas se usa «there are»: «There are a lot of mountains here!» significa ¡aquí hay muchas montañas!")
    b.cat(4, "¿La oración está bien escrita o tiene un error?", ["Bien escrita", "Tiene un error"],
          [("She has got blue eyes.", 0), ("My cat is black.", 0), ("Our school is near the park.", 0),
           ("They has got a big house.", 1), ("He have got two sisters.", 1), ("There is three bananas.", 1)],
          "Revisa si el verbo concuerda con quién es y con cuántas cosas hay.",
          "Lo correcto es «They have got», «He has got» y «There are three bananas»; las otras tres están bien escritas.")
    b.ord(4, "Ordena la invitación de Amanda.",
          ["Hi, Diego!", "Come to my party.", "It's on Saturday at 4 o'clock.", "See you there! Amanda"],
          "Una invitación empieza con un saludo y termina con una despedida.",
          "Primero el saludo, luego la invitación, después el día y la hora, y al final la despedida con la firma.")
    # Nivel 5: escribir en una situación nueva
    b.om(5, "Mira la pieza: 🛏️🛏️ 🪑 📚📚📚. ¿Qué descripción está bien escrita?",
         "There are two beds, a chair and three books.",
         ["There is two beds, a chair and three books.", "There are two beds, a chair and three book.",
          "There are two bed, a chairs and three books."],
         "Cuenta las cosas y revisa el verbo y los plurales.",
         "Hay dos camas, una silla y tres libros: «There are two beds, a chair and three books», con «are» y los plurales correctos.")
    b.co(5, "Amanda escribe sobre sus abuelos: «My grandparents live in Chillán. ___ house has got a big garden.»",
         "Their", ["There", "They're", "His"],
         "Necesitas el posesivo de «they» (ellos). Ojo: hay palabras que suenan igual.",
         "El posesivo de «they» es «their»: «Their house has got a big garden». «There» (allí) y «they're» (ellos son) suenan igual, pero significan otra cosa.")
    b.em(5, "Une cada inicio con su final para escribir la postal de {personaje}.",
         [["Hello from", "Valdivia!"], ["The river", "is very big."], ["My parents", "are very happy."],
          ["There are", "a lot of boats."]],
         "Revisa que cada oración tenga sentido y que el verbo concuerde con quién es.",
         "La postal dice: «Hello from Valdivia! The river is very big. My parents are very happy. There are a lot of boats.»")
    return b.items


# ---------------------------------------------------------------- 6° básico
def in06_oa5():
    b = Autor("ing", 6, 5)
    habilidades = ("My name is Benjamín. I can swim very well and I can ride a bike, but I can't skate. "
                   "My sister Amanda can play the guitar. She can't swim, so she takes lessons on Saturdays.")
    direcciones = ("Excuse me, where is the library? Go straight on Prat Street and turn left at the bank. "
                   "The library is between the post office and the supermarket. You can't miss it!")
    rutina = ("Vicente gets up at seven o'clock. He has breakfast at half past seven and goes to school by bus. "
              "School starts at a quarter past eight. In the afternoon, he plays soccer with his friends.")
    parque = ("It's Saturday afternoon in the park. Grandpa is reading the newspaper on a bench. Josefa and Diego "
              "are flying a kite, and the dog is running after a ball. Mom is taking photos.")
    verano = ("Last summer, Martina was in Pichilemu with her family. The beach was beautiful, but the water was "
              "very cold. She walked on the beach every day and watched the surfers. Her parents were very happy.")
    lluvia = ("Yesterday Tomás stayed at home because it was raining. In the morning, he cleaned his bedroom. "
              "After lunch, he played board games with his cousin. Then they cooked sopaipillas. "
              "At night, they watched a movie.")
    # Nivel 1: información explícita y muy visible
    b.om(1, "¿Qué NO puede hacer Benjamín?", "patinar", ["nadar", "andar en bicicleta", "tocar guitarra"],
         "Busca «can't», que significa no puede.",
         "Benjamín dice «I can't skate»: no puede patinar.", texto=habilidades)
    b.om(1, "¿Qué lugar busca la persona?", "la biblioteca", ["el banco", "el correo", "el supermercado"],
         "Lee la pregunta del comienzo.",
         "La persona pregunta «where is the library?»: busca la biblioteca.", texto=direcciones)
    b.co(1, "Completa según el texto: «Vicente goes to school by ___.»", "bus", ["car", "bike", "train"],
         "Busca la palabra «school» en el texto.",
         "El texto dice «goes to school by bus»: Vicente va al colegio en bus.", texto=rutina)
    # Nivel 2: información explícita
    b.om(2, "¿Dónde hay que doblar a la izquierda?", "en el banco",
         ["en el correo", "en el supermercado", "en la biblioteca"],
         "Busca «turn left», que significa dobla a la izquierda.",
         "El texto dice «turn left at the bank»: hay que doblar a la izquierda en el banco.", texto=direcciones)
    b.em(2, "Une cada persona con lo que está haciendo.",
         [["Grandpa", "lee el diario"], ["Josefa and Diego", "elevan un volantín"],
          ["the dog", "corre tras una pelota"], ["Mom", "saca fotos"]],
         "Busca el verbo terminado en -ing después de cada persona.",
         "Grandpa is reading (lee el diario), Josefa and Diego are flying a kite (elevan un volantín), the dog is running (corre tras una pelota) y Mom is taking photos (saca fotos).",
         texto=parque)
    b.cat(2, "¿Verdadero o falso según el texto?", ["Verdadero", "Falso"],
          [("El agua estaba muy fría.", 0), ("Martina caminaba por la playa.", 0),
           ("La playa era fea.", 1), ("Sus padres estaban tristes.", 1)],
          "Busca cada idea en el texto: «was» y «were» cuentan cómo era o estaba algo.",
          "El agua estaba fría y Martina caminaba por la playa; la playa era linda (beautiful) y sus padres estaban felices (happy).",
          texto=verano)
    # Nivel 3: vocabulario en contexto y relaciones
    b.cat(3, "Según el texto, ¿puede o no puede?", ["Puede (can)", "No puede (can't)"],
          [("Benjamín: swim", 0), ("Benjamín: ride a bike", 0), ("Benjamín: skate", 1),
           ("Amanda: play the guitar", 0), ("Amanda: swim", 1)],
          "Fíjate bien en quién hace cada cosa: Benjamín y Amanda no saben hacer lo mismo.",
          "Benjamín puede nadar y andar en bicicleta, pero no patinar; Amanda puede tocar guitarra, pero no nadar.",
          texto=habilidades)
    b.om(3, "¿A qué hora toma desayuno Vicente?", "7:30", ["7:00", "8:15", "7:15"],
         "«Half past» significa y media.",
         "«At half past seven» significa a las siete y media: 7:30.", texto=rutina)
    b.ord(3, "Ordena lo que hizo Tomás ayer.",
          ["cleaned his bedroom", "played board games", "cooked sopaipillas", "watched a movie"],
          "Fíjate en «in the morning», «after lunch», «then» y «at night».",
          "En la mañana ordenó su pieza, después de almuerzo jugó juegos de mesa, luego cocinaron sopaipillas y en la noche vieron una película.",
          texto=lluvia)
    # Nivel 4: relaciones entre ideas y vocabulario en contexto
    b.om(4, "¿Qué clases toma probablemente Amanda los sábados?", "clases de natación",
         ["clases de guitarra", "clases de patinaje", "clases de ciclismo"],
         "Lee la última oración: «so» (por eso) une una causa con su consecuencia.",
         "Amanda no sabe nadar (can't swim), por eso (so) toma clases los sábados: son clases de natación.",
         texto=habilidades)
    b.om(4, "¿Qué plano muestra dónde está la biblioteca? (🏤 correo, 📚 biblioteca, 🛒 supermercado)",
         "🏤 📚 🛒", ["📚 🏤 🛒", "🏤 🛒 📚", "🛒 🏤 📚"],
         "«Between» significa entre: la biblioteca queda en medio de dos lugares.",
         "«The library is between the post office and the supermarket»: la biblioteca está entre el correo y el supermercado.",
         texto=direcciones)
    b.om(4, "En el texto, «watched» significa…", "miró, observó", ["mira", "va a mirar", "lavó"],
         "La terminación -ed indica que la acción ya pasó.",
         "«Watched» es el pasado de «watch» (mirar): significa miró u observó.", texto=verano)
    b.om(4, "¿Por qué Tomás se quedó en casa?", "porque estaba lloviendo",
         ["porque estaba enfermo", "porque su primo lo visitó", "porque quería cocinar"],
         "Busca la palabra «because».",
         "El texto dice «because it was raining»: se quedó en casa porque estaba lloviendo.", texto=lluvia)
    # Nivel 5: inferencia simple e idea global
    b.nu(5, "¿Cuántos minutos pasan desde el desayuno hasta que empiezan las clases?", 45,
         "Primero averigua las dos horas: «half past seven» y «a quarter past eight».",
         "El desayuno es a las 7:30 y las clases empiezan a las 8:15: pasan 45 minutos.", unidad="minutos",
         texto=rutina)
    b.om(5, "¿Cómo está probablemente el tiempo en el parque?", "Hay viento.",
         ["Está lloviendo fuerte.", "Está nevando.", "Es de noche."],
         "¿Qué se necesita para elevar un volantín?",
         "Para elevar un volantín (fly a kite) se necesita viento; además es de tarde y todos están al aire libre.",
         texto=parque)
    b.om(5, "¿Cómo sabes que el texto habla del pasado?", "por «last summer», «was/were» y los verbos con -ed",
         ["por los nombres de las personas", "porque habla de una playa", "por los verbos terminados en -ing"],
         "Busca palabras que indiquen tiempo y fíjate en la forma de los verbos.",
         "«Last summer» (el verano pasado), «was/were» y los verbos con -ed (walked, watched) muestran que todo ya pasó.",
         texto=verano)
    return b.items


def in06_oa15():
    b = Autor("ing", 6, 15)
    # Nivel 1: reconocer posiciones y expresiones
    b.co(1, "Mira: la pelota ⚽ está debajo de la silla 🪑. Completa: «The ball is ___ the chair.»", "under",
         ["on", "in", "between"],
         "«Debajo de» se dice con una palabra que empieza con u.",
         "«Under» significa debajo de: «The ball is under the chair».")
    b.em(1, "Une cada palabra con su significado.",
         [["in", "dentro de"], ["on", "sobre"], ["under", "debajo de"], ["next to", "al lado de"], ["between", "entre"]],
         "Piensa en ejemplos: «in the box», «on the table».",
         "in = dentro de, on = sobre, under = debajo de, next to = al lado de y between = entre.")
    b.co(1, "Escucha el modelo y completa: «I ___ to study for the test.»", "need", ["needs", "can", "am"],
         "Con «I» el verbo no lleva -s.",
         "«I need to study for the test» significa necesito estudiar para la prueba.",
         audio="I need to study for the test.")
    # Nivel 2: completar y ordenar oraciones simples
    b.co(2, "Mira: 🏦 🏫 🏥. Completa: «The school is ___ the bank and the hospital.»", "between",
         ["next", "under", "on"],
         "La escuela está en medio de los otros dos lugares.",
         "«Between» significa entre: la escuela está entre el banco y el hospital.")
    b.cat(2, "¿Se completa con «has to» o con «have to»?", ["has to", "have to"],
          [("She ___ clean her room.", 0), ("My dad ___ work today.", 0), ("Tomás ___ feed the cat.", 0),
           ("I ___ do my homework.", 1), ("We ___ wear a uniform.", 1), ("They ___ walk the dog.", 1)],
          "Con he, she o una sola persona se usa la forma con -s.",
          "She, my dad y Tomás llevan «has to»; I, we y they llevan «have to».")
    b.ord(2, "Escucha el modelo y ordena: «Mi mochila está debajo de la cama.»",
          ["My backpack", "is", "under", "the bed."],
          "Primero qué cosa, luego «is» y después dónde está.",
          "«My backpack is under the bed.» significa mi mochila está debajo de la cama.",
          audio="My backpack is under the bed.")
    # Nivel 3: aplicar las expresiones de la unidad
    b.co(3, "Completa con la palabra que muestra un contraste: «I can swim, ___ I can't dive.»", "but",
         ["and", "because", "or"],
         "Las dos ideas se oponen: puede hacer una cosa y no la otra.",
         "«But» (pero) une ideas que contrastan: «I can swim, but I can't dive» significa sé nadar, pero no sé tirarme piqueros.")
    b.ord(3, "Escribe en inglés: «Ella está usando lentes y una chaqueta roja.»",
          ["She", "is wearing", "glasses", "and", "a red jacket."],
          "«Está usando» se dice «is wearing»; el color va antes de la prenda.",
          "«She is wearing glasses and a red jacket.» describe lo que ella lleva puesto.")
    b.om(3, "¿Qué oración está bien escrita?", "He has to get up early.",
         ["He have to get up early.", "He has to gets up early.", "He has get up early."],
         "Con «he» se usa «has to» y después el verbo sin cambios.",
         "Lo correcto es «He has to get up early»: «has to» + el verbo en su forma base (get).")
    b.em(3, "Une cada pregunta con su respuesta.",
         [["Where is the remote control?", "It's under the sofa."],
          ["What is your brother doing?", "He's washing the dishes."],
          ["What does your mom look like?", "She's tall with short hair."],
          ["What do you need to do today?", "I need to finish my project."]],
         "«Where» pregunta por un lugar; «doing», por una acción; «look like», por el aspecto.",
         "Where → under the sofa (lugar); doing → washing the dishes (acción); look like → tall with short hair (aspecto); need → I need to finish my project.")
    # Nivel 4: escribir oraciones completas
    b.co(4, "Completa la descripción: «Look! Grandma ___ a cake right now.»", "is making",
         ["makes", "making", "is make"],
         "«Right now» indica que la acción está pasando en este momento.",
         "Para acciones que ocurren ahora se usa is + verbo con -ing: «Grandma is making a cake right now».")
    b.cat(4, "¿La oración está bien escrita o tiene un error?", ["Bien escrita", "Tiene un error"],
          [("My sister is tall, but my brother is short.", 0), ("The lamp is on the table.", 0),
           ("They are playing soccer now.", 0), ("He need to buy bread.", 1),
           ("The cat is between the sofa.", 1), ("She have to go to the dentist.", 1)],
          "Revisa los verbos con he y she, y recuerda que «between» necesita dos cosas.",
          "Lo correcto es «He needs to buy bread», «She has to go to the dentist» y «between the sofa and the chair» (entre dos cosas); las demás están bien.")
    b.ord(4, "Escribe en inglés: «Me gusta el invierno, pero no me gusta la lluvia.»",
          ["I like", "winter,", "but", "I don't like", "rain."],
          "«But» va entre las dos ideas que se oponen.",
          "«I like winter, but I don't like rain.» usa «but» para contrastar lo que te gusta y lo que no.")
    b.om(4, "Diego: alto ✅, usa lentes ❌. ¿Qué oración lo describe bien?",
         "Diego is tall, but he doesn't wear glasses.",
         ["Diego is short, but he doesn't wear glasses.", "Diego is tall, but he wears glasses.",
          "Diego is tall, but he don't wear glasses."],
         "Revisa los datos y fíjate en el verbo que va con «he».",
         "Diego es alto y no usa lentes: «Diego is tall, but he doesn't wear glasses». Con «he» se usa «doesn't».")
    # Nivel 5: escribir en una situación nueva
    b.om(5, "{personaje} quiere escribir que su gato duerme sobre la cama, al lado de la ventana. ¿Qué oración es correcta?",
         "My cat is sleeping on the bed, next to the window.",
         ["My cat is sleeping under the bed, next to the window.", "My cat is sleeping on the bed, next the window.",
          "My cat is sleep on the bed, next to the window."],
         "Revisa la acción (-ing) y cada palabra de posición: sobre, al lado de.",
         "«Is sleeping» es la acción, «on» es sobre y «next to» es al lado de; «next» sin «to» queda incompleto.")
    b.em(5, "Une cada situación con lo que hay que hacer.",
         [["Sofía's bike is broken.", "She needs to fix it."], ["Tomás is very tired.", "He needs to sleep."],
          ["The plants are dry.", "We need to water them."], ["It's raining.", "You need to take an umbrella."]],
         "Piensa en la solución lógica y fíjate en she, he y them.",
         "Bicicleta rota → arreglarla; muy cansado → dormir; plantas secas → regarlas; lluvia → llevar paraguas.")
    b.cat(5, "¿«But» está bien usado o no tiene sentido?", ["Bien usado", "No tiene sentido"],
          [("It's sunny, but it's cold.", 0), ("I like pizza, but I don't like pasta.", 0),
           ("Diego is tall, but his sister is short.", 0), ("It's hot, but it's summer.", 1),
           ("He's hungry, but he wants to eat.", 1), ("I'm tired, but I want to sleep.", 1)],
          "«But» une dos ideas que se oponen o que sorprenden.",
          "«But» funciona cuando hay contraste (soleado, pero frío). Que haga calor en verano o que quieras dormir si estás cansado no se oponen.")
    return b.items


GENERADORES = {
    "5_basico.ingles.OA5": in05_oa5,
    "5_basico.ingles.OA14": in05_oa14,
    "6_basico.ingles.OA5": in06_oa5,
    "6_basico.ingles.OA15": in06_oa15,
}
