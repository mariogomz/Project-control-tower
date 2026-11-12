"""Escribe los registros del caso Aseguradora Faro («Estatus sin llamar»).

El acta, los indicadores, los supuestos y los permisos salen del caso trabajado
en el módulo 1. La ejecución de las semanas 1 a 12 es SIMULADA: sirve para ver
cómo se comporta una torre con datos, y como material para el War Room.

Uso:  python3 ejemplos/faro/_escenario.py
Edita las tablas de abajo y vuelve a correrlo para crear variantes.
"""
import csv
import json
from pathlib import Path

AQUI = Path(__file__).parent
DIR = "Director de Experiencia del Cliente"


def escribir(rel, columnas, filas):
    ruta = AQUI / rel
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(columnas)
        w.writerows(filas)


# ------------------------------------------------------------------ contexto (M1)

POS = {
    "proyecto": "Estatus sin llamar",
    "organizacion": "Aseguradora Faro",
    "nota": "Caso ficticio del curso. La ejecución de las semanas 1 a 12 es simulada.",
    "equipo": "Equipo de ejemplo",
    "sponsor": DIR,
    "decide": DIR,
    "vetos": ["Legal (autenticación)", "TI (presupuesto)"],
    "pm": "PM del proyecto",
    "a": "Los clientes con siniestro activo no saben en qué estado está su trámite: 46% de los contactos preguntan por el estatus y los avisos automáticos están apagados desde febrero.",
    "b": "El cliente con siniestro activo sabe cómo va su trámite sin llamar, y Grupo Industrial del Bajío se queda.",
    "dentro": ["Reactivar avisos", "Medir el SLA del despacho", "Ejecutivo para GIB"],
    "fuera": ["Chatbot en la app", "Canales nuevos", "Renegociar el contrato del despacho"],
    "restricciones": ["Cualquier canal de siniestros autentica al cliente (Legal)",
                      "≤1.2 M MXN en Q4 (TI)", "Antes de diciembre"],
    "inicio": "2026-09-07",
    "semanas": 12,
    "moneda": "MXN",
    "presupuesto": 400000,
    "condiciones_corte": [{
        "texto": "en la semana 6 los avisos llegan a menos de 60% de los siniestros abiertos",
        "indicador": "I1", "si": "<", "valor": 60, "semana": 6,
    }],
}

INDICADORES = [
    # id, nombre, tipo, unidad, base, meta, ámbar, rojo, sentido, fuente, dueño, cadencia, desde
    ("I1", "Siniestros abiertos que reciben aviso", "adelantado", "%", 0, 90, 80, 60, "sube",
     "Bitácora de envíos de la plataforma de avisos", "PM del proyecto", 1, 4),
    ("I2", "Contactos que preguntan por estatus", "rezagado", "%", 46, 30, 34, 40, "baja",
     "Clasificación de contactos del call center", "Dirección de Siniestros", 1, 6),
    ("I3", "Abandono de llamadas", "rezagado", "%", 18, 10, 14, 17, "baja",
     "Reporte telefónico, todas las llamadas", "Dirección de Siniestros", 1, 6),
    ("I4", "Siniestros dentro del SLA de 10 días del despacho", "adelantado", "%", "", 80, 65, 45, "sube",
     "Reporte semanal del despacho de ajustadores", "Compras", 1, 3),
    ("I5", "Quejas formales por semana", "rezagado", "quejas", 34, 34, 38, 45, "baja",
     "Registro de quejas de Atención a Clientes", "PM del proyecto", 1, 4),
]

SUPUESTOS = [
    # id, supuesto, si falla, prueba, dueño, semana de prueba
    ("S1", "Si el cliente recibe el aviso de estatus, deja de llamar.",
     "La causa de fondo es el despacho y conviene la opción más ambiciosa.",
     "Reactivar avisos para un tipo de siniestro durante 2 semanas y comparar.", "PM del proyecto", 5),
    ("S2", "46% de los contactos preguntan por el estatus.",
     "El beneficio en llamadas evitadas es menor al del caso.",
     "Reclasificar una muestra de 400 contactos.", "Dirección de Siniestros", 2),
    ("S3", "Los avisos automáticos se pueden reactivar sobre el sistema migrado sin desarrollo nuevo.",
     "El costo y la fecha del caso dejan de ser válidos.",
     "TI enciende los avisos en ambiente de prueba.", "TI", 2),
    ("S4", "Legal aprueba avisos por SMS si el cliente se autentica.",
     "No hay canal para avisar antes de diciembre.",
     "Legal revisa las plantillas de aviso.", "Legal", 3),
    ("S5", "GIB espera a ver resultados antes de decidir su renovación.",
     "Se pierden ~US$480 mil al año en primas aunque el proyecto salga bien.",
     "El ejecutivo de la cuenta lo confirma con GIB.", DIR, 6),
    ("S6", "El costo cabe en el techo de 400 mil MXN (estimado de TI).",
     "Hay que volver con el patrocinador y con TI por presupuesto.",
     "Comparar gasto real contra estimado en la semana 4.", "PM del proyecto", 4),
]

