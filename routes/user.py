from aiohttp_route_decorator import RouteCollector
import aiohttp
from controllers.user.user import User

route = RouteCollector()


@route('', methods=['POST', 'GET', 'PUT', 'DELETE'])
async def index(request):
    if request.method == 'POST':
        json_data = await request.json()
        print(" --- json_data = ", json_data)

        resp = User().register(json_data)

        return aiohttp.web.json_response({
            "data": "Hello API user; Method = %s" % request.method
        })

    if request.method == 'GET':
        return aiohttp.web.json_response({
            "data": "Hello API user; Method = %s" % request.method
        })

    if request.method == 'PUT':
        return aiohttp.web.json_response({
            "data": "Hello API user; Method = %s" % request.method
        })

    if request.method == 'DELETE':
        return aiohttp.web.json_response({
            "data": "Hello API user; Method = %s" % request.method
        })


@route('/ranges/{start_date}/{end_date}', method='GET')
async def get_ranged_user(request):
    print(" ---- start_date: ", request.match_info['start_date'])
    print(" ---- end_date: ", request.match_info['end_date'])
    return aiohttp.web.json_response({
        "data": "Hello user get"
    })

@route('/ranges', method='GET')
async def get_ranged_user(request):
    return aiohttp.web.json_response({
        "data": "Hello user DISINI .."
    })

# @route('/users', methods=['GET'])
# async def post_user(request):
#     return aiohttp.web.json_response({
#         "data": "Hello user post user"
#     })
