from app.user.model import User
import mongoengine
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

mongoengine.connect(config["MONGODB"]["HOST"])

user = User.objects().first()
print(user.user_org.to_mongo().to_dict())