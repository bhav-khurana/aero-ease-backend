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
