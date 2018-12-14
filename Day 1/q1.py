from functools import reduce

def main():
    input = []
    readFiles(input)

    result = reduce(lambda x, y: x + y, input)
    print(result)

def processFileLine(line):
    return int(line)

def readFiles(input):
    file = open("input.txt", "r")
    for line in file:
        input.append(processFileLine(line))

if __name__ == "__main__":
    main()
