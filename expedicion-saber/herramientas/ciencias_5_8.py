"""Ciencias Naturales 5° a 8° básico: 15 a 17 desafíos por OA (3 o 4 por nivel de dificultad, 1 a 5)."""
from autor import Autor


def cn05_oa1():
    b = Autor("cie", 5, 1)
    b.om(1, "¿Cuál es la unidad básica que forma a todos los seres vivos?", "la célula", ["el órgano", "el tejido", "el sistema"],
         "Es la parte más pequeña que tiene vida por sí misma.", "La célula es la unidad básica de todos los seres vivos.")
    b.co(1, "Un ser vivo formado por una sola célula es ___.", "unicelular", ["pluricelular", "un tejido", "un órgano"],
         "«Uni» significa uno.", "Unicelular: formado por una sola célula.")
    b.cat(1, "¿Unicelular o pluricelular?", ["Unicelular", "Pluricelular"],
          [("bacteria", 0), ("ameba", 0), ("levadura", 0), ("pudú", 1), ("copihue", 1), ("ser humano", 1)],
          "Los unicelulares solo se ven con microscopio.", "Bacteria, ameba y levadura tienen una célula; el pudú, el copihue y tú tienen muchísimas.")
    b.om(2, "¿Qué instrumento necesitas para observar la mayoría de las células?", "el microscopio", ["el telescopio", "el termómetro", "el estetoscopio"],
         "Las células son demasiado pequeñas para verlas a simple vista.", "El microscopio aumenta la imagen y permite ver las células.")
    b.ord(2, "Ordena de lo más simple a lo más complejo.", ["célula", "tejido", "órgano", "sistema", "organismo"],
          "Las células forman tejidos y así sucesivamente.", "Célula → tejido → órgano → sistema → organismo.")
    b.co(2, "Un grupo de células parecidas que cumplen la misma función forma un ___.", "tejido", ["órgano", "sistema", "organismo"],
         "Es el nivel que sigue a la célula.", "Células parecidas que trabajan juntas forman un tejido.")
    b.em(3, "Une cada nivel con un ejemplo del cuerpo humano.",
         [["célula", "neurona"], ["tejido", "tejido muscular"], ["órgano", "corazón"], ["sistema", "sistema digestivo"]],
         "Piensa de lo más pequeño a lo más grande.", "La neurona es una célula, el músculo es un tejido, el corazón un órgano y el digestivo un sistema.")
    b.om(3, "El corazón está formado por tejido muscular, tejido nervioso y otros tejidos. Por eso, el corazón es un…", "órgano", ["tejido", "célula", "sistema"],
         "Varios tejidos que trabajan juntos forman el siguiente nivel.", "Varios tejidos juntos forman un órgano: el corazón es un órgano.")
    b.cat(3, "¿Es una célula o un órgano?", ["Célula", "Órgano"],
          [("glóbulo rojo", 0), ("neurona", 0), ("glóbulo blanco", 0), ("corazón", 1), ("riñón", 1), ("estómago", 1)],
          "Los órganos están formados por millones de células.", "Glóbulos y neuronas son células; corazón, riñón y estómago son órganos.")
    b.om(4, "¿Qué estructura tienen las células vegetales y NO las animales?", "pared celular", ["membrana", "núcleo", "citoplasma"],
         "Es una cubierta rígida por fuera de la membrana.", "La pared celular solo está en las células vegetales y les da rigidez.")
    b.em(4, "Une cada estructura de la célula con su función.",
         [["membrana", "controla lo que entra y sale"], ["núcleo", "dirige las actividades de la célula"],
          ["cloroplasto", "realiza la fotosíntesis"], ["pared celular", "da rigidez a la célula vegetal"]],
         "El núcleo es como el centro de control.", "Membrana: controla el paso; núcleo: dirige; cloroplasto: fotosíntesis; pared: rigidez.")
    b.co(4, "El estómago, el intestino y el hígado trabajan juntos y forman el sistema ___.", "digestivo", ["respiratorio", "circulatorio", "nervioso"],
         "Todos participan en procesar los alimentos.", "Estos órganos procesan el alimento: forman el sistema digestivo.")
    b.om(5, "{personaje} observa al microscopio agua de un charco y ve un ser que se mueve y se alimenta, formado por una sola célula. ¿Qué puede concluir?",
         "Es un ser vivo unicelular.", ["No es un ser vivo porque tiene una sola célula.", "Es un tejido de otro animal.", "Es un órgano suelto."],
         "¿Una sola célula puede cumplir las funciones de la vida?", "Se mueve y se alimenta con una sola célula: es un ser vivo unicelular.")
    b.nu(5, "Una bacteria se divide en dos cada 20 minutos. Si {personaje} parte con 1 bacteria, ¿cuántas habrá después de 1 hora?", 8,
         "En 1 hora hay tres períodos de 20 minutos; en cada uno se duplican.", "1 → 2 → 4 → 8: después de 1 hora hay 8 bacterias.", unidad="bacterias")
    b.om(5, "Si se dañan muchas células del tejido muscular del corazón, ¿qué es lo más probable?",
         "El corazón funciona mal y afecta a todo el sistema circulatorio.",
         ["Solo se dañan esas células y nada más cambia.", "El sistema digestivo deja de existir.", "El corazón se transforma en otro órgano."],
         "Piensa en cómo los niveles dependen unos de otros.", "Las células forman el tejido, el tejido al órgano y el órgano al sistema: el daño afecta a todos.")
    b.cat(5, "¿Qué tiene solo la célula vegetal y qué tienen ambas (animal y vegetal)?", ["Solo vegetal", "Ambas"],
          [("pared celular", 0), ("cloroplastos", 0), ("membrana", 1), ("núcleo", 1), ("citoplasma", 1)],
          "Las plantas hacen fotosíntesis y tienen una cubierta rígida.", "Pared celular y cloroplastos son solo vegetales; membrana, núcleo y citoplasma están en ambas.")
    return b.items


def cn05_oa8():
    b = Autor("cie", 5, 8)
    b.om(1, "¿Qué forma de energía útil entrega una ampolleta?", "lumínica", ["sonora", "de movimiento", "química"],
         "¿Para qué enciendes una ampolleta?", "La ampolleta transforma la energía eléctrica en energía lumínica (luz).")
    b.om(1, "¿Qué aparato transforma la energía eléctrica principalmente en sonido?", "🔊 parlante", ["💡 ampolleta", "🔥 estufa", "🌀 ventilador"],
         "Piensa en el que puedes escuchar.", "El parlante transforma la energía eléctrica en energía sonora.")
    b.co(1, "Un ventilador transforma la energía eléctrica principalmente en energía de ___.", "movimiento", ["sonido", "luz", "calor"],
         "¿Qué hacen sus aspas?", "Las aspas giran: el ventilador entrega energía de movimiento.")
    b.em(2, "Une cada aparato con la energía útil que entrega.",
         [["hervidor", "calórica"], ["linterna", "lumínica"], ["timbre", "sonora"], ["licuadora", "de movimiento"]],
         "Piensa para qué usas cada aparato.", "Hervidor: calor; linterna: luz; timbre: sonido; licuadora: movimiento.")
    b.cat(2, "¿Qué energía útil entrega principalmente cada aparato?", ["Calórica", "Lumínica", "Sonora"],
          [("plancha", 0), ("estufa eléctrica", 0), ("lámpara", 1), ("semáforo", 1), ("bocina", 2), ("radio", 2)],
          "Pregúntate: ¿calienta, ilumina o suena?", "Plancha y estufa calientan; lámpara y semáforo iluminan; bocina y radio suenan.")
    b.om(2, "¿De dónde obtiene la energía eléctrica una linterna?", "de las pilas", ["de la ampolleta", "del interruptor", "del aire"],
         "¿Qué le cambias cuando deja de funcionar?", "Las pilas entregan la energía eléctrica a la linterna.")
    b.om(3, "Un hervidor eléctrico calienta el agua. ¿Qué transformación ocurre?", "eléctrica → calórica",
         ["calórica → eléctrica", "lumínica → sonora", "sonora → eléctrica"],
         "¿Qué energía recibe del enchufe y cuál entrega?", "Recibe energía eléctrica y la transforma en calórica.")
    b.ord(3, "Ordena lo que pasa al encender una linterna.",
          ["Cierras el interruptor.", "La corriente sale de la pila y recorre los cables.", "La corriente atraviesa la ampolleta.", "La ampolleta emite luz y calor."],
          "La corriente necesita un circuito cerrado para circular.", "Al cerrar el circuito, la corriente va de la pila a la ampolleta y esta emite luz y calor.")
    b.co(3, "Un secador de pelo transforma la energía eléctrica en energía calórica y de ___.", "movimiento", ["lumínica", "química", "nuclear"],
         "Además de calentar, sopla aire.", "El secador calienta y mueve el aire: calórica y de movimiento.")
    b.em(4, "Une cada científico con su aporte.",
         [["Thomas Edison", "perfeccionó la ampolleta incandescente"], ["Alessandro Volta", "inventó la pila eléctrica"],
          ["Benjamin Franklin", "demostró que el rayo es electricidad"], ["Michael Faraday", "produjo electricidad con imanes en movimiento"]],
         "La unidad del voltaje se llama así por uno de ellos.", "Edison: ampolleta; Volta: pila; Franklin: el rayo; Faraday: electricidad con imanes.")
    b.om(4, "¿Qué demostró Benjamin Franklin con su experimento del volantín en una tormenta?", "que los rayos son electricidad",
         ["que la luz viaja en línea recta", "cómo fabricar una pila", "cómo funciona la ampolleta"],
         "En una tormenta hay rayos.", "Franklin mostró que los rayos son descargas eléctricas.")
    b.om(4, "¿Por qué una ampolleta incandescente se pone muy caliente?", "porque gran parte de la energía eléctrica se transforma en calor",
         ["porque la luz siempre quema", "porque recibe calor del Sol", "porque gasta muy poca energía"],
         "La energía eléctrica no se transforma solo en luz.", "En la incandescente, la mayor parte de la energía eléctrica se transforma en calor.")
    b.nu(5, "{personaje} lee que una ampolleta recibe 100 unidades de energía eléctrica y entrega 10 como luz. El resto se transforma en calor. ¿Cuántas unidades se transforman en calor?", 90,
         "La energía no se pierde: se reparte entre luz y calor.", "100 − 10 = 90 unidades se transforman en calor.", unidad="unidades")
    b.om(5, "{personaje} quiere ahorrar energía. Dos ampolletas dan la misma luz. ¿Cuál conviene?", "la LED, porque transforma menos energía en calor",
         ["la incandescente, porque calienta más", "da lo mismo, ambas gastan igual", "la que más se calienta"],
         "Fíjate en cuánta energía se va en calor.", "La LED desperdicia menos energía en calor, así que usa menos electricidad para dar la misma luz.")
    b.cat(5, "En un ventilador y una ampolleta incandescente, ¿la energía es útil o se desperdicia?", ["Energía útil", "Energía desperdiciada"],
          [("movimiento de las aspas del ventilador", 0), ("luz de la ampolleta", 0), ("calor de la ampolleta", 1), ("zumbido del ventilador", 1)],
          "La útil es la que buscas al usar el aparato.", "Buscamos movimiento y luz; el calor de la ampolleta y el zumbido se desperdician.")
    b.co(5, "Cuando la electricidad se convierte en luz, calor y sonido, la energía no se crea ni se destruye: solo se ___.", "transforma",
         ["pierde para siempre", "multiplica", "crea"],
         "Recuerda la conservación de la energía.", "La energía se transforma de una forma en otra; no se crea ni se destruye.")
    return b.items


