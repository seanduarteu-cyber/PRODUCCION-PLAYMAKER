"""Ciencias Naturales 1° a 4° básico: 15 a 17 desafíos por OA (3 o 4 por nivel de dificultad, 1 a 5)."""
from autor import Autor


def cn01_oa1():
    b = Autor("cie", 1, 1)
    b.om(1, "¿Cuál es un ser vivo?", "🐶", ["🪨", "🚗", "🧸"],
         "Busca el que come, respira y crece.", "El perro 🐶 es un ser vivo: come, respira y crece.")
    b.cat(1, "¿Ser vivo o no vivo?", ["Ser vivo 🌱", "No vivo 🪨"],
          [("🐱 gato", 0), ("🌳 árbol", 0), ("🐦 pájaro", 0), ("🪨 piedra", 1), ("⚽ pelota", 1), ("🪑 silla", 1)],
          "Los seres vivos comen, respiran y crecen.", "Gato, árbol y pájaro son seres vivos; piedra, pelota y silla no.")
    b.co(1, "El pollito 🐣 ___ y se vuelve gallina 🐔.", "crece", ["se rompe", "se derrite", "se apaga"],
         "Piensa en cómo cambia con el tiempo.", "El pollito crece hasta ser gallina: los seres vivos crecen.")
    b.co(2, "El conejo 🐰 necesita ___ para vivir.", "agua y alimento", ["juguetes", "ropa", "zapatos"],
         "¿Qué le das a una mascota cada día?", "El conejo necesita agua y alimento, como todos los seres vivos.")
    b.om(2, "¿Qué necesitan todos los seres vivos?", "agua, alimento y aire 💧", ["juguetes y pelotas ⚽", "ropa y zapatos 👟", "luz de lámpara 💡"],
         "Sin esto, ningún ser vivo puede vivir.", "Todos los seres vivos necesitan agua, alimento y aire.")
    b.em(2, "Une cada animal con su cría.",
         [["🐔 gallina", "🐣 pollito"], ["🐄 vaca", "ternero"], ["🐶 perra", "cachorro"], ["🐸 rana", "renacuajo"]],
         "Las crías son los hijos de cada animal.", "Gallina-pollito, vaca-ternero, perra-cachorro, rana-renacuajo: los seres vivos se reproducen.")
    b.ord(2, "Ordena cómo crece una planta.", ["🌰 semilla", "🌱 brote", "🪴 planta pequeña", "🌳 árbol"],
          "Empieza por lo más pequeño.", "Semilla → brote → planta pequeña → árbol: la planta crece.")
    b.om(3, "Un gato 🐱 oye un ruido 🔔 y corre. ¿Qué hace el gato?", "responde a un estímulo", ["crece", "se reproduce", "se alimenta"],
         "El ruido lo hizo reaccionar.", "El gato reacciona al ruido: responde a un estímulo.")
    b.em(3, "Une cada ejemplo con lo que muestra.",
         [["👶 el bebé se hace grande", "crece"], ["🐱 la gata tiene gatitos", "se reproduce"], ["🐶 el perro viene si lo llamas", "responde a estímulos"]],
         "Busca la palabra que explica cada ejemplo.", "Hacerse grande es crecer; tener crías es reproducirse; reaccionar al llamado es responder a estímulos.")
    b.nu(3, "¿Cuántos son seres vivos? 🐦 🪑 🌻 ⚽ 🐞 🧸 🐄", 4,
         "Cuenta solo los que comen o crecen.", "Pájaro, girasol, chinita y vaca son seres vivos: son 4.", unidad="seres vivos")
    b.om(4, "La planta 🪴 de la ventana se inclina hacia el sol ☀️. ¿Qué muestra?", "que responde a estímulos",
         ["que es una cosa no viva", "que no necesita agua", "que se está reproduciendo"],
         "La luz es lo que la hace moverse.", "La planta se inclina hacia la luz: responde a un estímulo, como los seres vivos.")
    b.cat(4, "¿Ser vivo o no vivo? ¡Cuidado!", ["Ser vivo", "No vivo"],
          [("🌰 semilla", 0), ("🍄 hongo", 0), ("🐛 gusano", 0), ("🔥 fuego", 1), ("☁️ nube", 1), ("🤖 robot", 1)],
          "Algo puede moverse o cambiar y no estar vivo.", "Semilla, hongo y gusano están vivos; el fuego, la nube y el robot no comen ni se reproducen.")
    b.co(4, "El auto 🚗 se mueve, pero no es un ser vivo porque no ___.", "crece ni se reproduce", ["tiene ruedas", "hace ruido", "tiene color"],
         "Piensa en lo que hacen todos los seres vivos.", "El auto no crece ni se reproduce: por eso no es un ser vivo.")
    b.om(5, "{personaje} pone una piedra 🪨 y un poroto 🫘 en algodón mojado. Pasan unos días. ¿Qué ocurre?",
         "El poroto brota y la piedra sigue igual.", ["La piedra crece y el poroto no.", "Los dos brotan.", "Los dos se convierten en árboles."],
         "Solo uno de los dos es un ser vivo.", "El poroto es una semilla viva y brota; la piedra no es un ser vivo y no cambia.")
    b.om(5, "Martina no riega su planta 🪴 por muchas semanas. ¿Qué le pasará?", "Se secará, porque le falta agua.",
         ["Crecerá más rápido.", "Seguirá igual para siempre.", "Tendrá más flores."],
         "¿Qué necesitan todos los seres vivos?", "Sin agua la planta se seca: los seres vivos necesitan agua para vivir.")
    b.cat(5, "¿Esto prueba que algo es un ser vivo?", ["Sí, es de seres vivos", "No lo prueba"],
          [("crece", 0), ("se reproduce", 0), ("respira", 0), ("se mueve con el viento", 1), ("tiene colores", 1), ("brilla", 1)],
          "Una bolsa también se mueve con el viento.", "Crecer, reproducirse y respirar son de seres vivos; moverse con el viento, tener color o brillar, no.")
    return b.items


