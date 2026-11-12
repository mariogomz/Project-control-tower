# Project Operating System (POS) · torre de control

Este repositorio es el kit del POS del curso AI Project Management. Un POS es una carpeta con el
contexto, el plan y el pulso de un proyecto; la torre de control es la página que se genera a partir
de esa carpeta. Todo el contenido para estudiantes está en español.

## Estructura

| Ruta | Qué es |
|---|---|
| `plantilla/` | POS vacío. Se copia a `equipos/<nombre>/`. El formato de cada archivo está en `plantilla/LEEME.md`. |
| `ejemplos/faro/` | Caso resuelto: Aseguradora Faro, proyecto «Estatus sin llamar». La ejecución (semanas 1 a 12) es simulada. |
| `equipos/` | Un POS por equipo. |
| `torre/` | `motor.py` calcula estado y alertas; `construir.py` genera `torre.html`; `plantilla.html` es la página. |
| `.agents/skills/` | Skills del kit. `.claude/skills` apunta a la misma carpeta. |
| `tests/` | Pruebas del motor. |

Un POS tiene cuatro capas, una por módulo:

1. **Contexto** (M1): `pos.json`, `contexto/acta.md`, `registros/`
2. **Plan** (M2): `plan/`
3. **Pulso** (M3): `pulso/`
4. **Torre** (M4): `torre.html`, generada

## Comandos

```
python3 torre/construir.py ejemplos/faro            # genera la torre
python3 torre/construir.py ejemplos/faro --revisar  # revisa los registros
python3 torre/construir.py ejemplos/faro --brief    # brief de la última semana
python3 -m unittest discover -s tests               # pruebas
python3 ejemplos/faro/_escenario.py                 # regenera los registros de Faro
```

Solo hace falta Python 3.9 o superior. No hay dependencias que instalar.

## Skills

Si tu agente no las carga solo, lee el archivo antes de empezar la tarea.

| Cuándo | Skill |
|---|---|
| El equipo tiene su acta y quiere arrancar su POS | `.agents/skills/pos-instrumentar/SKILL.md` |
| Hay que registrar lo que pasó en la semana | `.agents/skills/pos-pulso/SKILL.md` |
| Hay que construir o leer la torre, o preparar un brief o un War Room | `.agents/skills/pos-torre/SKILL.md` |

## Reglas para cualquier agente

- Antes de actuar sobre un POS, lee su `registros/permisos.csv`. Lo que dice «nunca» no se hace; lo que
  dice «pregunta» se pregunta.
- No inventes datos. Una celda vacía y un hueco declarado valen más que un número plausible.
- No cambies metas, umbrales, línea base ni plan para que la torre se vea mejor.
- Los números y las alertas salen de `torre/motor.py`. Si una regla parece equivocada, propón el cambio
  en el motor con su prueba; no lo compenses en los datos.
- `ejemplos/faro/` se regenera desde `_escenario.py`: edita ese archivo, no los CSV.
- Después de tocar registros, corre `--revisar` y vuelve a construir la torre.
- Escribe para estudiantes en español claro, sin jerga técnica.