def cn05_oa10():
    b = Autor("cie", 5, 10)
    b.om(1, "¿Qué material deja pasar la corriente eléctrica?", "cobre", ["plástico", "madera seca", "goma"],
         "Los metales suelen conducir la electricidad.", "El cobre es un metal y conduce muy bien la electricidad.")
    b.cat(1, "¿Conductor o aislador de la electricidad?", ["Conductor", "Aislador"],
          [("clavo de hierro", 0), ("moneda", 0), ("papel de aluminio", 0), ("goma de borrar", 1), ("vaso de vidrio", 1), ("regla de plástico", 1)],
          "Los objetos de metal suelen ser conductores.", "Clavo, moneda y aluminio son metales: conductores. Goma, vidrio y plástico son aisladores.")
    b.co(1, "Los materiales que NO dejan pasar la corriente eléctrica se llaman ___.", "aisladores", ["conductores", "metales", "imanes"],
         "Aíslan, es decir, separan de la corriente.", "Los aisladores no dejan pasar la corriente eléctrica.")
    b.om(2, "¿Por qué los cables eléctricos están cubiertos de plástico?", "porque el plástico es aislador y nos protege",
         ["para que la corriente pase más rápido", "porque el plástico es conductor", "solo para que se vean bonitos"],
         "¿Qué pasaría si tocaras el metal del cable?", "El plástico es aislador: evita que la corriente pase a nuestro cuerpo.")
    b.co(2, "Por dentro, los cables tienen ___, un metal que conduce muy bien la electricidad.", "cobre", ["madera", "plástico", "vidrio"],
         "Es un metal rojizo que Chile produce en grandes cantidades.", "Los cables tienen cobre, un excelente conductor.")
    b.em(2, "Une cada parte de un enchufe con su función.",
         [["patas metálicas", "conducen la corriente"], ["cubierta de plástico", "aísla y protege la mano"], ["cable de cobre", "lleva la corriente al aparato"]],
         "Las partes de metal conducen; las de plástico aíslan.", "Las patas y el cable de cobre conducen; la cubierta plástica aísla.")
    b.om(3, "{personaje} arma un circuito con pila, cables, una ampolleta y un espacio abierto. Al poner un objeto en el espacio, la ampolleta se enciende. ¿Qué objeto puso?",
         "un clip metálico", ["un lápiz de cera", "una tapa plástica", "un trozo de cartón"],
         "La ampolleta se enciende si el objeto conduce la corriente.", "El clip es de metal, conduce la corriente y cierra el circuito.")
    b.ord(3, "Ordena los pasos para comprobar si un material es conductor.",
          ["Arma un circuito con pila, cables y ampolleta.", "Deja un espacio abierto en el circuito.", "Pon el material en el espacio.", "Observa si la ampolleta se enciende."],
          "Primero armas el circuito de prueba.", "Armas el circuito, dejas un espacio, pones el material y observas la ampolleta.")
    b.co(3, "Si la ampolleta del circuito de prueba NO se enciende, el material es ___.", "aislador", ["conductor", "metálico", "magnético"],
         "No dejó pasar la corriente.", "Si la ampolleta no se enciende, la corriente no pasó: el material es aislador.")
    b.om(4, "¿Por qué es peligroso tocar un enchufe con las manos mojadas?", "porque el agua con sales conduce la corriente hacia el cuerpo",
         ["porque el agua apaga la corriente", "porque el agua es aisladora", "porque las manos mojadas se enfrían"],
         "El agua de la llave y el sudor tienen sales disueltas.", "El agua con sales conduce la electricidad y puede llevar la corriente a tu cuerpo.")
    b.cat(4, "Algunos conductores no son metales. Clasifica.", ["Conductor", "Aislador"],
          [("grafito de un lápiz", 0), ("agua con sal", 0), ("cuerpo humano", 0), ("madera seca", 1), ("cerámica", 1), ("guante de goma", 1)],
          "El grafito, el agua con sal y tu cuerpo dejan pasar la corriente.", "Grafito, agua con sal y el cuerpo conducen; madera seca, cerámica y goma aíslan.")
    b.om(4, "¿Qué herramienta es más segura para un electricista?", "un alicate con mango de goma",
         ["un alicate de metal sin cubierta", "un destornillador mojado", "un alicate con mango de aluminio"],
         "Busca el mango que no deje pasar la corriente.", "La goma es aisladora: protege la mano del electricista.")
    b.om(5, "Tomás quiere hacer el mango de una herramienta para electricistas. ¿Qué material elige y por qué?", "goma, porque es aislador",
         ["cobre, porque es conductor", "aluminio, porque es liviano", "hierro, porque es resistente"],
         "El mango debe proteger la mano de la corriente.", "La goma es aisladora: impide que la corriente llegue a la mano.")
    b.em(5, "Une cada situación con la conducta segura.",
         [["cable pelado", "no lo toques y avisa a un adulto"], ["volantín enredado en el tendido eléctrico", "no intentes sacarlo"],
          ["manos mojadas", "sécalas antes de usar un aparato"], ["enchufe con muchos aparatos", "no lo sobrecargues"]],
         "Piensa en cómo evitar que la corriente pase por tu cuerpo.", "Cada conducta evita una descarga o un incendio.")
    b.nu(5, "{personaje} prueba en su circuito: una moneda, un clip, una llave, papel de aluminio, un clavo, una goma, un globo, un palo de helado, un vaso de vidrio y una tapa plástica. ¿Con cuántos se enciende la ampolleta?", 5,
         "Cuenta solo los objetos de metal.", "Moneda, clip, llave, aluminio y clavo son metales conductores: 5.", unidad="objetos")
    return b.items