RIESGOS = [
    # id, riesgo, señal temprana, prob, impacto, dueño, respuesta, semana de impacto
    ("R1", "Los avisos dicen «sigue en revisión» y las llamadas no bajan.",
     "Los contactos de estatus no bajan dos semanas después de encender avisos.", 4, 4,
     "PM del proyecto", "Aviso con fecha estimada y siguiente paso, no solo el estatus.", 7),
    ("R2", "El despacho sigue tardando 23 días.",
     "Menos de 45% de los siniestros dentro del SLA de 10 días.", 4, 5,
     "Dirección de Siniestros", "Escalar a Compras y abrir la renegociación del contrato como proyecto aparte.", 8),
    ("R3", "Legal frena los SMS por datos personales.",
     "Legal pide revisar plantillas o no responde en 5 días hábiles.", 3, 4,
     "PM del proyecto", "Aviso sin datos del siniestro, con enlace que exige autenticación.", 4),
    ("R4", "GIB se va antes de ver resultados.",
     "GIB pide reunión con dirección, cotiza con otra aseguradora o deja de contestar.", 3, 5,
     DIR, "Ejecutivo dedicado y reporte quincenal a GIB con sus siniestros.", 9),
]

PERMISOS = [
    ("Analizar datos agregados de contactos", "puede", "Del acta"),
    ("Redactar borradores internos: brief, minuta, reporte", "puede", "Del acta"),
    ("Registrar en el pulso una medición que viene de un reporte oficial", "puede", "Regla de la torre"),
    ("Avisar al PM cuando un indicador sale de rango", "puede", "Del acta"),
    ("Cualquier texto para clientes", "pregunta", "Del acta"),
    ("Cualquier compromiso de gasto", "pregunta", "Del acta"),
    ("Cualquier cosa que toque la autenticación", "pregunta", "Del acta"),
    ("Cambiar el estado de un supuesto o de un riesgo", "pregunta", "Regla de la torre"),
    ("Enviar el brief al patrocinador", "pregunta", "Regla de la torre"),
    ("Proponer un canal de siniestros sin autenticación", "nunca", "Del acta"),
    ("Citar el «−70%» del proveedor o el 6% de abandono como evidencia", "nunca", "Del acta"),
    ("Cambiar metas, umbrales o la línea base", "nunca", "Regla de la torre"),
    ("Escribirle a un cliente", "nunca", "Del acta: ninguna IA sola"),
]

DECISIONES = [
    # semana, decisión, decide, refs, por qué
    (0, "GO: pasa a planeación con un techo de 400 mil MXN. El chatbot: todavía no, cuando existan datos de los avisos.",
     DIR, "", "El chatbot no pasa el filtro: US$150 mil contra US$64 mil disponibles y sin autenticación fuerte."),
    (5, "El aviso no lleva datos del siniestro; lleva un enlace que exige autenticación.",
     DIR + ", con visto bueno de Legal", "S4;R3", "Cumple la restricción de autenticación sin frenar el envío."),
    (7, "Cambiar el aviso: fecha estimada y siguiente paso, alimentado por un archivo diario del despacho. Primero autos y los siniestros de GIB.",
     DIR, "S3;S1;R1;I1", "La prueba mostró que el aviso «sigue en revisión» baja las llamadas 9%; con fecha estimada, 31%."),
    (7, "Subir el techo de 400 a 520 mil MXN y mover los avisos completos de la semana 8 a la 11.",
     DIR + ", con visto bueno de TI", "S6;H7", "La integración con el despacho no estaba en el estimado."),
    (7, "Reporte quincenal a GIB con el estado de sus siniestros, a cargo del nuevo ejecutivo.",
     DIR, "R4;S5;H2", "GIB avisó que no renovará en enero si no ve cambios."),
    (7, "Compras exige al despacho el reporte semanal de SLA que marca el contrato.",
     DIR, "R2;I4", "Dos semanas sin reporte: no se puede gobernar lo que no se mide."),
    (12, "La renegociación del contrato del despacho se abre como proyecto aparte, antes de marzo de 2027.",
     DIR, "R2;I4", "Los avisos ya funcionan, pero el trámite sigue lejos del SLA de 10 días."),
]

