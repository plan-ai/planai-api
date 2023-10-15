from models import Bounty
from authentication import validate_user
from flask import make_response, jsonify
from task_annotation import annotate_task_skills


def get_bounties_by_user(jwt_auth: str):
    isAuthorized, resp = validate_user(jwt_auth)
    if not isAuthorized:
        return resp
    try:
        bounties = Bounty.objects(
            bounty_creator=resp
        ).all()  # gets all bounties by api requester
        bounty_list = []
        for bounty in bounties:
            bounty = bounty.to_mongo().to_dict()
            bounty_list.append(bounty)
        message = {
            "bounty_creator": resp.user_email,
            "bounty_creator_org": resp.user_org.org_name,
            "bounties": bounty_list,
        }
        status_code = 200
    except Exception as err:
        message = {"response": "Could not complete your request", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)


def annotate_task(jwt_auth: str, task_desc: str):
    isAuthorized, resp = validate_user(jwt_auth)
    if not isAuthorized:
        return resp
    try:
        message = {"parsed_skills": annotate_task_skills(task_desc)}
        status_code = 200
    except Exception as err:
        message = {"response": "Could not complete your request", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)


def add_bounty(
    jwt_auth: str,
    bounty_title: str,
    bounty_desc: str,
    bounty_stake: int,
    bounty_deadline,
    bounty_required_skills,
):
    isAuthorized, resp = validate_user(jwt_auth)
    if not isAuthorized:
        return resp
    try:
        bounty = Bounty(
            bounty_titl=bounty_title,
            bounty_desc=bount_desc,
            bounty_stake=bounty_stake,
            bounty_deadline=bounty_deadline,
            bounty_required_skills=bounty_required_skills,
        )
        bounty.save()
        message = {
            "message": "Bounty saved successfully",
            "bountyTitle": bounty_title,
            "bountyDesc": bount_desc,
            "bountyStake": bounty_stake,
            "bountyDeadline": bounty_deadline,
            "bountyRequiredSkiils": bounty_required_skills,
        }
        status_code = 200
    except Exception as err:
        message = {"message": "Bounty creation failed"}
        status_code = 400
    return make_response(jsonify(message), 400)
