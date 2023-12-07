import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))
import pnrBooking, pnrPassenger, schedule, seatInventory

absolutePath = os.path.dirname(__file__)
dataDirectory = 'data'

scheduleFileName = 'schedule.xlsx'
bookingPNRFileName = 'bookingPNR.xlsx'
passengerPNRFileName = 'passengerPNR.xlsx'
seatAvailabilityFileName = 'seatAvailability.xlsx'

scheduleFilePath = os.path.join(absolutePath, '..', dataDirectory, scheduleFileName)
bookingPNRFilePath = os.path.join(absolutePath, '..', dataDirectory, bookingPNRFileName)
passengerPNRFilePath = os.path.join(absolutePath, '..', dataDirectory, passengerPNRFileName)
seatAvailabilityFilePath = os.path.join(absolutePath, '..', dataDirectory, seatAvailabilityFileName)

scheduleData = pd.read_excel(scheduleFilePath)
bookingPNRData = pd.read_excel(bookingPNRFilePath)
passengerPNRData = pd.read_excel(passengerPNRFilePath)
seatAvailabilityData = pd.read_excel(seatAvailabilityFilePath)

scheduleDataObjects = []
for index, row in scheduleData.iterrows():
    scheduleDataObjects.append(schedule.Schedule(row['ScheduleID'], row['FlightNumber'], row['AircraftType'], row['AircraftTailNumber'], row['DepartureAirport'], row['ArrivalAirport'], row['DepartureTime'], row['ArrivalTime'], row['Status'], row['DepartureDates']))

# bookingPNRDataObjects = []
# for index, row in bookingPNRData.iterrows():
#     bookingPNRDataObjects.append({ pnrBooking.PNRBooking(**row.to_dict()) })

# passengerPNRDataObjects = []
# for index, row in passengerPNRData.iterrows():
#     passengerPNRDataObjects.append({ pnrPassenger.PNRPassenger(**row.to_dict()) })

# seatAvailabilityDataObjects = []
# for index, row in seatAvailabilityData.iterrows():
#     seatAvailabilityDataObjects.append({ seatInventory.SeatInventory(**row.to_dict()) })

print(scheduleDataObjects)
