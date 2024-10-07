from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, emit
from components.image_servidor import ImagenServidor
import os
import requests

app = Flask(__name__)
socketio = SocketIO(app)

# Inicializar el servicio de imágenes con tu API Key de Pixabay
API_KEY = "18692132-8999bfe8bc634497a86b29f30"  # Reemplaza esto con tu API Key real
image_service = ImagenServidor(api_key=API_KEY)

IMAGE_FOLDER = 'downloads'

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('request_image')
def handle_request_image(object_name):
    image_url = image_service.get_image_url(object_name)
    if image_url:
        emit('send_image', {'image_path': image_url})
    else:
        emit('send_image', {'image_path': None})
        
@app.route('/download_image/<path:image_url>/<string:custom_filename>', methods=['GET'])
def download_image(image_url, custom_filename):
    print(image_url)
    image_filename = os.path.basename(custom_filename)  # Obtiene el nombre del archivo de la URL
    # image_path = os.path.join(IMAGE_FOLDER, image_filename)
    image_path = os.path.join(IMAGE_FOLDER)

    if os.path.exists(image_path):
        os.remove(image_path)
    
    # Descargar la imagen solo si no existe localmente
    if not os.path.exists(image_path):
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Lanza un error si la solicitud falla
            with open(image_path, 'wb') as f:
                f.write(response.content)  # Guarda el contenido de la imagen en el archivo
        except requests.RequestException as e:
            return f"Error al descargar la imagen: {str(e)}", 500

    # Envía el archivo para su descarga
    return send_file(image_path, as_attachment=True, download_name=image_filename+'.jpg')

if __name__ == '__main__':
    socketio.run(app, debug=True)
