"""Inglés 1° a 4° básico: 18 o 19 desafíos por OA (3 o 4 por nivel de dificultad, 1 a 5).

OA1 (comprensión oral): casi todos los desafíos llevan "audio", un texto en inglés que el juego lee
en voz alta (en-US) y que no se muestra en pantalla; el enunciado se entiende sin él.
OA13 (expresión escrita): completar, ordenar palabras, emparejar y clasificar; algunos llevan
audio como modelo de pronunciación de la palabra que se copia o completa."""
from autor import Autor


# ---------------------------------------------------------------- 1° básico
def en01_oa1():
    b = Autor("ing", 1, 1)
    # Nivel 1: reconocer una palabra suelta
    b.om(1, "Escucha y elige el animal.", "🐱", ["🐶", "🐦", "🐟"],
         "Escucha bien: la palabra empieza con el sonido /k/.",
         "Escuchaste «cat», que significa gato 🐱.", audio="cat")
    b.om(1, "Escucha y elige el color.", "❤️", ["💙", "💚", "💛"],
         "Escucha bien: es una palabra muy cortita.",
         "Escuchaste «red», que significa rojo ❤️.", audio="red")
    b.nu(1, "Escucha el número y escríbelo.", 3,
         "Cuenta en inglés con tus dedos: one, two…",
         "Escuchaste «three», que significa tres: 3.", audio="three")
    b.om(1, "{personaje} te saluda. Escucha: ¿qué te dijo?", "¡Hola!", ["¡Chao!", "¡Gracias!", "¡Buenas noches!"],
         "Escucha bien: ¿suena a llegada o a despedida?",
         "Escuchaste «Hello!», que significa ¡hola!", audio="Hello!")
    # Nivel 2
    b.om(2, "Escucha y elige la parte de la cara.", "👃", ["👁️", "👂", "👄"],
         "Fíjate en el primer sonido: /n/.",
         "Escuchaste «nose», que significa nariz 👃.", audio="nose")
    b.om(2, "Escucha y elige el útil escolar.", "✏️", ["📏", "📕", "✂️"],
         "Fíjate en el primer sonido: /p/.",
         "Escuchaste «pencil», que significa lápiz ✏️.", audio="pencil")
    b.om(2, "Escucha. ¿Quién es?", "la mamá", ["el papá", "la hermana", "el abuelo"],
         "Recuerda: «father» es papá y «sister» es hermana.",
         "Escuchaste «mother», que significa mamá.", audio="mother")
    b.co(2, "Escucha la canción y completa: «One, two, three, ___!»", "four", ["five", "two", "ten"],
         "Escucha con atención el final de la canción.",
         "La canción dice «One, two, three, four!»: después de three (3) viene four (4).",
         audio="One, two, three, four!")
    # Nivel 3: frases cortas
    b.om(3, "Escucha y elige.", "pájaro azul", ["pájaro rojo", "pez azul", "gato azul"],
         "Vas a escuchar dos palabras: un color y un animal.",
         "Escuchaste «a blue bird»: «blue» es azul y «bird» es pájaro.", audio="a blue bird")
    b.nu(3, "Escucha a Martina. ¿Cuántos lápices tiene?", 6,
         "Escucha el número que dice antes de «pencils».",
         "Martina dice «I have six pencils»: «six» es seis.", audio="I have six pencils.")
    b.ord(3, "Escucha la canción de los colores y ordénalos como suenan.", ["❤️", "💛", "💙", "💚"],
          "Escucha un color a la vez y ve poniéndolos en orden.",
          "La canción dice red ❤️ (rojo), yellow 💛 (amarillo), blue 💙 (azul) y green 💚 (verde).",
          audio="Red, yellow, blue, green.")
    b.em(3, "Escucha y une cada palabra con su dibujo.", [["eye", "👁️"], ["ear", "👂"], ["mouth", "👄"], ["nose", "👃"]],
         "Todas son partes de la cara.",
         "eye es ojo 👁️, ear es oreja 👂, mouth es boca 👄 y nose es nariz 👃.",
         audio="eye, ear, mouth, nose")
    # Nivel 4: oraciones y varios datos
    b.om(4, "Escucha a Sofía. ¿Qué le dice a su profesora?", "¡Buenos días, profesora!",
         ["¡Buenas noches, profesora!", "¡Chao, profesora!", "¡Gracias, profesora!"],
         "Fíjate en la palabra del medio: ¿habla de la mañana, de la noche o se despide?",
         "Sofía dice «Good morning, teacher!», que significa ¡buenos días, profesora!",
         audio="Good morning, teacher!")
    b.cat(4, "Escucha a Diego. ¿Qué tiene en su mochila?", ["Sí tiene", "No tiene"],
          [("libro 📕", 0), ("lápiz ✏️", 0), ("goma", 0), ("regla 📏", 1), ("tijeras ✂️", 1)],
          "Diego nombra tres cosas.",
          "Diego dice «a book, a pencil and an eraser»: libro, lápiz y goma. No nombra la regla (ruler) ni las tijeras (scissors).",
          audio="In my bag, I have a book, a pencil and an eraser.")
    b.em(4, "Escucha y une a cada niño con su mascota.", [["Diego", "🐶"], ["Sofía", "🐱"], ["Amanda", "🐟"]],
         "Escucha primero el nombre y después el animal.",
         "Diego has a dog 🐶 (perro), Sofia has a cat 🐱 (gato) y Amanda has a fish 🐟 (pez).",
         audio="Diego has a dog. Sofia has a cat. Amanda has a fish.")
    # Nivel 5: diálogo, adivinanza, dos datos
    b.om(5, "Escucha a Martina. ¿Qué te pregunta?", "¿Cómo te llamas?",
         ["¿Cuántos años tienes?", "¿Cómo estás?", "¿Dónde vives?"],
         "Fíjate en la última palabra que dice.",
         "Martina pregunta «What's your name?», que significa ¿cómo te llamas?",
         audio="Hi! I'm Martina. What's your name?")
    b.om(5, "Escucha la adivinanza y elige el animal.", "🐄", ["🐼", "🐑", "🐷"],
         "Escucha los colores y el sonido que hace.",
         "Es «black and white» (blanco y negro) y dice «moo»: es la vaca 🐄.",
         audio="I am an animal. I am black and white. I say moo.")
    b.nu(5, "Escucha. ¿Cuántos animales hay en total?", 5,
         "Escucha cuántos gatos y cuántos perros hay, y súmalos.",
         "«Two cats and three dogs»: 2 gatos + 3 perros = 5 animales.",
         audio="I see two cats and three dogs.")
    return b.items