# ------------------------------------------------------------------ plan (M2)

HITOS = [
    # id, hito, semana plan, peso, dueño
    ("H1", "Acta firmada y línea base medida", 1, 5, "PM del proyecto"),
    ("H2", "Ejecutivo asignado a la cuenta GIB", 2, 10, DIR),
    ("H3", "Avisos encendidos en ambiente de prueba", 3, 15, "TI"),
    ("H4", "Plantillas de aviso aprobadas por Legal", 3, 10, "Legal"),
    ("H5", "Prueba de 2 semanas con siniestros de autos", 5, 15, "PM del proyecto"),
    ("H6", "Tablero de SLA del despacho funcionando", 4, 10, "Compras"),
    ("H7", "Avisos para todos los siniestros abiertos", 8, 20, "TI"),
    ("H8", "Primera revisión con el patrocinador", 6, 5, "PM del proyecto"),
    ("H9", "Reporte de beneficios y decisión sobre la fase 2", 12, 10, "Dirección de Siniestros"),
]

PRESUPUESTO = [0, 20, 60, 140, 190, 245, 275, 315, 355, 370, 380, 390, 400]  # miles, acumulado

# ------------------------------------------------------------------ pulso (M3) — simulado

MEDICIONES = {
    "I1": {4: 27, 5: 29, 6: 31, 7: 34, 8: 48, 9: 66, 10: 81, 11: 92, 12: 94},
    "I2": {1: 46, 2: 44, 3: 45, 4: 46, 5: 45, 6: 45, 7: 44, 8: 41, 9: 38, 10: 35, 11: 32, 12: 30},
    "I3": {1: 18, 2: 18.2, 3: 17.9, 4: 18.4, 5: 18.6, 6: 18.5, 7: 19, 8: 17.5, 9: 16, 10: 14.5, 11: 13, 12: 12},
    "I4": {3: 38, 4: 40, 5: 41, 8: 44, 9: 52, 10: 58, 11: 61, 12: 63},  # semanas 6 y 7: el despacho no envió reporte
    "I5": {1: 34, 2: 33, 3: 35, 4: 36, 5: 36, 6: 41, 7: 47, 8: 43, 9: 37, 10: 33, 11: 32, 12: 31},
}

AVANCE = [
    # semana, hito, estado, avance %, semana de pronóstico
    (1, "H1", "hecho", 100, 1),
    (2, "H2", "en_curso", 30, 4), (2, "H3", "en_curso", 40, 3), (2, "H4", "en_curso", 20, 3),
    (3, "H2", "en_curso", 50, 4), (3, "H3", "en_curso", 70, 4), (3, "H4", "en_curso", 50, 5),
    (3, "H6", "en_curso", 50, 4),
    (4, "H2", "hecho", 100, 4), (4, "H3", "hecho", 100, 4), (4, "H4", "en_curso", 60, 5),
    (4, "H6", "hecho", 100, 4),
    (5, "H4", "hecho", 100, 5), (5, "H5", "en_curso", 30, 7), (5, "H7", "en_curso", 10, 9),
    (6, "H5", "en_curso", 70, 7), (6, "H7", "en_curso", 15, 10), (6, "H8", "pendiente", 0, 7),
    (7, "H5", "hecho", 100, 7), (7, "H7", "en_curso", 20, 11), (7, "H8", "hecho", 100, 7),
    (8, "H7", "en_curso", 35, 11), (9, "H7", "en_curso", 55, 11), (10, "H7", "en_curso", 75, 11),
    (11, "H7", "hecho", 100, 11), (11, "H9", "en_curso", 30, 13),
    (12, "H9", "en_curso", 70, 13),
]

GASTO = [0, 22, 66, 150, 215, 270, 318, 362, 385, 405, 422, 440, 455]  # miles, acumulado real

