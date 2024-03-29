from werkzeug.security import generate_password_hash, check_password_hash
from addons.utils import json_load_str, get_json_template, get_unprocessable_request_json
from addons.database_blacklist.blacklist_helpers import (
    revoke_current_token
    # revoke_current_token, extract_identity
)
# from .user_model import UserModel
from database.user.user import UserModel
# from .user_functions import get_all_users, store_jwt_data, get_user_by_username, get_user_by_date, \
# from .user_functions import get_all_users, store_jwt_data, get_user_by_username, \
from database.user.user_functions import get_all_users, store_jwt_data, get_user_by_username, \
    del_user_by_userid, upd_user_by_userid, get_user_by_userid, insert_new_data, get_user_data_between
    # del_user_by_userid, upd_user_by_userid, get_user_by_userid, insert_new_data, get_user_data_by_hobby, \
    # get_user_data_between, del_all_data
import datetime
import asab
from addons.redis.my_redis import MyRedis


class User(MyRedis):
    def __init__(self):
        super().__init__(asab.Config)
        self.status_code = 200
        self.resp_status = None
        self.resp_data = None
        self.total_records = 0
        self.msg = None
        self.password_hash = None

    def set_status_code(self, code):
        self.status_code = code

    def set_resp_status(self, status):
        self.resp_status = status

    def set_resp_data(self, json_data):
        self.resp_data = json_data

    def set_msg(self, msg):
        self.msg = msg

    def set_password(self, passwd):
        self.password_hash = generate_password_hash(passwd)

    def is_password_match(self, password):
        return check_password_hash(self.password_hash, password)

    def revokesExistedToken(self, encoded_token=None):
        if encoded_token:
            revoke_current_token(self.rc, asab.Config, encoded_token, {"revoke": True})

    def do_logout(self, encoded_token=None):
        self.revokesExistedToken(encoded_token)
        return get_json_template(response=True, results=-1, total=-1, message="Logout Success.")

    def __validate_register_data(self, json_data):
        is_input_valid = True
        if "name" not in json_data:
            return False, "Name should not be EMPTY."

        if "username" not in json_data:
            return False, "Username should not be EMPTY."

        if "email" not in json_data:
            return False, "Email should not be EMPTY."

        if "password" not in json_data:
            return False, "Password should not be EMPTY."

        if "password_confirm" not in json_data:
            return False, "Password Confirmation is EMPTY."

        if json_data["password"] != json_data["password_confirm"]:
            return False, "Password Confirmation missmatch with Password."

        if is_input_valid:
            # is_id_exist, _ = get_user_by_username(UserModel, json_data["username"])
            is_id_exist, _ = get_user_by_username(UserModel, json_data["username"])
            if is_id_exist:
                return False, "Username `%s` have been used." % json_data["username"]

        return True, None

    def trx_register(self, json_data):
        is_valid, msg = self.__validate_register_data(json_data)
        self.set_resp_status(is_valid)
        self.set_msg(msg)

        if is_valid:
            msg = "Registration is success. Now, you can login into our system."
            self.set_password(json_data["password"])
            json_data["password"] = self.password_hash

            #  inserting
            is_valid, inserted_data, msg = insert_new_data(UserModel, json_data, msg)

            # clean up sensitive data
            json_data.pop("password")
            # json_data.pop("password_confirm")

            self.set_msg(msg)

        self.set_resp_data(json_data)

    def register(self, json_data):
        self.trx_register(json_data)
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def __validate_login_data(self, json_data):
        self.set_resp_status(False)
        self.set_resp_data(json_data)
        is_input_valid = True
        if "username" not in json_data:
            is_input_valid = False
            self.set_msg("Username should not be EMPTY.")

        if "password" not in json_data:
            is_input_valid = False
            self.set_msg("Password should not be EMPTY.")

        if is_input_valid:
            is_id_exist, user_data = get_user_by_username(UserModel, json_data["username"])
            if is_id_exist:
                self.password_hash = user_data["password"]
                if self.is_password_match(json_data["password"]):  # check password
                    self.set_resp_status(is_id_exist)
                    self.set_msg("User data FOUND.")

                    # access_token, refresh_token, access_token_expired, refresh_token_expired = store_jwt_data(json_data)
                    access_token, access_token_expired = store_jwt_data(json_data)

                    # set resp_data
                    resp_data = {"access_token": access_token,
                                 "access_token_expired": access_token_expired,
                                 "username": json_data["username"]}
                    self.set_resp_data(resp_data)
                else:
                    self.set_msg("Incorrect Password.")
            else:
                self.set_msg("Incorrect Username.")

    def validate_user(self, json_data):
        self.__validate_login_data(json_data)
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_get_users(self, get_args=None):
        is_valid, users, self.total_records = get_all_users(UserModel, get_args)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(users)

    def __extract_get_args(self, get_args):
        if get_args is not None:
            if "filter" in get_args:
                get_args["filter"] = json_load_str(get_args["filter"], "dict")
            if "range" in get_args:
                get_args["range"] = json_load_str(get_args["range"], "list")
            if "sort" in get_args:
                get_args["sort"] = json_load_str(get_args["sort"], "list")

        return get_args

    def get_users(self, get_args=None):
        get_args = self.__extract_get_args(get_args)
        self.trx_get_users(get_args=get_args)
        return get_json_template(response=self.resp_status, results=self.resp_data, message=self.msg,
                                 total=self.total_records)

    def trx_del_data_by_userid(self, userid):
        is_valid, user_data, msg = get_user_by_userid(UserModel, userid)
        if is_valid:
            is_valid, msg = del_user_by_userid(UserModel, userid)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Deleting data success.")

    def delete_data_by_userid(self, json_data):
        if "user_id" in json_data:
            if isinstance(json_data["user_id"], str):
                self.trx_del_data_by_userid(json_data["user_id"])
            elif isinstance(json_data["user_id"], list):
                for user_id in json_data["user_id"]:
                    self.trx_del_data_by_userid(user_id)
            else:
                return get_unprocessable_request_json()
            resp_data = {}
            if self.resp_status:
                resp_data = "Deleted ids: {}".format(json_data["user_id"])
            return get_json_template(response=self.resp_status, results=resp_data, total=-1, message=self.msg)
        else:
            return get_unprocessable_request_json()

    def trx_upd_data_by_userid(self, userid, json_data):
        is_valid, user_data, msg = upd_user_by_userid(UserModel, userid, new_data=json_data)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Updating data success.")

        self.set_resp_data(user_data)

    def update_data_by_userid(self, json_data):
        if "user_id" in json_data:
            user_id = json_data["user_id"]
            json_data.pop("user_id")
            self.trx_upd_data_by_userid(user_id, json_data)
            return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)
        else:
            return get_unprocessable_request_json()


    def trx_get_data_by_userid(self, userid):
        is_valid, user_data, _ = get_user_by_userid(UserModel, userid)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(user_data)

    def get_data_by_userid(self, userid):
        self.trx_get_data_by_userid(userid)
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def __sync_start_date(self, start_date):
        date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        date_obj_new = date_obj - datetime.timedelta(days=1)
        date_time = date_obj_new.strftime("%Y-%m-%d")
        return date_time

    def trx_get_data_between(self, start_date, end_date):
        try:
            start_date = self.__sync_start_date(start_date)
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            is_valid, user_data, msg, self.total_records = get_user_data_between(UserModel, start_date, end_date)
            self.set_resp_status(is_valid)
            self.set_msg(msg)
            if is_valid:
                self.set_msg("Collecting data success.")

            self.set_resp_data(user_data)
        except:
            self.set_resp_status(False)
            self.set_msg("Unprocessable Entity")
            self.set_resp_data({})
            self.set_status_code(422)


    def get_data_between(self, start_date, end_date):
        self.trx_get_data_between(start_date, end_date)
        return get_json_template(response=self.resp_status, results=self.resp_data, total=self.total_records,
                                 message=self.msg, status=self.status_code)

    # def trx_del_all_data(self, ses, get_args=None):
    #     is_valid, user_data, msg = del_all_data(ses, User, get_args)
    #     if user_data is None:
    #         is_valid = False
    #         msg = "user data not found"
    #     self.set_resp_status(is_valid)
    #     self.set_msg(msg)
    #     if is_valid:
    #         self.set_msg("Deleting all user data success.")
    #
    #     self.set_resp_data(user_data)
    #
    # def delete_all_user_data(self, get_args=None):
    #     get_args = self.__extract_get_args(get_args)
    #     run_transaction(sessionmaker(bind=engine), lambda var: self.trx_del_all_data(var, get_args))
    #     return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)
