from collections import defaultdict
from datetime import datetime, timedelta
import calendar
import Schedule from models


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
        find_routes([start_flight[0]], start_flight[2], start_flight[3] + start_flight[4])t

    return result



dataset = []

for index, row in Schedule.iterrows():
    if row['Status'] == 'Scheduled':
        for dep in row['DepartureEpoch']:
            dataset.append((row['ScheduleID'], row['DepartureAirport'], row['ArrivalAirport'], dep, row['Duration']))


# Example usage:
# Adjust the start_datetime accordingly
start_datetime = calendar.timegm(datetime(2023,12,14,0,0,0).timetuple())
start_airport = 'CNN'
end_airport = 'MAA'
result = get_possible_routes(dataset, k = 3, x = 30 * 3600, start_airport=start_airport, end_airport=end_airport, start_datetime_epoch=start_datetime, max_end_datetime_epoch = 100 * 3600 + start_datetime)
result

