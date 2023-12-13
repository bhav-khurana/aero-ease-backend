import pandas as pd
import os
import sys
from datetime import datetime
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
)
import pnrBooking, pnrPassenger, schedule, seatInventory

absolutePath = os.path.dirname(__file__)
dataDirectory = "data"

scheduleFileName = "SCH-ZZ-20231208_035117.csv"
bookingPNRFileName = "PNRB-ZZ-20231208_062017.csv"
passengerPNRFileName = "PNRP-ZZ-20231208_111136.csv"
seatAvailabilityFileName = "INV-ZZ-20231208_041852.csv"

scheduleFilePath = os.path.join(absolutePath, "..", dataDirectory, scheduleFileName)
bookingPNRFilePath = os.path.join(absolutePath, "..", dataDirectory, bookingPNRFileName)
passengerPNRFilePath = os.path.join(
    absolutePath, "..", dataDirectory, passengerPNRFileName
)
seatAvailabilityFilePath = os.path.join(
    absolutePath, "..", dataDirectory, seatAvailabilityFileName
)

scheduleData = pd.read_csv(scheduleFilePath)
bookingPNRData = pd.read_csv(bookingPNRFilePath)
passengerPNRData = pd.read_csv(passengerPNRFilePath)
seatAvailabilityData = pd.read_csv(seatAvailabilityFilePath)

scheduleDataObjects = []
for index, row in scheduleData.iterrows():
    scheduleDataObjects.append(
        schedule.Schedule(
            row["ScheduleID"],
            row["FlightNumber"],
            row["AircraftType"],
            row["AircraftTailNumber"],
            row["DepartureAirport"],
            row["ArrivalAirport"],
            datetime.strptime(str(row["DepartureTime"]), '%H:%M'),
            datetime.strptime(str(row["ArrivalTime"]), '%H:%M'),
            row["Status"],
            row["DepartureDates"],
            [],
            [],
            0,
        )
    )

bookingPNRDataObjects = []
for index, row in bookingPNRData.iterrows():
    bookingPNRDataObjects.append(
        pnrBooking.PNRBooking(
            row["RECLOC"],
            row["CREATION_DTZ"],
            row["DEP_KEY"],
            row["ACTION_CD"],
            row["COS_CD"], # FirstClass, etc.
            row["SEG_SEQ"],
            row["PAX_CNT"],
            row["CARRIER_CD"],
            row["FLT_NUM"],
            row["ORIG_CD"],
            row["DEST_CD"],
            row["DEP_DT"],
            row["DEP_DTML"],
            row["ARR_DTML"],
            row["DEP_DTMZ"],
            row["ARR_DTMZ"],
            0,
        )
    )

passengerPNRDataObjects = []
for index, row in passengerPNRData.iterrows():
    passengerPNRDataObjects.append(
        pnrPassenger.PNRPassenger(
            row["RECLOC"],
            row["CREATION_DTZ"],
            row["CUSTOMER_ID"],
            row["LAST_NAME"],
            row["FIRST_NAME"],
            row["NATIONALITY"],
            row["CONTACT_PH_NUM"],
            row["CONTACT_EMAIL"],
            row["DOC_ID"],
            row["DOC_TYPE"],
            row["SPECIAL_NAME_CD1"],
            row["SPECIAL_NAME_CD2"],
            row["SSR_CODE_CD1"],
            row["TierLevel"]
        )
    )

seatAvailabilityDataObjects = []
for index, row in seatAvailabilityData.iterrows():
    seatAvailabilityDataObjects.append(
        seatInventory.SeatInventory(
            row["InventoryId"],
            row["ScheduleId"],
            row["Dep_Key"],
            row["FlightNumber"],
            datetime.strptime(row["DepartureDate"], '%m/%d/%Y'),
            datetime.strptime(row["ArrivalDateTime"], '%Y-%m-%d %H:%M:%S'),
            row["DepartureAirport"],
            row["ArrivalAirport"],
            row["AvailableInventory"],
            row["FC_AvailableInventory"],
            row["BC_AvailableInventory"],
            row["PC_AvailableInventory"],
            row["EC_AvailableInventory"],
            row["FC_CD"],
            row["BC_CD"],
            row["PC_CD"],
            row["EC_CD"],
        )
    )
