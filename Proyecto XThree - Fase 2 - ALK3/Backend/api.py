from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List

import os
import shutil
import json

from Actas import Acta
from gemini import leer_acta_gemini
from procesamiento import guardar_acta_json, generar_resumen
from recortes import recortar_tabla
from qr import leer_qr
from gemini import leer_acta_gemini

app = FastAPI(title="API de Actas Electorales")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CARPETA_TEMP = "temp"

os.makedirs(CARPETA_TEMP, exist_ok=True)


@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando correctamente"
    }


@app.post("/procesar-actas")
async def procesar_actas(imagenes: List[UploadFile] = File(...)):

    resultados = []

    for imagen in imagenes:

        try:

            if not imagen.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                resultados.append({
                    "archivo": imagen.filename,
                    "estado": "error",
                    "mensaje": "Formato no válido"
                })
                continue

            ruta_original = os.path.join(CARPETA_TEMP, imagen.filename)

            ruta_recorte = os.path.join(
                CARPETA_TEMP,
                "recortes",
                "votos_" + imagen.filename
            )

            with open(ruta_original, "wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)

            recortar_tabla(ruta_original, ruta_recorte)

            qr_data_full = leer_qr(ruta_original)

            if not qr_data_full:
                resultados.append({
                    "archivo": imagen.filename,
                    "estado": "error",
                    "mensaje": "No se pudo leer el QR"
                })
                continue

            campos = qr_data_full.split(",")

            if len(campos) < 6:
                resultados.append({
                    "archivo": imagen.filename,
                    "estado": "error",
                    "mensaje": "El QR no tiene el formato esperado"
                })
                continue

            tipo_eleccion, distrito, municipio, seccion, casilla, fecha_qr = campos[:6]

            datos_votos = leer_acta_gemini(ruta_recorte)

            if not datos_votos:
                resultados.append({
                    "archivo": imagen.filename,
                    "estado": "error",
                    "mensaje": "Gemini no devolvió datos válidos"
                })
                continue

            acta = Acta(
                tipo_eleccion,
                distrito,
                municipio,
                seccion,
                casilla
            )

            acta.cargar_desde_json(
                datos_votos,
                qr_data=qr_data_full,
                fecha_captura=fecha_qr
            )

            acta_dict = json.loads(str(acta))

            guardar_acta_json(
                imagen.filename,
                acta_dict
            )

            resultados.append({
                "archivo": imagen.filename,
                "estado": "procesada",
                "acta": acta_dict
            })

        except Exception as e:

            resultados.append({
                "archivo": imagen.filename,
                "estado": "error",
                "mensaje": str(e)
            })

    resumen = generar_resumen()

    return {
        "mensaje": "Procesamiento terminado",
        "resultados": resultados,
        "resumen": resumen
    }


@app.get("/resumen")
def obtener_resumen():

    return generar_resumen()

@app.delete("/limpiar-resultados")
def limpiar_resultados():

    carpeta_resultados = "resultados"

    eliminados = 0

    if os.path.exists(carpeta_resultados):

        for archivo in os.listdir(carpeta_resultados):

            if archivo.endswith(".json"):

                ruta = os.path.join(
                    carpeta_resultados,
                    archivo
                )

                os.remove(ruta)

                eliminados += 1

    return {
        "mensaje": "Resultados eliminados correctamente",
        "archivos_eliminados": eliminados
    }