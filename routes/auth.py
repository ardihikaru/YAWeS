from aiohttp_route_decorator import RouteCollector
import aiohttp

route = RouteCollector()


@route('/login', method='POST')
async def auth_login(request):
    return aiohttp.web.json_response({
        "data": "Auth Login"
    })


@route('/logout', methods=['GET'])
async def auth_logout(request):
    return aiohttp.web.json_response({
        "data": "Auth logout"
    })
