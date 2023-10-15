from flask import Flask, make_response, jsonify
from flask_restful import Api, Resource, request
from authentication import generate_jwt, add_openai_token
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
            body.get("githubId"),
            body.get("userGhAccessToken"),
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
        body = request.get_json()
        return add_bounty(
            request.headers.get("Authorization"),
            body.get("bountyTitle"),
            body.get("bountyDesc"),
            body.get("bountyStake"),
            body.get("bountyDeadline"),
            body.get("bountyRequiredSkills"),
        )


class AnnotateTask(Resource):
    def post(self):
        body = request.get_json()
        return annotate_task(
            request.headers.get("Authorization"), body.get("taskDesc")
        )


class EstimateTime(Resource):
    def get(self):
        return estimate_time()


class AddJiraAuth(Resource):
    def post(self):
        return add_jira(
            request.headers.get("Authorization"), request.get_json().get("jiraToken")
        )


class GetDeveloperForJob(Resource):
    def get(self):
        return get_developers(
            request.headers.get("Authorization"), request.headers.get("task_skills",[])
        )


class OpenAI(Resource):
    def post(self):
        body = request.get_json()
        return add_openai_token(
            request.headers.get("Authorization"),
            body.get("openaiKey"),
            body.get("maxUsage"),
            body.get("timelyReminder")
        )


api.add_resource(FetchJWT, "/user/setup")
api.add_resource(SanityCheck, "/")
api.add_resource(Bounty, "/bounty")
api.add_resource(AnnotateTask, "/task/annotate")
api.add_resource(EstimateTime, "/task/time")
api.add_resource(AddJiraAuth, "/user/jira/auth")
api.add_resource(GetDeveloperForJob, "/job/qualified_candidates")
api.add_resource(OpenAI, "/openai")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
