"""Motor de la torre de control.

Lee una carpeta POS (archivos CSV, JSON y Markdown) y calcula, semana a semana,
el estado del proyecto: indicadores, avance, costo, supuestos, riesgos y alertas.

Solo usa la biblioteca estándar de Python. Las reglas son deterministas a
propósito: la IA propone y redacta, pero los números y las alertas salen de
aquí, siempre igual con los mismos registros.
"""
from __future__ import annotations

import csv
import json
from datetime import date, timedelta
from pathlib import Path

ESTADOS_SUPUESTO = {"sin_probar", "validado", "en_duda", "roto"}
ESTADOS_RIESGO = {"abierto", "materializado", "mitigado", "cerrado"}
ESTADOS_HITO = {"pendiente", "en_curso", "hecho"}
NIVELES_PERMISO = {"puede", "pregunta", "nunca"}
TIPOS_BITACORA = {"senal", "supuesto", "riesgo", "cambio"}


# ---------------------------------------------------------------- lectura

def _csv(ruta: Path) -> list[dict]:
    if not ruta.exists():
        return []
    with ruta.open(encoding="utf-8-sig", newline="") as f:
        filas = []
        for fila in csv.DictReader(f):
            limpia = {(k or "").strip(): (v or "").strip() for k, v in fila.items() if k}
            if any(limpia.values()):
                filas.append(limpia)
        return filas


def _num(x, defecto=None):
    try:
        return float(str(x).replace(",", "").replace("%", "").replace("$", ""))
    except (TypeError, ValueError):
        return defecto


def _ent(x, defecto=None):
    n = _num(x)
    return int(n) if n is not None else defecto


def _refs(texto: str) -> list[str]:
    return [r.strip() for r in (texto or "").replace(",", ";").split(";") if r.strip()]


