from mongoengine import StringField, EmbeddedDocument, BooleanField, FloatField

class OpenAI(EmbeddedDocument):
    custom_token = BooleanField(default = False)
    token = StringField(optional=True)  # will be none in case custom token is false
    spending_limit = FloatField(optional=True)  # may or may not be none