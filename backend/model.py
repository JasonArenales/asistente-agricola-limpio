from flask import Flask, request, jsonify, render_template, send_from_directory  # Añadido send_from_directory
from flask_cors import CORS
import logging
from transformers import pipeline
import torch
from PIL import Image
import io
import base64
from ultralytics import YOLO
import json
# Configurar logging para depuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar modelo de lenguaje natural
try:
    logger.info("Cargando el modelo deepset/roberta-base-squad2...")
    pipe = pipeline("question-answering", model="deepset/roberta-base-squad2")
    logger.info("Modelo cargado exitosamente.")
except Exception as e:
    logger.error(f"Error al cargar el modelo: {e}")
    raise

# Función para procesar preguntas
def get_answer(question, context):
    """Obtiene la respuesta a una pregunta basada en un contexto dado."""
    try:
        result = pipe(question=question, context=context)
        logger.info(f"Respuesta generada: {result['answer']}")
        return result['answer']
    except Exception as e:
        logger.error(f"Error al procesar la pregunta: {e}")
        return "[sin respuesta]"

# Cargar modelos YOLO disponibles
try:
    logger.info("Cargando modelos YOLO...")
    models = {
        "yolov5s": YOLO("yolov5s.pt"),
        "yolov5m": YOLO("yolov5m.pt")
    }
    logger.info("Modelos YOLO cargados exitosamente.")
except Exception as e:
    logger.error(f"Error cargando modelos YOLO: {e}")
    models = {}

# Flask API
app = Flask(__name__, static_folder='public')  # Usar la carpeta 'public' como static
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)


@app.route('/chat', methods=['POST'])
def chat():
    """Maneja las solicitudes POST para el chat y devuelve una respuesta."""
    try:
        data = request.get_json()
        if not data or 'pregunta' not in data:
            return jsonify({"respuesta": "Error: No se proporcionó una pregunta."}), 400
        pregunta = data['pregunta']
        contexto = "El cultivo de tomate necesita entre 20 y 25 grados de temperatura para crecer óptimamente. Es importante mantener el suelo húmedo y bien drenado. Se recomienda fertilizar con potasio."
        logger.info(f"Recibida pregunta: {pregunta}")
        respuesta = get_answer(pregunta, contexto)
        if respuesta == "[sin respuesta]":
            respuesta = "Lo siento, solo tengo información sobre el cultivo de tomates por ahora."
        return jsonify({"respuesta": respuesta})
    except Exception as e:
        logger.error(f"Error en la ruta /chat: {e}")
        return jsonify({"respuesta": "Error al obtener respuesta del modelo."}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Ruta para recibir imagen y modelo YOLO, y retornar resultados."""
    try:
        model_name = request.form.get('model')
        file = request.files.get('image')

        if not model_name or model_name not in models:
            return jsonify({"error": "Modelo YOLO no válido."}), 400
        if not file:
            return jsonify({"error": "Imagen no proporcionada."}), 400

        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes))

        # Procesar con YOLO
        results = models[model_name](image)

        # Obtener imagen anotada
        annotated_img = results[0].plot()
        buffered = io.BytesIO()
        Image.fromarray(annotated_img).save(buffered, format="JPEG")
        encoded_img = base64.b64encode(buffered.getvalue()).decode()

        # Parsear las detecciones
        detections = json.loads(results[0].tojson()) if results[0].boxes else []

        return jsonify({
            "image": encoded_img,
            "detections": detections
        })

    except Exception as e:
        logger.error(f"Error en la ruta /predict: {e}")
        return jsonify({"error": f"Error al procesar la imagen: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)