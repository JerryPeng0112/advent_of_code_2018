import re
from heapq import heapify, heappush, heappop

def main():
    data = readFiles()

    startSteps, endStep = getStartStep(data)
    stepToTake, stepDependOn = buildStepRelations(data)

    steps = calcSteps(data, startSteps, endStep, stepToTake, stepDependOn)
    print(steps)


def getStartStep(data):
    stepFrom = set(list(map(lambda x: x[0], data)))
    stepTo = set(list(map(lambda x: x[1], data)))
    startSteps = list(stepFrom.difference(stepTo))
    endStep = list(stepTo.difference(stepFrom))[0]
    heapify(startSteps)
    return startSteps, endStep


def buildStepRelations(data):
    stepToTake = {}
    stepDependOn = {}

    for d in data:

        if d[0] not in stepToTake:
            stepToTake[d[0]] = [d[1]]

        else:
            stepToTake[d[0]].append(d[1])

    for d in data:
        if d[1] not in stepDependOn:
            stepDependOn[d[1]] = [d[0]]
        else:
            stepDependOn[d[1]].append(d[0])

    return stepToTake, stepDependOn


def calcSteps(data, startSteps, endStep, stepToTake, stepDependOn):
    steps = ""
    stepHeap = startSteps
    nextStep = heappop(stepHeap)
    steps += nextStep

    while nextStep != endStep:
        
        for s in stepToTake[nextStep]:
            stepDependOn[s].remove(nextStep)

            if not stepDependOn[s]:
                heappush(stepHeap, s)

        nextStep = heappop(stepHeap)
        steps += nextStep

    return steps


def readLine(line):
    pattern = re.compile(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.")
    return pattern.match(line).groups()


def readFiles():
    data = []
    file = open("input.txt", "r")

    for line in file:
        data.append(readLine(line))

    file.close()
    return data


if __name__ == "__main__":
    main()
