from werkzeug.security import generate_password_hash, check_password_hash
from addons.utils import json_load_str, get_json_template, get_unprocessable_request_json
from addons.database_blacklist.blacklist_helpers import (
    revoke_current_token
)
from database.product.product import ProductModel as DataModel
from database.product.product_functions import get_all_data, del_data_by_id, upd_data_by_id, get_data_by_id, \
    insert_new_data, get_data_between_date
import datetime
import asab
from addons.redis.my_redis import MyRedis


class Product(MyRedis):
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

    def trx_register(self, json_data):
        msg = "Registering a new product succeed."

        #  inserting
        is_valid, inserted_data, msg = insert_new_data(DataModel, json_data, msg)

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
            is_id_exist, user_data = get_data_by_username(DataModel, json_data["username"])
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

    def trx_get_data(self, get_args=None):
        is_valid, users, self.total_records = get_all_data(DataModel, get_args)
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

    def get_data(self, get_args=None):
        get_args = self.__extract_get_args(get_args)
        self.trx_get_data(get_args=get_args)
        return get_json_template(response=self.resp_status, results=self.resp_data, message=self.msg,
                                 total=self.total_records)

    def trx_del_data_by_id(self, _id):
        is_valid, user_data, msg = get_data_by_id(DataModel, _id)
        if is_valid:
            is_valid, msg = del_data_by_id(DataModel, _id)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Deleting data success.")

    def delete_data_by_id(self, json_data):
        if "_id" in json_data:
            if isinstance(json_data["_id"], str):
                self.trx_del_data_by_id(json_data["_id"])
            elif isinstance(json_data["_id"], list):
                for _id in json_data["_id"]:
                    self.trx_del_data_by_id(_id)
            else:
                return get_unprocessable_request_json()
            resp_data = {}
            if self.resp_status:
                resp_data = "Deleted ids: {}".format(json_data["_id"])
            return get_json_template(response=self.resp_status, results=resp_data, total=-1, message=self.msg)
        else:
            return get_unprocessable_request_json()

    def trx_upd_data_by_id(self, _id, json_data):
        is_valid, user_data, msg = upd_data_by_id(DataModel, _id, new_data=json_data)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Updating data success.")

        self.set_resp_data(user_data)

    def update_data_by_id(self, json_data):
        if "_id" in json_data:
            _id = json_data["_id"]
            json_data.pop("_id")
            self.trx_upd_data_by_id(_id, json_data)
            return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)
        else:
            return get_unprocessable_request_json()


    def trx_get_data_by_id(self, _id):
        is_valid, user_data, _ = get_data_by_id(DataModel, _id)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(user_data)

    def get_data_by_id(self, _id):
        self.trx_get_data_by_id(_id)
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
            is_valid, user_data, msg, self.total_records = get_data_data_between(DataModel, start_date, end_date)
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
    # def delete_all_data_data(self, get_args=None):
    #     get_args = self.__extract_get_args(get_args)
    #     run_transaction(sessionmaker(bind=engine), lambda var: self.trx_del_all_data(var, get_args))
    #     return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)
