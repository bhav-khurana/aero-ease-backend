class Schedule:
    def __init__(self, scheduleID, flightNo, aircraftType, aircraftTailNo, departureAirport, arrivalAirport,
                 departureTime, arrivalTime, status, depatureDates,departureDateTimes, departureEpochs, duration):
        self.scheduleID = scheduleID
        self.flightNo = flightNo
        self.aircraftType = aircraftType
        self.aircraftTailNo = aircraftTailNo
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.status = status
        self.depatureDates = depatureDates
        self.departureDateTimes = departureDateTimes
        self.departureEpochs = departureEpochs
        self.duration = duration
