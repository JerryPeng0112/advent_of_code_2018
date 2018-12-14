from functools import reduce

def main():
    inputs = []
    readFiles(inputs)

    result = reduce(lambda x, y: x + y, inputs)
    print(result)

def processFileLine(line):
    return int(line)

def readFiles(inputs):
    file = open("input.txt", "r")
    for line in file:
        inputs.append(processFileLine(line))

if __name__ == "__main__":
    main()
