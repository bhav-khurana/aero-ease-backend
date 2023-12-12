import os
import sys
import random
from dimod import BinaryQuadraticModel, Binary
from dwave.system import LeapHybridBQMSampler
import numpy as np
from datetime import datetime
import string

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
)
import journey, pnr

from journeyGeneration import (
    actualJourneys,
    affectedPassengers,
)

from loadSheetData import (
    scheduleDataObjects,
    bookingPNRDataObjects,
    seatAvailabilityDataObjects,
    passengerPNRDataObjects,
)

print("Actual journeys: ", actualJourneys)
print("Actual passengers: ", affectedPassengers)

upgradesAllowed = False
downgradesAllowed = False
originalScheduleID = "SCH-ZZ-0000030"
originalDepartureDate = datetime(2024, 8, 20)


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


# The way it's supposed to look:
ssrWeights = {
    "INFT": 200,
    "WCHR": 200,
    "WCHS": 200,
    "WCHC": 200,
    "LANG": 200,
    "CHLD": 200,
    "MAAS": 200,
    "UNMR": 200,
    "BLND": 200,
    "DEAF": 200,
    "EXST": 200,
    "MEAL": 200,
    "NSST": 200,
    "NRPS": 200,
    "ADT": 200,
    "CHD": 200,
    "INF": 200,
    "INS": 200,
    "UNN": 200,
    "S65": 200,
    "NRPS": 200,
    " NRSA": 200,
}
cabinWeights = {"fc": 1500, "bc": 1500, "pc": 1500, "ec": 1500,}
classWeights = {letter: 800 for letter in string.ascii_uppercase}
connectingFlightsWeight = 100
paidServicesWeight = 200
bookingTypeWeight = 500
noPAXWeight = 50
loyaltyWeight = 1700
departureDiffWeights = [70, 50, 40, 30]
arrivalDiffWeights = [70, 50, 40, 30]
cityPairWeights = {"SSP": 40, "DCPSC": 30, "DCP": 20}
stopoverWeight = -20
sameEquipmentWeight = 50

