from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from endpoints.availableFlights import AvailableFlights
from endpoints.ruleSet import RuleSet
from endpoints.pnrDetails import PNRDetails
from endpoints.flightDetails import FlightDetails

app = Flask(__name__)
CORS(app)
api = Api(app)


class Home(Resource):
    def get(self):
        return {"status": "The API is running and healthy!"}


api.add_resource(Home, "/")
api.add_resource(AvailableFlights, "/flights")
api.add_resource(RuleSet, "/ruleset")
api.add_resource(PNRDetails, "/pnrDetails")
api.add_resource(FlightDetails, "/flightDetails")

if __name__ == "__main__":
    app.run(debug=True)
