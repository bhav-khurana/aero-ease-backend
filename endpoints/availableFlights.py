import pandas
import flask
import json
from flask_restful import Resource
from flask import request


class AvailableFlights(Resource):
    def get(self):
        excelDataFrame = pandas.read_csv(
            "./data/SCH-ZZ-20231208_035117.csv"
        )
        jsonData = json.loads(excelDataFrame.to_json(orient="records"))

        return flask.jsonify(jsonData)

    def delete(self):
        data = json.loads(request.data)
        print(data)
        cancelledFlights = []
        for flight in data:
            cancelledFlights.append((flight["scheduleID"], flight["date"]))
        
        # TODO: call the main function    
        
        # TODO: generate solution from data
        response = flask.jsonify({"message": "ok"})
        return response
