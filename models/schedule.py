class Schedule:
    def __init__(self, scheduleID, carrierCode, flightNo, aircraftTailNo, departureAirport, arrivalAirport,
                 departureTime, arrivalTime, status, departure_dates):
        self.scheduleID = scheduleID
        self.carrierCode = carrierCode
        self.flightNo = flightNo
        self.aircraftTailNo = aircraftTailNo
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.status = status
        self.departure_dates = departure_dates