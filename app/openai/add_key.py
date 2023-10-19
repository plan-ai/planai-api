from app.user.model import User
from app.user.auth import validate_user
from flask import make_response, jsonify


def add_openai_key(user: User, token: str) -> bool:
    openai_auth = user.user_org.org_open_ai
    openai_auth.custom_token = True
    openai_auth.token = token
    try:
        user.save()
        return True
    except:
        return False


def put_spending_limit(auth: str, openai_key: float):
    user = validate_user(auth)
    if user is None:
        return make_response({"message": "User validator failed"}, 401)
    try:
        if add_openai_key(user, openai_key) is True:
            return make_response(
                {
                    "message": "User OpenAI key update",
                    "user": user._id,
                    "openai_key": openai_key,
                },
                200,
            )
        else:
            return make_response({"messgae": "User OpenAI key update failed"}, 400)
    except Exception as err:
        return make_response({"message": "User OpenAI key update failed"}, 500)
