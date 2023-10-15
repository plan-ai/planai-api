from flask import Flask, make_response, jsonify
from flask_restful import Api, Resource, request
from authentication import generate_jwt
from bounty import get_bounties_by_user, annotate_task, add_bounty
from estimation import estimate_time
from jira_auth import add_jira
from developer import get_developers
import mongoengine
from flask_cors import CORS

import configparser

config = configparser.ConfigParser()
config.read("../config.ini")

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

# connects to mongoengine
mongoengine.connect(config["app"]["database_name"])


class FetchJWT(Resource):
    def post(self):
        body = request.get_json()
        return generate_jwt(
            body.get("github_id"),
            body.get("firebase_uid"),
            body.get("user_gh_access_token"),
            body.get("pub_key"),
        )


class SanityCheck(Resource):
    def get(self):
        return make_response(jsonify({"Status": "API is reachable"}), 200)


class Bounty(Resource):
    def get(self):
        return get_bounties_by_user(
            request.headers.get("Authorization"),
        )

    def post(self):
        body = request.body.get_json()
        return add_bounty(
            request.headers.get("Authorization"),
            body.get("bounty_title"),
            body.get("bounty_desc"),
            body.get("bounty_stake"),
            body.get("bounty_deadline"),
            body.get("bounty_required_skills"),
        )


class AnnotateTask(Resource):
    def post(self):
        return annotate_task(
            request.headers.get("Authorization"), request.body.get("task_desc")
        )


class EstimateTime(Resource):
    def get(self):
        return estimate_time()


class AddJiraAuth(Resource):
    def post(self):
        return bounty_jira_token(
            request.headers.get("Authorization"), request.body.get("jira_token")
        )


class GetDeveloperForJob(Resource):
    def get(self):
        return get_developers(
            request.headers.get("Authorization"), request.body.get("task_skills")
        )


api.add_resource(FetchJWT, "/user/setup")
api.add_resource(SanityCheck, "/")
api.add_resource(Bounty, "/bounty")
api.add_resource(AnnotateTask, "/task/annotate")
api.add_resource(EstimateTime, "/task/time")
api.add_resource(AddJiraAuth, "/user/jira/auth")
api.add_resource(GetDeveloperForJob, "/job/qualified_candidates")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
