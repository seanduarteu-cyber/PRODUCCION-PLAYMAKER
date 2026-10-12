"""Lenguaje y Comunicación 3° y 4° básico: 15 desafíos por OA (3 por nivel, 1 a 5)."""
from comun import (opcion_multiple as om, completar as co, ordenar as orden, emparejar as em,
                   categoria as cat)
from lenguaje_1_2 import LB


def le03_oa4():
    b = LB(3, 4)
    K = "El faro de la caleta llevaba años apagado. Don Tomás, el pescador más viejo, decidió repararlo. Trabajó una semana entera y, la última noche, la luz volvió a brillar sobre el mar."
    b(om(b.id(), 1, "¿Quién reparó el faro?", "Don Tomás", ["un niño", "el alcalde", "nadie"], "Busca quién decidió repararlo.", "Don Tomás, el pescador más viejo, lo reparó."), K)
    b(om(b.id(), 1, "¿Cuánto tiempo trabajó?", "una semana", ["un día", "un mes", "un año"], "Busca «trabajó».", "Trabajó una semana entera."), K)
    b(om(b.id(), 1, "¿Dónde estaba el faro?", "en la caleta", ["en la ciudad", "en el bosque", "en el desierto"], "Lee la primera oración.", "Era «el faro de la caleta»."), K)
    L = "{personaje} encontró un mapa antiguo en {lugar}. Siguió las pistas: cruzó un río, subió una colina y, junto a un árbol torcido, encontró un cofre lleno de {objetos}."
    b(orden(b.id(), 2, "Ordena lo que hizo {personaje}.", ["Encontró un mapa.", "Cruzó un río.", "Subió una colina.", "Encontró un cofre."], "Sigue las pistas en orden.", "Mapa, río, colina y cofre, en ese orden."), L)
    b(om(b.id(), 2, "¿Dónde estaba el cofre?", "junto a un árbol torcido", ["en el río", "en la cima de la colina", "bajo la arena"], "Busca la palabra «junto».", "El cofre estaba junto a un árbol torcido."), L)
    b(om(b.id(), 2, "¿Qué había en el cofre?", "{objetos}", ["monedas de chocolate", "ropa vieja", "nada"], "Lee el final.", "Era un cofre lleno de {objetos}."), L)
    M = "Cuando el curso supo que Matías se cambiaría de ciudad, nadie habló durante el recreo. Al día siguiente le regalaron un álbum con fotos y mensajes. Matías lo abrazó contra su pecho."
    b(om(b.id(), 3, "¿Cómo se sintió el curso al saber la noticia?", "triste", ["alegre", "enojado", "aburrido"], "¿Qué pasó en el recreo?", "Nadie habló en el recreo: estaban tristes."), M)
    b(om(b.id(), 3, "¿Por qué le regalaron un álbum?", "para que recordara a sus compañeros", ["porque era su cumpleaños", "porque ganó un concurso", "porque lo pidió"], "¿Qué tenía el álbum y por qué se lo dieron?", "Se iba de la ciudad: el álbum con fotos y mensajes era un recuerdo."), M)
    b(om(b.id(), 3, "¿Qué muestra que a Matías le gustó el regalo?", "lo abrazó contra su pecho", ["nadie habló en el recreo", "se cambió de ciudad", "lo guardó sin mirarlo"], "Busca qué hizo Matías con el álbum.", "Abrazar el álbum muestra que le gustó."), M)
    N = "La tormenta golpeaba las ventanas de la vieja casona. Adentro, a la luz de una vela, Clara leía un libro mientras su hermano menor, Lucas, se escondía bajo una frazada cada vez que sonaba un trueno."
    b(om(b.id(), 4, "¿Cómo era el ambiente de la historia?", "oscuro y tormentoso", ["soleado y tranquilo", "alegre y ruidoso", "caluroso y seco"], "Fíjate en la tormenta y la vela.", "Hay tormenta y solo la luz de una vela: oscuro y tormentoso."), N)
    b(em(b.id(), 4, "Une cada elemento con lo que dice el texto.", [["Clara", "leía un libro"], ["Lucas", "se escondía con cada trueno"], ["la casona", "era vieja"]],
         "Relee qué se dice de cada uno.", "Clara leía, Lucas se escondía y la casona era vieja."), N)
    b(om(b.id(), 4, "¿Qué palabra describe mejor a Lucas en esta escena?", "asustado", ["valiente", "aburrido", "enojado"], "¿Qué hacía cuando sonaba un trueno?", "Se escondía con cada trueno: estaba asustado."), N)
    O = "Rocío encontró una billetera en la plaza. Adentro había dinero y una credencial con una dirección. Aunque quería comprarse un helado, caminó diez cuadras para devolverla. La dueña, una señora mayor, le dio las gracias con una gran sonrisa."
    b(om(b.id(), 5, "¿Qué valor muestra Rocío?", "honestidad", ["envidia", "flojera", "egoísmo"], "¿Qué hizo con la billetera?", "Devolvió la billetera con el dinero: es honesta."), O)
    b(om(b.id(), 5, "¿Qué opinión se puede fundamentar con el texto?", "Rocío actuó bien, porque devolvió la billetera aunque quería un helado",
         ["Rocío fue egoísta porque caminó diez cuadras", "La señora se enojó con Rocío", "Rocío se quedó con el dinero"],
         "Busca una opinión con un ejemplo del texto.", "El texto muestra que devolvió la billetera aunque quería algo para ella."), O)
    b(cat(b.id(), 5, "¿Lo dice el texto o se infiere?", ["Lo dice el texto", "Se infiere"],
          [("Rocío caminó diez cuadras.", 0), ("La billetera tenía una credencial.", 0), ("Rocío es honesta.", 1), ("La señora se sintió aliviada.", 1)],
          "Si está escrito tal cual, lo dice el texto; si lo deduces, se infiere.", "Las cuadras y la credencial están escritas; la honestidad y el alivio se deducen."), O)
    return b.items


