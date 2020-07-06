# from core.web_service import WebService

import asab
import aiohttp

import asab.web
import asab.web.rest
import asab.web.session

from addons.session import AppSession
from addons.websocket_factory import WebSocketFactory

import logging
import pymongo
import json
from addons.utils import web_response_format
# from addons.encoders.json_encoder import JSONEncoder

L = logging.getLogger(__name__)

asab.Config.add_defaults(
    {
        "tags": {
            "index_hit": "Index was hit!",
        },
    }
)


class WebService(asab.Application):
    async def initialize(self):
        # Loading the web service module
        self.add_module(asab.web.Module)
        ##  Load the OAuth module
        # self.add_module(asab.web.authn.oauth.Module)
        # oauth_client_service = self.get_service("asab.OAuthClientService")

        # Locate web service
        websvc = self.get_service("asab.WebService")

        # Adding MyModule
        from modules import Modules
        self.add_module(Modules)

        # Locating the service
        # mysvc = self.get_service("MyService")
        # mysvc.hallo()
        self.db_data = self.get_service("DatabaseService")
        # db_data = self.get_service("DatabaseService")
        # db_data.find_doc("Users")

        # coba disini
        # print(" 000 disini coba ..")
        # import pymongo
        # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        # mydb = myclient["flask-mongodb"]
        #
        # users = mydb["users"]
        # user_data = users.find_one()
        # print(" --- disini ..")
        # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #
        # mydb = myclient["flask-mongodb"]  # Database Name
        # mycol = mydb["Users"]  # Collection name
        #
        # mydoc = list(mycol.find())  # add all data in a List
        # print(mydoc)
        # print(" ---- ")

        # from motor.motor_asyncio import AsyncIOMotorClient  # pip install motor
        # uri = "mongodb://localhost:27017/"
        # client = AsyncIOMotorClient(uri)
        # db = client.get_database("flask-mongodb")
        # users = db.get_collection("Users")
        # mydoc = list(mycol.find())  # add all data in a List
        # user_data = users.find_one()
        # print(user_data)

        # Create a dedicated web container
        container = asab.web.WebContainer(websvc, 'webservice:yawes')

        # Add a web session service
        asab.web.session.ServiceWebSession(self, "asab.ServiceWebSession", container.WebApp, session_class=AppSession)

        # Enable exception to JSON exception middleware
        container.WebApp.middlewares.append(asab.web.rest.JsonExceptionMiddleware)

        # Add a route
        container.WebApp.router.add_get('/mongo_add', self.mongo_add)
        container.WebApp.router.add_get('/', self.index)
        container.WebApp.router.add_get('/api/login', self.login)
        container.WebApp.router.add_get('/json', self.json)
        print("Test with curl:\n\t$ curl http://localhost:8080/api/login")
        container.WebApp.router.add_get('/users', self.get_user)
        container.WebApp.router.add_post('/api/jsondict', self.jsondict)
        print("""
        Test dict schema example with curl:
        	$ curl http://localhost:8080/api/jsondict -X POST -H "Content-Type: application/json" -d '{"key1":"sample text"}'
        or as form
        	$ curl http://localhost:8080/api/jsondict -X POST -d "key1=sample%20text"
        """)

        container.WebApp.router.add_get('/error', self.error)

        # Add a web app
        asab.web.StaticDirProvider(container.WebApp, '/', "webapp")

        # Add a websocket handler
        # container.WebApp.router.add_get('/subscribe', WebSocketFactory(self))
        container.WebApp.router.add_get('/subscribe', WebSocketFactory(self))

        # Add Pub/Sub example
        self.PubSub.subscribe("Application.tick!", self._on_tick)  # FYI: string value is case sensitive!
        self.PubSub.subscribe("index_hit!", self._on_index_hit)

    # @asab.web.authn.authn_required_handler
    # async def user(self, request, *, identity):
    #     return asab.web.rest.json_response(request=request, data={
    #         'message': 'Hello "{}".'.format(identity),
    #     })

    async def mongo_add(self, request):
        print(" --- disini ..")
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["flask-mongodb"]  # Database Name
        mycol = mydb["Users"]  # Collection name

        mydoc = list(mycol.find())  # add all data in a List
        print(mydoc)
        print(" ---- ")

        j = await request.json()  # request in json formate
        x = mycol.insert_one(j)  # insert data in mongodb
        response_obj = {'id': str(x)}
        print(" --- resp:", response_obj)
        return aiohttp.web.Response(text=json.dumps(response_obj))
        # return aiohttp.web.Response(text=json.dumps(response_obj), status=200)

    async def _on_tick(self, message_type):
        pass
        # print(message_type)
        # int_val = 99
        # str_val = "this is warning!"
        # L.warning("{}, {}".format(int_val, str_val))
        # L.warning("{}: {}, ({})".format(asab.Config["tags"]["index_hit"], int_val, str_val))

    async def _on_index_hit(self, message_type):
        print(message_type)
        L.warning("example of warning: %s " % message_type)

    async def login(self, request):
        session = request.get('Session')
        return aiohttp.web.Response(text='Hello {}!\n'.format(session))

    async def json(self, request):
        session = request.get('Session')
        return aiohttp.web.json_response({
            "data": "Hello World"
        })

    async def get_user(self, request):
        resp_data = self.db_data.find_all("Users")

        print(" -- resp_data = ", resp_data)
        return aiohttp.web.json_response(web_response_format(resp_data))

    @asab.web.rest.json_schema_handler({
        'type': 'object',
        'properties': {
            'key1': {'type': 'string'},
            'key2': {'type': 'number'},
        }})
    async def jsondict(self, request, *, json_data):
        return aiohttp.web.Response(text='Valid data {}\n'.format(json_data))

    async def error(self, request):
        raise RuntimeError("Errror!!")

    async def index(self, request):
        self.PubSub.publish("index_hit!")
        return aiohttp.web.Response(text="Hello world!")


if __name__ == '__main__':
    app = WebService()
    app.run()
