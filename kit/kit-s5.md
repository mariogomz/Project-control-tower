# Kit · Sesión 5 · Del caso al acta, y el acta al POS

Este documento tiene tres partes: lo que hace quien dicta antes de la sesión, el guion de la demo
guiada y un recurso para quien quiera saber cómo se hizo la skill.

## A. Antes de la sesión · instalar el modo charter en cada cuenta de equipo

Se hace una vez por cuenta, en ChatGPT, modo Work: Plugins → Skills → framing-brief → editar con chat
(**@skill-creator**). Sirve igual si el equipo se quedó con la skill de referencia o con la suya.

**Pegar todo lo que está dentro del recuadro**

````text
Agrega a mi skill framing-brief el archivo references/charter.md con exactamente el contenido que va abajo, sin cambiar nada. Además, al final de la sección «Modos de esta skill» del SKILL.md agrega esta línea, textual: "Si el equipo ya tiene su Framing Brief v1 y pide el acta, la definición de éxito o la decisión ('modo charter'), lee references/charter.md y sigue sus pasos. Si ese archivo no existe, dilo y pide que lo agreguen." No cambies nada más, no me hagas preguntas y avísame cuando esté lista.

# Modo charter (Framing Brief v1 → v2 y bloque POS)

## Entradas
1. El Framing Brief v1 (obligatorio). Si no trae opción recomendada ni supuesto que cambia la decisión, detente y pídelos.
2. Lo que el equipo llenó hoy en su tablero: las razones del pre-mortem, el bloque de éxito (seis campos) y el acta (sponsor, stakeholders, alcance, permisos de la IA).
3. El Framing Brief v0, si el v1 no repite sus secciones (solicitud, afectados, A → B, ángulos, encuadres, evidencia).
Si falta algo, escribe [POR CONFIRMAR: qué falta y quién lo sabe]. No lo inventes.

## Reglas de este modo
- Siguen valiendo las reglas del SKILL.md: dato, supuesto o esperanza en cada afirmación; nada inventado.
- Cuando el equipo pega su material y pide "Pasa el contexto a acta", arma el acta con lo que pegó. No lo entrevistes: haz como máximo tres preguntas, una por mensaje, y solo por lo más grave que falte. Lo demás va como [POR CONFIRMAR] y a la lista de huecos.
- El acta se queda a nivel de encuadre: qué es éxito, quién decide, hasta dónde llega el proyecto y cuál es el siguiente paso. No es un plan.
- La decisión la toma el equipo en su panel. Tú la registras si ya existe; no la recomiendas ni la cambias. Si todavía no la tomaron, déjala como [POR CONFIRMAR: la decide el panel].

## Pasos
1. Repite textual, del v1: el A → B, la opción recomendada y el supuesto que cambia la decisión, con su prueba.
2. Revisa el bloque de éxito, campo por campo: (1) beneficio y efecto negativo a vigilar, máximo tres beneficios; (2) indicador y el instrumento que lo mide, es decir, el sistema o reporte; (3) línea base con valor, fecha y fuente; (4) meta y fecha; (5) examen intermedio y guardrail: una señal temprana de que vamos bien y algo que no debe empeorar; (6) dueños: quién recibe el beneficio, quién lo mide y quién decide si hay desviación. Cada campo está o no está.
3. Pasa las tres razones del pre-mortem que eligió el equipo al registro de supuestos, cada una con dueño y fecha de prueba.
4. Sponsor: quién decide (una persona o un rol, no un comité) y quién puede vetar, diciendo sobre qué.
5. Stakeholders: quién gana, quién pierde y quién se ve afectado. Parte de los afectados del v0.
6. Alcance: qué incluye, qué no incluye (al menos tres cosas) y las restricciones que nadie negocia.
7. Permisos de la IA en tres líneas: puede (lo que hace sola), pregunta antes (lo que necesita un sí de una persona) y nunca (lo que no hace aunque se lo pidan). Revisa que ningún permiso contradiga una restricción.
8. La decisión: go, investigar, todavía no o no-go; qué autoriza, quién es dueño del siguiente paso y cuándo se vuelve a revisar. Después entrega, en este orden: el Framing Brief v2, la revisión final con la lista de huecos y el bloque POS.

