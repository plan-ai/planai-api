import mongoengine
import configparser
from flask_restful import Api, Resource, request
from flask_cors import CORS
from flask import Flask
from app.user.auth import create_user_github, update_token, login_user_github
from app.openai.add_key import put_openai_key
from app.openai.add_spending_limit import put_spending_limit
from app.openai.usage import get_openai_usage

config = configparser.ConfigParser()
config.read("config.ini")

mongoengine.connect(config["MONGODB"]["HOST"])

app = Flask(__name__)
api = Api(app)
cors = CORS(app)


class GithubSignup(Resource):
    def post(self):
        body = request.json()
        return create_user_github(
            org_name=body["orgName"],
            user_uid=body["githubId"],
            user_token=body["ghAccessToken"],
        )


class UpdateToken(Resource):
    def get(self):
        return update_token(current_jwt=request.args.get("jwt"))


class UserGithubLogin(Resource):
    def get(self):
        return login_user_github(
            github_uid=request.headers.get("githubId"),
            gh_access_token=request.headers.get("ghAccessToken"),
        )

class OpenAIKey(Resource):
    def put(self):
        return put_openai_key(
            auth = request.headers.get("Authorization"),
            openai_key = request.headers.get("openAIKey")
        )

class OpenAISpendingLimit(Resource):
    def put(self):
        return put_spending_limit(
            auth = request.headers.get("Authorization"),
            spending_limit = float(request.headers.get("spendingLimit"))
        )

class OpenAIUsage(Resource):
    def get(self):
        return get_openai_usage(auth = request.headers.get("Authorization"))

api.add_resource(GithubSignup, "/user/signup/github")
api.add_resource(UpdateToken, "/user/jwt")
api.add_resource(UserGithubLogin, "/user/login/github")
api.add_resource(OpenAIKey,"/openai/key")
api.add_resource(OpenAISpendingLimit,"/openai/spending")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
