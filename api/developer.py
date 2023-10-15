from flask import make_response, jsonify
from models import Freelancer


def get_developers(resp: str, job_skills):
    isAuthorized, resp = validate_user(jwt_auth)
    if not isAuthorized:
        return resp
    try:
        freelancers = Freelancer.objects.all()
        freelancer_list = []
        for freelancer in freelancers:
            del freelancer["_id"]
            freelancer_list.append(freelancer)
        message = {"freelancers": freelancer_list}
        status_code = 200
    except Exception as err:
        message = {"message": "Freelancers could not be fetched", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)
