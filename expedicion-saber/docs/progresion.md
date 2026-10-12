# Progresión

Todo lo que sigue está implementado en `js/motor.js` y probado en `pruebas/motor.test.js`. Los parámetros
viven en `mundos/mundos.json` (`progresion` y `economia`).

## Árbol de objetivos

Cada OA declara sus `prerequisitos`. Un OA está **disponible** cuando cada prerequisito cumple una de estas condiciones:

1. está **dominado**;
2. va en **dificultad 3 o más**, así el jugador no queda bloqueado hasta dominarlo del todo;
3. es de un **nivel escolar anterior** al del jugador: se asume aprendido (un niño de 3° básico no parte por 1°).

Los OA de cursos superiores al del jugador no se muestran como disponibles. Los de cursos anteriores quedan
abiertos para **repasar**. El jugador ve el árbol completo de cada asignatura, con el estado de cada nodo y qué
le falta para abrir los bloqueados.

```mermaid
flowchart LR
  m1_1["1° Mat OA 1"] --> m1_4["1° Mat OA 4"]
  m1_1 --> m1_9["1° Mat OA 9"]
  m1_1 --> m2_1["2° Mat OA 1"]
  m1_4 --> m2_3["2° Mat OA 3"]
  m1_9 --> m2_9["2° Mat OA 9"]
  m2_1 --> m2_11["2° Mat OA 11"]
  m2_9 --> m2_11
  m2_9 --> m3_6["3° Mat OA 6"]
  m2_11 --> m3_8["3° Mat OA 8"]
  m3_8 --> m3_9["3° Mat OA 9"]
  m3_9 --> m3_11["3° Mat OA 11"]
  m3_6 --> m4_3["4° Mat OA 3"]
  m3_8 --> m4_5["4° Mat OA 5"]
  m3_9 --> m4_6["4° Mat OA 6"]
  m3_11 --> m4_8["4° Mat OA 8"]
  l1_3["1° Len OA 3"] --> l1_4["1° Len OA 4"]
  l1_4 --> l1_8["1° Len OA 8"]
  l1_8 --> l2_5["2° Len OA 5"]
  l1_4 --> l2_21["2° Len OA 21"]
  l2_5 --> l3_4["3° Len OA 4"]
  l1_4 --> l3_20["3° Len OA 20"]
  l2_21 --> l3_22["3° Len OA 22"]
  l3_4 --> l4_4["4° Len OA 4"]
  l3_4 --> l4_10["4° Len OA 10"]
  l3_22 --> l4_21["4° Len OA 21"]
```

El validador revisa que cada prerequisito exista, que no apunte a un nivel superior y que no haya ciclos.

## Dificultad adaptativa

Cada OA tiene su propio nivel de dificultad (1 a 5) por jugador, y cada desafío del banco tiene el suyo.

- **Acierto** = resolver el desafío al primer intento. Resolverlo al segundo o tercero cuenta como fallo para
  la adaptación, pero igual da monedas.
- **3 aciertos seguidos** suben un nivel.
- **2 fallos seguidos** bajan un nivel.
- Si falla dos seguidos estando ya en nivel 1, el juego sugiere repasar los prerequisitos de ese OA.
- Los desafíos se eligen del nivel actual y no se repiten hasta agotar los de ese nivel.

## Dominio de un objetivo

Un OA queda **dominado** al lograr 3 aciertos seguidos estando en dificultad 5, que es la misma regla de
«subir» aplicada sobre el último nivel. Requiere al menos 15 aciertos, uno por desafío del mínimo del banco,
y entrega **100 monedas** una sola vez.

Un **tramo** es el conjunto de todos los OA de una asignatura en un nivel (por ejemplo, Matemática 2° básico:
OA 1, 3, 9 y 11). Los tramos dominados habilitan las mejoras finales del avatar.

## Sesión

- Una sesión son **10 desafíos** del OA recomendado: el primero disponible y no dominado del curso del jugador,
  en orden de nivel, dificultad del OA y número. El jugador también puede elegir un OA desde el árbol.
- Si domina el OA a mitad de sesión, sigue con el siguiente recomendado.
- Cada desafío admite **3 intentos**: tras el primer error aparece la pista; tras el tercero se muestran la
  respuesta correcta y la explicación del error.
- No hay temporizador ni ranking. Salir a mitad de sesión guarda las monedas ganadas, pero no da el bono de sesión.
- Para 1° y 2° básico el enunciado se lee en voz alta automáticamente (voz del dispositivo, en español).

## Persistencia

`localStorage`, clave `expedicion-saber-v1`. Varios perfiles en el mismo dispositivo, cada uno con su nivel
escolar, sus monedas, su progreso por OA, su racha y un avatar por mundo. El progreso académico y las monedas son
del perfil, así que se comparten entre mundos. El avatar y sus mejoras son propios de cada mundo.

Perfil (resumen):

```json
{
  "id": "p…", "nombre": "León", "nivel_escolar": "3_basico", "mundo": "bloques", "monedas": 130,
  "racha": { "dias": 1, "ultimo": "2026-10-12" },
  "oas": { "3_basico.matematica.OA6": { "nivel": 3, "ok": 0, "fallos": 0, "dominado": false, "vistos": ["…"], "respondidos": 10, "aciertos": 8 } },
  "avatares": { "bloques": { "casco": 1, "armadura": 0, "herramienta": 1, "botas": 0, "estructura": 0 }, "plataformas": { … }, "heroes": { … } }
}
```