BITACORA = [
    # semana, tipo, ref, estado, texto, fuente
    (1, "senal", "S3", "", "La documentación de avisos que tenemos es el manual de 2023, anterior a la migración de febrero.", "Reunión semanal con TI"),
    (2, "senal", "S3;R2", "", "El evento de cambio de estatus no llega desde el portal del despacho; solo lo vemos en los siniestros que ajustamos en casa.", "Reunión semanal con TI"),
    (2, "senal", "H2;R4", "", "La vacante del ejecutivo de GIB entra a la fila con las otras seis.", "Correo de Recursos Humanos"),
    (2, "senal", "S4;R3", "", "Antes de cualquier envío queremos ver las plantillas. No podemos dar fecha.", "Correo de Legal"),
    (2, "supuesto", "S2", "validado", "Muestra de 400 contactos reclasificada: 44% preguntan por el estatus.", "Dirección de Siniestros"),
    (2, "supuesto", "S3", "en_duda", "En ambiente de prueba los avisos solo salen para siniestros ajustados en casa.", "TI"),
    (3, "senal", "S3;R2", "", "El despacho actualiza el estatus en su portal una vez por semana, en lote.", "Llamada con el despacho"),
    (3, "senal", "R2;I4", "", "Primera medición: 38% de los siniestros dentro del SLA de 10 días. El despacho cuestiona cómo se midió.", "Tablero de SLA"),
    (3, "senal", "S4;R3", "", "Legal no ha respondido en 6 días hábiles.", "Seguimiento del PM"),
    (3, "supuesto", "S4", "en_duda", "Legal no confirma; pide revisar las plantillas.", "Legal"),
    (4, "senal", "R4;S5", "", "GIB pidió reunión con dirección y preguntó por tres siniestros abiertos.", "Correo del ejecutivo de GIB"),
    (4, "senal", "S6;H7", "", "Integrar el archivo diario del despacho no estaba en el estimado. Serían unos 180 mil MXN más.", "Reunión semanal con TI"),
    (4, "supuesto", "S3", "roto", "TI confirma que 70% de los siniestros, los del despacho, no generan evento de estatus. Reactivar no alcanza: hace falta integrar un archivo diario.", "TI"),
    (4, "supuesto", "S6", "en_duda", "La integración suma unos 180 mil MXN al estimado.", "TI"),
    (5, "senal", "S6;H7", "", "TI mueve la fecha de avisos completos por segunda vez.", "Reunión semanal con TI"),
    (5, "supuesto", "S4", "validado", "Legal aprueba el aviso sin datos del siniestro, con enlace que exige autenticación.", "Legal"),
    (5, "riesgo", "R3", "mitigado", "Plantillas aprobadas con el formato de enlace autenticado.", "Legal"),
    (6, "senal", "R1;S1", "", "En la prueba, 4 de cada 10 clientes que reciben «sigue en revisión» llaman ese mismo día.", "Supervisoras del call center"),
    (6, "senal", "R4;S5", "", "GIB pidió cotización a otra aseguradora.", "Corredor de GIB"),
    (6, "senal", "I4;R2", "", "El despacho no envió el reporte semanal.", "Compras"),
    (6, "supuesto", "S5", "en_duda", "GIB pidió cotización a otra aseguradora.", "Corredor de GIB"),
    (7, "senal", "R4;S5", "", "GIB avisa que no renovará en enero si no ve cambios.", "Reunión con GIB"),
    (7, "supuesto", "S1", "en_duda", "Con el aviso actual las llamadas de estatus bajan 9%. Con fecha estimada y siguiente paso bajan 31%.", "Resultado de la prueba de 2 semanas"),
    (7, "riesgo", "R1", "materializado", "Los avisos «sigue en revisión» no bajan las llamadas y suben las quejas.", "Resultado de la prueba de 2 semanas"),
    (7, "supuesto", "S5", "roto", "GIB avisa que no renovará en enero si no ve cambios.", "Reunión con GIB"),
    (7, "supuesto", "S6", "roto", "El costo proyectado supera el techo de 400 mil MXN.", "PM del proyecto"),
    (7, "cambio", "", "", "Alcance: avisos con fecha estimada y siguiente paso, alimentados por archivo diario del despacho; primero autos y GIB. El techo sube de 400 a 520 mil MXN. Los avisos completos pasan de la semana 8 a la 11.", "Revisión con el patrocinador"),
    (9, "senal", "R4", "", "GIB recibió el primer reporte quincenal de sus siniestros y acepta esperar a marzo.", "Ejecutivo de GIB"),
    (9, "supuesto", "S1", "validado", "Con fecha estimada, la baja de 31% en llamadas de estatus se sostiene tres semanas.", "Clasificación de contactos"),
    (9, "riesgo", "R1", "mitigado", "El aviso nuevo ya está en autos y en los siniestros de GIB.", "PM del proyecto"),
    (9, "riesgo", "R4", "mitigado", "GIB acepta esperar a marzo tras el primer reporte quincenal.", "Ejecutivo de GIB"),
    (9, "supuesto", "S5", "validado", "Con el reporte quincenal, GIB acepta esperar a marzo.", "Ejecutivo de GIB"),
    (10, "senal", "R2;I4", "", "El despacho pide revisar el SLA de 10 días; dice que con el volumen actual no es alcanzable.", "Compras"),
]