def en01_oa13():
    b = Autor("ing", 1, 13)
    # Nivel 1: copiar letras y palabras
    b.co(1, "Escucha el modelo y completa la palabra: c___t 🐱", "a", ["o", "e", "u"],
         "Escucha el sonido del medio de la palabra.",
         "Gato se escribe «cat»: c-a-t.", audio="cat")
    b.em(1, "Une cada palabra con su dibujo.", [["dog", "🐶"], ["cat", "🐱"], ["fish", "🐟"]],
         "Fíjate en la primera letra de cada palabra.",
         "dog es perro 🐶, cat es gato 🐱 y fish es pez 🐟.")
    b.om(1, "{personaje} escribió el modelo «blue» 💙. ¿Qué palabra es igual?", "blue", ["bleu", "blu", "bule"],
         "Compara letra por letra con el modelo.",
         "Azul se escribe «blue»: b-l-u-e.")
    b.co(1, "Escucha el modelo y completa la palabra: r___d ❤️", "e", ["a", "i", "o"],
         "Escucha el sonido del medio de la palabra.",
         "Rojo se escribe «red»: r-e-d.", audio="red")
    # Nivel 2
    b.co(2, "Completa la cuenta: «one, two, ___» 1️⃣ 2️⃣ 3️⃣", "three", ["four", "tree", "ten"],
         "Busca cómo se escribe el número 3 en inglés.",
         "3 en inglés es «three». Ojo: «tree» significa árbol.")
    b.co(2, "Escucha el modelo y completa la palabra: p___ncil ✏️", "e", ["a", "i", "o"],
         "Escucha con atención la primera parte de la palabra.",
         "Lápiz se escribe «pencil»: p-e-n-c-i-l.", audio="pencil")
    b.em(2, "Une cada palabra en inglés con su significado.",
         [["mother", "mamá"], ["father", "papá"], ["sister", "hermana"], ["brother", "hermano"]],
         "«Mother» y «father» se parecen: fíjate en cómo empiezan.",
         "mother es mamá, father es papá, sister es hermana y brother es hermano.")
    b.cat(2, "¿Es un color o un animal?", ["Color 🎨", "Animal 🐾"],
          [("red", 0), ("blue", 0), ("green", 0), ("dog", 1), ("bird", 1), ("cat", 1)],
          "Piensa qué significa cada palabra.",
          "red, blue y green son colores (rojo, azul, verde); dog, bird y cat son animales (perro, pájaro, gato).")
    # Nivel 3: palabras completas y oraciones simples
    b.ord(3, "Ordena las letras para escribir «dog» 🐶.", ["d", "o", "g"],
          "Empieza con la letra d.",
          "Perro se escribe «dog»: d-o-g.")
    b.co(3, "Ayuda a {personaje} a completar: «I have a ___.» 🐶", "dog", ["cat", "dig", "bird"],
         "Mira el dibujo: ¿qué animal es?",
         "🐶 es «dog» (perro): «I have a dog» significa tengo un perro.")
    b.ord(3, "Ordena las palabras para escribir «Este es mi papá».", ["This", "is", "my", "father."],
          "La oración empieza con mayúscula y termina con punto.",
          "«This is my father.» significa este es mi papá.")
    b.co(3, "Completa: «It is ___.» 💛", "yellow", ["yelow", "red", "green"],
         "Mira el color del corazón y revisa bien cada letra.",
         "💛 es «yellow» (amarillo), que se escribe con doble l.")
    # Nivel 4
    b.co(4, "Completa: «I have two ___.» 👀", "eyes", ["eye", "ears", "nose"],
         "Mira el dibujo. Como son dos, la palabra termina en -s.",
         "👀 son «eyes» (ojos); como son dos, lleva -s al final.")
    b.om(4, "¿Qué palabra está bien escrita? 📕", "book", ["bok", "boock", "buk"],
         "Recuerda cómo se ve la palabra «libro» en inglés: es cortita.",
         "Libro se escribe «book»: b-o-o-k.")
    b.ord(4, "Ordena las palabras para escribir «Mi gato es negro».", ["My", "cat", "is", "black."],
          "Primero «My cat» (mi gato).",
          "«My cat is black.» significa mi gato es negro.")
    b.cat(4, "¿Es un útil escolar o una parte de la cara?", ["Útil escolar", "Parte de la cara"],
          [("pencil", 0), ("book", 0), ("eraser", 0), ("eye", 1), ("mouth", 1), ("ear", 1)],
          "Piensa qué significa cada palabra.",
          "pencil (lápiz), book (libro) y eraser (goma) son útiles; eye (ojo), mouth (boca) y ear (oreja) son partes de la cara.")
    # Nivel 5: usar el modelo en una oración nueva
    b.co(5, "Sigue el modelo. «I am six.» 6️⃣ → «I am ___.» 7️⃣", "seven", ["six", "eight", "sevn"],
         "Busca el número 7 y revisa bien sus letras.",
         "7 en inglés es «seven»: «I am seven» significa tengo siete años.")
    b.ord(5, "Mira el modelo «This is my sister.» y escribe «Este es mi hermano».", ["This", "is", "my", "brother."],
          "Usa el modelo y cambia solo la última palabra.",
          "«This is my brother.»: «brother» significa hermano.")
    b.co(5, "Modelo: «a red apple» 🍎. Completa: «a ___ frog» 🐸", "green", ["red", "grean", "blue"],
         "¿De qué color es la rana? Revisa bien las letras.",
         "La rana es verde: «a green frog». Verde se escribe «green», con doble e.")
    return b.items


