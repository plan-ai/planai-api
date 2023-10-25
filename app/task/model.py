from mongoengine import (
    Document,
    ReferenceField,
    StringField,
    BooleanField,
    IntField,
    EmbeddedDocument,
)
from app.user.model import User
from app.freelancer.model import Freelancer


class AnonymizedTask(EmbeddedDocument):
    anonymized_task_title = StringField()
    anonymized_task_desc = StringField()


class Task(Document):
    task_created_by = ReferenceField(User)
    task_title = StringField()
    task_desc = StringField()
    task_reward = (
        IntField()
    )  # this represents task reward without dividing by 10^(deimals), hence is an int
    task_assigned = BooleanField(default=False)
    task_assigned_to = ReferenceField(Freelancer, optional=True)
    task_anonymized = EmbeddedDocument(AnonymizedTask)
    task_completed = BooleanField()
