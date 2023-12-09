import uuid
from datetime import datetime
import calendar
import sys, os
from dateutil import parser
from loadSheetData import (
    scheduleDataObjects,
    bookingPNRDataObjects,
    seatAvailabilityDataObjects,
    passengerPNRDataObjects,
)

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
)
import journey, pnr


def getSeconds(t):
    return (t.hour * 60 + t.minute) * 60 + t.second


# Changing dates and times to epochs
# For schedule_file ->
for schedule in scheduleDataObjects:
    dateListString = schedule.departureDates[1:-1]
    dateList = dateListString.split(", ")
    dateTimeObjList = []
    for dateString in dateList:
        dateString = dateString.strip()
        if dateString != "":
            dateTimeObjList.append(datetime.strptime(dateString[1:-1], "%m/%d/%Y"))
    schedule.departureDateTimes = dateTimeObjList

for schedule in scheduleDataObjects:
    listEpochDates = []
    for dates in schedule.departureDateTimes:
        timestamp = calendar.timegm(schedule.departureTime.timetuple())
        tempDateTimeObj = datetime.combine(
            dates, datetime.fromtimestamp(timestamp).time()
        )
        tmpEpoch = calendar.timegm(tempDateTimeObj.timetuple())
        listEpochDates.append(tmpEpoch)
    schedule.departureEpochs = listEpochDates
    schedule.duration = (
        getSeconds(schedule.arrivalTime) - getSeconds(schedule.departureTime) + 86400
    ) % 86400

# Getting the data for passengers with cancelled flights
cancelledFlights = []
for schedule in scheduleDataObjects:
    if schedule.status == "Cancelled":
        cancelledFlights.append(schedule)

listOfCancelFlightNum = []

for flight in cancelledFlights:
    listOfCancelFlightNum.append(flight.flightNo)

for booking in bookingPNRDataObjects:
    parsedTime = parser.parse(booking.departureDTMZ)
    booking.departureDTMZEpoch = parsedTime.timestamp()


# Filtering out the bookings that were cancelled
# Returns a list of reclocs by comparing flight number and departure epochs
def getAffectedPassengers(scheduleID, departureDate):
    bookingsCancelled = []
    cancelledFlightDepEpoch = 0
    for flight in scheduleDataObjects:
        if flight.scheduleID == scheduleID:
            index = 0
            for i in range(len(flight.departureDateTimes)):
                if flight.departureDateTimes[i] == departureDate:
                    index = i
                    break
            cancelledFlightDepEpoch = flight.departureEpochs[index]
    for booking in bookingPNRDataObjects:
        if booking.departureDTMZEpoch == cancelledFlightDepEpoch:
            bookingsCancelled.append(booking)

    reclocsCancelled = []
    for booking in bookingsCancelled:
        reclocsCancelled.append(booking.recloc)

    pnrObjects = []
    for recloc in reclocsCancelled:
        pnrObjects.append(pnr.PNR(recloc))
        ssr = []
        for passenger in passengerPNRDataObjects:
            if passenger.recloc == recloc:
                ssr = (
                    str(passenger.specialNameCode1)[1:-1].split(",")
                    + str(passenger.specialNameCode2)[1:-1].split(",")
                    + str(passenger.ssr)[1:-1].split(",")
                )
                break
        pnrObjects[-1].ssr = ssr

    for booking in bookingsCancelled:
        for pnrObject in pnrObjects:
            if pnrObject.recloc == booking.recloc:
                pnrObject.noPAX = booking.paxCount
                pnrObject.classData = booking.classCode
                break

    for recloc in reclocsCancelled:
        connections = 0
        curr = 0
        for booking in bookingsCancelled:
            if booking.recloc == recloc:
                curr = booking.departureDTMZEpoch
                break

        bookingPNRDataObjects.sort(key=lambda x: x.departureDTMZEpoch)
        for booking in bookingPNRDataObjects:
            if booking.recloc == recloc:
                if (
                    booking.departureDTMZEpoch > curr
                    and booking.departureDTMZEpoch - curr < 3600 * 24
                ):
                    connections += 1
                    curr = booking.departureDTMZEpoch

        for pnrObject in pnrObjects:
            if pnrObject.recloc == recloc:
                pnrObject.connectingFlights = connections
                break

    return pnrObjects


class JourneyTemp:
    def __init__(self, journeyID, flights):
        self.journeyID = journeyID
        self.flights = flights

    def __repr__(self):
        flights_repr = ", ".join(
            f"({scheduleID}, {departureEpoch}, {departureDate})"
            for scheduleID, departureEpoch, departureDate in self.flights
        )
        return f"JourneyTemp(journeyID={self.journeyID}, flights=[{flights_repr}])"