def cn01_oa4():
    b = Autor("cie", 1, 4)
    b.om(1, "¿Cuál es una flor?", "🌻", ["🍎", "🫘", "🪵"],
         "Tiene pétalos de colores.", "El girasol 🌻 es una flor.")
    b.om(1, "¿Cuál es un fruto?", "🍎", ["🌷", "🫘", "🪵"],
         "Se come y tiene semillas adentro.", "La manzana 🍎 es un fruto: guarda semillas adentro.")
    b.cat(1, "¿Grande o pequeño?", ["Grande", "Pequeño"],
          [("🍉 sandía", 0), ("🎃 zapallo", 0), ("🍍 piña", 0), ("🫐 arándano", 1), ("🍒 cereza", 1), ("🫘 poroto", 1)],
          "Piensa si cabe en tu mano.", "Sandía, zapallo y piña son grandes; arándano, cereza y poroto son pequeños.")
    b.cat(2, "Ordena por color.", ["Rojo 🔴", "Amarillo 🟡"],
          [("🍓 frutilla", 0), ("🍒 cereza", 0), ("🍅 tomate", 0), ("🍌 plátano", 1), ("🍋 limón", 1), ("🌻 girasol", 1)],
          "Mira bien el color de cada uno.", "Frutilla, cereza y tomate son rojos; plátano, limón y girasol son amarillos.")
    b.em(2, "Une cada parte de la planta con un ejemplo.",
         [["flor", "🌷 tulipán"], ["fruto", "🍐 pera"], ["semilla", "🫘 poroto"], ["tallo", "🪵 tronco"]],
         "El tronco sostiene al árbol.", "Tulipán: flor; pera: fruto; poroto: semilla; tronco: tallo.")
    b.co(2, "La cáscara de la piña 🍍 es ___ al tocarla.", "áspera", ["lisa", "blanda", "suave"],
         "Imagina que pasas tu mano por encima.", "La cáscara de la piña es áspera: tiene muchas escamas duras.")
    b.cat(3, "Clasifica por textura.", ["Piel lisa", "Piel áspera o peluda"],
          [("🍎 manzana", 0), ("🍒 cereza", 0), ("🍅 tomate", 0), ("🍍 piña", 1), ("🥥 coco", 1), ("🥝 kiwi", 1)],
          "La textura es cómo se siente al tocar.", "Manzana, cereza y tomate son lisos; piña, coco y kiwi son ásperos o peludos.")
    b.nu(3, "¿Cuántos frutos son rojos? 🍎 🍌 🍓 🍋 🍒 🍐", 3,
         "Fíjate solo en el color.", "Manzana, frutilla y cereza son rojas: son 3.", unidad="frutos")
    b.em(3, "Une cada fruto con su forma.",
         [["🍌 plátano", "alargada y curva"], ["🍊 naranja", "redonda"], ["🍐 pera", "ancha abajo, angosta arriba"]],
         "Imagina el contorno de cada fruto.", "El plátano es alargado y curvo, la naranja es redonda y la pera es ancha abajo.")
    b.ord(3, "Ordena las semillas de la más pequeña a la más grande.", ["semilla de frutilla 🍓", "lenteja", "poroto 🫘", "cuesco de palta 🥑"],
          "Las de la frutilla son puntitos en su piel.", "Semilla de frutilla → lenteja → poroto → cuesco de palta.")
    b.om(4, "¿Qué criterio usó Tomás? Grupo A: 🍉 🎃 🍍  Grupo B: 🫐 🍒 🫘", "tamaño", ["color", "textura", "sabor"],
         "Compara cuánto espacio ocupa cada uno.", "En el grupo A todos son grandes y en el B todos pequeños: usó el tamaño.")
    b.co(4, "Diego separó 🍏 🍒 🍋 de 🍍 🥥 🥝. Usó el criterio de ___.", "textura", ["color", "tamaño", "sabor"],
         "Hay colores y tamaños distintos en cada grupo.", "Manzana verde, cereza y limón son lisos; piña, coco y kiwi son ásperos: usó la textura.")
    b.cat(4, "Clasifica los tallos según su textura.", ["Duro y rugoso", "Blando y liso"],
          [("tronco de roble", 0), ("tronco de araucaria", 0), ("rama de pino", 0), ("tallo de tulipán", 1), ("tallo de margarita", 1), ("tallo de pasto", 1)],
          "Los troncos de los árboles son de madera.", "Los troncos y ramas de árboles son duros y rugosos; los tallos de flores y pasto son blandos y lisos.")
    b.om(5, "{personaje} toca un fruto con los ojos cerrados. Es grande, áspero y tiene hojas arriba. ¿Cuál es?", "🍍 piña",
         ["🍒 cereza", "🍉 sandía", "🍎 manzana"],
         "Usa las tres pistas: tamaño, textura y forma.", "La piña es grande, áspera y tiene hojas arriba; la sandía es grande pero lisa.")
    b.nu(5, "{personaje} clasifica 10 semillas por tamaño. 6 son grandes y el resto, pequeñas. ¿Cuántas son pequeñas?", 4,
         "Quita las grandes del total.", "10 − 6 = 4: hay 4 semillas pequeñas.", unidad="semillas")
    b.co(5, "🍓 🍒 🫐 🍇 se parecen en su ___.", "tamaño", ["color", "forma", "textura"],
         "Unos son rojos, otros azules; unos lisos, otros no.", "Todos son frutos pequeños: se parecen en su tamaño, no en color, forma ni textura.")
    b.ord(5, "Ordena del fruto más pequeño al más grande.", ["🫐 arándano", "🍒 cereza", "🍋 limón", "🍍 piña", "🍉 sandía"],
          "Empieza por el que es como una bolita.", "Arándano → cereza → limón → piña → sandía.")
    return b.items


