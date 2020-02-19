from flask_api import status
from flask_restful import Resource, reqparse
from api.adapters.lib import Lib
from api.services.auth import validar_jwt
from api.config import Config


class SalesServices(Resource):
    def __init__(self):
        self.db = Config().get_connection()
        self.lib = Lib()

        self.params_request = reqparse.RequestParser(bundle_errors=True)
        self.params_request.add_argument(
            "codigo", type=str, required=True, help="O campo 'codigo' nao pode ser vazio",
        )
        self.params_request.add_argument(
            "venda_cpf", type=str, required=True, help="O campo 'cpf' nao pode ser vazio"
        )

    @validar_jwt
    def get(self):
        """
        :return: mensagem json
        """
        sale_list = []
        for sale in self.db.find_all({}, 'sale'):
            sale['_id'] = str(sale['_id'])
            porcentagem, indice = self.lib.calcular_cashback(float(sale['valor']))
            sale['cashback_porcentagem'] = porcentagem
            sale['cashback_valor'] = round((float(sale['valor']) * float(indice)), 2)
            sale_list.append(sale)

        if sale_list:
            return sale_list, status.HTTP_200_OK

        response = {"message": "Sales not found."}
        return response, status.HTTP_404_NOT_FOUND

    @validar_jwt
    def post(self):
        """
        Create Sales
        :param params: request requisicao
        :return: mensagem json
        """
        self.params_request.add_argument(
            "valor", type=float, required=True, help="O campo 'valor' nao pode ser vazio",
        )
        self.params_request.add_argument(
            "data", type=str, required=True, help="O campo 'data' nao pode ser vazio"
        )

        params = self.params_request.parse_args()

        if self.lib.valida_cpf(params.get("venda_cpf")) is False:
            return {"message": "campo CPF incorreto"}, status.HTTP_404_NOT_FOUND

        if self.lib.valida_data(params.get("data")) is False:
            return {"message": "Invalid Data field"}, status.HTTP_404_NOT_FOUND

        params["status"] = "Em validação" if params.get("venda_cpf") != "15350946056" else "Aprovado"

        if self.db.find_one({'codigo': params.get("codigo")}, 'sale'):
            response = {"message": "Codigo '{}' ja existe.".format(params.get("codigo"))}
            return response, status.HTTP_400_BAD_REQUEST

        self.db.insert(params, 'sale')
        payload = {
            "codigo": params["codigo"],
            "valor": params["valor"],
            "data": params["data"],
            "venda_cpf": params["venda_cpf"]
        }
        return payload, status.HTTP_201_CREATED

    @validar_jwt
    def put(self):
        """
        update_sale
        :param params: request requisicao
        :return: mensagem json
        """
        self.params_request.add_argument(
            "campos_put", type=dict, required=True, help="O campo 'campos_put' nao pode ser vazio"
        )
        params = self.params_request.parse_args()

        if self.lib.valida_cpf(params.get("venda_cpf")) is False:
            return {"message": "campo CPF incorreto"}, status.HTTP_404_NOT_FOUND

        query = {'venda_cpf': params.get("venda_cpf"), 'codigo': params.get("codigo")}
        status_check = self.db.find_one(query, 'sale')
        if status_check:
            if status_check['status'] != 'Aprovado':
                put_list = {}
                for key, value in params['campos_put'].items():

                    if key == 'status' and value != 'Aprovado':
                        value = "Em validação"

                    if value:
                        put_list[key] = value

                if self.db.find_one({'codigo': put_list.get("codigo")}, 'sale') and params.get("codigo") != put_list.get("codigo"):
                    response = {"message": "Codigo '{}' ja existe.".format(put_list.get("codigo"))}
                    return response, status.HTTP_400_BAD_REQUEST

                campos_put = put_list
                self.db.update_one(query, campos_put, 'sale')
                return campos_put, status.HTTP_200_OK
            else:
                response = {"message": "A venda com status Aprovada não pode ser alterada"}
                return response, status.HTTP_404_NOT_FOUND
        else:
            response = {"message": "Venda com codigo '{}' nao existe.".format(params.get("codigo"))}
            return response, status.HTTP_400_BAD_REQUEST

    @validar_jwt
    def delete(self):
        """
        delete_sale
        :param params: request requisicao
        :return: mensagem json
        """
        params = self.params_request.parse_args()

        status_check = self.db.find_one(params, 'sale')
        if status_check:
            if status_check['status'] != 'Aprovado':
                self.db.find_one_and_delete(params, 'sale')
                return {"message": "Venda deletada com sucesso."}, status.HTTP_200_OK
            else:
                response = {"message": "A venda com status Aprovada não pode ser excluída"}
                return response, status.HTTP_404_NOT_FOUND
        else:
            response = {"message": "Venda com codigo '{}' nao existe.".format(params.get("codigo"))}
            return response, status.HTTP_400_BAD_REQUEST


