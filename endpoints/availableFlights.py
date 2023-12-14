import pandas
import flask
import json
from flask_restful import Resource
from flask import request
from endpoints.ruleSet import RuleSet
from utils.universalFunction import universalFunction
from datetime import datetime

class AvailableFlights(Resource):
    def get(self):
        excelDataFrame = pandas.read_csv(
            "./data/SCH-ZZ-20231208_035117.csv"
        )
        jsonData = json.loads(excelDataFrame.to_json(orient="records"))

        return flask.jsonify(jsonData)

    def delete(self):
        data = json.loads(request.data)
        cancelledFlights = []
        for flight in data:
            cancelledFlights.append((flight["scheduleID"], datetime.strptime(flight["date"], "%m/%d/%Y")))
          
        print("ruleSet: ", RuleSet.ruleset)
        solution = universalFunction(cancelledFlights, json.loads(RuleSet.ruleset))
        
        # generate solution from data
        response = flask.jsonify(solution)
        return response
