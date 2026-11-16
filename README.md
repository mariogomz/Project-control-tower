# Project Operating System · torre de control

Kit del proyecto transversal del curso AI Project Management. Un **POS** es una carpeta con el contexto,
el plan y el pulso de un proyecto. La **torre de control** es la página que se genera a partir de esa
carpeta: compara lo que está pasando contra lo que se firmó, levanta alertas y arma el brief para quien decide.

## Para la sesión 5: el acta en el POS

La primera capa del POS es el acta de constitución del proyecto, y para verla no se instala nada.

- **`pos/index.html`** es la página. Tiene tres pestañas: *Cómo funciona*, *Ejemplo* (Aseguradora Faro)
  y *Mi equipo*.
- Arriba va la **ruta del proyecto** en 3D, de hoy a la meta, con los supuestos y los riesgos del acta.
  Cada punto se puede tocar. Al lado, la **decisión** y el medidor **Lista para firma**.
- Debajo, el **acta de constitución** en módulos, con los nombres que usa la disciplina: propósito,
  objetivos y criterios de éxito, alcance, supuestos y restricciones, riesgos, presupuesto, hitos,
  stakeholders y sponsor. Cada módulo abre su detalle.
- Más abajo, **cómo llegamos aquí**: la solicitud, el problema, la evidencia y las opciones. Es el caso
  de negocio que sostiene el acta, y por eso va en segundo nivel.
- En el ejemplo, **«Ver lo que viene»** simula doce semanas para mostrar lo que agregan el plan, el
  pulso y la torre. Los datos de esa simulación están en `pos/simulacion-faro.json`.
- **`kit/kit-s5.md`** trae el modo charter de la skill `framing-brief`, el guion de la demo guiada y un
  recurso sobre cómo se hizo la skill.

El modo charter termina entregando un **bloque POS**: el Framing Brief v2 en un formato que la página
lee. El equipo lo copia del chat, lo pega en *Mi equipo* y ve su acta, con lo que falta marcado.

El formato del bloque es el mismo en tres lugares, y `tests/test_pos.py` lo comprueba: la plantilla dentro
de `kit/kit-s5.md`, el ejemplo `pos/ejemplo-faro.json` y lo que lee `pos/pagina.html`. Si cambias uno,
cambia los tres y corre `python3 pos/_armar.py` para volver a armar `pos/index.html`.

Lo que sigue en este documento (la carpeta POS y la torre) es trabajo anterior que sirve de base para el módulo 4.

## Verlo funcionando

Abre `ejemplos/faro/torre.html` con doble clic. Es el caso Aseguradora Faro («Estatus sin llamar») con
doce semanas de ejecución simulada. Arriba a la derecha puedes cambiar de capa para ver cómo crece el
POS módulo a módulo; abajo de la pantalla de vuelo puedes recorrer las semanas.

| Capa | Módulo | Qué agrega | Dónde vive |
|---|---|---|---|
| 1 · Contexto | M1 | El acta, qué es éxito, supuestos, riesgos, permisos de la IA, decisiones | `pos.json`, `contexto/`, `registros/` |
| 2 · Plan | M2 | Hitos, fechas y presupuesto: la ruta planeada | `plan/` |
| 3 · Pulso | M3 | Mediciones, avance, gasto y señales de cada semana: la ruta real | `pulso/` |
| 4 · Torre | M4 | Alertas, de la señal a la decisión, brief ejecutivo | `torre.html` |

## Empezar con tu equipo

Necesitas Python 3.9 o superior y un agente que trabaje sobre carpetas, como Codex. No hay
nada más que instalar.

1. Abre esta carpeta con tu agente.
2. Pídele: **«Instrumenta el acta de mi equipo»** y pégale tu acta, tu definición de éxito, tu pre-mortem,
   tus supuestos y tu tabla de permisos. Usará la skill `pos-instrumentar` y creará `equipos/<tu-equipo>/`.
3. Abre `equipos/<tu-equipo>/torre.html`. Esa es tu torre en la capa 1: ya sabe qué vigilar y todavía
   no tiene datos.

Cada semana, cuando el proyecto esté en marcha: **«Registra el pulso de la semana»** con la minuta o
la exportación de tu tablero (skill `pos-pulso`), y **«Construye la torre y dame el brief»** (skill `pos-torre`).

A mano también funciona:

```
python3 torre/construir.py equipos/<tu-equipo> --revisar   # revisa los registros
python3 torre/construir.py equipos/<tu-equipo>             # escribe torre.html
python3 torre/construir.py equipos/<tu-equipo> --brief     # imprime el brief de la semana
python3 torre/construir.py ejemplos/faro --semana 6 --salida crisis.html   # la torre como estaba en la semana 6
```

El formato de cada archivo está en [`plantilla/LEEME.md`](plantilla/LEEME.md).

## Cómo decide la torre qué es una alerta

Las alertas salen de reglas fijas en `torre/motor.py`. Los mismos registros dan siempre la misma torre.

| Regla | Atención | Crítica |
|---|---|---|
| Indicador fuera de rango | Cruza el umbral ámbar | Cruza el umbral rojo |
| Indicador sin medir | Dos periodos sin dato | |
| Supuesto | En duda, o prueba vencida | Roto |
| Hito | Atrasado, o pronóstico movido | Tres semanas de atraso o más |
| Avance y costo | Menos de $0.90 de avance por cada $1 planeado o gastado | Menos de $0.80 |
| Fecha de cierre | | Se mueve dos semanas o más |
| Riesgo | | Ocurrió |
| Señales sin decisión | Dos señales sobre el mismo tema y ninguna decisión | Tres señales, o tres semanas |
| Condición de corte | | Se cumplió lo que el acta definió como límite |

Una decisión registrada que nombra el tema apaga la alerta de supuesto roto, riesgo ocurrido, señales
sin decisión o condición de corte. Un indicador en rojo solo se apaga cuando el dato mejora.

## Estructura

```
plantilla/          POS vacío para copiar
ejemplos/faro/      caso resuelto; _escenario.py regenera sus registros
equipos/            un POS por equipo
torre/              motor.py (reglas), construir.py (genera la página), plantilla.html (la página)
.agents/skills/     skills del kit; Codex las encuentra aquí
AGENTS.md           instrucciones para el agente
tests/              python3 -m unittest discover -s tests
```

## Notas

- Aseguradora Faro es un caso ficticio. Su acta sale del módulo 1; la ejecución de las semanas 1 a 12 es simulada.
- La vista 3D usa three.js (licencia MIT, incluida en `torre/vendor/`). La torre funciona sin internet;
  con internet carga además las tipografías.