def cn01_oa12():
    b = Autor("cie", 1, 12)
    b.om(1, "¿En qué estación hace más calor? ☀️", "verano", ["invierno", "otoño", "primavera"],
         "Es la estación de ir a la playa.", "En verano hace más calor.")
    b.om(1, "¿Qué ropa usas en invierno? ❄️", "🧥 parka", ["🩱 traje de baño", "🩴 chalas", "🕶️ lentes de sol"],
         "En invierno hace frío.", "En invierno usamos parka para abrigarnos del frío.")
    b.em(1, "Une cada estación con su dibujo.", [["verano", "☀️"], ["otoño", "🍂"], ["invierno", "❄️"], ["primavera", "🌸"]],
         "Piensa en el clima de cada estación.", "Verano ☀️, otoño 🍂, invierno ❄️ y primavera 🌸.")
    b.ord(2, "Ordena las estaciones, empezando por el verano.", ["verano ☀️", "otoño 🍂", "invierno ❄️", "primavera 🌸"],
          "Después del calor, empiezan a caer las hojas.", "Verano → otoño → invierno → primavera, y vuelve el verano.")
    b.co(2, "En otoño 🍂, las hojas de muchos árboles se ___.", "caen", ["derriten", "vuelven azules", "multiplican"],
         "Mira el suelo de una plaza en otoño.", "En otoño muchos árboles pierden sus hojas: se caen.")
    b.om(2, "¿En qué estación los árboles se llenan de flores nuevas 🌸 después del frío?", "primavera", ["otoño", "invierno", "verano"],
         "Viene justo después del invierno.", "En primavera las plantas florecen después del frío del invierno.")
    b.cat(3, "¿Verano o invierno?", ["Verano ☀️", "Invierno ❄️"],
          [("días calurosos", 0), ("ir a la playa 🏖️", 0), ("días más largos", 0), ("lluvia y frío 🌧️", 1), ("nieve en la cordillera 🏔️", 1), ("días más cortos", 1)],
          "Piensa en el calor y en el frío.", "En verano hay calor, playa y días largos; en invierno, lluvia, nieve y días cortos.")
    b.om(3, "En Chile, ¿en qué mes empieza el verano?", "diciembre", ["junio", "marzo", "septiembre"],
         "Es el mes de Navidad.", "En Chile el verano empieza en diciembre y dura hasta marzo.")
    b.co(3, "En Chile, el invierno empieza en ___.", "junio", ["diciembre", "marzo", "septiembre"],
         "Es a mitad de año.", "En Chile el invierno empieza en junio y dura hasta septiembre.")
    b.om(4, "¿Por qué muchos animales tienen el pelo más grueso en invierno?", "para protegerse del frío",
         ["para nadar mejor", "porque comen más fruta", "para esconderse del sol"],
         "Piensa para qué te pones parka.", "El pelo grueso los abriga, como una parka: los protege del frío.")
    b.em(4, "Une cada estación con lo que pasa en la naturaleza.",
         [["primavera", "nacen flores y brotes"], ["verano", "maduran muchas frutas"], ["otoño", "caen las hojas"], ["invierno", "llueve y nieva más"]],
         "Las cerezas y sandías se comen en el calor.", "Primavera: flores; verano: frutas maduras; otoño: caen hojas; invierno: lluvia y nieve.")
    b.nu(4, "Cada estación dura más o menos el mismo tiempo. ¿Cuántos meses dura cada una?", 3,
         "Un año tiene 12 meses y 4 estaciones.", "12 meses repartidos en 4 estaciones: cada una dura unos 3 meses.", unidad="meses")
    b.om(5, "En el cumpleaños de {personaje} hace frío y llueve. ¿En qué mes puede ser?", "julio", ["enero", "febrero", "diciembre"],
         "En Chile, ¿cuándo hace frío?", "Julio es invierno en Chile: hace frío y llueve. Enero, febrero y diciembre son de verano.")
    b.om(5, "En Chile, Navidad 🎄 es en diciembre. ¿Qué estación empieza?", "verano", ["invierno", "otoño", "primavera"],
         "En Chile, en Navidad hace calor.", "En Chile el verano empieza en diciembre; por eso en Navidad hace calor.")
    b.ord(5, "Ordena lo que le pasa a un cerezo en el año, desde la primavera.", ["🌸 florece", "🍒 da frutos", "🍂 se le caen las hojas", "❄️ queda sin hojas"],
          "Las flores llegan después del frío.", "Primavera: florece; verano: da cerezas; otoño: bota las hojas; invierno: queda sin hojas.")
    b.cat(5, "En Chile, ¿ropa de verano o de invierno en cada mes?", ["Ropa de verano 🩱", "Ropa de invierno 🧥"],
          [("enero", 0), ("febrero", 0), ("julio", 1), ("agosto", 1)],
          "Recuerda: el verano empieza en diciembre.", "Enero y febrero son de verano; julio y agosto, de invierno.")
    return b.items


