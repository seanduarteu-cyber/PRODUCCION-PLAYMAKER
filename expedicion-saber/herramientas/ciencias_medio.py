"""Ciencias 1° a 4° medio: 15 desafíos por OA (3 por nivel de dificultad, 1 a 5).
1° y 2° medio: Ciencias Naturales (Biología, Física, Química). 3° y 4° medio: Ciencias para la Ciudadanía."""
from autor import Autor


# ---------------- 1° medio ----------------
def cn1m_oa2():
    b = Autor("cie", "1m", 2)
    b.om(1, "¿Quiénes propusieron la teoría de la evolución por selección natural?", "Charles Darwin y Alfred Wallace", ["Isaac Newton y Galileo", "Gregor Mendel y Pasteur", "Marie Curie y Bohr"], "Uno de ellos viajó en el Beagle.", "Darwin y Wallace propusieron la selección natural.")
    b.co(1, "Los restos o huellas de organismos antiguos conservados en rocas se llaman ___.", "fósiles", ["minerales", "células", "genes"], "Son evidencia del pasado.", "Los fósiles son evidencia de seres vivos antiguos.")
    b.om(1, "¿Qué significa que los organismos «evolucionan»?", "que las poblaciones cambian a lo largo de muchas generaciones", ["que un individuo cambia en un día", "que todos los seres vivos son iguales", "que los animales eligen cambiar"], "La evolución ocurre en poblaciones, no en un individuo.", "Las poblaciones cambian a través de generaciones.")
    b.cat(2, "¿Es evidencia de la evolución?", ["Evidencia de evolución", "No es evidencia"], [("registro fósil", 0), ("estructuras homólogas", 0), ("similitudes en el ADN", 0), ("el color favorito de una persona", 1), ("la forma de las nubes", 1)],
          "Piensa en lo que muestra un ancestro común.", "Fósiles, homologías y ADN son evidencias; los gustos y las nubes no.")
    b.om(2, "El brazo humano, el ala del murciélago y la aleta de la ballena tienen los mismos huesos básicos. Son estructuras…", "homólogas", ["análogas", "vestigiales", "artificiales"], "Mismo origen, distinta función.", "Tienen el mismo origen evolutivo: son homólogas.")
    b.co(2, "En la selección natural, los individuos con características ___ sobreviven y se reproducen más.", "ventajosas", ["inútiles", "iguales", "dañinas"], "Piensa en la adaptación al ambiente.", "Las características ventajosas aumentan la supervivencia.")
    b.ord(3, "Ordena los pasos de la selección natural.", ["Hay variación entre individuos.", "Algunas variantes sobreviven mejor.", "Esos individuos se reproducen más.", "La característica se vuelve más común en la población."],
          "Variación → supervivencia → reproducción → cambio en la población.", "Así cambia la frecuencia de una característica.")
    b.om(3, "¿Por qué el uso excesivo de antibióticos genera bacterias resistentes?", "porque sobreviven y se reproducen las bacterias que ya eran resistentes", ["porque los antibióticos enseñan a las bacterias", "porque las bacterias se vuelven más grandes", "porque los antibióticos crean bacterias nuevas"], "Piensa en selección natural.", "El antibiótico elimina a las sensibles y deja a las resistentes.")
    b.em(3, "Une cada término con su definición.", [["adaptación", "característica que aumenta la supervivencia"], ["especie", "grupo que puede reproducirse y tener descendencia fértil"], ["mutación", "cambio en el ADN"]], "Vocabulario de evolución.", "Adaptación, especie y mutación.")
    b.om(4, "Las polillas oscuras aumentaron en Inglaterra cuando el hollín oscureció los árboles. ¿Por qué?", "las aves veían menos a las polillas oscuras sobre los troncos", ["el hollín pintó a las polillas", "las polillas claras se volvieron oscuras", "las aves preferían las polillas claras por su sabor"], "Piensa en el camuflaje.", "Las oscuras se camuflaban mejor y sobrevivían más.")
    b.om(4, "¿Qué diferencia a Darwin de Lamarck?", "Darwin explicó el cambio por selección natural; Lamarck, por uso y herencia de lo adquirido", ["Darwin creía que las especies no cambian", "Lamarck descubrió el ADN", "No hay diferencia"], "Lamarck pensaba que el cuello de la jirafa se alargaba por estirarlo.", "Lamarck: herencia de caracteres adquiridos; Darwin: selección natural.")
    b.cat(4, "¿Explicación de Darwin o de Lamarck?", ["Darwin", "Lamarck"], [("Las jirafas de cuello largo alcanzaban más alimento y dejaban más crías.", 0), ("Hay variación y el ambiente selecciona.", 0), ("La jirafa estiró su cuello y se lo heredó a sus crías.", 1), ("El uso desarrolla un órgano y ese cambio se hereda.", 1)],
          "Lamarck habla de uso y desuso.", "Selección de variantes: Darwin; uso y herencia de lo adquirido: Lamarck.")
    b.om(5, "En las islas Galápagos, los pinzones tienen picos distintos según su alimento. ¿Qué explica mejor esto?", "poblaciones de un ancestro común se adaptaron a recursos diferentes", ["cada pinzón eligió su pico", "los picos cambian cada semana", "son aves sin relación entre sí"], "Piensa en ancestro común y ambientes distintos.", "Un ancestro común dio origen a especies adaptadas a cada alimento.")
    b.om(5, "Si dos especies tienen ADN muy parecido, lo más probable es que…", "compartan un ancestro común reciente", ["vivan en el mismo país", "tengan el mismo tamaño", "no estén emparentadas"], "El ADN funciona como un registro del parentesco.", "Más similitud genética indica parentesco más cercano.")
    b.ord(5, "Ordena del más antiguo al más reciente según el registro fósil.", ["bacterias", "peces", "reptiles", "mamíferos"], "Las formas simples aparecen primero.", "Bacterias, peces, reptiles y mamíferos, en ese orden.")
    return b.items


