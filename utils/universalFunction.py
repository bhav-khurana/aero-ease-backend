from journeyGeneration import (
    getActualJourneys,
    getAffectedPassengers,
)

from solutionGenerator import (
    solutionGenerator,
)

class Weights:
    def __init__(
        self,
        ssrWeights,
        cabinWeights,
        classWeights,
        connectingFlightsWeight,
        paidServicesWeight,
        bookingTypeWeight,
        noPAXWeight,
        loyaltyWeight,
        stopoverWeight,
        sameEquipmentWeight,
        cityPairWeights,
        departureDiffWeights,
        arrivalDiffWeights,
    ):
        self.ssrWeights = ssrWeights
        self.cabinWeights = cabinWeights
        self.classWeights = classWeights
        self.connectingFlightsWeight = connectingFlightsWeight
        self.paidServicesWeight = paidServicesWeight
        self.bookingTypeWeight = bookingTypeWeight
        self.noPAXWeight = noPAXWeight
        self.loyaltyWeight = loyaltyWeight
        self.stopoverWeight = stopoverWeight
        self.sameEquipmentWeight = sameEquipmentWeight
        self.cityPairWeights = cityPairWeights
        self.departureDiffWeights = departureDiffWeights
        self.arrivalDiffWeights = arrivalDiffWeights

def jsonToWeights(jsonData):
    ssrWeights = {item["type"]: item["value"] if item["enabled"] else 0 for item in jsonData["pnrRankingRules"]["ssr"]}
    cabinWeights = {item["cabin"]: item["value"] if item["enabled"] else 0 for item in jsonData["pnrRankingRules"]["cabin"]}
    classWeights = {item["class"]: item["value"] if item["enabled"] else 0 for item in jsonData["pnrRankingRules"]["class"]}
    connectingFlightsWeight = jsonData["pnrRankingRules"]["other"][0]["value"] if jsonData["pnrRankingRules"]["other"][0]["enabled"] else 0
    paidServicesWeight = jsonData["pnrRankingRules"]["other"][1]["value"] if jsonData["pnrRankingRules"]["other"][1]["enabled"] else 0
    bookingTypeWeight = jsonData["pnrRankingRules"]["other"][2]["value"] if jsonData["pnrRankingRules"]["other"][2]["enabled"] else 0
    noPAXWeight = jsonData["pnrRankingRules"]["other"][3]["value"] if jsonData["pnrRankingRules"]["other"][3]["enabled"] else 0
    loyaltyWeight = jsonData["pnrRankingRules"]["other"][4]["value"] if jsonData["pnrRankingRules"]["other"][4]["enabled"] else 0
    stopoverWeight = jsonData["flightRankingRules"]["general"][0]["score"] if jsonData["flightRankingRules"]["general"][0]["enabled"] else 0
    sameEquipmentWeight = jsonData["flightRankingRules"]["general"][1]["score"] if jsonData["flightRankingRules"]["general"][1]["enabled"] else 0
    departureDiffWeights = [item["score"] if item["enabled"] else 0 for item in jsonData["flightRankingRules"]["std"]]
    arrivalDiffWeights = [item["score"] if item["enabled"] else 0 for item in jsonData["flightRankingRules"]["arrivalDelay"]]
    cityPairWeights = {item["title"]: item["score"] if item["enabled"] else 0 for item in jsonData["flightRankingRules"]["cityPair"]}

    return Weights(
        ssrWeights,
        cabinWeights,
        classWeights,
        connectingFlightsWeight,
        paidServicesWeight,
        bookingTypeWeight,
        noPAXWeight,
        loyaltyWeight,
        stopoverWeight,
        sameEquipmentWeight,
        cityPairWeights,
        departureDiffWeights,
        arrivalDiffWeights,
    )

