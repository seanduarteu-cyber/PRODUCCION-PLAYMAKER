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


# ---------------------------------------------------------------- 7° básico
def in07_oa9():
    b = Autor("ing", 7, 9)
    aviso = ("NOTICE: Clean-up Day at Playa Grande! Join us this Saturday at 10 a.m. Bring gloves, a hat and "
             "a water bottle. We will give bags to all volunteers. Let's keep our beach clean!")
    chat = ("Diego: Can you send me the science homework? Sofía: Sure! I'm sending you a photo now. "
            "Diego: Thanks! My laptop isn't working, so I'm using my mom's phone.")
    sueno = ("Sleep is very important for teenagers. Experts say that young people need eight to ten hours of sleep "
             "every night. Without enough sleep, it is difficult to concentrate at school. "
             "Try to turn off your phone one hour before bed.")
    correo = ("Hi Amanda, Greetings from San Pedro de Atacama! The desert is amazing. Yesterday we visited the "
              "Valle de la Luna and watched the sunset. Tonight we're going to look at the stars because the sky "
              "is very clear here. Love, Martina")
    reglas = ("COMPUTER LAB RULES: Do not eat or drink near the computers. Ask the teacher before you print. "
              "Save your work on your USB drive. Turn off the computer when you finish.")
    reciclaje = ("Every year, Chile produces a lot of plastic waste. Many Chilean cities have recycling points in "
                 "parks and supermarkets. People can take bottles, cans and paper there. Recycling helps to reduce "
                 "pollution and protect animals in the ocean.")
    # Nivel 1: información explícita y muy visible
    b.om(1, "When is the Clean-up Day?", "on Saturday at 10 a.m.",
         ["on Sunday at 10 a.m.", "on Saturday at 10 p.m.", "on Friday at 2 p.m."],
         "Busca el día y la hora en la segunda oración.",
         "El aviso dice «this Saturday at 10 a.m.»: el sábado a las 10 de la mañana.", texto=aviso)
    b.nu(1, "What is the minimum number of hours of sleep teenagers need?", 8,
         "Busca «eight to ten hours».",
         "Los expertos dicen que necesitan de ocho a diez horas (eight to ten): como mínimo, 8 horas.",
         unidad="horas", texto=sueno)
    b.om(1, "Where is Martina?", "in San Pedro de Atacama", ["in Chiloé", "in Valparaíso", "in Punta Arenas"],
         "Lee el saludo: «Greetings from…».",
         "Martina escribe «Greetings from San Pedro de Atacama!»: está en San Pedro de Atacama.", texto=correo)
    # Nivel 2: información explícita
    b.om(2, "What does Diego need?", "the science homework",
         ["a new laptop", "his mom's phone", "a photo of Sofía"],
         "Lee el primer mensaje de Diego.",
         "Diego pregunta «Can you send me the science homework?»: necesita la tarea de ciencias.", texto=chat)
    b.ord(2, "Put Martina's activities in order.",
          ["She visited the Valle de la Luna.", "She watched the sunset.", "She is going to look at the stars."],
          "Fíjate en «yesterday» (ayer) y en «tonight» (esta noche).",
          "Ayer visitó el Valle de la Luna y vio la puesta de sol; esta noche va a mirar las estrellas.", texto=correo)
    b.cat(2, "Is it allowed in the computer lab?", ["Allowed", "Not allowed"],
          [("eat a sandwich near the computers", 1), ("drink juice near the computers", 1),
           ("save your work on a USB drive", 0), ("print after asking the teacher", 0)],
          "«Do not» indica una prohibición.",
          "No se puede comer ni beber cerca de los computadores; sí se puede guardar el trabajo en un pendrive e imprimir después de preguntarle al profesor.",
          texto=reglas)
    # Nivel 3: vocabulario en contexto y relaciones
    b.cat(3, "Según el aviso, ¿quién aporta cada cosa?", ["Los voluntarios", "Los organizadores"],
          [("gloves", 0), ("a hat", 0), ("a water bottle", 0), ("bags", 1)],
          "«Bring» significa traer; «we will give» significa nosotros entregaremos.",
          "Los voluntarios traen guantes, gorro y botella de agua; los organizadores entregan las bolsas (we will give bags).",
          texto=aviso)
    b.om(3, "In the chat, «Sure!» means…", "¡Claro!", ["¡Para nada!", "¡Lo siento!", "¡Chao!"],
         "Fíjate en lo que hace Sofía después: envía una foto.",
         "«Sure!» significa ¡claro!: Sofía acepta y envía una foto de la tarea.", texto=chat)
    b.em(3, "Match the words from the text with their meaning.",
         [["waste", "basura, desechos"], ["cans", "latas"], ["reduce", "reducir"], ["pollution", "contaminación"]],
         "Algunas se parecen al español; para las otras, usa el contexto.",
         "waste = basura o desechos, cans = latas, reduce = reducir y pollution = contaminación.", texto=reciclaje)
    # Nivel 4: relaciones entre ideas y vocabulario en contexto
    b.om(4, "Why is Diego using his mom's phone?", "because his laptop isn't working",
         ["because he lost his phone", "because Sofía asked him to", "because his mom is sending the homework"],
         "Busca la palabra «so»: lo que va antes es la causa.",
         "«My laptop isn't working, so I'm using my mom's phone»: usa el celular de su mamá porque su notebook no funciona.",
         texto=chat)
    b.om(4, "In the text, «turn off» means…", "apagar", ["encender", "cargar", "revisar"],
         "Piensa en qué conviene hacer con el celular antes de dormir.",
         "«Turn off» significa apagar: el texto aconseja apagar el celular una hora antes de dormir.", texto=sueno)
    b.om(4, "In the text, «there» refers to…", "the recycling points", ["the ocean", "the animals", "people's houses"],
         "Busca en la oración anterior a qué lugar se refiere.",
         "«People can take bottles, cans and paper there»: «there» (allí) se refiere a los puntos de reciclaje (recycling points).",
         texto=reciclaje)
    # Nivel 5: idea principal, propósito e inferencia
    b.om(5, "What is the purpose of this notice?", "to invite people to clean the beach",
         ["to sell gloves and hats", "to describe a beautiful beach", "to tell people not to go to the beach"],
         "Fíjate en «Join us» y en la última oración.",
         "«Join us» (únete) y «Let's keep our beach clean» muestran que el aviso invita a limpiar la playa.", texto=aviso)
    b.om(5, "What is the main idea of the text?", "Sleeping well is important for teenagers.",
         ["Phones are bad for school.", "Teenagers sleep too much.", "Experts need more sleep."],
         "Lee la primera oración y piensa de qué hablan todas las demás.",
         "Todo el texto explica por qué dormir bien es importante para los adolescentes; lo del celular es solo un consejo.",
         texto=sueno)
    b.om(5, "How does Martina feel about her trip?", "She is enjoying it.",
         ["She is bored.", "She is scared.", "She wants to go home."],
         "Busca palabras que muestren su opinión, como «amazing».",
         "Martina dice que el desierto es «amazing» (increíble) y cuenta sus actividades con entusiasmo: lo está pasando bien.",
         texto=correo)
    b.om(5, "Who is this text for?", "students who use the computer lab",
         ["people who sell computers", "parents at home", "technicians who fix printers"],
         "Piensa quién usa la sala y le pide permiso al profesor.",
         "Las reglas hablan de «ask the teacher» y de guardar «your work»: son para los estudiantes que usan la sala de computación.",
         texto=reglas)
    b.om(5, "Which is the best title for the text?", "Recycling in Chile",
         ["How to Make Plastic", "Animals in the Ocean", "The Best Supermarkets"],
         "El mejor título resume todo el texto, no solo un detalle.",
         "Todo el texto trata sobre reciclar en Chile; los otros títulos hablan de un detalle o de temas que no están.",
         texto=reciclaje)
    return b.items