def cn1m_oa9():
    b = Autor("cie", "1m", 9)
    b.om(1, "¿Qué transportan las ondas?", "energía", ["materia", "agua siempre", "aire siempre"], "Las ondas no trasladan la materia de un lugar a otro.", "Las ondas transportan energía, no materia.")
    b.co(1, "La cantidad de oscilaciones por segundo se llama ___.", "frecuencia", ["amplitud", "longitud de onda", "rapidez"], "Se mide en hertz (Hz).", "La frecuencia se mide en Hz.")
    b.cat(1, "¿Onda mecánica o electromagnética?", ["Mecánica", "Electromagnética"], [("sonido", 0), ("ola del mar", 0), ("onda sísmica", 0), ("luz", 1), ("ondas de radio", 1), ("rayos X", 1)],
          "Las mecánicas necesitan un medio; las electromagnéticas viajan en el vacío.", "Sonido, olas y sismos son mecánicas; luz, radio y rayos X, electromagnéticas.")
    b.om(2, "La distancia entre dos crestas consecutivas es la…", "longitud de onda", ["amplitud", "frecuencia", "rapidez"], "Se representa con λ.", "Es la longitud de onda (λ).")
    b.om(2, "En el espacio no se escucha el sonido porque…", "el sonido necesita un medio material para propagarse", ["no hay luz", "hace mucho frío", "el sonido es muy rápido"], "¿Qué tipo de onda es el sonido?", "Es una onda mecánica: en el vacío no se propaga.")
    b.em(2, "Une cada fenómeno con su nombre.", [["el eco", "reflexión"], ["un lápiz que parece quebrado en el agua", "refracción"], ["una cortina que reduce el ruido", "absorción"]], "Piensa qué le pasa a la onda en cada caso.", "Rebotar es reflexión; cambiar de medio, refracción; quedar retenida, absorción.")
    b.nu(3, "Una onda tiene frecuencia 4 Hz y longitud de onda 3 m. ¿Cuál es su rapidez, en m/s? (v = λ · f)", 12, "Multiplica λ por f.", "v = 3 · 4 = 12 m/s.", unidad="m/s")
    b.nu(3, "Una onda viaja a 20 m/s con frecuencia 5 Hz. ¿Cuánto mide su longitud de onda, en metros?", 4, "λ = v ÷ f.", "λ = 20 ÷ 5 = 4 m.", unidad="m")
    b.om(3, "Un sonido más agudo tiene…", "mayor frecuencia", ["mayor amplitud", "menor frecuencia", "menor rapidez siempre"], "El tono depende de la frecuencia.", "Los sonidos agudos tienen mayor frecuencia.")
    b.cat(4, "¿Onda transversal o longitudinal?", ["Transversal", "Longitudinal"], [("una cuerda que se agita hacia arriba y abajo", 0), ("la luz", 0), ("el sonido en el aire", 1), ("un resorte que se comprime y se estira", 1)],
          "Transversal: vibra perpendicular a la dirección de avance; longitudinal: en la misma dirección.", "Cuerda y luz son transversales; sonido y resorte, longitudinales.")
    b.om(4, "Si subes el volumen de un parlante, cambia principalmente la…", "amplitud", ["frecuencia", "longitud de onda", "rapidez del sonido"], "El volumen se relaciona con la energía de la onda.", "Más volumen es más amplitud.")
    b.nu(4, "Un murciélago emite un sonido que vuelve en 0,2 s. Si el sonido viaja a 340 m/s, ¿a cuántos metros está el obstáculo?", 34, "El sonido va y vuelve: la distancia es la mitad del recorrido.", "340 · 0,2 = 68 m de ida y vuelta: el obstáculo está a 34 m.", unidad="m")
    b.om(5, "En un sismo llegan primero las ondas P y luego las S. ¿Qué indica la diferencia de tiempo?", "la distancia al epicentro", ["la hora del día", "la temperatura del suelo", "la profundidad del mar"], "Viajan a distinta rapidez.", "Mientras más tiempo entre P y S, más lejos está el epicentro.")
    b.om(5, "La luz pasa del aire al agua y se desvía. ¿Por qué?", "cambia su rapidez al cambiar de medio", ["el agua absorbe toda la luz", "la luz rebota en el agua", "la frecuencia se duplica"], "Así funciona la refracción.", "Al cambiar de medio cambia la rapidez y la luz se desvía.")
    b.ord(5, "Ordena de menor a mayor frecuencia.", ["ondas de radio", "microondas", "luz visible", "rayos X"], "Piensa en el espectro electromagnético.", "Radio < microondas < luz visible < rayos X.")
    return b.items


def cn1m_oa18():
    b = Autor("cie", "1m", 18)
    b.om(1, "¿Qué dice la ley de conservación de la masa?", "en una reacción química la masa total no cambia", ["la masa siempre aumenta", "la masa desaparece al quemar algo", "solo se conserva el agua"], "Lavoisier: «nada se pierde, nada se crea…».", "La masa de los reactivos es igual a la de los productos.")
    b.co(1, "Las sustancias que reaccionan se llaman ___.", "reactivos", ["productos", "catalizadores", "soluciones"], "Están a la izquierda de la flecha.", "Los reactivos están antes de la flecha.")
    b.om(1, "¿Quién formuló la ley de conservación de la masa?", "Antoine Lavoisier", ["Charles Darwin", "Isaac Newton", "Gregor Mendel"], "Químico francés del siglo XVIII.", "Fue Lavoisier.")
    b.cat(2, "¿Cambio químico o físico?", ["Cambio químico", "Cambio físico"], [("quemar papel", 0), ("oxidarse un clavo", 0), ("cocinar un huevo", 0), ("derretir hielo", 1), ("cortar madera", 1), ("disolver azúcar", 1)],
          "En un cambio químico se forman sustancias nuevas.", "Quemar, oxidar y cocinar forman sustancias nuevas; los otros solo cambian forma o estado.")
    b.nu(2, "Reaccionan 10 g de una sustancia con 6 g de otra y se forma un solo producto. ¿Cuántos gramos de producto se forman?", 16, "La masa se conserva.", "10 + 6 = 16 g.", unidad="g")
    b.om(2, "En la ecuación 2 H₂ + O₂ → 2 H₂O, ¿cuántos átomos de hidrógeno hay en los reactivos?", 4, [2, 6, 8], "2 moléculas de H₂ tienen 2 átomos cada una.", "2 · 2 = 4 átomos de hidrógeno.")
    b.co(3, "Para balancear H₂ + Cl₂ → ___ HCl, el coeficiente del HCl es…", "2", ["1", "3", "4"], "Cuenta los átomos de H y de Cl a cada lado.", "H₂ + Cl₂ → 2 HCl: 2 H y 2 Cl a cada lado.")
    b.nu(3, "Al quemar 12 g de carbono con 32 g de oxígeno se forma dióxido de carbono. ¿Cuántos gramos de CO₂ se forman?", 44, "Suma las masas de los reactivos.", "12 + 32 = 44 g de CO₂.", unidad="g")
    b.om(3, "Un trozo de leña pesa 2 kg y las cenizas, 0,1 kg. ¿Por qué no se cumple aparentemente la ley?", "porque se liberaron gases como CO₂ y vapor de agua que no se pesaron", ["porque la masa se destruyó", "porque el fuego crea masa", "porque la balanza estaba mala"], "En un sistema abierto se escapan gases.", "La masa faltante salió como gases.")
    b.em(4, "Une cada grupo de reactivos con sus productos balanceados.", [["N₂ + 3 H₂ →", "2 NH₃"], ["2 Na + Cl₂ →", "2 NaCl"], ["C + O₂ →", "CO₂"]],
         "Cuenta los átomos a cada lado.", "N₂ + 3 H₂ → 2 NH₃; 2 Na + Cl₂ → 2 NaCl; C + O₂ → CO₂.")
    b.om(4, "¿Qué ecuación está balanceada?", "CH₄ + 2 O₂ → CO₂ + 2 H₂O", ["CH₄ + O₂ → CO₂ + H₂O", "CH₄ + 2 O₂ → CO₂ + H₂O", "CH₄ + O₂ → 2 CO₂ + 2 H₂O"], "Cuenta C, H y O en cada lado.", "1 C, 4 H y 4 O a cada lado.")
    b.ord(4, "Ordena los pasos para balancear una ecuación.", ["Escribir reactivos y productos.", "Contar los átomos de cada elemento.", "Ajustar coeficientes.", "Verificar que los átomos sean iguales a cada lado."], "Primero escribir, luego contar, ajustar y comprobar.", "Ese es el procedimiento para balancear.")
    b.nu(5, "En un frasco cerrado se mezclan 50 g de vinagre y 5 g de bicarbonato. La reacción produce gas que queda dentro. ¿Cuánto pesa el frasco con su contenido, si vacío pesa 200 g?", 255, "En un sistema cerrado la masa total no cambia.", "200 + 50 + 5 = 255 g.", unidad="g")
    b.om(5, "¿Por qué Lavoisier realizaba sus experimentos en recipientes cerrados?", "para no perder gases y medir toda la masa", ["para que no entrara luz", "para que fueran más rápidos", "para que no los vieran otros científicos"], "¿Qué se escapa en un recipiente abierto?", "Así incluía los gases en la medición de la masa.")
    b.cat(5, "En 2 H₂O → 2 H₂ + O₂, ¿cuántos átomos hay de cada elemento en los productos?", ["4 átomos", "2 átomos"], [("hidrógeno", 0), ("oxígeno", 1), ("hidrógeno en los reactivos", 0), ("oxígeno en los reactivos", 1)],
          "Multiplica coeficiente por subíndice.", "Hay 4 H y 2 O a cada lado: la ecuación está balanceada.")
    return b.items