def cn06_oa1():
    b = Autor("cie", 6, 1)
    b.om(1, "¿Qué gas liberan las plantas en la fotosíntesis?", "oxígeno", ["dióxido de carbono", "nitrógeno", "humo"],
         "Es el gas que tú respiras.", "En la fotosíntesis las plantas liberan oxígeno.")
    b.co(1, "Las plantas fabrican su propio alimento mediante la ___.", "fotosíntesis", ["respiración", "digestión", "evaporación"],
         "«Foto» significa luz.", "La fotosíntesis es el proceso con que las plantas fabrican su alimento usando luz.")
    b.om(1, "¿Qué parte de la planta realiza principalmente la fotosíntesis?", "la hoja", ["la raíz", "la flor", "la semilla"],
         "Es la parte verde que recibe más luz.", "Las hojas tienen clorofila y reciben la luz: ahí ocurre la fotosíntesis.")
    b.cat(2, "En la fotosíntesis, ¿qué necesita la planta y qué produce?", ["Lo necesita", "Lo produce"],
          [("agua", 0), ("dióxido de carbono", 0), ("luz", 0), ("oxígeno", 1), ("glucosa (azúcar)", 1)],
          "Piensa en lo que entra y lo que sale.", "Necesita agua, dióxido de carbono y luz; produce glucosa y oxígeno.")
    b.em(2, "Une cada requerimiento con cómo llega a la planta.",
         [["agua", "la absorbe la raíz"], ["dióxido de carbono", "entra por los estomas de las hojas"], ["luz", "la capta la clorofila de las hojas"]],
         "Los estomas son pequeños poros de las hojas.", "La raíz absorbe agua, el CO₂ entra por los estomas y la clorofila capta la luz.")
    b.co(2, "El pigmento verde que capta la luz se llama ___.", "clorofila", ["glucosa", "savia", "almidón"],
         "Le da el color verde a las hojas.", "La clorofila es el pigmento verde que capta la luz.")
    b.ord(3, "Ordena el camino del agua en la fotosíntesis.",
          ["La raíz absorbe agua del suelo.", "El agua sube por el tallo.", "El agua llega a las hojas.", "En las hojas, con luz y CO₂, se forma glucosa."],
          "El agua entra por abajo.", "Raíz → tallo → hojas, donde se usa para formar glucosa.")
    b.om(3, "¿Qué sustancias produce la planta en la fotosíntesis?", "glucosa y oxígeno",
         ["agua y dióxido de carbono", "oxígeno y agua", "glucosa y dióxido de carbono"],
         "Una es alimento y la otra es un gas que respiras.", "La planta produce glucosa (alimento) y libera oxígeno.")
    b.co(3, "agua + dióxido de carbono + luz → glucosa + ___", "oxígeno", ["nitrógeno", "dióxido de carbono", "clorofila"],
         "Es el gas que se libera.", "La fotosíntesis produce glucosa y oxígeno.")
    b.om(4, "{personaje} tapa una hoja de una planta con papel aluminio durante varios días. ¿Qué pasará en esa hoja?",
         "no producirá glucosa porque no recibe luz", ["producirá más glucosa", "producirá más oxígeno", "hará fotosíntesis igual que las otras"],
         "¿Qué requisito de la fotosíntesis le quitaste?", "Sin luz no hay fotosíntesis: esa hoja no fabrica glucosa.")
    b.om(4, "Una planta acuática bajo una lámpara suelta burbujitas. ¿Qué gas contienen?", "oxígeno",
         ["dióxido de carbono", "vapor de agua", "nitrógeno"],
         "Con luz, la planta hace fotosíntesis.", "Las burbujas son oxígeno liberado por la fotosíntesis.")
    b.cat(4, "¿Ocurre la fotosíntesis?", ["Sí ocurre", "No ocurre"],
          [("hoja verde al sol", 0), ("tallo verde de un cactus al sol", 0), ("alga verde en agua iluminada", 0),
           ("raíz bajo tierra", 1), ("hoja dentro de una caja oscura", 1), ("planta en plena noche", 1)],
          "Se necesita clorofila y luz al mismo tiempo.", "Hay fotosíntesis donde hay partes verdes con luz; en la raíz, la caja oscura y la noche no.")
    b.om(5, "¿Por qué casi todos los seres vivos dependen de la fotosíntesis?",
         "porque produce el alimento base de las cadenas alimentarias y el oxígeno que respiramos",
         ["porque las plantas consumen el oxígeno sobrante", "porque los animales también hacen fotosíntesis", "porque la fotosíntesis produce dióxido de carbono"],
         "Piensa en las cadenas alimentarias y en el aire.", "Las plantas son productoras: dan alimento a los consumidores y liberan oxígeno.")
    b.om(5, "En un invernadero de Atacama hay mucha luz y agua, pero el aire está encerrado y casi sin dióxido de carbono. ¿Qué pasará?",
         "las plantas harán menos fotosíntesis por falta de CO₂",
         ["harán más fotosíntesis por tener mucha luz", "no les afectará porque el CO₂ no se necesita", "liberarán más oxígeno que antes"],
         "Revisa los tres requisitos de la fotosíntesis.", "Sin suficiente dióxido de carbono, la fotosíntesis disminuye aunque haya luz y agua.")
    b.em(5, "Une cada experimento con lo que demuestra.",
         [["planta en una caja oscura", "la luz es necesaria"], ["planta sin riego", "el agua es necesaria"],
          ["planta en un frasco sin dióxido de carbono", "el CO₂ es necesario"], ["planta acuática que suelta burbujas con luz", "se libera oxígeno"]],
         "Cada experimento quita o mide una sola cosa.", "Quitar luz, agua o CO₂ muestra que son necesarios; las burbujas muestran que se libera oxígeno.")
    b.nu(5, "{personaje} cuenta las burbujas de una planta acuática: con poca luz suelta 6 por minuto y con mucha luz, 4 veces más. ¿Cuántas burbujas suelta en 1 minuto con mucha luz?", 24,
         "Multiplica las burbujas con poca luz por 4.", "6 × 4 = 24 burbujas: más luz, más fotosíntesis.", unidad="burbujas")
    return b.items


def cn06_oa8():
    b = Autor("cie", 6, 8)
    b.om(1, "¿De dónde proviene la mayor parte de la energía que usamos en la Tierra?", "del Sol",
         ["de la Luna", "de las estrellas lejanas", "del centro de la Tierra"],
         "Lo ves en el cielo cada día.", "Casi toda la energía de la Tierra viene, directa o indirectamente, del Sol.")
    b.cat(1, "¿Fuente renovable o no renovable?", ["Renovable", "No renovable"],
          [("solar", 0), ("eólica (viento)", 0), ("hidráulica (ríos)", 0), ("petróleo", 1), ("carbón", 1), ("gas natural", 1)],
          "Las renovables no se agotan.", "Sol, viento y ríos se renuevan; petróleo, carbón y gas se agotan.")
    b.co(1, "Los seres vivos necesitan ___ para crecer, moverse y mantenerse vivos.", "energía", ["oscuridad", "ruido", "plástico"],
         "La obtienen de los alimentos.", "Los seres vivos necesitan energía para todos sus procesos vitales.")
    b.om(2, "¿Por qué el petróleo es una fuente no renovable?", "porque tarda millones de años en formarse",
         ["porque se produce cada día", "porque viene del viento", "porque nunca se acaba"],
         "Piensa en cuánto tarda en formarse.", "El petróleo tarda millones de años en formarse: se agota antes de renovarse.")
    b.em(2, "Une cada central con lo que usa para producir electricidad.",
         [["eólica", "viento"], ["hidroeléctrica", "agua de los ríos"], ["solar", "luz del Sol"], ["geotérmica", "calor del interior de la Tierra"]],
         "Los nombres dan pistas: «eólica» viene de Eolo, el viento.", "Eólica: viento; hidroeléctrica: ríos; solar: luz; geotérmica: calor interno de la Tierra.")
    b.om(2, "¿Qué ejemplo muestra que la energía produce cambios en un objeto?", "el hielo se derrite al recibir calor",
         ["una piedra quieta en el suelo", "un libro guardado en el estante", "una mesa sin usar"],
         "Busca algo que cambie.", "El hielo cambia de estado porque recibe energía calórica.")
    b.ord(3, "Ordena el camino de la energía hasta que {personaje} corre.",
          ["Sol", "pasto (fotosíntesis)", "vaca", "leche que toma", "músculos al correr"],
          "La energía empieza en el Sol y pasa por la cadena alimentaria.", "Sol → pasto → vaca → leche → músculos: la energía viene indirectamente del Sol.")
    b.om(3, "La energía del viento proviene indirectamente del Sol porque…", "el Sol calienta el aire de forma desigual y lo pone en movimiento",
         ["el Sol sopla aire hacia la Tierra", "la Luna mueve el aire", "el viento se forma en el interior de la Tierra"],
         "El aire caliente sube y el frío ocupa su lugar.", "El Sol calienta distinto el aire de cada lugar y eso produce el viento.")
    b.cat(3, "¿La energía viene directa o indirectamente del Sol?", ["Directamente", "Indirectamente"],
          [("panel solar", 0), ("ropa secándose al sol", 0), ("lagartija calentándose al sol", 0), ("viento", 1), ("leña", 1), ("agua de un embalse", 1)],
          "Indirecta: la energía solar pasó antes por otro proceso.", "Panel, ropa y lagartija usan la luz solar; viento, leña y embalse la recibieron a través de otros procesos.")
    b.om(4, "¿Por qué se dice que el petróleo guarda energía del Sol?", "se formó de restos de seres vivos antiguos que obtuvieron energía del Sol",
         ["se formó de rocas calientes de los volcanes", "se formó con agua de mar evaporada", "lo fabricaron los seres humanos"],
         "Piensa en de qué está hecho el petróleo.", "El petróleo viene de seres vivos antiguos, que obtuvieron su energía de la fotosíntesis.")
    b.co(4, "En el desierto de Atacama llega muchísima luz solar; por eso conviene instalar centrales de energía ___.", "solar",
         ["a carbón", "a petróleo", "a leña"],
         "Aprovecha lo que más abunda allí.", "Atacama tiene una de las radiaciones solares más altas del mundo: ideal para energía solar.")
    b.om(4, "Si el Sol dejara de brillar, ¿qué pasaría primero en un ecosistema?", "las plantas no podrían hacer fotosíntesis y faltaría alimento",
         ["los animales tendrían más alimento", "las rocas producirían luz", "aumentaría la fotosíntesis"],
         "¿Quiénes captan la energía del Sol?", "Sin luz, las plantas no fabrican alimento y toda la cadena alimentaria se afecta.")
    b.om(5, "¿Cuál de estas fuentes de energía NO depende del Sol?", "geotérmica",
         ["eólica", "hidroeléctrica", "leña"],
         "Una usa el calor del interior de la Tierra.", "La geotérmica usa el calor interno de la Tierra; las demás dependen del Sol.")
    b.om(5, "Un auto a bencina y una ciclista suben el mismo cerro. ¿De dónde sale, en último término, la energía de ambos?", "del Sol",
         ["del motor y de los pedales, que la crean", "del interior de la Tierra", "de la Luna"],
         "La bencina viene del petróleo y la ciclista se alimenta.", "La bencina viene de seres vivos antiguos y los alimentos de plantas: ambos dependen del Sol.")
    b.co(5, "Si Chile cambia centrales a carbón por centrales solares, disminuye el uso de fuentes ___.", "no renovables",
         ["renovables", "solares", "eólicas"],
         "¿Qué tipo de fuente es el carbón?", "El carbón es no renovable; reemplazarlo reduce el uso de fuentes no renovables.")
    b.nu(5, "{personaje} visita una región con 12 centrales: 5 solares, 3 eólicas, 1 geotérmica y 3 a carbón. ¿Cuántas usan fuentes renovables?", 9,
         "Solo el carbón es no renovable.", "5 + 3 + 1 = 9 centrales usan fuentes renovables.", unidad="centrales")
    return b.items