def in07_oa16():
    b = Autor("ing", 7, 16)
    # Nivel 1: reconocer obligación, prohibición y razones
    b.em(1, "Une cada señal con su regla.",
         [["📵", "You mustn't use your phone."], ["🤫", "You must be quiet."], ["🚭", "You mustn't smoke."],
          ["🚳", "You mustn't ride a bike here."], ["⛑️", "You must wear a helmet."]],
         "«Must» indica obligación y «mustn't», prohibición.",
         "📵 no usar el celular, 🤫 guardar silencio, 🚭 no fumar, 🚳 no andar en bicicleta y ⛑️ usar casco.")
    b.co(1, "Completa la regla: «You ___ run in the hallway.» 🏃❌", "mustn't", ["must", "can", "has to"],
         "La ❌ indica que está prohibido.",
         "Para prohibir se usa «mustn't»: «You mustn't run in the hallway» significa no debes correr en el pasillo.")
    b.co(1, "Escucha el modelo y completa: «I'm happy ___ it's my birthday.»", "because", ["so", "but", "if"],
         "La segunda parte explica la razón.",
         "«Because» (porque) introduce la razón: estoy feliz porque es mi cumpleaños.",
         audio="I'm happy because it's my birthday.")
    # Nivel 2: completar y ordenar reglas simples
    b.cat(2, "¿Obligación o prohibición?", ["Obligación", "Prohibición"],
          [("You must wear a uniform.", 0), ("We have to be on time.", 0), ("Students must bring their books.", 0),
           ("You mustn't shout.", 1), ("You mustn't eat in class.", 1), ("You mustn't litter.", 1)],
          "«Must» y «have to» obligan; «mustn't» prohíbe.",
          "Must y have to expresan obligación (uniforme, puntualidad, libros); mustn't expresa prohibición (gritar, comer en clase, botar basura).")
    b.co(2, "Completa: «My sister ___ to wake up at 6 a.m. every day.»", "has", ["have", "must", "is"],
         "Con «my sister» (she) se usa la forma con -s.",
         "Con she se usa «has to»: «My sister has to wake up at 6 a.m.» significa mi hermana tiene que despertarse a las 6. «Must» no lleva «to».")
    b.ord(2, "Escucha el modelo y ordena la regla: «Debes apagar tu celular.»",
          ["You", "must", "turn off", "your phone."],
          "Después de «must» va el verbo sin «to».",
          "«You must turn off your phone.» expresa una obligación: debes apagar tu celular.",
          audio="You must turn off your phone.")
    # Nivel 3: aplicar must, because, so e if
    b.co(3, "Completa: «It's raining, ___ I'm taking an umbrella.»", "so", ["because", "but", "if"],
         "La segunda parte es la consecuencia de la primera.",
         "«So» (así que) introduce la consecuencia: está lloviendo, así que llevo paraguas.")
    b.em(3, "Une cada causa con su efecto.",
         [["If you heat ice,", "it melts."], ["If it rains,", "the streets get wet."],
          ["If you don't water plants,", "they die."], ["If you exercise,", "you get stronger."]],
         "Piensa en lo que siempre ocurre en cada caso.",
         "Si calientas hielo, se derrite; si llueve, las calles se mojan; si no riegas las plantas, se mueren; si haces ejercicio, te pones más fuerte.")
    b.om(3, "¿Qué oración está bien escrita?", "You mustn't feed the animals.",
         ["You mustn't to feed the animals.", "You don't must feed the animals.", "You mustn't feeding the animals."],
         "Después de «mustn't» va el verbo en su forma base, sin «to».",
         "Lo correcto es «You mustn't feed the animals»: mustn't + verbo sin «to» y sin -ing.")
    b.ord(3, "Escribe en inglés: «Me quedé en casa porque estaba enfermo.»",
          ["I stayed", "at home", "because", "I was sick."],
          "«Because» va antes de la razón.",
          "«I stayed at home because I was sick.» usa «because» para justificar.")
    # Nivel 4: elegir la función correcta
    b.co(4, "Completa: «If you mix blue and yellow, you ___ green.»", "get", ["gets", "got", "getting"],
         "Con «if» + presente, la otra parte también va en presente.",
         "Para hechos que siempre ocurren se usa if + presente: «If you mix blue and yellow, you get green».")
    b.cat(4, "¿Se completa con «because» o con «so»?", ["because", "so"],
          [("I ate a sandwich ___ I was hungry.", 0), ("We can't play outside ___ it's raining.", 0),
           ("She's tired ___ she ran ten kilometers.", 0), ("I was hungry, ___ I ate a sandwich.", 1),
           ("It's cold, ___ I'm wearing a jacket.", 1), ("The bus was late, ___ I missed the class.", 1)],
          "«Because» va antes de la causa; «so», antes de la consecuencia.",
          "Después de «because» viene la razón (I was hungry, it's raining, she ran); después de «so» viene el resultado (I ate, I'm wearing a jacket, I missed the class).")
    b.ord(4, "Escribe en inglés: «Si llueve, los niños juegan adentro.»",
          ["If it rains,", "the children", "play", "inside."],
          "Empieza con la condición (if).",
          "«If it rains, the children play inside.»: la condición va con «if» y en presente.")
    b.co(4, "Lee el letrero del museo: 📸🚫. Completa: «Visitors ___ take photos in the museum.»", "mustn't",
         ["must", "don't have to", "has to"],
         "El letrero prohíbe algo.",
         "📸🚫 es una prohibición: «Visitors mustn't take photos». «Don't have to» significa que no es necesario, no que esté prohibido.")
    # Nivel 5: distinguir matices y justificar
    b.om(5, "¿Qué oración significa «No es necesario que traigas comida»?", "You don't have to bring food.",
         ["You mustn't bring food.", "You must bring food.", "You have to bring food."],
         "Ojo: «mustn't» prohíbe, pero «don't have to» dice que algo no es necesario.",
         "«You don't have to bring food» significa no es necesario que traigas comida; «You mustn't bring food» significa está prohibido traer comida.")
    b.om(5, "{personaje} escribe una regla para la sala con su razón. ¿Cuál está bien escrita y tiene sentido?",
         "We must recycle paper because it helps the environment.",
         ["We mustn't recycle paper because it helps the environment.",
          "We must to recycle paper because it helps the environment.",
          "We must recycle paper because it hurts the environment."],
         "Revisa la gramática de «must» y que la razón tenga sentido.",
         "«We must recycle paper because it helps the environment» está bien: must + verbo sin «to», y la razón justifica la regla.")
    b.em(5, "Une cada regla con su justificación.",
         [["You must wear a helmet", "because it protects your head."],
          ["You mustn't swim here", "because the sea is dangerous."],
          ["You have to wear sunscreen", "because the sun is very strong."],
          ["You mustn't feed the animals", "because human food can make them sick."]],
         "Busca la razón lógica de cada regla.",
         "El casco protege la cabeza; no se nada si el mar es peligroso; el bloqueador protege del sol fuerte; la comida humana enferma a los animales.")
    return b.items


