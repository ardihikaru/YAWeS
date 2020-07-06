import json
from datetime import datetime


def mongo_list_to_dict(mongo_resp):
    result = []
    list_data = json.loads(mongo_resp)
    for data in list_data:
        data = mongo_dict_to_dict(data, is_dict=True)
        result.append(data)
    return result


def mongo_dict_to_dict(mongo_resp, is_dict=False):
    if is_dict:
        data = mongo_resp
    else:
        data = json.loads(mongo_resp)
    data["id"] = data["_id"]["$oid"]
    data.pop("_id")

    if "created_at" in data and \
            data["created_at"] is not None and \
            "$date" in data["created_at"]:
        data["created_at"] = datetime.fromtimestamp(int(str(data["created_at"]["$date"])[:-3])).strftime("%Y-%m-%d, "
                                                                                                         "%H:%M:%S")

    if "updated_at" in data and \
            data["updated_at"] is not None and \
            "$date" in data["updated_at"]:
        data["updated_at"] = datetime.fromtimestamp(int(str(data["updated_at"]["$date"])[:-3])).strftime("%Y-%m-%d, "
                                                                                                         "%H:%M:%S")

    return data


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
