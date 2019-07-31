import re
import datetime
import enum

class Status(enum.Enum):
    BEGIN = 0
    WAKE = 1
    SLEEP = 2

def main():

    data = readFiles()

    soldierSchedules = processData(data)
    ID, mostFreqMinute = calcMostFreqMinute(soldierSchedules)
    result = int(ID) * mostFreqMinute

    print(result)

def processData(data):
    soldierSchedules = {}
    currID = None
    prevSleepTime = None

    for datum in data:
        if datum["type"] == Status.BEGIN:
            currID = datum["id"]
            if currID not in soldierSchedules:
                soldierSchedules[currID] = []
            soldierSchedules[currID].append([Status.WAKE.value for i in range(60)]) 


        elif datum["type"] == Status.SLEEP:
            prevSleepTime = datum["datetime"].minute
        
        else:
            wakeTime = datum["datetime"].minute
            for t in range(prevSleepTime, wakeTime):
                soldierSchedules[currID][-1][t] = Status.SLEEP.value
        
    return soldierSchedules
    
def calcMostFreqMinute(soldierSchedules):
    ID, mostFreqMinute, maxCount = -1, -1, -1

    for id, schedule in soldierSchedules.items():
        count = [0 for i in range(60)]
        
        for shift in schedule:
            for t in range(60):
                if shift[t] == Status.SLEEP.value:
                    count[t] += 1

        for t in range(60):
            if count[t] > maxCount:
                maxCount = count[t]
                mostFreqMinute = t
                ID = id

    return ID, mostFreqMinute

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
    file.close()

    return sorted(data, key=lambda x : x["datetime"])

if __name__ == "__main__":
    main()