def cn02_oa1():
    b = Autor("cie", 2, 1)
    b.om(1, "¿Qué animal tiene plumas? 🪶", "🐦", ["🐶", "🐟", "🐸"],
         "Las plumas sirven para volar y abrigarse.", "El pájaro 🐦 tiene plumas: es un ave.")
    b.om(1, "¿Cuál es un pez?", "🐟", ["🐱", "🐦", "🐍"],
         "Vive en el agua y tiene aletas.", "El pez 🐟 vive en el agua, tiene aletas y escamas.")
    b.co(1, "El perro 🐶 tiene el cuerpo cubierto de ___.", "pelo", ["plumas", "escamas", "piel húmeda"],
         "Piensa en cómo se siente al acariciarlo.", "El perro tiene pelo, como todos los mamíferos.")
    b.cat(2, "¿Mamífero o ave?", ["Mamífero", "Ave"],
          [("🐄 vaca", 0), ("🐶 perro", 0), ("pudú", 0), ("🐧 pingüino", 1), ("cóndor", 1), ("🐔 gallina", 1)],
          "Las aves tienen plumas; los mamíferos, pelo.", "Vaca, perro y pudú son mamíferos; pingüino, cóndor y gallina son aves.")
    b.co(2, "Los peces 🐟 respiran con ___.", "branquias", ["pulmones", "la piel seca", "plumas"],
         "Es una estructura que saca el aire del agua.", "Los peces respiran con branquias, que toman el oxígeno del agua.")
    b.om(2, "¿Qué tienen las mamás mamíferas para alimentar a sus crías? 🍼", "mamas con leche", ["plumas", "escamas", "branquias"],
         "Su nombre viene de esta parte del cuerpo.", "Los mamíferos tienen mamas: alimentan a sus crías con leche.")
    b.cat(3, "¿Mamífero, reptil o pez?", ["Mamífero", "Reptil", "Pez"],
          [("🐱 gato", 0), ("huemul", 0), ("🦎 lagartija", 1), ("🐢 tortuga", 1), ("jurel", 2), ("🦈 tiburón", 2)],
          "Fíjate en si tiene pelo, escamas secas o aletas y branquias.", "Gato y huemul: mamíferos; lagartija y tortuga: reptiles; jurel y tiburón: peces.")
    b.em(3, "Une cada grupo con su cubierta.",
         [["mamíferos", "pelo"], ["aves", "plumas"], ["reptiles", "escamas secas"], ["anfibios", "piel húmeda y desnuda"]],
         "La rana es un anfibio.", "Mamíferos: pelo; aves: plumas; reptiles: escamas secas; anfibios: piel húmeda y desnuda.")
    b.nu(3, "¿Cuántos son aves? 🐧 🐶 🦅 🐟 🦜 🐍", 3,
         "Cuenta los que tienen plumas.", "Pingüino, águila y loro tienen plumas: son 3 aves.", unidad="aves")
    b.om(4, "La ballena 🐋 vive en el mar, pero es un mamífero. ¿Por qué?", "respira con pulmones y amamanta a sus crías",
         ["porque es muy grande", "porque nada", "porque tiene aletas"],
         "Piensa en cómo respira y cómo alimenta a sus crías.", "La ballena respira con pulmones y sus crías toman leche: es un mamífero.")
    b.nu(4, "¿Cuántos son mamíferos? 🐬 🐟 🦇 🐦 🐄 🐍", 3,
         "¡Ojo! Algunos mamíferos nadan o vuelan.", "Delfín, murciélago y vaca son mamíferos: son 3.", unidad="mamíferos")
    b.cat(4, "¿Con qué respira?", ["Pulmones", "Branquias"],
          [("🐬 delfín", 0), ("🐢 tortuga marina", 0), ("🐧 pingüino", 0), ("salmón", 1), ("🦈 tiburón", 1), ("congrio", 1)],
          "Que viva en el agua no significa que tenga branquias.", "Delfín, tortuga y pingüino suben a respirar con pulmones; salmón, tiburón y congrio usan branquias.")
    b.om(5, "{personaje} ve un animal con escamas secas, que respira con pulmones y pone huevos en la arena. ¿Qué es?", "un reptil",
         ["un pez", "un anfibio", "un ave"],
         "Los peces tienen branquias y los anfibios, piel húmeda.", "Escamas secas, pulmones y huevos en tierra: es un reptil, como la tortuga.")
    b.om(5, "El murciélago 🦇 vuela, pero tiene pelo y sus crías toman leche. ¿Qué es?", "un mamífero", ["un ave", "un reptil", "un insecto"],
         "Volar no lo hace ave: busca plumas.", "Tiene pelo y amamanta: el murciélago es un mamífero que vuela.")
    b.ord(5, "Ordena cómo cambia la rana 🐸 en su vida.", ["huevo", "renacuajo con branquias", "renacuajo con patas", "rana adulta con pulmones"],
          "Primero vive solo en el agua.", "Huevo → renacuajo con branquias → renacuajo con patas → rana con pulmones.")
    b.cat(5, "¿Ave, reptil o anfibio?", ["Ave", "Reptil", "Anfibio"],
          [("🐧 pingüino", 0), ("flamenco", 0), ("🐊 cocodrilo", 1), ("🐍 culebra", 1), ("sapo", 2), ("salamandra", 2)],
          "Plumas, escamas secas o piel húmeda.", "Pingüino y flamenco: aves; cocodrilo y culebra: reptiles; sapo y salamandra: anfibios.")
    return b.items


def cn02_oa7():
    b = Autor("cie", 2, 7)
    b.om(1, "¿Qué órgano late y bombea la sangre? 🫀", "el corazón", ["el estómago", "los pulmones", "los huesos"],
         "Lo sientes en el pecho: pum, pum.", "El corazón late y bombea la sangre a todo el cuerpo.")
    b.om(1, "¿Con qué órganos respiras? 🌬️", "los pulmones", ["el corazón", "el estómago", "los músculos"],
         "Se llenan de aire cuando inspiras.", "Respiras con los pulmones.")
    b.em(1, "Une cada parte con su dibujo.", [["corazón", "🫀"], ["pulmones", "🫁"], ["huesos", "🦴"], ["músculos", "💪"]],
         "El brazo fuerte muestra un músculo.", "Corazón 🫀, pulmones 🫁, huesos 🦴 y músculos 💪.")
    b.co(2, "Al tragar, la comida 🍎 llega al ___.", "estómago", ["corazón", "pulmón", "cráneo"],
         "Está en la guatita.", "La comida baja hasta el estómago, donde se procesa.")
    b.om(2, "¿Qué parte del cuerpo te sostiene y te da forma? 🦴", "el esqueleto", ["el estómago", "los pulmones", "la sangre"],
         "Está formado por huesos.", "El esqueleto es el conjunto de huesos que sostiene el cuerpo.")
    b.co(2, "Cuando inspiras, los pulmones se llenan de ___.", "aire", ["sangre", "comida", "agua"],
         "Respira hondo y fíjate en tu pecho.", "Al inspirar, los pulmones se llenan de aire.")
    b.cat(3, "¿Dónde está cada órgano?", ["Pecho", "Guatita (abdomen)"],
          [("🫀 corazón", 0), ("🫁 pulmones", 0), ("estómago", 1), ("intestinos", 1)],
          "Las costillas cubren el pecho.", "Corazón y pulmones están en el pecho; estómago e intestinos, en la guatita.")
    b.co(3, "Los ___ mueven los huesos cuando caminas.", "músculos", ["pulmones", "intestinos", "dientes"],
         "Se ponen duros cuando haces fuerza.", "Los músculos tiran de los huesos y así nos movemos.")
    b.em(3, "Une cada parte con su función.",
         [["corazón", "bombea la sangre"], ["pulmones", "toman el aire"], ["estómago", "procesa la comida"],
          ["músculos", "mueven el cuerpo"], ["esqueleto", "sostiene el cuerpo"]],
         "Piensa en qué pasaría si cada uno no funcionara.", "Corazón: sangre; pulmones: aire; estómago: comida; músculos: movimiento; esqueleto: sostén.")
    b.nu(4, "El corazón de Josefa late 80 veces en 1 minuto. ¿Cuántas veces late en 2 minutos?", 160,
         "Suma los latidos de cada minuto.", "80 + 80 = 160 latidos en 2 minutos.", unidad="latidos")
    b.om(4, "¿Qué protegen las costillas?", "el corazón y los pulmones", ["el estómago y los pies", "los músculos de las piernas", "los dedos de las manos"],
         "Las costillas forman una jaula en el pecho.", "Las costillas rodean el pecho y protegen el corazón y los pulmones.")
    b.ord(4, "Ordena el camino de la comida.", ["boca 👄", "esófago", "estómago", "intestinos"],
          "Empieza donde masticas.", "Boca → esófago → estómago → intestinos.")
    b.om(5, "Después de correr 🏃, el corazón late más rápido. ¿Por qué?", "para llevar más sangre a los músculos",
         ["porque el estómago tiene hambre", "porque los huesos crecen", "porque los pulmones se detienen"],
         "Los músculos trabajan mucho al correr.", "Al correr los músculos necesitan más sangre, y el corazón late más rápido para llevarla.")
    b.om(5, "Si no tuviéramos esqueleto, ¿cómo sería el cuerpo?", "blando, sin forma y sin poder estar de pie",
         ["igual que ahora", "más alto y fuerte", "más rápido para correr"],
         "¿Qué sostiene tu cuerpo?", "Sin esqueleto el cuerpo no tendría sostén ni forma, y no podríamos pararnos.")
    b.cat(5, "¿Qué órgano está trabajando?", ["Corazón", "Pulmones", "Estómago"],
          [("late más rápido al correr", 0), ("bombea sangre", 0), ("se inflan al inspirar", 1), ("sacan el aire al soplar", 1),
           ("recibe el almuerzo", 2), ("mezcla la comida con jugos", 2)],
          "Piensa en sangre, aire o comida.", "Latir y bombear: corazón; inflarse y soplar: pulmones; recibir y mezclar comida: estómago.")
    b.nu(5, "Benjamín respira 20 veces en un minuto. Después de saltar, respira 35 veces en un minuto. ¿Cuántas veces más respira?", 15,
         "Resta lo que respira en reposo.", "35 − 20 = 15: respira 15 veces más, porque sus músculos necesitan más aire.", unidad="veces")
    return b.items