def le03_oa20():
    b = LB(3, 20)
    b(om(b.id(), 1, "¿Qué palabra es un sustantivo?", "mesa", ["rápido", "correr", "bonita"], "Los sustantivos nombran personas, animales, cosas o lugares.", "«Mesa» nombra una cosa: es un sustantivo."))
    b(co(b.id(), 1, "___ casas", "las", ["el", "la", "los"], "«Casas» es femenino y plural.", "Se dice «las casas»."))
    b(om(b.id(), 1, "¿Qué palabra es un adjetivo?", "alegre", ["saltar", "perro", "ayer"], "Los adjetivos dicen cómo es algo.", "«Alegre» dice cómo es alguien."))
    b(om(b.id(), 2, "En «el perro grande», ¿cuál es el adjetivo?", "grande", ["el", "perro", "el perro"], "¿Qué palabra dice cómo es el perro?", "«Grande» describe al perro."))
    b(co(b.id(), 2, "___ árboles altos", "los", ["la", "las", "el"], "«Árboles» es masculino y plural.", "Se dice «los árboles altos»."))
    b(cat(b.id(), 2, "¿Es sustantivo o adjetivo?", ["Sustantivo", "Adjetivo"], [("árbol", 0), ("ciudad", 0), ("niña", 0), ("verde", 1), ("alto", 1), ("feliz", 1)],
          "Sustantivo: nombra. Adjetivo: describe.", "árbol, ciudad y niña nombran; verde, alto y feliz describen."))
    b(co(b.id(), 3, "Las flores ___.", "rojas", ["rojo", "roja", "rojos"], "El adjetivo concuerda con «flores»: femenino y plural.", "«Las flores rojas»."))
    b(cat(b.id(), 3, "¿Sustantivo propio o común?", ["Propio", "Común"], [("Chile", 0), ("Andrea", 0), ("Biobío", 0), ("perro", 1), ("ciudad", 1), ("río", 1)],
          "Los propios nombran a uno en particular y llevan mayúscula.", "Chile, Andrea y Biobío son nombres propios."))
    b(om(b.id(), 3, "¿Qué artículo indefinido acompaña a «mariposa»?", "una", ["un", "unos", "el"], "Mariposa es femenino singular.", "Se dice «una mariposa»."))
    b(em(b.id(), 4, "Une cada sustantivo con el adjetivo que concuerda con él.", [["casa", "blanca"], ["perros", "juguetones"], ["sol", "amarillo"]],
         "Fíjate en el género (masculino o femenino) y en el número (singular o plural).", "casa blanca, perros juguetones y sol amarillo."))
    b(om(b.id(), 4, "¿Qué palabra puede reemplazar a «perro» sin cambiar el sentido?", "can", ["gato", "casa", "ladrar"], "Busca un sinónimo.", "«Can» es otra forma de decir perro."))
    b(co(b.id(), 4, "La niña ___ ganó la carrera.", "veloz", ["veloces", "rápidos", "lentos"], "«Niña» es singular.", "«La niña veloz» concuerda en número."))
    b(cat(b.id(), 5, "Clasifica cada palabra.", ["Artículo", "Sustantivo", "Adjetivo"], [("el", 0), ("una", 0), ("dragón", 1), ("bosque", 1), ("verde", 2), ("enorme", 2)],
          "Artículos acompañan, sustantivos nombran y adjetivos describen.", "el y una son artículos; dragón y bosque, sustantivos; verde y enorme, adjetivos."))
    b(om(b.id(), 5, "En «Una nube gris tapó el sol», ¿cuántos sustantivos hay?", 2, [1, 3, 4], "Busca las palabras que nombran cosas.", "Hay 2 sustantivos: nube y sol."))
    b(co(b.id(), 5, "Los ___ gatos durmieron.", "pequeños", ["pequeña", "pequeño", "pequeñas"], "«Gatos» es masculino y plural.", "«Los pequeños gatos»."))
    return b.items


