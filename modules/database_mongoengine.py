import asab
from mongoengine import connect
from .models.user.user import User
from addons.utils import mongo_list_to_dict, mongo_dict_to_dict
from addons.encoders.json_encoder import JSONEncoder
from addons.encoders.mongoengine_encoder import MongoEncoder


class DatabaseService(asab.Service):
    def __init__(self, app, service_name):
        super().__init__(app, service_name)
        self.__initialize_db()

    def __initialize_db(self):
        connect('flask-mongodb')

    def find_all(self, col_name_str):
        user = User.objects.first()
        user_obj = mongo_dict_to_dict(user.to_json())
        return user_obj
