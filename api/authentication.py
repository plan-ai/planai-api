import jwt
from models import Bountier
import requests
from flask import make_response, jsonify
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")


def parse_emails(emails_json):
    emails = []
    for email_json in emails_json:
        email = email_json["email"]
        if len(email.split("users.noreply.github.com")) == 1:
            emails.append(email)
            if email_json["primary"] == True:
                primary_email = email
    return emails, primary_email


def verify_gh_access_token(github_uid, gh_access_token):
    """
    Used as an internal helper function to validate if the
    github_uid and gh_acess_token sent into the function
    are of convergent origin and return the name and
    avatar url(github profile pic) if true
    """
    url = "https://api.github.com/user"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {gh_access_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(url, headers=headers).json()
    if int(github_uid) != response["id"]:
        return False, None, None, None, None
    email_response = requests.get(
        "https://api.github.com/user/emails", headers=headers
    ).json()
    try:
        emails, primary_email = parse_emails(email_response)
    except:
        emails, primary_email = None, None
    return True, response["name"], response["avatar_url"], emails, primary_email


def generate_jwt(github_uid, gh_access_token):
    """
    Used to generate a unique jwt token for a user
    to authenticate requests to the server from the
    user

    Parameters
    --------------------
    github_uid:string
                  Unique github user id of the user's github account
    firebase_uid:string
                    Unique firebase uid of the user
    gh_access_token:string
                       Github access token of the user
    pub_key:string
               User's pubblic key on the solana blockchain



    Returns
    --------------------
    auth_creds:
               Unique JWT token of the user that can be used to authenticate the user
    firebase:
             Unique firebase uid of the user
    """
    try:
        (
            is_gh_valid,
            user_gh_name,
            _,
            emails,
            primary_email,
        ) = verify_gh_access_token(github_uid, gh_access_token)
        if not is_gh_valid:
            raise Exception
        user = Bountier.objects(user_github=github_uid).first()
        if user is None:
            user = Bountier(
                user_github=github_uid,
                user_name=user_gh_name,
                user_github_auth=gh_access_token,
                user_email=emails,
                user_primary_email=primary_email,
            )
            user.save()
        else:
            if user.user_email is None or user.user_primary_email is None:
                user.update(
                    set__user_email=emails, set__user_primary_email=primary_email
                )
        token = jwt.encode(
            {"github": github_uid, "gh_token": gh_access_token},
            config["jwt"]["secretToken"],
            "HS256",
        )
        message = {"auth_creds": token}
        status_code = 200
    except Exception as err:
        message = {"error": "JWTFetchFailed", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)


def validate_user(token):
    unauthorizedResponse = make_response(
        jsonify({"message": "Invalid or Expired User token"}), 401
    )
    try:
        jwt_data = jwt.decode(token, config["jwt"]["secretToken"], ["HS256"])
        github_uid = jwt_data["github"]
        gh_access_token = jwt_data["gh_token"]
        (
            is_gh_valid,
            _,
            _,
            _,
            _,
        ) = verify_gh_access_token(github_uid, gh_access_token)
        user = Bountier.objects(user_github=github_uid).first()
        if user is not None and is_gh_valid:
            return True, user
        return False, unauthorizedResponse
    except Exception:
        return False, unauthorizedResponse
