import asab
import asab.web
import asab.web.rest
import asab.web.session
from addons.session import AppSession
from routes import auth as route_auth
from routes import user as route_user


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


if __name__ == '__main__':
    app = WebService()
    app.run()