def cargar(carpeta) -> dict:
    """Carga una carpeta POS completa en un diccionario."""
    c = Path(carpeta)
    meta = json.loads((c / "pos.json").read_text(encoding="utf-8"))
    meta["semanas"] = _ent(meta.get("semanas"), 12) or 12
    acta = c / "contexto" / "acta.md"

    indicadores = []
    for f in _csv(c / "registros" / "indicadores.csv"):
        indicadores.append({
            "id": f.get("id", ""), "nombre": f.get("nombre", ""),
            "tipo": f.get("tipo", "adelantado") or "adelantado",
            "unidad": f.get("unidad", ""),
            "linea_base": _num(f.get("linea_base")), "meta": _num(f.get("meta")),
            "ambar": _num(f.get("ambar")), "rojo": _num(f.get("rojo")),
            "sentido": f.get("sentido", "sube") or "sube",
            "fuente": f.get("fuente", ""), "dueno": f.get("dueno", ""),
            "cadencia": _ent(f.get("cadencia_semanas"), 1) or 1,
            "desde": _ent(f.get("desde_semana"), 1) or 1,
        })

    supuestos = [{
        "id": f.get("id", ""), "supuesto": f.get("supuesto", ""),
        "si_falla": f.get("si_falla", ""), "prueba": f.get("prueba", ""),
        "dueno": f.get("dueno", ""), "semana_prueba": _ent(f.get("semana_prueba")),
        "estado": f.get("estado", "sin_probar") or "sin_probar",
    } for f in _csv(c / "registros" / "supuestos.csv")]

    riesgos = [{
        "id": f.get("id", ""), "riesgo": f.get("riesgo", ""),
        "senal_temprana": f.get("senal_temprana", ""),
        "probabilidad": _ent(f.get("probabilidad"), 3), "impacto": _ent(f.get("impacto"), 3),
        "dueno": f.get("dueno", ""), "respuesta": f.get("respuesta", ""),
        "semana_impacto": _ent(f.get("semana_impacto")),
        "estado": f.get("estado", "abierto") or "abierto",
    } for f in _csv(c / "registros" / "riesgos.csv")]

    decisiones = [{
        "semana": _ent(f.get("semana"), 0), "decision": f.get("decision", ""),
        "decide": f.get("decide", ""), "refs": _refs(f.get("refs", "")),
        "por_que": f.get("por_que", ""),
    } for f in _csv(c / "registros" / "decisiones.csv")]

    permisos = [{
        "accion": f.get("accion", ""), "nivel": (f.get("nivel", "") or "").lower(),
        "nota": f.get("nota", ""),
    } for f in _csv(c / "registros" / "permisos.csv")]

    hitos = [{
        "id": f.get("id", ""), "hito": f.get("hito", ""),
        "semana_plan": _ent(f.get("semana_plan"), 0), "peso": _num(f.get("peso"), 1) or 1,
        "dueno": f.get("dueno", ""),
    } for f in _csv(c / "plan" / "hitos.csv")]

    presupuesto = {_ent(f.get("semana"), 0): _num(f.get("plan_acumulado"), 0)
                   for f in _csv(c / "plan" / "presupuesto.csv")}

    mediciones = [{
        "semana": _ent(f.get("semana"), 0), "indicador": f.get("indicador", ""),
        "valor": _num(f.get("valor")), "fuente": f.get("fuente", ""),
    } for f in _csv(c / "pulso" / "mediciones.csv")]

    avance = [{
        "semana": _ent(f.get("semana"), 0), "hito": f.get("hito", ""),
        "estado": f.get("estado", "pendiente") or "pendiente",
        "avance": _num(f.get("avance"), 0) or 0,
        "semana_pronostico": _ent(f.get("semana_pronostico")),
    } for f in _csv(c / "pulso" / "hitos.csv")]

    gasto = {_ent(f.get("semana"), 0): _num(f.get("real_acumulado"), 0)
             for f in _csv(c / "pulso" / "gasto.csv")}

    bitacora = [{
        "semana": _ent(f.get("semana"), 0), "tipo": (f.get("tipo", "") or "").lower(),
        "refs": _refs(f.get("ref", "")), "estado": f.get("estado", ""),
        "texto": f.get("texto", ""), "fuente": f.get("fuente", ""),
    } for f in _csv(c / "pulso" / "bitacora.csv")]

    hay_pulso = bool(mediciones or avance or gasto or bitacora)
    return {
        "carpeta": str(c), "meta": meta,
        "acta": acta.read_text(encoding="utf-8") if acta.exists() else "",
        "indicadores": indicadores, "supuestos": supuestos, "riesgos": riesgos,
        "decisiones": decisiones, "permisos": permisos, "hitos": hitos,
        "presupuesto": presupuesto, "mediciones": mediciones, "avance": avance,
        "gasto": gasto, "bitacora": bitacora,
        "capas": {
            "contexto": bool(indicadores or supuestos or riesgos or permisos),
            "plan": bool(hitos),
            "pulso": hay_pulso,
        },
    }


# ---------------------------------------------------------------- revisión

