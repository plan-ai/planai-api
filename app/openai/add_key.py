from app.user.model import User

def add_openai_key(user:User, token:str) -> bool:
    openai_auth = user.user_org.org_open_ai
    openai_auth.custom_token = True
    openai_auth.token = token
    try:
        user.save()
        return True
    except:
        return False

