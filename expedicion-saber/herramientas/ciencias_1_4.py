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
    b.om(5, "{personaje} no riega su planta 🪴 por muchas semanas. ¿Qué le pasará?", "Se secará, porque le falta agua.",
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
    b.om(1, "¿Qué ropa usa {personaje} en invierno? ❄️", "🧥 parka", ["🩱 traje de baño", "🩴 chalas", "🕶️ lentes de sol"],
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
    b.nu(3, "{personaje} ve estos animales: 🐧 🐶 🦅 🐟 🦜 🐍. ¿Cuántos son aves?", 3,
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
    b.nu(4, "El corazón de {personaje} late 80 veces en 1 minuto. ¿Cuántas veces late en 2 minutos?", 160,
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
    b.nu(5, "{personaje} respira 20 veces en un minuto. Después de saltar, respira 35 veces en un minuto. ¿Cuántas veces más respira?", 15,
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
    b.om(4, "{personaje} revuelve sal 🧂 en agua y ya no la ve. ¿Qué pasó?", "la sal se disolvió en el agua",
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
    b.om(4, "{personaje} pone dos plantas iguales al sol, pero riega solo una. ¿Qué quiere averiguar?", "si la planta necesita agua",
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
    b.co(4, "{personaje} usa un ___, un objeto de vidrio que separa la luz blanca en colores.", "prisma", ["espejo", "imán", "termómetro"],
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
    b.nu(4, "{personaje} cuenta los planetas desde el Sol. ¿En qué lugar está Saturno?", 6,
         "Mercurio es el 1, Venus el 2…", "Mercurio 1, Venus 2, Tierra 3, Marte 4, Júpiter 5 y Saturno 6.")
    b.om(4, "¿Por qué a un cometa le aparece una cola al acercarse al Sol?", "el calor del Sol evapora su hielo y libera gas y polvo",
         ["se incendia como un fósforo", "choca con la Luna", "le crecen rocas nuevas"],
         "Los cometas están hechos de hielo y polvo.", "Cerca del Sol, el hielo del cometa se evapora y suelta gas y polvo que forman la cola.")
    b.om(5, "{personaje} visita un observatorio en el desierto de Atacama. ¿Por qué ese lugar es bueno para observar el cielo?", "tiene cielos despejados, secos y oscuros",
         ["está más cerca del Sol", "ahí nunca es de día", "las estrellas están más bajas"],
         "Piensa en las nubes y en la luz de las ciudades.", "En Atacama casi no hay nubes, el aire es seco y hay poca luz artificial: el cielo se ve muy bien.")
    b.em(5, "Une cada planeta con su característica.",
         [["Venus", "el más caliente, con nubes gruesas"], ["Marte", "rocoso y de color rojizo"], ["Júpiter", "el más grande, con una gran mancha roja"],
          ["Saturno", "grandes anillos muy visibles"], ["Neptuno", "el más lejano del Sol"]],
         "Saturno es famoso por sus anillos.", "Venus: el más caliente; Marte: rojizo; Júpiter: el más grande; Saturno: anillos; Neptuno: el más lejano.")
    b.ord(5, "Ordena del más pequeño al más grande.", ["la Luna", "la Tierra", "Júpiter", "el Sol"],
          "La Luna cabe muchas veces dentro de la Tierra.", "Luna → Tierra → Júpiter → Sol: el Sol es mucho más grande que todos los planetas.")
    return b.items


def cn03_oa12():
    b = Autor("cie", 3, 12)
    b.om(1, "¿Qué movimiento de la Tierra produce el día y la noche?", "la rotación", ["la traslación", "el movimiento de la Luna", "el viento"],
         "Es el giro de la Tierra sobre sí misma.", "La rotación, el giro de la Tierra sobre su eje, produce el día y la noche.")
    b.co(1, "La Tierra da una vuelta completa alrededor del ___ en un año.", "Sol", ["planeta Marte", "cinturón de asteroides", "satélite lunar"],
         "Es la estrella del Sistema Solar.", "La Tierra se traslada alrededor del Sol y demora un año en dar la vuelta.")
    b.nu(1, "¿Cuántas horas demora la Tierra en dar una vuelta sobre sí misma?", 24,
         "Es lo que dura un día completo.", "Una rotación completa dura 24 horas: un día.", unidad="horas")
    b.om(2, "¿Cuánto demora la Tierra en dar una vuelta completa alrededor del Sol?", "un año", ["un día", "una semana", "un mes"],
         "Es el tiempo entre un cumpleaños y el siguiente.", "La traslación dura un año, unos 365 días.")
    b.em(2, "Une cada concepto con su significado.",
         [["rotación", "giro de la Tierra sobre sí misma"], ["traslación", "vuelta de la Tierra alrededor del Sol"], ["eje terrestre", "línea imaginaria de polo a polo"]],
         "«Trasladarse» es ir de un lugar a otro.", "Rotación: giro sobre sí misma; traslación: vuelta al Sol; eje: línea imaginaria entre los polos.")
    b.om(2, "¿Por dónde sale el Sol cada mañana?", "por el este", ["por el oeste", "por el norte", "por el sur"],
         "En Santiago, el Sol aparece por la cordillera.", "Por la rotación de la Tierra, el Sol se ve salir por el este y ocultarse por el oeste.")
    b.cat(3, "¿Rotación o traslación?", ["Rotación", "Traslación"],
          [("dura 24 horas", 0), ("produce el día y la noche", 0), ("giro sobre el eje", 0),
           ("dura unos 365 días", 1), ("vuelta alrededor del Sol", 1), ("junto con la inclinación, produce las estaciones", 1)],
          "Uno es un giro corto; el otro, un viaje largo.", "Rotación: 24 horas, día y noche, giro sobre el eje; traslación: un año, vuelta al Sol y estaciones.")
    b.om(3, "Cuando en Chile es mediodía, en China, al otro lado del planeta, es…", "de noche",
         ["también mediodía", "de mañana temprano, siempre", "imposible saberlo"],
         "La mitad de la Tierra que no mira al Sol está a oscuras.", "Mientras un lado de la Tierra mira al Sol (día), el lado opuesto está de noche.")
    b.ord(3, "Ordena lo que ves durante un día en Chile.", ["el Sol sale por el este", "el Sol está alto al mediodía", "el Sol se oculta por el oeste", "es de noche"],
          "Todo empieza en la mañana.", "Por la rotación, vemos el Sol salir por el este, subir, ocultarse por el oeste y luego llega la noche.")
    b.om(4, "{personaje} ilumina una pelota con una linterna en una pieza oscura para hacer un modelo. ¿Qué representa la linterna?", "el Sol",
         ["la Luna", "la Tierra", "una estrella fugaz"],
         "La pelota es la Tierra. ¿Qué la ilumina?", "La linterna representa al Sol, que ilumina la Tierra (la pelota).")
    b.co(4, "Las estaciones se producen por la traslación y la ___ del eje de la Tierra.", "inclinación", ["rotación", "forma", "longitud"],
         "El eje de la Tierra no está derecho.", "Las estaciones ocurren porque la Tierra gira alrededor del Sol con su eje inclinado.")
    b.nu(4, "Un año normal tiene 365 días. Cada 4 años hay un año bisiesto con 1 día más. ¿Cuántos días tiene un año bisiesto?", 366,
         "Suma el día extra.", "365 + 1 = 366 días.", unidad="días")
    b.om(5, "¿Por qué en diciembre es verano en Chile e invierno en España?", "por la inclinación del eje, el hemisferio sur recibe los rayos del Sol más directos",
         ["porque Chile está más cerca del Sol que España", "porque en España es de noche en diciembre", "porque la Tierra deja de girar en diciembre"],
         "Chile y España están en hemisferios distintos.", "La inclinación del eje hace que en diciembre el hemisferio sur reciba la luz más directa: verano en Chile, invierno en España.")
    b.om(5, "Si la Tierra girara más lento sobre su eje, ¿qué pasaría?", "los días y las noches durarían más",
         ["el año duraría menos", "no habría estaciones", "el Sol saldría por el oeste"],
         "El giro sobre el eje produce el día y la noche.", "La rotación produce el día y la noche: si fuera más lenta, cada día y cada noche serían más largos.")
    b.nu(5, "{personaje} cumple 9 años hoy. ¿Cuántas vueltas alrededor del Sol ha dado la Tierra desde su nacimiento?", 9,
         "¿Cuánto dura una vuelta al Sol?", "Cada traslación dura un año: en 9 años la Tierra dio 9 vueltas al Sol.", unidad="vueltas")
    b.cat(5, "En diciembre, ¿qué estación hay en cada ciudad?", ["Verano", "Invierno"],
          [("Santiago", 0), ("Punta Arenas", 0), ("Buenos Aires", 0), ("Madrid", 1), ("Nueva York", 1), ("Tokio", 1)],
          "Piensa en qué hemisferio está cada ciudad.", "Santiago, Punta Arenas y Buenos Aires están en el hemisferio sur (verano); Madrid, Nueva York y Tokio, en el norte (invierno).")
    return b.items


def cn04_oa1():
    b = Autor("cie", 4, 1)
    b.om(1, "¿Cuál es un factor biótico (ser vivo) de un ecosistema?", "un huemul", ["una roca", "el agua de un río", "la luz del sol"],
         "Biótico significa que tiene vida.", "El huemul es un ser vivo: es un factor biótico.")
    b.cat(1, "¿Biótico o abiótico?", ["Biótico (vivo)", "Abiótico (no vivo)"],
          [("araucaria", 0), ("cóndor", 0), ("hongo", 0), ("agua", 1), ("aire", 1), ("roca", 1)],
          "Pregúntate: ¿nace, crece y se reproduce?", "Araucaria, cóndor y hongo son bióticos; agua, aire y roca son abióticos.")
    b.co(1, "La luz, el agua y la temperatura son factores ___ del ecosistema.", "abióticos", ["bióticos", "vivos", "animales"],
         "Ninguno de ellos es un ser vivo.", "Luz, agua y temperatura no tienen vida: son factores abióticos.")
    b.om(2, "¿Qué es un ecosistema?", "seres vivos y el ambiente de un lugar, interactuando",
         ["solo los animales de un bosque", "solo las rocas y el agua de un lugar", "una planta sola en un macetero"],
         "Incluye lo vivo y lo no vivo.", "Un ecosistema reúne los seres vivos y los factores no vivos de un lugar, que se relacionan entre sí.")
    b.em(2, "Une cada ser vivo con lo que usa del ambiente.",
         [["el pasto", "la luz del sol para fabricar alimento"], ["la trucha", "el oxígeno disuelto en el agua"], ["la lombriz", "el suelo húmedo para vivir"]],
         "Piensa dónde vive cada uno.", "El pasto usa la luz; la trucha, el oxígeno del agua; la lombriz, el suelo húmedo.")
    b.nu(2, "En un bosque de Chiloé, {personaje} anota: zorro, musgo, lluvia, roca, chucao, helecho. ¿Cuántos son factores bióticos?", 4,
         "Cuenta solo los seres vivos.", "Zorro, musgo, chucao y helecho son seres vivos: son 4.", unidad="factores")
    b.cat(3, "¿Biótico o abiótico?", ["Biótico", "Abiótico"],
          [("bacterias del suelo", 0), ("líquenes", 0), ("semillas", 0), ("temperatura", 1), ("viento", 1), ("sal del mar", 1)],
          "Algunos seres vivos son muy pequeños o parecen inmóviles.", "Bacterias, líquenes y semillas tienen vida; temperatura, viento y sal no.")
    b.om(3, "En el desierto de Atacama llueve muy poco. ¿Qué factor abiótico limita más la vida ahí?", "la falta de agua",
         ["el exceso de árboles", "la falta de rocas", "la cantidad de huemules"],
         "¿Qué necesitan todos los seres vivos y escasea en el desierto?", "En Atacama casi no llueve: la falta de agua limita a los seres vivos.")
    b.om(3, "{personaje} deja una planta dentro de una caja cerrada y oscura. ¿Qué factor abiótico le falta?", "la luz",
         ["los animales", "los hongos", "las bacterias"],
         "Los factores abióticos no tienen vida.", "En la caja oscura falta la luz, un factor abiótico que la planta necesita para fabricar alimento.")
    b.om(4, "Un incendio quema los árboles de un bosque. ¿Qué les pasa a los animales que vivían ahí?", "pierden su refugio y su alimento",
         ["no les afecta", "tienen más comida", "se vuelven abióticos"],
         "Los animales dependen de los árboles.", "Al perder los árboles, los animales se quedan sin refugio ni alimento.")
    b.co(4, "Si un río se contamina y le falta oxígeno, los ___ del río pueden morir.", "peces", ["guijarros", "granos de arena", "reflejos del sol"],
         "¿Quién respira dentro del agua?", "Los peces necesitan el oxígeno del agua: sin él, mueren.")
    b.em(4, "Une cada tipo de interacción con un ejemplo.",
         [["abiótico afecta a biótico", "la lluvia hace crecer el pasto"], ["biótico afecta a abiótico", "las raíces sujetan el suelo"],
          ["biótico afecta a biótico", "el zorro se come un ratón"]],
         "Fíjate si participan seres vivos, cosas no vivas o ambos.", "Lluvia → pasto: abiótico a biótico; raíces → suelo: biótico a abiótico; zorro → ratón: entre seres vivos.")
    b.ord(5, "Una sequía afecta a una laguna. Ordena lo que ocurre.",
          ["deja de llover por meses", "baja el nivel del agua", "las plantas acuáticas se secan", "los patos se van a otro lugar"],
          "Empieza por el cambio en un factor abiótico.", "Sin lluvia baja el agua, se secan las plantas y los patos, sin alimento ni refugio, se van.")
    b.om(5, "En una laguna del altiplano, los flamencos comen pequeños crustáceos. Si el agua se vuelve demasiado salada y los crustáceos mueren, ¿qué pasará?",
         "los flamencos tendrán menos alimento", ["los flamencos no se verán afectados", "los flamencos comerán sal", "aumentarán los flamencos"],
         "Un cambio abiótico puede afectar a varios seres vivos.", "La sal afectó a los crustáceos, y al faltar ese alimento, también se afectan los flamencos.")
    b.cat(5, "¿Qué tipo de interacción es?", ["Entre seres vivos", "Entre ser vivo y ambiente"],
          [("el picaflor bebe néctar de una flor", 0), ("el zorro caza un conejo", 0), ("el pudú come hojas de un arbusto", 0),
           ("una lagartija toma sol en una roca", 1), ("las raíces absorben agua del suelo", 1), ("el viento lleva semillas lejos", 1)],
          "Si participan dos seres vivos, es entre seres vivos.", "Picaflor-flor, zorro-conejo y pudú-arbusto son seres vivos; sol, roca, agua, suelo y viento son parte del ambiente.")
    b.co(5, "Las raíces sujetan el suelo. Si se tala el bosque de un cerro, la lluvia ___ el suelo con más facilidad.", "arrastra",
         ["fortalece", "congela", "fabrica"],
         "Sin raíces, nada retiene la tierra.", "Sin árboles que lo sujeten, la lluvia arrastra el suelo: lo biótico también afecta a lo abiótico.")
    return b.items


def cn04_oa3():
    b = Autor("cie", 4, 3)
    b.om(1, "¿Cuál es un productor en una cadena alimentaria?", "el pasto", ["el zorro", "el puma", "el conejo"],
         "Los productores fabrican su propio alimento.", "El pasto es un productor: fabrica su alimento con la luz del sol.")
    b.co(1, "Los ___ fabrican su propio alimento con la luz del sol.", "productores", ["consumidores", "descomponedores", "carnívoros"],
         "Son las plantas y las algas.", "Los productores, como plantas y algas, fabrican su alimento con la luz del sol.")
    b.cat(1, "¿Productor o consumidor?", ["Productor", "Consumidor"],
          [("pasto", 0), ("algas", 0), ("copihue", 0), ("puma", 1), ("cóndor", 1), ("chinita", 1)],
          "Los consumidores se alimentan de otros seres vivos.", "Pasto, algas y copihue son productores; puma, cóndor y chinita son consumidores.")
    b.em(2, "Une cada función con un ejemplo.", [["productor", "quillay"], ["consumidor", "conejo"], ["descomponedor", "hongo"]],
         "El hongo crece sobre troncos y hojas muertas.", "El quillay es productor, el conejo es consumidor y el hongo es descomponedor.")
    b.om(2, "¿Qué hacen los descomponedores, como los hongos y las bacterias?", "descomponen restos de seres vivos y devuelven nutrientes al suelo",
         ["fabrican alimento con la luz", "cazan a otros animales", "comen solo plantas vivas"],
         "Actúan sobre hojas caídas y animales muertos.", "Los descomponedores transforman los restos de seres vivos en nutrientes para el suelo.")
    b.ord(2, "Ordena esta cadena alimentaria, empezando por el productor.", ["pasto", "conejo", "zorro culpeo"],
          "Empieza por quien fabrica su alimento.", "Pasto → conejo → zorro culpeo: el conejo come pasto y el zorro come conejos.")
    b.ord(3, "Ordena esta cadena alimentaria del mar de Chile.", ["fitoplancton", "zooplancton", "anchoveta", "pingüino de Humboldt"],
          "El fitoplancton son algas microscópicas.", "Fitoplancton → zooplancton → anchoveta → pingüino de Humboldt.")
    b.om(3, "En la cadena pasto → conejo → zorro, ¿qué es el conejo?", "consumidor primario", ["productor", "descomponedor", "consumidor secundario"],
         "Se alimenta directamente del productor.", "El conejo come pasto, un productor: es consumidor primario.")
    b.nu(3, "{personaje} observa en la costa la cadena alga → caracol → pez → gaviota. ¿Cuántos consumidores hay?", 3,
         "Todos menos el productor.", "Caracol, pez y gaviota son consumidores: son 3. El alga es el productor.", unidad="consumidores")
    b.co(4, "En una cadena alimentaria, las flechas indican hacia dónde pasa la ___.", "energía del alimento", ["lluvia", "luz de la luna", "sombra"],
         "La flecha va desde el que es comido hacia el que come.", "Las flechas muestran cómo pasa la energía del alimento de un ser vivo a otro.")
    b.cat(4, "Clasifica cada ser vivo.", ["Productor", "Consumidor", "Descomponedor"],
          [("algarrobo", 0), ("luche (alga)", 0), ("guanaco", 1), ("cóndor", 1), ("hongo", 2), ("bacteria del suelo", 2)],
          "El cóndor come animales muertos, pero no los descompone.", "Algarrobo y luche: productores; guanaco y cóndor: consumidores; hongo y bacteria: descomponedores.")
    b.om(4, "Si desaparecen todos los productores de un ecosistema, ¿qué pasa?", "los consumidores se quedan sin alimento",
         ["los consumidores tienen más alimento", "solo se afectan los descomponedores", "no pasa nada"],
         "Toda cadena empieza en un productor.", "Sin productores no hay alimento para los herbívoros, y luego tampoco para los carnívoros.")
    b.om(5, "En la cadena maqui → zorzal → peuco, si desaparecen los peucos, ¿qué pasará primero?", "aumentarán los zorzales",
         ["aumentará el maqui", "disminuirán los zorzales", "desaparecerán los hongos"],
         "¿Quién se comía a los zorzales?", "Sin su depredador, los zorzales aumentan; después, al comer más, puede disminuir el maqui.")
    b.om(5, "¿Qué pasaría en un bosque sin descomponedores?", "se acumularían restos y el suelo perdería nutrientes",
         ["las plantas crecerían más", "los animales tendrían más alimento", "no pasaría nada"],
         "Piensa en las hojas caídas y los animales muertos.", "Sin descomponedores, los restos no se transforman y las plantas no reciben nutrientes del suelo.")
    b.em(5, "Une cada ser vivo del bosque con su función.",
         [["maqui", "productor"], ["zorzal", "consumidor primario"], ["peuco", "consumidor secundario"], ["hongo", "descomponedor"]],
         "El zorzal come frutos de maqui y el peuco caza zorzales.", "Maqui: productor; zorzal: consumidor primario; peuco: secundario; hongo: descomponedor.")
    b.ord(5, "{personaje} dibuja el camino de la energía. Ordénalo desde el comienzo.", ["el Sol", "el pasto", "el guanaco", "el puma"],
          "La energía de toda cadena viene de una estrella.", "Sol → pasto → guanaco → puma: el pasto usa la luz del Sol y la energía pasa a los consumidores.")
    return b.items


def cn04_oa5():
    b = Autor("cie", 4, 5)
    b.om(1, "¿Qué hueso protege el cerebro?", "el cráneo", ["las costillas", "el fémur", "la columna"],
         "Está en la cabeza.", "El cráneo es una caja de huesos que protege el cerebro.")
    b.co(1, "Las ___ protegen el corazón y los pulmones.", "costillas", ["falanges", "rótulas", "vértebras"],
         "Forman una especie de jaula en el pecho.", "Las costillas rodean el pecho y protegen el corazón y los pulmones.")
    b.om(1, "¿Cuáles son las tres funciones del esqueleto?", "protección, soporte y movimiento",
         ["digestión, respiración y visión", "fabricar sangre, oír y oler", "pensar, hablar y comer"],
         "Piensa en el cráneo, la columna y las piernas.", "El esqueleto protege órganos, sostiene el cuerpo y permite el movimiento.")
    b.em(2, "Une cada función del esqueleto con un ejemplo.",
         [["protección", "el cráneo cubre el cerebro"], ["soporte", "la columna nos mantiene erguidos"], ["movimiento", "los huesos de las piernas nos permiten caminar"]],
         "Soporte es sostener el cuerpo.", "Cráneo: protección; columna: soporte; huesos de las piernas: movimiento.")
    b.nu(2, "¿Cuántos huesos tiene el esqueleto de una persona adulta?", 206,
         "Son más de 200.", "El esqueleto adulto tiene 206 huesos.", unidad="huesos")
    b.co(2, "La columna vertebral está formada por huesos llamados ___.", "vértebras", ["costillas", "falanges", "rótulas"],
         "Su nombre se parece al de la columna.", "La columna vertebral está formada por vértebras.")
    b.cat(3, "¿Qué función cumple principalmente cada hueso?", ["Protección", "Soporte", "Movimiento"],
          [("cráneo", 0), ("costillas", 0), ("columna vertebral", 1), ("pelvis", 1), ("huesos de los dedos", 2), ("huesos del brazo", 2)],
          "El cráneo y las costillas cubren órganos delicados.", "Cráneo y costillas protegen; columna y pelvis sostienen; dedos y brazos permiten movimiento.")
    b.ord(3, "Ordena estos huesos desde la cabeza hasta los pies.", ["cráneo", "costillas", "pelvis", "fémur", "tibia"],
          "El fémur está en el muslo.", "Cráneo → costillas → pelvis → fémur → tibia.")
    b.om(3, "¿Cómo se llama la unión entre dos huesos que les permite moverse, como en la rodilla?", "articulación",
         ["músculo", "vértebra", "cráneo"],
         "También está en el codo y en los dedos.", "Las articulaciones unen huesos y permiten el movimiento, como la rodilla o el codo.")
    b.co(3, "Los huesos no se mueven solos: los ___ tiran de ellos.", "músculos", ["pulmones", "cartílagos", "dientes"],
         "Se contraen cuando haces fuerza.", "Los músculos están unidos a los huesos y, al contraerse, los mueven.")
    b.om(4, "¿Por qué {personaje} debe usar casco en bicicleta, si el cráneo ya protege el cerebro?",
         "porque un golpe fuerte puede quebrar el cráneo y dañar el cerebro",
         ["porque el cráneo es blando como una esponja", "porque el casco hace crecer los huesos", "porque el cerebro está fuera del cráneo"],
         "El cráneo es duro, pero tiene un límite.", "El cráneo protege, pero un golpe fuerte puede romperlo; el casco agrega protección.")
    b.em(4, "Une cada hueso con su ubicación.",
         [["fémur", "muslo"], ["húmero", "brazo"], ["tibia", "pierna, bajo la rodilla"], ["falanges", "dedos"], ["esternón", "centro del pecho"]],
         "El fémur es el hueso más largo del cuerpo.", "Fémur: muslo; húmero: brazo; tibia: bajo la rodilla; falanges: dedos; esternón: centro del pecho.")
    b.nu(4, "Las costillas van en pares: tenemos 12 pares. ¿Cuántas costillas tenemos en total?", 24,
         "Un par son dos.", "12 pares × 2 = 24 costillas.", unidad="costillas")
    b.om(5, "{personaje} se quebró el fémur. ¿Qué función del esqueleto se afecta más?", "el soporte y el movimiento de la pierna",
         ["la protección del cerebro", "la protección del corazón", "la digestión de la comida"],
         "¿Dónde está el fémur y qué hace?", "El fémur está en el muslo: sostiene el cuerpo y permite mover la pierna.")
    b.em(5, "Une cada órgano con el hueso que lo protege.",
         [["cerebro", "cráneo"], ["corazón y pulmones", "costillas"], ["médula espinal", "columna vertebral"]],
         "La médula espinal va por dentro de la espalda.", "El cráneo protege el cerebro, las costillas al corazón y los pulmones, y la columna a la médula espinal.")
    b.ord(5, "Ordena lo que pasa cuando pateas una pelota.",
          ["el cerebro da la orden", "los músculos de la pierna se contraen", "los músculos tiran de los huesos", "la pierna se mueve y patea"],
          "Todo empieza con una orden.", "El cerebro ordena, los músculos se contraen, tiran de los huesos y la pierna se mueve en la articulación.")
    return b.items


def cn04_oa16():
    b = Autor("cie", 4, 16)
    b.om(1, "¿Cuál es la capa más externa de la Tierra, donde vivimos?", "la corteza", ["el manto", "el núcleo", "el magma"],
         "Es la capa más delgada, como la cáscara de una fruta.", "La corteza es la capa externa y sólida donde vivimos.")
    b.ord(1, "Ordena las capas de la Tierra desde afuera hacia adentro.", ["corteza", "manto", "núcleo"],
          "El núcleo está en el centro.", "Corteza → manto → núcleo.")
    b.om(1, "¿Qué debes hacer durante un sismo en la sala de clases?", "agacharte, cubrirte y afirmarte",
         ["correr por la escalera", "pararte junto a la ventana", "subirte a una silla"],
         "Protege tu cabeza bajo la mesa.", "Durante un sismo, agáchate, cúbrete bajo la mesa y afírmate hasta que pase.")
    b.co(2, "La corteza terrestre está dividida en grandes trozos llamados ___.", "placas tectónicas", ["capas de hielo", "cráteres", "núcleos"],
         "Se mueven lentamente sobre el manto.", "La corteza está dividida en placas tectónicas que se mueven sobre el manto.")
    b.em(2, "Une cada fenómeno con su descripción.",
         [["sismo", "movimiento brusco del suelo"], ["tsunami", "olas gigantes que llegan a la costa"], ["erupción volcánica", "salida de lava, gases y cenizas"]],
         "Tsunami es una palabra japonesa relacionada con el mar.", "Sismo: el suelo se mueve; tsunami: olas gigantes; erupción: el volcán expulsa lava, gases y cenizas.")
    b.om(2, "Estás en la playa y ocurre un sismo muy fuerte. ¿Qué debes hacer?", "ir a pie a un lugar alto, lejos del mar",
         ["acercarte a mirar el mar", "quedarte en la arena", "meterte al agua"],
         "Después de un sismo fuerte en la costa puede venir un tsunami.", "Tras un sismo fuerte en la costa, hay que evacuar a una zona alta por si llega un tsunami.")
    b.cat(3, "¿Medida segura o peligrosa?", ["Segura", "Peligrosa"],
          [("tener una mochila de emergencia", 0), ("conocer las vías de evacuación", 0), ("ir a la zona de seguridad", 0),
           ("usar el ascensor durante un sismo", 1), ("bajar a la playa a ver el mar retirarse", 1), ("acercarse a un volcán en erupción", 1)],
          "Piensa qué te protege y qué te expone al peligro.", "Prepararse y evacuar es seguro; el ascensor, la playa tras un sismo y los volcanes activos son peligrosos.")
    b.om(3, "¿Por qué en Chile hay tantos sismos y volcanes?", "porque está donde se encuentran dos placas tectónicas",
         ["porque es un país muy largo", "porque tiene mucha nieve en la cordillera", "porque está cerca de la Antártica"],
         "Piensa en lo que pasa bajo el suelo frente a la costa.", "Frente a Chile, la placa de Nazca choca y se hunde bajo la placa Sudamericana.")
    b.co(3, "Bajo la superficie, la roca fundida se llama ___.", "magma", ["lava", "ceniza", "arena"],
         "Cuando sale por el volcán cambia de nombre.", "Bajo tierra es magma; cuando sale por el volcán se llama lava.")
    b.om(4, "{personaje} está en la costa y, después de un sismo, ve que el mar se retira de golpe. ¿Qué puede significar?", "que se acerca un tsunami",
         ["que es una marea baja normal", "que el peligro ya pasó", "que va a llover"],
         "Es una señal natural de alerta.", "Si el mar se retira de golpe tras un sismo, puede venir un tsunami: hay que evacuar a la altura.")
    b.ord(4, "Ordena cómo se forma un tsunami.",
          ["las placas se mueven bajo el mar", "ocurre un sismo submarino", "se desplaza una gran masa de agua", "olas gigantes llegan a la costa"],
          "Empieza bajo el fondo del mar.", "Las placas se mueven, ocurre un sismo bajo el mar, el agua se desplaza y llegan olas gigantes a la costa.")
    b.nu(4, "El terremoto de Valdivia fue en 1960 y el del 27F en el centro-sur de Chile, en 2010. ¿Cuántos años pasaron entre ambos?", 50,
         "Resta los años.", "2010 − 1960 = 50 años.", unidad="años")
    b.em(4, "Une cada capa de la Tierra con su característica.",
         [["corteza", "capa delgada y sólida donde vivimos"], ["manto", "roca muy caliente que se mueve lentamente"], ["núcleo", "centro de la Tierra, el más caliente"]],
         "El manto mueve a las placas.", "Corteza: delgada y sólida; manto: roca caliente que se mueve; núcleo: el centro, lo más caliente.")
    b.om(5, "¿Por qué la cordillera de los Andes tiene tantos volcanes?", "porque la placa de Nazca se hunde bajo la Sudamericana y se forma magma",
         ["porque es muy alta y fría", "porque llueve mucho en ella", "porque el núcleo está más cerca de la superficie ahí"],
         "Piensa en el choque de placas frente a Chile.", "Al hundirse la placa de Nazca bajo la Sudamericana se funde roca; ese magma sube y forma volcanes.")
    b.cat(5, "¿Cuándo se hace cada acción ante un sismo?", ["Antes", "Durante", "Después"],
          [("preparar una mochila de emergencia", 0), ("participar en simulacros", 0), ("agacharse, cubrirse y afirmarse", 1),
           ("alejarse de las ventanas", 1), ("revisar si hay heridos", 2), ("revisar si hay olor a gas", 2)],
          "Algunas cosas se preparan con tiempo.", "Antes: mochila y simulacros; durante: protegerse y alejarse de ventanas; después: revisar heridos y fugas de gas.")
    b.co(5, "En la costa, si un sismo no te deja mantenerte en pie, debes evacuar a la altura sin esperar la ___.", "alarma oficial",
         ["zona de seguridad", "ruta de evacuación", "mochila de emergencia"],
         "Cada minuto cuenta si viene un tsunami.", "Si el sismo no te deja estar de pie, evacúa de inmediato hacia la altura, sin esperar la alarma.")
    b.om(5, "{personaje} está en un edificio de Valparaíso durante un sismo fuerte. Cuando termina, ¿qué debe hacer?",
         "bajar por la escalera con calma hacia la zona de seguridad",
         ["usar el ascensor para salir más rápido", "quedarse junto a la ventana", "encender fósforos para ver mejor"],
         "Puede haber cortes de luz y fugas de gas.", "Se baja por la escalera con calma; el ascensor puede quedar detenido y el fuego es peligroso si hay gas.")
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
    "3_basico.ciencias.OA12": cn03_oa12,
    "4_basico.ciencias.OA1": cn04_oa1,
    "4_basico.ciencias.OA3": cn04_oa3,
    "4_basico.ciencias.OA5": cn04_oa5,
    "4_basico.ciencias.OA16": cn04_oa16,
}
