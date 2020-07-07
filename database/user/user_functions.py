import asab
from mongoengine import DoesNotExist, NotUniqueError, Q, ValidationError

# from addons.redis.translator import redis_get, redis_set
from addons.utils import mongo_list_to_dict, mongo_dict_to_dict
from datetime import datetime
import jwt
from datetime import timedelta


def insert_new_data(db_model, new_data, msg):
    new_data.pop("password_confirm")
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
        return False, None, "Duplicate Email `%s`" % new_data["email"]
        # return False, str(e)

    new_data["id"] = str(inserted_data.id)
    new_data["created_at"] = inserted_data.created_at.strftime("%Y-%m-%d, %H:%M:%S")
    new_data["updated_at"] = inserted_data.updated_at.strftime("%Y-%m-%d, %H:%M:%S")

    if len(inserted_data) > 0:
        return True, inserted_data, msg
    else:
        return False, None, msg


def get_all_users(db_model, args=None):
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


def get_user_by_userid(db_model, userid):
    try:
        data = db_model.objects.get(id=userid).to_json()
    # except DoesNotExist:
    except Exception as e:
        return False, None, str(e)

    dict_data = mongo_dict_to_dict(data)

    return True, dict_data, None


def get_user_by_username(db_model, username):
    try:
        data = db_model.objects.get(username=username).to_json()
    # except DoesNotExist:
    except Exception as e:
        # print(" --- e:", e)
        return False, None

    dict_data = mongo_dict_to_dict(data)

    return True, dict_data


def del_user_by_userid(db_model, userid):
    try:
        db_model.objects.get(id=userid).delete()
    # except DoesNotExist:
    except Exception as e:
        return False, str(e)

    return True, None


def upd_user_by_userid(db_model, userid, new_data):
    try:
        db_model.objects.get(id=userid).update(**new_data)
    # except DoesNotExist:
    except Exception as e:
        return False, None, str(e)

    new_data["id"] = userid
    new_data["updated_at"] = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

    return True, new_data, None


def store_jwt_data(json_data):
    payload = {
        "username": json_data["username"],
        'exp': datetime.utcnow() + timedelta(seconds=int(asab.Config["jwt"]["exp_delta_seconds"]))
    }
    access_token = jwt.encode(payload, asab.Config["jwt"]["secret_key"], algorithm=asab.Config["jwt"]["algorithm"])

    decoded_data = jwt.decode(access_token, verify=False)
    # print(" --- decoded_data: ", decoded_data)

    # access_jti = get_jti(encoded_token=access_token)
    # refresh_jti = get_jti(encoded_token=refresh_token)

    # redis_set(rc, access_jti, False, app.config["LIMIT_ACCESS_TOKEN"])
    # redis_set(rc, refresh_jti, False, app.config["LIMIT_REFRESH_TOKEN"])

    access_token_expired = jwt.decode(access_token, verify=False)["exp"]
    # refresh_token_expired = jwt.decode(jwt_token, verify=False)["exp"]

    # redis_set(rc, json_data["username"] + "-access-token-exp", False, app.config["LIMIT_ACCESS_TOKEN"])
    # redis_set(rc, json_data["username"] + "-refresh-token-exp", False, app.config["LIMIT_REFRESH_TOKEN"])

    return access_token.decode(), access_token_expired
    # return access_token, refresh_token, access_token_expired, refresh_token_expired


# def get_user_data_by_hobby(ses, db_model, hobby, register_after):
#     try:
#         data = ses.query(db_model).filter_by(hobby=hobby).filter(cast(db_model.create_time, Date) >= register_after).all()
#     except DoesNotExist:
#         return False, None
#     dict_user = sqlresp_to_dict(data)
#
#     if len(dict_user) > 0:
#         return True, dict_user
#     else:
#         return False, None


# def get_user_by_date(db_model, val_date):
#     try:
#         print()
#         val_date = datetime.strptime(val_date, "%Y-%m-%d").date()
#         print(" --- TYPE val_date: ", type(val_date))
#         print(" --- val_date: ", val_date)
#         print(" --- datetime.now(): ", datetime.now())
#         # data = db_model.objects.get(created_at__eq=val_date).all().to_json()
#         # data = db_model.objects.get(created_at__lte=datetime.now()).all().to_json()
#         # data = db_model.objects.get(created_at__lte=datetime.now()).to_json()
#         # data = db_model.objects.get(created_at=val_date).to_json()
#         data = db_model.objects.get(created_at__gt=val_date).to_json()
#         # data = db_model.objects.get(created_at__gte=datetime.now()).to_json()
#         # data = db_model.objects.get(created_at__lte=datetime.now())
#         # print(" --- data:", data)
#     # except DoesNotExist:
#     except Exception as e:
#         print(" ---- DISINI lohhh e:", e)
#         return False, None, "Data not found", 0
#
#     # dict_data = mongo_dict_to_dict(data)
#     dict_data = mongo_list_to_dict(data)
#
#     return True, dict_data, None, len(dict_data)


def get_user_data_between(db_model, start_date, end_date):
    try:
        # start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        # end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        # start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S").date()
        # end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S").date()
        # start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        # end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        # if start_date == end_date:
        #     is_exist, data = get_user_by_date(db_model, start_date)
        #     print(" --- is_exist, data", is_exist, data)
        #     if is_exist:
        #         return is_exist, [data], None, 1
        #     else:
        #         return False, None, "Data not found", 0
        # else:
        data = db_model.objects(
            Q(created_at__gte=start_date) & Q(created_at__lte=end_date)).all().to_json()
                # Q(created_at__gte=datetime(2017, 11, 8)) & Q(created_at__lte=datetime(2020, 1, 9))).all()

    except DoesNotExist:
    # except Exception as e:
    #     print(" ----- e:", e)
    #     return False, [], str(e), 0
        return False, [], "Data not found", 0

    dict_data = mongo_list_to_dict(data)

    if len(dict_data) > 0:
        return True, dict_data, None, len(dict_data)
    else:
        return False, None, "Data not found", 0


# def del_all_data(ses, data_model, args=None):
#     deleted_data = []
#     no_filter = True
#     try:
#         data = None
#         if len(args["filter"]) > 0:
#             if "id" in args["filter"]:
#                 for i in range(len(args["filter"]["id"])):
#                     uid = args["filter"]["id"][i]
#                     data = ses.query(data_model).filter_by(id=uid).one()
#                     deleted_data.append(data.to_dict())
#                     ses.query(data_model).filter_by(id=uid).delete()
#                     no_filter = False
#         if no_filter:
#             data = ses.query(data_model).all()
#             ses.query(data_model).delete()
#     except DoesNotExist:
#         return False, None, "User not found"
#
#     if no_filter:
#         dict_drone = sqlresp_to_dict(data)
#     else:
#         dict_drone = deleted_data
#
#     if len(dict_drone) > 0:
#         return True, dict_drone, None
#     else:
#         return False, None, None

