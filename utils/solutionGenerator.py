import os
import sys
from dimod import BinaryQuadraticModel, Binary, ConstrainedQuadraticModel
from dwave.system import LeapHybridCQMSampler

num_of_solutions = 5
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
)
from utils.loadSheetData import (
    scheduleDataObjects,
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
classWeights = {"FirstClass": 1500, "BusinessClass": 1500, "PremiumEconomyClass": 1500, "EconomyClass": 1500,}
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
        try:
            sum += ssrWeights[pnr.ssr[i]]
        except:
            print("Invalid SSR", pnr.ssr[i])
    return sum

def cabinAssigner(classData):
    cabin_mapping = {
        'FirstClass': 'fc',
        'BusinessClass': 'bc',
        'PremiumEconomyClass': 'pc',
        'EconomyClass': 'ec',
    }
    return cabin_mapping.get(classData, 'Invalid classData')

def scheduleIDToEpochs(scheduleID, departureDate):
    departureEpoch = 0
    arrivalEpoch = 0
    for schedule in scheduleDataObjects:
        if schedule.scheduleID == scheduleID:
            index = 0
            for i in range(len(schedule.departureEpochs)):
                if schedule.departureDateTimes[i].date() == departureDate.date():
                    index = i
                    break
            departureEpoch = schedule.departureEpochs[index]
            arrivalEpoch = departureEpoch + schedule.duration
    return departureEpoch, arrivalEpoch

def scheduleIDToAirportsAndAircraft(scheduleID, departureDate):
    departureAirport = ""
    arrivalAirport = ""
    aircraft = ""
    for schedule in scheduleDataObjects:
        if schedule.scheduleID == scheduleID:
            departureAirport = schedule.departureAirport
            arrivalAirport = schedule.arrivalAirport
            aircraft = schedule.aircraftTailNo
    return departureAirport, arrivalAirport, aircraft

def classRankAssigner(classData):
    rankMapping = {
        'fc': 1,
        'bc': 2,
        'pc': 3,
        'ec': 4,
    }
    return rankMapping.get(classData, 'Invalid classData')

def loyaltyMapper(loyalty):
    loyalty_mapping = {
        'Silver': 1,
        'Gold': 2,
        'Platinum': 3,
        'nan': 0,
    }
    return loyalty_mapping.get(loyalty, 'Invalid loyalty')

def coefficientCalculator(journey, pnr, weights, upgradesAllowed, downgradesAllowed):
    sum = 0
    journeyDepartureAirport, _, _ = scheduleIDToAirportsAndAircraft(journey.flights[0][0], journey.flights[0][2])
    _, journeyArrivalAirport, _ = scheduleIDToAirportsAndAircraft(journey.flights[-1][0], journey.flights[-1][2])
    originalDepartureAirport, originalArrivalAirport, originalAircraft = scheduleIDToAirportsAndAircraft(pnr.originalScheduleID, pnr.originalDepartureDate)
    if journeyDepartureAirport != originalDepartureAirport or journeyArrivalAirport != originalArrivalAirport:
        sum -= 10000
    sum += ssrCalculator(pnr, weights.ssrWeights)
    if upgradesAllowed and downgradesAllowed:
        sum += weights.classWeights[pnr.classData]
    elif upgradesAllowed:
        if classRankAssigner(journey.availableSeats[0]) <= classRankAssigner(cabinAssigner(pnr.classData)):
            sum += weights.classWeights[pnr.classData]
        else:
            sum -= 10000
    elif downgradesAllowed:
        if classRankAssigner(journey.availableSeats[0]) >= classRankAssigner(cabinAssigner(pnr.classData)):
            sum += weights.classWeights[pnr.classData]
        else:
            sum -= 10000
    else:
        if journey.availableSeats[0] != cabinAssigner(pnr.classData):
            sum -= 10000
        else:
            sum += weights.classWeights[pnr.classData]
    sum += weights.connectingFlightsWeight * pnr.connectingFlights
    sum += weights.noPAXWeight * pnr.noPAX
    loyaltyScore = 0
    for loyalty in pnr.loyalty:
        try:
            loyaltyScore = max(weights.loyaltyWeight * loyaltyMapper(loyalty), loyaltyScore)
        except:
            print("Invalid loyalty", loyalty)
    sum += loyaltyScore
    if journey.availableSeats[1] < pnr.noPAX:
        sum -= 10000
    if len(journey.flights) > 1:
        sum += weights.stopoverWeight * (len(journey.flights) - 1)
    
    overallDeparture, _ = scheduleIDToEpochs(
        journey.flights[0][0], journey.flights[0][2]
    )
    _, overallArrival = scheduleIDToEpochs(
        journey.flights[-1][0], journey.flights[-1][2]
    )
    originalDeparture, originalArrival = scheduleIDToEpochs(
        pnr.originalScheduleID, pnr.originalDepartureDate
    )
    if overallDeparture < originalDeparture:
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
        sum -= 10000
    _, _, journeyAircraft = scheduleIDToAirportsAndAircraft(journey.flights[0][0], journey.flights[0][2])
    if originalAircraft == journeyAircraft:
        sum += weights.sameEquipmentWeight
    return sum


def generateVariablesAndCoefficients(journeys, pnrs, weights, upgradesAllowed, downgradesAllowed):
    x = []
    c = []
    n = 0
    obj = BinaryQuadraticModel(vartype="BINARY")

    for i in range(len(pnrs)):
        for j in range(len(journeys)):
            x.append(Binary(f"x{i}_{j}"))
            c.append(0)
            c[n] = -(coefficientCalculator(journeys[j], pnrs[i], weights, upgradesAllowed, downgradesAllowed)/1000)*3
            obj.add_variable(f"x{i}_{j}")
            obj.add_linear(f"x{i}_{j}", c[n])
            n += 1

    return obj, c


def addQuadraticConstraints(obj, journeys, pnrs):
    for i in range(len(pnrs)):
        for j in range(len(journeys)):
            for k in range(j + 1, len(journeys)):
                obj.set_quadratic(f"x{i}_{j}", f"x{i}_{k}", 100)


def addLinearInequalityConstraints(obj, journeys, pnrs):
    for j in range(len(journeys)):
        terms = [(f"x{i}_{j}", pnrs[i].noPAX) for i in range(len(pnrs))]
        obj.add_linear_inequality_constraint(
            terms,
            lagrange_multiplier = 10,
            label = f"col_{j}",
            ub = journeys[j].availableSeats[1],
        )
        print(journeys[j].availableSeats[0], journeys[j].availableSeats[1])


def solveFlightSchedule(obj):
    cqm = ConstrainedQuadraticModel()
    cqm.set_objective(obj)
    cqmSampler = LeapHybridCQMSampler()
    cqmAnswer = cqmSampler.sample_cqm(cqm)
    solutionsList = cqmAnswer.samples(n = num_of_solutions, sorted_by = 'energy')
    return solutionsList


def solutionGenerator(journeys, pnrs, weights, upgradesAllowed, downgradesAllowed):
    obj, c = generateVariablesAndCoefficients(journeys, pnrs, weights, upgradesAllowed, downgradesAllowed)
    print("coefficients: ", c)
    addQuadraticConstraints(obj, journeys, pnrs)
    addLinearInequalityConstraints(obj, journeys, pnrs)
     # list of all solutions
    solutions = solveFlightSchedule(obj)
    passengerFlights = [] # list of key: passenger PNR, value: Journey(id, flights, availableSeats)
    for num in range(num_of_solutions):
        passengerFlights.append({"solution_no": num + 1})
        for i in range(len(pnrs)):
            passengerFlights[num][pnrs[i].recloc] = None
            for j in range(len(journeys)):
                if solutions[num][f"x{i}_{j}"] == 1:
                    passengerFlights[num][pnrs[i].recloc] = journeys[j].to_dict()
                    break

    return passengerFlights
