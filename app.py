from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from Imagenes.image_servidor import ImagenServidor

app = Flask(__name__)
socketio = SocketIO(app)

# Inicializar el servicio de imágenes
image_service = ImagenServidor(image_directory='static/imagen')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('request_image')
def handle_request_image(object_name):
    image_path = image_service.get_image_path(object_name)
    if image_path:
        emit('send_image', {'image_path': image_path})
    else:
        emit('send_image', {'image_path': None})

if __name__ == '__main__':
    socketio.run(app, debug=True)
