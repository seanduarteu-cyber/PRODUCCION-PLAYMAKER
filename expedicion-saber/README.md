# Expedición Saber

Videojuego educativo basado en las Bases Curriculares del Mineduc. El jugador resuelve desafíos de su curso,
gana monedas y las gasta en mejorar su avatar. No hay ranking, ni competencia con otros jugadores, ni tiempo
que castigue: el refuerzo es ver crecer el avatar.

**Estado:** Matemática y Lenguaje de 1° a 4° básico, con un mundo completo (Valle Bloque, estética voxel).
Isla Brinco (plataformas) y Ciudad Voltia (héroes) ya tienen su configuración de ambientación y mejoras, pero
les falta el dibujo del avatar.

## Cómo jugar en local

```bash
cd expedicion-saber
python3 -m http.server 8000
# abrir http://localhost:8000/index.html
```

Se necesita un servidor porque el juego carga los JSON con `fetch`. El progreso se guarda en el navegador.

## Estructura

```
contenido/            Banco: un JSON por nivel y asignatura + indice.json (generado, no editar a mano)
mundos/mundos.json    Tres mundos (tokens de ambientación, espacios y niveles del avatar), economía y progresión
js/motor.js           Reglas sin interfaz: árbol, dificultad adaptativa, dominio, monedas, racha, mejoras, guardado
js/avatar_bloques.js  Dibujo voxel del avatar de Valle Bloque (5 espacios × 5 niveles)
js/ui.js              Perfiles, mundos, base, árbol, taller y resumen de sesión
js/retos.js           Sesión de 10 desafíos y los 6 tipos de desafío
herramientas/         Generadores del banco, registro de OA, validador y simulación de la economía
pruebas/              Pruebas del motor (Node) y prueba de punta a punta (Playwright)
docs/                 Contenido, progresión y economía
```

## Comandos

```bash
python3 herramientas/generar.py            # regenera contenido/ desde los generadores
python3 herramientas/validar.py            # valida el banco (esquema, ≥15 desafíos por OA, ≥3 por nivel, árbol)
node pruebas/motor.test.js                 # 11 pruebas del motor
python3 herramientas/simular_economia.py   # simula ingresos y tiempos de cada mejora
node pruebas/e2e.js                        # juega una sesión completa en el navegador (con el servidor en el puerto 8765)
```

## Documentación

- [docs/contenido.md](docs/contenido.md): esquema del banco, tipos de desafío, ambientación, cobertura y
  códigos pendientes de verificación.
- [docs/progresion.md](docs/progresion.md): árbol de prerequisitos, dificultad adaptativa, dominio, sesiones y guardado.
- [docs/economia.md](docs/economia.md): tabla de costos y justificación del balance.

## Precisión curricular

Cada OA lleva su código oficial y la página de curriculumnacional.cl donde se confirmó. Tres códigos de Lenguaje
(LE01 OA 04, LE01 OA 08 y LE02 OA 21) están marcados como **pendientes de verificación**: no se inventaron, pero
no se pudo confirmar su redacción. El texto de cada objetivo es un resumen fiel, no una cita literal.

## Personajes y nombres

Todos los nombres, personajes y diseños son originales (Valle Bloque, Rocío la minera, Isla Brinco, Pipo,
Ciudad Voltia, Capitana Chispa, el mineral «lumita»). No se usan marcas, personajes ni nombres de juegos o
franquicias existentes.
