from aiohttp_route_decorator import RouteCollector
import aiohttp
from controllers.user.user import User

route = RouteCollector()


#  example: curl http://localhost:8080/api/auth/login -X POST -H "Content-Type: application/json" -d '{"username":"ardi", "password": "ardi"}'
@route('/login', method='POST')
async def auth_login(request):
    json_data = await request.json()
    resp = User().validate_user(json_data)

    return aiohttp.web.json_response(resp)
    # return aiohttp.web.json_response({
    #     "data": "Auth Login"
    # })


@route('/logout', methods=['GET'])
async def auth_logout(request):
    return aiohttp.web.json_response({
        "data": "Auth logout"
    })