def revisar(pos: dict) -> list[str]:
    """Problemas de forma en los registros. Lista vacía = todo en orden."""
    p: list[str] = []
    m = pos["meta"]
    for campo in ("proyecto", "inicio", "semanas", "decide"):
        if not m.get(campo):
            p.append(f"pos.json: falta '{campo}'")
    try:
        date.fromisoformat(m.get("inicio") or "")
    except ValueError:
        p.append("pos.json: 'inicio' debe tener formato AAAA-MM-DD")
    for nombre, filas in (("indicadores", pos["indicadores"]), ("supuestos", pos["supuestos"]),
                          ("riesgos", pos["riesgos"]), ("permisos", pos["permisos"])):
        if not filas:
            p.append(f"registros/{nombre}.csv: está vacío")

    def unicos(filas, nombre):
        vistos = set()
        for f in filas:
            if not f["id"]:
                p.append(f"{nombre}: hay una fila sin id")
            elif f["id"] in vistos:
                p.append(f"{nombre}: id repetido {f['id']}")
            vistos.add(f["id"])
        return vistos

    ids_i = unicos(pos["indicadores"], "indicadores.csv")
    ids_s = unicos(pos["supuestos"], "supuestos.csv")
    ids_r = unicos(pos["riesgos"], "riesgos.csv")
    ids_h = unicos(pos["hitos"], "plan/hitos.csv")
    todos = ids_i | ids_s | ids_r | ids_h

    for i in pos["indicadores"]:
        if i["sentido"] not in ("sube", "baja"):
            p.append(f"indicadores.csv {i['id']}: 'sentido' debe ser sube o baja")
        if i["tipo"] not in ("adelantado", "rezagado"):
            p.append(f"indicadores.csv {i['id']}: 'tipo' debe ser adelantado o rezagado")
        if i["meta"] is None:
            p.append(f"indicadores.csv {i['id']}: falta la meta")
        if i["ambar"] is None or i["rojo"] is None:
            p.append(f"indicadores.csv {i['id']}: faltan umbrales ámbar o rojo")
        elif i["sentido"] == "sube" and i["rojo"] > i["ambar"]:
            p.append(f"indicadores.csv {i['id']}: con sentido 'sube' el rojo debe ser menor que el ámbar")
        elif i["sentido"] == "baja" and i["rojo"] < i["ambar"]:
            p.append(f"indicadores.csv {i['id']}: con sentido 'baja' el rojo debe ser mayor que el ámbar")
        if not i["fuente"]:
            p.append(f"indicadores.csv {i['id']}: no dice de dónde sale el dato (fuente)")
        if not i["dueno"]:
            p.append(f"indicadores.csv {i['id']}: no tiene dueño")
    for s in pos["supuestos"]:
        if s["estado"] not in ESTADOS_SUPUESTO:
            p.append(f"supuestos.csv {s['id']}: estado desconocido '{s['estado']}'")
        if s["semana_prueba"] is None:
            p.append(f"supuestos.csv {s['id']}: no tiene semana de prueba")
    for r in pos["riesgos"]:
        if r["estado"] not in ESTADOS_RIESGO:
            p.append(f"riesgos.csv {r['id']}: estado desconocido '{r['estado']}'")
        if not r["senal_temprana"]:
            p.append(f"riesgos.csv {r['id']}: no define su señal temprana")
    for x in pos["permisos"]:
        if x["nivel"] not in NIVELES_PERMISO:
            p.append(f"permisos.csv '{x['accion']}': nivel debe ser puede, pregunta o nunca")
    for d in pos["decisiones"]:
        if not d["decide"]:
            p.append(f"decisiones.csv semana {d['semana']}: falta quién decide")
        for ref in d["refs"]:
            if ref not in todos:
                p.append(f"decisiones.csv semana {d['semana']}: referencia desconocida {ref}")
    for f in pos["mediciones"]:
        if f["indicador"] not in ids_i:
            p.append(f"pulso/mediciones.csv semana {f['semana']}: indicador desconocido {f['indicador']}")
        if f["valor"] is None:
            p.append(f"pulso/mediciones.csv semana {f['semana']} {f['indicador']}: valor vacío")
    for f in pos["avance"]:
        if f["hito"] not in ids_h:
            p.append(f"pulso/hitos.csv semana {f['semana']}: hito desconocido {f['hito']}")
        if f["estado"] not in ESTADOS_HITO:
            p.append(f"pulso/hitos.csv semana {f['semana']} {f['hito']}: estado desconocido '{f['estado']}'")
    for f in pos["bitacora"]:
        if f["tipo"] not in TIPOS_BITACORA:
            p.append(f"pulso/bitacora.csv semana {f['semana']}: tipo desconocido '{f['tipo']}'")
        for ref in f["refs"]:
            if ref not in todos:
                p.append(f"pulso/bitacora.csv semana {f['semana']}: referencia desconocida {ref}")
        if f["tipo"] == "supuesto" and f["estado"] not in ESTADOS_SUPUESTO:
            p.append(f"pulso/bitacora.csv semana {f['semana']}: estado de supuesto desconocido '{f['estado']}'")
        if f["tipo"] == "riesgo" and f["estado"] not in ESTADOS_RIESGO:
            p.append(f"pulso/bitacora.csv semana {f['semana']}: estado de riesgo desconocido '{f['estado']}'")
        if f["tipo"] == "senal" and not f["fuente"]:
            p.append(f"pulso/bitacora.csv semana {f['semana']}: la señal no dice su fuente")
    for c in m.get("condiciones_corte", []):
        if c.get("indicador") not in ids_i:
            p.append(f"pos.json: condición de corte con indicador desconocido {c.get('indicador')}")
    return p


