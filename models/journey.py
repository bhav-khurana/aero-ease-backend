class Journey:
    def __init__(self, journeyID, flights, availableCount):
        self.journeyID = journeyID #the ID of the journey
        self.flights = flights #a list of (scheduleID, departureEpoch, departureDate)
        self.availableCount = availableCount #available seats (class, noOfSeats)