## Revisión final (entrégala siempre)
- [ ] El beneficio dice qué cambia para alguien, no qué se entrega
- [ ] Cada indicador tiene instrumento, línea base con fecha y fuente, y meta con fecha
- [ ] Hay examen intermedio y guardrail
- [ ] Los tres dueños tienen nombre o rol
- [ ] Decide una sola persona o rol, y cada veto dice sobre qué
- [ ] El alcance dice al menos tres cosas que no incluye
- [ ] Los supuestos abiertos tienen dueño y fecha de prueba, incluidos los tres del pre-mortem
- [ ] Ningún permiso de la IA contradice una restricción, y hay al menos una tarea en "nunca"
- [ ] La decisión dice qué autoriza, quién sigue y cuándo se revisa
- [ ] No hay cifras, fuentes ni personas que el equipo no mencionó
- [ ] No hay plan, hitos ni presupuesto detallado
Lista los huecos encontrados, del más grave al menos grave.

## Formato de salida: Framing Brief v2
Encabezado (versión, fecha, dueño) · Todo lo del v1 (solicitud, A → B, encuadre, opciones, opción recomendada, supuesto que cambia la decisión) · Bloque de éxito (seis campos) · Sponsor: quién decide y quién veta qué · Stakeholders: quién gana, quién pierde, quién se ve afectado · Alcance: incluye, no incluye, restricciones · Supuestos abiertos con dueño y fecha · Permisos de la IA en tres líneas · La decisión, lo que autoriza y la siguiente revisión · Huecos

## Bloque POS
Después del Brief v2 y de los huecos, entrega el bloque POS: todo el contenido del Brief (lo del v0, lo del v1 y lo del v2) en el formato de abajo, dentro de un solo bloque de código, para que el equipo lo copie y lo pegue en la página del POS.

