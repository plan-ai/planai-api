from app.user.model import User
from app.user.auth import validate_user
from flask import make_response, jsonify


def add_spending_limit(user: User, spending_limit: float) -> bool:
    org = user.user_org
    openai_auth = org.org_open_ai
    if openai_auth.custom_token != True:
        return False
    try:
        org.update(set__org_open_ai__spending_limit=spending_limit)
        return True
    except:
        return False


def put_spending_limit(auth: str, spending_limit: float):
    user = validate_user(auth)
    if user is None:
        return make_response({"message": "User validator failed"}, 401)
    try:
        if add_spending_limit(user, spending_limit) is True:
            return make_response(
                {
                    "message": "User spending limit update",
                    "user": str(user.id),
                    "spending_limit": spending_limit,
                },
                200,
            )
        else:
            return make_response({"messgae": "User spending limit update failed"}, 400)
    except Exception as err:
        return make_response({"message": "User spending limit update failed"}, 500)
