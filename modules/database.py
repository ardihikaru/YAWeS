import asab
import pymongo
import json
from addons.encoders.json_encoder import JSONEncoder


class DatabaseService(asab.Service):
    def __init__(self, app, service_name):
        super().__init__(app, service_name)
        self.__initialize_db()

    def __initialize_db(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = client["flask-mongodb"]  # Database Name

    def find_all(self, col_name_str):
        col_name = self.db[col_name_str]  # Collection nambe
        doc = list(col_name.find())  # add all data in a List
        doc = json.loads(json.dumps(doc, indent=4, cls=JSONEncoder))
        return doc
