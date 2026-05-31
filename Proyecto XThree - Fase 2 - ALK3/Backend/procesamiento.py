import os
import json

CARPETA_RESULTADOS = "resultados"

NORMALIZACION = {
    "PANAL": "NUEVA ALIANZA",
    "NA": "NUEVA ALIANZA",
    "NUEVA-ALIANZA": "NUEVA ALIANZA",
    "NUEVA ALIANZA": "NUEVA ALIANZA",

    "MOVIMIENTO CIUDADANO": "MC",
    "MOVIMIENTO-CIUDADANO": "MC",

    "CANDIDATOS NO REGISTRADOS": "NO REGISTRADOS",
    "CANDIDATOS-NO-REGISTRADOS": "NO REGISTRADOS",
    "CANDIDATO NO REGISTRADO": "NO REGISTRADOS",
    "NO REGISTRADOS": "NO REGISTRADOS",

    "CANDIDATURA INDEPENDIENTE": "CANDIDATO INDEPENDIENTE",
    "CANDIDATO INDEPENDIENTE": "CANDIDATO INDEPENDIENTE",

    "CANDIDATURA COMÚN 1": "CANDIDATO INDEPENDIENTE",
    "CANDIDATURA COMUN 1": "CANDIDATO INDEPENDIENTE",
    "CANDIDATURA-COMUN": "CANDIDATO INDEPENDIENTE",
    "CANDIDATURA-COMÚN": "CANDIDATO INDEPENDIENTE",
    "ALIANZA": "CANDIDATO INDEPENDIENTE",
    "OTRO": "CANDIDATO INDEPENDIENTE",
    "PARTIDO-1": "CANDIDATO INDEPENDIENTE",
    "FUERZA POR MÉXICO": "CANDIDATO INDEPENDIENTE",
    "FUERZA POR MEXICO": "CANDIDATO INDEPENDIENTE",
    "PES": "CANDIDATO INDEPENDIENTE"

}


def normalizar_nombre(nombre):
    nombre = nombre.strip().upper()

    if nombre in NORMALIZACION:
        return NORMALIZACION[nombre]

    return nombre


def guardar_acta_json(nombre_archivo, acta_dict):
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    nombre_limpio = os.path.splitext(nombre_archivo)[0]
    ruta_salida = os.path.join(CARPETA_RESULTADOS, f"{nombre_limpio}.json")

    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        json.dump(acta_dict, archivo, indent=2, ensure_ascii=False)

    return ruta_salida


def generar_resumen():
    resumen = {
        "actas_procesadas": 0,
        "total_votos": 0,
        "votos_nulos": 0,
        "votos_por_partido": {}
    }

    if not os.path.exists(CARPETA_RESULTADOS):
        return resumen

    for archivo in os.listdir(CARPETA_RESULTADOS):
        if archivo.endswith(".json"):
            ruta = os.path.join(CARPETA_RESULTADOS, archivo)

            with open(ruta, "r", encoding="utf-8") as f:
                acta = json.load(f)

            resumen["actas_procesadas"] += 1
            resumen["total_votos"] += acta.get("total_votos", 0)
            resumen["votos_nulos"] += acta.get("votos_nulos", 0)

            votos_partido = acta.get("votos_partido", {})

            for partido, votos in votos_partido.items():
                partido_normalizado = normalizar_nombre(partido)

                if partido_normalizado not in resumen["votos_por_partido"]:
                    resumen["votos_por_partido"][partido_normalizado] = 0

                resumen["votos_por_partido"][partido_normalizado] += votos

    return resumen