from datetime import datetime
from jwt import decode as decode_token
from addons.redis.translator import redis_set, redis_get
import jwt


# def _epoch_utc_to_datetime(epoch_utc):
#     """
#     Helper function for converting epoch timestamps (as stored in JWTs) into
#     python datetime objects (which are easier to use with sqlalchemy).
#     """
#     return datetime.fromtimestamp(epoch_utc)


# def extract_identity(encoded_token):
#     decoded_token = decode_token(encoded_token)
#     return decoded_token["identity"]

# added into blacklist key-value; key = access_token, value = data, exp = exp_delta_seconds
def revoke_current_token(rc, config, encoded_token, json_data):
    result = {"message": None, "resp_code": 400}
    decoded_token = jwt.decode(encoded_token, verify=False)
    redis_set(rc, encoded_token.decode(), decoded_token, config["jwt"]["exp_delta_seconds"])
    result["message"] = "Token revoked"
    result["resp_code"] = 200

    return result


def is_token_revoked(rc, decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    data = redis_get(rc, decoded_token.encode())
    if data is None:
        return False
    else:
        return True

