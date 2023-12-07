class SeatInventory:
    def __init__(self, inventoryID, scheduleID, flightNo, departureDate, arrivalDate,
                 departureAirport, arrivalAirport, totalAvailable, fcAvailable,
                 bcAvailable, pcAvailable, ecAvailable,
                 fc_cd, bc_cd, pc_cd, ec_cd):
        self.inventoryID = inventoryID
        self.scheduleID = scheduleID
        self.flightNo = flightNo
        self.departureDate = departureDate
        self.arrivalDate = arrivalDate
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport
        self.totalAvailable = totalAvailable
        self.fcAvailable = fcAvailable
        self.bcAvailable = bcAvailable
        self.pcAvailable = pcAvailable
        self.ecAvailable = ecAvailable
        self.fc_cd = fc_cd
        self.bc_cd = bc_cd
        self.pc_cd = pc_cd
        self.ec_cd = ec_cd