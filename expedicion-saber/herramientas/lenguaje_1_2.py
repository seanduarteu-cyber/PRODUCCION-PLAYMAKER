"""Lenguaje y Comunicación 1° y 2° básico: 15 desafíos por OA (3 por nivel, 1 a 5).

Los desafíos de comprensión llevan el cuento en el campo opcional "texto"."""
from comun import (opcion_multiple as om, completar as co, ordenar as orden, emparejar as em,
                   categoria as cat, numerica as nu)


class LB:
    def __init__(self, curso, oa):
        self.curso, self.oa, self.k, self.items = curso, oa, 0, []

    def id(self):
        self.k += 1
        return f"len{self.curso}-oa{self.oa}-{self.k:03d}"

    def __call__(self, item, texto=None):
        if texto:
            item = {**item, "texto": texto}
            # "texto" va justo después del enunciado para que el JSON se lea en orden
            item = {k: item[k] for k in ["id", "tipo", "dificultad", "texto", "enunciado"]} | {k: v for k, v in item.items() if k not in ("id", "tipo", "dificultad", "texto", "enunciado")}
        self.items.append(item)


def le01_oa3():
    b = LB(1, 3)
    b(nu(b.id(), 1, "¿Cuántas sílabas tiene la palabra «pato»?", 2, "Aplaude cada vez que dices un pedacito: pa… to.", "«Pato» se separa en pa-to: 2 sílabas."))
    b(om(b.id(), 1, "¿Con qué sonido empieza la palabra «mesa»?", "m", ["s", "p", "l"], "Di la palabra lento y fíjate en el primer sonido.", "«Mesa» empieza con el sonido /m/."))
    b(em(b.id(), 1, "Une las palabras que riman.", [["luna", "cuna"], ["gato", "pato"], ["sol", "col"]], "Las palabras que riman terminan igual.", "luna-cuna, gato-pato y sol-col terminan con los mismos sonidos."))
    b(nu(b.id(), 2, "¿Cuántas sílabas tiene la palabra «pelota»?", 3, "Aplaude: pe… lo… ta.", "«Pelota» se separa en pe-lo-ta: 3 sílabas."))
    b(om(b.id(), 2, "¿Qué palabra empieza con el mismo sonido que «casa»?", "copa", ["mesa", "luna", "pera"], "Escucha el primer sonido de «casa»: /k/.", "«Casa» y «copa» empiezan con /k/."))
    b(orden(b.id(), 2, "Ordena las sílabas para formar una palabra.", ["pe", "lo", "ta"], "Es algo redondo para jugar a la pelota.", "pe + lo + ta = pelota."))
    b(nu(b.id(), 3, "¿Cuántas sílabas tiene la palabra «mariposa»?", 4, "Aplaude: ma… ri… po… sa.", "«Mariposa» se separa en ma-ri-po-sa: 4 sílabas."))
    b(om(b.id(), 3, "¿Con qué sonido termina la palabra «pan»?", "n", ["p", "a", "m"], "Di la palabra y quédate en el último sonido.", "«Pan» termina con el sonido /n/."))
    b(cat(b.id(), 3, "Separa las palabras según su número de sílabas.", ["Una sílaba", "Dos sílabas"],
          [("sol", 0), ("pan", 0), ("mar", 0), ("casa", 1), ("gato", 1), ("luna", 1)], "Aplaude cada palabra.", "sol, pan y mar tienen 1 sílaba; ca-sa, ga-to y lu-na tienen 2."))
    b(orden(b.id(), 4, "Ordena las sílabas para formar una palabra.", ["bi", "ci", "cle", "ta"], "Tiene dos ruedas y pedales.", "bi + ci + cle + ta = bicicleta."))
    b(om(b.id(), 4, "Si en «casa» cambias el sonido /k/ por /m/, ¿qué palabra se forma?", "masa", ["taza", "cama", "pasa"], "Cambia solo el primer sonido.", "c-asa → m-asa: «masa»."))
    b(em(b.id(), 4, "Une cada sonido con la palabra que empieza con él.", [["s", "sapo"], ["m", "mano"], ["l", "lápiz"], ["t", "tomate"]],
         "Di cada palabra y escucha su primer sonido.", "sapo empieza con /s/, mano con /m/, lápiz con /l/ y tomate con /t/."))
    b(nu(b.id(), 5, "¿Cuántos sonidos (fonemas) tiene la palabra «sol»?", 3, "Estira la palabra: sss… ooo… lll.", "«Sol» tiene 3 sonidos: /s/ /o/ /l/."))
    b(om(b.id(), 5, "¿Qué palabra se forma si unes los sonidos /p/ /a/ /n/?", "pan", ["paz", "pon", "pie"], "Junta los sonidos de a uno.", "/p/ + /a/ + /n/ = pan."))
    b(cat(b.id(), 5, "¿Rima con «ratón»?", ["Rima con ratón", "No rima"], [("camión", 0), ("botón", 0), ("cajón", 0), ("ratita", 1), ("perro", 1), ("mesa", 1)],
          "Riman si terminan igual: …ón.", "camión, botón y cajón terminan en «-ón», como ratón."))
    return b.items