# ---------------------------------------------------------------- 2° básico
def en02_oa1():
    b = Autor("ing", 2, 1)
    # Nivel 1
    b.om(1, "Escucha y elige el juguete.", "⚽", ["🧸", "🚗", "🎈"],
         "Escucha bien: es una palabra muy cortita.",
         "Escuchaste «ball», que significa pelota ⚽.", audio="ball")
    b.om(1, "Escucha. ¿Cómo se siente?", "😀", ["😢", "😠", "😴"],
         "Escucha bien: empieza con el sonido /h/.",
         "Escuchaste «happy», que significa feliz 😀.", audio="happy")
    b.om(1, "Escucha y elige la comida.", "🍌", ["🍎", "🍞", "🧀"],
         "Se parece mucho a una palabra en español.",
         "Escuchaste «banana», que significa plátano 🍌.", audio="banana")
    b.nu(1, "Escucha el número y escríbelo.", 12,
         "Es un número entre 10 y 20.",
         "Escuchaste «twelve», que es el 12.", audio="twelve")
    # Nivel 2
    b.om(2, "Escucha y elige la ropa.", "👕", ["👖", "👟", "🧢"],
         "Escucha bien: empieza con el sonido de la letra T.",
         "Escuchaste «T-shirt», que significa polera 👕.", audio="T-shirt")
    b.nu(2, "Escucha el número y escríbelo.", 15,
         "Termina en «-teen», así que está entre 13 y 19.",
         "Escuchaste «fifteen», que es el 15.", audio="fifteen")
    b.om(2, "Escucha. ¿Qué parte de la casa es?", "la cocina 🍳", ["el baño 🛁", "el dormitorio 🛏️", "el living 🛋️"],
         "Recuerda: «bedroom» es dormitorio y «bathroom» es baño.",
         "Escuchaste «kitchen», que significa cocina 🍳.", audio="kitchen")
    b.om(2, "Escucha a Diego. ¿Cómo se siente?", "😠", ["😀", "😢", "😴"],
         "No dice «happy» ni «sad».",
         "Diego dice «I'm angry!», que significa ¡estoy enojado! 😠", audio="I'm angry!")
    # Nivel 3: I like / I don't like
    b.om(3, "Escucha a {personaje}. ¿Qué le gusta?", "🍎", ["🍌", "🍇", "🥕"],
         "Escucha la palabra que va después de «I like».",
         "{personaje} dice «I like apples»: le gustan las manzanas 🍎.", audio="I like apples.")
    b.om(3, "Escucha a Tomás. ¿Qué dice?", "No le gusta la leche.",
         ["Le gusta la leche.", "No le gusta el pan.", "Le gusta el jugo."],
         "Fíjate si dice «I like» o «I don't like».",
         "Tomás dice «I don't like milk»: no le gusta la leche. «Don't» significa no.", audio="I don't like milk.")
    b.co(3, "Escucha a Amanda y completa: «I like ___.»", "ice cream 🍦", ["cake 🍰", "pizza 🍕", "milk 🥛"],
         "Escucha la comida que nombra al final.",
         "Amanda dice «I like ice cream»: le gusta el helado 🍦.", audio="I like ice cream.")
    b.ord(3, "Escucha y ordena la ropa como la nombran.", ["🧦", "👟", "🧢", "👗"],
          "Escucha una prenda a la vez.",
          "El orden es socks 🧦 (calcetines), shoes 👟 (zapatos), cap 🧢 (jockey) y dress 👗 (vestido).",
          audio="Socks, shoes, cap, dress.")
    # Nivel 4
    b.cat(4, "Escucha a Martina. ¿Qué le gusta y qué no?", ["Le gusta 😀", "No le gusta 😖"],
          [("🍕", 0), ("🍰", 0), ("🐟", 1), ("🥕", 1)],
          "Fíjate en «I like» y en «I don't like».",
          "Martina dice «I like pizza, I like cake» (pizza y torta) y «I don't like fish, I don't like carrots» (pescado y zanahorias).",
          audio="I like pizza. I like cake. I don't like fish. I don't like carrots.")
    b.em(4, "Escucha y une a cada niño con cómo se siente.", [["Diego", "😀"], ["Sofía", "😢"], ["Amanda", "😴"]],
         "Escucha primero el nombre y después cómo está.",
         "Diego is happy 😀 (feliz), Sofia is sad 😢 (triste) y Amanda is tired 😴 (cansada).",
         audio="Diego is happy. Sofia is sad. Amanda is tired.")
    b.nu(4, "Escucha a {personaje}. ¿Cuántos juguetes tiene?", 11,
         "Escucha bien el número: hay números que suenan parecido.",
         "Dice «I have eleven toys»: «eleven» es 11 (no confundir con «seven», 7).", audio="I have eleven toys.")
    b.om(4, "Escucha. ¿Dónde está el gato?", "en el dormitorio", ["en la cocina", "en el baño", "en el jardín"],
         "Escucha la última palabra.",
         "Dice «It's in the bedroom»: «bedroom» significa dormitorio.", audio="Where is the cat? It's in the bedroom.")
    # Nivel 5: diálogos y dos datos
    b.om(5, "Escucha el diálogo. ¿Qué fruta le gusta a Diego?", "🍇", ["🍌", "🍎", "🍓"],
         "Ojo: Diego nombra dos frutas, pero solo una le gusta.",
         "A las bananas dice «No, I don't», y luego «I like grapes»: le gustan las uvas 🍇.",
         audio="Do you like bananas, Diego? No, I don't. I like grapes.")
    b.nu(5, "Escucha. ¿Cuántas pelotas hay en total?", 15,
         "Escucha cuántas rojas y cuántas azules hay, y súmalas.",
         "«Ten red balls and five blue balls»: 10 + 5 = 15 pelotas.",
         audio="I have ten red balls and five blue balls.")
    b.om(5, "Escucha. ¿Cómo está Sofía y por qué?", "Feliz, porque es su cumpleaños.",
         ["Triste, porque es su cumpleaños.", "Feliz, porque tiene un perro.", "Cansada, porque es su cumpleaños."],
         "Escucha cómo se siente y qué celebra.",
         "Sofía dice «I'm happy! It's my birthday!»: está feliz porque es su cumpleaños.",
         audio="Hi, Sofia! How are you? I'm happy! It's my birthday!")
    return b.items


