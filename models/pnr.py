class PNR:
    def __init__ (self,recloc, ssr, cabinData , classData , downlineConnections , paidServices , bookingType , noPAX , loyalty):
        self.recloc = recloc
        self.ssr = ssr
        self.cabinData = cabinData
        self.classData = classData
        self.downlineConnections = downlineConnections
        self.paidServices = paidServices
        self.bookingType = bookingType #booked as a group
        self.noPAX = noPAX
        self.loyalty = loyalty
