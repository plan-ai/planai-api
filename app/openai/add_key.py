from app.user.model import User
from app.user.auth import validate_user
from flask import make_response, jsonify


def add_openai_key(user: User, token: str) -> bool:
    org = user.user_org
    try:
        org.update(set__org_open_ai__custom_token=True, set__org_open_ai__token=token)
        return True
    except Exception as err:
        print(repr(err))
        return False


def put_openai_key(auth: str, openai_key: str):
    user = validate_user(auth)
    if user is None:
        return make_response({"message": "User validator failed"}, 401)
    try:
        if add_openai_key(user, openai_key) is True:
            return make_response(
                {
                    "message": "User OpenAI key updated",
                    "user": str(user.id),
                    "openai_key": openai_key,
                },
                200,
            )
        else:
            return make_response({"messgae": "User OpenAI key update failed"}, 400)
    except Exception as err:
        return make_response({"message": "User OpenAI key update failed"}, 500)
