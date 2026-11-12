---
name: pos-instrumentar
description: Convierte el acta del equipo (Framing Brief v2, definición de éxito, pre-mortem, supuestos, permisos y decisión) en los registros que la torre de control puede leer. Úsala cuando el equipo ya tiene su acta y quiere arrancar su POS, o cuando pide "instrumentar el acta", "crear el POS del equipo" o "preparar la torre".
---

# Instrumentar el acta

El acta dice qué es éxito, qué se supone, qué puede salir mal y quién decide. Esta skill la pasa a
tablas, sin cambiarla, para que la torre sepa qué vigilar.

## Entradas

Pide lo que falte, una cosa a la vez:

1. El acta o Framing Brief v2 del equipo, tal como quedó.
2. La tarjeta de éxito: beneficio, indicador, línea base, meta, examen intermedio, dueños.
3. El pre-mortem.
4. Los supuestos, con su prueba y su dueño.
5. La tabla Puede / Pregunta antes / Nunca.
6. La decisión (go, investigar, todavía no, no-go), quién la tomó y con qué límite.

## Pasos

1. Copia `plantilla/` a `equipos/<nombre-del-equipo>/`. No trabajes sobre `plantilla/` ni sobre `ejemplos/`.
2. `pos.json`: proyecto, equipo, quién decide, vetos, PM, A y B, dentro, fuera, restricciones, fecha de
   inicio, semanas, moneda y presupuesto. Si el acta trae una condición para detenerse, va en `condiciones_corte`.
3. `contexto/acta.md`: pega el acta completa. No la resumas ni la mejores.
4. `registros/indicadores.csv`: una fila por indicador. Cada uno necesita meta, umbral ámbar, umbral rojo,
   fuente del dato, dueño, cada cuántas semanas se mide y desde qué semana tiene sentido evaluarlo.
5. `registros/supuestos.csv`: una fila por supuesto, con qué pasa si falla, cómo se prueba, dueño y semana de prueba.
6. `registros/riesgos.csv`: una fila por punto del pre-mortem. Cada riesgo necesita su señal temprana:
   qué veríamos primero si empieza a ocurrir.
7. `registros/permisos.csv`: la tabla del equipo, una acción por fila, con nivel `puede`, `pregunta` o `nunca`.
8. `registros/decisiones.csv`: la decisión de arranque en la semana 0.
9. Corre `python3 torre/construir.py equipos/<nombre> --revisar` y corrige lo que marque.
10. Corre `python3 torre/construir.py equipos/<nombre>` y entrega la ruta de `torre.html`.

El formato exacto de cada archivo está en `plantilla/LEEME.md`. El caso resuelto está en `ejemplos/faro/`.

## Lo que no debes hacer

- Inventar metas, umbrales, fuentes, dueños o fechas. Si el equipo no lo definió, deja la celda vacía
  y anótalo en la lista de huecos.
- Planear. Los hitos y el presupuesto llegan en el módulo 2; no llenes `plan/`.
- Cambiar la decisión del equipo o el texto del acta.
- Llenar `pulso/`. Eso es lo que pasa después.

## Cierre

Entrega tres cosas: la ruta de la torre, la lista de huecos (lo que el acta no define y la torre necesita)
y esta pregunta para el Escéptico del equipo:

> ¿Qué de esto firmamos con nuestro nombre, y qué indicador todavía no tiene una fuente real detrás?