# ---------------------------------------------------------------- cálculo

def ultima_semana(pos: dict) -> int:
    semanas = [f["semana"] for f in pos["mediciones"] + pos["avance"] + pos["bitacora"]]
    semanas += list(pos["gasto"].keys())
    return max(semanas) if semanas else 0


def fecha_semana(pos: dict, semana: int) -> str:
    """Viernes de la semana indicada (semana 0 = día de arranque)."""
    try:
        inicio = date.fromisoformat(pos["meta"].get("inicio") or "")
    except ValueError:
        inicio = date.today()
    if semana <= 0:
        return inicio.isoformat()
    return (inicio + timedelta(days=7 * (semana - 1) + 4)).isoformat()


def _acumulado(serie: dict, semana: int):
    claves = [k for k in serie if k <= semana]
    return serie[max(claves)] if claves else None


def _estado_indicador(ind: dict, valor) -> str:
    if valor is None:
        return "sin_dato"
    a, r = ind["ambar"], ind["rojo"]
    if ind["sentido"] == "baja":
        if r is not None and valor > r:
            return "rojo"
        if a is not None and valor > a:
            return "ambar"
        return "verde"
    if r is not None and valor < r:
        return "rojo"
    if a is not None and valor < a:
        return "ambar"
    return "verde"


def _fmt(valor, unidad=""):
    if valor is None:
        return "sin dato"
    txt = f"{valor:,.0f}" if abs(valor) >= 100 or float(valor).is_integer() else f"{valor:,.1f}"
    if unidad == "%":
        return txt + "%"
    if unidad in ("$", "USD", "MXN"):
        return "$" + txt
    return f"{txt} {unidad}".strip()


def nombres(pos: dict) -> dict:
    n = {}
    for i in pos["indicadores"]:
        n[i["id"]] = i["nombre"]
    for s in pos["supuestos"]:
        n[s["id"]] = s["supuesto"]
    for r in pos["riesgos"]:
        n[r["id"]] = r["riesgo"]
    for h in pos["hitos"]:
        n[h["id"]] = h["hito"]
    return n


