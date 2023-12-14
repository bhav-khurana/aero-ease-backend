import flask
from flask_restful import Resource
from flask import request
import os
import pandas as pd

absolutePath = os.path.dirname(__file__)
dataDirectory = "data"
scheduleFileName = "SCH-ZZ-20231208_035117.csv"
scheduleFilePath = os.path.join(
    absolutePath, "..", dataDirectory, scheduleFileName
)

class FlightDetails(Resource):
    def get(self):
        args = request.args
        scheduleID = args.get("scheduleID")
        details = {} # {flightNo, departureAirport, arrivalAirport, departureTime, arrivalTime}
        df = pd.read_csv(scheduleFilePath)
        for _, row in df.iterrows():
            if row['ScheduleID'] == scheduleID:
                details = {
                    "flightNo": row['FlightNumber'],
                    "departureAirport": row['DepartureAirport'],
                    "arrivalAirport": row['ArrivalAirport'],
                    "departureTime": row['DepartureTime'],
                    "arrivalTime": row['ArrivalTime']
                }
                break
        response = flask.jsonify(details)
        return response