def cn02_oa9():
    b = Autor("cie", 2, 9)
    b.om(1, "¿Qué le pasa al hielo 🧊 al sol ☀️?", "se derrite", ["se agranda", "se vuelve piedra", "se pone más duro"],
         "Piensa en un helado en verano.", "Con el calor del sol, el hielo se derrite y se vuelve agua líquida.")
    b.om(1, "Dejas agua 💧 en el congelador. ¿Qué obtienes?", "🧊 hielo", ["🔥 fuego", "🪨 piedra", "🧂 sal"],
         "En el congelador hace mucho frío.", "Con mucho frío, el agua se congela y se vuelve hielo.")
    b.co(1, "El agua derramada ___ por la mesa. 💧", "escurre", ["rebota", "se para", "crece"],
         "El agua no se queda quieta en un solo lugar.", "El agua es líquida: escurre por la mesa.")
    b.cat(2, "¿Se disuelve en agua o no?", ["Se disuelve", "No se disuelve"],
          [("🧂 sal", 0), ("azúcar", 0), ("jugo en polvo", 0), ("🪨 piedra", 1), ("arena", 1), ("clavo", 1)],
          "Si revuelves y ya no lo ves, se disolvió.", "Sal, azúcar y jugo en polvo se disuelven; piedra, arena y clavo no.")
    b.om(2, "Echas agua en un molde de estrella ⭐. ¿Qué forma toma el agua?", "forma de estrella", ["forma de gota", "forma de cubo", "forma de pelota"],
         "El agua se acomoda al recipiente.", "El agua toma la forma del recipiente: en el molde, forma de estrella.")
    b.em(2, "Une cada estado del agua con un ejemplo.", [["sólido", "🧊 hielo"], ["líquido", "💧 agua de la llave"], ["gaseoso", "♨️ vapor de la tetera"]],
         "El vapor sube de la tetera caliente.", "Hielo: sólido; agua de la llave: líquido; vapor: gaseoso.")
    b.ord(3, "Un cubo de hielo se calienta cada vez más. Ordena lo que pasa.", ["🧊 hielo (sólido)", "💧 agua (líquido)", "♨️ vapor (gas)"],
          "Primero se derrite y después hierve.", "Hielo → agua líquida → vapor: con calor, el agua cambia de estado.")
    b.co(3, "Cuando el agua hierve, se transforma en ___.", "vapor", ["hielo", "sal", "nieve"],
         "Mira lo que sale de una olla hirviendo.", "Al hervir, el agua líquida se transforma en vapor.")
    b.om(3, "Pasas agua de una botella a un plato. ¿Qué pasa con su forma?", "toma la forma del plato",
         ["mantiene la forma de la botella", "se vuelve sólida", "queda en forma de gota"],
         "Los líquidos no tienen forma propia.", "El agua es líquida: toma la forma del recipiente donde la pones.")
    b.cat(4, "¿Qué característica del agua muestra cada caso?", ["Escurre", "Toma la forma del recipiente", "Cambia de estado"],
          [("la lluvia baja por la calle", 0), ("el agua corre por un tobogán", 0), ("el jugo llena un vaso con forma de corazón", 1),
           ("el agua de la piscina tiene su forma", 1), ("el charco se seca al sol", 2), ("la nieve se derrite en primavera", 2)],
          "Secarse y derretirse son cambios de estado.", "Bajar y correr: escurre; llenar el vaso o la piscina: toma su forma; secarse y derretirse: cambia de estado.")
    b.om(4, "Martina revuelve sal 🧂 en agua y ya no la ve. ¿Qué pasó?", "la sal se disolvió en el agua",
         ["la sal desapareció para siempre", "la sal se volvió hielo", "la sal se fue al aire"],
         "Prueba el agua: ¿está salada?", "La sal se disolvió: sigue en el agua aunque no la veas, por eso el agua queda salada.")
    b.co(4, "Un helado 🍦 al sol se ___ porque sube su temperatura.", "derrite", ["congela", "endurece", "enfría"],
         "El calor cambia el estado del hielo.", "Con el calor, el helado se derrite: pasa de sólido a líquido.")
    b.om(5, "{personaje} deja ropa mojada al sol ☀️ y se seca. ¿Adónde fue el agua?", "se evaporó y pasó al aire",
         ["se convirtió en hielo", "se quedó escondida en la ropa", "desapareció para siempre"],
         "El calor del sol cambia el estado del agua.", "El calor evaporó el agua: pasó al aire como vapor.")
    b.om(5, "En la cordillera hay nieve en invierno, y en verano gran parte se derrite. ¿Por qué?", "el frío congela el agua y el calor la derrite",
         ["la nieve se disuelve en el aire", "en verano llueve más fuerte", "la nieve escurre hacia arriba"],
         "Piensa en la temperatura de cada estación.", "Con frío el agua se congela en nieve; con el calor del verano se derrite y baja por los ríos.")
    b.co(5, "Mezclas arena con agua y esperas. La arena queda ___.", "en el fondo del vaso", ["disuelta en el agua", "flotando en el aire", "pegada en el borde de arriba"],
         "La arena no se disuelve en agua.", "La arena no se disuelve: se hunde y queda en el fondo del vaso.")
    b.nu(5, "El agua hierve a 100 grados. Si el agua de la olla está a 60 grados, ¿cuántos grados le faltan para hervir?", 40,
         "Resta la temperatura que tiene.", "100 − 60 = 40: le faltan 40 grados para hervir y convertirse en vapor.", unidad="grados")
    return b.items


