from mongoengine import Document, StringField, EmailField, URLField


class Freelancer(Document):
    user_name = StringField()
    user_email = EmailField()
    user_addr = StringField()
    user_github = URLField()
    user_linkedin = URLField()
    user_resume = URLField()
    user_additional_metadata = URLField(optional=True)