# ---------------- 2° medio ----------------
def cn2m_oa7():
    b = Autor("cie", "2m", 7)
    b.om(1, "¿Quién es considerado el padre de la genética?", "Gregor Mendel", ["Charles Darwin", "Louis Pasteur", "Robert Hooke"], "Experimentó con arvejas.", "Mendel estudió la herencia en arvejas.")
    b.co(1, "Las distintas formas de un mismo gen se llaman ___.", "alelos", ["cromosomas", "células", "proteínas"], "Por ejemplo, A y a.", "A y a son alelos de un gen.")
    b.cat(1, "¿Homocigoto o heterocigoto?", ["Homocigoto", "Heterocigoto"], [("AA", 0), ("aa", 0), ("BB", 0), ("Aa", 1), ("Bb", 1)], "Homocigoto: dos alelos iguales.", "AA, aa y BB son homocigotos; Aa y Bb, heterocigotos.")
    b.om(2, "Si A (semilla amarilla) es dominante sobre a (verde), ¿de qué color es una planta Aa?", "amarilla", ["verde", "amarilla y verde a rayas", "blanca"], "El alelo dominante se expresa.", "Aa muestra el rasgo dominante: amarilla.")
    b.em(2, "Une cada término con su definición.", [["genotipo", "combinación de alelos"], ["fenotipo", "característica observable"], ["dominante", "alelo que se expresa en el heterocigoto"]], "Genotipo: letras; fenotipo: lo que se ve.", "Genotipo, fenotipo y dominante.")
    b.om(2, "¿Qué genotipo tiene una planta de semilla verde si verde es recesivo (a)?", "aa", ["AA", "Aa", "aA"], "Un rasgo recesivo solo aparece con dos alelos recesivos.", "Solo aa muestra el rasgo recesivo.")
    b.nu(3, "Cruzas Aa × Aa. De cada 4 descendientes, en promedio, ¿cuántos muestran el rasgo dominante?", 3, "Haz un cuadro de Punnett: AA, Aa, Aa, aa.", "3 de 4 tienen al menos una A: proporción 3:1.")
    b.om(3, "En el cruce Aa × aa, ¿qué proporción de la descendencia es aa?", "1/2", ["1/4", "3/4", "0"], "Cuadro de Punnett: Aa, Aa, aa, aa.", "2 de 4 son aa: la mitad.")
    b.co(3, "Al cruzar AA × aa, todos los hijos son ___.", "Aa", ["AA", "aa", "AA y aa"], "Cada padre aporta un alelo.", "Uno aporta A y el otro a: todos son Aa.")
    b.ord(4, "Ordena los pasos para resolver un cruce con un cuadro de Punnett.", ["Escribir el genotipo de los padres.", "Separar los gametos de cada padre.", "Combinar los gametos en el cuadro.", "Contar las proporciones de genotipos y fenotipos."], "Padres, gametos, cuadro y conteo.", "Ese es el procedimiento del cuadro de Punnett.")
    b.om(4, "Dos padres de ojos cafés (dominante) tienen un hijo de ojos azules (recesivo). ¿Cuál es el genotipo de los padres?", "ambos heterocigotos (Cc)", ["ambos CC", "uno CC y otro cc", "ambos cc"], "El hijo cc recibió un alelo c de cada padre.", "Ambos deben portar el alelo c: son Cc.")
    b.nu(4, "En un cruce dihíbrido AaBb × AaBb, de 16 descendientes, ¿cuántos muestran ambos rasgos dominantes?", 9, "Proporción 9:3:3:1.", "9 de 16 muestran ambos rasgos dominantes.")
    b.om(5, "¿Qué proporción fenotípica se espera en un cruce AaBb × AaBb?", "9:3:3:1", ["3:1", "1:1", "1:2:1"], "Es un cruce dihíbrido.", "Mendel obtuvo 9:3:3:1 en cruces dihíbridos.")
    b.om(5, "Una planta de flor morada puede ser MM o Mm. ¿Qué cruce te permite saber su genotipo?", "cruzarla con una planta mm (cruce de prueba)", ["cruzarla con otra MM", "mirarla con lupa", "regarla más"], "Si aparece un hijo mm, era Mm.", "El cruce de prueba con mm revela si hay un alelo recesivo oculto.")
    b.cat(5, "¿Qué principio de Mendel describe cada idea?", ["Segregación", "Distribución independiente"], [("Los dos alelos de un gen se separan al formar gametos.", 0), ("Cada gameto lleva un solo alelo de cada gen.", 0), ("El color de la semilla se hereda sin depender de su forma.", 1), ("Genes de rasgos distintos se combinan al azar.", 1)],
          "Segregación: un gen; distribución independiente: varios genes.", "Las dos primeras hablan de un gen; las otras, de genes distintos.")
    return b.items


def cn2m_oa9():
    b = Autor("cie", "2m", 9)
    b.om(1, "¿Qué es un sistema de referencia?", "el punto desde el cual se describe un movimiento", ["la velocidad máxima de un auto", "un tipo de energía", "el peso de un objeto"], "El movimiento depende de quién lo observa.", "Es el punto o lugar desde donde se mide la posición.")
    b.co(1, "En el movimiento rectilíneo uniforme (MRU), la velocidad es ___.", "constante", ["cero siempre", "cada vez mayor", "negativa siempre"], "Uniforme significa sin cambios.", "En el MRU la velocidad no cambia.")
    b.nu(1, "Un ciclista recorre 30 m en 6 s con velocidad constante. ¿Cuál es su rapidez, en m/s?", 5, "v = d ÷ t.", "30 ÷ 6 = 5 m/s.", unidad="m/s")
    b.om(2, "Vas sentado en un bus en movimiento. Respecto de tu asiento, tú estás…", "en reposo", ["moviéndote rápido", "acelerando siempre", "cayendo"], "Depende del sistema de referencia.", "Respecto del asiento no cambias de posición.")
    b.nu(2, "Un auto viaja a 20 m/s durante 10 s. ¿Cuántos metros recorre?", 200, "d = v · t.", "20 · 10 = 200 m.", unidad="m")
    b.em(2, "Une cada magnitud con su unidad en el SI.", [["posición", "m"], ["velocidad", "m/s"], ["aceleración", "m/s²"]], "Piensa en cómo se calcula cada una.", "Posición en metros, velocidad en m/s y aceleración en m/s².")
    b.nu(3, "Un auto pasa de 0 a 20 m/s en 4 s. ¿Cuál es su aceleración, en m/s²?", 5, "a = Δv ÷ Δt.", "(20 − 0) ÷ 4 = 5 m/s².", unidad="m/s²")
    b.om(3, "¿Cuál es la diferencia entre distancia y desplazamiento?", "la distancia es el camino total; el desplazamiento es el cambio de posición", ["son exactamente lo mismo", "el desplazamiento siempre es mayor", "la distancia tiene dirección"], "Si das una vuelta completa, ¿cuánto te desplazaste?", "Una vuelta completa tiene distancia, pero desplazamiento cero.")
    b.cat(3, "¿MRU o MRUA?", ["MRU (velocidad constante)", "MRUA (velocidad que cambia)"], [("un tren a 80 km/h constantes", 0), ("una persona que camina siempre igual", 0), ("un auto que frena en un semáforo", 1), ("una pelota que cae", 1)],
          "¿La velocidad cambia o no?", "Velocidad constante: MRU; si acelera o frena: MRUA.")
    b.nu(4, "Una corredora da una vuelta completa a una pista de 400 m y vuelve al punto de partida. ¿Cuál es su desplazamiento, en metros?", 0, "Compara la posición inicial con la final.", "Termina donde empezó: el desplazamiento es 0 m.", unidad="m")
    b.om(4, "Un auto frena de 30 m/s a 10 m/s en 5 s. ¿Cuál es su aceleración?", "−4 m/s²", ["4 m/s²", "−8 m/s²", "8 m/s²"], "a = (v final − v inicial) ÷ t.", "(10 − 30) ÷ 5 = −4 m/s²: va frenando.")
    b.ord(4, "Ordena de menor a mayor rapidez.", ["una persona caminando (1,5 m/s)", "un ciclista (6 m/s)", "un auto en la ciudad (14 m/s)", "un avión (250 m/s)"], "Compara los números en m/s.", "1,5 < 6 < 14 < 250 m/s.")
    b.nu(5, "Un bus parte del reposo con aceleración 2 m/s². ¿Qué velocidad tiene después de 7 s, en m/s?", 14, "v = v₀ + a · t.", "0 + 2 · 7 = 14 m/s.", unidad="m/s")
    b.nu(5, "Un objeto parte del reposo y acelera a 2 m/s² durante 5 s. ¿Qué distancia recorre, en metros? (d = a · t² ÷ 2)", 25, "t² = 25.", "2 · 25 ÷ 2 = 25 m.", unidad="m")
    b.om(5, "En un gráfico posición-tiempo, una recta horizontal indica que el objeto…", "está detenido", ["acelera", "se mueve con rapidez constante", "va cada vez más rápido"], "La posición no cambia con el tiempo.", "Si la posición no cambia, está en reposo.")
    return b.items


