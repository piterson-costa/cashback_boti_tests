from flask import Flask
from flask_restful import Api
from api.services.dealers import DealersServices
from api.services.sales import SalesServices
from api.services.auth import AuthServices
from api.services.cashback import CashbackServices
from api.config import Config

config = Config()
app = Flask(__name__)
app.config.from_object(config)
api = Api(app)


api.add_resource(DealersServices, '/dealers')
api.add_resource(SalesServices, "/sales", "/sales_create", "/sales_update", "/sales_delete")
api.add_resource(AuthServices, "/login")
api.add_resource(CashbackServices, "/get_cashback")


def test_client():
    return None
