from mongoengine import Document, IntField, StringField, URLField
from mongoengine import (
    ReferenceField,
    BooleanField,
    EmbeddedDocumentListField,
    EmbeddedDocument,
)
from mongoengine import ListField, DateTimeField, EmailField


class JiraIntegration(Document):
    jira_token = StringField()


class Org(Document):
    org_name = StringField()
    org_github = URLField()
    org_jira = ReferenceField(JiraIntegration)


class Bountier(Document):
    user_github = StringField()
    user_name = StringField()
    user_email = ListField(EmailField())
    user_primary_email = EmailField()
    user_org = ReferenceField(Org)
    user_github_auth = StringField()
    bounty_jira_token = StringField()
    openai_token = StringField()  # might be none as well
    max_usage = IntField()
    timely_reminder = IntField()


class Skill(Document):
    skill_name = StringField()


class UserSkills(EmbeddedDocument):
    skill = ReferenceField(Skill)
    skill_stake = IntField()

    user_gh_token = StringField()


class Freelancer(Document):
    user_name = StringField()
    user_email = EmailField()
    user_github = URLField()
    user_linkedin = URLField()
    user_resume = URLField()
    user_other_sources = URLField()
    user_avg_rating = IntField()
    user_profile_pic = URLField()
    user_skills = EmbeddedDocumentListField(UserSkills)


class Bounty(Document):
    bounty_title = StringField()
    bounty_desc = StringField()
    bounty_stake = IntField()
    bounty_assigned = ReferenceField(
        Freelancer, default=None
    )  # might be none as well if not yet assigned
    bounty_creator = ReferenceField(Bountier)  # can not be none
    bounty_deadline = DateTimeField()
    bounty_required_skills = ListField(StringField)
    bounty_completed = BooleanField(default=False)  # true if bounty is completed
