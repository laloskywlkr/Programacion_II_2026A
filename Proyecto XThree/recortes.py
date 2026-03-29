import cv2
import os

def recortar_tabla(ruta_imagen, ruta_salida):
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"Error al cargar imagen para recorte: {ruta_imagen}")
        return None

    alto, ancho, _ = imagen.shape

    y_inicio = int(alto * 0.10)
    y_fin    = int(alto * 0.71)
    x_inicio = int(ancho * 0.35)
    x_fin    = int(ancho * 0.69)

    recorte = imagen[y_inicio:y_fin, x_inicio:x_fin]

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    cv2.imwrite(ruta_salida, recorte)

    return ruta_salida