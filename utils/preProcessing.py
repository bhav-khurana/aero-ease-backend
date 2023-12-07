from collections import defaultdict
from datetime import datetime, timedelta
import calendar
from loadSheetData import scheduleDataObjects, bookingPNRDataObjects
import pandas as pd


def get_seconds(t):
  return (t.hour * 60 + t.minute) * 60 + t.second

# changing dates and times to epochs
# for schedule_file->
for schedule in scheduleDataObjects:
  date_list_string = schedule.departureDates[1:-1]
  date_list = date_list_string.split(',')
  datetime_obj_list = []
  for date_string in date_list:
    date_string = date_string.strip()
    if date_string != '':
      datetime_obj_list.append(datetime.strptime(date_string[1:-1], '%m/%d/%Y'))
  schedule.departureDateTimes = datetime_obj_list

for schedule in scheduleDataObjects:
  list_epoch_dates = []
  for dates in schedule.departureDateTimes:
    temp_datetime_obj = datetime.combine(dates,schedule.departureTime)
    tmp_epoch = calendar.timegm(temp_datetime_obj.timetuple())
    list_epoch_dates.append(tmp_epoch)
  schedule.departureEpochs = list_epoch_dates
  schedule.duration = ((get_seconds(schedule.arrivalTime)-get_seconds(schedule.departureTime) + 86400) % 86400)

#getting the data for passengers with cancelled flights
# cancelled_flights = schedule_file[schedule_file['Status'] == 'Cancelled']
cancelled_flights = []
for schedule in scheduleDataObjects:
  if schedule.status == 'Cancelled':
    cancelled_flights.append(schedule)

list_of_cancel_flightnum = []

for flight in cancelled_flights:
  list_of_cancel_flightnum.append(flight.flightNo)

for booking in bookingPNRDataObjects:
  booking.departureDTMZEpoch = calendar.timegm((booking.departureDTMZ).timetuple())

# filtering out the bookings that were cancelled
# TODO: Modify
# Returns a list of reclocs by comparing flight number and departure epochs
def get_affected_passengers(scheduleID,departureDate):
  bookings_cancelled = []
  cancelled_flight_dep_epoch = 0
  for flight in scheduleDataObjects:
      if flight.scheduleID == scheduleID:
        index = 0
        for i in range(len(flight.departureDateTimes)):
           if flight.departureDateTimes[i] == departureDate:
              index = i
              break
      cancelled_flight_dep_epoch = flight.departureEpochs[index]
  for booking in bookingPNRDataObjects:
     if booking.departureDTMZEpoch == cancelled_flight_dep_epoch:
        bookings_cancelled.append(booking.recloc)
  return bookings_cancelled


def get_possible_routes(dataset, k, x, start_airport, end_airport, start_datetime_epoch, max_end_datetime_epoch):
    def find_routes(route, current_airport, current_time):
        nonlocal result

        # Check if the current route exceeds the allowed time
        if current_time > max_end_datetime_epoch:
            return

        # Check if the current airport is the destination
        if current_airport == end_airport:
            result.append(route.copy())
            return

        # Find possible connecting flights
        possible_flights = [flight for flight in dataset if flight[1] == current_airport and flight[3] >= current_time]

        for i in range(min(k, len(possible_flights))):
            next_flight = possible_flights[i]
            next_departure_time = next_flight[3] + next_flight[4]  # Departure time + Duration

            # Check if the downtime at the current stop is within limits
            if next_departure_time - current_time <= x:
                find_routes(route + [next_flight[0]], next_flight[2], next_departure_time)

    result = []
    start_flights = [flight for flight in dataset if flight[1] == start_airport and flight[3] >= start_datetime_epoch]

    for start_flight in start_flights:
        find_routes([start_flight[0]], start_flight[2], start_flight[3] + start_flight[4])

    return result



dataset = []

for schedule in scheduleDataObjects:
    if schedule.status == 'Scheduled':
        for dep in row['DepartureEpoch']:
            dataset.append((row['ScheduleID'], row['DepartureAirport'], row['ArrivalAirport'], dep, row['Duration']))


# Example usage:
start_datetime = calendar.timegm(datetime(2023,12,14,0,0,0).timetuple())
start_airport = 'CNN'
end_airport = 'MAA'
result = get_possible_routes(dataset, k = 3, x = 30 * 3600, start_airport=start_airport, end_airport=end_airport, start_datetime_epoch=start_datetime, max_end_datetime_epoch = 100 * 3600 + start_datetime)
result

