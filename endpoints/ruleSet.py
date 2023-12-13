import flask
import json
from flask_restful import Resource
from flask import request

class RuleSet(Resource):
    ruleset = {}
    def post(self):
        data = json.loads(request.data)
        RuleSet.ruleset = data
        response = flask.jsonify({"message": "ok"})
        return response