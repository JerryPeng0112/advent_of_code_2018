import re
def main():

    data = readFiles()

    minX, minY, maxX, maxY = getMinAndMax(data)
    print(minX, minY, maxX, maxY)

    #print(result)

def getMinAndMax(data):
    xs = []
    ys = []
    for datum in data:
        xs.append(datum["x"])
        ys.append(datum["y"])

    return min(xs), min(ys), max(xs), max(ys)

def processFileLine(line):
    matches = re.compile("(.*), (.*)").findall(line)[0]
    matches = [int(match) for match in matches]

    data = {"x": matches[0], "y": matches[1]}

    return data

def readFiles():
    data = []
    file = open("input.txt", "r")
    for line in file:
        data.append(processFileLine(line))
    return data

if __name__ == "__main__":
    main()