def cn2m_oa15():
    b = Autor("cie", "2m", 15)
    b.om(1, "En una solución de agua con sal, ¿cuál es el soluto?", "la sal", ["el agua", "el vaso", "el aire"], "El soluto está en menor cantidad y se disuelve.", "La sal es el soluto; el agua, el solvente.")
    b.co(1, "La sustancia que disuelve y está en mayor cantidad se llama ___.", "solvente", ["soluto", "precipitado", "catalizador"], "El agua suele cumplir este papel.", "El solvente disuelve al soluto.")
    b.cat(1, "¿Es una solución (mezcla homogénea)?", ["Solución", "No es solución"], [("agua con azúcar disuelta", 0), ("aire", 0), ("bebida gaseosa", 0), ("agua con arena", 1), ("ensalada", 1)],
          "En una solución no se distinguen sus componentes.", "Agua azucarada, aire y bebida son soluciones; agua con arena y ensalada, no.")
    b.om(2, "¿Qué es una solución saturada?", "la que ya no puede disolver más soluto a esa temperatura", ["la que tiene poco soluto", "la que no tiene solvente", "la que es de color oscuro"], "Si agregas más, se queda en el fondo.", "Ya contiene el máximo de soluto que puede disolver.")
    b.em(2, "Une cada solución con su estado físico.", [["aire", "gaseosa"], ["agua de mar", "líquida"], ["bronce (aleación)", "sólida"]], "Las soluciones pueden ser sólidas, líquidas o gaseosas.", "Aire: gas; agua de mar: líquida; bronce: sólida.")
    b.om(2, "Si aumentas la temperatura del agua, generalmente puedes disolver…", "más azúcar", ["menos azúcar", "nada de azúcar", "la misma cantidad siempre"], "Piensa en preparar té con azúcar.", "La solubilidad de muchos sólidos aumenta con la temperatura.")
    b.nu(3, "Se disuelven 20 g de sal en 80 g de agua. ¿Cuál es el % m/m de la solución?", 20, "% m/m = masa de soluto ÷ masa de solución · 100. La solución pesa 100 g.", "20 ÷ 100 · 100 = 20 %.", unidad="%")
    b.nu(3, "¿Cuántos gramos de azúcar hay en 200 g de una solución al 10 % m/m?", 20, "10 % de 200.", "0,10 · 200 = 20 g.", unidad="g")
    b.co(3, "Diluir una solución significa agregar más ___.", "solvente", ["soluto", "calor", "sal"], "Diluir baja la concentración.", "Se agrega solvente y la concentración baja.")
    b.nu(4, "Tienes 100 mL de jugo concentrado al 40 % y agregas agua hasta 200 mL. ¿Cuál es la nueva concentración, en %?", 20, "La cantidad de soluto no cambia: el volumen se duplica.", "Al duplicar el volumen, la concentración baja a la mitad: 20 %.", unidad="%")
    b.om(4, "¿Qué solución está más concentrada?", "10 g de sal en 50 mL", ["10 g de sal en 100 mL", "5 g de sal en 100 mL", "10 g de sal en 500 mL"], "Compara la cantidad de soluto por volumen.", "10 g en 50 mL equivalen a 20 g por cada 100 mL: la mayor concentración.")
    b.ord(4, "Ordena de más diluida a más concentrada.", ["2 g en 100 mL", "5 g en 100 mL", "10 g en 100 mL", "20 g en 100 mL"], "Mismo volumen: compara gramos.", "2 < 5 < 10 < 20 g por cada 100 mL.")
    b.nu(5, "Necesitas 500 mL de suero al 1 % m/v. ¿Cuántos gramos de soluto necesitas?", 5, "1 % m/v = 1 g por cada 100 mL.", "500 mL · 1 g/100 mL = 5 g.", unidad="g")
    b.om(5, "Al abrir una bebida gaseosa tibia sale más gas que de una fría. ¿Por qué?", "los gases son menos solubles en líquidos a mayor temperatura", ["el calor crea más gas", "la bebida fría no tiene gas", "el plástico absorbe el gas"], "Con los gases ocurre lo contrario que con muchos sólidos.", "A mayor temperatura, el gas se disuelve menos y escapa.")
    b.nu(5, "Una solución de 300 mL contiene 60 g de soluto. ¿Cuántos gramos de soluto hay en 50 mL de ella?", 10, "Calcula cuánto soluto hay por mL.", "60 ÷ 300 = 0,2 g/mL; 0,2 · 50 = 10 g.", unidad="g")
    return b.items


