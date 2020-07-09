from aiohttp_route_decorator import RouteCollector
import aiohttp
from controllers.part.part import Part as DataController
import json
from addons.utils import get_unprocessable_request
# from aiohttp_jwt import login_required

route = RouteCollector()


# Example: curl http://localhost:8080/api/product -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFyZGkiLCJleHAiOjE1OTQwOTg5OTZ9.qdN_-G--uG1oaTXqNsvssx7G0BfkOIQNL_Ub_ycvhqI" -H "Content-Type: application/json" -d '{"name": "ardi2", "username":"ardi2", "email": "ardihikaru3@gmail.com", "password": "ardi", "password_confirm": "ardi"}'
@route('', methods=['POST', 'GET', 'PUT', 'DELETE'])
async def index(request):
    if request.method == 'POST':
        try:
            json_data = await request.json()
            resp = DataController().register(json_data)
        except:
            return get_unprocessable_request()

        return aiohttp.web.json_response(resp)

    if request.method == 'GET':
        resp = DataController().get_data()
        return aiohttp.web.json_response(resp)

    if request.method == 'PUT':
        try:
            json_data = await request.json()
            resp = DataController().update_data_by_id(json_data)
        except:
            return get_unprocessable_request()

        return aiohttp.web.json_response(resp)

    if request.method == 'DELETE':
        try:
            json_data = await request.json()
            resp = DataController().delete_data_by_id(json_data)
        except:
            return get_unprocessable_request()

        return aiohttp.web.json_response(resp)


@route('/ranges/{start_date}/{end_date}', method='GET')
async def get_ranged_user(request):
    try:
        start_date = str(request.match_info['start_date'])
        end_date = str(request.match_info['end_date'])
        resp = DataController().get_data_between(start_date, end_date)

        return aiohttp.web.Response(
            text=json.dumps(resp, indent=4),
            status=resp["status"],
            content_type='application/json'
        )
    except:
        return get_unprocessable_request()