def le01_oa4():
    b = LB(1, 4)
    b(om(b.id(), 1, "¿Qué palabra corresponde al dibujo? 🐱", "gato", ["pato", "dato", "rato"], "Lee cada palabra despacio.", "🐱 es un gato: g-a-t-o."))
    b(om(b.id(), 1, "¿Qué palabra corresponde al dibujo? 🌙", "luna", ["lana", "lupa", "cuna"], "Fíjate en todas las letras.", "🌙 es la luna: l-u-n-a."))
    b(om(b.id(), 1, "¿Qué palabra corresponde al dibujo? ☀️", "sol", ["sal", "col", "sopa"], "Mira la letra del medio.", "☀️ es el sol: s-o-l."))
    b(co(b.id(), 2, "El ___ ladra.", "perro", ["sol", "mesa", "pan"], "¿Quién puede ladrar?", "El perro ladra."))
    b(co(b.id(), 2, "Mi mamá me ___.", "mima", ["mesa", "mapa", "mano"], "Busca una palabra que tenga sentido.", "«Mi mamá me mima»."))
    b(om(b.id(), 2, "Lee: «El oso come miel». ¿Quién come miel?", "el oso", ["la abeja", "el niño", "la mamá"], "Busca quién hace la acción.", "La oración dice que el oso come miel."))
    b(om(b.id(), 3, "¿Qué palabra está bien escrita? 🧀", "queso", ["keso", "ceso", "qeso"], "El sonido /k/ antes de e se escribe «qu».", "Se escribe «queso», con qu."))
    b(om(b.id(), 3, "¿Qué palabra está bien escrita? 🐴", "caballo", ["cabayo", "kaballo", "cavallo"], "Lleva «ll».", "Se escribe «caballo»."))
    b(orden(b.id(), 3, "Ordena las palabras para formar una oración.", ["El", "gato", "duerme", "mucho."], "La oración empieza con mayúscula y termina con punto.", "«El gato duerme mucho.»"))
    b(co(b.id(), 4, "La ___ vuela alto. 🐦", "paloma", ["piedra", "silla", "pala"], "¿Qué puede volar?", "La paloma vuela alto."))
    b(orden(b.id(), 4, "Ordena las palabras para formar una oración.", ["{personaje}", "busca", "{objetos}", "en {lugar}."], "Primero quién, después qué hace.", "«{personaje} busca {objetos} en {lugar}.»"))
    b(om(b.id(), 4, "Lee: «Tito tiene un trompo azul». ¿De qué color es el trompo?", "azul", ["rojo", "verde", "amarillo"], "Busca la palabra que dice el color.", "La oración dice «trompo azul»."))
    b(cat(b.id(), 5, "Lee cada palabra y sepárala.", ["Animales", "Objetos"], [("perro", 0), ("gallina", 0), ("ratón", 0), ("cuchara", 1), ("lápiz", 1), ("silla", 1)],
          "Lee con calma cada palabra.", "perro, gallina y ratón son animales; cuchara, lápiz y silla son objetos."))
    b(om(b.id(), 5, "¿Qué palabra tiene el grupo «tr»?", "tren", ["tela", "pera", "mano"], "Busca la t seguida de r.", "«Tren» empieza con tr."))
    b(co(b.id(), 5, "El ___ pasa por el túnel. 🚂", "tren", ["tierra", "trigo", "tres"], "¿Qué pasa por un túnel?", "El tren pasa por el túnel."))
    return b.items


