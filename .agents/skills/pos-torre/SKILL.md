---
name: pos-torre
description: Construye y lee la torre de control de un POS - estado de la semana, alertas, brief ejecutivo y escenarios de crisis. Úsala cuando pidan "construir la torre", "cómo va el proyecto", "el brief de la semana", "qué necesita decisión" o al preparar una revisión con el patrocinador o un War Room.
---

# Torre de control

La torre compara el pulso contra el acta y el plan. Los números y las alertas salen de reglas fijas
(`torre/motor.py`), no de tu criterio: tu trabajo es correrla, explicarla y redactar.

## Comandos

```
python3 torre/construir.py <carpeta>              # escribe <carpeta>/torre.html
python3 torre/construir.py <carpeta> --revisar    # revisa la forma de los registros
python3 torre/construir.py <carpeta> --brief      # imprime el brief de la última semana
python3 torre/construir.py <carpeta> --semana 6   # como si hoy fuera la semana 6
python3 torre/construir.py <carpeta> --etapa contexto   # abre en la capa 1 (también: plan, pulso, torre)
```

`torre.html` es un solo archivo: se abre con doble clic y se puede compartir.

## Cómo leerla con el equipo

1. Estado y alertas críticas: qué regla se disparó y desde qué semana.
2. «De la señal a la decisión»: cuántas semanas pasaron entre la primera señal y la decisión.
3. Indicadores sin medir y pruebas vencidas: lo que no tiene dato detrás.
4. Qué decisión hace falta y de quién es. La torre no decide.

## Brief para quien decide

Parte del brief que imprime `--brief`. Puedes reescribirlo para que se lea mejor, con estas reglas:

- Toda cifra debe coincidir con la torre. Si no está en los registros, no va.
- Tres bloques: qué cambió, qué necesita decisión y de quién, qué no tiene dato detrás.
- Cierra con: «Borrador hecho con IA a partir de los registros. Exactitud a cargo de: [nombre]».
- Enviar el brief es una acción de «pregunta antes», salvo que `permisos.csv` diga otra cosa.

## Modo War Room

Construye la torre cortada en la semana de la crisis (`--semana N --salida crisis.html`) y trabaja solo
con lo que se sabía entonces. Entrega: qué señales ya estaban, qué decisión faltó, dos opciones de
recuperación con su costo y lo que cada una deja fuera, y el mensaje para el patrocinador.

## Lo que no debes hacer

- Cambiar registros para que una alerta desaparezca.
- Presentar el brief como aprobado. Es un borrador hasta que una persona lo firma.
- Inventar causas. Si los registros no explican algo, dilo.
