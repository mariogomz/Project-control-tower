# Kit · Sesión 5 · Del caso al acta, y el acta al POS

Todo lo que van a copiar está en este documento. Cada prompt va dentro de un recuadro: copien solo lo que está dentro.

## 0. Antes de empezar

- **Modo Work.** Abran ChatGPT y cambien a modo Work. Las skills solo aparecen ahí.
- **Tengan a la mano** su Framing Brief v1 (está en su tablero de la sesión 4, zona 4).
- **La página del POS:** [PEGAR AQUÍ EL ENLACE DE LA PÁGINA]

## 1. Agregar el modo charter a su skill (1 minuto)

**Dónde va:** en el chat de **@skill-creator** (Plugins → Skills → framing-brief → editar con chat).

Sirve igual si se quedaron con la skill de referencia o con la suya.

**Copien todo lo que está dentro del recuadro**

````text
Agrega a mi skill framing-brief el archivo references/charter.md con exactamente el contenido que va abajo, sin cambiar nada. Además, al final de la sección «Modos de esta skill» del SKILL.md agrega esta línea, textual: "Si el equipo ya tiene su Framing Brief v1 y pide el acta, la definición de éxito o la decisión ('modo charter'), lee references/charter.md y sigue sus pasos. Si ese archivo no existe, dilo y pide que lo agreguen." No cambies nada más, no me hagas preguntas y avísame cuando esté lista.

# Modo charter (Framing Brief v1 → v2 y bloque POS)

## Entradas
1. El Framing Brief v1 (obligatorio). Si no trae proyecto recomendado ni supuesto que cambia la decisión, detente y pídelos.
2. El Framing Brief v0, si el v1 no repite sus secciones (solicitud, afectados, A → B, ángulos, encuadres, evidencia).
3. Lo que el equipo ya escribió en su tablero sobre éxito, pre-mortem, límites, quién decide y permisos de la IA (si existe).
Si falta algo, escribe [POR CONFIRMAR: qué falta y quién lo sabe]. No lo inventes.

## Reglas de este modo
- Siguen valiendo las reglas del SKILL.md: una pregunta por mensaje; dato, supuesto o esperanza en cada afirmación; nada inventado.
- El acta se queda a nivel de encuadre: qué es éxito, hasta dónde llega el proyecto y quién decide. No es un plan.
- La decisión la toma el equipo o quien el equipo diga que decide. Tú la registras; no la recomiendas ni la cambias.
- Si el equipo pega todo de una vez, no repitas preguntas que ya están respondidas: muestra lo que encontraste en cada paso y pide que lo confirmen.
- Muestra al inicio de cada mensaje en qué paso van, así: "Paso 2 de 8 · Éxito".

## Pasos
1. Repite textual, del v1: el A → B, el proyecto recomendado y el supuesto que cambia la decisión, con su prueba. Pregunta si algo cambió desde la sesión 4.
2. Éxito. Completa la tarjeta, un campo a la vez: beneficio (qué cambia y para quién) y un efecto negativo a vigilar; indicador y de dónde sale el dato; línea base; meta con plazo; examen intermedio (qué deberíamos ver a mitad de camino) y lo que no debe empeorar; dueños: quién responde por el beneficio, quién lo mide y a quién se avisa si se desvía.
3. Pre-mortem. Pregunta: "Imaginen que el proyecto terminó y fracasó. ¿Qué pasó?" Pide de 3 a 5 causas con sus palabras. No agregues las tuyas.
4. Límites. Qué queda dentro, qué queda fuera y qué restricciones hay. Parte de lo obligatorio del v1 y de las opciones descartadas.
5. Quién decide. Una persona o un rol, no un comité. Luego, quién puede frenar y sobre qué.
6. Permisos de la IA. Tres listas: puede hacerlo sola, pregunta antes, nunca. Para cada tarea que propongan, pregunta: ¿la IA es capaz?, ¿tiene el contexto?, ¿tiene la autoridad?, ¿alguien puede revisar el resultado?
7. La decisión. Pregunta cuál fue: go, investigar, todavía no o no-go; quién la tomó, con qué límite (dinero o tiempo) y cuándo es la primera revisión. Regístrala con sus palabras.
8. Entrega, en este orden: el Framing Brief v2, la revisión final con la lista de huecos y el bloque POS.

## Revisión final (entrégala siempre)
- [ ] El beneficio dice qué cambia para alguien, no qué se entrega
- [ ] Cada indicador tiene fuente, línea base y meta con plazo
- [ ] Hay un examen intermedio
- [ ] Los tres dueños tienen nombre o rol
- [ ] Algo quedó escrito como "fuera"
- [ ] Decide una sola persona o rol
- [ ] Hay al menos una tarea en "nunca"
- [ ] La decisión tiene límite y primera revisión
- [ ] No hay cifras, fuentes ni personas que el equipo no mencionó
Lista los huecos encontrados, del más grave al menos grave.

## Formato de salida: Framing Brief v2
Encabezado (versión, fecha, dueño) · Del v1: solicitud, A → B, encuadre, proyecto recomendado, supuesto que cambia la decisión · Éxito (beneficio, efecto negativo, indicador, línea base, meta, examen intermedio, dueños) · Pre-mortem · Límites (dentro, fuera, restricciones) · Quién decide y quién puede frenar · Permisos de la IA · Decisión · Huecos

