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


GENERADORES = {
    "1_medio.ciencias.OA2": cn1m_oa2, "1_medio.ciencias.OA9": cn1m_oa9, "1_medio.ciencias.OA18": cn1m_oa18,
    "2_medio.ciencias.OA7": cn2m_oa7, "2_medio.ciencias.OA9": cn2m_oa9, "2_medio.ciencias.OA15": cn2m_oa15,
}