def le01_oa8():
    b = LB(1, 8)
    A = "{personaje} tiene un perro llamado Pelusa. Pelusa es blanco y le gusta correr en {lugar}."
    b(om(b.id(), 1, "¿Cómo se llama el perro?", "Pelusa", ["Toby", "Nube", "Coco"], "Busca la palabra «llamado».", "El texto dice: «un perro llamado Pelusa»."), A)
    b(om(b.id(), 1, "¿De qué color es Pelusa?", "blanco", ["negro", "café", "gris"], "Busca el color en el texto.", "El texto dice: «Pelusa es blanco»."), A)
    b(om(b.id(), 1, "¿Qué le gusta hacer a Pelusa?", "correr", ["dormir", "nadar", "comer"], "Busca «le gusta».", "A Pelusa le gusta correr."), A)
    B = "En {lugar} llovió toda la noche. En la mañana salió el sol. Después apareció un arcoíris."
    b(orden(b.id(), 2, "Ordena lo que pasó.", ["Llovió toda la noche.", "Salió el sol.", "Apareció un arcoíris."], "Busca las palabras «noche», «mañana» y «después».", "Primero llovió, luego salió el sol y después apareció el arcoíris."), B)
    b(om(b.id(), 2, "¿Cuándo llovió?", "en la noche", ["en la tarde", "en la mañana", "nunca"], "Lee la primera oración.", "Llovió toda la noche."), B)
    b(om(b.id(), 2, "¿Qué apareció al final?", "un arcoíris", ["una estrella", "un perro", "un barco"], "Lee la última oración.", "Al final apareció un arcoíris."), B)
    C = "Ana perdió su gorro. Lo buscó en su pieza y en el patio. Al final, lo encontró debajo de la cama. Ana sonrió."
    b(om(b.id(), 3, "¿Dónde estaba el gorro?", "debajo de la cama", ["en el patio", "en la cocina", "en la mochila"], "Busca «lo encontró».", "Lo encontró debajo de la cama."), C)
    b(om(b.id(), 3, "¿Cómo se sintió Ana al final?", "feliz", ["triste", "enojada", "asustada"], "¿Qué hizo Ana al final? Sonreír…", "Ana sonrió: estaba feliz."), C)
    b(orden(b.id(), 3, "Ordena lo que pasó.", ["Ana perdió su gorro.", "Lo buscó en el patio.", "Lo encontró debajo de la cama."], "¿Qué pasó primero?", "Primero lo perdió, luego lo buscó y al final lo encontró."), C)
    D = "La tortuga y la liebre hicieron una carrera. La liebre corrió muy rápido y se durmió bajo un árbol. La tortuga caminó sin parar y llegó primero."
    b(om(b.id(), 4, "¿Quién ganó la carrera?", "la tortuga", ["la liebre", "el árbol", "nadie"], "¿Quién llegó primero?", "La tortuga llegó primero."), D)
    b(om(b.id(), 4, "¿Por qué perdió la liebre?", "porque se durmió", ["porque se cayó", "porque se perdió", "porque llovió"], "¿Qué hizo la liebre bajo el árbol?", "La liebre se durmió bajo el árbol."), D)
    b(em(b.id(), 4, "Une cada personaje con lo que lo describe.", [["la liebre", "corrió rápido y se durmió"], ["la tortuga", "caminó sin parar"], ["el árbol", "donde durmió la liebre"]],
         "Relee qué hizo cada uno.", "La liebre corrió y se durmió; la tortuga caminó sin parar."), D)
    E = "{personaje} quería terminar {la_construccion}, pero le faltaban {objetos}. Su amiga Lía le regaló cinco. Al final, {la_construccion} quedó lista."
    b(om(b.id(), 5, "¿Qué le faltaba a {personaje}?", "{objetos}", ["agua", "un mapa", "una llave"], "Busca «le faltaban».", "Le faltaban {objetos}."), E)
    b(om(b.id(), 5, "¿Quién ayudó a {personaje}?", "Lía", ["nadie", "su perro", "un robot"], "Busca quién regaló algo.", "Su amiga Lía le regaló cinco."), E)
    b(cat(b.id(), 5, "¿Pasó en el cuento?", ["Pasó en el cuento", "No pasó"],
          [("Lía le regaló cinco.", 0), ("Se terminó {la_construccion}.", 0), ("Llovió toda la noche.", 1), ("{personaje} se fue a dormir.", 1)],
          "Relee el cuento y busca cada idea.", "Lía regaló cinco y se terminó {la_construccion}; lo otro no aparece."), E)
    return b.items