NOTAS = {
    3: """# Reunión semanal · semana 3

Asistentes: PM, TI, Compras, Dirección de Siniestros.

- TI: avisos en ambiente de prueba al 70%. Funcionan para los siniestros que Faro ajusta en casa.
  Para los del despacho no hay evento: el despacho actualiza el estatus en su portal una vez por
  semana, en lote. TI «lo va a revisar».
- Compras: primer corte del tablero de SLA. 38% de los siniestros dentro de los 10 días.
  El despacho cuestiona cómo se midió y pide ver el detalle.
- Legal no vino. Lleva 6 días hábiles sin responder sobre las plantillas.
- RH: la vacante del ejecutivo de GIB sigue en fila. Fecha probable: semana 4.

Acuerdos: TI revisa lo del evento. Compras manda el detalle al despacho. PM insiste con Legal.
Nadie quedó a cargo de decidir qué pasa si los avisos no cubren los siniestros del despacho.
""",
    6: """# Reunión semanal · semana 6

Asistentes: PM, TI, Compras, supervisoras del call center. El patrocinador está de viaje:
la primera revisión se mueve a la semana 7.

- Prueba con siniestros de autos, semana 2 de 2: los avisos llegan a 31% de los siniestros
  abiertos. Las supervisoras reportan que 4 de cada 10 clientes que reciben «sigue en revisión»
  llaman ese mismo día. Las quejas subieron de 36 a 41.
- TI: la fecha de avisos completos pasa a la semana 10. Insisten en los 180 mil MXN adicionales
  para integrar el archivo diario del despacho.
- Compras: el despacho no envió el reporte semanal de SLA.
- El corredor de GIB comenta que GIB pidió cotización a otra aseguradora.

Acuerdos: esperar a la revisión con el patrocinador.
""",
    7: """# Primera revisión con el patrocinador · semana 7

Asistentes: Director de Experiencia del Cliente, PM, TI, Legal, Compras, Dirección de Siniestros.

Resultado de la prueba de 2 semanas: con el aviso actual las llamadas de estatus bajan 9%
(el caso suponía entre 25% y 45%). En el grupo que recibió aviso con fecha estimada y siguiente
paso, bajan 31%. Quejas de la semana: 47.

GIB avisó ayer que no renovará en enero si no ve cambios.

Decisiones del director:
1. El aviso cambia: fecha estimada y siguiente paso, alimentado por un archivo diario del despacho.
   Primero autos y los siniestros de GIB.
2. El techo sube de 400 a 520 mil MXN (TI de acuerdo). Avisos completos: semana 11.
3. Reporte quincenal a GIB con el estado de sus siniestros, a cargo del nuevo ejecutivo.
4. Compras exige al despacho el reporte semanal de SLA que marca el contrato.

El chatbot sigue fuera.
""",
}

