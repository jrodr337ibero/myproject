import os

class ImagenServidor:
    def __init__(self, image_directory):
        self.image_directory = image_directory

    def get_image_path(self, object_name):
        """
        Devuelve la ruta de la imagen correspondiente al objeto.
        Si no se encuentra, devuelve None.
        """
        image_path = os.path.join(self.image_directory, f"{object_name}.jpg")
        if os.path.exists(image_path):
            return image_path
        return None