# ---------------------------------------------------------------- 8° básico
def in08_oa9():
    b = Autor("ing", 8, 9)
    mistral = ("Gabriela Mistral was born in Vicuña, Chile, in 1889. She worked as a teacher for many years and "
               "wrote beautiful poems for children. In 1945, she won the Nobel Prize in Literature. She was the first "
               "Latin American writer to receive this prize.")
    pebre = ("PEBRE (for 4 people). Ingredients: 3 tomatoes, 1 onion, some cilantro, oil and salt. First, chop the "
             "tomatoes, the onion and the cilantro. Then, put everything in a bowl. Finally, add oil and salt, "
             "mix well and serve with bread.")
    tormenta = ("A strong storm hit the south of Chile yesterday. In Puerto Montt, heavy rain and wind closed some "
                "schools and roads. Nobody was hurt, but many houses lost electricity for several hours. "
                "Experts say the weather will improve on Friday.")
    chiloe = ("Visit Chiloé! Discover its colorful wooden churches and its palafitos, traditional houses on stilts "
              "over the water. Try curanto, a delicious dish cooked in a hole in the ground. You can get there by "
              "ferry from Pargua. Come and enjoy the magic of the island!")
    violeta = ("Violeta Parra was a Chilean singer, songwriter and artist. She was born in 1917. She traveled around "
               "the Chilean countryside and collected traditional songs. She also made arpilleras, colorful pictures "
               "sewn on cloth. Today, her song “Gracias a la vida” is famous all over the world.")
    robotica = ("Last week, students from a school in Rancagua won a national robotics competition. Their robot can "
                "separate plastic, glass and paper for recycling. The team worked on the project for six months. "
                "In December, they will travel to Brazil to compete with teams from other countries.")
    # Nivel 1: información explícita y muy visible
    b.nu(1, "In what year did Gabriela Mistral win the Nobel Prize?", 1945,
         "Busca el año que aparece junto a «Nobel Prize».",
         "El texto dice «In 1945, she won the Nobel Prize in Literature»: lo ganó en 1945.", texto=mistral)
    b.nu(1, "How many tomatoes do you need?", 3,
         "Revisa la lista de ingredientes.",
         "Los ingredientes dicen «3 tomatoes»: necesitas 3 tomates. El 4 es el número de personas.",
         unidad="tomates", texto=pebre)
    b.om(1, "Which part of Chile did the storm hit?", "the south", ["the north", "the center", "Easter Island"],
         "Lee la primera oración.",
         "La noticia dice «hit the south of Chile»: la tormenta afectó al sur de Chile.", texto=tormenta)
    b.co(1, "Complete: «The robot separates plastic, glass and ___.»", "paper", ["metal", "food", "cans"],
         "Busca la oración que habla del robot.",
         "El texto dice «separate plastic, glass and paper»: el robot separa plástico, vidrio y papel.", texto=robotica)
    # Nivel 2: información explícita
    b.ord(2, "Put the steps in order.",
          ["Chop the vegetables.", "Put everything in a bowl.", "Add oil and salt and mix.", "Serve with bread."],
          "Fíjate en «first», «then» y «finally», y en el orden dentro de cada oración.",
          "Primero se pican las verduras, luego se pone todo en un bol, después se agrega aceite y sal y se mezcla, y al final se sirve con pan.",
          texto=pebre)
    b.om(2, "How can you get to Chiloé?", "by ferry from Pargua",
         ["by train from Pargua", "by ferry from Valparaíso", "by plane from Pargua"],
         "Busca la palabra «ferry».",
         "El folleto dice «by ferry from Pargua»: se llega en transbordador desde Pargua.", texto=chiloe)
    b.om(2, "What did Violeta Parra collect?", "traditional songs",
         ["colorful stones", "old paintings", "famous books"],
         "Busca el verbo «collected».",
         "El texto dice «collected traditional songs»: recopiló canciones tradicionales.", texto=violeta)
    # Nivel 3: vocabulario en contexto
    b.om(3, "In the text, «won» is the past form of…", "win", ["want", "wonder", "one"],
         "Piensa en qué se hace con un premio.",
         "«Won» es el pasado irregular de «win» (ganar): ella ganó el Premio Nobel.", texto=mistral)
    b.om(3, "According to the brochure, palafitos are…", "traditional houses on stilts",
         ["colorful wooden churches", "a typical dish", "small boats"],
         "La explicación aparece justo después de la palabra «palafitos».",
         "El folleto explica que los palafitos son «traditional houses on stilts over the water»: casas tradicionales sobre pilotes.",
         texto=chiloe)
    b.em(3, "Match the words with their meaning.",
         [["songwriter", "compositora"], ["countryside", "el campo"], ["sewn", "cosido"], ["famous", "famosa"]],
         "Piensa en el contexto: canciones, lugares, telas y fama.",
         "songwriter = compositora, countryside = el campo, sewn = cosido y famous = famosa.", texto=violeta)
    # Nivel 4: vocabulario y relaciones entre ideas
    b.om(4, "In the recipe, «chop» means…", "picar", ["lavar", "hervir", "mezclar"],
         "Piensa qué se hace con el tomate y la cebolla antes de ponerlos en el bol.",
         "«Chop» significa picar, cortar en trozos pequeños: así se preparan el tomate, la cebolla y el cilantro.",
         texto=pebre)
    b.om(4, "In the text, «Nobody was hurt» means…", "Nadie resultó herido.",
         ["Nadie ayudó.", "Todos se enfermaron.", "Nadie tenía luz."],
         "«Nobody» significa nadie; «hurt» tiene que ver con lesiones.",
         "«Nobody was hurt» significa nadie resultó herido; lo que perdieron muchas casas fue la electricidad.",
         texto=tormenta)
    b.cat(4, "True or false?", ["True", "False"],
          [("She was Chilean.", 0), ("She collected songs from the countryside.", 0),
           ("She only sang; she didn't make art.", 1), ("Her song is famous only in Chile.", 1)],
          "Fíjate en las palabras «also» y «all over the world».",
          "Era chilena y recopiló canciones del campo; también hizo arpilleras (also made) y su canción es famosa en todo el mundo (all over the world).",
          texto=violeta)
    # Nivel 5: idea principal y propósito
    b.om(5, "What is the main purpose of the text?", "to give information about Gabriela Mistral's life",
         ["to teach how to write poems", "to invite tourists to Vicuña", "to sell a book of poems"],
         "Piensa en qué tipo de texto es: cuenta datos de la vida de una persona.",
         "Es una biografía breve: informa sobre la vida de Gabriela Mistral (dónde nació, en qué trabajó y qué premio ganó).",
         texto=mistral)
    b.om(5, "What is the main idea of the news?", "A storm caused problems in the south of Chile.",
         ["Puerto Montt has new schools.", "The weather is always bad in the south.", "Many people were hurt in a storm."],
         "La idea principal resume toda la noticia; descarta lo que el texto no dice.",
         "La noticia cuenta que una tormenta causó problemas en el sur (colegios, caminos y luz); además dice que nadie resultó herido.",
         texto=tormenta)
    b.om(5, "What is the purpose of the brochure?", "to persuade tourists to visit Chiloé",
         ["to explain how to build churches", "to give a recipe for curanto", "to report news about Chiloé"],
         "Fíjate en «Visit», «Discover» y «Try»: son invitaciones.",
         "Los folletos turísticos buscan convencer: «Visit», «Discover» y «Try» invitan a los turistas a ir a Chiloé.",
         texto=chiloe)
    b.om(5, "Which is the best headline for this news?", "Chilean Students Win Robotics Competition",
         ["Rancagua Builds a New School", "Robots Are Dangerous for Students", "Brazil Wins Recycling Prize"],
         "El titular debe resumir lo más importante de la noticia.",
         "Lo principal es que estudiantes de Rancagua ganaron un concurso nacional de robótica; los otros titulares no dicen eso.",
         texto=robotica)
    return b.items