def cn03_oa1():
    b = Autor("cie", 3, 1)
    b.om(1, "¿Qué parte de la planta absorbe el agua del suelo?", "la raíz", ["la hoja", "la flor", "el fruto"],
         "Está bajo la tierra.", "La raíz absorbe el agua y las sales minerales del suelo.")
    b.cat(1, "¿Qué necesita una planta para vivir?", ["Lo necesita", "No lo necesita"],
          [("agua", 0), ("luz", 0), ("aire", 0), ("música", 1), ("oscuridad total", 1), ("plástico", 1)],
          "Piensa en lo que le das a una planta de tu casa.", "Las plantas necesitan agua, luz y aire; no necesitan música, oscuridad ni plástico.")
    b.co(1, "Las hojas necesitan la ___ del sol para fabricar su alimento.", "luz", ["sombra", "lluvia", "nieve"],
         "Por eso las plantas buscan el sol.", "Las hojas usan la luz del sol para fabricar su alimento.")
    b.em(2, "Une cada parte de la planta con su función.",
         [["raíz", "absorbe agua y sales minerales"], ["tallo", "transporta el agua y sostiene"], ["hojas", "fabrican alimento con la luz"]],
         "Piensa de abajo hacia arriba.", "La raíz absorbe, el tallo transporta y sostiene, y las hojas fabrican el alimento.")
    b.om(2, "¿Qué parte sostiene la planta y lleva el agua hacia las hojas?", "el tallo", ["la raíz", "la flor", "la semilla"],
         "Une la raíz con las hojas.", "El tallo sostiene la planta y transporta el agua desde la raíz hasta las hojas.")
    b.co(2, "Además de absorber agua, la raíz ___ la planta al suelo.", "fija", ["suelta", "separa", "levanta"],
         "Por eso el viento no se lleva a los árboles.", "La raíz fija la planta al suelo y la mantiene firme.")
    b.ord(3, "Ordena el camino del agua en una planta.", ["suelo", "raíz", "tallo", "hojas"],
          "El agua entra por abajo.", "Suelo → raíz → tallo → hojas.")
    b.om(3, "Una planta crece en un rincón oscuro y sus hojas están amarillas y débiles. ¿Qué le falta?", "luz",
         ["más tierra", "más oscuridad", "una maceta más grande"],
         "Fíjate en dónde está la planta.", "Sin luz, las hojas no pueden fabricar alimento y se ponen amarillas.")
    b.nu(3, "Josefa riega su planta con 2 vasos de agua cada día. ¿Cuántos vasos usa en una semana?", 14,
         "Una semana tiene 7 días.", "2 vasos × 7 días = 14 vasos de agua.", unidad="vasos")
    b.cat(4, "¿Qué parte de la planta comemos?", ["Raíz", "Tallo", "Hoja"],
          [("zanahoria", 0), ("betarraga", 0), ("espárrago", 1), ("caña de azúcar", 1), ("lechuga", 2), ("acelga", 2)],
          "La raíz crece bajo tierra; el tallo sostiene; la hoja es verde y plana.", "Zanahoria y betarraga son raíces; espárrago y caña, tallos; lechuga y acelga, hojas.")
    b.om(4, "Vicente pone dos plantas iguales al sol, pero riega solo una. ¿Qué quiere averiguar?", "si la planta necesita agua",
         ["si la planta necesita luz", "si la planta necesita aire", "si la planta necesita tierra"],
         "¿Qué es lo único distinto entre las dos plantas?", "Lo único que cambia es el riego: quiere saber si la planta necesita agua.")
    b.om(4, "Si las hojas de una planta quedan cubiertas de barro y no les llega luz, ¿qué pasará?", "no podrá fabricar su alimento",
         ["absorberá más agua", "crecerá más rápido", "sus raíces se volverán hojas"],
         "Recuerda para qué usan la luz las hojas.", "Las hojas necesitan luz para fabricar alimento; cubiertas, la planta se debilita.")
    b.om(5, "Si cortas todas las raíces de una planta, ¿qué le pasará?", "no podrá absorber agua y se marchitará",
         ["crecerá más rápido", "sus hojas se pondrán más verdes", "tomará el agua por las flores"],
         "Piensa en qué parte toma el agua del suelo.", "Sin raíces no absorbe agua, el tallo no tiene qué transportar y la planta se marchita.")
    b.om(5, "{personaje} pone un clavel blanco en agua con colorante azul. Al día siguiente los pétalos se ven azulados. ¿Qué demuestra?",
         "que el tallo transporta el agua hacia arriba",
         ["que las flores toman color del aire", "que la raíz fabrica colorante", "que las hojas absorben agua de lluvia"],
         "¿Cómo llegó el colorante a los pétalos?", "El agua con colorante subió por el tallo hasta la flor: el tallo transporta el agua.")
    b.co(5, "El tamarugo, árbol del norte de Chile, tiene raíces muy ___ para llegar al agua subterránea.", "profundas",
         ["cortas", "superficiales", "débiles"],
         "En el desierto, el agua está muy abajo.", "Sus raíces son muy profundas: así alcanzan el agua que está bajo el suelo del desierto.")
    b.em(5, "Une cada problema con su causa.",
         [["hojas amarillas en un lugar oscuro", "falta de luz"], ["planta marchita y tierra seca", "falta de agua"],
          ["planta pequeña en tierra muy pobre", "faltan sales minerales del suelo"]],
         "Busca qué necesidad no se cumple en cada caso.", "Lugar oscuro: falta luz; tierra seca: falta agua; tierra pobre: faltan sales minerales.")
    return b.items


