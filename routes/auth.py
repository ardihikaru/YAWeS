from aiohttp_route_decorator import RouteCollector
import aiohttp
from controllers.user.user import User

route = RouteCollector()


#  Example: curl http://localhost:8080/api/auth/login -X POST -H "Content-Type: application/json" -d '{"username":"ardi", "password": "ardi"}'
@route('/login', method='POST')
async def auth_login(request):
    json_data = await request.json()
    resp = User().validate_user(json_data)

    return aiohttp.web.json_response(resp)
    # return aiohttp.web.json_response({
    #     "data": "Auth Login"
    # })


# Example: curl http://localhost:8080/api/auth/logout -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFyZGkiLCJleHAiOjE1OTQwOTg5OTZ9.qdN"
@route('/logout', methods=['GET'])
async def auth_logout(request):
    access_token = None
    try:
        access_token = (request.headers['authorization']).replace("Bearer ", "")
        access_token = access_token.encode()
    except:
        pass
    resp = User().do_logout(access_token)

    return aiohttp.web.json_response(resp)