def cn06_oa13():
    b = Autor("cie", 6, 13)
    b.om(1, "¿Cómo se llama el paso de sólido a líquido?", "fusión", ["solidificación", "condensación", "evaporación"],
         "Ocurre cuando un helado se derrite.", "El paso de sólido a líquido es la fusión.")
    b.co(1, "El agua de una cubetera se transforma en hielo en el congelador: es una ___.", "solidificación", ["fusión", "evaporación", "sublimación"],
         "Pasa de líquido a sólido.", "De líquido a sólido es solidificación.")
    b.om(1, "¿En qué estado está el agua de un cubo de hielo 🧊?", "sólido", ["líquido", "gaseoso", "vapor"],
         "Tiene forma propia.", "El hielo es agua en estado sólido.")
    b.em(2, "Une cada cambio con su nombre.",
         [["sólido → líquido", "fusión"], ["líquido → sólido", "solidificación"], ["gas → líquido", "condensación"], ["sólido → gas", "sublimación"]],
         "Sublimación es el paso directo, sin ser líquido.", "Fusión, solidificación, condensación y sublimación.")
    b.om(2, "En una mañana fría se empañan los vidrios del bus por dentro. ¿Qué cambio de estado ocurre?", "condensación",
         ["evaporación", "fusión", "sublimación"],
         "El vapor del aire toca el vidrio frío.", "El vapor de agua se enfría en el vidrio y pasa a líquido: condensación.")
    b.nu(2, "¿A qué temperatura hierve el agua pura al nivel del mar?", 100,
         "Es un número redondo en grados Celsius.", "El agua pura hierve a 100 °C al nivel del mar.", unidad="°C")
    b.ord(3, "Ordena lo que pasa al calentar un cubo de hielo en una olla hasta que desaparece.",
          ["El hielo está sólido.", "El hielo se funde.", "El agua líquida se calienta.", "El agua hierve y se vuelve vapor."],
          "Primero cambia a líquido y después a gas.", "Sólido → fusión → líquido caliente → ebullición.")
    b.cat(3, "¿Qué cambio de estado ocurre?", ["Fusión", "Condensación", "Sublimación"],
          [("helado que se derrite", 0), ("chocolate al sol", 0), ("gotas en una botella fría", 1), ("rocío en el pasto al amanecer", 1),
           ("naftalina que se achica en el clóset", 2), ("hielo seco que desaparece sin mojar", 2)],
          "La sublimación pasa de sólido a gas sin mojar.", "Helado y chocolate se funden; gotas y rocío son condensación; naftalina y hielo seco subliman.")
    b.om(3, "En el ciclo del agua, ¿qué cambio de estado forma las nubes?", "condensación del vapor de agua",
         ["evaporación del agua de las nubes", "fusión del vapor", "sublimación del agua de mar"],
         "El vapor sube y se enfría.", "Al subir, el vapor se enfría y se condensa en gotitas que forman las nubes.")
    b.om(4, "¿En qué se diferencia la evaporación de la ebullición?", "la evaporación ocurre en la superficie a cualquier temperatura; la ebullición, en todo el líquido",
         ["son exactamente lo mismo", "la evaporación necesita fuego", "la ebullición ocurre solo en la superficie"],
         "Piensa en un charco que se seca y en una olla que burbujea.", "El charco se evapora sin hervir; en la ebullición se forman burbujas en todo el líquido.")
    b.cat(4, "¿El material absorbe o libera calor en este cambio?", ["Absorbe calor", "Libera calor"],
          [("fusión", 0), ("evaporación", 0), ("sublimación", 0), ("condensación", 1), ("solidificación", 1)],
          "Para separar las partículas se necesita energía.", "Fusión, evaporación y sublimación absorben calor; condensación y solidificación lo liberan.")
    b.nu(4, "Mientras el hielo se funde, el termómetro marca la misma temperatura aunque sigas calentando. ¿Cuál es esa temperatura?", 0,
         "Es el punto de fusión del agua.", "El hielo se funde a 0 °C y se mantiene ahí hasta derretirse por completo.", unidad="°C")
    b.co(4, "La ropa colgada se seca aunque el agua no hierva: el agua de la ropa se ___.", "evapora", ["condensa", "solidifica", "funde"],
         "Pasa de líquido a gas desde la superficie.", "El agua de la ropa se evapora lentamente sin hervir.")
    b.om(5, "¿Por qué la ropa tendida se seca más rápido en un día caluroso y con viento?", "porque el calor y el viento aceleran la evaporación",
         ["porque el viento produce condensación", "porque el calor hace hervir el agua de la ropa", "porque el agua se solidifica"],
         "El calor da energía y el viento se lleva el vapor.", "Más calor y viento hacen que el agua se evapore más rápido.")
    b.ord(5, "Ordena el ciclo del agua empezando por el mar.",
          ["El agua del mar se evapora.", "El vapor sube y se condensa en nubes.", "Cae lluvia o nieve en la cordillera.", "La nieve se funde y baja por los ríos al mar."],
          "Sigue los cambios: evaporación, condensación, precipitación, fusión.", "Evaporación → condensación → precipitación → fusión de la nieve.")
    b.em(5, "Une cada situación de la naturaleza con su cambio de estado.",
         [["glaciar que se derrite", "fusión"], ["escarcha que desaparece sin mojar", "sublimación"],
          ["lava que se enfría y forma roca", "solidificación"], ["neblina que se forma sobre el mar en la mañana", "condensación"]],
         "Piensa de qué estado a qué estado pasa cada uno.", "Glaciar: fusión; escarcha: sublimación; lava: solidificación; neblina: condensación.")
    return b.items


