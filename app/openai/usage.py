from app.user.auth import validate_user
from flask import make_response, jsonify


def get_openai_usage(auth: str):
    user = validate_user(auth)
    if user is None:
        return make_response({"message": "User validator failed"}, 401)
    try:
        openai_usage = user.user_org.org_open_ai.usage_history.to_mongo().to_dict()
        messgae = {"result": openai_usage}
        status_code = 200
    except Exception as err:
        message = {"message": "Error in fetching openai usage data"}
        status_code = 500
    return make_response(jsonify(message), status_code)
