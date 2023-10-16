from flask import make_response, jsonify
from authentication import validate_user
import configparser
from langchain.llms import OpenAI

config = configparser.ConfigParser()
config.read("../config.ini")

model_name = config["openAI"]["model"]
temperature = 0.0


def anonymize_issue(jwt_auth: str, issue_desc: str):
    isAuthorized, resp = validate_user(jwt_auth)
    if not isAuthorized:
        return resp
    try:
        openai_api_key = resp.openai_token
        if openai_api_key is None:
            openai_api_key = config["openAI"]["apiKey"]
        model = OpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=openai_api_key,
        )
        prompt = f"""Take the following task and find a way to remove company specific information from it and create a freelance task that is anoymized:
                     {issue_desc}
        Send all output in form:
        
        projectTitle: 
        project:
        """
        message = {"anoymised_issue": model(prompt)}
        status_code = 200
    except Exception as err:
        message = {"message": "Error in anoymising issue", "reason": repr(err)}
        status_code = 400
    return make_response(jsonify(message), status_code)
