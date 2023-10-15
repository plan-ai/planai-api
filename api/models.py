from mongoengine import Document, IntField, StringField, URLField
from mongoengine import (
    ReferenceField,
    BooleanField,
    EmbeddedDocumentListField,
    EmbeddedDocument,
)
from mongoengine import ListField, DateTimeField, EmailField, BinaryField


class JiraIntegration(Document):
    jira_token = StringField()


class Org(Document):
    org_name = StringField()
    org_github = URLField()
    org_jira = ReferenceField(JiraIntegration)


class Bountier(Document):
    user_name = StringField()
    user_email = EmailField()
    user_org = ReferenceField(Org)


class Skill(Document):
    skill_name = StringField()


class UserSkills(EmbeddedDocument):
    skill = ReferenceField(Skill)
    skill_stake = IntField()


class Freelancer(Document):
    user_name = StringField()
    user_email = EmailField()
    user_github = URLField()
    user_linkedin = URLField()
    user_resume = URLField()
    user_other_sources = URLField()
    user_skills = EmbeddedDocumentListField(UserSkills)
    user_password = BinaryField()


class Bounty(Document):
    bounty_title = StringField()
    bounty_description = StringField()
    bounty_stake = IntField()
    bounty_assigned = ReferenceField(
        Freelancer
    )  # might be none as well if not yet assigned
    bounty_creator = ReferenceField(Bountier)  # can not be none
    bounty_deadline = DateTimeField()
    bounty_required_skills = ListField(StringField)
    bounty_completed = BooleanField()  # true if bounty is completed
    user_password = BinaryField()