def le02_oa5():
    b = LB(2, 5)
    F = "Martina vive cerca del mar. Todas las mañanas camina por la playa con su abuelo. Juntos recogen conchitas de colores y las guardan en un frasco."
    b(om(b.id(), 1, "¿Con quién camina Martina?", "con su abuelo", ["con su mamá", "con su perro", "sola"], "Busca «camina por la playa con…».", "Camina con su abuelo."), F)
    b(om(b.id(), 1, "¿Dónde vive Martina?", "cerca del mar", ["en el campo", "en la cordillera", "en el desierto"], "Lee la primera oración.", "Martina vive cerca del mar."), F)
    b(om(b.id(), 1, "¿Qué guardan en el frasco?", "conchitas", ["piedras", "arena", "peces"], "Busca «las guardan».", "Guardan conchitas de colores."), F)
    G = "{personaje} se despertó temprano. Tomó desayuno, preparó sus herramientas y salió hacia {lugar}. Allí trabajó toda la mañana."
    b(orden(b.id(), 2, "Ordena lo que hizo {personaje}.", ["Se despertó temprano.", "Tomó desayuno.", "Preparó sus herramientas.", "Salió hacia {lugar}."], "Sigue el orden del texto.", "Se despertó, desayunó, preparó sus herramientas y salió."), G)
    b(om(b.id(), 2, "¿Qué hizo primero {personaje}?", "se despertó", ["salió hacia {lugar}", "trabajó", "tomó desayuno"], "Mira la primera oración.", "Lo primero fue despertarse."), G)
    b(om(b.id(), 2, "¿Cuánto tiempo trabajó?", "toda la mañana", ["toda la noche", "un minuto", "toda la semana"], "Lee la última oración.", "Trabajó toda la mañana."), G)
    H = "Benja esperaba el cumpleaños de su abuela. Le hizo una tarjeta con dibujos. Cuando ella la abrió, se le llenaron los ojos de lágrimas y lo abrazó fuerte."
    b(om(b.id(), 3, "¿Cómo se sintió la abuela al recibir la tarjeta?", "emocionada", ["enojada", "aburrida", "asustada"], "Lágrimas y un abrazo fuerte: ¿qué sentía?", "Lloró de emoción y lo abrazó: estaba emocionada."), H)
    b(om(b.id(), 3, "¿Por qué Benja hizo una tarjeta?", "porque era el cumpleaños de su abuela", ["porque estaba aburrido", "porque se lo pidió la profesora", "porque estaba enfermo"], "Lee la primera oración.", "Esperaba el cumpleaños de su abuela."), H)
    b(om(b.id(), 3, "¿Qué hizo la abuela al final?", "lo abrazó", ["lo retó", "se fue", "se durmió"], "Lee la última parte.", "La abuela lo abrazó fuerte."), H)
    I = "En un bosque oscuro y frío vivía un búho muy sabio llamado Don Ulises. Cada noche, los animales iban a pedirle consejos. Un día llegó un zorro que se había perdido, y Don Ulises le mostró el camino con calma."
    b(om(b.id(), 4, "¿Cómo era el bosque?", "oscuro y frío", ["soleado y caluroso", "pequeño y seco", "lleno de flores"], "Busca las palabras que describen el bosque.", "El texto dice «un bosque oscuro y frío»."), I)
    b(em(b.id(), 4, "Une cada personaje con lo que dice el texto de él.", [["Don Ulises", "búho sabio"], ["el zorro", "se había perdido"], ["los animales", "pedían consejos"]],
         "Relee qué hace cada personaje.", "Don Ulises es un búho sabio, el zorro se perdió y los animales pedían consejos."), I)
    b(om(b.id(), 4, "¿Qué palabra describe mejor a Don Ulises?", "sabio", ["miedoso", "egoísta", "perezoso"], "¿Para qué lo buscaban los animales?", "Daba consejos y ayudó al zorro: es sabio."), I)
    J = "Sofía quería ganar la carrera del colegio. Entrenó todas las tardes durante un mes. El día de la carrera llegó segunda, pero mejoró su tiempo y se sintió orgullosa."
    b(om(b.id(), 5, "¿En qué lugar llegó Sofía?", "segunda", ["primera", "tercera", "última"], "Busca «llegó».", "Llegó segunda."), J)
    b(om(b.id(), 5, "¿Por qué Sofía se sintió orgullosa si no ganó?", "porque mejoró su tiempo", ["porque ganó un premio", "porque no corrió", "porque se cansó"], "Lee la última oración.", "Se sintió orgullosa porque mejoró su tiempo."), J)
    b(om(b.id(), 5, "¿Qué opinión se puede fundamentar con el texto?", "Sofía fue perseverante, porque entrenó durante un mes", ["Sofía no se esforzó nada", "Sofía es la más rápida de todos", "A Sofía no le gustan las carreras"],
         "Busca una opinión que tenga un ejemplo en el texto.", "Entrenar todas las tardes durante un mes muestra perseverancia."), J)
    return b.items


