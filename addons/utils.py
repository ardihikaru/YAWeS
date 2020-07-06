import json
from bson import ObjectId
import datetime
from addons.encoders.json_encoder import JSONEncoder

def web_response_format(data, msg="-", is_list=False):
    if is_list:
        total = len(data)
    else:  # should be a dict!
        total = 1
    obj_resp = {
        "message": msg,
        "data": data,
        "total": total
    }

    return obj_resp

#
# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)


# data = {'message': '-', 'data': [{'_id': ObjectId('5efe071088be17f5c3c53b05'), 'name': 'string', 'username': 'string', 'email': 'string', 'hobby': 'string', 'password': 'pbkdf2:sha256:150000$SL4kJhM5$da1dfc8b390082c7a17577101926fae8fcdc96697552b7d046995a852b6649bd', 'created_at': datetime.datetime(2020, 7, 2, 16, 10, 56, 540000), 'updated_at': datetime.datetime(2020, 7, 3, 0, 10, 56, 541000)}, {'_id': ObjectId('5efe072988be17f5c3c53b06'), 'name': 'ardi', 'username': 'ardi', 'email': 'ardi', 'hobby': 'ardi', 'password': 'pbkdf2:sha256:150000$5ar2I2K5$4a8292e02448c1fcf3d5ceacc26d05becd4ee2cfdb7e0e4174d1b2e19ca7d425', 'created_at': datetime.datetime(2020, 7, 2, 16, 11, 21, 979000), 'updated_at': datetime.datetime(2020, 7, 3, 0, 11, 21, 979000)}], 'total': 1}

# databaru = JSONEncoder().encode(data)
# databaru = DateTimeEncoder().encode(data)
# print(databaru)
# print(type(databaru))


# from json import JSONEncoder

# employee = {
#     "id": 456,
#     "name": "William Smith",
#     "salary": 8000,
#     "joindate": datetime.datetime.now()
# }
#
# # subclass JSONEncoder
# # class DateTimeEncoder(JSONEncoder):
# #         #Override the default method
# #         def default(self, obj):
# #             if isinstance(obj, (datetime.date, datetime.datetime)):
# #                 return obj.isoformat()
#
# print("Printing to check how it will look like")
# print(DateTimeEncoder().encode(employee))
# print(DateTimeEncoder().encode(data))
# print(type(data))

# print("Encode DateTime Object into JSON using custom JSONEncoder")
# # employeeJSONData = json.dumps(employee, indent=4, cls=DateTimeEncoder)
# employeeJSONData = json.dumps(data, indent=4, cls=JSONEncoder)
# print(employeeJSONData)
# print(type(employeeJSONData))