Reglas del bloque:
- Copia los textos del Brief tal cual. No resumas, no mejores y no agregues nada. Las fechas también: usa las del Brief, no la de hoy.
- Usa exactamente estas claves y no agregues otras. Si un dato no existe, deja "" o []. Si falta y alguien lo sabe, escribe "[POR CONFIRMAR: qué falta y quién lo sabe]".
- "etiqueta" y "tipo" de una línea de valor o costo solo pueden ser: dato, supuesto o esperanza. Los semáforos: verde, amarillo o rojo. "resultado": go, investigar, todavía no o no-go.
- En "opciones" van las seis casillas en su orden; "es_la_solicitud" es true solo en la del sponsor.
- En "exito.indicadores", "fuente" es el instrumento que mide el indicador. En "exito.duenos": "beneficio" es quién recibe el beneficio, "medicion" quién lo mide y "desviaciones" quién decide si hay desviación.
- En "supuestos" van solo los del registro de supuestos del v1 y los tres del pre-mortem (estos con "fuente": "Pre-mortem"). No repitas ahí el supuesto que cambia la decisión, las líneas de valor o costo ni los hallazgos de los ángulos: ya están en su sección.
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
  "interesados": {"ganan": "", "pierden": "", "afectados": ""},
  "acta": {"dentro": [""], "fuera": [""], "restricciones": [""], "decide": "", "vetos": [""]},
  "permisos": {"puede": [""], "pregunta": [""], "nunca": [""]},
  "decision": {"resultado": "", "texto": "", "quien": "", "fecha": "", "autoriza": "", "limite": "", "dueno_siguiente_paso": "", "siguiente_revision": ""},
  "huecos": [""]
}
```

## No hagas
- Planear: cronograma, tareas, responsables de tareas o presupuesto detallado. Eso es del módulo 2.
- Cambiar o recomendar la decisión.
- Inventar metas, líneas base, fuentes, dueños o fechas.
- Dejar un campo vacío sin decirlo en la lista de huecos.
````

**Prueba rápida después de instalar:** chat nuevo, modo Work, `@framing brief, modo charter`. Debe pedir
el Framing Brief v1. Si pide otra cosa, el archivo no quedó instalado.

## B. En la sesión · demo guiada

Un equipo voluntario comparte pantalla. En cada paso, el voluntario lo hace primero y después los
demás equipos hacen lo mismo con su propia iniciativa.

**La página del POS:** [PEGAR AQUÍ EL ENLACE DE LA PÁGINA]

| Paso | Qué hace el equipo | Qué mirar en pantalla |
|---|---|---|
| 1. Así se ve un POS | Nada todavía: quien dicta abre **Ejemplo** y corre «Ver lo que viene» | La ruta, la decisión y los módulos del acta; después, doce semanas simuladas |
| 2. La skill arma el acta | Chat nuevo, modo Work: **@framing brief, modo charter**. Pegan su Framing Brief v1 y lo que llenaron en las rondas 1 a 3. Piden: **«Pasa el contexto a acta»** | Cómo repite sin reescribir, cuándo escribe «por confirmar» y la lista de huecos al final |
| 3. El acta entra al POS | Copian el bloque POS completo, de la primera `{` a la última `}`. En la página: **Mi equipo** → pegar → **Mostrar mi acta** | El medidor «Lista para firma» y los módulos con huecos |
| 4. Panel de decisión | El Sponsor lee el acta en la página, en silencio, y decide. El Escéptico da la mejor razón para no hacerlo. El PM propone qué autoriza la decisión | El módulo **Decisión**: qué autoriza, quién sigue y cuándo se revisa |
| 5. La decisión queda registrada | Le dicen a la skill qué decidieron y piden: **«vuelve a darme el bloque POS completo»**. Lo pegan en **Mi equipo → Pegar otro bloque** | El sello cambia a Go, Investigar, Todavía no o No-go |

Si la skill agrega un plan, hitos o un presupuesto detallado, sale: eso es del módulo 2.

**Pregunta para el Escéptico:** ¿qué parte de esta acta firmamos con nuestro nombre, y qué parte todavía
es fluidez sin evidencia?

## C. Recurso · cómo se hizo esta skill

Para quien quiera hacer una skill parecida para otro documento de su trabajo. Este es el pedido con el
que se puede construir un modo como el de hoy, en un chat con **@skill-creator**:

```text
Quiero agregar un modo a una skill que ya tengo. La skill acompaña a un equipo a construir un
documento por versiones. Ayúdame a escribir el archivo de referencia del modo nuevo. Hazme una
pregunta a la vez y no escribas nada hasta tener mis respuestas.

Pregúntame, en este orden:
1. Qué recibe el modo: qué versión anterior del documento es obligatoria y qué pasa si falta.
2. Qué reglas no se rompen nunca: qué no puede inventar y cómo marca lo que falta.
3. Los pasos, uno por uno: qué revisa cada paso y cómo sabe que está completo.
4. Qué no le toca hacer, aunque se lo pidan.
5. La revisión final: la lista de comprobaciones que entrega siempre.
6. El formato de salida: las secciones del documento, en orden.

Después escribe el archivo con esta estructura: Entradas · Reglas · Pasos · Revisión final ·
Formato de salida · No hagas. Al terminar, dime qué partes agregaste sin que yo las decidiera.
```

Tres ideas que hacen que una skill sea confiable, y que están en la de hoy:

- **Dice qué hacer cuando falta algo.** Escribe «por confirmar: qué falta y quién lo sabe» en lugar de rellenar.
- **Dice qué no le toca.** Si le piden un cronograma, responde que eso es de otro momento.
- **Termina revisándose.** Entrega siempre la lista de huecos, del más grave al menos grave.