# ---------------- 3° medio: Ciencias para la Ciudadanía ----------------
def cc3m_oa1():
    b = Autor("cie", "3m", 1)
    b.cat(1, "¿Favorece o perjudica la salud?", ["Favorece", "Perjudica"], [("dormir 8 a 9 horas", 0), ("hacer actividad física", 0), ("comer frutas y verduras", 0), ("fumar", 1), ("tomar sol sin protección", 1), ("dormir 4 horas por jugar", 1)],
          "Piensa en hábitos saludables y de riesgo.", "Dormir bien, moverse y comer frutas favorecen la salud; fumar, el sol sin protección y dormir poco la perjudican.")
    b.om(1, "¿Qué protege la piel de la radiación ultravioleta?", "usar bloqueador solar y sombrero", ["tomar agua fría", "usar ropa oscura de noche", "comer chocolate"], "Piensa en lo que usas en la playa.", "El bloqueador y el sombrero reducen la exposición a los rayos UV.")
    b.co(1, "La práctica regular de ejercicio ayuda a reducir el ___.", "estrés", ["sueño", "hambre siempre", "crecimiento"], "Piensa en cómo te sientes después de hacer deporte.", "La actividad física ayuda a manejar el estrés.")
    b.om(2, "¿Qué factor de la salud es ambiental?", "la contaminación del aire", ["los genes heredados", "la edad", "el grupo sanguíneo"], "Los factores ambientales vienen del entorno.", "La contaminación del aire es un factor ambiental.")
    b.em(2, "Une cada factor con su tipo.", [["la herencia genética", "biológico"], ["el smog de la ciudad", "ambiental"], ["el acceso a la salud", "social"]], "Biológico: del cuerpo; ambiental: del entorno; social: de la sociedad.", "Genes: biológico; smog: ambiental; acceso a la salud: social.")
    b.om(2, "El índice UV en el norte de Chile en verano puede ser «extremo». ¿Qué significa?", "que el riesgo de daño en la piel es muy alto", ["que hará mucho frío", "que lloverá", "que no hay sol"], "El índice UV mide la intensidad de la radiación solar.", "Un índice extremo indica alto riesgo de quemaduras.")
    b.om(3, "¿Por qué el consumo de alcohol es especialmente dañino en la adolescencia?", "porque el cerebro todavía está en desarrollo", ["porque los adolescentes son más altos", "porque el alcohol es más caro", "porque no afecta a los adultos"], "El cerebro madura hasta cerca de los 25 años.", "El cerebro en desarrollo es más vulnerable al alcohol.")
    b.cat(3, "¿Es un factor de riesgo o de protección frente al estrés?", ["Protección", "Riesgo"], [("tener amigos con quienes conversar", 0), ("dormir bien", 0), ("dormir con el celular encendido", 1), ("acumular tareas hasta el último día", 1)],
          "La protección reduce el estrés; el riesgo lo aumenta.", "El apoyo social y el sueño protegen; el celular de noche y postergar aumentan el estrés.")
    b.om(3, "En el sur de Chile, en invierno, aumentan las enfermedades respiratorias. ¿Qué factor ambiental influye?", "el humo de la calefacción a leña", ["el exceso de sol", "el agua de mar", "la falta de árboles"], "Piensa en el aire de Temuco u Osorno en invierno.", "El humo de la leña contamina el aire y afecta los pulmones.")
    b.ord(4, "Ordena de menor a mayor riesgo para la piel.", ["quedarse bajo techo", "estar a la sombra con bloqueador", "tomar sol con bloqueador al mediodía", "tomar sol sin protección al mediodía"], "Piensa en la exposición al sol.", "El riesgo aumenta con más exposición y menos protección.")
    b.om(4, "Un estudio muestra que quienes duermen menos tienen peores notas. ¿Qué conclusión es más prudente?", "hay una relación, pero se necesitan más datos para afirmar que una causa la otra", ["dormir poco siempre causa malas notas", "las notas no dependen de nada", "estudiar de noche es mejor"], "Correlación no siempre es causalidad.", "Una asociación no prueba por sí sola que una cosa cause la otra.")
    b.nu(4, "Una persona duerme 6 horas en vez de las 9 recomendadas para su edad. ¿Cuántas horas de sueño le faltan en una semana de 5 días de clases?", 15, "Calcula la diferencia por día y multiplica.", "3 horas × 5 días = 15 horas.", unidad="horas")
    b.om(5, "¿Por qué los plaguicidas pueden afectar la salud de quienes viven cerca de cultivos?", "pueden llegar al aire, el agua y los alimentos", ["solo afectan a los insectos", "desaparecen al instante", "mejoran el sistema inmune"], "Piensa en cómo se dispersan.", "Pueden contaminar aire, agua y alimentos si no se usan bien.")
    b.om(5, "¿Qué medida pública reduce más los efectos del smog en la salud?", "restringir la leña húmeda y mejorar el transporte público", ["cerrar los parques", "aumentar los autos", "prohibir el ejercicio al aire libre siempre"], "Ataca las fuentes de contaminación.", "Reducir las fuentes de emisión mejora la calidad del aire.")
    b.em(5, "Une cada problema de salud con un factor que lo favorece.", [["cáncer de piel", "radiación UV"], ["obesidad", "sedentarismo"], ["asma", "contaminación del aire"]], "Relaciona causa y efecto.", "UV, sedentarismo y contaminación favorecen esos problemas.")
    return b.items


def cc3m_oa2():
    b = Autor("cie", "3m", 2)
    b.om(1, "¿Qué instrumento amplió la capacidad de ver objetos muy lejanos?", "el telescopio", ["el microscopio", "el termómetro", "el estetoscopio"], "Galileo lo usó para observar Júpiter.", "El telescopio permite observar astros lejanos.")
    b.co(1, "El ___ permite ver células y microorganismos.", "microscopio", ["telescopio", "radar", "satélite"], "Amplía objetos muy pequeños.", "El microscopio amplía lo muy pequeño.")
    b.em(1, "Une cada tecnología con el sentido que amplía.", [["telescopio", "vista a gran distancia"], ["audífono", "audición"], ["cámara térmica", "ver el calor"]], "Piensa en qué percibe cada una.", "Telescopio, audífono y cámara térmica amplían distintos sentidos.")
    b.om(2, "¿Por qué el norte de Chile tiene grandes observatorios astronómicos?", "por sus cielos despejados, secos y con poca contaminación lumínica", ["porque está más cerca de las estrellas", "porque hace mucho frío", "porque hay muchas ciudades"], "Atacama tiene cielos muy limpios.", "El cielo seco y oscuro de Atacama es ideal para observar.")
    b.om(2, "¿Qué hace un satélite de telecomunicaciones?", "transmite señales de teléfono, internet o televisión", ["produce lluvia", "fabrica alimentos", "mide la temperatura del cuerpo"], "Está en órbita alrededor de la Tierra.", "Retransmite señales de comunicación.")
    b.cat(2, "¿Robótica o telecomunicaciones?", ["Robótica", "Telecomunicaciones"], [("brazo robótico en una fábrica", 0), ("robot explorador en Marte", 0), ("fibra óptica", 1), ("antenas de telefonía 5G", 1)],
          "Robótica: máquinas que actúan; telecomunicaciones: transmitir información.", "Brazos y rovers son robótica; fibra y antenas, telecomunicaciones.")
    b.om(3, "Un robot explorador en Marte permite a los científicos…", "estudiar un lugar donde las personas aún no pueden ir", ["vivir en Marte", "controlar el clima de la Tierra", "fabricar oxígeno en la Tierra"], "Piensa en los rovers.", "Los robots exploran lugares inaccesibles para las personas.")
    b.co(3, "Los radiotelescopios como ALMA captan ondas ___, invisibles para el ojo humano.", "de radio", ["sonoras", "sísmicas", "de agua"], "Su nombre da la pista.", "Captan ondas de radio del universo.")
    b.om(3, "¿Qué ventaja tiene la fibra óptica frente al cable de cobre?", "transmite más información y más rápido usando luz", ["es más pesada", "funciona sin luz", "no necesita instalación"], "La información viaja como pulsos de luz.", "Transmite datos con luz a gran velocidad.")
    b.ord(4, "Ordena cronológicamente estos avances.", ["telescopio de Galileo (siglo XVII)", "radio (fines del siglo XIX)", "primer satélite artificial (1957)", "internet móvil 5G (siglo XXI)"], "Del más antiguo al más reciente.", "Telescopio, radio, satélite y 5G, en ese orden.")
    b.om(4, "La física cuántica permitió desarrollar…", "los transistores de los computadores y celulares", ["la rueda", "el fuego", "la imprenta"], "Piensa en la electrónica moderna.", "Los transistores se basan en la física cuántica.")
    b.om(4, "¿Qué riesgo ético se discute con la robótica y la inteligencia artificial?", "la pérdida de algunos empleos y el uso de datos personales", ["que los robots tengan hambre", "que la luz se apague", "que los planetas se acerquen"], "Piensa en el trabajo y la privacidad.", "Se debate sobre el empleo y la privacidad de los datos.")
    b.om(5, "Un médico usa un estetoscopio digital que envía sonidos del corazón a otro hospital. ¿Qué tecnologías combina?", "amplificación de sentidos y telecomunicaciones", ["robótica y astronomía", "solo astronomía", "ninguna tecnología"], "Amplifica la audición y transmite datos.", "Amplía la audición y transmite la información a distancia.")
    b.cat(5, "¿Qué amplía cada tecnología?", ["Percepción humana", "Comprensión de la materia"], [("telescopio espacial", 0), ("lentes de visión nocturna", 0), ("acelerador de partículas", 1), ("microscopio electrónico de átomos", 1)],
          "Unas amplían los sentidos; otras permiten entender la materia.", "Telescopio y visión nocturna amplían la percepción; acelerador y microscopio atómico estudian la materia.")
    b.om(5, "¿Por qué los datos de ALMA son útiles para científicos de todo el mundo?", "porque observan cómo se forman estrellas y planetas", ["porque predicen el clima de mañana", "porque miden sismos", "porque cuentan la población"], "ALMA observa el universo frío y lejano.", "Estudia la formación de estrellas, planetas y galaxias.")
    return b.items


