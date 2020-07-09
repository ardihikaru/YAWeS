from mongoengine import DoesNotExist, NotUniqueError, Q, ValidationError
from addons.utils import mongo_list_to_dict, mongo_dict_to_dict
from datetime import datetime


def insert_new_data(db_model, new_data, msg):
    parts = None
    if "parts" in new_data:
        parts = new_data["parts"]
        new_data.pop("parts")

    try:
        inserted_data = db_model(**new_data).save()

    except ValidationError as e:
        try:
            err_ar = str(e).split("(")
            err = err_ar[2].replace(")", "")
            return False, None, err
        except:
            return False, None, str(e)

    except NotUniqueError as e:
        return False, None, str(e)

    new_data["id"] = str(inserted_data.id)
    new_data["created_at"] = inserted_data.created_at.strftime("%Y-%m-%d, %H:%M:%S")
    new_data["updated_at"] = inserted_data.updated_at.strftime("%Y-%m-%d, %H:%M:%S")

    # TBD
    if parts is not None:
        pass

    if len(inserted_data) > 0:
        return True, inserted_data, msg
    else:
        return False, None, msg


def get_all_data(db_model, args=None):
    try:
        data = db_model.objects().to_json()
        # if args is not None:
        #     if len(args["range"]) == 0:
        #         args["range"] = [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]]
        # else:
        #     args = {
        #         "filter": {},
        #         "range": [local_settings["pagination"]["offset"], local_settings["pagination"]["limit"]],
        #         "sort": []
        #     }
        # data_all = ses.query(db_model).all()
        # data = ses.query(db_model).offset(args["range"][0]).limit(args["range"][1]).all()
    except DoesNotExist:
        return False, None, 0
    data_dict = mongo_list_to_dict(data)

    if len(data_dict) > 0:
        return True, data_dict, len(data_dict)
    else:
        return False, None, 0


def get_data_by_id(db_model, _id):
    try:
        data = db_model.objects.get(id=_id).to_json()
    # except DoesNotExist:
    except Exception as e:
        return False, None, str(e)

    dict_data = mongo_dict_to_dict(data)

    return True, dict_data, None


def del_data_by_id(db_model, _id):
    try:
        db_model.objects.get(id=_id).delete()
    # except DoesNotExist:
    except Exception as e:
        return False, str(e)

    return True, None


def upd_data_by_id(db_model, _id, new_data):
    try:
        db_model.objects.get(id=_id).update(**new_data)
    # except DoesNotExist:
    except Exception as e:
        return False, None, str(e)

    new_data["id"] = _id
    new_data["updated_at"] = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

    return True, new_data, None


def get_data_between_date(db_model, start_date, end_date):
    try:
        data = db_model.objects(
            Q(created_at__gte=start_date) & Q(created_at__lte=end_date)).all().to_json()

    except DoesNotExist:
        return False, [], "Data not found", 0

    dict_data = mongo_list_to_dict(data)

    if len(dict_data) > 0:
        return True, dict_data, None, len(dict_data)
    else:
        return False, None, "Data not found", 0