def le03_oa22():
    b = LB(3, 22)
    b(om(b.id(), 1, "¿Cuál es el plural de «lápiz»?", "lápices", ["lápizes", "lápizs", "lápis"], "Las palabras que terminan en z cambian la z por c y agregan -es.", "lápiz → lápices."))
    b(co(b.id(), 1, "Un pez, dos ___.", "peces", ["pezes", "pezs", "pez"], "La z cambia a c antes de -es.", "pez → peces."))
    b(om(b.id(), 1, "¿Cuál es el plural de «luz»?", "luces", ["luzes", "luzs", "lus"], "z → c + es.", "luz → luces."))
    b(co(b.id(), 2, "___rafa 🦒", "ji", ["gi", "ge", "je"], "Esta palabra se escribe con j.", "Se escribe «jirafa»."))
    b(co(b.id(), 2, "___latina 🍮", "ge", ["je", "gue", "ji"], "Esta palabra se escribe con g.", "Se escribe «gelatina»."))
    b(cat(b.id(), 2, "¿Se escribe con g o con j?", ["Con g", "Con j"], [("gigante", 0), ("gente", 0), ("girasol", 0), ("jefe", 1), ("jinete", 1), ("tejido", 1)],
          "Recuerda cómo las viste escritas.", "gigante, gente y girasol van con g; jefe, jinete y tejido, con j."))
    b(co(b.id(), 3, "ratón → raton___", "cito", ["sito", "zito", "ito"], "Las palabras terminadas en n forman el diminutivo con -cito.", "ratón → ratoncito."))
    b(om(b.id(), 3, "¿Cuál está bien escrita?", "florcita", ["florsita", "florzita", "flortita"], "Diminutivo de palabras terminadas en r: -cita.", "flor → florcita."))
    b(om(b.id(), 3, "¿Cuál es el diminutivo de «camión»?", "camioncito", ["camionsito", "camionzito", "camiónsito"], "Termina en n: -cito.", "camión → camioncito."))
    b(om(b.id(), 4, "¿Qué oración usa bien las comas?", "Compré manzanas, peras, uvas y plátanos.",
         ["Compré, manzanas peras uvas y plátanos.", "Compré manzanas peras, uvas, y, plátanos.", "Compré manzanas peras uvas y, plátanos."],
         "En una enumeración, la coma separa los elementos; antes de «y» no va coma.", "manzanas, peras, uvas y plátanos."))
    b(co(b.id(), 4, "Vivo en ___.", "Valdivia", ["valdivia", "Valdibia", "balbivia"], "Los nombres de ciudades llevan mayúscula.", "Se escribe «Valdivia»."))
    b(cat(b.id(), 4, "¿Lleva mayúscula?", ["Con mayúscula", "Con minúscula"], [("Antofagasta", 0), ("Martina", 0), ("Los Andes", 0), ("cerro", 1), ("playa", 1), ("mamá", 1)],
          "Los nombres propios llevan mayúscula.", "Antofagasta, Martina y Los Andes son nombres propios."))
    b(om(b.id(), 5, "¿Cuándo se usa el punto aparte?", "al terminar un párrafo", ["al terminar cada palabra", "después de una coma", "al inicio de un texto"], "Separa ideas en párrafos.", "El punto aparte cierra un párrafo."))
    b(om(b.id(), 5, "¿Qué oración está bien escrita?", "Los peces nadan rápido en el río Maule.",
         ["los pezes nadan rápido en el río maule.", "Los pezes nadan rápido en el río Maule.", "Los peces nadan rápido en el Río maule."],
         "Revisa mayúsculas y el plural de pez.", "Mayúscula al inicio y en «Maule», y «peces» con c."))
    b(co(b.id(), 5, "Necesito lápiz___ goma y cuaderno.", ",", [".", "?", "!"], "Es una enumeración.", "Necesito lápiz, goma y cuaderno."))
    return b.items


