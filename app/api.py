import mongoengine
import configparser
from flask_restful import Api, Resource, request
from flask_cors import CORS
from flask import Flask, make_response, jsonify
from app.user.auth import create_user_github, update_token, login_user_github
from app.openai_config.add_key import put_openai_key
from app.openai_config.add_spending_limit import put_spending_limit
from app.openai_config.usage import get_openai_usage
from app.task.fetch import get_tasks, get_task_details
from app.task.anonymize import get_anonymized_task

config = configparser.ConfigParser()
config.read("config.ini")

mongoengine.connect(config["MONGODB"]["HOST"])

app = Flask(__name__)
api = Api(app)
cors = CORS(app)


class GithubSignup(Resource):
    def post(self):
        body = request.json
        return create_user_github(
            org_name=body["orgName"],
            user_uid=body["githubId"],
            user_token=body["ghAccessToken"],
        )


class UpdateToken(Resource):
    def get(self):
        return update_token(current_jwt=request.args.get("jwt"))


class UserGithubLogin(Resource):
    def post(self):
        body = request.json
        return login_user_github(
            github_uid=body["githubId"],
            gh_access_token=body["ghAccessToken"],
        )


class OpenAIKey(Resource):
    def put(self):
        return put_openai_key(
            auth=request.headers.get("Authorization"),
            openai_key=request.headers.get("openAIKey"),
        )


class OpenAISpendingLimit(Resource):
    def put(self):
        return put_spending_limit(
            auth=request.headers.get("Authorization"),
            spending_limit=float(request.headers.get("spendingLimit")),
        )


class OpenAIUsage(Resource):
    def get(self):
        return get_openai_usage(auth=request.headers.get("Authorization"))


class SanityCheck(Resource):
    def get(self):
        return make_response(jsonify({"message": "API is up!"}), 200)


class AddJiraAuth(Resource):
    def put(self):
        body = request.json
        return add_jira_integration(
            auth=request.headers.get("Authorization"),
            jira_token=body["jiraToken"],
            jira_id=body["jiraId"],
        )


class Task(Resource):
    def get(self):
        return get_tasks(auth=request.headers.get("Authorization"))


class TaskDetails(Resource):
    def get(self):
        return get_task_details(
            auth=request.headers.get("Authorization"),
            task_id=request.args.get("taskId"),
        )


class TaskAnoymization(Resource):
    def post(self):
        return get_anonymized_task(
            auth=request.headers.get("Authorization"),
            task_id=request.args.get("taskId"),
        )


api.add_resource(SanityCheck, "/")
api.add_resource(GithubSignup, "/user/signup/github")
api.add_resource(UpdateToken, "/user/jwt")
api.add_resource(UserGithubLogin, "/user/login/github")
api.add_resource(OpenAIKey, "/openai/key")
api.add_resource(OpenAISpendingLimit, "/openai/spending")
api.add_resource(AddJiraAuth, "/user/jira")
api.add_resource(Task, "/task")
api.add_resource(TaskDetails, "/task/detail")
api.add_resource(TaskAnoymization, "/task/anonymization")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