def en02_oa13():
    b = Autor("ing", 2, 13)
    # Nivel 1
    b.co(1, "Escucha el modelo y completa la palabra: c___ke 🍰", "a", ["e", "o", "u"],
         "Escucha el sonido después de la c.",
         "Torta se escribe «cake»: c-a-k-e.", audio="cake")
    b.em(1, "Une cada palabra con su dibujo.",
         [["ball", "⚽"], ["car", "🚗"], ["teddy bear", "🧸"], ["balloon", "🎈"]],
         "Piensa en los juguetes que conoces. Ojo: dos empiezan con «ball».",
         "ball es pelota ⚽, car es auto 🚗, teddy bear es oso de peluche 🧸 y balloon es globo 🎈.")
    b.om(1, "{personaje} escribió el modelo «happy» 😀. ¿Qué palabra es igual?", "happy", ["hapy", "happi", "hoppy"],
         "Compara letra por letra con el modelo.",
         "Feliz se escribe «happy»: h-a-p-p-y, con doble p.")
    # Nivel 2
    b.co(2, "Completa: «I like ___.» 🍕", "pizza", ["piza", "milk", "cake"],
         "Mira el dibujo y revisa bien las letras.",
         "🍕 es «pizza», con doble z: «I like pizza» significa me gusta la pizza.")
    b.co(2, "Completa la serie: «eleven, twelve, ___»", "thirteen", ["thirty", "threeteen", "fourteen"],
         "Busca el número que viene después del 12 y revisa sus letras.",
         "13 se escribe «thirteen». «Thirty» es 30.")
    b.cat(2, "¿Es ropa o comida?", ["Ropa 👕", "Comida 🍽️"],
          [("shirt", 0), ("socks", 0), ("dress", 0), ("bread", 1), ("cheese", 1), ("apple", 1)],
          "Piensa qué significa cada palabra.",
          "shirt (camisa), socks (calcetines) y dress (vestido) son ropa; bread (pan), cheese (queso) y apple (manzana) son comida.")
    b.em(2, "Une cada palabra con su significado.",
         [["happy", "feliz"], ["sad", "triste"], ["angry", "enojado"], ["tired", "cansado"]],
         "Piensa en las caras: 😀 😢 😠 😴.",
         "happy es feliz, sad es triste, angry es enojado y tired es cansado.")
    # Nivel 3
    b.ord(3, "Ordena las palabras para escribir «Me gustan las manzanas rojas».", ["I", "like", "red", "apples."],
          "En inglés el color va antes de la fruta.",
          "«I like red apples.» significa me gustan las manzanas rojas.")
    b.co(3, "Completa: «I am ___.» 😢", "sad", ["happy", "angry", "sadd"],
         "Mira la cara: ¿cómo se siente?",
         "😢 es «sad» (triste): «I am sad» significa estoy triste.")
    b.co(3, "Escucha el modelo y completa la palabra: dre___ 👗", "ss", ["s", "sh", "z"],
         "Escucha la palabra y fíjate cómo termina.",
         "Vestido se escribe «dress», con doble s al final.", audio="dress")
    b.ord(3, "Ordena las letras para escribir «milk» 🥛.", ["m", "i", "l", "k"],
          "Empieza con la letra m.",
          "Leche se escribe «milk»: m-i-l-k.")
    # Nivel 4
    b.co(4, "Completa: «I don't ___ carrots.» 🥕😖", "like", ["likes", "liking", "no"],
         "Después de «I don't» va la palabra tal como está, sin cambios.",
         "«I don't like carrots» significa no me gustan las zanahorias.")
    b.ord(4, "Ordena las palabras para escribir «No me gusta el pescado».", ["I", "don't", "like", "fish."],
          "Para decir que no te gusta, usa «don't» antes de «like».",
          "«I don't like fish.» significa no me gusta el pescado.")
    b.co(4, "Completa: «The bed is in the ___.» 🛏️", "bedroom", ["kitchen", "bathroom", "bedrom"],
         "¿En qué parte de la casa duermes? Revisa las letras.",
         "La cama está en el dormitorio: «bedroom», con doble o.")
    b.cat(4, "¿Está bien escrita o mal escrita?", ["Bien escrita ✅", "Mal escrita ❌"],
          [("shoes", 0), ("juice", 0), ("doll", 0), ("shose", 1), ("juise", 1), ("dol", 1)],
          "Lee cada palabra lento y recuerda cómo se ve.",
          "Se escribe shoes (zapatos), juice (jugo) y doll (muñeca); shose, juise y dol están mal escritas.")
    # Nivel 5
    b.co(5, "Sigue el modelo. «I like dogs.» 🐶😀 → «I ___ cats.» 🐱😖", "don't like",
         ["like", "not like", "doesn't like"],
         "La carita 😖 dice que NO le gustan.",
         "Para decir que no te gusta algo se usa «I don't like»: «I don't like cats».")
    b.ord(5, "Escribe en inglés: «Tengo doce juguetes».", ["I", "have", "twelve", "toys."],
          "«Tengo» se dice «I have».",
          "«I have twelve toys.» significa tengo doce juguetes.")
    b.co(5, "Modelo: «My shirt is blue.» 👕💙 Completa: «My ___ is red.» 🧢❤️", "cap", ["shirt", "shoes", "kap"],
         "Mira la prenda que va con el corazón rojo.",
         "🧢 es «cap» (jockey): «My cap is red» significa mi jockey es rojo.")
    return b.items