def calcular(pos: dict, w: int) -> dict:
    """Estado del proyecto al cierre de la semana w (0 = arranque)."""
    meta = pos["meta"]
    alertas: list[dict] = []

    def alerta(clave, regla, sev, titulo, detalle, refs=()):
        alertas.append({"clave": clave, "regla": regla, "severidad": sev,
                        "titulo": titulo, "detalle": detalle, "refs": list(refs)})

    # --- indicadores
    indicadores = []
    for ind in pos["indicadores"]:
        serie = sorted(((m["semana"], m["valor"]) for m in pos["mediciones"]
                        if m["indicador"] == ind["id"] and m["semana"] <= w and m["valor"] is not None))
        valor = serie[-1][1] if serie else None
        ultima = serie[-1][0] if serie else None
        previo = serie[-2][1] if len(serie) > 1 else None
        activo = w >= ind["desde"]
        estado = _estado_indicador(ind, valor) if activo else "no_aplica"
        apagado = activo and (ultima is None or w - ultima >= 2 * ind["cadencia"])
        if activo and valor is None:
            estado = "sin_dato"
        indicadores.append({"id": ind["id"], "valor": valor, "semana_dato": ultima,
                            "previo": previo, "estado": estado, "apagado": apagado,
                            "serie": serie})
        if estado == "rojo":
            alerta(f"ind-{ind['id']}", "Indicador en rojo", "critica",
                   f"{ind['id']} {ind['nombre']}: {_fmt(valor, ind['unidad'])}",
                   f"Meta {_fmt(ind['meta'], ind['unidad'])}; el umbral rojo es {_fmt(ind['rojo'], ind['unidad'])}. Dueño: {ind['dueno']}.",
                   [ind["id"]])
        elif estado == "ambar":
            alerta(f"ind-{ind['id']}", "Indicador en ámbar", "atencion",
                   f"{ind['id']} {ind['nombre']}: {_fmt(valor, ind['unidad'])}",
                   f"Meta {_fmt(ind['meta'], ind['unidad'])}; el umbral ámbar es {_fmt(ind['ambar'], ind['unidad'])}. Dueño: {ind['dueno']}.",
                   [ind["id"]])
        if apagado:
            desde_txt = f"desde la semana {ultima}" if ultima is not None else "nunca se ha medido"
            alerta(f"ind-apagado-{ind['id']}", "Indicador sin medir", "atencion",
                   f"{ind['id']} {ind['nombre']}: sin dato reciente",
                   f"Debía medirse cada {ind['cadencia']} semana(s) en «{ind['fuente']}»; {desde_txt}. Dueño: {ind['dueno']}.",
                   [ind["id"]])

    # --- hitos, avance y valor ganado
    peso_total = sum(h["peso"] for h in pos["hitos"]) or 1
    hitos, ganado = [], 0.0
    fin_plan = max((h["semana_plan"] for h in pos["hitos"]), default=meta.get("semanas", 0))
    fin_pronostico = fin_plan
    for h in pos["hitos"]:
        filas = sorted((a for a in pos["avance"] if a["hito"] == h["id"] and a["semana"] <= w),
                       key=lambda a: a["semana"])
        ult = filas[-1] if filas else None
        estado = ult["estado"] if ult else "pendiente"
        av = 100.0 if estado == "hecho" else (ult["avance"] if ult else 0.0)
        pron = (ult["semana_pronostico"] if ult and ult["semana_pronostico"] else h["semana_plan"])
        real = None
        if estado == "hecho":
            primera = next(a for a in filas if a["estado"] == "hecho")
            real = primera["semana_pronostico"] or primera["semana"]
            pron = real
        elif h["semana_plan"] <= w:
            pron = max(pron, w + 1)
        atraso = pron - h["semana_plan"]
        ganado += h["peso"] * av / 100.0
        fin_pronostico = max(fin_pronostico, pron)
        hitos.append({"id": h["id"], "estado": estado, "avance": av,
                      "pronostico": pron, "real": real, "atraso": atraso})
        if estado != "hecho" and h["semana_plan"] <= w:
            alerta(f"hito-{h['id']}", "Hito atrasado",
                   "critica" if atraso >= 3 else "atencion",
                   f"{h['id']} {h['hito']}: {atraso} semana(s) de atraso",
                   f"Estaba planeado para la semana {h['semana_plan']}; el pronóstico es la semana {pron}. Dueño: {h['dueno']}.",
                   [h["id"]])
        elif estado != "hecho" and atraso >= 1:
            alerta(f"hito-{h['id']}", "Pronóstico movido", "atencion",
                   f"{h['id']} {h['hito']}: el pronóstico se mueve {atraso} semana(s)",
                   f"Plan: semana {h['semana_plan']}. Pronóstico: semana {pron}. Dueño: {h['dueno']}.",
                   [h["id"]])

    bac = meta.get("presupuesto") or (max(pos["presupuesto"].values()) if pos["presupuesto"] else None)
    pct_real = ganado / peso_total if pos["hitos"] else None
    pv = _acumulado(pos["presupuesto"], w)
    ac = _acumulado(pos["gasto"], w)
    ev = bac * pct_real if (bac and pct_real is not None) else None
    spi = (ev / pv) if (ev is not None and pv) else None
    cpi = (ev / ac) if (ev is not None and ac) else None
    eac = (bac / cpi) if (bac and cpi) else None
    pct_plan = (pv / bac) if (pv is not None and bac) else None
    if spi is not None and w >= 2 and spi < 0.9:
        alerta("spi", "Avance por debajo del plan", "critica" if spi < 0.8 else "atencion",
               f"Avance: por cada $1 de trabajo planeado llevamos ${spi:.2f}",
               f"Avance real {pct_real:.0%} contra {pct_plan:.0%} planeado a la semana {w} (SPI {spi:.2f}).")
    if cpi is not None and w >= 2 and cpi < 0.9:
        alerta("cpi", "Costo por encima del plan", "critica" if cpi < 0.8 else "atencion",
               f"Costo: cada $1 gastado está rindiendo ${cpi:.2f} de avance",
               f"Gastado {_fmt(ac, '$')} para un avance que vale {_fmt(ev, '$')} (CPI {cpi:.2f}). Al ritmo actual el proyecto cerraría en {_fmt(eac, '$')} contra {_fmt(bac, '$')} aprobados.")
    if pos["hitos"] and fin_pronostico - fin_plan >= 2:
        alerta("cierre", "Fecha de cierre en riesgo", "critica",
               f"El cierre se mueve {fin_pronostico - fin_plan} semanas",
               f"Plan: semana {fin_plan}. Pronóstico: semana {fin_pronostico}.")

    # --- bitácora: supuestos, riesgos, señales
    bit = [b for b in pos["bitacora"] if b["semana"] <= w]
    decs = [d for d in pos["decisiones"] if d["semana"] <= w]

    def decidido(ref, desde):
        """Semana de la primera decisión que nombra esta referencia a partir de 'desde'."""
        sem = sorted(d["semana"] for d in decs if ref in d["refs"] and d["semana"] >= (desde or 0))
        return sem[0] if sem else None

    supuestos = []
    for s in pos["supuestos"]:
        cambios = sorted((b for b in bit if b["tipo"] == "supuesto" and s["id"] in b["refs"]),
                         key=lambda b: b["semana"])
        estado = cambios[-1]["estado"] if cambios else s["estado"]
        evidencia = cambios[-1]["texto"] if cambios else ""
        desde = cambios[-1]["semana"] if cambios else None
        vencida = estado == "sin_probar" and s["semana_prueba"] is not None and s["semana_prueba"] < w
        atendido = decidido(s["id"], desde) if estado in ("roto", "en_duda") else None
        supuestos.append({"id": s["id"], "estado": estado, "evidencia": evidencia,
                          "desde": desde, "vencida": vencida, "decidido": atendido})
        if atendido is not None:
            pass
        elif estado == "roto":
            alerta(f"sup-{s['id']}", "Supuesto roto", "critica",
                   f"{s['id']} ya no se sostiene: {s['supuesto']}",
                   f"Si falla: {s['si_falla']} Evidencia: {evidencia}", [s["id"]])
        elif estado == "en_duda":
            alerta(f"sup-{s['id']}", "Supuesto en duda", "atencion",
                   f"{s['id']} en duda: {s['supuesto']}",
                   f"Si falla: {s['si_falla']} Evidencia: {evidencia}", [s["id"]])
        elif vencida:
            alerta(f"sup-{s['id']}", "Prueba vencida", "atencion",
                   f"{s['id']} sigue sin probarse: {s['supuesto']}",
                   f"La prueba («{s['prueba']}») era para la semana {s['semana_prueba']}. Dueño: {s['dueno']}.",
                   [s["id"]])

    riesgos = []
    for r in pos["riesgos"]:
        cambios = sorted((b for b in bit if b["tipo"] == "riesgo" and r["id"] in b["refs"]),
                         key=lambda b: b["semana"])
        estado = cambios[-1]["estado"] if cambios else r["estado"]
        atendido = decidido(r["id"], cambios[-1]["semana"]) if estado == "materializado" else None
        riesgos.append({"id": r["id"], "estado": estado,
                        "exposicion": r["probabilidad"] * r["impacto"],
                        "nota": cambios[-1]["texto"] if cambios else "", "decidido": atendido})
        if estado == "materializado" and atendido is None:
            alerta(f"riesgo-{r['id']}", "Riesgo materializado", "critica",
                   f"{r['id']} ya ocurrió: {r['riesgo']}",
                   f"Respuesta prevista: {r['respuesta']} Dueño: {r['dueno']}.", [r["id"]])

    nom = nombres(pos)
    senales = [b for b in bit if b["tipo"] == "senal"]
    rastros, grupos = [], {}
    for ref in sorted({x for s in senales for x in s["refs"]}):
        sem = sorted(s["semana"] for s in senales if ref in s["refs"])
        dec = sorted(d["semana"] for d in decs if ref in d["refs"] and d["semana"] >= sem[0])
        primera_dec = dec[0] if dec else None
        rastros.append({"ref": ref, "senales": sem, "decision": primera_dec,
                        "espera": (primera_dec - sem[0]) if primera_dec is not None else (w - sem[0])})
        if primera_dec is None and len(sem) >= 2:
            grupos.setdefault(tuple(sem), []).append(ref)
    for sem, refs in grupos.items():
        edad = w - sem[0]
        detalle = " · ".join(f"{r}: {nom.get(r, r)}" for r in refs)
        alerta("senal-" + "-".join(refs), "Señales sin decisión",
               "critica" if edad >= 3 or len(sem) >= 3 else "atencion",
               f"{', '.join(refs)}: {len(sem)} señales en {edad + 1} semana(s) y ninguna decisión",
               f"{detalle}. Primera señal en la semana {sem[0]}. Nadie con autoridad ha decidido qué hacer.",
               refs)

    # --- condiciones de corte
    for i, c in enumerate(meta.get("condiciones_corte", [])):
        est = next((x for x in indicadores if x["id"] == c.get("indicador")), None)
        if not est or est["valor"] is None or w < c.get("semana", 0):
            continue
        v, lim = est["valor"], c.get("valor")
        cumple = v < lim if c.get("si") == "<" else v > lim
        if cumple and decidido(c["indicador"], c.get("semana", 0)) is None:
            alerta(f"corte-{i}", "Condición de corte", "critica",
                   f"Se cumplió la condición de corte: {c.get('texto', '')}",
                   f"{c['indicador']} está en {_fmt(v)} a la semana {w}. El acta dice que esto obliga a decidir si el proyecto sigue. Decide: {meta.get('decide', '')}.",
                   [c["indicador"]])

    orden = {"critica": 0, "atencion": 1}
    alertas.sort(key=lambda a: (orden[a["severidad"]], a["clave"]))
    criticas = sum(1 for a in alertas if a["severidad"] == "critica")
    hay_pulso = any(f["semana"] <= w for f in pos["mediciones"] + pos["avance"] + pos["bitacora"]) \
        or any(k <= w for k in pos["gasto"])
    salud = "sin_datos" if not hay_pulso else "rojo" if criticas else "ambar" if alertas else "verde"

    return {
        "semana": w, "fecha": fecha_semana(pos, w), "salud": salud,
        "indicadores": indicadores, "hitos": hitos, "supuestos": supuestos, "riesgos": riesgos,
        "evm": {"bac": bac, "pv": pv, "ev": ev, "ac": ac, "spi": spi, "cpi": cpi, "eac": eac,
                "pct_plan": pct_plan, "pct_real": pct_real,
                "fin_plan": fin_plan, "fin_pronostico": fin_pronostico},
        "senales": [{"semana": s["semana"], "refs": s["refs"], "texto": s["texto"], "fuente": s["fuente"]}
                    for s in senales],
        "cambios": [{"semana": b["semana"], "texto": b["texto"]} for b in bit if b["tipo"] == "cambio"],
        "decisiones": decs, "rastros": rastros, "alertas": alertas,
    }


