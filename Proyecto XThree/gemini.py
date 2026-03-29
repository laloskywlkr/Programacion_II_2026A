from google import genai
from PIL import Image
import json
from datetime import datetime

client = genai.Client(api_key="AIzaSyCHiUVXucvr5dJtKdacawQI8x6-C57urrU")

def leer_acta_gemini(ruta_imagen):
    try:
        img = Image.open(ruta_imagen)
        
        instruccion = """
        Analiza la tabla de la imagen. Extrae los votos.
        Responde ÚNICAMENTE con un objeto JSON siguiendo esta estructura:
        {
          "partidos": [
            {"partido": "PAN", "votos": 10},
            {"partido": "PRI", "votos": 5}
          ],
          "total": 15,
          "nulos": 0
        }
        No incluyas palabras como 'Aquí tienes el JSON' ni bloques de código ```json.
        Solo el texto del JSON.
        """
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
            contents=[instruccion, img]
        )
        
        texto = response.text.strip()
        if texto.startswith("```"):
            texto = texto.replace("```json", "").replace("```", "").strip()

        datos = json.loads(texto)
        
        datos["fecha_procesamiento"] = datetime.utcnow().isoformat()
        
        return datos

    except Exception as e:
        print(f"Error procesando {ruta_imagen}: {e}")
        return None