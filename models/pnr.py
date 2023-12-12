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
    
    def __repr__(self):
        return (
            f"PNR(recloc={self.recloc}, ssr={self.ssr}, cabinData={self.cabinData}, "
            f"classData={self.classData}, connectingFlights={self.connectingFlights}, "
            f"paidServices={self.paidServices}, bookingType={self.bookingType}, "
            f"noPAX={self.noPAX}, loyalty={self.loyalty})    "
        )