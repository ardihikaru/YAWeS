# import asab
# import aiohttp
#
# import asab.web
# import asab.web.rest
# import asab.web.session
#
# from .session import AppSession
# from .websocket_factory import WebSocketFactory
# from ..modules
#
# import logging
# L = logging.getLogger(__name__)
#
# asab.Config.add_defaults(
#     {
#         "tags":{
#             "index_hit": "Index was hit!",
#         },
#     }
# )
#
# class WebService(asab.Application):
#     async def initialize(self):
#         # Loading the web service module
#         self.add_module(asab.web.Module)
#
#         # Locate web service
#         websvc = self.get_service("asab.WebService")
#
#         # Create a dedicated web container
#         container = asab.web.WebContainer(websvc, 'webservice:yawes')
#
#         # Add a web session service
#         asab.web.session.ServiceWebSession(self, "asab.ServiceWebSession", container.WebApp, session_class=AppSession)
#
#         # Enable exception to JSON exception middleware
#         container.WebApp.middlewares.append(asab.web.rest.JsonExceptionMiddleware)
#
#         # Add a route
#         container.WebApp.router.add_get('/', self.index)
#         container.WebApp.router.add_get('/api/login', self.login)
#         container.WebApp.router.add_get('/json', self.json)
#         print("Test with curl:\n\t$ curl http://localhost:8080/api/login")
#
#         container.WebApp.router.add_get('/error', self.error)
#
#         # Add a web app
#         asab.web.StaticDirProvider(container.WebApp, '/', "webapp")
#
#         # Add a websocket handler
#         # container.WebApp.router.add_get('/subscribe', WebSocketFactory(self))
#         container.WebApp.router.add_get('/subscribe', WebSocketFactory(self))
#
#         # Add Pub/Sub example
#         self.PubSub.subscribe("Application.tick!", self._on_tick)  # FYI: string value is case sensitive!
#         self.PubSub.subscribe("index_hit!", self._on_index_hit)
#
#     async def _on_tick(self, message_type):
#         print(message_type)
#         int_val = 99
#         str_val = "this is warning!"
#         L.warning("{}, {}".format(int_val, str_val))
#         L.warning("{}: {}, ({})".format(asab.Config["tags"]["index_hit"], int_val, str_val))
#
#     async def _on_index_hit(self, message_type):
#         print(message_type)
#         L.warning("example of warning: %s " % message_type)
#
#     async def login(self, request):
#         session = request.get('Session')
#         return aiohttp.web.Response(text='Hello {}!\n'.format(session))
#
#     async def json(self, request):
#         session = request.get('Session')
#         return aiohttp.web.json_response({
#             "data": "Hello World"
#         })
#
#     async def error(self, request):
#         raise RuntimeError("Errror!!")
#
#     async def index(self, request):
#         self.PubSub.publish("index_hit!")
#         return aiohttp.web.Response(text="Hello world!")
