#  NOTE: USING LOCAL DATETIME RIGHT NOW IN AUTH TO ALLOW
#  FOR FAST DEV AND MVP. THIS WILL FAIL IN CASE OF DISTRIBUTED SYSTEMS
#  PLEASE REFACTOR THIS CODE BEFORE PUSHING TO PROD
from datetime import datetime, timedelta
from app.user.model import User, Auth, Org
from app.billing.model import Plan
from app.openai.model import OpenAI
from flask import make_response, jsonify
import hashlib
import jwt
import configparser

# reads confg file
config = configparser.ConfigParser()
config.read("config.ini")

# set app defaults
secret_token = config["AUTH"]["SECRET"]
session_time = int(config["AUTH"]["EXPIRY"].strip())
# Create a new SHA-256 hash object
sha256_hash = hashlib.sha256()


def sha256(input: str):
    # Update the hash object with the bytes-like object
    sha256_hash.update(input.encode())

    # Get the hexadecimal representation of the hash
    return sha256_hash.hexdigest()


def create_user(
    user_name: str, user_email: str, user_auth_provider: Auth, user_org: Org
):
    user = User(
        user_name=user_name,
        user_email=user_email,
        user_auth_provider=user_auth_provider,
        user_org=user_org,
        user_created=datetime.now(),
    )
    try:
        user.save()
        return user
    except:
        return None


def create_org(org_name: str, user_email: str):
    org_domain = user_email.split("@")[1]
    free_plan = Plan.objects(plan_type="freeTier").first()
    if free_plan is None:
        return None
    openai = OpenAI(custom_token=False, token=None, spending_limit=None)
    org = Org(
        org_name=org_name,
        org_domain=org_domain,
        org_created=datetime.now(),
        org_plan=free_plan,
        org_open_ai=OpenAI,
    )
    try:
        org.save()
        return org
    except:
        return None


def create_auth(user_auth_provider: str, user_hashed_token: str, user_uid: str):
    auth = Auth(
        user_auth_provider=user_auth_provider,
        user_hashed_token=user_hashed_token,
        user_uid=user_uid,
    )
    try:
        auth.save()
        return auth
    except:
        return None


def encode_jwt(user_auth: Auth, secret_token: str):
    jwt_payload = {
        "hashedToken": user_auth.user_hashed_token,
        "authProvider": user_auth.user_auth_provider,
        "dateTime": datetime.now(),
    }
    jwt_token = jwt.encode(jwt_payload, secret_token, "HS256")
    return jwt_token


def validate_user(jwt_token: str):
    jwt_payload = jwt.decode(jwt_token, secret_token, ["HS256"])
    time_diff = datetime.now() - datetime.strptime(
        jwt_payload["dateTime"], "%Y-%m-%d %H:%M:%S"
    )
    user_auth = Auth(
        user_hashed_token=jwt_payload["hashedToken"],
        user_auth_provider=jwt_payload["authProvider"],
    )
    user = User.objects(user_auth=user_auth).first()
    if time_diff < session_time and user is not None:
        return user
    return None


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


def create_user_github(org_name: str, user_uid: str, user_token: str):
    try:
        (
            is_gh_valid,
            user_gh_name,
            user_gh_profile_pic,
            emails,
            primary_email,
        ) = verify_gh_access_token(user_uid, user_token)
        if not is_gh_valid:
            message = {"message": "Githb auth failed"}
            status_code = 422
            return make_response(jsonify(message), status_code)
        hashed_token = sha256(user_token)
        auth = create_auth("github", hashed_token, user_uid)
        if auth is None:
            message = {"message": "Githb auth object creation failed"}
            status_code = 400
            return make_response(jsonify(message), status_code)
        org = create_org(org_name, primary_email)
        if org is None:
            message = {"message": "Org object creation failed"}
            status_code = 400
            return make_response(jsonify(message), status_code)
        user = create_user(user_gh_name, primary_email, auth, org)
        if user is None:
            message = {"message": "User object creation failed"}
            status_code = 400
            return make_response(jsonify(message), status_code)
        jwt = encode_jwt(auth, secret_token)
        messgae = {"message": "User created sucessfully", "user": user._id, "jwt": jwt}
        status_code = 200
    except Exception as err:
        message = {"messgae": "User creation failed", "reason": repr(err)}
        status_code = 500
    return make_response(jsonify(message), status_code)


def login_user_github(github_uid: str, gh_access_token: str):
    try:
        hashed_token = sha256(gh_access_token)
        auth = Auth(
            user_auth_provider="github",
            user_hashed_token=hashed_token,
            user_uid=github_uid,
        )
        user = User.objects(user_auth_provider=auth).first()
        if user is None:
            return make_response({"message": "User validator failed"}, 401)
        message = {
            "jwt_token": encode_jwt(auth, secret_token),
            "user_name": user.user_name,
            "user_email": user.user_email,
            "user_profile_pic": user.user_profile_pic,
            "id": str(user._id),
        }
        status_code = 200
    except Exception as err:
        message = {
            "message": "User validation failed unexpectedly",
            "reason": repr(err),
        }
        status_code = 500
    return make_response(jsonify(message), status_code)


def update_token(current_jwt: str):
    try:
        user = validate_user(current_jwt)
        if user is None:
            return make_response({"message": "User validator failed"}, 401)
        message = {"updated_jwt": encode(user.user_auth_provider, secret_token)}
        status_code = 200
    except Exception as err:
        message = {"message": "JWT auth failed unexpectedly", "reason": repr(err)}
        status_code = 500
    return make_response(jsonify(message), status_code)
