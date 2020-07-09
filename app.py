import asab
import asab.web
import asab.web.rest
import asab.web.session
from addons.session import AppSession
from routes import auth as route_auth
from routes import user as route_user
from routes import product as route_product
# from routes import part as route_part
from aiohttp_jwt import JWTMiddleware, login_required, check_permissions, match_any
import aiohttp  # https://github.com/hzlmn/aiohttp-jwt/blob/master/example/basic.py
import jwt
from mongoengine import connect
from addons.database_blacklist.blacklist_helpers import is_token_revoked
from addons.redis.my_redis import MyRedis
import json


class WebService(asab.Application):
    async def initialize(self):
        # Connect Database
        connect('flask-mongodb')

        # Loading the web service module
        self.add_module(asab.web.Module)

        # Locate web service
        websvc = self.get_service("asab.WebService")

        # Create a dedicated web container
        container = asab.web.WebContainer(websvc, 'webservice:yawes')

        #  Config routes
        route_auth.route.add_to_router(container.WebApp.router, prefix='/api/auth')
        route_user.route.add_to_router(container.WebApp.router, prefix='/api/users')
        route_product.route.add_to_router(container.WebApp.router, prefix='/api/products')
        # route_part.route.add_to_router(container.WebApp.router, prefix='/api/parts')

        # Add a web session service
        asab.web.session.ServiceWebSession(self, "asab.ServiceWebSession", container.WebApp, session_class=AppSession)

        # Enable exception to JSON exception middleware
        container.WebApp.middlewares.append(asab.web.rest.JsonExceptionMiddleware)

        # Enable exception to JWT middleware
        container.WebApp.middlewares.append(JWTMiddleware(
            secret_or_pub_key=asab.Config["jwt"]["secret_key"],
            request_property="user",
            whitelist=[r"/api/products*", r"/api/parts*", r"/api/auth/login"],
            # whitelist=[r"/api/users*", r"/api/auth/login"],
            # whitelist=[r"/api/auth/login"],
            # credentials_required=False,
            token_getter=self.get_token,
            is_revoked=self.is_revoked,
        ))
        # container.WebApp.router.add_get('/coba', self.protected_handler)
        container.WebApp.router.add_get("/public", self.public_handler)
        container.WebApp.router.add_get("/protected", self.auth_required_handler)
        container.WebApp.router.add_get("/protected2", self.protected_handler)

    async def is_revoked(self, request, payload):
        access_token = None
        try:
            access_token = (request.headers['authorization']).replace("Bearer ", "")

            #  check if the access token has been blacklisted or not
            if is_token_revoked(MyRedis(asab.Config).get_rc(), access_token):
                return True
        except:
            pass
        return False

    async def get_token(self, request):
        access_token = None
        try:
            access_token = (request.headers['authorization']).replace("Bearer ", "")
            access_token = access_token.encode()

            #  check if the access token has been blacklisted or not
            # if is_token_revoked(MyRedis(asab.Config).get_rc(), asab.Config, access_token):
            #     print(" ---- access token blacklisted !!!!!!!")
            #     return aiohttp.web.Response(
            #             text=json.dumps({
            #                 "status": 402,
            #                 "message": "Your access token has been expired",
            #             }, indent=4),
            #             status=402,
            #             content_type='application/json'
            #         )
        except:
            pass
        return access_token

        # print(" --- access_token:", access_token)
        # print(" --- TYPE access_token:", type(access_token))
        # try:
        #     # decoded_data = jwt.decode(access_token, verify=False)
        #     # print(" --- decoded_data: ", decoded_data)
        #     payload = jwt.decode(access_token, asab.Config["jwt"]["secret_key"],
        #                          algorithm=asab.Config["jwt"]["algorithm"])
        #     print(" --- payload:", payload)
        #
        # # except jwt.ExpiredSignatureError:
        # #     print(" --- ExpiredSignatureError ..")
        # #     pass
        #
        # except jwt.ExpiredSignature:
        #     print(" --- token expired ..")
        #     # return aiohttp.web.Response(
        #     #     text=json.dumps({
        #     #         "status": 402,
        #     #         "message": "Your access token has been expired",
        #     #     }, indent=4),
        #         # status=402,
        #         # content_type='application/json'
        #     # )
        #     return access_token
        #     # pass

        # # return aiohttp.web.json_response({'user': request['user']})
        # return jwt.encode({"username": "johndoe"}, asab.Config["jwt"]["secret_key"])
        # # return aiohttp.web.json_response({'user': request['user']})
        # # return jwt.encode(
        # #     {"username": "johndoe", "scopes": ["username:johndoe"]}, asab.Config["jwt"]["secret_key"]
        # # )

    # async def protected_handler(self, request):
    #     return aiohttp.web.json_response({'user': request['payload']})

    @login_required
    async def auth_required_handler(self, request):
        return aiohttp.web.json_response({"username": request["user"]})

    async def public_handler(self, request):
        return aiohttp.web.json_response(
            {
                "username": request["user"].get("username")
                if "user" in request
                else "anonymous"
            }
        )

    @check_permissions(["app/user:admin", "username:johndoe"], comparison=match_any)
    async def protected_handler(self, request):
        print(" --- disini protected_handler ..")
        return aiohttp.web.json_response({"username": request["user"].get("username")})


if __name__ == '__main__':
    app = WebService()
    app.run()
