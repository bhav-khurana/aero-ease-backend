import pandas as pd
import os

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
