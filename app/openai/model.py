from mongoengine import (
    StringField,
    EmbeddedDocument,
    BooleanField,
    FloatField,
    EmbeddedDocumentListField,
    IntField,
    DateTimeField,
    ReferenceField
)
import configparser

# reads confg file
config = configparser.ConfigParser()
config.read("../config.ini")

class UsageHistory(EmbeddedDocument):
    input_tokens = IntField()
    output_tokens = IntField()
    usage_time = DateTimeField()
    purpose = StringField()

class OpenAI(EmbeddedDocument):
    custom_token = BooleanField(default=False)
    token = StringField(default=config["OpenAI"]["TOKEN"].strip())  # will be none in case custom token is false
    spending_limit = FloatField(default=int(config["OpenAI"]["LIMIT"].strip()))  # may or may not be none
    current_spend = FloatField(default=0)
    usage_history = EmbeddedDocumentListField(UsageHistory,default=[])

