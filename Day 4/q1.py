import re
import datetime
import enum

class Status(enum.Enum):
    BEGIN = 0
    WAKE = 1
    SLEEP = 2

def main():

    data = readFiles()
    #for i in data:
    #    print(i)
    #print("HERE I AM")

    soldierStatus = processData(data)
    #for key, value in soldierStatus.items():
    #    for i in value:
    #        print(i)
    #print(soldierStatus)
    #soldierID = getSleepSoldier(soldierStatus)
    #sleepMinute = calcSleepMinute(soldierStatus[soldierID])
    #result = soldierID * sleepMinute

    #print(result)

def processData(data):
    soldierStatus = {}
    currID = None
    prevSleepMin = None

    for datum in data:
        if datum["type"] == Status.BEGIN:
            currID = datum["id"]
            if currID not in soldierStatus:
                soldierStatus[currID] = []
            soldierStatus[currID].append([Status.WAKE.value for i in range(60)]) 


        elif datum["type"] == Status.SLEEP:
            sleepTime = datum["datetime"].minute
        
        else:
            wakeTime = datum["datetime"].minute
            for t in range(sleepTime, wakeTime):
                soldierStatus[currID][-1][t] = Status.SLEEP.value
        
    return soldierStatus

def processFileLine(line):
    matches = re.compile("\[(.*)\] (.*)").findall(line)[0]
    info = [match for match in matches]

    data = {}
    data["datetime"] = datetime.datetime.strptime(info[0], "%Y-%m-%d %H:%M")

    if "Guard" in info[1]:
        data["type"] = Status.BEGIN
        data["id"] = info[1].split(" ")[1][1:]

    elif "wakes" in info[1]:
        data["type"] = Status.WAKE

    else:
        data["type"] = Status.SLEEP

    return data

def readFiles():
    data = []
    file = open("input.txt", "r")
    for line in file:
        data.append(processFileLine(line))

    return sorted(data, key=lambda x : x["datetime"])

if __name__ == "__main__":
    main()