def cc3m_oa3():
    b = Autor("cie", "3m", 3)
    b.cat(1, "¿Es un agente infeccioso?", ["Agente infeccioso", "No es agente infeccioso"], [("virus", 0), ("bacteria", 0), ("hongo", 0), ("vitamina", 1), ("glóbulo rojo", 1)],
          "Los agentes infecciosos causan enfermedades transmisibles.", "Virus, bacterias y hongos pueden causar infecciones; las vitaminas y los glóbulos rojos no.")
    b.om(1, "¿Qué medida reduce el contagio de enfermedades respiratorias?", "lavarse las manos y ventilar los espacios", ["compartir botellas", "toser sobre la mano y no lavarla", "cerrar todas las ventanas"], "Piensa en cómo se transmiten los virus.", "El lavado de manos y la ventilación reducen el contagio.")
    b.co(1, "Las ___ preparan al sistema inmune para reconocer un agente infeccioso.", "vacunas", ["vitaminas", "bebidas", "radiografías"], "Se aplican en campañas de inmunización.", "Las vacunas entrenan al sistema inmune.")
    b.em(2, "Une cada enfermedad con su forma principal de transmisión.", [["influenza", "gotitas respiratorias"], ["hepatitis A", "agua o alimentos contaminados"], ["dengue", "picadura de mosquito"]], "Cada agente usa una vía distinta.", "La influenza es respiratoria; la hepatitis A, por agua o alimentos; el dengue, por mosquito.")
    b.om(2, "¿Por qué los antibióticos no sirven contra la gripe?", "porque la gripe la causa un virus y los antibióticos actúan contra bacterias", ["porque la gripe no es una enfermedad", "porque los antibióticos son vitaminas", "porque la gripe la causa un hongo"], "Diferencia virus y bacterias.", "Los antibióticos atacan bacterias, no virus.")
    b.co(2, "Cuando una enfermedad se extiende por varios países y continentes, se llama ___.", "pandemia", ["epidemia local", "alergia", "inmunidad"], "La COVID-19 fue un ejemplo.", "Una pandemia afecta a muchos países.")
    b.om(3, "¿Qué es la inmunidad de grupo (o de rebaño)?", "cuando muchas personas están inmunes, el agente circula menos y protege a quienes no pueden vacunarse", ["cuando todos se enferman a la vez", "cuando solo los animales se vacunan", "cuando no existe ningún virus"], "Piensa en bebés o personas que no pueden vacunarse.", "Una alta cobertura de vacunación frena la transmisión.")
    b.ord(3, "Ordena cómo actúa una vacuna.", ["Se aplica la vacuna.", "El sistema inmune reconoce el antígeno.", "Se generan anticuerpos y células de memoria.", "Ante el agente real, la defensa es más rápida."], "Aplicación, reconocimiento, memoria y protección.", "Así una vacuna genera protección.")
    b.om(3, "¿Por qué la vacuna contra la influenza se aplica todos los años en otoño?", "porque el virus cambia y antes del invierno aumentan los contagios", ["porque la vacuna dura un día", "porque es obligatoria cada mes", "porque en verano no hay virus nunca"], "El virus de la influenza muta y circula más en invierno.", "Cada año cambian las cepas y en invierno hay más contagios.")
    b.nu(4, "Una persona contagia en promedio a 3 personas. Si cada una contagia a otras 3, ¿cuántas personas nuevas se contagian en la segunda ronda?", 9, "3 × 3.", "En la segunda ronda se contagian 3 × 3 = 9 personas.", unidad="personas")
    b.om(4, "Un titular dice: «Remedio casero cura todas las infecciones». ¿Qué es lo más prudente?", "buscar evidencia en fuentes científicas confiables antes de creerlo", ["compartirlo de inmediato", "dejar de vacunarse", "creerlo porque tiene muchos likes"], "Las afirmaciones extraordinarias requieren evidencia.", "Hay que verificar en fuentes confiables.")
    b.cat(4, "¿Prevención eficaz o mito?", ["Prevención eficaz", "Mito"], [("vacunarse según el calendario", 0), ("lavarse las manos con jabón", 0), ("tomar antibióticos para un resfrío", 1), ("las vacunas no funcionan nunca", 1)],
          "Piensa en la evidencia científica.", "Vacunarse y lavarse las manos funcionan; los antibióticos para virus y negar las vacunas son mitos.")
    b.om(5, "Viajas a una zona tropical con dengue. ¿Qué medida tiene mejor evidencia?", "usar repelente y evitar el agua estancada", ["tomar antibióticos antes de viajar", "no tomar agua", "dormir sin mosquitero"], "El dengue lo transmite un mosquito.", "Evitar las picaduras y los criaderos de mosquitos previene el dengue.")
    b.om(5, "¿Por qué es importante terminar un tratamiento antibiótico indicado por el médico?", "para no dejar bacterias vivas que puedan volverse resistentes", ["porque sabe bien", "para curar virus", "para ganar peso"], "Relaciona con la selección natural.", "Cortarlo antes puede favorecer bacterias resistentes.")
    b.om(5, "¿Qué dato permite comparar mejor un brote entre dos ciudades de distinto tamaño?", "los casos por cada 100.000 habitantes", ["el número total de casos", "el nombre de la ciudad", "la cantidad de hospitales privados"], "Hay que considerar la población.", "La tasa por habitante permite comparar ciudades de distinto tamaño.")
    return b.items


