from random import randint
from api.app import app
from testes.config import Config
from api.adapters.lib import Lib
from flask_api import status
import unittest


class TesteSales(unittest.TestCase):
    codigo = randint(1, 9999999)
    codigo_two = randint(1, 9999999)
    email = "email_{}@teste.com".format(randint(1, 9999999))
    nome = "piterson costa"
    cpf_valido = Lib.gera_cpf()
    senha = "piterson123"
    valor = 2222.00
    data = "2020-03-15"
    JWT = ""

    def setUp(self):
        config = Config()
        app.config.from_object(config)
        self.app = app.test_client()
        payload = {
            "email": self.email,
            "senha": self.senha,
            "nome": self.nome,
            "cpf": self.cpf_valido,
        }
        response_dealer = self.app.post("/dealers", data=payload)

        if response_dealer.status_code == status.HTTP_201_CREATED:
            payload_login = {"cpf": self.cpf_valido, "senha": self.senha}
            login_request = self.app.get("/login", data=payload_login)
            self.__class__.JWT = login_request.json.get("authorization")

    def test_create_sales_success(self):
        payload = {
            "codigo": self.codigo,
            "valor": self.valor,
            "data": self.data,
            "venda_cpf": '15350946056'
        }
        headers = {"authorization": str(self.__class__.JWT)}
        sales_request = self.app.post("/sales", headers=headers, data=payload)
        self.assertEqual(sales_request.status_code, status.HTTP_201_CREATED)

        # # user to delete
        payload = {
            "codigo": self.codigo_two,
            "valor": self.valor,
            "data": self.data,
            "venda_cpf": self.cpf_valido,
        }
        headers = {"authorization": str(self.__class__.JWT)}
        self.app.post("/sales", headers=headers, data=payload)

    def test_get_sales_success(self):
        headers = {"authorization": str(self.__class__.JWT)}
        sales_request = self.app.get("/sales", headers=headers)
        self.assertEqual(sales_request.status_code, status.HTTP_200_OK)

    def test_delete_sale_success(self):
        payload = {
            "codigo": self.codigo_two,
            "venda_cpf": self.cpf_valido
        }

        headers = {"authorization": str(self.__class__.JWT)}
        sales_request = self.app.delete("/sales_delete", headers=headers, data=payload)
        self.assertEqual(sales_request.status_code, status.HTTP_200_OK)

    def test_delete_sale_fail(self):
        payload = {
            "codigo": self.codigo,
            "venda_cpf": '15350946056'
        }

        headers = {"authorization": str(self.__class__.JWT)}
        sales_request = self.app.delete("/sales_delete", headers=headers, data=payload)
        self.assertEqual(sales_request.status_code, status.HTTP_404_NOT_FOUND)