def cn07_oa8():
    b = Autor("cie", 7, 8)
    b.om(1, "¿Por qué un cuchillo afilado corta mejor que uno sin filo?", "porque concentra la fuerza en un área más pequeña",
         ["porque es más pesado", "porque tiene más área de contacto", "porque está más frío"],
         "El filo es muy delgado.", "Con menos área, la misma fuerza produce más presión.")
    b.co(1, "La presión es la fuerza aplicada sobre una ___.", "superficie", ["masa", "temperatura", "velocidad"],
         "P = F ÷ A.", "La presión es fuerza dividida por la superficie (área).")
    b.om(1, "¿Para qué sirven las raquetas de nieve?", "para no hundirse, porque reparten el peso en un área mayor",
         ["para caminar más rápido", "para derretir la nieve", "para aumentar la presión sobre la nieve"],
         "Son mucho más anchas que un zapato.", "Al aumentar el área, disminuye la presión y no te hundes.")
    b.cat(2, "¿El objeto aumenta o disminuye la presión?", ["Aumenta la presión", "Disminuye la presión"],
          [("clavo con punta", 0), ("aguja", 0), ("chinche", 0), ("raquetas de nieve", 1), ("orugas de un tractor", 1), ("mochila con tirantes anchos", 1)],
          "Área pequeña: más presión. Área grande: menos presión.", "Punta y filo concentran la fuerza; lo ancho la reparte.")
    b.om(2, "¿Qué pasa con la presión del agua a medida que bajas en una piscina?", "aumenta", ["disminuye", "se mantiene igual", "desaparece"],
         "Mientras más bajas, más agua tienes encima.", "La presión del agua aumenta con la profundidad.")
    b.co(2, "Al subir a la cordillera, la presión atmosférica ___.", "disminuye", ["aumenta", "se duplica", "no cambia"],
         "Arriba hay menos aire sobre ti.", "A mayor altura hay menos aire encima: la presión atmosférica disminuye.")
    b.nu(3, "Una caja de 600 N se apoya sobre una superficie de 3 m². ¿Qué presión ejerce?", 200,
         "P = F ÷ A.", "600 N ÷ 3 m² = 200 Pa.", unidad="Pa")
    b.om(3, "Un bidón con agua tiene tres agujeros a distintas alturas. ¿Por cuál sale el chorro más lejos?", "por el de más abajo",
         ["por el de más arriba", "por el del medio", "todos llegan igual de lejos"],
         "¿Dónde hay más agua encima?", "Abajo la presión es mayor, por eso el chorro sale con más fuerza.")
    b.em(3, "Une cada objeto con cómo usa la presión.",
         [["chinche", "punta fina: mucha presión"], ["raqueta de nieve", "base ancha: poca presión"],
          ["gata hidráulica", "el líquido transmite la presión"], ["bombilla para tomar jugo", "la presión del aire empuja el líquido"]],
         "Fíjate si es sólido, líquido o gas.", "Chinche y raqueta usan el área; la gata usa un líquido; la bombilla, la presión atmosférica.")
    b.nu(4, "Un bloque de 120 N se apoya sobre una cara de 40 cm² y luego sobre una de 20 cm². ¿Cuántas veces mayor es la presión en la segunda posición?", 2,
         "Con la misma fuerza, si el área baja a la mitad…", "120 ÷ 40 = 3 N/cm² y 120 ÷ 20 = 6 N/cm²: el doble.", unidad="veces")
    b.om(4, "En una prensa hidráulica empujas el pistón pequeño con poca fuerza. ¿Qué ocurre en el pistón grande?",
         "ejerce una fuerza mayor, porque el líquido transmite la presión por igual",
         ["ejerce menos fuerza", "no se mueve porque los líquidos no transmiten presión", "el líquido se comprime y desaparece"],
         "La presión es la misma en todo el líquido; el área no.", "Igual presión sobre un área mayor da una fuerza mayor (principio de Pascal).")
    b.co(4, "Los muros de un embalse son más gruesos en la base porque la presión del agua ___ con la profundidad.", "aumenta",
         ["disminuye", "no cambia", "desaparece"],
         "Abajo hay más agua encima.", "La presión aumenta con la profundidad, por eso la base debe ser más resistente.")
    b.ord(4, "Ordena de menor a mayor presión atmosférica.",
          ["Ojos del Salado (6.893 m)", "Putre (3.500 m)", "Santiago (570 m)", "Valparaíso (0 m)"],
          "A más altura, menos presión.", "La presión aumenta al bajar: Ojos del Salado, Putre, Santiago y Valparaíso.")
    b.nu(5, "{personaje} empuja con 400 N el pistón pequeño de una prensa hidráulica, de 2 cm². El pistón grande mide 20 cm². ¿Qué fuerza ejerce el pistón grande?", 4000,
         "Calcula la presión en el pistón pequeño y úsala en el grande.", "400 ÷ 2 = 200 N/cm²; 200 × 20 = 4.000 N.", unidad="N")
    b.om(5, "¿Por qué se te tapan los oídos al subir rápido en auto a la cordillera?",
         "porque baja la presión del aire exterior y queda distinta a la del oído interno",
         ["porque aumenta la presión exterior al subir", "porque hace más frío", "porque el auto vibra"],
         "Compara la presión dentro y fuera de tu oído.", "Al subir, la presión exterior baja y se desequilibra con la del oído interno.")
    b.cat(5, "¿Dónde actúa la presión en cada caso?", ["En sólidos", "En líquidos", "En gases"],
          [("una chinche entra fácil en el corcho", 0), ("huellas de un camión en el barro", 0), ("una gata hidráulica levanta un auto", 1),
           ("un buzo siente más presión al bajar", 1), ("una ventosa se pega a un vidrio", 2), ("un globo se agranda en la cima de un cerro", 2)],
          "Pregúntate qué transmite o ejerce la presión.", "Chinche y camión: sólidos; gata y buzo: líquidos; ventosa y globo: gases (presión atmosférica).")
    return b.items


def cn07_oa13():
    b = Autor("cie", 7, 13)
    b.om(1, "Según la teoría cinético-molecular, las partículas de un gas…", "se mueven rápido y en todas direcciones",
         ["están quietas", "están muy juntas y ordenadas", "solo se mueven hacia abajo"],
         "Los gases llenan todo el recipiente.", "Las partículas de un gas se mueven rápido y en todas direcciones.")
    b.co(1, "Si calientas un globo, su volumen ___.", "aumenta", ["disminuye", "no cambia", "desaparece"],
         "El calor hace que las partículas se muevan más.", "Al calentarse, el gas se expande y el globo se agranda.")
    b.om(1, "¿Qué le pasa a un globo inflado si lo metes al congelador?", "se achica", ["se infla más", "explota", "no cambia nada"],
         "El frío hace que las partículas se muevan menos.", "Al enfriarse, el gas ocupa menos volumen y el globo se achica.")
    b.em(2, "Une cada ley con lo que relaciona.",
         [["Ley de Boyle", "presión y volumen (temperatura fija)"], ["Ley de Charles", "volumen y temperatura (presión fija)"],
          ["Ley de Gay-Lussac", "presión y temperatura (volumen fijo)"]],
         "Cada ley mantiene fija una variable.", "Boyle: P y V; Charles: V y T; Gay-Lussac: P y T.")
    b.cat(2, "¿Es una propiedad de los gases?", ["Sí", "No"],
          [("se comprime fácilmente", 0), ("ocupa todo el recipiente", 0), ("se difunde en el aire", 0),
           ("tiene forma fija", 1), ("tiene volumen fijo", 1), ("sus partículas están quietas", 1)],
          "Piensa en el aire dentro de una jeringa.", "Los gases se comprimen, llenan el recipiente y se difunden; no tienen forma ni volumen fijos.")
    b.om(2, "Aprietas una jeringa tapada con aire y su volumen baja. ¿Qué pasa con la presión del aire?", "aumenta",
         ["disminuye", "no cambia", "se vuelve cero"],
         "Las mismas partículas en menos espacio chocan más seguido.", "Menos volumen, más presión (ley de Boyle).")
    b.nu(3, "Un gas ocupa 6 L a 2 atm. Si la presión sube a 3 atm sin cambiar la temperatura, ¿qué volumen ocupa?", 4,
         "P × V se mantiene constante.", "2 × 6 = 12; 12 ÷ 3 = 4 L.", unidad="L")
    b.om(3, "¿Por qué aumenta la presión de los neumáticos después de un viaje largo?",
         "el aire se calienta y sus partículas chocan más rápido y más seguido contra las paredes",
         ["entra más aire por la válvula", "las partículas se hacen más grandes", "el neumático se achica por el frío"],
         "El roce con el camino calienta el neumático.", "Más temperatura, más movimiento de partículas y más presión (Gay-Lussac).")
    b.co(3, "El olor de un perfume llega a toda la sala porque las partículas del gas se ___.", "difunden", ["condensan", "detienen", "funden"],
         "Se mueven y se mezclan con el aire.", "Las partículas se mueven y se esparcen: se difunden.")
    b.nu(4, "Un globo tiene 3 L. Si su temperatura absoluta (en kelvin) se duplica a presión constante, ¿qué volumen tendrá?", 6,
         "Volumen y temperatura absoluta son proporcionales.", "Si la temperatura absoluta se duplica, el volumen también: 6 L.", unidad="L")
    b.om(4, "Una lata de aerosol dice «no exponer al calor». ¿Por qué?", "al calentarse, aumenta la presión del gas dentro y puede explotar",
         ["el gas se enfría y se congela", "la presión disminuye y la lata se aplasta", "el gas se transforma en sólido"],
         "La lata no puede cambiar su volumen.", "Con volumen fijo, más temperatura significa más presión (Gay-Lussac).")
    b.cat(4, "¿Qué ley explica cada situación?", ["Boyle (P y V)", "Charles (V y T)", "Gay-Lussac (P y T)"],
          [("jeringa tapada que se aprieta", 0), ("bombín que comprime aire", 0), ("globo que se agranda al sol", 1),
           ("globo que se achica en el refrigerador", 1), ("olla a presión que se calienta", 2), ("lata cerrada que se calienta", 2)],
          "Fíjate en qué variable se mantiene fija.", "Apretar cambia P y V; globos cambian V con T; recipientes rígidos cambian P con T.")
    b.ord(5, "{personaje} pone un globo en la boca de una botella vacía y la mete en agua caliente. Ordena lo que ocurre.",
          ["La botella se calienta.", "Las partículas de aire se mueven más rápido.", "Las partículas chocan con más fuerza y se separan más.", "El aire ocupa más volumen y el globo se infla."],
          "Primero cambia la temperatura y luego el movimiento de las partículas.", "Calor → partículas más rápidas → más separación → más volumen (Charles).")
    b.om(5, "{personaje} cierra una botella plástica vacía en la cumbre de un cerro. Al llegar a la costa, la botella está aplastada. ¿Por qué?",
         "la presión exterior aumenta al bajar y comprime el aire de la botella",
         ["el aire de adentro se calentó", "el plástico se derritió", "la presión exterior disminuyó al bajar"],
         "Compara la presión del aire arriba y abajo.", "Abajo la presión atmosférica es mayor y reduce el volumen del aire encerrado (Boyle).")
    b.nu(5, "Un gas ocupa 12 L a 1 atm. Se comprime primero a 6 L y después a 3 L, sin cambiar la temperatura. ¿Cuál es la presión final?", 4,
         "Cada vez que el volumen baja a la mitad, la presión se duplica.", "12 L → 6 L: 2 atm; 6 L → 3 L: 4 atm.", unidad="atm")
    b.em(5, "Une cada observación con su explicación según la teoría cinético-molecular.",
         [["un gas se comprime fácilmente", "hay mucho espacio vacío entre sus partículas"],
          ["un gas llena todo el recipiente", "sus partículas se mueven libremente en todas direcciones"],
          ["un gas caliente ejerce más presión", "sus partículas chocan más rápido y más seguido"]],
         "Piensa en el espacio y el movimiento de las partículas.", "Espacio vacío permite comprimir; el movimiento libre llena el recipiente; más velocidad, más choques.")
    return b.items