# Example usage
jsonData = {
  "flightRankingRules": {
    "arrivalDelay": [
      {
        "enabled": True,
        "score": 70,
        "difference": 6,
        "description": "Arrival delay is less than 6 hours."
      },
      {
        "enabled": True,
        "score": 50,
        "difference": 12,
        "description": "Arrival delay is less than 12 hours."
      },
      {
        "enabled": True,
        "score": 40,
        "difference": 24,
        "description": "Arrival delay is less than 24 hours."
      },
      {
        "enabled": True,
        "score": 30,
        "difference": 48,
        "description": "Arrival delay is less than 48 hours."
      }
    ],
    "cityPair": [
      { "enabled": True, "score": 40, "title": "Same city pair" },
      { "enabled": True, "score": 30, "title": "Different city pair but the same city" },
      { "enabled": True, "score": 20, "title": "Different cities" }
    ],
    "std": [
      { "enabled": True, "score": 70, "difference": 6, "description": "SPF is less than 6 hours." },
      {
        "enabled": True,
        "score": 50,
        "difference": 12,
        "description": "SPF is less than 12 hours."
      },
      {
        "enabled": True,
        "score": 40,
        "difference": 24,
        "description": "SPF is less than 24 hours."
      },
      {
        "enabled": True,
        "score": 30,
        "difference": 48,
        "description": "SPF is less than 48 hours."
      }
    ],
    "general": [
      {
        "enabled": True,
        "title": "Stopover",
        "score": -20,
        "description": "If the flight has a stopover, then this score will be deducted."
      },
      {
        "title": "Same Equipement",
        "enabled": True,
        "score": 50,
        "description": "Is the flight operated by the same equipment?"
      }
    ]
  },
  "pnrRankingRules": {
    "ssr": [
      { "type": "INFT", "enabled": True, "value": 433, "description": "Infant" },
      { "type": "WCHR", "enabled": True, "value": 200, "description": "Wheelchair, can walk" },
      {
        "type": "WCHS",
        "enabled": True,
        "value": 200,
        "description": "Wheelchair, can't climb stairs"
      },
      { "type": "WCHC", "enabled": True, "value": 200, "description": "Complete immobile" },
      { "type": "LANG", "enabled": True, "value": 200, "description": "Language restrictions" },
      { "type": "CHLD", "enabled": True, "value": 200, "description": "Child" },
      {
        "type": "MAAS",
        "enabled": True,
        "value": 200,
        "description": "Meet and assist - many reasons"
      },
      { "type": "UNMR", "enabled": True, "value": 200, "description": "Unaccompanied minor" },
      { "type": "BLND", "enabled": True, "value": 200, "description": "Blind" },
      { "type": "DEAF", "enabled": True, "value": 200, "description": "Deaf" },
      {
        "type": "EXST",
        "enabled": True,
        "value": 200,
        "description": "Large person taking up two seats"
      },
      { "type": "MEAL", "enabled": True, "value": 200, "description": "Meal request" },
      { "type": "NSST", "enabled": True, "value": 200, "description": "Seat information" },
      { "type": "NRPS", "enabled": True, "value": 200 }
    ],
    "cabin": [
      { "cabin": "F", "enabled": True, "value": 1500 },
      { "cabin": "J", "enabled": True, "value": 1500 },
      { "cabin": "Y", "enabled": True, "value": 1500 }
    ],
    "class": [
      { "class": "A", "enabled": True, "value": 800 },
      { "class": "C", "enabled": True, "value": 800 },
      { "class": "K", "enabled": True, "value": 800 }
    ],
    "other": [
      {
        "title": "Connection",
        "description": "If the flight is a connection, the priority is incremented by the 'value' times the number of downline connections.",
        "enabled": True,
        "value": 100
      },
      {
        "title": "Paid Service",
        "description": "If the flight is a paid service, the priority is incremented by the value.",
        "enabled": True,
        "value": 200
      },
      { "title": "Group Booking", "enabled": True, "value": 500 },
      {
        "title": "Loyality",
        "enabled": True,
        "value": 1700,
        "description": "If the passenger is a loyality member, the priority is incremented by the 'value'."
      },
      {
        "title": "Number of Passengers",
        "enabled": True,
        "value": 50,
        "description": "If the number of passengers is greater than 1, the priority is incremented by the 'value' times the number of passengers."
      }
    ]
  }
}

def printWeights(weights):
    print("SSR Weights:", weights.ssrWeights)
    print("Cabin Weights:", weights.cabinWeights)
    print("Class Weights:", weights.classWeights)
    print("Connecting Flights Weight:", weights.connectingFlightsWeight)
    print("Paid Services Weight:", weights.paidServicesWeight)
    print("Booking Type Weight:", weights.bookingTypeWeight)
    print("No PAX Weight:", weights.noPAXWeight)
    print("Loyalty Weight:", weights.loyaltyWeight)
    print("Stopover Weight:", weights.stopoverWeight)
    print("Same Equipment Weight:", weights.sameEquipmentWeight)
    print("City Pair Weights:", weights.cityPairWeights)
    print("Departure Diff Weights:", weights.departureDiffWeights)
    print("Arrival Diff Weights:", weights.arrivalDiffWeights)

# weightsInstance = jsonToWeights(jsonData)
# printWeights(weightsInstance)

def getCombinedAffectedPassengers(scheduleDatetimeTuples):
    combinedAffectedPassengers = []
    for scheduleID, datetime in scheduleDatetimeTuples:
        affectedPassengers = getAffectedPassengers(scheduleID, datetime)
        combinedAffectedPassengers.extend(affectedPassengers)
    return combinedAffectedPassengers

def getCombinedActualJourneys(scheduleDatetimeTuples):
    combinedActualJourneys = []
    for scheduleID, datetime in scheduleDatetimeTuples:
        actualJourneys = getActualJourneys(scheduleID, datetime)
        combinedActualJourneys.extend(actualJourneys)
    return combinedActualJourneys


def universalFunction(scheduleDatetimeTuples, jsonData):
    weights = jsonToWeights(jsonData)
    affectedPassengers = getCombinedAffectedPassengers(scheduleDatetimeTuples)
    actualJourneys = getCombinedActualJourneys(scheduleDatetimeTuples)

    solution = solutionGenerator(
        actualJourneys,
        affectedPassengers,
        weights,
    )

    return solution