# ---------------------------------------------------------------- 3° básico
def en03_oa1():
    b = Autor("ing", 3, 1)
    # Nivel 1
    b.om(1, "Escucha. ¿Cómo está el día?", "☀️", ["🌧️", "❄️", "💨"],
         "Escucha con atención y piensa en el cielo.",
         "Escuchaste «It's sunny»: «sunny» significa soleado ☀️.", audio="It's sunny.")
    b.om(1, "Escucha y elige la parte del cuerpo.", "brazo 💪", ["pierna 🦵", "mano ✋", "pie 🦶"],
         "Recuerda: «leg» es pierna y «hand» es mano.",
         "Escuchaste «arm», que significa brazo 💪.", audio="arm")
    b.om(1, "Escucha. ¿Qué día es?", "lunes", ["martes", "domingo", "viernes"],
         "Recuerda: «Sunday» es domingo y «Friday» es viernes.",
         "Escuchaste «Monday», que significa lunes.", audio="Monday")
    b.om(1, "Escucha y elige el animal.", "🐸", ["🐍", "🐢", "🦆"],
         "Escucha bien: empieza con el sonido /f/.",
         "Escuchaste «frog», que significa rana 🐸.", audio="frog")
    # Nivel 2
    b.om(2, "Escucha a Diego. ¿Qué sabe hacer?", "nadar 🏊", ["volar 🦅", "bailar 💃", "cantar 🎤"],
         "Escucha la palabra que va después de «I can».",
         "Diego dice «I can swim»: sabe nadar 🏊.", audio="I can swim.")
    b.om(2, "Escucha. ¿Qué día es?", "jueves", ["martes", "viernes", "miércoles"],
         "Escucha con atención: hay dos días que suenan parecido.",
         "Escuchaste «Thursday», que significa jueves. «Tuesday» es martes.", audio="Thursday")
    b.om(2, "Escucha. ¿Qué hace Martina?", "Se lava los dientes.", ["Se lava las manos.", "Se peina.", "Toma desayuno."],
         "Fíjate en la última palabra.",
         "Martina dice «I brush my teeth»: «teeth» significa dientes, así que se lava los dientes.",
         audio="I brush my teeth.")
    b.nu(2, "Escucha. ¿Cuántos peces hay?", 7,
         "Escucha el número que va después de «There are».",
         "Dice «There are seven fish»: «seven» es 7.", audio="There are seven fish in the river.")
    # Nivel 3
    b.om(3, "Escucha cómo está el día. ¿Qué te pones para salir?", "botas y paraguas ☂️",
         ["traje de baño", "lentes de sol 🕶️", "sandalias"],
         "Escucha las dos palabras que dicen cómo está el día.",
         "Dice «It's rainy and cold»: está lluvioso y frío, así que necesitas botas y paraguas ☂️.",
         audio="It's rainy and cold today.")
    b.em(3, "Escucha y une cada animal con el lugar donde vive.",
         [["🐟", "mar"], ["🐒", "selva"], ["🐪", "desierto"], ["🐄", "granja"]],
         "Escucha qué lugar nombra después de cada animal.",
         "The fish lives in the sea (mar), the monkey in the jungle (selva), the camel in the desert (desierto) y the cow on the farm (granja).",
         audio="The fish lives in the sea. The monkey lives in the jungle. The camel lives in the desert. The cow lives on the farm.")
    b.ord(3, "Escucha la mañana de {personaje} y ordena lo que hace.",
          ["Se levanta.", "Toma desayuno.", "Se lava los dientes.", "Va al colegio."],
          "Escucha las acciones una por una.",
          "Dice: I get up (se levanta), I eat breakfast (toma desayuno), I brush my teeth (se lava los dientes) y I go to school (va al colegio).",
          audio="I get up. I eat breakfast. I brush my teeth. I go to school.")
    b.co(3, "Escucha y completa: «There ___ two dogs in the park.»", "are", ["is", "am", "be"],
         "Son dos perros: más de uno.",
         "Dice «There are two dogs»: con más de uno se usa «there are» (hay).",
         audio="There are two dogs in the park.")
    # Nivel 4
    b.em(4, "Escucha y une a cada niño con lo que sabe hacer.", [["Diego", "🏊"], ["Sofía", "🚲"], ["Amanda", "💃"]],
         "Escucha el nombre y lo que dice después de «can».",
         "Diego can swim 🏊 (nadar), Sofia can ride a bike 🚲 (andar en bici) y Amanda can dance 💃 (bailar).",
         audio="Diego can swim. Sofia can ride a bike. Amanda can dance.")
    b.ord(4, "Escucha qué hace Benjamín cada día y ordénalo de lunes a miércoles.",
          ["nadar 🏊", "bailar 💃", "jugar fútbol ⚽"],
          "Escucha los días: Monday, Tuesday y Wednesday.",
          "El lunes (Monday) nada, el martes (Tuesday) baila y el miércoles (Wednesday) juega fútbol.",
          audio="On Monday, I swim. On Tuesday, I dance. On Wednesday, I play soccer.")
    b.om(4, "Escucha a Tomás. ¿Qué NO puede hacer?", "nadar", ["correr", "saltar", "bailar"],
         "Fíjate en «can't»: significa no puede.",
         "Tomás dice «I can run, but I can't swim»: puede correr, pero no puede nadar.",
         audio="I can run, but I can't swim.")
    b.cat(4, "Escucha a Sofía. ¿Qué hay en su pieza?", ["Hay", "No hay"],
          [("una cama", 0), ("una lámpara", 0), ("dos sillas", 0), ("un televisor", 1), ("una alfombra", 1), ("un ropero", 1)],
          "Escucha lo que dice después de «there is» y «there are».",
          "Sofía dice que hay una cama (a bed), una lámpara (a lamp) y dos sillas (two chairs). No nombra televisor, alfombra ni ropero.",
          audio="In my bedroom, there is a bed and a lamp. There are two chairs.")
    # Nivel 5
    b.nu(5, "Escucha. ¿Cuántos animales hay en la granja en total?", 7,
         "Escucha cuántas vacas y cuántos caballos hay, y súmalos.",
         "«Three cows and four horses»: 3 vacas + 4 caballos = 7 animales.",
         audio="There are three cows and four horses on the farm.")
    b.om(5, "Escucha. ¿Qué día van a la playa y cómo está el tiempo?", "El sábado, con sol.",
         ["El domingo, con sol.", "El sábado, con lluvia.", "El lunes, con viento."],
         "Escucha el día y el clima.",
         "Dice «It's Saturday. It's sunny and hot»: es sábado y hace sol.",
         audio="It's Saturday. It's sunny and hot. Let's go to the beach!")
    b.om(5, "Escucha la adivinanza y elige el animal.", "🐒", ["🐘", "🦁", "🐊"],
         "Escucha dónde vive, qué puede hacer y qué le gusta.",
         "«I live in the jungle, I can climb trees and I like bananas»: vive en la selva, trepa árboles y le gustan los plátanos. Es el mono 🐒.",
         audio="I live in the jungle. I am brown. I can climb trees. I like bananas.")
    return b.items


