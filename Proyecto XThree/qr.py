import cv2
from pyzbar.pyzbar import decode, ZBarSymbol

def leer_qr(ruta_imagen):
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        return None
    
    codigos=decode(imagen, symbols=[ZBarSymbol.QRCODE])

    if codigos:
        return codigos[0].data.decode("utf-8")
    return None