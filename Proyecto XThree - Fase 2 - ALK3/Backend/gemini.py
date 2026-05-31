from google import genai
from PIL import Image
import json
from datetime import datetime

client = genai.Client(api_key="AIzaSyBuRXxk6KmZGO9H4s02BXGsor6nS8r5Od8")

def leer_acta_gemini(ruta_imagen):
    try:
        img = Image.open(ruta_imagen)

        instruccion = """
        Analiza la tabla de la imagen. Extrae todos los votos visibles.

        Incluye partidos individuales, coaliciones, candidaturas comunes, votos nulos y total.

        Si aparece una coalición, usa el nombre unido con guiones, por ejemplo:
        "PAN-PRI-PRD" o "MORENA-PT-PVEM".

        Responde ÚNICAMENTE con este JSON:

        {
          "partidos": [
            {"partido": "PAN", "votos": 10},
            {"partido": "PRI", "votos": 5},
            {"partido": "PAN-PRI-PRD", "votos": 3}
          ],
          "total": 18,
          "nulos": 0
        }

        No incluyas explicación.
        No incluyas bloques ```json.
        Solo responde el JSON.
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
        print(f"Error procesando con Gemini: {e}")
        return None