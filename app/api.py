import mongoengine
import configparser
from flask_restful import Api, Resource, request
from flask_cors import CORS
from flask import Flask
from app.user.auth import create_user_github, update_token, login_user_github

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


api.add_resource(GithubSignup, "/user/signup/github")
api.add_resource(UpdateToken, "/user/jwt")
api.add_resource(UserGithubLogin, "/user/login/github")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
