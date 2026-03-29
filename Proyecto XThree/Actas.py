import json
from datetime import datetime

class Acta:
    def __init__(self, tipo_eleccion, distrito, municipio, seccion, tipo_casilla):
        self.__tipo_eleccion = tipo_eleccion
        self.__distrito = distrito
        self.__municipio = municipio
        self.__seccion = seccion
        self.__tipo_casilla = tipo_casilla

        self.__total_votos = 0
        self.__votos_partido = {}
        self.__votos_nulos = 0
        self.__qr_data = ""
        self.__fecha_captura = ""
        self.__fecha_procesamiento = datetime.utcnow().isoformat()

    def cargar_desde_json(self, datos, qr_data="", fecha_captura=None):
        
        lista_partidos = datos.get("partidos", [])
        for item in lista_partidos:
            partido = str(item.get("partido", "DESCONOCIDO")).upper()
            try:
                votos = int(item.get("votos", 0))
            except:
                votos = 0
            self.__votos_partido[partido] = votos

        try:
            self.__total_votos = int(datos.get("total", 0))
            self.__votos_nulos = int(datos.get("nulos", 0))
        except:
            self.__total_votos = 0
            self.__votos_nulos = 0

        self.__qr_data = qr_data
        self.__fecha_captura = fecha_captura

        self.__fecha_procesamiento = datetime.utcnow().isoformat()

    def __str__(self):
        acta_dict = {
            "tipo_eleccion": self.__tipo_eleccion,
            "distrito": self.__distrito,
            "municipio": self.__municipio,
            "seccion": self.__seccion,
            "tipo_casilla": self.__tipo_casilla,
            "total_votos": self.__total_votos,
            "votos_partido": self.__votos_partido,
            "votos_nulos": self.__votos_nulos,
            "qr_data": self.__qr_data,
            "fecha_captura": self.__fecha_captura,
            "fecha_procesamiento": self.__fecha_procesamiento
        }
        return json.dumps(acta_dict, indent=2, ensure_ascii=False)