def linea_de_tiempo(pos: dict, hasta: int | None = None) -> list[dict]:
    """Estados de la semana 0 a la última con datos; cada alerta lleva la semana en que apareció."""
    fin = ultima_semana(pos) if hasta is None else min(hasta, ultima_semana(pos))
    estados, activas = [], {}
    for w in range(0, fin + 1):
        e = calcular(pos, w)
        vigentes = {}
        for a in e["alertas"]:
            a["desde"] = activas.get(a["clave"], w)
            vigentes[a["clave"]] = a["desde"]
        activas = vigentes
        e["brief"] = brief(pos, e, estados[-1] if estados else None)
        estados.append(e)
    return estados


# ---------------------------------------------------------------- brief

SALUD_TXT = {"verde": "VERDE", "ambar": "ÁMBAR", "rojo": "ROJO", "sin_datos": "SIN DATOS"}


def brief(pos: dict, e: dict, previo: dict | None) -> str:
    """Brief ejecutivo armado por reglas. Es un borrador: lo acepta y lo firma una persona."""
    meta, w = pos["meta"], e["semana"]
    L = [f"{meta.get('proyecto', 'Proyecto')} · semana {w} de {meta.get('semanas', '?')} · estado {SALUD_TXT[e['salud']]}", ""]
    if e["salud"] == "sin_datos":
        L += ["Todavía no hay pulso registrado. La torre tiene el acta, los indicadores y los supuestos, "
              "pero ningún dato de ejecución.", ""]
    evm = e["evm"]
    if evm["pct_real"] is not None and evm["pct_plan"] is not None:
        linea = f"Avance {evm['pct_real']:.0%} contra {evm['pct_plan']:.0%} planeado."
        if evm["ac"] is not None and evm["pv"] is not None:
            linea += f" Gastado {_fmt(evm['ac'], '$')} de {_fmt(evm['pv'], '$')} previstos a la fecha."
        if evm["fin_pronostico"] != evm["fin_plan"]:
            linea += f" El cierre pasa de la semana {evm['fin_plan']} a la {evm['fin_pronostico']}."
        L += [linea, ""]
    nuevas = [a for a in e["alertas"] if a.get("desde") == w]
    resueltas = []
    if previo:
        ahora = {a["clave"] for a in e["alertas"]}
        resueltas = [a for a in previo["alertas"] if a["clave"] not in ahora]
    decs = [d for d in e["decisiones"] if d["semana"] == w]
    if nuevas or resueltas or decs:
        L.append("Qué cambió esta semana")
        L += [f"- Nuevo: {a['titulo']}" for a in nuevas[:6]]
        if len(nuevas) > 6:
            L.append(f"- y {len(nuevas) - 6} alertas nuevas más")
        if resueltas:
            cuenta = {}
            for a in resueltas:
                cuenta[a["regla"]] = cuenta.get(a["regla"], 0) + 1
            L.append(f"- Se cerraron {len(resueltas)} alertas: "
                     + ", ".join(f"{n} de «{r.lower()}»" for r, n in cuenta.items()))
        L += [f"- Decisión de {d['decide']}: {d['decision']}" for d in decs]
        L.append("")
    crit = [a for a in e["alertas"] if a["severidad"] == "critica"]
    if crit:
        L.append(f"En rojo (decide: {meta.get('decide', 'sin definir')})")
        L += [f"- {a['titulo']} (abierto desde la semana {a.get('desde', w)})" for a in crit]
        L.append("")
    huecos = [a for a in e["alertas"] if a["regla"] in ("Indicador sin medir", "Prueba vencida")]
    if huecos:
        L.append("Qué no tiene dato detrás")
        L += [f"- {a['titulo']}" for a in huecos]
        L.append("")
    if e["salud"] == "verde":
        L += ["Sin alertas abiertas.", ""]
    L.append(f"Borrador armado por reglas a partir de los registros. Lo acepta y lo firma: {meta.get('pm', meta.get('decide', ''))}.")
    return "\n".join(L)