def en03_oa13():
    b = Autor("ing", 3, 13)
    # Nivel 1
    b.co(1, "Escucha el modelo y completa la palabra: ar___ 💪", "m", ["n", "w", "mm"],
         "Escucha con atención el último sonido.",
         "Brazo se escribe «arm»: a-r-m.", audio="arm")
    b.em(1, "Une cada día con su significado.", [["Monday", "lunes"], ["Friday", "viernes"], ["Sunday", "domingo"]],
         "Fíjate en cómo empieza cada palabra.",
         "Monday es lunes, Friday es viernes y Sunday es domingo.")
    b.om(1, "Copia el modelo «rainy» 🌧️. ¿Qué palabra es igual?", "rainy", ["rainny", "reiny", "rany"],
         "Compara letra por letra con el modelo.",
         "Lluvioso se escribe «rainy»: r-a-i-n-y.")
    b.co(1, "Ayuda a {personaje} a completar: «It's ___.» ☀️", "sunny", ["rainy", "suny", "windy"],
         "Mira el dibujo y revisa bien las letras.",
         "☀️ es «sunny» (soleado), con doble n.")
    # Nivel 2
    b.cat(2, "¿Es una parte del cuerpo o un día de la semana?", ["Parte del cuerpo", "Día de la semana"],
          [("leg", 0), ("head", 0), ("hand", 0), ("Tuesday", 1), ("Saturday", 1), ("Wednesday", 1)],
          "Piensa qué significa cada palabra.",
          "leg (pierna), head (cabeza) y hand (mano) son partes del cuerpo; Tuesday (martes), Saturday (sábado) y Wednesday (miércoles) son días.")
    b.co(2, "Escucha el modelo y completa: Wedn___sday (miércoles)", "e", ["a", "i", "s"],
         "Ojo: esta palabra no se escribe como suena.",
         "Miércoles se escribe «Wednesday»: W-e-d-n-e-s-d-a-y.", audio="Wednesday")
    b.co(2, "Completa: «I ___ swim.» 🏊✅", "can", ["can't", "is", "are"],
         "El ✅ dice que sí puedes.",
         "«I can swim» significa sé nadar. «Can» es poder o saber hacer algo.")
    b.ord(2, "Ordena los días de la semana.", ["Monday", "Tuesday", "Wednesday", "Thursday"],
          "Empieza por el lunes.",
          "Monday (lunes), Tuesday (martes), Wednesday (miércoles) y Thursday (jueves).")
    # Nivel 3
    b.ord(3, "Ordena las palabras para escribir «Me lavo la cara».", ["I", "wash", "my", "face."],
          "En inglés se dice «lavo mi cara».",
          "«I wash my face.» significa me lavo la cara.")
    b.co(3, "Completa: «There ___ three cats.» 🐱🐱🐱", "are", ["is", "am", "be"],
         "Son tres gatos: más de uno.",
         "Con más de uno se usa «there are»: «There are three cats» significa hay tres gatos.")
    b.co(3, "Completa: «A fish lives in the ___.» 🐟🌊", "sea", ["see", "farm", "tree"],
         "Ojo: hay dos palabras que suenan igual.",
         "Mar se escribe «sea». «See» suena igual, pero significa ver.")
    b.em(3, "Une cada oración con su dibujo.",
         [["It's sunny.", "☀️"], ["It's rainy.", "🌧️"], ["It's snowy.", "❄️"], ["It's windy.", "💨"]],
         "Piensa en «sun» (sol), «rain» (lluvia), «snow» (nieve) y «wind» (viento).",
         "sunny es soleado ☀️, rainy es lluvioso 🌧️, snowy es nevado ❄️ y windy es ventoso 💨.")
    # Nivel 4
    b.co(4, "Completa: «A bird can ___, but it can't swim.» 🐦", "fly", ["swim", "fli", "flies"],
         "Después de «can» va la acción tal cual, sin -s.",
         "«A bird can fly» significa un pájaro puede volar. Después de «can» va «fly», sin -s.")
    b.ord(4, "Escribe en inglés: «Un pez no puede caminar».", ["A", "fish", "can't", "walk."],
          "«No puede» se dice «can't».",
          "«A fish can't walk.» significa un pez no puede caminar.")
    b.cat(4, "¿Se usa «There is» o «There are»?", ["There is", "There are"],
          [("a dog", 0), ("one tree", 0), ("a cloud", 0), ("two cats", 1), ("five birds", 1), ("many stars", 1)],
          "Fíjate si es uno o más de uno.",
          "Con uno se usa «there is» (a dog, one tree, a cloud); con más de uno, «there are» (two cats, five birds, many stars).")
    b.co(4, "Completa: «Today is Friday. Tomorrow is ___.»", "Saturday", ["Thursday", "Sunday", "Saturdy"],
         "«Tomorrow» es mañana: el día que viene después.",
         "Después de Friday (viernes) viene Saturday (sábado).")
    # Nivel 5
    b.co(5, "Sigue el modelo. «A monkey lives in the jungle.» 🐒🌴 → «A camel lives in the ___.» 🐪🏜️", "desert",
         ["dessert", "jungle", "sea"],
         "Ojo con la doble s: cambia el significado.",
         "Desierto se escribe «desert». «Dessert», con doble s, significa postre.")
    b.ord(5, "Escribe en inglés: «Hay dos vacas en la granja».", ["There", "are", "two", "cows", "on the farm."],
          "«Hay», con más de uno, se dice «There are».",
          "«There are two cows on the farm.» significa hay dos vacas en la granja.")
    b.co(5, "{personaje} anota el tiempo. Modelo: «On Monday, it's sunny.» ☀️ Completa sobre el martes: «On ___, it's rainy.» 🌧️",
         "Tuesday", ["Thursday", "Monday", "Tusday"],
         "Martes y jueves se parecen en inglés; revisa bien las letras.",
         "Martes se escribe «Tuesday». «Thursday» es jueves.")
    return b.items


