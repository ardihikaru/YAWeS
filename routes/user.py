from aiohttp_route_decorator import RouteCollector
import aiohttp
from controllers.user.user import User
import json
from addons.utils import get_unprocessable_request
# from aiohttp_jwt import login_required

route = RouteCollector()


# Example: curl http://localhost:8080/api/users -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFyZGkiLCJleHAiOjE1OTQwOTg5OTZ9.qdN_-G--uG1oaTXqNsvssx7G0BfkOIQNL_Ub_ycvhqI" -H "Content-Type: application/json" -d '{"name": "ardi2", "username":"ardi2", "email": "ardihikaru3@gmail.com", "password": "ardi", "password_confirm": "ardi"}'
@route('', methods=['POST', 'GET', 'PUT', 'DELETE'])
# @login_required  # NO NEED if: credentials_required=False (app.py)
async def index(request):
    if request.method == 'POST':
        try:
            json_data = await request.json()
            resp = User().register(json_data)
        except:
            return get_unprocessable_request()

        return aiohttp.web.json_response(resp)

    if request.method == 'GET':
        resp = User().get_users()
        return aiohttp.web.json_response(resp)

    if request.method == 'PUT':
        try:
            json_data = await request.json()
            resp = User().update_data_by_userid(json_data)
        except:
            return get_unprocessable_request()

        return aiohttp.web.json_response(resp)

    if request.method == 'DELETE':
        return aiohttp.web.json_response({
            "data": "Hello API user; Method = %s" % request.method
        })


@route('/ranges/{start_date}/{end_date}', method='GET')
async def get_ranged_user(request):
    try:
        start_date = str(request.match_info['start_date'])
        end_date = str(request.match_info['end_date'])
        resp = User().get_data_between(start_date, end_date)

        # return aiohttp.web.json_response(resp)
        return aiohttp.web.Response(
            text=json.dumps(resp, indent=4),
            status=resp["status"],
            content_type='application/json'
        )
    except:
        return get_unprocessable_request()
    # print(" --- request.match_info: ", type(request.match_info), request.match_info)


# @route('/ranges', method='GET')
# async def get_ranged_user(request):
#     return aiohttp.web.json_response({
#         "data": "Hello user DISINI .."
#     })

# @route('/users', methods=['GET'])
# async def post_user(request):
#     return aiohttp.web.json_response({
#         "data": "Hello user post user"
#     })
