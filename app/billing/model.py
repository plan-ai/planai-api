from mongoengine import EmbeddedDocument,StringField
from app.openai.model import OpenAI

class Plan(EmbeddedDocument):
    plan_type = StringField(choices=["freeTier"])
    open_ai_api_integration = OpenAI()