def cn07_oa14():
    b = Autor("cie", 7, 14)
    b.cat(1, "¿Sustancia pura o mezcla?", ["Sustancia pura", "Mezcla"],
          [("agua destilada", 0), ("oro", 0), ("sal de mesa", 0), ("ensalada de frutas", 1), ("agua de mar", 1), ("aire", 1)],
          "Una mezcla tiene dos o más sustancias.", "Agua destilada, oro y sal son puras; ensalada, agua de mar y aire son mezclas.")
    b.om(1, "¿Qué método usas para separar piedras de la arena?", "tamizado", ["destilación", "decantación", "evaporación"],
         "Se usa un harnero o colador.", "El tamiz deja pasar la arena y retiene las piedras.")
    b.co(1, "Una mezcla en la que se distinguen sus componentes a simple vista es ___.", "heterogénea", ["homogénea", "un elemento", "un compuesto"],
         "«Hetero» significa distinto.", "Si ves sus partes, la mezcla es heterogénea.")
    b.cat(2, "¿Mezcla homogénea o heterogénea?", ["Homogénea", "Heterogénea"],
          [("agua con sal disuelta", 0), ("aire limpio", 0), ("té con azúcar disuelta", 0), ("agua con aceite", 1), ("arena con piedras", 1), ("cereal con leche", 1)],
          "En la homogénea no distingues sus partes.", "Agua salada, aire y té con azúcar se ven uniformes; las otras no.")
    b.em(2, "Une cada mezcla con su método de separación.",
         [["agua y arena", "filtración"], ["agua y aceite", "decantación"], ["arena y piedras", "tamizado"], ["agua y alcohol", "destilación"]],
         "Piensa si son sólidos, líquidos o ambos.", "Filtración retiene sólidos, decantación separa líquidos que no se mezclan, el tamiz separa por tamaño y la destilación usa la ebullición.")
    b.om(2, "¿Qué es un elemento?", "una sustancia pura formada por un solo tipo de átomo",
         ["una mezcla de dos sustancias", "una sustancia formada por varios tipos de átomos unidos", "cualquier líquido"],
         "Está en la tabla periódica.", "Un elemento es una sustancia pura con un solo tipo de átomo, como el oro o el oxígeno.")
    b.cat(3, "¿Elemento o compuesto?", ["Elemento", "Compuesto"],
          [("oxígeno (O₂)", 0), ("hierro (Fe)", 0), ("cobre (Cu)", 0), ("agua (H₂O)", 1), ("dióxido de carbono (CO₂)", 1), ("sal de mesa (NaCl)", 1)],
          "Mira cuántos tipos de átomo hay en la fórmula.", "O₂, Fe y Cu tienen un solo tipo de átomo; H₂O, CO₂ y NaCl tienen dos.")
    b.om(3, "Quieres obtener agua para beber a partir de agua de mar, recuperando el agua. ¿Qué método usas?", "destilación",
         ["filtración", "tamizado", "decantación"],
         "La sal está disuelta: no la retiene un filtro.", "Al destilar, el agua se evapora, se condensa aparte y la sal queda atrás.")
    b.co(3, "La destilación separa líquidos aprovechando que tienen distinto punto de ___.", "ebullición", ["fusión", "color", "masa"],
         "Uno hierve antes que el otro.", "Cada líquido hierve a una temperatura distinta: su punto de ebullición.")
    b.ord(4, "Ordena los pasos para separar arena, sal y agua.",
          ["Filtra la mezcla.", "La arena queda en el papel filtro.", "Calienta el agua salada que pasó.", "Al evaporarse el agua, queda la sal."],
          "Primero separa lo que no se disuelve.", "Filtrar retiene la arena; después, evaporar el agua deja la sal.")
    b.om(4, "¿Por qué el agua y el aceite se pueden separar por decantación?", "porque no se mezclan y tienen distinta densidad",
         ["porque tienen el mismo color", "porque el aceite se evapora primero", "porque el agua es un elemento"],
         "El aceite flota sobre el agua.", "No se mezclan y el aceite es menos denso: queda arriba y se puede separar.")
    b.nu(4, "Una mezcla de arena y sal pesa 500 g. {personaje} la separa y obtiene 120 g de sal. ¿Cuántos gramos de arena había?", 380,
         "La masa total es la suma de las partes.", "500 − 120 = 380 g de arena.", unidad="g")
    b.om(5, "El agua de la llave, ¿es una sustancia pura o una mezcla?", "una mezcla homogénea, porque tiene sales disueltas",
         ["una sustancia pura, porque es transparente", "un elemento, porque es agua", "una mezcla heterogénea, porque se ve igual en todas partes"],
         "Que se vea transparente no significa que sea pura.", "El agua de la llave tiene sales y gases disueltos: es una mezcla homogénea.")
    b.om(5, "En el norte, algunos buscadores de oro mueven arena con agua en una batea. ¿Qué propiedad aprovechan?",
         "el oro es más denso y queda en el fondo", ["el oro flota sobre el agua", "el oro se disuelve en el agua", "el oro es atraído por un imán"],
         "El oro es muy pesado para su tamaño.", "El oro es más denso que la arena: se va al fondo y la arena sale con el agua.")
    b.nu(5, "{personaje} tiene 300 g de una mezcla de arena, sal y piedras. Con el tamiz saca 100 g de piedras y, al filtrar y evaporar, obtiene 60 g de sal. ¿Cuántos gramos de arena había?", 140,
         "Resta las piedras y la sal del total.", "300 − 100 − 60 = 140 g de arena.", unidad="g")
    b.em(5, "Une cada material con su clasificación.",
         [["oro", "elemento"], ["agua destilada", "compuesto"], ["agua de mar", "mezcla homogénea"], ["arena con conchitas", "mezcla heterogénea"]],
         "Primero decide si es pura o mezcla.", "Oro: elemento; agua destilada: compuesto; agua de mar: homogénea; arena con conchitas: heterogénea.")
    return b.items