def in08_oa16():
    b = Autor("ing", 8, 16)
    # Nivel 1: reconocer cantidades, gustos y el tiempo
    b.cat(1, "¿Contable o incontable?", ["Countable", "Uncountable"],
          [("apple", 0), ("egg", 0), ("tomato", 0), ("milk", 1), ("rice", 1), ("water", 1)],
          "¿Puedes contarlo de uno en uno (one, two, three)?",
          "Apple, egg y tomato se cuentan (two apples); milk, rice y water no se cuentan de uno en uno: son incontables.")
    b.em(1, "Une cada símbolo con el tiempo que indica.",
         [["☀️", "It's sunny."], ["🌧️", "It's raining."], ["❄️", "It's snowing."], ["💨", "It's windy."],
          ["☁️", "It's cloudy."]],
         "Piensa en «sun», «rain», «snow», «wind» y «cloud».",
         "☀️ sunny (soleado), 🌧️ raining (lloviendo), ❄️ snowing (nevando), 💨 windy (con viento) y ☁️ cloudy (nublado).")
    b.co(1, "Escucha el modelo y completa: «I love ___ in the sea.»", "swimming", ["swim", "swims", "swam"],
         "Después de «love» el verbo termina en -ing.",
         "Después de love, like o hate se usa el verbo con -ing: «I love swimming in the sea».",
         audio="I love swimming in the sea.")
    # Nivel 2: completar y ordenar oraciones simples
    b.co(2, "Completa: «How ___ water do you drink every day?»", "much", ["many", "some", "any"],
         "«Water» no se cuenta de uno en uno.",
         "Con sustantivos incontables, como water, se pregunta «How much…?».")
    b.co(2, "Completa: «Santiago is ___ than Valparaíso.» (más grande)", "bigger", ["biger", "more big", "biggest"],
         "Adjetivo corto + -er; ojo con la consonante final.",
         "«Big» dobla la g: bigger. «Santiago is bigger than Valparaíso» significa Santiago es más grande que Valparaíso.")
    b.ord(2, "Escucha el modelo y ordena la pregunta: «¿Cómo está el tiempo hoy?»",
          ["What's", "the weather", "like", "today?"],
          "En esta pregunta, «like» significa cómo es y va después de «the weather».",
          "«What's the weather like today?» significa ¿cómo está el tiempo hoy?",
          audio="What's the weather like today?")
    # Nivel 3: aplicar las estructuras
    b.co(3, "Completa: «There aren't ___ eggs in the fridge.»", "any", ["some", "much", "a"],
         "En oraciones negativas se usa una palabra especial.",
         "En oraciones negativas y en preguntas se usa «any»: «There aren't any eggs in the fridge».")
    b.om(3, "¿Qué oración está bien escrita?", "I prefer reading to watching TV.",
         ["I prefer read to watching TV.", "I prefer reading than watching TV.", "I prefers reading to watching TV."],
         "Después de «prefer» va un verbo con -ing, y se compara con «to».",
         "Se dice prefer + verbo con -ing + to + verbo con -ing: «I prefer reading to watching TV».")
    b.em(3, "Une cada adjetivo con su comparativo.",
         [["good", "better"], ["bad", "worse"], ["big", "bigger"], ["happy", "happier"],
          ["expensive", "more expensive"]],
         "Ojo: good y bad son irregulares.",
         "good → better, bad → worse, big → bigger, happy → happier y expensive → more expensive.")
    b.co(3, "Completa: «Look at those dark clouds! It's going ___ rain.»", "to", ["for", "at", "will"],
         "Para predecir algo que ves venir se usa «be going» + una palabra corta + el verbo.",
         "«It's going to rain» significa va a llover: going to sirve para predicciones con evidencia, como las nubes negras.")
    # Nivel 4: elegir la estructura correcta
    b.co(4, "Completa: «Ojos del Salado is the ___ volcano in the world.»", "highest",
         ["higher", "most high", "more high"],
         "Comparas con todos los volcanes del mundo: necesitas el superlativo.",
         "Con «the … in the world» se usa el superlativo: high → the highest. El Ojos del Salado es el volcán más alto del mundo.")
    b.cat(4, "¿Se completa con «much» o con «many»?", ["much", "many"],
          [("How ___ money do you have?", 0), ("There isn't ___ time.", 0), ("How ___ sugar do you want?", 0),
           ("How ___ students are there?", 1), ("I don't have ___ friends in this city.", 1),
           ("Are there ___ tourists in Pucón?", 1)],
          "«Much» va con lo que no se cuenta; «many», con lo que se cuenta.",
          "Money, time y sugar son incontables: much. Students, friends y tourists son contables: many.")
    b.ord(4, "Escribe en inglés: «Preferiría quedarme en casa que salir.»",
          ["I'd rather", "stay", "at home", "than", "go out."],
          "Después de «I'd rather» va el verbo sin «to».",
          "«I'd rather stay at home than go out.» significa preferiría quedarme en casa que salir.")
    b.om(4, "{personaje} pregunta: «What's the weather like in Punta Arenas tomorrow?» El pronóstico dice ❄️. ¿Qué respuesta está bien escrita?",
         "It's going to snow.", ["It's going to snowing.", "It going to snow.", "It's go to snow."],
         "Revisa que esté «is», que diga «going to» y que el verbo vaya sin -ing.",
         "Para predecir el tiempo se usa It's going to + verbo: «It's going to snow» significa va a nevar.")
    # Nivel 5: escribir en una situación nueva
    b.co(5, "Temperaturas: Arica 25 °C, Santiago 18 °C, Punta Arenas 8 °C. Completa: «Punta Arenas is the ___ city of the three.»",
         "coldest", ["colder", "most cold", "hottest"],
         "Comparas tres ciudades: busca la más fría y usa el superlativo.",
         "Punta Arenas tiene la temperatura más baja: es «the coldest» (la más fría). Con tres o más se usa el superlativo.")
    b.om(5, "Martina odia levantarse temprano, pero le encanta dormir hasta tarde. ¿Qué oración la describe?",
         "She hates getting up early, but she loves sleeping late.",
         ["She hates get up early, but she loves sleeping late.",
          "She loves getting up early, but she hates sleeping late.",
          "She hates getting up early, but she love sleeping late."],
         "Revisa el significado, el -ing después de love y hate, y la -s con she.",
         "«She hates getting up early, but she loves sleeping late»: hate y love + verbo con -ing, y con she el verbo lleva -s.")
    b.cat(5, "¿La oración está bien escrita o tiene un error?", ["Bien escrita", "Tiene un error"],
          [("There isn't much milk.", 0), ("This is the most interesting book in the library.", 0),
           ("We have a lot of homework.", 0), ("I'd rather to walk.", 1), ("My brother is more tall than me.", 1),
           ("How many bread do you want?", 1)],
          "Revisa would rather, los comparativos y si el sustantivo se cuenta o no.",
          "Lo correcto es «I'd rather walk», «taller than me» y «How much bread…?»; las otras tres están bien escritas.")
    return b.items


GENERADORES = {
    "5_basico.ingles.OA5": in05_oa5,
    "5_basico.ingles.OA14": in05_oa14,
    "6_basico.ingles.OA5": in06_oa5,
    "6_basico.ingles.OA15": in06_oa15,
    "7_basico.ingles.OA9": in07_oa9,
    "7_basico.ingles.OA16": in07_oa16,
    "8_basico.ingles.OA9": in08_oa9,
    "8_basico.ingles.OA16": in08_oa16,
}
