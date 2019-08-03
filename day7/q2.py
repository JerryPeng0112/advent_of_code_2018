import re
from copy import deepcopy
from heapq import heapify
from collections import deque


NUM_WORKERS = 5
BASE_TIME = 60


class Worker:
    def __init__(self):
        self.time = 0
        self.step = None


def main():
    data = readFiles()

    startSteps, endStep = getStartStep(data)
    stepToTake, stepDependOn = buildStepRelations(data)

    time = calcTime(data, startSteps, endStep, stepToTake, stepDependOn)
    print(time)


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


def calcTime(data, startSteps, endStep, stepToTake, stepDependOn):
    workers = [Worker() for i in range(NUM_WORKERS)]
    completeTime = {}
    stepTracker = deepcopy(stepDependOn)

    stepHeap = deque(startSteps)
    nextStep = stepHeap.popleft()

    while nextStep != endStep:

        for s in stepToTake[nextStep]:
            stepDependOn[s].remove(nextStep)

            if not stepDependOn[s]:
                stepHeap.append(s)

        # Assign workers
        assign(workers, nextStep, stepToTake, stepTracker, completeTime)
        nextStep = stepHeap.popleft()

    assign(workers, nextStep, stepToTake, stepTracker, completeTime)

    return max(list(map(lambda x: x.time, workers)))


def assign(workers, nextStep, stepToTake, stepTracker, completeTime):
    # Find available worker
    minWorkerTime = min(list(map(lambda x: x.time, workers)))
    minWorkerIndex = list(map(lambda x: x.time, workers)).index(minWorkerTime)

    # Find latest time nextStep can be taken
    dependents = stepTracker[nextStep] if nextStep in stepTracker.keys() else []
    latestStartTime = 0
    if dependents:
        latestStartTime = max(list(map(lambda x: completeTime[x], dependents)))

    latestStartTime = max([latestStartTime, minWorkerTime])

    # Calculate time to finish step
    finishTime = latestStartTime + BASE_TIME + 1 + ord(nextStep) - ord('A')

    assignedWorker = workers[minWorkerIndex]
    assignedWorker.time = finishTime
    assignedWorker.step = nextStep
    completeTime[nextStep] = finishTime



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