def cn03_oa9():
    b = Autor("cie", 3, 9)
    b.om(1, "¿Cuál es una fuente natural de luz?", "el Sol", ["una ampolleta", "una linterna", "una vela"],
         "No la fabricaron las personas.", "El Sol es una fuente natural de luz; la ampolleta, la linterna y la vela son artificiales.")
    b.co(1, "La luz viaja en línea ___.", "recta", ["curva", "circular", "en zigzag"],
         "Piensa en un rayo de sol que entra por la ventana.", "La luz viaja en línea recta.")
    b.om(1, "¿En qué objeto puedes ver tu imagen reflejada?", "un espejo", ["una hoja de cuaderno", "un trozo de madera", "una toalla"],
         "Es liso y muy brillante.", "El espejo refleja la luz de forma ordenada y por eso ves tu imagen.")
    b.om(2, "¿Cuándo se puede ver un arcoíris?", "cuando la luz del sol atraviesa gotas de agua",
         ["cuando el cielo está nublado y sin sol", "en una noche oscura", "cuando sopla mucho viento"],
         "Se necesitan sol y gotitas de agua.", "El arcoíris aparece cuando la luz del sol atraviesa gotas de agua y se separa en colores.")
    b.co(2, "Las sombras se forman porque la luz no puede ___ los objetos opacos.", "atravesar", ["calentar", "tocar", "pintar"],
         "Un objeto opaco no deja pasar la luz.", "La luz no atraviesa los objetos opacos y detrás de ellos se forma una sombra.")
    b.cat(2, "¿Produce su propia luz o solo la refleja?", ["Produce luz", "Solo refleja luz"],
          [("el Sol", 0), ("una linterna encendida", 0), ("una fogata", 0), ("la Luna", 1), ("un espejo", 1), ("una cuchara", 1)],
          "¡Ojo con la Luna!", "El Sol, la linterna y la fogata producen luz; la Luna, el espejo y la cuchara solo reflejan la luz que reciben.")
    b.ord(3, "Ordena estos colores como aparecen en el arcoíris, desde arriba.", ["rojo", "naranjo", "amarillo", "verde", "azul", "violeta"],
          "Arriba está el rojo y abajo, el violeta.", "Rojo, naranjo, amarillo, verde, azul y violeta (entre azul y violeta está el añil).")
    b.em(3, "Une cada fenómeno con la característica de la luz que muestra.",
         [["arcoíris", "la luz se separa en colores"], ["tu imagen en un espejo", "la luz se refleja"], ["sombra con la forma del objeto", "la luz viaja en línea recta"]],
         "Piensa en qué le pasa a la luz en cada caso.", "Arcoíris: se separa en colores; espejo: se refleja; sombra: viaja en línea recta.")
    b.nu(3, "¿Cuántos colores se distinguen en el arcoíris?", 7,
         "Rojo, naranjo, amarillo… sigue contando.", "Se distinguen 7 colores: rojo, naranjo, amarillo, verde, azul, añil y violeta.", unidad="colores")
    b.om(4, "Miras una vela por un tubo recto y la ves. Si doblas el tubo, ya no la ves. ¿Qué demuestra?", "que la luz viaja en línea recta",
         ["que la luz se separa en colores", "que la vela se apagó", "que el tubo produce luz"],
         "La luz no puede doblar la curva del tubo.", "La luz viaja en línea recta: no puede seguir la curva del tubo doblado.")
    b.cat(4, "¿Forma una imagen nítida al reflejar la luz?", ["Sí, como un espejo", "No forma imagen"],
          [("espejo", 0), ("cuchara metálica pulida", 0), ("agua quieta de un lago", 0), ("ladrillo", 1), ("cartón", 1), ("toalla", 1)],
          "Las superficies lisas y brillantes reflejan mejor.", "Espejo, cuchara pulida y agua quieta son lisos y forman imagen; ladrillo, cartón y toalla son ásperos.")
    b.co(4, "El ___ es un objeto de vidrio que separa la luz blanca en colores.", "prisma", ["espejo", "imán", "termómetro"],
         "Tiene forma triangular.", "El prisma separa la luz blanca en los colores del arcoíris.")
    b.om(5, "{personaje} quiere iluminar un rincón que está detrás de una roca. Tiene una linterna y un espejo. ¿Qué debe hacer?",
         "apuntar la linterna al espejo para que la luz rebote hacia el rincón",
         ["doblar el rayo de luz con la mano", "apuntar la linterna directo a la roca", "tapar el espejo con la mano"],
         "La luz no dobla sola, pero puede rebotar.", "La luz viaja en línea recta, pero se refleja en el espejo y así puede llegar al rincón.")
    b.om(5, "Para ver un arcoíris después de la lluvia, ¿dónde debe estar el Sol?", "detrás de ti, con gotas de agua frente a ti",
         ["frente a ti, tapado por nubes", "bajo el horizonte, de noche", "justo encima de las gotas, sin luz"],
         "La luz debe llegar a las gotas y volver hacia tus ojos.", "Con el Sol a tu espalda, su luz entra en las gotas de enfrente, se separa en colores y llega a tus ojos.")
    b.cat(5, "¿Qué característica de la luz explica cada caso?", ["Viaja en línea recta", "Se refleja", "Se separa en colores"],
          [("tu sombra en el patio", 0), ("rayos de sol rectos entre los árboles", 0), ("ver tu cara en una ventana", 1),
           ("el brillo de la Luna", 1), ("arcoíris después de la lluvia", 2), ("colores al pasar luz por un prisma", 2)],
          "La Luna no produce luz propia.", "Sombra y rayos rectos: línea recta; ventana y Luna: reflexión; arcoíris y prisma: separación en colores.")
    b.ord(5, "Ordena el camino de la luz para que puedas ver la Luna.",
          ["el Sol emite luz", "la luz llega a la Luna", "la Luna refleja la luz", "la luz llega a tus ojos"],
          "La Luna no tiene luz propia.", "El Sol emite luz, llega a la Luna, la Luna la refleja y llega a tus ojos.")
    return b.items


