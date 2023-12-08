class PNR:
    def __init__ (self,recloc, ssr, cabinData , classData , connectingFlights , paidServices , bookingType , noPAX , loyalty):
        self.recloc = recloc
        self.ssr = ssr
        self.cabinData = cabinData
        self.classData = classData
        self.connectingFlights = connectingFlights
        self.paidServices = paidServices
        self.bookingType = bookingType #booked as a group etc
        self.noPAX = noPAX
        self.loyalty = loyalty
