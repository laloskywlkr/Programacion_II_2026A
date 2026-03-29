import os
import time
from Actas import Acta
from recortes import recortar_tabla
from qr import leer_qr
from gemini import leer_acta_gemini

carpeta_entrada = r"C:\Users\lalov\Downloads\Proyecto XThree\Actas_Malinalco"
carpeta_recortes = r"C:\Users\lalov\Downloads\Proyecto XThree\Actas_Malinalco\Actas_Recortadas"

actas = []

for archivo in os.listdir(carpeta_entrada):
    if archivo.lower().endswith((".jpg", ".jpeg", ".png")):
        ruta_original = os.path.join(carpeta_entrada, archivo)
        ruta_recorte = os.path.join(carpeta_recortes, "votos_" + archivo)

        print(f"--- Procesando: {archivo} ---")

        recortar_tabla(ruta_original, ruta_recorte)

        qr_data_full=leer_qr(ruta_original)
        if not qr_data_full:
            print(f"Sin QR en {archivo}")
            continue

        campos=qr_data_full.split(",")
        tipo_eleccion, distrito, municipio, seccion, casilla, fecha_qr = campos[:6]

        datos_votos = leer_acta_gemini(ruta_recorte)
        if not datos_votos:
            continue

        acta = Acta(tipo_eleccion, distrito, municipio, seccion, casilla)
        acta.cargar_desde_json(datos_votos, qr_data=qr_data_full, fecha_captura=fecha_qr)

        actas.append(acta)
        print(f"OK")
    
        time.sleep(0.5)
for a in actas:
    print(a)