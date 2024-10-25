import requests
import json
import time
import base64
from deep_translator import GoogleTranslator

class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):

        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        return response.json()[0]['id']

    def generate_image(self, prompt, model, images=1, width=512, height=512):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {"query": prompt}
        }
        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }

        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        return response.json()['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images'][0]
            attempts -= 1
            time.sleep(delay)

    def save_image(self, image_base64, filename="image.png"):
        image_data = base64.b64decode(image_base64)
        with open(filename, "wb") as file:
            file.write(image_data)