def cn03_oa11():
    b = Autor("cie", 3, 11)
    b.om(1, "¿Cuál es la estrella del Sistema Solar?", "el Sol", ["la Luna", "la Tierra", "Marte"],
         "Nos da luz y calor.", "El Sol es la estrella del Sistema Solar.")
    b.nu(1, "¿Cuántos planetas tiene el Sistema Solar?", 8,
         "Mercurio, Venus, Tierra… sigue contando.", "Hay 8 planetas: Mercurio, Venus, Tierra, Marte, Júpiter, Saturno, Urano y Neptuno.", unidad="planetas")
    b.co(1, "La Luna gira alrededor de la ___.", "Tierra", ["Marte", "Venus", "estrella Polar"],
         "Es el satélite natural de nuestro planeta.", "La Luna es el satélite de la Tierra y gira a su alrededor.")
    b.om(2, "¿Cuál es el planeta más grande del Sistema Solar?", "Júpiter", ["la Tierra", "Mercurio", "Marte"],
         "Es un gigante gaseoso.", "Júpiter es el planeta más grande del Sistema Solar.")
    b.co(2, "El planeta conocido como «el planeta rojo» es ___.", "Marte", ["Venus", "Saturno", "Neptuno"],
         "Está justo después de la Tierra.", "Marte se ve rojizo por el polvo de su superficie.")
    b.om(2, "¿Qué planeta está más cerca del Sol?", "Mercurio", ["Venus", "la Tierra", "Neptuno"],
         "Es el primero de la lista.", "Mercurio es el planeta más cercano al Sol.")
    b.ord(3, "Ordena los planetas desde el más cercano al Sol.", ["Mercurio", "Venus", "Tierra", "Marte", "Júpiter", "Saturno"],
          "La Tierra es el tercero.", "Mercurio → Venus → Tierra → Marte → Júpiter → Saturno (luego siguen Urano y Neptuno).")
    b.em(3, "Une cada cuerpo con su descripción.",
         [["Sol", "estrella que da luz y calor"], ["Luna", "satélite natural de la Tierra"], ["cometa", "hielo y polvo con una cola brillante"],
          ["asteroide", "roca pequeña de forma irregular"], ["planeta", "cuerpo grande y redondo que gira alrededor del Sol"]],
         "El cometa tiene cola.", "Sol: estrella; Luna: satélite; cometa: hielo y polvo con cola; asteroide: roca irregular; planeta: cuerpo redondo que orbita el Sol.")
    b.cat(3, "¿Planeta rocoso o planeta gigante?", ["Rocoso (cerca del Sol)", "Gigante (lejos del Sol)"],
          [("Mercurio", 0), ("Venus", 0), ("Tierra", 0), ("Marte", 0), ("Júpiter", 1), ("Saturno", 1), ("Urano", 1), ("Neptuno", 1)],
          "Los cuatro primeros son pequeños y de roca.", "Mercurio, Venus, Tierra y Marte son rocosos; Júpiter, Saturno, Urano y Neptuno son gigantes.")
    b.om(4, "¿Por qué el Sol se ve mucho más grande que las otras estrellas del cielo?", "porque está mucho más cerca de la Tierra",
         ["porque es la estrella más grande del universo", "porque es un planeta", "porque solo brilla de día"],
         "Un objeto lejano se ve pequeño.", "El Sol es una estrella mediana, pero está mucho más cerca que las demás; por eso se ve tan grande.")
    b.co(4, "Entre Marte y Júpiter hay un cinturón de ___.", "asteroides", ["cometas", "lunas", "estrellas"],
         "Son rocas de distintos tamaños.", "Entre Marte y Júpiter está el cinturón de asteroides.")
    b.nu(4, "Si cuentas los planetas desde el Sol, ¿en qué lugar está Saturno?", 6,
         "Mercurio es el 1, Venus el 2…", "Mercurio 1, Venus 2, Tierra 3, Marte 4, Júpiter 5 y Saturno 6.")
    b.om(4, "¿Por qué a un cometa le aparece una cola al acercarse al Sol?", "el calor del Sol evapora su hielo y libera gas y polvo",
         ["se incendia como un fósforo", "choca con la Luna", "le crecen rocas nuevas"],
         "Los cometas están hechos de hielo y polvo.", "Cerca del Sol, el hielo del cometa se evapora y suelta gas y polvo que forman la cola.")
    b.om(5, "En el desierto de Atacama hay muchos observatorios astronómicos. ¿Por qué es un buen lugar?", "tiene cielos despejados, secos y oscuros",
         ["está más cerca del Sol", "ahí nunca es de día", "las estrellas están más bajas"],
         "Piensa en las nubes y en la luz de las ciudades.", "En Atacama casi no hay nubes, el aire es seco y hay poca luz artificial: el cielo se ve muy bien.")
    b.em(5, "Une cada planeta con su característica.",
         [["Venus", "el más caliente, con nubes gruesas"], ["Marte", "rocoso y de color rojizo"], ["Júpiter", "el más grande, con una gran mancha roja"],
          ["Saturno", "grandes anillos muy visibles"], ["Neptuno", "el más lejano del Sol"]],
         "Saturno es famoso por sus anillos.", "Venus: el más caliente; Marte: rojizo; Júpiter: el más grande; Saturno: anillos; Neptuno: el más lejano.")
    b.ord(5, "Ordena del más pequeño al más grande.", ["la Luna", "la Tierra", "Júpiter", "el Sol"],
          "La Luna cabe muchas veces dentro de la Tierra.", "Luna → Tierra → Júpiter → Sol: el Sol es mucho más grande que todos los planetas.")
    return b.items


GENERADORES = {
    "1_basico.ciencias.OA1": cn01_oa1,
    "1_basico.ciencias.OA4": cn01_oa4,
    "1_basico.ciencias.OA12": cn01_oa12,
    "2_basico.ciencias.OA1": cn02_oa1,
    "2_basico.ciencias.OA7": cn02_oa7,
    "2_basico.ciencias.OA9": cn02_oa9,
    "3_basico.ciencias.OA1": cn03_oa1,
    "3_basico.ciencias.OA9": cn03_oa9,
    "3_basico.ciencias.OA11": cn03_oa11,
}
