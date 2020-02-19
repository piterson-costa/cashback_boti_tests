from api.adapters.lib import Lib
from flask import request, current_app
from functools import wraps
import jwt
import datetime

from flask_api import status
from flask_restful import Resource, reqparse
from api.config import Config

config = Config()
db = config.get_connection()
lib = Lib()


class AuthServices(Resource):
    def __init__(self):
        self.db = Config().get_connection()

    def get(self):
        """
        login - valid_dealer
        :param params: request requisicao
        :return: mensagem json
        """
        params_request = reqparse.RequestParser()
        params_request.add_argument("cpf", type=str, required=True, help="O campo 'cpf' nao pode ser vazio")
        params_request.add_argument("senha", type=str, required=True, help="O campo 'senha' nao pode ser vazio")

        params = params_request.parse_args()

        data = self.db.find_one({'cpf': params['cpf']}, 'dealer')
        if not data:
            response = {"message": "O cpf esta incorreto"}
            return response, status.HTTP_401_UNAUTHORIZED
        else:
            if lib.verify_password(data['senha'], params['senha']):
                response = {"authorization": gerar_jwt(params['cpf'])}
                return response, status.HTTP_200_OK
            else:
                response = {"message": "A senha esta incorreta"}
                return response, status.HTTP_401_UNAUTHORIZED


def gerar_jwt(dealer_cpf: str) -> str:
    """
    :param dealer_cpf: cpf do revendedor
    :return: token jwt
    """
    token_jwt = jwt.encode({
        'dealer': dealer_cpf,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, config.SECRET_KEY)

    return token_jwt.decode("utf-8")


def validar_jwt(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get('authorization')
        if not authorization:
            return 'Header authorization obrigatorio', status.HTTP_401_UNAUTHORIZED
        try:
            data = jwt.decode(authorization, config.SECRET_KEY, True, 'HS256')
            db.find_one({'cpf': data['dealer']}, 'dealer')

        except Exception:
            return 'Header authorization incorreto', status.HTTP_401_UNAUTHORIZED

        return f(*args, **kwargs)

    return wrapper
