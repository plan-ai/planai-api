from mongoengine import StringField, EmbeddedDocument, BooleanField

class OpenAI(EmbeddedDocument):
    custom_token = BooleanField(default = False)
    token = StringField()  # will be none in case custom token is false