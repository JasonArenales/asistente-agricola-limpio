from transformers import pipeline
import logging

# Configurar logging para depuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Cargar el modelo con pipeline
    logger.info("Cargando el modelo deepset/roberta-base-squad2...")
    pipe = pipeline("question-answering", model="deepset/roberta-base-squad2")
    logger.info("Modelo cargado exitosamente.")
except Exception as e:
    logger.error(f"Error al cargar el modelo: {e}")
    raise

# Función para procesar preguntas
def get_answer(question, context):
    """Obtiene la respuesta a una pregunta basada en un contexto dado.
    
    Args:
        question (str): La pregunta a responder.
        context (str): El contexto donde buscar la respuesta.
    
    Returns:
        str: La respuesta extraída del contexto.
    """
    try:
        result = pipe(question=question, context=context)
        logger.info(f"Respuesta generada: {result['answer']}")
        return result['answer']
    except Exception as e:
        logger.error(f"Error al procesar la pregunta: {e}")
        return "[sin respuesta]"

# Exponer una API simple con Flask
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    """Maneja las solicitudes POST para el chat y devuelve una respuesta.
    
    Returns:
        JSON: Objeto con la respuesta al usuario.
    """
    try:
        data = request.get_json()
        if not data or 'pregunta' not in data:
            return jsonify({"respuesta": "Error: No se proporcionó una pregunta."}), 400
        pregunta = data['pregunta']
        contexto = "El cultivo de tomate necesita entre 20 y 25 grados de temperatura para crecer óptimamente. Es importante mantener el suelo húmedo y bien drenado. Se recomienda fertilizar con potasio."
        logger.info(f"Recibida pregunta: {pregunta}")
        respuesta = get_answer(pregunta, contexto)
        return jsonify({"respuesta": respuesta})
    except Exception as e:
        logger.error(f"Error en la ruta /chat: {e}")
        return jsonify({"respuesta": "Error al obtener respuesta del modelo."}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)