from random import choices, seed, randint, random, choice
from string import ascii_uppercase, digits
from sys import argv

airports = ["MAA","BLR", "BOM", "DUB", "VNS", "JFK", "DEL", "LAX"]
departure_dates = "['08/19/2024', '08/20/2024', '08/21/2024', '08/22/2024', '08/23/2024', '08/24/2024', '08/25/2024' ]"
names_all = ["Hello", "Bye" , "Good" , "Cool" , "Apple", "Ball"]
time = ['14:00','16:00','18:00', '20:00']

def get_airport_codes():
    pass

def get_pnr():
    return ''.join(choices(ascii_uppercase+digits, k=6))

def get_flight(length):
    arr = []
    last = randint(0,7)
    for i in range(length):
        if random()  <= 0.5:
            while((Next := randint(0,7)) == last):
                continue
            arr.append((last, Next))
            last = Next
        else:
            arr.append((-1,-1))
    return arr


def get_people(number):
    names = []
    for i in range(number):
        names.append(choices(names_all,k=2))
    return names


def get_schedule_id(start,end,i):
    return "SCH-ZZ-0000"+str(i*8*8+start*8+end).zfill(3)

def get_inventory_id(start,end,i,day):
    return "INV-ZZ-"+str(day*196 + i*64 + start*8 + end).zfill(7)


def main(samples=25):
    people = [] 
    pnr = []  	
    flight = []	

    for i in range(samples):
        pnr.append(get_pnr())
        people.append(get_people(randint(1,3)))
        flight.append(get_flight(randint(1,3)))

    with open("people-out.csv", "w") as f:
        f.write("RECLOC,LAST_NAME,FIRST_NAME\n")
        for i in range(samples):
            for first, last in people[i]:
                f.write("{},{},{}\n".format(pnr[i],first,last))

    with open("schedule-out.csv","w") as f:
        f.write("ScheduleID,FlightNumber,DepartureAirport,ArrivalAirport,DepartureTime,ArrivalTime,DepartureDates\n")
        for start in range(8):
            for end in range(8):
                if start == end: continue
                for i in range(3):
                    if start == -1: continue
                    f.write("{},{},{},{},{},{},{}\n".format(
                    get_schedule_id(start,end,i),
                    1000+(start*8+end),
                    airports[start],
                    airports[end],
                    time[i],
                    time[(i+1)],
                    departure_dates))
    with open('pnr-out.csv','w') as f:
        f.write("RECLOC,ACTION_CD,COS_CD,SEG_SEQ,PAX_CNT,FLT_NUM,ORIG_CD,DEST_CD,DEP_DT,DEP_DTMZ\n")
        for passenger_number in range(samples):
            counter = 1
            date_offset = randint(0,5)
            time_counter = -1
            for start,end in flight[passenger_number]:
                time_counter += 1
                if start == -1: continue
                f.write("{},HK,{},{},{},{},{},{},{},{}\n".format(
                    pnr[passenger_number],
                    choice(ascii_uppercase),
                    counter,
                    len(people[passenger_number]),
                    (1000+start*8+end),
                    airports[start],
                    airports[end],
                    time[time_counter],
                    "08/{}/2024".format(19+date_offset)
                    ))
                counter += 1
    with open('seating-out.csv','w') as f:
        f.write("InventoryId,ScheduleId,FlightNumber,AircraftType,DepartureDate,ArrivalDate,DepartureAirport,ArrivalAirport,TotalCapacity,"
                "TotalInventory,BookedInventory,Oversold,AvailableInventory,FirstClass,BusinessClass,PremiumEconomyClass,EconomyClass,"
                "FC_TotalInventory,FC_BookedInventory,FC_AvailableInventory, BC_TotalInventory,BC_BookedInventory,BC_AvailableInventory,"
                "PC_TotalInventory,PC_BookedInventory,PC_AvailableInventory, EC_TotalInventory,EC_BookedInventory,EC_AvailableInventory,"
                "FC_CD,BC_CD,PC_CD,EC_CD\n")
        for day in range(6):
            for start in range(8):
                for end in range(8):
                    if start == end : continue
                    for t in range(3):
                        fc = randint(10,27)
                        bc = randint(20,54)
                        pc = randint(35,81)
                        ec = randint(40,108)
                        fc_inv = randint(1,5)
                        bc_inv = randint(1,7)
                        pc_inv = randint(1,10)
                        ec_inv = randint(1,20)
                        f.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                            get_inventory_id(start,end,t,day),
                            get_schedule_id(start,end,t),
                            (1000+start*8+end),
                            "Boeing 787",
                            (f"08/%d/2024"%(19+day)),
                            (f"08/%d/2024"%(19+day)),
                            airports[start],
                            airports[end],
                            270,
                            270 + fc_inv + bc_inv + pc_inv + ec_inv,
                            fc + bc + pc + ec,
                            fc + bc + pc + ec - 270,
                            270 - fc - bc - pc - ec + fc_inv + bc_inv + pc_inv + ec_inv,
                            27,
                            54,
                            81,
                            108,
                            27+fc_inv,
                            fc,
                            27+fc_inv - fc,
                            54+bc_inv,
                            bc,
                            54+bc_inv - bc,
                            81+pc_inv,
                            pc,
                            81+pc_inv - pc,
                            108+ec_inv,
                            ec,
                            108+ec_inv - ec,
                            "\"{'F': 16, 'P': 11}\"",
                            "\"{'C': 22, 'J': 16, 'Z': 16}\"",
                            "\"{'Q': 24, 'R': 16, 'S': 8, 'T': 8, 'H': 16, 'M': 8}\"",
                            "\"{'Y': 8, 'A': 8, 'B': 4, 'D': 4, 'E': 4, 'G': 8, 'I': 4, 'K': 8, 'L': 4, 'N': 4, 'O': 4, 'U': 8, 'V': 4, 'W': 4, 'X': 4}\""
                            ))




                
                    
    

if __name__ == "__main__":
    if len(argv) != 2:
        print("USAGE: python3 faker.py [Number of Samples]")
        exit(1)
    seed(1729)
    try:
        samples = int(argv[1])
    except:
        print("USAGE: python3 data.py [Number of Samples]")
        exit(1)
    main(samples)
