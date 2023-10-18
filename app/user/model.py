from mongoengine import Document, StringField
from mongoengine import EmbeddedDocument, DateTimeField, ReferenceField
from mongoengine import EmailField
from app.billing.model import Plan
from app.openai.model import OpenAI

class Auth(EmbeddedDocument):
    user_auth_provider = StringField(choices=["google","github"])
    user_hashed_token = StringField()

class Org(Document):
    org_name = StringField()
    org_email = EmailField()  # might be same as user_email in some cases
    org_created = DateTimeField()
    org_plan = ReferenceField(Plan)
    org_open_ai = OpenAI()

class User(Document):
    user_name = StringField()
    user_email = EmailField()
    user_auth_provider = Auth()
    user_org = ReferenceField(Org)
    user_created = DateTimeField()
