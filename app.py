import asab
import asab.web
import asab.web.rest
import asab.web.session
from addons.session import AppSession
from routes import auth as route_auth
from routes import user as route_user
from aiohttp_jwt import JWTMiddleware, login_required, check_permissions, match_any
import aiohttp  # https://github.com/hzlmn/aiohttp-jwt/blob/master/example/basic.py
import jwt


class WebService(asab.Application):
    async def initialize(self):
        # Loading the web service module
        self.add_module(asab.web.Module)

        # Locate web service
        websvc = self.get_service("asab.WebService")

        # Create a dedicated web container
        container = asab.web.WebContainer(websvc, 'webservice:yawes')

        #  Config routes
        route_auth.route.add_to_router(container.WebApp.router, prefix='/api/auth')
        route_user.route.add_to_router(container.WebApp.router, prefix='/api/users')

        # Add a web session service
        asab.web.session.ServiceWebSession(self, "asab.ServiceWebSession", container.WebApp, session_class=AppSession)

        # Enable exception to JSON exception middleware
        container.WebApp.middlewares.append(asab.web.rest.JsonExceptionMiddleware)

        # Enable exception to JWT middleware
        container.WebApp.middlewares.append(JWTMiddleware(
            secret_or_pub_key=asab.Config["config"]["secret_key"],
            request_property="user",
            whitelist=[r"/api/users*", r"/api/auth/login"],
            credentials_required=False,
            token_getter=self.get_token,
            # whitelist=[r"/api/auth/login"],
        ))
        # container.WebApp.router.add_get('/coba', self.protected_handler)
        container.WebApp.router.add_get("/public", self.public_handler)
        container.WebApp.router.add_get("/protected", self.auth_required_handler)
        container.WebApp.router.add_get("/protected2", self.protected_handler)

    async def get_token(self, request):
        print(" --- disini ..")
        # return jwt.encode({"username": "johndoe"}, asab.Config["config"]["secret_key"])
        return jwt.encode(
            {"username": "johndoe", "scopes": ["username:johndoe"]}, asab.Config["config"]["secret_key"]
        )

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
