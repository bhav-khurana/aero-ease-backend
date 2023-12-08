class Journey:
    def __init__(self, journeyID, flights, availableCount):
        self.journeyID = journeyID  # ID of the journey
        self.flights = flights  # List of (scheduleID, departureEpoch, departureDate)
        self.availableCount = availableCount  # Available seats (class, noOfSeats)
