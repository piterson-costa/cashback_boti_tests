from flask_api import status
from flask_restful import Resource
from api.config import Config
import requests
import json


class CashbackServices(Resource):
    def __init__(self):
        self.config = Config()

    def get(self):
        """
            :return: mensagem json
        """
        try:
            req = requests.get(self.config.URL_API, headers={'token': self.config.SECRET_KEY})
        except ConnectionError:
            return 'Problema ao conectar com a API', status.HTTP_500_INTERNAL_SERVER_ERROR

        http_code = req.status_code
        if http_code != 200:
            response = {"message": "Problema ao conectar com a API."}
            return response, http_code
        else:
            ret = json.loads(req.text)
            return ret['body'], status.HTTP_200_OK

