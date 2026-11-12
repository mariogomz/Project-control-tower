# Cómo se llena un POS

Un POS es una carpeta. Cada archivo responde una pregunta. Se abren con Excel, Google Sheets o
cualquier editor de texto, y tu agente (Codex, Claude Code) también los lee y los escribe.

Copia esta carpeta a `equipos/<nombre-de-tu-equipo>/` y trabaja ahí. El caso resuelto está en
`ejemplos/faro/`.

## Capa 1 · Contexto (módulo 1)

**`pos.json`** · la ficha del proyecto.

| Campo | Qué va |
|---|---|
| `proyecto`, `organizacion`, `equipo` | Nombres |
| `sponsor`, `decide`, `vetos`, `pm` | Quién patrocina, quién decide, quién puede frenar, quién lleva el proyecto |
| `a`, `b` | De dónde venimos y a dónde vamos, una frase cada uno |
| `dentro`, `fuera`, `restricciones` | Listas cortas |
| `inicio` | Fecha de arranque, `AAAA-MM-DD` |
| `semanas`, `moneda`, `presupuesto` | Duración, moneda y techo aprobado |
| `condiciones_corte` | Opcional. Qué resultado obliga a decidir si el proyecto sigue: `{"texto": "...", "indicador": "I1", "si": "<", "valor": 60, "semana": 6}` |

**`contexto/acta.md`** · el acta completa, tal como la firmó el equipo.

**`registros/indicadores.csv`** · qué es éxito y cómo se mide.

| Columna | Qué va |
|---|---|
| `id` | `I1`, `I2`… |
| `nombre` | Qué se mide |
| `tipo` | `adelantado` (avisa antes) o `rezagado` (confirma después) |
| `unidad` | `%`, `días`, `quejas`… |
| `linea_base`, `meta` | Dónde estamos y a dónde queremos llegar |
| `ambar`, `rojo` | Umbrales. A partir de dónde hay que poner atención y a partir de dónde hay que decidir |
| `sentido` | `sube` si más es mejor, `baja` si menos es mejor |
| `fuente` | De qué reporte o sistema sale el dato |
| `dueno` | Quién responde por este indicador |
| `cadencia_semanas` | Cada cuántas semanas se mide |
| `desde_semana` | A partir de qué semana tiene sentido evaluarlo |

**`registros/supuestos.csv`** · lo que tiene que ser cierto.
`id` (`S1`…), `supuesto`, `si_falla`, `prueba`, `dueno`, `semana_prueba`, `estado` (`sin_probar`, `validado`, `en_duda`, `roto`).

**`registros/riesgos.csv`** · lo que salió del pre-mortem.
`id` (`R1`…), `riesgo`, `senal_temprana`, `probabilidad` (1 a 5), `impacto` (1 a 5), `dueno`, `respuesta`, `semana_impacto`, `estado` (`abierto`, `materializado`, `mitigado`, `cerrado`).

**`registros/permisos.csv`** · qué puede hacer la IA sola.
`accion`, `nivel` (`puede`, `pregunta`, `nunca`), `nota`.

**`registros/decisiones.csv`** · quién decidió qué.
`semana`, `decision`, `decide`, `refs` (a qué responde, por ejemplo `S3;R1`), `por_que`.

## Capa 2 · Plan (módulo 2)

**`plan/hitos.csv`** · `id` (`H1`…), `hito`, `semana_plan`, `peso` (cuánto del proyecto representa; lo usual es que sumen 100), `dueno`.

**`plan/presupuesto.csv`** · `semana`, `plan_acumulado` (cuánto se planea haber gastado al cierre de esa semana).

Si tu plan vive en Jira u otra herramienta, exporta y pídele a tu agente que lo pase a estas dos tablas.

## Capa 3 · Pulso (módulo 3)

Aquí solo se agregan filas; no se borra ni se corrige el pasado.

**`pulso/mediciones.csv`** · `semana`, `indicador`, `valor`, `fuente`. Si esa semana no hubo dato, no hay fila.

**`pulso/hitos.csv`** · `semana`, `hito`, `estado` (`pendiente`, `en_curso`, `hecho`), `avance` (0 a 100), `semana_pronostico`. Solo los hitos que cambiaron.

**`pulso/gasto.csv`** · `semana`, `real_acumulado`.

**`pulso/bitacora.csv`** · `semana`, `tipo`, `ref`, `estado`, `texto`, `fuente`.

| `tipo` | Qué es | `estado` |
|---|---|---|
| `senal` | Algo que alguien dijo o reportó, citado textual, y a qué apunta (`ref`) | vacío |
| `supuesto` | Un supuesto cambió de estado; `texto` es la evidencia | `validado`, `en_duda`, `roto` |
| `riesgo` | Un riesgo cambió de estado | `materializado`, `mitigado`, `cerrado` |
| `cambio` | Cambio aprobado de alcance, fecha o presupuesto | vacío |

**`pulso/notas/semana-NN.md`** · la minuta o las notas de la semana, sin editar.

## Capa 4 · Torre (módulo 4)

```
python3 torre/construir.py equipos/<nombre> --revisar   # ¿están bien formados los registros?
python3 torre/construir.py equipos/<nombre>             # escribe torre.html
```

`torre.html` se abre con doble clic.