## Bloque POS
Después del Brief v2 y de los huecos, entrega el bloque POS: todo el contenido del Brief (lo del v0, lo del v1 y lo del v2) en el formato de abajo, dentro de un solo bloque de código, para que el equipo lo copie y lo pegue en la página del POS.

Reglas del bloque:
- Copia los textos del Brief tal cual. No resumas, no mejores y no agregues nada. Las fechas también: usa las del Brief, no la de hoy.
- Usa exactamente estas claves y no agregues otras. Si un dato no existe, deja "" o []. Si falta y alguien lo sabe, escribe "[POR CONFIRMAR: qué falta y quién lo sabe]".
- "etiqueta" y "tipo" de una línea de valor o costo solo pueden ser: dato, supuesto o esperanza. Los semáforos: verde, amarillo o rojo. "resultado": go, investigar, todavía no o no-go.
- En "opciones" van las seis casillas en su orden; "es_la_solicitud" es true solo en la del sponsor.
- Dentro de los textos usa comillas angulares « » en lugar de comillas dobles.
- No escribas nada después del bloque.

```json
{
  "pos": "1",
  "iniciativa": "",
  "equipo": "",
  "organizacion": "",
  "fecha": "",
  "version_brief": "v2",
  "solicitud": {"texto": "", "quien": "", "cuando": ""},
  "afectados": {"viven_el_problema": "", "lo_pide": "", "nuestro_papel": ""},
  "a": "",
  "b": "",
  "angulos": [
    {"angulo": "Lo que no aparece", "hallazgo": "", "etiqueta": ""},
    {"angulo": "Para qué", "hallazgo": "", "etiqueta": ""},
    {"angulo": "Dónde sí funciona", "hallazgo": "", "etiqueta": ""},
    {"angulo": "El espejo", "hallazgo": "", "etiqueta": ""},
    {"angulo": "El lugar del otro", "hallazgo": "", "etiqueta": ""}
  ],
  "encuadres": [{"texto": "", "elegido": true, "por_que": ""}],
  "evidencia": [{"afirmacion": "", "fuente": "", "fecha": "", "etiqueta": ""}],
  "linea_base": "",
  "preguntas_abiertas": [""],
  "ideas_estacionadas": [""],
  "necesidad": "",
  "objetivos": [{"objetivo": "", "linea_base": "", "fuente": ""}],
  "obligatorio": [""],
  "opciones": [
    {"casilla": "Seguir como estamos", "descripcion": "", "obligatorio": "", "ajuste": "", "valor": "", "lograr": "", "tipo": "", "en_lista_corta": false, "recomendada": false, "es_la_solicitud": false}
  ],
  "proyecto": {
    "nombre": "",
    "descripcion": "",
    "valor": [{"linea": "", "rango": "", "fuente": "", "tipo": ""}],
    "costo": [{"linea": "", "rango": "", "fuente": "", "tipo": ""}],
    "beneficiario": "",
    "efecto_negativo": ""
  },
  "supuesto_clave": {"supuesto": "", "si_es_falso": "", "prueba": "", "fecha": "", "dueno": ""},
  "supuestos": [{"supuesto": "", "fuente": "", "etiqueta": "", "dueno": "", "fecha_prueba": ""}],
  "exito": {
    "beneficio": "",
    "efecto_negativo": "",
    "indicadores": [{"indicador": "", "fuente": "", "linea_base": "", "meta": "", "plazo": ""}],
    "examen_intermedio": "",
    "guardrail": "",
    "duenos": {"beneficio": "", "medicion": "", "desviaciones": ""}
  },
  "premortem": [""],
  "acta": {"dentro": [""], "fuera": [""], "restricciones": [""], "decide": "", "vetos": [""]},
  "permisos": {"puede": [""], "pregunta": [""], "nunca": [""]},
  "decision": {"resultado": "", "texto": "", "quien": "", "fecha": "", "limite": "", "primera_revision": ""},
  "huecos": [""]
}
```

## No hagas
- Planear: cronograma, tareas, responsables de tareas o presupuesto detallado. Eso es del módulo 2.
- Cambiar o recomendar la decisión.
- Inventar metas, líneas base, fuentes, dueños o fechas.
- Dejar un campo vacío sin decirlo en la lista de huecos.
````

**Hasta aquí se copia**

## 2. Armar el acta (20 minutos)

1. Chat nuevo en modo Work. Escriban **@framing brief, modo charter**.
2. Péguenle su Framing Brief v1. Si su v1 no repite lo del v0, peguen también el v0.
3. Respondan corto, una pregunta a la vez. Si no saben algo: «no sé».
4. Al final reciben tres cosas: su Framing Brief v2, la lista de huecos y el bloque POS.

## 3. Ver el acta en su POS (2 minutos)

1. Copien el bloque POS completo, desde la primera `{` hasta la última `}`.
2. Abran la página del POS → **Mi equipo** → peguen → **Mostrar mi acta**.
3. Revisen la barra de arriba: cuántas partes están listas y cuántas quedaron por confirmar.

## 4. Cerrar un hueco (5 minutos)

1. Abran la tarjeta **Lo que falta**, al final de la página.
2. Elijan el hueco más grave que puedan resolver hoy.
3. Vuelvan al chat, díganle a la skill el dato que faltaba y pidan: **«vuelve a darme el bloque POS completo»**.
4. Péguenlo otra vez en **Mi equipo → Pegar otro bloque**.

**Pregunta para el Escéptico del equipo:** ¿qué parte de esta acta firmamos con nuestro nombre, y qué parte todavía es fluidez sin evidencia?
