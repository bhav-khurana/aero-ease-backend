import os
import sys
import random
from dimod import BinaryQuadraticModel, Binary
from dwave.system import LeapHybridBQMSampler
import numpy as np

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
originalDepartureDate = "2024-08-20"



class weights:
    def __init__(self, ssrWeights, cabinWeights, classWeights, connectingFlightsWeight, paidServicesWeight, bookingTypeWeight, noPAXWeight, loyaltyWeight, stopoverWeight, sameEquipment, cityPairWeights, departureDiffWeights, arrivalDiffWeights):
        self.ssrWeights = ssrWeights
        self.cabinWeights = cabinWeights
        self.classWeights = classWeights
        self.connectingFlightsWeight = connectingFlightsWeight
        self.paidServicesWeight = paidServicesWeight
        self.bookingTypeWeight = bookingTypeWeight
        self.noPAXWeight = noPAXWeight
        self.loyaltyWeight = loyaltyWeight
        self.stopoverWeight = stopoverWeight
        self.sameEquipment = sameEquipment
        self.cityPairWeights = cityPairWeights
        self.departureDiffWeights = departureDiffWeights
        self.arrivalDiffWeights = arrivalDiffWeights


#The way it's supposed to look:
ssrWeights = {'ADT': 0, 'CHD': 0, 'INF': 0, 'INS': 0, 'UNN': 0, 'S65': 0, 'NRPS': 0, 'NRSA': 0, 'WCHR': 0, 'BLND': 0, 'DEAF': 0}
cabinWeights = {'Y': 0, 'J': 0, 'F': 0}
classWeights = {'A': 0, 'C': 0, 'K': 0}
cityPairWeights = {'SSP': 0, 'DCPSC': 0, 'DCP': 0}
departureDiffWeights = [70, 50, 40, 30]
arrivalDiffWeights = [70, 50, 40, 30]

def ssrCalculator(pnr, ssrWeights):
    sum = 0
    for i in range(len(pnr.ssr)):
        sum += ssrWeights[pnr.ssr[i]]
    return sum

def scheduleIDToEpochs(scheduleID, departureDate):
    departureEpoch = 0
    arrivalEpoch = 0
    #TODO: Add code for converting scheduleID to epochs
    return departureEpoch, arrivalEpoch


def coefficientCalculator(journey, pnr, weights):
    sum =0
    sum += ssrCalculator(pnr, weights.ssrWeights)
    if upgradesAllowed and downgradesAllowed:
        sum += weights.cabinWeights[pnr.cabinData]
    elif upgradesAllowed:
        #TODO: Add code for upgrades
        pass
    elif downgradesAllowed:
        #TODO: Add code for downgrades
        pass
    else:
        if journey.availableCount[0] != pnr.cabinData:
            sum -= 10000
        else:
            sum += weights.cabinWeights[pnr.cabinData]
    sum += weights.classWeights[pnr.classData]
    sum += weights.connectingFlightsWeight * pnr.connectingFlights
    sum += weights.paidServicesWeight * pnr.paidServices
    sum += weights.bookingTypeWeight * pnr.bookingType
    sum += weights.noPAXWeight * pnr.noPAX
    sum += weights.loyaltyWeight * pnr.loyalty
    if journey.availableCount[1] < pnr.noPAX:
        sum -= 10000
    if len(journey.flights) > 1:
        sum += weights.stopoverWeight * (len(journey.flights) - 1)
    #TODO: Add code for same equipment
    #TODO: Add code for city pair
    overallDeparture, _ = scheduleIDToEpochs(journey.flights[0].scheduleID ,journey.flights[0].departureDate)
    _, overallArrival = scheduleIDToEpochs(journey.flights[-1].scheduleID ,journey.flights[-1].departureDate)
    originalDeparture, originalArrival = scheduleIDToEpochs(originalScheduleID, originalDepartureDate)
    if overallDeparture < originalDeparture:
        sum -=10000
    elif overallDeparture - originalDeparture <= 6*3600:
        sum += departureDiffWeights[0]
    elif overallDeparture - originalDeparture <= 12*3600:
        sum += departureDiffWeights[1]
    elif overallDeparture - originalDeparture <= 24*3600:
        sum += departureDiffWeights[2]
    elif overallDeparture - originalDeparture <= 48*3600:
        sum += departureDiffWeights[3]
    else:
        sum -= 10000
    if overallArrival - originalArrival <= 6*3600:
        sum += arrivalDiffWeights[0]
    elif overallArrival - originalArrival <= 12*3600:
        sum += arrivalDiffWeights[1]
    elif overallArrival - originalArrival <= 24*3600:
        sum += arrivalDiffWeights[2]
    elif overallArrival - originalArrival <= 48*3600:
        sum += arrivalDiffWeights[3]
    else:
        sum -= 10000
    return sum

def generateVariablesAndCoefficients(journeys, pnrs):
    x=[]
    c=[]
    n=0
    obj = BinaryQuadraticModel(vartype='BINARY')

    for i in range(len(pnr)):
        for j in range(len(journey)):
            x.append(Binary(f'x{i}_{j}'))
            c.append(0)
            c[n] = -coefficientCalculator(journeys[j], pnrs[i], weights)
            obj.add_variable(f'x{i}_{j}')
            obj.add_linear(f'x{i}_{j}', c[n])
            n+=1
    
    return obj, c

def addQuadraticConstraints(obj, journeys, pnrs):
    for i in range(len(pnrs)):
        for j in range(len(journeys)):
            for k in range(j+1, len(journeys)):
                    obj.set_quadratic(f'x{i}_{j}', f'x{i}_{k}', 10000)

def addLinearInequalityConstraints(obj, journeys, pnrs):
    for j in range(len(journeys)):
        terms = [(f'x{i}_{j}', 2*pnrs[i].noPAX) for i in range(len(pnrs))]
        obj.add_linear_inequality_constraint(terms, lagrange_multiplier=1000, label=f'col_{j}', ub=2*journeys[j].availableCount[1])

def solveFlightSchedule(obj):
    bqm_sampler = LeapHybridBQMSampler()
    bqm_answer = bqm_sampler.sample(obj)
    return bqm_answer

def solutionGenerator(journeys, pnrs):
    obj, c = generateVariablesAndCoefficients(journeys, pnrs)
    addQuadraticConstraints(obj, journeys, pnrs)
    addLinearInequalityConstraints(obj, journeys, pnrs)
    print(c)
    print(solveFlightSchedule(obj))

solutionGenerator(actualJourneys, affectedPassengers)