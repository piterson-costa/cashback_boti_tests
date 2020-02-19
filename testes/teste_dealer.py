from random import randint
from api.app import app
from testes.config import Config
from flask_api import status
import unittest


class TesteDealer(unittest.TestCase):
    EMAIL = "email_{}@teste.com".format(randint(1, 9999999))
    PASSWORD = "piterson123"
    NOME = "Piterson"
    CPF = " 08199968907"
    CPF_INVALIDO = "123123"

    def setUp(self):
        config = Config()
        app.config.from_object(config)
        self.app = app.test_client()
        self.response_get = self.app.get("/dealers")

    def test_create_dealer_fail(self):
        response_post = self.app.post("/dealers")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_post.status_code)

    def test_create_dealer_email_fail(self):
        payload = {
            "nome": self.NOME,
            "cpf": self.CPF_INVALIDO,
            "email": None,
            "senha": self.PASSWORD
        }
        response_post = self.app.post("/dealers", data=payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_post.status_code)
        response = {"message": {"email": "O campo 'email' esta incorreto"}}
        self.assertEqual(response, response_post.json)

    def test_create_dealer_cpf_fail(self):
        payload = {
            "nome": self.NOME,
            "cpf": self.CPF_INVALIDO,
            "email": self.EMAIL,
            "senha": self.PASSWORD
        }
        response_post = self.app.post("/dealers", data=payload)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response_post.status_code)

        response = {"message": "campo CPF incorreto"}
        self.assertEqual(response, response_post.json)

    def test_create_dealer_success(self):
        payload = {
            "nome": self.NOME,
            "cpf": self.CPF,
            "email": self.EMAIL,
            "senha": self.PASSWORD
        }
        response_post = self.app.post("/dealers", data=payload)
        self.assertEqual(status.HTTP_201_CREATED, response_post.status_code)