ACTA = """# Acta de arranque · Estatus sin llamar

Aseguradora Faro · caso ficticio del curso

## De dónde venimos y a dónde vamos

**Solicitud original.** «Necesitamos un chatbot en la app antes de diciembre. Los clientes se
quejan de que no les contestamos.» La pide el director de Experiencia del Cliente.

**El problema.** Los clientes con siniestro activo no saben en qué estado está su trámite.
Lo sabemos porque 46% de los contactos preguntan por el estatus y los avisos automáticos están
apagados desde febrero. Nos falta saber cuántos dejarían de llamar si recibieran el aviso.

**A dónde vamos.** El cliente con siniestro activo sabe cómo va su trámite sin llamar, y Grupo
Industrial del Bajío se queda.

## El proyecto

Avisos automáticos de estatus + un dueño para la cuenta de GIB + medir el SLA del despacho.

| | |
|---|---|
| **Dentro** | Reactivar avisos · medir el SLA del despacho · ejecutivo para GIB |
| **Fuera** | Chatbot en la app · canales nuevos · renegociar el contrato del despacho |
| **Restricciones** | Cualquier canal de siniestros autentica al cliente (Legal) · ≤1.2 M MXN en Q4 (TI) · antes de diciembre |
| **Decide** | El director que patrocina |
| **Vetos** | Legal (autenticación) · TI (presupuesto) |

## Qué es éxito

| Campo | Faro |
|---|---|
| Beneficio | El cliente sabe cómo va su siniestro sin llamar; GIB renueva |
| Efecto negativo a vigilar | Más difícil hablar con una persona |
| Indicador | % de contactos de estatus (clasificación del call center) y abandono (reporte telefónico, todas las llamadas) |
| Línea base | 46% de contactos de estatus · 18% de abandono · trámite de 23 días |
| Meta | Contactos de estatus 25–30% y abandono ≤10% en dos trimestres |
| Examen intermedio | Avisos llegando a ≥90% de los siniestros abiertos en la semana 4 · las quejas no suben |
| Dueños | Beneficio: dirección de Siniestros · medición: el PM · desviaciones: el director que patrocina |

## Supuesto abierto

Si el cliente recibe el aviso, deja de llamar. Prueba de 2 semanas. Dueño: el PM.

## Decisión

**GO.** Pasa a planeación con un techo de 400 mil MXN. El chatbot: todavía no, cuando existan
datos de los avisos.

## Qué puede hacer la IA

| Puede | Pregunta antes | Nunca |
|---|---|---|
| Analizar datos agregados de contactos y redactar borradores internos | Cualquier texto para clientes, cualquier compromiso de gasto, cualquier cosa que toque la autenticación | Proponer un canal de siniestros sin autenticación; citar el «−70%» del proveedor o el 6% de abandono como evidencia |

---

Los registros de esta carpeta (`registros/`) son esta misma acta en forma de tablas: es lo que
la torre lee para saber qué vigilar.
"""


def main():
    (AQUI / "pos.json").write_text(json.dumps(POS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (AQUI / "contexto").mkdir(exist_ok=True)
    (AQUI / "contexto" / "acta.md").write_text(ACTA, encoding="utf-8")

    escribir("registros/indicadores.csv",
             ["id", "nombre", "tipo", "unidad", "linea_base", "meta", "ambar", "rojo", "sentido",
              "fuente", "dueno", "cadencia_semanas", "desde_semana"], INDICADORES)
    escribir("registros/supuestos.csv",
             ["id", "supuesto", "si_falla", "prueba", "dueno", "semana_prueba", "estado"],
             [s + ("sin_probar",) for s in SUPUESTOS])
    escribir("registros/riesgos.csv",
             ["id", "riesgo", "senal_temprana", "probabilidad", "impacto", "dueno", "respuesta",
              "semana_impacto", "estado"], [r + ("abierto",) for r in RIESGOS])
    escribir("registros/permisos.csv", ["accion", "nivel", "nota"], PERMISOS)
    escribir("registros/decisiones.csv", ["semana", "decision", "decide", "refs", "por_que"], DECISIONES)

    escribir("plan/hitos.csv", ["id", "hito", "semana_plan", "peso", "dueno"], HITOS)
    escribir("plan/presupuesto.csv", ["semana", "plan_acumulado"],
             [(i, v * 1000) for i, v in enumerate(PRESUPUESTO)])

    escribir("pulso/mediciones.csv", ["semana", "indicador", "valor", "fuente"],
             sorted((sem, ind, val, next(i[9] for i in INDICADORES if i[0] == ind))
                    for ind, serie in MEDICIONES.items() for sem, val in serie.items()))
    escribir("pulso/hitos.csv", ["semana", "hito", "estado", "avance", "semana_pronostico"], AVANCE)
    escribir("pulso/gasto.csv", ["semana", "real_acumulado"],
             [(i, v * 1000) for i, v in enumerate(GASTO) if i > 0])
    escribir("pulso/bitacora.csv", ["semana", "tipo", "ref", "estado", "texto", "fuente"], BITACORA)
    for sem, texto in NOTAS.items():
        ruta = AQUI / "pulso" / "notas" / f"semana-{sem:02d}.md"
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(texto, encoding="utf-8")
    print("Caso Faro escrito en", AQUI)


if __name__ == "__main__":
    main()
