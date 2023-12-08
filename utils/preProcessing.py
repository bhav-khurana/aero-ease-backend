import uuid
from collections import defaultdict
from datetime import datetime, timedelta
import calendar
from loadSheetData import scheduleDataObjects, bookingPNRDataObjects, seatAvailabilityDataObjects
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))
import journey


def getSeconds(t):
    return (t.hour * 60 + t.minute) * 60 + t.second

# Changing dates and times to epochs
# For schedule_file ->
for schedule in scheduleDataObjects:
    dateListString = schedule.departureDates[1:-1]
    dateList = dateListString.split(',')
    dateTimeObjList = []
    for dateString in dateList:
        dateString = dateString.strip()
        if dateString != '':
            dateTimeObjList.append(datetime.strptime(dateString[1:-1], '%m/%d/%Y'))
    schedule.departureDateTimes = dateTimeObjList

for schedule in scheduleDataObjects:
    listEpochDates = []
    for dates in schedule.departureDateTimes:
        tempDateTimeObj = datetime.combine(dates, schedule.departureTime)
        tmpEpoch = calendar.timegm(tempDateTimeObj.timetuple())
        listEpochDates.append(tmpEpoch)
    schedule.departureEpochs = listEpochDates
    schedule.duration = ((getSeconds(schedule.arrivalTime) - getSeconds(schedule.departureTime) + 86400) % 86400)

# Getting the data for passengers with cancelled flights
# cancelledFlights = schedule_file[schedule_file['Status'] == 'Cancelled']
cancelledFlights = []
for schedule in scheduleDataObjects:
    if schedule.status == 'Cancelled':
        cancelledFlights.append(schedule)

listOfCancelFlightNum = []

for flight in cancelledFlights:
    listOfCancelFlightNum.append(flight.flightNo)

for booking in bookingPNRDataObjects:
    booking.departureDTMZEpoch = calendar.timegm((booking.departureDTMZ).timetuple())

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
            bookingsCancelled.append(booking.recloc)
    return bookingsCancelled

class JourneyTemp:
    def __init__(self, journeyID, flights):
        self.journeyID = journeyID
        self.flights = flights

def getPossibleRoutes(dataset, maxConnectingFlights, maxDownTime, startAirport, endAirport, startDatetimeEpoch, maxEndDatetimeEpoch, minDownTime):
    def findRoutes(route, currentAirport, currentTime):
        nonlocal result

        # Check if the current route exceeds the allowed time
        if currentTime > maxEndDatetimeEpoch:
            return

        # Check if the current airport is the destination
        if currentAirport == endAirport:
            journey_id = str(uuid.uuid4())
            flights_info = [(flight[0], flight[3], flight[4]) for flight in route]  # Fix index to access departureDate
            result.append(JourneyTemp(journey_id, flights_info))
            return

        # Find possible connecting flights
        possibleFlights = [flight for flight in dataset if flight[1] == currentAirport and flight[3] >= currentTime]

        for i in range(min(maxConnectingFlights, len(possibleFlights))):
            nextFlight = possibleFlights[i]
            nextDepartureTime = nextFlight[3] + nextFlight[4]  # Departure time + Duration

            # Check if the downtime at the current stop is within limits
            if nextDepartureTime - currentTime <= maxDownTime and nextDepartureTime - currentTime >= minDownTime:
                findRoutes(route + [nextFlight], nextFlight[2], nextDepartureTime)

    result = []
    startFlights = [flight for flight in dataset if flight[1] == startAirport and flight[3] >= startDatetimeEpoch]

    for startFlight in startFlights:
        findRoutes([startFlight], startFlight[2], startFlight[3] + startFlight[4])

    return result



dataset = []

for schedule in scheduleDataObjects:
    if schedule.status == 'Scheduled':
        for dep in schedule.departureEpochs:
            dataset.append((schedule.scheduleID, schedule.departureAirport, schedule.arrivalAirport, dep, schedule.duration))


# Example usage:
startDatetime = calendar.timegm(datetime(2023, 12, 14, 0, 0, 0).timetuple())
startAirport = 'CNN'
endAirport = 'MAA'
result = getPossibleRoutes(dataset, maxConnectingFlights=3, maxDownTime=30 * 3600, startAirport=startAirport,
                            endAirport=endAirport, startDatetimeEpoch=startDatetime,
                            maxEndDatetimeEpoch=100 * 3600 + startDatetime, minDownTime=1*3600)

# Print the details of each Journey
for journeyInd in result:
    print(f"Journey ID: {journeyInd.journeyID}")
    print("Flights:")
    for flight in journeyInd.flights:
        print(f"  Schedule ID: {flight[0]}, Departure Epochs: {flight[1]}, Departure Date: {flight[2]}")
    print()

