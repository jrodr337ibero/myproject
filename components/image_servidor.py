import requests

class ImagenServidor:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_image_url(self, object_name):
        """
        Busca la URL de la imagen correspondiente al objeto utilizando la API de Pixabay.
        Si no se encuentra, devuelve None.
        """
        url = f"https://pixabay.com/api/"
        params = {
            'key': self.api_key,
            'q': object_name,
            'image_type': 'photo',
            'per_page': 3  # Número de imágenes a devolver
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data['hits']:
            # Devuelve la URL de la primera imagen encontrada
            return data['hits'][0]['largeImageURL']
        return None
