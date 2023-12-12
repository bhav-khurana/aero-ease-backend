import flask
import json
from flask_restful import Resource
from flask import request

class RuleSet(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)