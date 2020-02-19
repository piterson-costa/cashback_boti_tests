from api.adapters.dbconnection import MyMongoDB


class Config(object):
    SECRET_KEY = 'ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm'
    URL_API = 'https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf=12312312323'
    BD = 'boticario_teste'

    def get_connection(self):
        db = MyMongoDB(self.BD)
        return db
