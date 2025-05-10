from functools import wraps
from flask import request
from flask_jwt_extended import decode_token

def ws_auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = request.environ.get('user_id')
        if not user_id:
            print("Unauthorized WebSocket call")
            return False
        return func(user_id, *args, **kwargs)
    return wrapper

    #     token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    #     print(token)
    #     if not token:
    #         print("Unauthorized")
    #         return False

    #     try:
    #         decoded_data = decode_token(token)
    #         user_id = decoded_data["sub"]
    #         return func(user_id, *args, **kwargs)
    #     except Exception as e:
    #         print(e)
    #         print("Unauthorized")
    #         return False
    # return wrapper