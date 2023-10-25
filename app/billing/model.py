from mongoengine import StringField, IntField, Document


class Plan(Document):
    plan_type = StringField(choices=["freeTier"])
    plan_billing = IntField(default=0)  # plan charges per month
