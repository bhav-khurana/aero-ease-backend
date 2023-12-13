class PNRPassenger:
    def __init__(
        self,
        recloc,
        creationDate,
        customerID,
        lastName,
        firstName,
        nationality,
        contactNo,
        contact_email,
        docID,
        docType,
        specialNameCode1,
        specialNameCode2,
        ssr,
        loyalty,
    ):
        self.recloc = recloc
        self.creationDate = creationDate
        self.customerID = customerID
        self.lastName = lastName
        self.firstName = firstName
        self.nationality = nationality
        self.contactNo = contactNo
        self.contact_email = contact_email
        self.docID = docID
        self.docType = docType
        self.specialNameCode1 = specialNameCode1
        self.specialNameCode2 = specialNameCode2
        self.ssr = ssr
        self.loyalty = loyalty
