import pandas
import flask
import json
from flask_restful import Resource
from flask import request


class AvailableFlights(Resource):
    def get(self):
        excelDataFrame = pandas.read_csv(
            "./data/schedule.csv"
        )
        jsonData = json.loads(excelDataFrame.to_json(orient="records"))

        return flask.jsonify(jsonData)

    def delete(self):
        data = json.loads(request.data)
        print(data)
        # TODO: parse the data
        # TODO: generate solution from data
        response = flask.jsonify({"message": "ok"})
        return response