# function to get alternate routes/flights
def getPossibleRoutes(
    dataset,
    maxConnectingFlights,
    maxDownTime,
    startAirport,
    endAirport,
    startDatetimeEpoch,
    maxEndDatetimeEpoch,
    minDownTime,
):
    def findRoutes(route, currentAirport, currentTime):
        nonlocal result

        # Check if the current route exceeds the allowed time
        if currentTime > maxEndDatetimeEpoch:
            return

        # Check if the current airport is the destination
        if currentAirport == endAirport:
            journey_id = str(uuid.uuid4())
            flights_info = [
                (flight[0], flight[3], flight[4]) for flight in route
            ]  # Fix index to access departureDate
            result.append(JourneyTemp(journey_id, flights_info))
            return

        # Find possible connecting flights
        possibleFlights = [
            flight
            for flight in dataset
            if flight[1] == currentAirport and flight[3] >= currentTime
        ]

        for i in range(min(maxConnectingFlights, len(possibleFlights))):
            nextFlight = possibleFlights[i]
            nextDepartureTime = (
                nextFlight[3] + nextFlight[4]
            )  # Departure time + Duration

            # Check if the downtime at the current stop is within limits
            if (
                nextDepartureTime - currentTime <= maxDownTime
                and nextDepartureTime - currentTime >= minDownTime
            ):
                findRoutes(route + [nextFlight], nextFlight[2], nextDepartureTime)

    result = []
    startFlights = [
        flight
        for flight in dataset
        if flight[1] == startAirport and flight[3] >= startDatetimeEpoch
    ]

    for startFlight in startFlights:
        findRoutes([startFlight], startFlight[2], startFlight[3] + startFlight[4])

    return result


# Creating a dataset for the getPossibleRoutes function
dataset = []
for schedule in scheduleDataObjects:
    if schedule.status == "Scheduled":
        for dep in schedule.departureEpochs:
            dataset.append(
                (
                    schedule.scheduleID,
                    schedule.departureAirport,
                    schedule.arrivalAirport,
                    dep,
                    schedule.duration,
                )
            )

# Example usage:
startDatetime = calendar.timegm(datetime(2023, 12, 10, 0, 0, 0).timetuple())
startAirport = "COK"
endAirport = "BOM"
possibleRoutes = getPossibleRoutes(
    dataset,
    maxConnectingFlights=4,
    maxDownTime=24 * 3600,
    startAirport=startAirport,
    endAirport=endAirport,
    startDatetimeEpoch=startDatetime,
    maxEndDatetimeEpoch=100 * 3600 + startDatetime,
    minDownTime=1 * 3600,
)


# Function to get actual journeys from the possible routes
# Returns a list of Journey objects (journeyID, flights, availableSeats)
def getActualJourneys(possibleRoutes):
    # Function to get available seats for a particular flight
    def getAvailableSeats(scheduleID, departureDate):
        seatsAvailable = []
        for seat in seatAvailabilityDataObjects:
            if seat.scheduleID == scheduleID and seat.departureDate == departureDate:
                seatsAvailable = [
                    ("fc", seat.fcAvailable),
                    ("bc", seat.bcAvailable),
                    ("pc", seat.pcAvailable),
                    ("ec", seat.ecAvailable),
                ]
        return seatsAvailable

    # list of actual journey objects (journeyID, flights, availableSeats)
    actualJourneys = []
    for tempJourney in possibleRoutes:
        fcSeats = []
        bcSeats = []
        pcSeats = []
        ecSeats = []

        for flight in tempJourney.flights:
            seatsAvailable = getAvailableSeats(flight[0], flight[2])
            fcSeats.append(seatsAvailable[0][1])
            bcSeats.append(seatsAvailable[1][1])
            pcSeats.append(seatsAvailable[2][1])
            ecSeats.append(seatsAvailable[3][1])

        minFCSeats = min(fcSeats)
        minBCSeats = min(bcSeats)
        minPCSeats = min(pcSeats)
        minECSeats = min(ecSeats)

        actualJourneys.append(
            journey.Journey(
                tempJourney.journeyID, tempJourney.flights, ("fc", minFCSeats)
            )
        )
        actualJourneys.append(
            journey.Journey(
                tempJourney.journeyID, tempJourney.flights, ("bc", minBCSeats)
            )
        )
        actualJourneys.append(
            journey.Journey(
                tempJourney.journeyID, tempJourney.flights, ("pc", minPCSeats)
            )
        )
        actualJourneys.append(
            journey.Journey(
                tempJourney.journeyID, tempJourney.flights, ("ec", minECSeats)
            )
        )

    return actualJourneys


print("possibleRoutes:", possibleRoutes)

actualJourneys = getActualJourneys(possibleRoutes)
for journey in actualJourneys:
    print(journey.journeyID, journey.flights, journey.availableSeats)