def le04_oa4():
    b = LB(4, 4)
    P = "El volcán despertó una mañana de invierno. Las cenizas cubrieron los techos del pueblo y los animales huyeron hacia el valle. Los bomberos ayudaron a las familias a salir a tiempo."
    b(om(b.id(), 1, "¿Qué pasó cuando despertó el volcán?", "las cenizas cubrieron los techos", ["empezó a nevar", "se secó el río", "llegó el verano"], "Lee la segunda oración.", "Las cenizas cubrieron los techos del pueblo."), P)
    b(om(b.id(), 1, "¿Quiénes ayudaron a las familias?", "los bomberos", ["los animales", "los turistas", "nadie"], "Lee la última oración.", "Los bomberos ayudaron a las familias."), P)
    b(om(b.id(), 1, "¿En qué estación ocurrió?", "en invierno", ["en verano", "en otoño", "en primavera"], "Lee la primera oración.", "Fue una mañana de invierno."), P)
    Q = "Como no había llovido en meses, el estero se secó. Los agricultores no pudieron regar y la cosecha fue pequeña. Por eso, el pueblo decidió construir un estanque para guardar agua."
    b(om(b.id(), 2, "¿Por qué se secó el estero?", "porque no había llovido en meses", ["porque construyeron un estanque", "porque hubo una inundación", "porque lo taparon"], "Busca la palabra «como».", "«Como no había llovido en meses, el estero se secó»."), Q)
    b(om(b.id(), 2, "¿Cuál fue una consecuencia de la sequía?", "la cosecha fue pequeña", ["llovió mucho", "el estero creció", "los agricultores se mudaron"], "¿Qué pasó porque no pudieron regar?", "Sin riego, la cosecha fue pequeña."), Q)
    b(em(b.id(), 2, "Une cada causa con su consecuencia.", [["No llovió en meses", "El estero se secó"], ["No pudieron regar", "La cosecha fue pequeña"], ["Faltaba agua", "Construyeron un estanque"]],
         "La causa es por qué pasa algo; la consecuencia, lo que pasa después.", "Cada causa lleva a la consecuencia que sigue en el texto."), Q)
    R = "Ignacio siempre llegaba primero a clases y ayudaba a ordenar la sala. Una mañana vio que su compañera Paula lloraba porque había olvidado su colación. Sin decir nada, partió su sándwich en dos y le dio la mitad."
    b(om(b.id(), 3, "¿Qué palabra describe mejor a Ignacio?", "generoso", ["egoísta", "impuntual", "desordenado"], "¿Qué hizo con su sándwich?", "Compartió su sándwich: es generoso."), R)
    b(om(b.id(), 3, "¿Por qué lloraba Paula?", "porque olvidó su colación", ["porque llegó tarde", "porque perdió su mochila", "porque Ignacio la molestó"], "Busca «porque».", "Lloraba porque había olvidado su colación."), R)
    b(om(b.id(), 3, "¿Qué parte del texto muestra que Ignacio es responsable?", "llegaba primero y ayudaba a ordenar la sala", ["partió su sándwich en dos", "Paula lloraba", "había olvidado su colación"],
         "Busca algo que muestre responsabilidad, no generosidad.", "Llegar primero y ordenar la sala muestran responsabilidad."), R)
    S = "El desierto de Atacama amaneció cubierto de flores moradas. El cielo, limpio y azul, contrastaba con la tierra seca y rojiza. Era el desierto florido, que aparece solo en algunos años lluviosos."
    b(om(b.id(), 4, "¿Qué adjetivos describen el cielo?", "limpio y azul", ["seco y rojizo", "morado y florido", "oscuro y nublado"], "Busca la palabra «cielo».", "«El cielo, limpio y azul»."), S)
    b(om(b.id(), 4, "¿Cuándo aparece el desierto florido?", "en algunos años lluviosos", ["todos los veranos", "cada invierno", "nunca"], "Lee la última oración.", "Aparece solo en algunos años lluviosos."), S)
    b(cat(b.id(), 4, "¿Qué describe cada adjetivo?", ["El cielo", "La tierra"], [("limpio", 0), ("azul", 0), ("seca", 1), ("rojiza", 1)],
          "Relee la segunda oración.", "Limpio y azul describen el cielo; seca y rojiza, la tierra."), S)
    T = "En la escuela de Paula votaron si el recreo debía ser más largo. Paula votó que sí: dijo que con más tiempo podrían jugar, conversar y descansar antes de la siguiente clase. Joaquín votó que no, porque así saldrían más tarde a sus casas."
    b(om(b.id(), 5, "¿Qué argumento dio Paula?", "con más tiempo podrían jugar, conversar y descansar", ["saldrían más tarde a sus casas", "no le gusta el recreo", "el recreo es aburrido"], "Busca lo que dijo Paula.", "Paula dijo que podrían jugar, conversar y descansar."), T)
    b(om(b.id(), 5, "¿Por qué Joaquín votó que no?", "porque saldrían más tarde", ["porque quiere más clases", "porque no tiene amigos", "porque llovía"], "Busca «porque».", "Votó que no porque saldrían más tarde."), T)
    b(om(b.id(), 5, "¿Cuál es una opinión bien fundamentada?", "Estoy de acuerdo con Paula, porque descansar ayuda a concentrarse en la siguiente clase",
         ["Paula tiene razón porque sí", "Joaquín está mal y punto", "No me importa el recreo"], "Una opinión fundamentada da una razón.", "Da una postura y una razón que la apoya."), T)
    return b.items


