class PNRBooking:
    def __init__(self, recloc, creationDate, departureKey, actionCode, classCode, segSeq,
                 paxCount, carrierCode, flightNo, originCode, destinationCode, departuredate,
                 departureDTML, arrivalDTML, departureDTMZ, arrivalDTMZ, depatureDTMZEpoch):
        self.recloc = recloc
        self.creationDate = creationDate
        self.departureKey = departureKey
        self.actionCode = actionCode
        self.classCode = classCode
        self.segSeq = segSeq
        self.paxCount = paxCount
        self.carrierCode = carrierCode
        self.flightNo = flightNo
        self.originCode = originCode
        self.destinationCode = destinationCode
        self.departuredate = departuredate
        self.departureDTML = departureDTML
        self.arrivalDTML = arrivalDTML
        self.departureDTMZ = departureDTMZ
        self.arrivalDTMZ = arrivalDTMZ
        self.departureDTMZEpoch = depatureDTMZEpoch