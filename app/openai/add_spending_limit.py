from app.user.model import User

def add_spending_limit(user:User, spending_limit: float) -> bool:
    openai_auth = user.user_org.org_open_ai
    if openai_auth.custom_token != True:
        return False
    openai_auth.spending_limit = org_open_ai
    try:
        user.save()
        return True
    except:
        return False

