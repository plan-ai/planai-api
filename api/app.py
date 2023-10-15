from flask import Flask, make_response, jsonify
from flask_restful import Api, Resource, request
import mongoengine
from flask_cors import CORS

import configparser

config = configparser.ConfigParser()
config.read("../config.ini")

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

#connects to mongoengine
mongoengine.connect(config["database_name"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)