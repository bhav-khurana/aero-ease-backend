from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from endpoints.availableFlights import AvailableFlights

app = Flask(__name__)
CORS(app)
api = Api(app)


class Home(Resource):
    def get(self):
        return {"status": "The API is running and healthy!"}


api.add_resource(Home, "/")
api.add_resource(AvailableFlights, "/flights")

if __name__ == "__main__":
    app.run(debug=True)