def le02_oa21():
    b = LB(2, 21)
    b(om(b.id(), 1, "¿Qué palabra está bien escrita?", "quince", ["kince", "cince", "qince"], "El sonido /k/ antes de i se escribe «qu».", "Se escribe «quince»."))
    b(co(b.id(), 1, "___ vive en Chile.", "Ana", ["ana", "aNa", "anA"], "Los nombres propios empiezan con mayúscula.", "«Ana» es un nombre: va con mayúscula."))
    b(om(b.id(), 1, "¿Dónde va el punto en una oración?", "al final", ["al inicio", "en medio de cada palabra", "no se usa"], "El punto indica que la oración terminó.", "El punto va al final de la oración."))
    b(co(b.id(), 2, "pa___te 🎁", "que", ["qe", "ke", "ce"], "El sonido /k/ antes de e se escribe «qu».", "Se escribe «paquete»."))
    b(co(b.id(), 2, "___tarra 🎸", "gui", ["gi", "ge", "güi"], "Para el sonido suave de /g/ antes de i se escribe «gu».", "Se escribe «guitarra»."))
    b(cat(b.id(), 2, "¿Se escribe con c o con qu?", ["Con c", "Con qu"], [("cine", 0), ("cereza", 0), ("cielo", 0), ("queso", 1), ("quince", 1), ("mosquito", 1)],
          "Si suena /s/ antes de e o i, va c; si suena /k/, va qu.", "cine, cereza y cielo van con c; queso, quince y mosquito con qu."))
    b(co(b.id(), 3, "pin___no 🐧", "güi", ["gui", "gi", "ui"], "Si la u se pronuncia, lleva diéresis (ü).", "Se escribe «pingüino»: la u suena."))
    b(co(b.id(), 3, "ci___ña", "güe", ["gue", "ge", "üe"], "Se dice ci-güe-ña: la u suena.", "Se escribe «cigüeña»."))
    b(om(b.id(), 3, "¿Qué palabra está bien escrita?", "vergüenza", ["verguenza", "vergenza", "berguenza"], "Se dice ver-güen-za: la u suena.", "Se escribe «vergüenza», con ü."))
    b(co(b.id(), 4, "pe___o 🐶", "rr", ["r", "nr", "l"], "Entre vocales, el sonido fuerte se escribe con rr.", "Se escribe «perro»."))
    b(co(b.id(), 4, "En___ique", "r", ["rr", "l", "d"], "Después de n se escribe una sola r, aunque suene fuerte.", "Se escribe «Enrique»."))
    b(cat(b.id(), 4, "¿Se escribe con r o con rr?", ["Con r", "Con rr"], [("ratón", 0), ("enredo", 0), ("pera", 0), ("perro", 1), ("carro", 1), ("tierra", 1)],
          "Al inicio o después de n va r; el sonido fuerte entre vocales va con rr.", "ratón, enredo y pera llevan r; perro, carro y tierra, rr."))
    b(om(b.id(), 5, "¿Qué oración está bien escrita?", "Mi amiga Sofía vive en Talca.", ["mi amiga sofía vive en talca.", "Mi amiga sofía vive en Talca", "mi amiga Sofía vive en talca."],
         "Revisa la mayúscula inicial, los nombres y el punto final.", "Mayúscula al inicio, en «Sofía» y «Talca», y punto al final."))
    b(orden(b.id(), 5, "Ordena las palabras para formar una oración bien escrita.", ["Los", "niños", "juegan", "en", "el", "parque."], "La palabra con mayúscula va primero y la del punto, al final.", "«Los niños juegan en el parque.»"))
    b(cat(b.id(), 5, "¿Lleva mayúscula siempre?", ["Siempre con mayúscula", "Con minúscula"], [("Chile", 0), ("Pedro", 0), ("Valparaíso", 0), ("perro", 1), ("ciudad", 1), ("río", 1)],
          "Los nombres propios llevan mayúscula.", "Chile, Pedro y Valparaíso son nombres propios."))
    return b.items


GENERADORES = {
    "1_basico.lenguaje.OA3": le01_oa3, "1_basico.lenguaje.OA4": le01_oa4, "1_basico.lenguaje.OA8": le01_oa8,
    "2_basico.lenguaje.OA5": le02_oa5, "2_basico.lenguaje.OA21": le02_oa21,
}
