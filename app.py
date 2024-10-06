from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from components.image_servidor import ImagenServidor

app = Flask(__name__)
socketio = SocketIO(app)

# Inicializar el servicio de imágenes con tu API Key de Pixabay
API_KEY = "18692132-8999bfe8bc634497a86b29f30"  # Reemplaza esto con tu API Key real
image_service = ImagenServidor(api_key=API_KEY)

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

if __name__ == '__main__':
    socketio.run(app, debug=True)