def cn08_oa10():
    b = Autor("cie", 8, 10)
    b.om(1, "¿Qué instrumento mide la intensidad de corriente?", "amperímetro", ["voltímetro", "termómetro", "barómetro"],
         "La corriente se mide en amperes.", "El amperímetro mide la intensidad de corriente en amperes.")
    b.em(1, "Une cada magnitud con su unidad.",
         [["voltaje", "volt (V)"], ["intensidad de corriente", "ampere (A)"], ["resistencia", "ohm (Ω)"], ["potencia", "watt (W)"]],
         "Cada unidad lleva el nombre de un científico.", "Voltaje: V; corriente: A; resistencia: Ω; potencia: W.")
    b.co(1, "En un circuito en ___, la corriente tiene un solo camino.", "serie", ["paralelo", "abierto", "mixto"],
         "Los componentes van uno tras otro.", "En serie hay un solo camino para la corriente.")
    b.nu(2, "Si por una resistencia de 6 Ω circulan 2 A, ¿cuál es el voltaje? (V = I · R)", 12,
         "Multiplica la intensidad por la resistencia.", "V = 2 A · 6 Ω = 12 V.", unidad="V")
    b.om(2, "Los enchufes de una casa están conectados en paralelo. ¿Qué ventaja tiene?", "si un aparato se apaga, los demás siguen funcionando",
         ["todos se apagan juntos", "la corriente tiene un solo camino", "cada aparato recibe menos voltaje"],
         "En paralelo cada aparato tiene su propio camino.", "En paralelo, cada aparato funciona aunque otro se desconecte.")
    b.cat(2, "¿Circuito en serie o en paralelo?", ["Serie", "Paralelo"],
          [("un solo camino para la corriente", 0), ("si una ampolleta se quema, todas se apagan", 0), ("la misma corriente pasa por todas las ampolletas", 0),
           ("varios caminos para la corriente", 1), ("cada ampolleta recibe el mismo voltaje", 1), ("los enchufes de una casa", 1)],
          "Serie: uno tras otro. Paralelo: ramas.", "En serie hay un camino y una sola corriente; en paralelo hay ramas con el mismo voltaje.")
    b.nu(3, "Una pila de 9 V se conecta a una resistencia de 3 Ω. ¿Qué intensidad de corriente circula?", 3,
         "I = V ÷ R.", "I = 9 V ÷ 3 Ω = 3 A.", unidad="A")
    b.nu(3, "Un hervidor funciona con 220 V y 10 A. ¿Qué potencia tiene? (P = V · I)", 2200,
         "Multiplica el voltaje por la intensidad.", "P = 220 V · 10 A = 2.200 W.", unidad="W")
    b.om(3, "Si aumentas la resistencia de un circuito sin cambiar el voltaje, ¿qué pasa con la corriente?", "disminuye",
         ["aumenta", "no cambia", "se duplica"],
         "I = V ÷ R: R está dividiendo.", "Con el mismo voltaje, más resistencia significa menos corriente.")
    b.om(3, "{personaje} conecta 3 ampolletas iguales en serie y una se quema. ¿Qué pasa?", "todas se apagan, porque se abre el único camino",
         ["solo se apaga la quemada", "las otras brillan más", "las otras siguen igual"],
         "En serie hay un solo camino.", "Al quemarse una, el circuito queda abierto y la corriente deja de circular.")
    b.nu(4, "Dos resistencias de 4 Ω y 8 Ω están en serie con una batería de 24 V. ¿Qué corriente circula?", 2,
         "En serie, las resistencias se suman.", "R = 4 + 8 = 12 Ω; I = 24 ÷ 12 = 2 A.", unidad="A")
    b.co(4, "Energía eléctrica consumida = potencia × ___.", "tiempo", ["voltaje", "resistencia", "intensidad"],
         "Por eso se mide en kilowatt-hora.", "La energía es la potencia por el tiempo de uso (kWh).")
    b.ord(4, "Ordena de menor a mayor energía consumida en 1 hora.",
          ["ampolleta LED de 9 W", "notebook de 60 W", "televisor de 150 W", "plancha de 1.200 W", "hervidor de 2.000 W"],
          "En el mismo tiempo, más potencia significa más energía.", "Con igual tiempo, la energía crece con la potencia: 9, 60, 150, 1.200 y 2.000 W.")
    b.nu(5, "{personaje} usa una estufa de 2.000 W durante 3 horas. Si 1 kWh cuesta $200, ¿cuánto cuesta ese uso?", 1200,
         "2.000 W = 2 kW. Calcula los kWh y multiplica por el precio.", "2 kW × 3 h = 6 kWh; 6 × $200 = $1.200.", unidad="pesos")
    b.om(5, "Al conectar muchos aparatos potentes en un mismo enchufe, el automático se corta. ¿Por qué?",
         "cada aparato en paralelo suma corriente y el total supera el límite",
         ["el voltaje del enchufe sube a 1.000 V", "la resistencia total aumenta mucho", "los aparatos en paralelo se apagan entre sí"],
         "En paralelo, cada rama agrega su propia corriente.", "Las corrientes de cada aparato se suman: si superan el límite, el automático se corta para evitar un incendio.")
    b.om(5, "Una ampolleta LED de 10 W da la misma luz que una incandescente de 60 W. ¿Qué afirmación es correcta?",
         "la LED es más eficiente: desperdicia menos energía como calor",
         ["la incandescente es más eficiente porque consume más", "ambas son igual de eficientes porque dan la misma luz", "la LED consume 60 W y entrega 10 W"],
         "Eficiencia: cuánta energía se convierte en lo que buscas.", "La LED usa 10 W para la misma luz: aprovecha mejor la energía.")
    b.cat(5, "¿Ahorra energía o gasta más?", ["Ahorra energía", "Gasta más"],
          [("cambiar ampolletas por LED", 0), ("desenchufar cargadores sin uso", 0), ("elegir un refrigerador con etiqueta de eficiencia A", 0),
           ("dejar el televisor en espera toda la noche", 1), ("abrir seguido la puerta del refrigerador", 1), ("dejar luces encendidas en piezas vacías", 1)],
          "Piensa si se usa energía sin necesidad.", "LED, desenchufar y equipos eficientes ahorran; los aparatos en espera, el refrigerador abierto y las luces sin uso gastan.")
    return b.items


def cn08_oa11():
    b = Autor("cie", 8, 11)
    b.om(1, "¿Cómo se llama la transferencia de calor por contacto directo?", "conducción", ["convección", "radiación", "evaporación"],
         "Ocurre cuando dos cuerpos se tocan.", "Por contacto directo, el calor se transfiere por conducción.")
    b.co(1, "El calor siempre pasa del cuerpo más ___ al más frío.", "caliente", ["frío", "grande", "pesado"],
         "Piensa en una taza de té que se enfría.", "El calor fluye del cuerpo más caliente al más frío.")
    b.om(1, "¿Con qué instrumento se mide la temperatura?", "termómetro", ["barómetro", "amperímetro", "balanza"],
         "«Termo» significa calor.", "La temperatura se mide con un termómetro.")
    b.em(2, "Une cada forma de transferencia de calor con un ejemplo.",
         [["conducción", "una cuchara metálica se calienta en la sopa"], ["convección", "el agua de la olla circula al calentarse"], ["radiación", "el Sol calienta tu cara"]],
         "La radiación no necesita contacto ni un medio.", "Cuchara: conducción; agua que circula: convección; Sol: radiación.")
    b.cat(2, "¿Buen conductor o buen aislante del calor?", ["Buen conductor", "Buen aislante"],
          [("cobre", 0), ("aluminio", 0), ("acero", 0), ("lana", 1), ("madera", 1), ("corcho", 1)],
          "Los metales conducen bien el calor.", "Cobre, aluminio y acero conducen; lana, madera y corcho aíslan.")
    b.om(2, "¿Por qué las ollas tienen mangos de madera o plástico?", "porque son aislantes y no conducen bien el calor a la mano",
         ["porque conducen muy bien el calor", "para que la olla se caliente más rápido", "porque el metal es aislante"],
         "El mango es la parte que tomas.", "La madera y el plástico son aislantes: protegen tu mano del calor.")
    b.om(3, "¿Qué diferencia hay entre calor y temperatura?", "el calor es energía que se transfiere; la temperatura mide la agitación de las partículas",
         ["son exactamente lo mismo", "la temperatura es energía que pasa de un cuerpo a otro", "el calor se mide con termómetro en °C"],
         "Uno es energía en tránsito y el otro una medida.", "El calor es energía transferida; la temperatura indica cuánto se agitan las partículas.")
    b.co(3, "Sobre una estufa, el aire caliente sube y el aire frío baja: esa circulación es ___.", "convección", ["conducción", "radiación", "solidificación"],
         "Ocurre en líquidos y gases que se mueven.", "El movimiento de aire caliente y frío es convección.")
    b.cat(3, "¿Conducción, convección o radiación?", ["Conducción", "Convección", "Radiación"],
          [("planchar una polera", 0), ("tocar una baranda fría", 0), ("brisa marina en la costa", 1), ("agua que circula al hervir", 1),
           ("calor del Sol que llega a la Tierra", 2), ("calor de una fogata que sientes a distancia", 2)],
          "Contacto, movimiento de un fluido o sin contacto.", "Plancha y baranda: conducción; brisa y agua: convección; Sol y fogata: radiación.")
    b.nu(4, "Mezclas 1 L de agua a 80 °C con 1 L de agua a 20 °C. Sin pérdidas de calor, ¿qué temperatura final alcanzan?", 50,
         "Con cantidades iguales, la temperatura final queda justo al medio.", "(80 + 20) ÷ 2 = 50 °C: equilibrio térmico.", unidad="°C")
    b.om(4, "Dejas una taza de té a 70 °C en una pieza a 20 °C. ¿Qué pasa después de mucho rato?", "el té queda a unos 20 °C, igual que la pieza",
         ["el té se queda a 70 °C", "la pieza sube a 70 °C", "el té baja a 0 °C"],
         "El calor pasa hasta que no haya diferencia de temperatura.", "El té cede calor hasta alcanzar el equilibrio térmico con la pieza.")
    b.ord(4, "Ordena lo que pasa al poner una cuchara fría en sopa caliente.",
          ["Pones la cuchara fría en la sopa.", "Las partículas de la sopa chocan con las de la cuchara.", "La cuchara se calienta y la sopa se enfría un poco.", "Ambas llegan a la misma temperatura."],
          "El calor pasa por contacto hasta igualar temperaturas.", "Contacto → choques de partículas → transferencia de calor → equilibrio térmico.")
    b.nu(5, "{personaje} mezcla 2 L de agua a 80 °C con 1 L a 20 °C. Sin pérdidas, ¿qué temperatura final alcanzan?", 60,
         "Hay el doble de agua caliente: el resultado queda más cerca de 80.", "(2 × 80 + 1 × 20) ÷ 3 = 180 ÷ 3 = 60 °C.", unidad="°C")
    b.om(5, "Un termo mantiene el café caliente por horas. ¿Cómo lo logra?", "sus paredes con vacío y superficie plateada reducen conducción, convección y radiación",
         ["produce calor con una pila", "solo evita la radiación", "su vidrio es buen conductor del calor"],
         "Piensa en las tres formas de transferencia.", "El vacío frena la conducción y la convección; lo plateado refleja la radiación.")
    b.om(5, "En una mañana fría tocas una baranda de metal y una banca de madera, ambas a la misma temperatura. El metal se siente más frío. ¿Por qué?",
         "el metal conduce más rápido el calor de tu mano", ["el metal está a menor temperatura", "la madera produce calor", "el frío pasa del metal a tu mano"],
         "Ambas están a la misma temperatura; cambia la rapidez con que sacan calor.", "El metal es buen conductor: saca calor de tu mano más rápido y lo sientes más frío.")
    b.co(5, "Para que una casa en Punta Arenas pierda menos calor en invierno, sus muros deben tener un buen material ___.", "aislante",
         ["conductor", "metálico", "transparente"],
         "Se busca frenar la salida del calor.", "Un material aislante reduce la conducción de calor hacia afuera.")
    return b.items


