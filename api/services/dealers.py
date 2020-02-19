from flask_api import status
from flask_restful import Resource, reqparse
from api.config import Config
from api.adapters.lib import Lib


class DealersServices(Resource):
    def __init__(self):
        self.db = Config().get_connection()
        self.lib = Lib()

    def get(self):
        dealers = []
        for dealer in self.db.find_all({}, 'dealer'):
            dealer['_id'] = str(dealer['_id'])
            dealers.append(dealer)

        if dealers:
            return dealers, status.HTTP_200_OK

        response = {"message": "Erro ao resgatar dados."}
        return response, status.HTTP_404_NOT_FOUND

    def post(self):
        params_request = reqparse.RequestParser(bundle_errors=True)
        params_request.add_argument(
            "email",
            type=self.lib.valida_email,
            required=True,
            nullable=False,
            trim=True,
            help="O campo 'email' esta incorreto",
        )
        params_request.add_argument(
            "senha",
            type=self.lib.valida_nulo,
            required=True,
            nullable=False,
            trim=True,
            help="O campo 'senha' esta incorreto",
        )
        params_request.add_argument(
            "nome",
            type=self.lib.valida_nulo,
            required=True,
            nullable=False,
            trim=True,
            help="O campo 'nome' esta incorreto",
        )
        params_request.add_argument(
            "cpf",
            type=self.lib.valida_nulo,
            required=True,
            nullable=False,
            trim=True,
            help="O campo 'cpf' esta incorreto",
        )

        params = params_request.parse_args()

        if self.lib.valida_cpf(params.get("cpf")) is False:
            response = {"message": "campo CPF incorreto"}
            return response, status.HTTP_404_NOT_FOUND

        if self.db.find_one({'email': params.get("email")}, 'dealer'):
            response = {"message": "O email '{}' ja existe.".format(params.get("email"))}
            return response, status.HTTP_400_BAD_REQUEST
        else:
            params['senha'] = self.lib.hash_password(params['senha'])
            self.db.insert(params, 'dealer')

            payload = {
                "nome": params["nome"],
                "cpf": params["cpf"],
                "email": params["email"],
                "senha": params["senha"]
            }
            return payload, status.HTTP_201_CREATED
