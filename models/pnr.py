class PNR:
    def __init__(
        self,
        recloc,
        ssr=None,
        cabinData=None,
        classData=None,
        connectingFlights=None,
        paidServices=None,
        bookingType=None,
        noPAX=None,
        loyalty=None,
    ):
        self.recloc = recloc
        self.ssr = ssr
        self.cabinData = cabinData
        self.classData = classData
        self.connectingFlights = connectingFlights
        self.paidServices = paidServices
        self.bookingType = bookingType  # Booked as a group etc.
        self.noPAX = noPAX
        self.loyalty = loyalty
