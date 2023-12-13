import uuid
from datetime import datetime
import numpy as np
import sys, os
from dateutil import parser
from utils.loadSheetData import (
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
import calendar
from datetime import datetime

# Iterate over each schedule in scheduleDataObjects
for schedule in scheduleDataObjects:
    # Extract departure dates as strings and split them into a list
    dateListString = schedule.departureDates[1:-1]
    dateList = dateListString.split(", ")
    dateTimeObjList = []

    # Convert each date string to a datetime object and add to the list
    for dateString in dateList:
        dateString = dateString.strip()
        if dateString != "":
            dateTimeObjList.append(datetime.strptime(dateString[1:-1], "%m/%d/%Y"))

    # Assume schedule.departureTime is a time object associated with the schedule
    # You may need to adjust this based on your actual data structure
    schedule.departureDateTimes = dateTimeObjList

for schedule in scheduleDataObjects:
    listEpochDates = []

    for dt in schedule.departureDateTimes:
        schedule_datetime = datetime.combine(dt.date(), schedule.departureTime.time())

        tmpEpoch = int(schedule_datetime.timestamp())
        listEpochDates.append(tmpEpoch)

    schedule.departureEpochs = listEpochDates
    schedule.duration = (
        getSeconds(schedule.arrivalTime) - getSeconds(schedule.departureTime) + 86400
    ) % 86400

nan = float("nan")
# Getting the data for passengers with cancelled flights
for booking in bookingPNRDataObjects:
    departure_string = booking.departureDTML
    parsedTime = datetime.strptime(departure_string, "%m/%d/%Y %H:%M")
    booking.departureDTMLEpoch = int(parsedTime.timestamp())

# Filtering out the bookings that were cancelled
# Returns a list of reclocs by comparing flight number and departure epochs
def getAffectedPassengers(scheduleID, departureDate):
    bookingsCancelled = []
    flightNo = 0
    cancelledFlightDepEpoch = 0
    for flight in scheduleDataObjects:
        if flight.scheduleID == scheduleID:
            flightNo = flight.flightNo
            index = 0
            for i in range(len(flight.departureDateTimes)):
                if flight.departureDateTimes[i] == departureDate:
                    index = i
                    break
            cancelledFlightDepEpoch = flight.departureEpochs[index]
            break
    for booking in bookingPNRDataObjects:
        if (
            booking.flightNo == flightNo
            and booking.departureDTMLEpoch == cancelledFlightDepEpoch
        ):
            bookingsCancelled.append(booking)

    reclocsCancelled = []
    for booking in bookingsCancelled:
        reclocsCancelled.append(booking.recloc)

    pnrObjects = []
    for recloc in reclocsCancelled:
        pnrObjects.append(pnr.PNR(recloc))
        ssr = set()
        loyalities = []
        for passenger in passengerPNRDataObjects:
            if passenger.recloc == recloc:
                if passenger.ssr != None and passenger.ssr != nan:
                    ssr.add(passenger.ssr)
                if passenger.specialNameCode1 != None and passenger.specialNameCode1 != nan:
                    ssr.add(passenger.specialNameCode1)
                if passenger.specialNameCode2 != None and passenger.specialNameCode2 != nan:
                    ssr.add(passenger.specialNameCode2)
                if passenger.loyalty != None and passenger.loyalty != nan:
                    loyalities.append(passenger.loyalty)

        ssr = list(ssr)
        pnrObjects[-1].ssr = ssr
        pnrObjects[-1].loyalty = loyalities

    for booking in bookingsCancelled:
        for pnrObject in pnrObjects:
            if pnrObject.recloc == booking.recloc:
                pnrObject.noPAX = booking.paxCount
                pnrObject.classData = booking.classCode
                pnrObject.originalScheduleID = scheduleID
                pnrObject.originalDepartureDate = departureDate
                break

    bookingPNRDataObjects.sort(key=lambda x: x.departureDTMLEpoch)
    for recloc in reclocsCancelled:
        connections = 0
        curr = 0
        for booking in bookingsCancelled:
            if booking.recloc == recloc:
                curr = booking.departureDTMLEpoch
                break

        for booking in bookingPNRDataObjects:
            if booking.recloc == recloc:
                if (
                    booking.departureDTMLEpoch > curr
                    and booking.departureDTMLEpoch - curr < 3600 * 24
                ):
                    connections += 1
                    curr = booking.departureDTMLEpoch

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
        return f"JourneyTemp(journeyID={self.journeyID}, flights=[{flights_repr}])\n"

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
                (flight[0], flight[3], datetime.utcfromtimestamp(flight[3] + 19800))
                for flight in route
            ] # 19800 is the offset for IST
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


def getPossibleRoutesUsingScheduleIDAndDepDate(scheduleID, departureDate):
    dataset = []
    startAirport = ""
    endAirport = ""
    startDatetime = 0
    for schedule in scheduleDataObjects:
        if schedule.status == "Scheduled":
            for i in range(len(schedule.departureEpochs)):
                dataset.append(
                    (
                        schedule.scheduleID,
                        schedule.departureAirport,
                        schedule.arrivalAirport,
                        schedule.departureEpochs[i],
                        schedule.duration,
                    )
                )
                if (
                    schedule.scheduleID == scheduleID
                    and schedule.departureDateTimes[i] == departureDate
                ):
                    startAirport = schedule.departureAirport
                    endAirport = schedule.arrivalAirport
                    startDatetime = schedule.departureEpochs[i]
                    
    possibleRoutes = getPossibleRoutes(
        dataset,
        maxConnectingFlights = 3,
        maxDownTime = 24 * 3600,
        startAirport = startAirport,
        endAirport = endAirport,
        startDatetimeEpoch = startDatetime,
        maxEndDatetimeEpoch = 48 * 3600 + startDatetime,
        minDownTime = 1 * 3600,
    )
    return possibleRoutes


# Function to get actual journeys from the possible routes
# Returns a list of Journey objects (journeyID, flights, availableSeats)
def getJourneys(possibleRoutes):
    # Function to get available seats for a particular flight
    def getAvailableSeats(scheduleID, departureDate):
        seatsAvailable = []
        for seat in seatAvailabilityDataObjects:
            if (
                scheduleID == seat.scheduleID
                and departureDate.date() == seat.departureDate.date()
            ):
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


def getActualJourneys(scheduleID, departureDate):
    possibleRoutes = getPossibleRoutesUsingScheduleIDAndDepDate(
        scheduleID, departureDate
    )
    actualJourneys = getJourneys(possibleRoutes)
    return actualJourneys