# ---------------------------------------------------------------- 4° básico
def en04_oa1():
    b = Autor("ing", 4, 1)
    # Nivel 1
    b.om(1, "Escucha y elige la profesión.", "bombero 🚒", ["policía 🚓", "doctor 🏥", "profesor 🏫"],
         "Es una palabra larga, formada por dos palabras.",
         "Escuchaste «firefighter», que significa bombero 🚒.", audio="firefighter")
    b.om(1, "Escucha. ¿Qué hora es?", "3:00", ["2:00", "8:00", "10:00"],
         "«O'clock» significa en punto.",
         "Escuchaste «It's three o'clock»: son las 3:00.", audio="It's three o'clock.")
    b.om(1, "Escucha y elige el deporte.", "🏀", ["⚽", "🎾", "🏐"],
         "Ojo: varios deportes terminan en «ball».",
         "Escuchaste «basketball», que significa básquetbol 🏀.", audio="basketball")
    b.om(1, "Escucha y elige el lugar.", "parque 🌳", ["banco 🏦", "hospital 🏥", "cine 🎬"],
         "Escucha bien: es una palabra muy cortita.",
         "Escuchaste «park», que significa parque 🌳.", audio="park")
    # Nivel 2
    b.om(2, "Escucha. ¿Qué lugar de la ciudad es?", "biblioteca", ["librería", "laboratorio", "liceo"],
         "Ojo: se parece a una palabra en español, pero no significa lo mismo.",
         "«Library» significa biblioteca, no librería (que en inglés es «bookstore»).", audio="library")
    b.om(2, "Escucha. ¿Dónde está la pelota?", "debajo de la mesa",
         ["sobre la mesa", "dentro de la caja", "al lado de la mesa"],
         "Fíjate en la palabra que va antes de «the table».",
         "Dice «under the table»: «under» significa debajo de.", audio="The ball is under the table.")
    b.nu(2, "Escucha a {personaje}. ¿Qué hora es? Escribe solo el número.", 10,
         "«O'clock» significa en punto.",
         "Dice «It's ten o'clock»: son las 10 en punto.", unidad="en punto", audio="It's ten o'clock.")
    b.om(2, "Escucha a Amanda. ¿Qué toma al desayuno?", "jugo de naranja 🍊", ["leche 🥛", "té ☕", "agua 💧"],
         "Escucha lo que dice después de «I drink».",
         "Amanda dice «I drink orange juice»: toma jugo de naranja 🍊.",
         audio="I drink orange juice for breakfast.")
    # Nivel 3
    b.om(3, "Escucha. ¿Qué está haciendo Vicente?", "Está corriendo. 🏃",
         ["Está nadando. 🏊", "Está leyendo. 📖", "Está durmiendo. 😴"],
         "La acción que termina en «-ing» dice lo que está haciendo ahora.",
         "Dice «He is running»: está corriendo 🏃.", audio="Look! He is running.")
    b.em(3, "Escucha y une cada profesión con su lugar de trabajo.",
         [["profesor", "escuela 🏫"], ["doctor", "hospital 🏥"], ["cocinero", "restaurante 🍽️"]],
         "Escucha lo que dice después de «works in».",
         "A teacher (profesor) works in a school (escuela), a doctor works in a hospital y a cook (cocinero) works in a restaurant (restaurante).",
         audio="A teacher works in a school. A doctor works in a hospital. A cook works in a restaurant.")
    b.co(3, "Escucha y completa: «The cat is ___ the bed.»", "on", ["in", "under", "at"],
         "Escucha la palabra cortita que va antes de «the bed».",
         "Dice «The cat is on the bed»: «on» significa sobre (encima de).", audio="The cat is on the bed.")
    # Nivel 4
    b.em(4, "Escucha y une a cada niño con la hora en que se levanta.",
         [["Diego", "8:00"], ["Sofía", "6:00"], ["Amanda", "7:00"]],
         "Escucha el nombre y después la hora. «Gets up» significa se levanta.",
         "Diego gets up at eight (8:00), Sofia at six (6:00) y Amanda at seven (7:00).",
         audio="Diego gets up at eight. Sofia gets up at six. Amanda gets up at seven.")
    b.ord(4, "Escucha la tarde de Josefa y ordena lo que hace.",
          ["tocar guitarra 🎸", "leer un libro 📖", "andar en bici 🚲"],
          "Escucha «first» (primero), «then» (luego) y «finally» (al final).",
          "Primero (first) toca guitarra, luego (then) lee un libro y al final (finally) anda en bici.",
          audio="First, I play the guitar. Then, I read a book. Finally, I ride my bike.")
    b.cat(4, "Escucha a Diego. ¿Qué le gusta hacer y qué no?", ["Le gusta 😀", "No le gusta 😖"],
          [("nadar 🏊", 0), ("jugar fútbol ⚽", 0), ("bailar 💃", 1), ("leer 📖", 1)],
          "Fíjate en «I like» y en «I don't like».",
          "Diego dice que le gusta swimming (nadar) y playing soccer (jugar fútbol), pero no le gusta dancing (bailar) ni reading (leer).",
          audio="I like swimming and playing soccer. I don't like dancing or reading.")
    b.om(4, "Escucha. ¿Qué hora es?", "4:30", ["4:15", "3:30", "5:30"],
         "«Half» significa media.",
         "Dice «half past four»: las cuatro y media, 4:30.", audio="What time is it? It's half past four.")
    # Nivel 5
    b.om(5, "Escucha. ¿Dónde está la mamá y qué está haciendo?", "En la cocina, cocinando.",
         ["En el comedor, comiendo.", "En la cocina, lavando platos.", "En el jardín, cocinando."],
         "Escucha el lugar y la acción que termina en «-ing».",
         "Dice «She is in the kitchen. She is cooking»: está en la cocina, cocinando.",
         audio="Where is Mom? She is in the kitchen. She is cooking.")
    b.om(5, "Escucha la adivinanza. ¿Qué profesión es?", "veterinario", ["doctor", "granjero", "cocinero"],
         "Fíjate a quién ayuda esta persona.",
         "«I work with animals. I help sick dogs and cats»: ayuda a animales enfermos, así que es veterinario.",
         audio="I work with animals. I help sick dogs and cats.")
    b.nu(5, "Escucha. ¿A qué hora termina la película? Escribe solo el número.", 7,
         "Escucha a qué hora empieza y cuántas horas dura; luego súmalas.",
         "Empieza «at five o'clock» (5:00) y dura «two hours» (2 horas): 5 + 2 = 7 en punto.",
         unidad="en punto", audio="The movie starts at five o'clock. It is two hours long.")
    return b.items


