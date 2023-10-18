from mongoengine import StringField, IntField, Document


class Plan(Document):
    plan_type = StringField(choices=["freeTier"])
    plan_billing = IntField()  # plan charges per month
