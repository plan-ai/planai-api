from app.billing.model import Plan
import mongoengine
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")

mongoengine.connect(config["MONGODB"]["HOST"])
# creating default free plan
free_plan = Plan(plan_type="freeTier", plan_billing=0)

free_plan.save()
