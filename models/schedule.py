class Schedule:
    def __init__(
        self,
        scheduleID,
        flightNo,
        aircraftType,
        aircraftTailNo,
        departureAirport,
        arrivalAirport,
        departureTime,
        arrivalTime,
        status,
        departureDates,
        departureDateTimes,
        departureEpochs,
        duration,
    ):
        self.scheduleID = scheduleID
        self.flightNo = flightNo
        self.aircraftType = aircraftType
        self.aircraftTailNo = aircraftTailNo
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.status = status
        self.departureDates = departureDates
        self.departureDateTimes = departureDateTimes
        self.departureEpochs = departureEpochs
        self.duration = duration
        
    def __repr__(self):
        return f"Schedule ID: {self.scheduleID}\nFlight No: {self.flightNo}\nAircraft Type: {self.aircraftType}\n" \
               f"Aircraft Tail No: {self.aircraftTailNo}\nDeparture Airport: {self.departureAirport}\n" \
               f"Arrival Airport: {self.arrivalAirport}\nDeparture Time: {self.departureTime}\n" \
               f"Arrival Time: {self.arrivalTime}\nStatus: {self.status}\nDeparture Dates: {self.departureDates}\n" \
               f"Departure DateTimes: {self.departureDateTimes}\nDeparture Epochs: {self.departureEpochs}\n" \
               f"Duration: {self.duration}\n\n"