# ---------------- 4° medio: Ciencias para la Ciudadanía ----------------
def cc4m_oa1():
    b = Autor("cie", "4m", 1)
    b.om(1, "¿Qué significa el pictograma de calavera en un envase?", "que el producto es tóxico", ["que es comestible", "que es reciclable", "que es para niños"], "Es un símbolo de peligro.", "La calavera indica toxicidad.")
    b.cat(1, "¿Dónde guardar estos productos?", ["Lejos del alcance de niños", "Puede estar a la mano"], [("cloro", 0), ("medicamentos", 0), ("destapador de cañerías", 0), ("agua embotellada", 1), ("fruta", 1)],
          "Los químicos y medicamentos se guardan en altura o bajo llave.", "Cloro, medicamentos y destapadores deben estar fuera del alcance de los niños.")
    b.co(1, "Antes de usar un producto de limpieza hay que leer su ___.", "etiqueta", ["precio", "color", "marca solamente"], "Ahí están las instrucciones y advertencias.", "La etiqueta indica el uso seguro y los riesgos.")
    b.om(2, "¿Por qué nunca se debe mezclar cloro con productos que contienen amoníaco?", "porque se liberan gases tóxicos", ["porque pierden el olor", "porque se vuelven agua", "porque cambian de color"], "La mezcla genera gases peligrosos.", "Al mezclarlos se liberan gases tóxicos que dañan las vías respiratorias.")
    b.em(2, "Une cada pictograma con su significado.", [["llama", "inflamable"], ["corrosión (gotas sobre una mano)", "corrosivo"], ["signo de exclamación", "irritante o nocivo"]], "Son pictogramas del sistema internacional.", "La llama indica inflamable; las gotas, corrosivo; la exclamación, irritante.")
    b.om(2, "¿Qué hacer con medicamentos vencidos?", "llevarlos a un punto de recolección en farmacias", ["botarlos al inodoro", "guardarlos para otra vez", "quemarlos en casa"], "Hay programas de recolección.", "Los puntos de recolección evitan contaminar el agua.")
    b.om(3, "Si un producto químico salpica los ojos, lo primero es…", "lavar con abundante agua y consultar a un centro de salud", ["frotar fuerte", "esperar a que pase", "aplicar otro químico"], "Primeros auxilios básicos.", "Lavar con mucha agua y pedir ayuda médica.")
    b.cat(3, "¿Uso seguro o inseguro?", ["Seguro", "Inseguro"], [("usar guantes al limpiar con cloro", 0), ("ventilar al usar productos fuertes", 0), ("guardar químicos en botellas de bebida", 1), ("mezclar productos para que limpien más", 1)],
          "Piensa en evitar intoxicaciones y confusiones.", "Guantes y ventilación son seguros; reenvasar en botellas de bebida y mezclar productos es peligroso.")
    b.om(3, "¿Por qué no se debe guardar un químico en una botella de bebida?", "porque alguien puede confundirlo y tomarlo", ["porque el plástico se derrite siempre", "porque pierde el color", "porque es ilegal tener botellas"], "Piensa en niños y adultos distraídos.", "El reenvasado causa intoxicaciones por confusión.")
    b.om(4, "Un medicamento dice «tomar cada 8 horas». ¿Cuántas dosis son al día?", "3", ["2", "4", "8"], "24 ÷ 8.", "24 ÷ 8 = 3 dosis al día.")
    b.om(4, "¿Qué indica la «fecha de vencimiento» de un medicamento?", "hasta cuándo el fabricante garantiza su eficacia y seguridad", ["el día en que se fabricó", "el precio del producto", "cuándo se puede regalar"], "Después de esa fecha puede no funcionar bien.", "Garantiza su efecto y seguridad hasta esa fecha.")
    b.ord(4, "Ordena qué hacer ante una posible intoxicación en casa.", ["Alejar a la persona del producto.", "Revisar la etiqueta del envase.", "Llamar a un centro de información toxicológica o de emergencias.", "Seguir las indicaciones recibidas."], "Proteger, identificar, llamar y seguir instrucciones.", "Primero alejar, luego identificar el producto y pedir ayuda.")
    b.om(5, "¿Por qué los detergentes con fosfatos pueden dañar lagos y ríos?", "porque favorecen el crecimiento excesivo de algas y reducen el oxígeno", ["porque enfrían el agua", "porque la vuelven salada", "porque matan solo a los peces grandes"], "Los fosfatos son nutrientes para las algas.", "El exceso de algas consume el oxígeno: eutrofización.")
    b.om(5, "Un plaguicida dice «no aplicar con viento». ¿Por qué?", "porque el viento puede llevarlo a personas, casas o fuentes de agua", ["porque se vuelve más fuerte", "porque se evapora y desaparece sin efecto", "porque mancha la ropa"], "Piensa en la deriva del producto.", "El viento dispersa el plaguicida fuera del área de aplicación.")
    b.cat(5, "¿Qué riesgo principal tiene cada producto?", ["Corrosivo", "Inflamable"], [("ácido de baterías", 0), ("soda cáustica", 0), ("bencina", 1), ("alcohol de quemar", 1)],
          "Corrosivo daña la piel; inflamable se enciende.", "Ácidos y soda son corrosivos; bencina y alcohol, inflamables.")
    return b.items


def cc4m_oa2():
    b = Autor("cie", "4m", 2)
    b.om(1, "¿Qué hacer si un enchufe se calienta mucho?", "dejar de usarlo y revisar la instalación", ["conectar más aparatos", "mojarlo para enfriarlo", "taparlo con un paño"], "El calor indica sobrecarga o falla.", "Un enchufe caliente puede provocar un incendio.")
    b.cat(1, "¿Seguro o peligroso?", ["Seguro", "Peligroso"], [("desenchufar tirando del enchufe, no del cable", 0), ("tener detector de monóxido de carbono", 0), ("usar un alargador con muchos aparatos", 1), ("tocar enchufes con las manos mojadas", 1)],
          "Piensa en sobrecargas y en el agua.", "Desenchufar bien y usar detectores es seguro; sobrecargar y tocar con las manos mojadas es peligroso.")
    b.co(1, "El ___ es un gas sin olor que puede producirse con estufas mal ventiladas.", "monóxido de carbono", ["oxígeno", "vapor de agua", "nitrógeno"], "Es un gas tóxico.", "El monóxido de carbono (CO) es tóxico e inodoro.")
    b.om(2, "¿Por qué una estufa a gas o a parafina necesita ventilación?", "para evitar la acumulación de monóxido de carbono", ["para que caliente menos", "para que no se apague con el viento", "para ahorrar gas"], "La combustión incompleta produce CO.", "La ventilación evita intoxicaciones por CO.")
    b.em(2, "Une cada riesgo con una medida de prevención.", [["sobrecarga eléctrica", "no usar alargadores en cadena"], ["intoxicación por CO", "ventilar y revisar las estufas"], ["quemadura solar en el trabajo", "usar bloqueador y ropa adecuada"]], "Cada riesgo tiene su medida.", "Prevenir sobrecargas, ventilar y protegerse del sol.")
    b.om(2, "¿Qué dispositivo corta la corriente si alguien recibe una descarga?", "el interruptor diferencial", ["el enchufe triple", "el foco LED", "el medidor de agua"], "Protege a las personas de las descargas.", "El diferencial corta la corriente ante una fuga a tierra.")
    b.om(3, "¿Por qué no se debe usar un secador de pelo cerca de la tina con agua?", "porque el agua conduce la electricidad y puede causar una descarga", ["porque el agua se enfría", "porque el secador se ensucia", "porque gasta más luz"], "El agua con sales es conductora.", "Si cae al agua, la corriente puede pasar por el cuerpo.")
    b.nu(3, "Un hervidor de 2.000 W se usa 15 minutos al día. ¿Cuántos Wh consume al día?", 500, "15 minutos es un cuarto de hora.", "2.000 W × 0,25 h = 500 Wh.", unidad="Wh")
    b.om(3, "¿Qué tipo de radiación es más peligrosa para el ADN?", "la radiación ionizante, como los rayos X en exceso", ["la luz de una vela", "las ondas de radio FM", "la luz de una linterna"], "La radiación ionizante tiene mucha energía.", "Los rayos X y gamma pueden dañar el ADN si hay sobreexposición.")
    b.ord(4, "Ordena qué hacer ante un amago de incendio eléctrico.", ["Cortar la electricidad en el tablero.", "Usar un extintor adecuado (nunca agua).", "Evacuar si el fuego no se controla.", "Llamar a bomberos (132)."], "Primero cortar la energía.", "Cortar la corriente, extinguir sin agua, evacuar y llamar al 132.")
    b.om(4, "¿Por qué no se apaga con agua un incendio eléctrico?", "porque el agua conduce la corriente y puede electrocutar", ["porque el agua aviva el fuego eléctrico siempre", "porque el agua es cara", "porque se evapora antes"], "Piensa en la conductividad.", "El agua puede conducir la electricidad hacia la persona.")
    b.cat(4, "¿Radiación ionizante o no ionizante?", ["Ionizante", "No ionizante"], [("rayos X", 0), ("rayos gamma", 0), ("ondas de radio", 1), ("microondas", 1)],
          "La ionizante tiene energía suficiente para arrancar electrones.", "Los rayos X y gamma son ionizantes; la radio y las microondas no lo son.")
    b.om(5, "En un taller, ¿qué solución reduce mejor el riesgo eléctrico?", "instalar diferenciales, revisar cables y capacitar al personal", ["trabajar más rápido", "desconectar la luz de emergencia", "usar alargadores en cadena"], "Combina medidas técnicas y de capacitación.", "Las medidas técnicas y la capacitación previenen accidentes.")
    b.om(5, "Una familia en Coyhaique usa leña húmeda y su casa se llena de humo. ¿Qué propuesta es más completa?", "usar leña seca certificada, revisar el cañón y ventilar", ["cerrar todas las ventanas", "usar más leña húmeda", "quemar plástico para que prenda"], "Piensa en la combustión y la ventilación.", "La leña seca contamina menos y la ventilación evita la acumulación de gases.")
    b.nu(5, "Cambias 5 ampolletas de 60 W por LED de 10 W. ¿Cuántos watts ahorras cuando todas están encendidas?", 250, "Ahorro por ampolleta: 60 − 10.", "50 W × 5 = 250 W.", unidad="W")
    return b.items


