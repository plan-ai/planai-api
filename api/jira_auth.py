from flask import make_response, jsonify
from authentication import validate_user


def add_jira(jwt_auth: str, jira_auth: str):
    isAuthorized, resp = validate_user(jwt_auth)
    if not isAuthorized:
        return resp
    try:
        resp.update(set__bounty_jira_token=jira_auth)
        message = {"message": "User updated sucessfully", "user": str(resp.id)}
        status_code = 200
    except Exception as err:
        message = {"message": "User could not be updated", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)