def en04_oa13():
    b = Autor("ing", 4, 13)
    # Nivel 1
    b.co(1, "Escucha el modelo y completa la palabra: sch___ol 🏫", "o", ["u", "oo", "a"],
         "Revisa el modelo: lleva dos letras iguales seguidas.",
         "Escuela se escribe «school»: s-c-h-o-o-l.", audio="school")
    b.em(1, "Une cada profesión con su significado.",
         [["teacher", "profesor"], ["farmer", "granjero"], ["firefighter", "bombero"], ["cook", "cocinero"]],
         "Piensa en «farm» (granja) y «fire» (fuego).",
         "teacher es profesor, farmer es granjero, firefighter es bombero y cook es cocinero.")
    b.om(1, "Copia el modelo «breakfast» 🍳. ¿Qué palabra es igual?", "breakfast",
         ["brekfast", "breakfas", "braekfast"],
         "Compara letra por letra con el modelo.",
         "Desayuno se escribe «breakfast»: b-r-e-a-k-f-a-s-t.")
    # Nivel 2
    b.co(2, "Completa: «It's ___ o'clock.» (8:00)", "eight", ["eigth", "ate", "seven"],
         "Busca el número 8 y revisa bien sus letras.",
         "8 se escribe «eight»: «It's eight o'clock» significa son las ocho en punto.")
    b.cat(2, "¿Es un deporte o un lugar de la ciudad?", ["Deporte", "Lugar"],
          [("tennis", 0), ("volleyball", 0), ("swimming", 0), ("bank", 1), ("museum", 1), ("zoo", 1)],
          "Piensa qué significa cada palabra.",
          "tennis (tenis), volleyball (vóleibol) y swimming (natación) son deportes; bank (banco), museum (museo) y zoo (zoológico) son lugares.")
    b.co(2, "Completa: «The cat is ___ the box.» (El gato está dentro de la caja.)", "in", ["on", "under", "at"],
         "«Dentro de» se dice con una palabra muy corta.",
         "«In» significa dentro de: «The cat is in the box».")
    b.em(2, "Une cada palabra con su dibujo.",
         [["guitar", "🎸"], ["bike", "🚲"], ["camera", "📷"], ["piano", "🎹"]],
         "Varias se parecen al español.",
         "guitar es guitarra 🎸, bike es bicicleta 🚲, camera es cámara 📷 y piano es piano 🎹.")
    # Nivel 3
    b.co(3, "Completa: «She is ___.» 🏃‍♀️", "running", ["runing", "run", "runs"],
         "Después de «is», la acción termina en -ing. Revisa bien las letras.",
         "«She is running» significa ella está corriendo. «Run» dobla la n: running.")
    b.ord(3, "Ordena las palabras para escribir «Mi papá está cocinando».", ["My", "dad", "is", "cooking."],
          "«Está cocinando» se dice con «is» y una acción terminada en -ing.",
          "«My dad is cooking.» significa mi papá está cocinando.")
    b.co(3, "Ayuda a {personaje} a completar: «I have lunch at ___ o'clock.» (1:00)", "one", ["won", "two", "first"],
         "Busca cómo se escribe el número 1.",
         "1 se escribe «one». «Won» suena igual, pero significa ganó.")
    b.ord(3, "Ordena las sílabas para escribir «basketball» 🏀.", ["bas", "ket", "ball"],
          "Termina con «ball» (pelota).",
          "Básquetbol se escribe «basketball»: bas-ket-ball.")
    # Nivel 4
    b.co(4, "Completa: «The shoes are ___ the bed.» (Los zapatos están debajo de la cama.)", "under",
         ["on", "in", "onder"],
         "Piensa qué significa cada palabra y revisa las letras.",
         "«Under» significa debajo de: «The shoes are under the bed».")
    b.ord(4, "Escribe en inglés: «Los niños están jugando fútbol».", ["The", "children", "are", "playing", "soccer."],
          "Con varios niños se usa «are», y la acción termina en -ing.",
          "«The children are playing soccer.» significa los niños están jugando fútbol.")
    b.cat(4, "¿Se completa con «is» o con «are»?", ["is", "are"],
          [("She ___ dancing.", 0), ("My dad ___ cooking.", 0), ("The dog ___ sleeping.", 0),
           ("They ___ swimming.", 1), ("We ___ reading.", 1), ("The girls ___ singing.", 1)],
          "Si es uno, va «is»; si son varios, va «are».",
          "She, my dad y the dog son uno: «is». They, we y the girls son varios: «are».")
    b.co(4, "Completa: «A ___ works in a hospital.» 🏥", "nurse", ["farmer", "nurce", "pilot"],
         "¿Quién cuida a los enfermos? Revisa bien las letras.",
         "«Nurse» significa enfermera o enfermero, y trabaja en un hospital.")
    # Nivel 5
    b.co(5, "Sigue el modelo. «I play tennis.» → «I am playing tennis.» Completa: «I read a book.» → «I am ___ a book.»",
         "reading", ["read", "reads", "readding"],
         "Agrega -ing como en el modelo y revisa si la letra se dobla.",
         "«Read» + -ing = «reading»: «I am reading a book» significa estoy leyendo un libro.")
    b.ord(5, "Escribe en inglés: «El gato está debajo de la silla».", ["The cat", "is", "under", "the chair."],
          "Primero quién, después dónde está.",
          "«The cat is under the chair.» significa el gato está debajo de la silla.")
    b.co(5, "Modelo: «A firefighter works in a fire station.» Completa: «A teacher works in a ___.»", "school",
         ["hospital", "scool", "bank"],
         "¿Dónde trabaja un profesor? Revisa bien las letras.",
         "Un profesor (teacher) trabaja en una escuela: «school».")
    return b.items


GENERADORES = {
    "1_basico.ingles.OA1": en01_oa1,
    "1_basico.ingles.OA13": en01_oa13,
    "2_basico.ingles.OA1": en02_oa1,
    "2_basico.ingles.OA13": en02_oa13,
    "3_basico.ingles.OA1": en03_oa1,
    "3_basico.ingles.OA13": en03_oa13,
    "4_basico.ingles.OA1": en04_oa1,
    "4_basico.ingles.OA13": en04_oa13,
}