def le04_oa10():
    b = LB(4, 10)
    b(om(b.id(), 1, "«El perro estaba exhausto después de correr todo el día; se tiró a dormir». ¿Qué significa «exhausto»?", "muy cansado", ["muy feliz", "con hambre", "enojado"], "¿Qué hizo el perro después?", "Se tiró a dormir después de correr: estaba muy cansado."))
    b(om(b.id(), 1, "«Después de ganar, Tomás estaba radiante: sonreía sin parar». ¿Qué significa «radiante»?", "muy feliz", ["muy triste", "muy cansado", "muy enojado"], "¿Qué hacía Tomás?", "Sonreía sin parar: estaba muy feliz."))
    b(om(b.id(), 1, "«Abrió la caja con cautela, despacio y mirando bien, por si había algo peligroso». ¿Qué significa «cautela»?", "cuidado", ["rapidez", "alegría", "ruido"], "Busca las pistas «despacio» y «mirando bien».", "Con cautela es con cuidado."))
    b(om(b.id(), 2, "¿Qué significa «deshacer»?", "lo contrario de hacer", ["hacer otra vez", "hacer antes", "hacer mucho"], "El prefijo «des-» indica lo contrario.", "des + hacer = lo contrario de hacer."))
    b(om(b.id(), 2, "¿Qué significa «releer»?", "volver a leer", ["leer poco", "no leer", "leer antes"], "El prefijo «re-» indica repetición.", "re + leer = volver a leer."))
    b(em(b.id(), 2, "Une cada prefijo con su significado.", [["des-", "lo contrario"], ["re-", "otra vez"], ["sub-", "debajo de"]], "Piensa en deshacer, rehacer y submarino.", "des- = lo contrario; re- = otra vez; sub- = debajo de."))
    b(om(b.id(), 3, "Un «zapatero» es…", "una persona que hace o arregla zapatos", ["un zapato grande", "un lugar con zapatos", "un zapato viejo"], "El sufijo «-ero» suele indicar oficio.", "zapat + ero = quien trabaja con zapatos."))
    b(om(b.id(), 3, "Alguien «miedoso» es alguien que…", "siente miedo con facilidad", ["no tiene miedo", "asusta a otros", "estudia el miedo"], "El sufijo «-oso» significa «que tiene mucho».", "miedoso = que tiene mucho miedo."))
    b(em(b.id(), 3, "Une cada palabra con su significado.", [["perrito", "perro pequeño"], ["panadero", "persona que hace pan"], ["librería", "lugar donde venden libros"]],
         "Fíjate en el final de cada palabra.", "-ito: pequeño; -ero: oficio; -ería: lugar."))
    b(cat(b.id(), 4, "¿Es de la familia de «pan»?", ["Familia de pan", "No es de la familia"], [("panadero", 0), ("panadería", 0), ("empanada", 0), ("pantalón", 1), ("pantalla", 1), ("panda", 1)],
          "Deben tener relación con el significado de pan, no solo las mismas letras.", "panadero, panadería y empanada vienen de pan; las otras solo se parecen."))
    b(cat(b.id(), 4, "¿Es de la familia de «mar»?", ["Familia de mar", "No es de la familia"], [("marino", 0), ("marinero", 0), ("marea", 0), ("martes", 1), ("martillo", 1), ("mariposa", 1)],
          "Piensa si tienen que ver con el mar.", "marino, marinero y marea vienen de mar."))
    b(om(b.id(), 4, "¿Qué palabra es de la familia de «flor»?", "florero", ["flota", "flojo", "forro"], "Busca la que tiene que ver con flores.", "Un florero es donde se ponen flores."))
    b(orden(b.id(), 5, "Ordena las palabras alfabéticamente, como en el diccionario.", ["abeja", "barco", "casa", "dedo"], "Mira la primera letra.", "a, b, c, d."))
    b(orden(b.id(), 5, "Ordena alfabéticamente.", ["cama", "cara", "casa", "cazo"], "Las dos primeras letras son iguales: mira la tercera.", "m, r, s, z: cama, cara, casa, cazo."))
    b(om(b.id(), 5, "En el diccionario, ¿entre qué palabras aparece «río»?", "rincón y rizo", ["rana y rata", "risa y rueda", "mapa y mesa"], "Compara letra por letra: r-i-o.", "rincón (r-i-n) va antes y rizo (r-i-z) va después de río (r-i-o)."))
    return b.items