def cc4m_oa3():
    b = Autor("cie", "4m", 3)
    b.om(1, "¿Qué gas es uno de los principales responsables del calentamiento global?", "dióxido de carbono (CO₂)", ["oxígeno (O₂)", "helio (He)", "nitrógeno (N₂)"], "Se libera al quemar combustibles fósiles.", "El CO₂ intensifica el efecto invernadero.")
    b.co(1, "El aumento del promedio de la temperatura del planeta se llama calentamiento ___.", "global", ["local", "nocturno", "polar solamente"], "Afecta a todo el planeta.", "Se llama calentamiento global.")
    b.cat(1, "¿Aumenta o reduce las emisiones de CO₂?", ["Aumenta", "Reduce"], [("quemar carbón para producir electricidad", 0), ("deforestar bosques", 0), ("usar energía solar", 1), ("plantar árboles nativos", 1)],
          "Piensa en qué emite o absorbe CO₂.", "Quemar carbón y deforestar aumentan el CO₂; la energía solar y la reforestación lo reducen.")
    b.om(2, "¿Qué efecto del cambio climático ya se observa en Chile?", "sequías más prolongadas en la zona central", ["más nieve todo el año en Santiago", "desaparición del océano", "ningún cambio"], "Piensa en la «megasequía».", "La zona central enfrenta una sequía prolongada.")
    b.em(2, "Une cada efecto del cambio climático con su consecuencia.", [["retroceso de glaciares", "menos agua en los ríos en verano"], ["aumento del nivel del mar", "riesgo para zonas costeras"], ["olas de calor", "más incendios forestales"]], "Relaciona causa y consecuencia.", "Glaciares, nivel del mar y olas de calor tienen esas consecuencias.")
    b.om(2, "¿Qué es el efecto invernadero natural?", "la retención de parte del calor por gases de la atmósfera, que permite la vida", ["un daño causado solo por los invernaderos", "el frío del invierno", "la lluvia ácida"], "Sin él, la Tierra sería mucho más fría.", "Es natural y necesario; el problema es su intensificación.")
    b.om(3, "¿Por qué el océano se acidifica con más CO₂ en la atmósfera?", "porque el océano absorbe CO₂ y se forma ácido carbónico", ["porque llueve más sal", "porque los peces liberan ácido", "porque el agua se calienta y hierve"], "El CO₂ se disuelve en el agua.", "El CO₂ disuelto forma ácido carbónico y baja el pH.")
    b.ord(3, "Ordena la cadena de causas.", ["Se queman combustibles fósiles.", "Aumenta el CO₂ en la atmósfera.", "Se retiene más calor.", "Sube la temperatura promedio."], "De la causa humana al efecto global.", "Emisiones, más CO₂, más calor retenido y aumento de temperatura.")
    b.om(3, "¿Cómo afecta la acidificación a los moluscos como los choritos?", "les cuesta formar sus conchas de carbonato de calcio", ["crecen más rápido", "cambian de color a verde", "no les afecta en nada"], "El ácido disuelve el carbonato de calcio.", "Un agua más ácida dificulta la formación de conchas.")
    b.cat(4, "¿Mitigación o adaptación?", ["Mitigación (reducir emisiones)", "Adaptación (prepararse a los efectos)"], [("instalar paneles solares", 0), ("usar transporte público eléctrico", 0), ("construir embalses para la sequía", 1), ("plantar cultivos resistentes a la sequía", 1)],
          "Mitigar ataca la causa; adaptarse prepara para los efectos.", "Energía solar y transporte eléctrico mitigan; embalses y cultivos resistentes adaptan.")
    b.om(4, "¿Por qué los bosques ayudan a mitigar el cambio climático?", "porque absorben CO₂ en la fotosíntesis y lo almacenan", ["porque producen CO₂ de día", "porque enfrían el Sol", "porque generan petróleo"], "Recuerda la fotosíntesis.", "Los árboles capturan CO₂ y lo almacenan en su biomasa.")
    b.nu(4, "Un auto emite 2 kg de CO₂ cada 10 km. ¿Cuántos kg emite en un viaje de 150 km?", 30, "Calcula cuántos tramos de 10 km hay.", "150 ÷ 10 = 15 tramos; 15 × 2 = 30 kg.", unidad="kg")
    b.om(5, "Un municipio de la zona central quiere enfrentar la sequía. ¿Qué propuesta combina mitigación y adaptación?", "reutilizar aguas grises para riego e instalar energía solar en edificios públicos", ["regar con más agua potable", "talar bosques para tener más espacio", "prohibir la lluvia artificial"], "Busca una que ahorre agua y reduzca emisiones.", "Reutilizar agua es adaptación; la energía solar es mitigación.")
    b.om(5, "Un gráfico muestra que el CO₂ atmosférico pasó de unas 280 ppm (año 1800) a más de 400 ppm (hoy). ¿Qué conclusión es correcta?", "la concentración de CO₂ aumentó mucho desde la Revolución Industrial", ["el CO₂ disminuyó", "no hubo cambios", "el CO₂ solo cambia por los volcanes"], "Compara los dos valores.", "El aumento coincide con el uso masivo de combustibles fósiles.")
    b.om(5, "¿Cuál es el mejor argumento para proteger los glaciares andinos?", "son reservas de agua dulce para ciudades y cultivos en épocas secas", ["son bonitos en las fotos", "sirven para patinar", "no tienen ninguna importancia"], "Piensa en el agua en verano.", "Los glaciares liberan agua en verano y en sequías.")
    return b.items


GENERADORES = {
    "1_medio.ciencias.OA2": cn1m_oa2, "1_medio.ciencias.OA9": cn1m_oa9, "1_medio.ciencias.OA18": cn1m_oa18,
    "2_medio.ciencias.OA7": cn2m_oa7, "2_medio.ciencias.OA9": cn2m_oa9, "2_medio.ciencias.OA15": cn2m_oa15,
    "3_medio.ciencias.OA1": cc3m_oa1, "3_medio.ciencias.OA2": cc3m_oa2, "3_medio.ciencias.OA3": cc3m_oa3,
    "4_medio.ciencias.OA1": cc4m_oa1, "4_medio.ciencias.OA2": cc4m_oa2, "4_medio.ciencias.OA3": cc4m_oa3,
}