currentWeights = Weights(
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


def ssrCalculator(pnr, ssrWeights):
    sum = 0
    for i in range(len(pnr.ssr)):
        sum += ssrWeights[pnr.ssr[i]]
    return sum

def cabinAssigner(classData):
    classData = classData.upper()    
    cabin_mapping = {
        'A': 'fc', 'B': 'bc', 'C': 'pc', 'D': 'ec',
        'E': 'fc', 'F': 'bc', 'G': 'pc', 'H': 'ec',
        'I': 'fc', 'J': 'bc', 'K': 'pc', 'L': 'ec',
        'M': 'fc', 'N': 'bc', 'O': 'pc', 'P': 'ec',
        'Q': 'fc', 'R': 'bc', 'S': 'pc', 'T': 'ec',
        'U': 'fc', 'V': 'bc', 'W': 'pc', 'X': 'ec',
        'Y': 'fc', 'Z': 'bc',
    }
    return cabin_mapping.get(classData, 'Invalid classData')

def scheduleIDToEpochs(scheduleID, departureDate):
    print("scheduleID: ", scheduleID)
    print("departureDate: ", type(departureDate.date()))
    departureEpoch = 0
    arrivalEpoch = 0
    for schedule in scheduleDataObjects:
        if schedule.scheduleID == scheduleID:
            index = 0
            for i in range(len(schedule.departureEpochs)):
                if schedule.departureDateTimes[i].date() == departureDate.date():
                    print("oye match ho gya")
                    index = i
                    break
            departureEpoch = schedule.departureEpochs[index]
            arrivalEpoch = departureEpoch + schedule.duration
    return departureEpoch, arrivalEpoch


def coefficientCalculator(journey, pnr, weights):
    sum = 0
    sum += ssrCalculator(pnr, weights.ssrWeights)
    if upgradesAllowed and downgradesAllowed:
        sum += weights.cabinWeights[cabinAssigner(pnr.classData)]
    elif upgradesAllowed:
        # TODO: Add code for upgrades
        pass
    elif downgradesAllowed:
        # TODO: Add code for downgrades
        pass
    else:
        if journey.availableSeats[0] != cabinAssigner(pnr.classData):
            print("oye yahan pe aaya")
            sum -= 10000
        else:
            sum += weights.cabinWeights[cabinAssigner(pnr.classData)]
    sum += weights.classWeights[pnr.classData]
    sum += weights.connectingFlightsWeight * pnr.connectingFlights
    # sum += weights.paidServicesWeight * pnr.paidServices
    # sum += weights.bookingTypeWeight * pnr.bookingType
    sum += weights.noPAXWeight * pnr.noPAX
    # sum += weights.loyaltyWeight * pnr.loyalty
    if journey.availableSeats[1] < pnr.noPAX:
        print("abe yahan pe aaya")
        sum -= 10000
    if len(journey.flights) > 1:
        sum += weights.stopoverWeight * (len(journey.flights) - 1)
    # TODO: Add code for same equipment
    # TODO: Add code for city pair
    print("--------------------")
    overallDeparture, _ = scheduleIDToEpochs(
        journey.flights[0][0], journey.flights[0][2]
    )
    print("--------------------")
    _, overallArrival = scheduleIDToEpochs(
        journey.flights[-1][0], journey.flights[-1][2]
    )
    print("--------------------")
    originalDeparture, originalArrival = scheduleIDToEpochs(
        originalScheduleID, originalDepartureDate
    )
    print("--------------------")
    if overallDeparture < originalDeparture:
        print("overallDeparture: ", overallDeparture)
        print("originalDeparture: ", originalDeparture)
        print("yes yahan pe aaya")
        sum -= 10000
    elif overallDeparture - originalDeparture <= 6 * 3600:
        sum += departureDiffWeights[0]
    elif overallDeparture - originalDeparture <= 12 * 3600:
        sum += departureDiffWeights[1]
    elif overallDeparture - originalDeparture <= 24 * 3600:
        sum += departureDiffWeights[2]
    elif overallDeparture - originalDeparture <= 48 * 3600:
        sum += departureDiffWeights[3]
    else:
        print("yahan pe aaya")
        sum -= 10000
    if overallArrival - originalArrival <= 6 * 3600:
        sum += arrivalDiffWeights[0]
    elif overallArrival - originalArrival <= 12 * 3600:
        sum += arrivalDiffWeights[1]
    elif overallArrival - originalArrival <= 24 * 3600:
        sum += arrivalDiffWeights[2]
    elif overallArrival - originalArrival <= 48 * 3600:
        sum += arrivalDiffWeights[3]
    else:
        print("nhi yahan pe aaya")
        sum -= 10000
    return sum


def generateVariablesAndCoefficients(journeys, pnrs, weights):
    x = []
    c = []
    n = 0
    obj = BinaryQuadraticModel(vartype="BINARY")

    for i in range(len(pnrs)):
        for j in range(len(journeys)):
            x.append(Binary(f"x{i}_{j}"))
            c.append(0)
            c[n] = -coefficientCalculator(journeys[j], pnrs[i], weights)
            obj.add_variable(f"x{i}_{j}")
            obj.add_linear(f"x{i}_{j}", c[n])
            n += 1

    return obj, c


def addQuadraticConstraints(obj, journeys, pnrs):
    for i in range(len(pnrs)):
        for j in range(len(journeys)):
            for k in range(j + 1, len(journeys)):
                obj.set_quadratic(f"x{i}_{j}", f"x{i}_{k}", 10000)


def addLinearInequalityConstraints(obj, journeys, pnrs):
    for j in range(len(journeys)):
        terms = [(f"x{i}_{j}", 2 * pnrs[i].noPAX) for i in range(len(pnrs))]
        obj.add_linear_inequality_constraint(
            terms,
            lagrange_multiplier=1000,
            label=f"col_{j}",
            ub=2 * journeys[j].availableSeats[1],
        )


def solveFlightSchedule(obj):
    bqm_sampler = LeapHybridBQMSampler()
    bqm_answer = bqm_sampler.sample(obj)
    return bqm_answer


def solutionGenerator(journeys, pnrs, weights):
    obj, c = generateVariablesAndCoefficients(journeys, pnrs, weights)
    addQuadraticConstraints(obj, journeys, pnrs)
    addLinearInequalityConstraints(obj, journeys, pnrs)
    print(c)
    print(solveFlightSchedule(obj))


solutionGenerator(actualJourneys, affectedPassengers, currentWeights)
