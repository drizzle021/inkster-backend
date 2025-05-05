from functools import wraps
from flask import request
from flask_jwt_extended import decode_token

def ws_auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        if not token:
            print(e)
            print("Unauthorized")
            return False

        try:
            decoded_data = decode_token(token)
            user_id = decoded_data["sub"]
            return func(user_id, *args, **kwargs)
        except Exception as e:
            print(e)
            print("Unauthorized")
            return False
    return wrapper