def le04_oa21():
    b = LB(4, 21)
    b(co(b.id(), 1, "am___ulancia 🚑", "b", ["v", "p", "d"], "Después de m siempre va b.", "Se escribe «ambulancia»: mb."))
    b(co(b.id(), 1, "en___iar", "v", ["b", "p", "d"], "Después de n va v.", "Se escribe «enviar»: nv."))
    b(om(b.id(), 1, "¿Qué palabra está bien escrita?", "bicicleta", ["vicicleta", "bisicleta", "bicicleda"], "Empieza con «bi», que significa dos.", "Se escribe «bicicleta»."))
    b(co(b.id(), 2, "___uevo 🥚", "h", ["j", "g", "w"], "Las palabras que empiezan con «ue» llevan h.", "Se escribe «huevo»."))
    b(om(b.id(), 2, "¿Qué palabra está bien escrita?", "hoy", ["oy", "joy", "hoi"], "Lleva una h que no suena.", "Se escribe «hoy»."))
    b(om(b.id(), 2, "¿Qué palabra está bien escrita?", "hielo", ["ielo", "yelo", "jielo"], "Las palabras que empiezan con «ie» llevan h.", "Se escribe «hielo»."))
    b(co(b.id(), 3, "___ muchos niños en el patio.", "Hay", ["Ay", "Ahí", "Ai"], "«Hay» viene del verbo haber: indica que existe algo.", "«Hay muchos niños»."))
    b(co(b.id(), 3, "¡___, me pisaste!", "Ay", ["Hay", "Ahí", "Ai"], "«Ay» expresa dolor o sorpresa.", "«¡Ay, me pisaste!»."))
    b(co(b.id(), 3, "Deja la mochila ___, junto a la puerta.", "ahí", ["hay", "ay", "ai"], "«Ahí» indica un lugar.", "«Deja la mochila ahí»."))
    b(cat(b.id(), 4, "Clasifica según la sílaba tónica.", ["Aguda", "Grave", "Esdrújula"], [("canción", 0), ("reloj", 0), ("árbol", 1), ("mesa", 1), ("pájaro", 2), ("música", 2)],
          "Aguda: última sílaba; grave: penúltima; esdrújula: antepenúltima.", "can-CIÓN y re-LOJ son agudas; ÁR-bol y ME-sa, graves; PÁ-ja-ro y MÚ-si-ca, esdrújulas."))
    b(om(b.id(), 4, "«Lápiz» es una palabra…", "grave", ["aguda", "esdrújula", "sobresdrújula"], "Separa: lá-piz. ¿Dónde está la fuerza?", "LÁ-piz: la fuerza está en la penúltima sílaba."))
    b(om(b.id(), 4, "¿Por qué «camión» lleva tilde?", "porque es aguda y termina en n", ["porque es grave y termina en n", "porque es esdrújula", "porque todas las palabras llevan tilde"],
         "Las agudas llevan tilde si terminan en n, s o vocal.", "ca-MIÓN es aguda y termina en n."))
    b(om(b.id(), 5, "¿Qué palabra está bien escrita?", "música", ["musica", "músíca", "musicá"], "Las esdrújulas siempre llevan tilde.", "MÚ-si-ca es esdrújula: lleva tilde en la ú."))
    b(om(b.id(), 5, "«Dígamelo» es una palabra…", "sobresdrújula", ["esdrújula", "grave", "aguda"], "Separa: dí-ga-me-lo.", "La fuerza está antes de la antepenúltima: es sobresdrújula."))
    b(co(b.id(), 5, "El ___ cantó al amanecer.", "pájaro", ["pajaro", "pajáro", "pájaró"], "PÁ-ja-ro es esdrújula.", "Las esdrújulas llevan tilde: pájaro."))
    return b.items


GENERADORES = {
    "3_basico.lenguaje.OA4": le03_oa4, "3_basico.lenguaje.OA20": le03_oa20, "3_basico.lenguaje.OA22": le03_oa22,
    "4_basico.lenguaje.OA4": le04_oa4, "4_basico.lenguaje.OA10": le04_oa10, "4_basico.lenguaje.OA21": le04_oa21,
}
