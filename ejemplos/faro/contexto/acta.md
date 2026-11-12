# Acta de arranque · Estatus sin llamar

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
