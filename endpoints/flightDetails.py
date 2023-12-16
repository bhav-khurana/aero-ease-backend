import flask
from flask_restful import Resource
from flask import jsonify, request
import os
import pandas as pd

absolutePath = os.path.dirname(__file__)
dataDirectory = "data"
scheduleFileName = "SCH-ZZ-20231208_035117.csv"
scheduleFilePath = os.path.join(
    absolutePath, "..", dataDirectory, scheduleFileName
)

df = pd.read_csv(scheduleFilePath)
class FlightDetails(Resource):
    def post(self):
        scheduleIDArr = request.json
        flight_details_dict = {}  # Use a dictionary to store details by scheduleID
        print(scheduleIDArr)
        for _, row in df.iterrows():
            if row['ScheduleID'] in scheduleIDArr:
                details = {
                    "flightNo": row['FlightNumber'],
                    "departureAirport": row['DepartureAirport'],
                    "arrivalAirport": row['ArrivalAirport'],
                    "departureTime": row['DepartureTime'],
                    "arrivalTime": row['ArrivalTime']
                }
                schedule_id = row['ScheduleID']
                flight_details_dict[schedule_id] = details
        print("Resp", flight_details_dict)
        response = jsonify(flight_details_dict)
        return response
