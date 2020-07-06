import asab
# import pymongo
# import mongoengine
from mongoengine import connect
from .models.user.user import User
import json
from addons.encoders.json_encoder import JSONEncoder

# connect('flask-mongodb')


class DatabaseService(asab.Service):
    def __init__(self, app, service_name):
        super().__init__(app, service_name)
        self.__initialize_db()

    def __initialize_db(self):
        connect('flask-mongodb')

    def find_all(self, col_name_str):
        print(" find_all")
        user = User.objects.first()
        user_obj = json.loads(user.to_json())
        print(" --- user_obj:", user_obj)
        print(" --- TYPE user_obj:", type(user_obj))
        print(" ----- ")
        return user_obj
        # col_name = self.db[col_name_str]  # Collection nambe
        # doc = list(col_name.find())  # add all data in a List
        # doc = json.loads(json.dumps(doc, indent=4, cls=JSONEncoder))
        # return doc