def cn08_oa12():
    b = Autor("cie", 8, 12)
    b.om(1, "¿Quién propuso que la materia está formada por átomos indivisibles, como esferas macizas?", "John Dalton",
         ["Niels Bohr", "Ernest Rutherford", "J. J. Thomson"],
         "Fue el primer modelo atómico científico.", "Dalton propuso átomos indivisibles, como esferas macizas.")
    b.om(1, "¿Qué partícula descubrió Thomson?", "el electrón", ["el protón", "el neutrón", "el núcleo"],
         "Tiene carga negativa.", "Thomson descubrió el electrón, de carga negativa.")
    b.co(1, "Thomson imaginó el átomo como un budín con pasas: una esfera positiva con ___ incrustados.", "electrones",
         ["protones", "neutrones", "núcleos"],
         "Las pasas tienen carga negativa.", "En el modelo de Thomson, los electrones están incrustados en una esfera positiva.")
    b.ord(2, "Ordena los modelos atómicos del más antiguo al más reciente.", ["Dalton", "Thomson", "Rutherford", "Bohr"],
          "El modelo de Bohr corrigió al de Rutherford.", "Dalton (1808), Thomson (1904), Rutherford (1911) y Bohr (1913).")
    b.em(2, "Une cada científico con su modelo.",
         [["Dalton", "esfera maciza e indivisible"], ["Thomson", "esfera positiva con electrones incrustados"],
          ["Rutherford", "núcleo pequeño y positivo con electrones alrededor"], ["Bohr", "electrones en órbitas de energía definida"]],
         "Cada modelo agregó una idea nueva.", "Dalton: esfera maciza; Thomson: budín con pasas; Rutherford: núcleo; Bohr: órbitas de energía.")
    b.om(2, "¿Qué descubrió Rutherford?", "que el átomo tiene un núcleo pequeño, denso y positivo",
         ["que el átomo es indivisible", "el electrón", "que los electrones están en niveles de energía fijos"],
         "Lo descubrió con una lámina de oro.", "Rutherford descubrió el núcleo atómico: pequeño, denso y positivo.")
    b.om(3, "En el experimento de Rutherford se lanzaron partículas alfa contra una lámina de oro muy delgada. ¿Qué pasó con la mayoría?",
         "atravesaron la lámina sin desviarse", ["rebotaron todas", "se quedaron pegadas al oro", "se desviaron todas"],
         "El resultado mostró que el átomo es casi vacío.", "La mayoría pasó derecho: el átomo es casi todo espacio vacío.")
    b.co(3, "Como la mayoría de las partículas alfa atravesó la lámina, Rutherford concluyó que el átomo es casi todo ___.", "espacio vacío",
         ["materia sólida", "carga positiva repartida", "electrones"],
         "Si casi nada choca, ¿qué hay dentro?", "Si casi todas pasan sin chocar, el átomo es casi todo espacio vacío.")
    b.cat(3, "¿Qué científico propuso cada idea?", ["Dalton", "Thomson", "Rutherford"],
          [("los átomos de un mismo elemento son iguales", 0), ("los átomos se combinan en proporciones fijas", 0),
           ("el átomo tiene electrones negativos", 1), ("la carga positiva está repartida en toda la esfera", 1),
           ("la carga positiva está concentrada en un núcleo", 2), ("el átomo es en su mayor parte vacío", 2)],
          "Dalton no conocía partículas dentro del átomo.", "Dalton habló de átomos iguales y combinaciones; Thomson, de electrones; Rutherford, del núcleo y el vacío.")
    b.om(4, "¿Qué evidencia llevó a Thomson a descubrir el electrón?", "experimentos con rayos catódicos en tubos de vacío",
         ["el bombardeo de una lámina de oro", "los colores de la luz que emite el hidrógeno", "el peso de los gases al reaccionar"],
         "Usó tubos de vidrio con electricidad.", "Thomson estudió los rayos catódicos y mostró que eran partículas negativas: electrones.")
    b.om(4, "¿Por qué Bohr modificó el modelo de Rutherford?", "para explicar la luz que emiten los átomos, con electrones en órbitas de energía fija",
         ["porque Rutherford negó que existiera el núcleo", "para demostrar que el átomo es indivisible", "porque descubrió que el átomo no tiene electrones"],
         "Bohr estudió la luz del hidrógeno.", "Bohr propuso órbitas con energía definida para explicar los colores de luz que emiten los átomos.")
    b.em(4, "Une cada científico con la evidencia que usó.",
         [["Dalton", "cómo se combinan las sustancias"], ["Thomson", "rayos catódicos"], ["Rutherford", "lámina de oro y partículas alfa"], ["Bohr", "luz emitida por el hidrógeno"]],
         "Dalton trabajó con reacciones químicas, no con partículas.", "Dalton: combinaciones; Thomson: rayos catódicos; Rutherford: lámina de oro; Bohr: luz del hidrógeno.")
    b.nu(4, "Dalton publicó su teoría atómica en 1808 y Bohr presentó su modelo en 1913. ¿Cuántos años pasaron entre ambos?", 105,
         "Resta el año más antiguo al más reciente.", "1913 − 1808 = 105 años.", unidad="años")
    b.om(5, "Si el núcleo de un átomo fuera una bolita en el centro de un estadio, ¿dónde estarían los electrones?",
         "en las graderías, muy lejos del núcleo", ["pegados a la bolita", "dentro de la bolita", "repartidos en una esfera maciza"],
         "Recuerda que el átomo es casi todo vacío.", "El núcleo es diminuto y los electrones están muy lejos: el átomo es casi todo vacío.")
    b.om(5, "Algunas partículas alfa rebotaron en la lámina de oro. Según el modelo de Thomson, eso no debía pasar. ¿Por qué?",
         "porque en ese modelo la carga positiva estaba repartida y no podía desviarlas tanto",
         ["porque Thomson decía que el átomo era vacío", "porque Thomson no conocía los electrones", "porque el oro no tiene átomos"],
         "Para que una partícula rebote, debe chocar con algo concentrado.", "Una carga positiva repartida no hace rebotar partículas; un núcleo concentrado sí.")
    b.ord(5, "Ordena cómo cambió la idea de átomo a lo largo del tiempo.",
          ["El átomo es indivisible.", "Se descubre el electrón: el átomo tiene partes.", "Se descubre un núcleo positivo y pequeño.", "Los electrones ocupan niveles de energía."],
          "Cada idea corrigió a la anterior con nueva evidencia.", "Dalton → Thomson (electrón) → Rutherford (núcleo) → Bohr (niveles de energía).")
    b.cat(5, "De la teoría de Dalton, ¿qué idea sigue vigente y cuál fue corregida?", ["Sigue vigente", "Fue corregida"],
          [("la materia está formada por átomos", 0), ("en una reacción los átomos se reordenan, no se destruyen", 0),
           ("los átomos se combinan en proporciones definidas", 0), ("el átomo es indivisible", 1), ("el átomo es una esfera maciza sin partes", 1)],
          "Thomson y Rutherford encontraron partes dentro del átomo.", "Los átomos y sus combinaciones siguen vigentes; la indivisibilidad y la esfera maciza fueron corregidas.")
    return b.items


GENERADORES = {
    "5_basico.ciencias.OA1": cn05_oa1, "5_basico.ciencias.OA8": cn05_oa8, "5_basico.ciencias.OA10": cn05_oa10,
    "6_basico.ciencias.OA1": cn06_oa1, "6_basico.ciencias.OA8": cn06_oa8, "6_basico.ciencias.OA13": cn06_oa13,
    "7_basico.ciencias.OA8": cn07_oa8, "7_basico.ciencias.OA13": cn07_oa13, "7_basico.ciencias.OA14": cn07_oa14,
    "8_basico.ciencias.OA10": cn08_oa10, "8_basico.ciencias.OA11": cn08_oa11, "8_basico.ciencias.OA12": cn08_oa12,
}
