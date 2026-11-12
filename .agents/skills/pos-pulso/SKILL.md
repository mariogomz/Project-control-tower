---
name: pos-pulso
description: Registra el pulso semanal de un proyecto en su POS a partir de minutas, correos, transcripciones o exportaciones de Jira u otra herramienta - mediciones, avance de hitos, gasto y señales. Úsala cuando pidan "registrar la semana", "actualizar el pulso", "cargar la minuta" o "qué cambió esta semana".
---

# Pulso semanal

Cada semana deja rastro en reuniones, correos y tableros. Esta skill lo pasa a `pulso/` para que la
torre pueda compararlo contra el acta y el plan.

## Antes de escribir

1. Lee `registros/permisos.csv` del POS. Manda sobre todo lo demás.
2. Confirma qué semana se registra (semana 1 = primera semana después del arranque).
3. Pide las fuentes: minuta, transcripción, correos, exportación del tablero, reporte de gasto.
   Guarda la minuta en `pulso/notas/semana-NN.md`.

## Qué se registra y dónde

| Archivo | Qué va | Regla |
|---|---|---|
| `pulso/mediciones.csv` | Valor de cada indicador que se midió esta semana | Solo si viene de la fuente que el indicador declara. Si no hay dato, no hay fila. |
| `pulso/hitos.csv` | Hitos que cambiaron: estado, avance %, semana de pronóstico | Solo los que cambiaron. |
| `pulso/gasto.csv` | Gasto real acumulado | Una fila por semana. |
| `pulso/bitacora.csv` tipo `senal` | Algo que alguien dijo o reportó y que apunta a un supuesto, riesgo, hito o indicador | Cita textual, con su fuente y con las referencias (`S3;R2`). |
| `pulso/bitacora.csv` tipo `supuesto` o `riesgo` | Cambio de estado | Propón el cambio con su evidencia y **pregunta antes de escribirlo**. |
| `pulso/bitacora.csv` tipo `cambio` | Cambio aprobado de alcance, fecha o presupuesto | Solo si lo aprobó quien decide. |
| `registros/decisiones.csv` | Decisiones tomadas | Con quién decidió y a qué referencias responde. |

Una señal no es una interpretación: es lo que se dijo. «TI mueve la fecha por segunda vez» es una señal.
«El proyecto va mal» no lo es.

## Después de escribir

1. Corre `python3 torre/construir.py <carpeta> --revisar` y corrige lo que marque.
2. Corre `python3 torre/construir.py <carpeta>` para actualizar la torre.
3. Reporta: qué filas agregaste, qué cambios de estado propones y esperan respuesta, y qué
   encontraste en las fuentes que no supiste dónde poner.

## Lo que no debes hacer

- Cambiar metas, umbrales, línea base o el plan. La torre mide contra lo que se firmó.
- Rellenar una medición que falta con una estimación. Un indicador sin medir es información.
- Suavizar una cita o resumir varias señales en una.
- Decidir. Si las fuentes muestran un problema sin dueño, dilo; no lo resuelvas.
