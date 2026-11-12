#!/usr/bin/env python3
"""Construye la torre de control de una carpeta POS.

    python3 torre/construir.py ejemplos/faro              # escribe ejemplos/faro/torre.html
    python3 torre/construir.py ejemplos/faro --semana 6   # corta los datos en la semana 6
    python3 torre/construir.py ejemplos/faro --revisar    # solo revisa los registros
    python3 torre/construir.py ejemplos/faro --brief      # imprime el brief de la semana

El resultado es un solo archivo HTML que se abre con doble clic, sin servidor.
Solo usa la biblioteca estándar de Python.
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import motor  # noqa: E402

THREE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.min.js"
ETAPAS = ["contexto", "plan", "pulso", "torre"]


def datos(pos, hasta=None, etapa=None):
    estados = motor.linea_de_tiempo(pos, hasta)
    n = int(pos["meta"].get("semanas") or 0) or max((h["semana_plan"] for h in pos["hitos"]), default=0)
    bac = estados[0]["evm"]["bac"]
    peso = sum(h["peso"] for h in pos["hitos"]) or 1
    plan = []
    for w in range(n + 1):
        pv = motor._acumulado(pos["presupuesto"], w)
        if pv is not None and bac:
            plan.append(pv / bac)
        elif pos["hitos"]:
            plan.append(sum(h["peso"] for h in pos["hitos"] if h["semana_plan"] <= w) / peso)
        else:
            plan.append(None)
    capas = pos["capas"]
    maxima = 4 if capas["pulso"] else 2 if capas["plan"] else 1
    inicial = min(maxima, ETAPAS.index(etapa) + 1) if etapa else maxima
    return {
        "meta": pos["meta"], "semanas": n, "capas": capas,
        "etapa_maxima": maxima, "etapa_inicial": inicial,
        "indicadores": pos["indicadores"], "supuestos": pos["supuestos"], "riesgos": pos["riesgos"],
        "permisos": pos["permisos"], "hitos": pos["hitos"], "plan": plan,
        "fechas": [motor.fecha_semana(pos, w) for w in range(n + 3)],
        "estados": estados, "generado": date.today().isoformat(),
    }


def html(d, three="inline", artefacto=False):
    plantilla = (AQUI / "plantilla.html").read_text(encoding="utf-8")
    cabeza, cuerpo = plantilla.split("<!--CUERPO-->")
    if three == "cdn":
        lib = f'<script src="{THREE_CDN}"></script>'
    else:
        fuente = (AQUI / "vendor" / "three.min.js").read_text(encoding="utf-8")
        if fuente.startswith("console.warn("):  # aviso de obsolescencia del paquete; no aporta en la torre
            fuente = "!" + fuente[fuente.index("/**"):]
        lib = "<script>" + fuente + "</script>"
    carga = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    cuerpo = cuerpo.replace("<!--THREE-->", lib).replace("/*__DATOS__*/null", carga)
    titulo = f"Torre · {d['meta'].get('proyecto', 'POS')}"
    cabeza = cabeza.replace("__TITULO__", titulo)
    if artefacto:  # vista previa publicada: el visor pone su propio esqueleto
        marca = '<meta name="' + "cl" + 'aude:viewport-fit-sides" content="cover">\n'
        return cabeza.replace("</title>\n", "</title>\n" + marca, 1) + cuerpo
    return ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + cabeza + "</head>\n<body>\n" + cuerpo + "</body>\n</html>\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Construye la torre de control de una carpeta POS.")
    ap.add_argument("carpeta", help="carpeta del POS (la que contiene pos.json)")
    ap.add_argument("--semana", type=int, help="usar solo los datos hasta esta semana")
    ap.add_argument("--etapa", choices=ETAPAS, help="capa que se muestra al abrir")
    ap.add_argument("--salida", help="archivo de salida (por defecto <carpeta>/torre.html)")
    ap.add_argument("--three", choices=["inline", "cdn"], default="inline",
                    help="inline: funciona sin internet; cdn: archivo más ligero")
    ap.add_argument("--artefacto", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--revisar", action="store_true", help="solo revisar los registros")
    ap.add_argument("--brief", action="store_true", help="imprimir el brief de la semana")
    a = ap.parse_args(argv)

    pos = motor.cargar(a.carpeta)
    problemas = motor.revisar(pos)
    if problemas:
        print(f"Revisión: {len(problemas)} problema(s) en los registros")
        for p in problemas:
            print("  -", p)
    else:
        print("Revisión: registros en orden")
    if a.revisar:
        return 1 if problemas else 0

    d = datos(pos, a.semana, a.etapa)
    ultimo = d["estados"][-1]
    if a.brief:
        print()
        print(ultimo["brief"])
        return 0
    salida = Path(a.salida) if a.salida else Path(a.carpeta) / "torre.html"
    salida.write_text(html(d, a.three, a.artefacto), encoding="utf-8")
    crit = sum(1 for x in ultimo["alertas"] if x["severidad"] == "critica")
    print(f"Torre escrita en {salida}")
    print(f"Semana {ultimo['semana']} de {d['semanas']} · estado {motor.SALUD_TXT[ultimo['salud']]} · "
          f"{crit} alerta(s) crítica(s), {len(ultimo['alertas']) - crit} de atención")
    return 0


if __name__ == "__main__":
    sys.exit(main())
