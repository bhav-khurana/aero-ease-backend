class Journey:
    def __init__(self, journeyID, flights, availableCount):
        self.journeyID = journeyID  # ID of the journey
        self.flights = flights  # List of (scheduleID, departureEpoch, departureDate)
        self.availableCount = availableCount  # Available seats (class, noOfSeats)

    def __repr__(self):
        flights_repr = ", ".join(
            f"({scheduleID}, {departureEpoch}, {departureDate})"
            for scheduleID, departureEpoch, departureDate in self.flights
        )
        return (
            f"Journey(journeyID={self.journeyID}, flights=[{flights_repr}], "
            f"availableCount={self.availableCount})"
        )
