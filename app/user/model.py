from mongoengine import Document, StringField
from mongoengine import EmbeddedDocument, DateTimeField, ReferenceField
from mongoengine import EmailField, URLField
from app.billing.model import Plan
from app.openai.model import OpenAI


class Auth(EmbeddedDocument):
    user_auth_provider = StringField(choices=["github", "gogle"])
    user_hashed_token = StringField()
    user_uid = StringField()


class Org(Document):
    org_name = StringField()
    org_domain = StringField()
    org_created = DateTimeField()
    org_plan = ReferenceField(Plan)
    org_open_ai = OpenAI()


class User(Document):
    user_name = StringField()
    user_email = EmailField()
    user_auth_provider = Auth()
    user_org = ReferenceField(Org)
    user_created = DateTimeField()
    user_profile_pic = URLField()
