import flask
from flask_restful import Resource
from flask import request
import os
import pandas as pd

absolutePath = os.path.dirname(__file__)
dataDirectory = "data"
passengerPNRFileName = "PNRP-ZZ-20231208_111136.csv"
passengerPNRFilePath = os.path.join(
    absolutePath, "..", dataDirectory, passengerPNRFileName
)

class PNRDetails(Resource):
    def get(self):
        args = request.args
        pnr = args.get("pnr")
        details = [] # list of passengers
        df = pd.read_csv(passengerPNRFilePath)
        for _, row in df.iterrows():
            if row['RECLOC'] == pnr:
                details.append({
                    "customerID": row['CUSTOMER_ID'],
                    "firstName": row['FIRST_NAME'],
                    "lastName": row['LAST_NAME'],
                    "email": row['CONTACT_EMAIL'],
                })
        response = flask.jsonify(details)
        return response