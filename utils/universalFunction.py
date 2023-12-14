from utils.journeyGeneration import (
    getActualJourneys,
    getAffectedPassengers,
)

from utils.solutionGenerator import (
    solutionGenerator,
)
import os
import pandas as pd
from datetime import datetime

absolutePath = os.path.dirname(__file__)
dataDirectory = "data"
scheduleFileName = "SCH-ZZ-20231208_035117.csv"
scheduleFilePath = os.path.join(absolutePath, "..", dataDirectory, scheduleFileName)

class Weights:
    def __init__(
        self,
        ssrWeights,
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
    print(jsonData["pnrRankingRules"]["ssr"])
    ssrWeights = {item["type"]: item["value"] if item["enabled"] else 0 for item in jsonData["pnrRankingRules"]["ssr"]}
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

def printWeights(weights):
    print("SSR Weights:", weights.ssrWeights)
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
        actualJourneys = getActualJourneys(scheduleID, datetime, scheduleDatetimeTuples)
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



