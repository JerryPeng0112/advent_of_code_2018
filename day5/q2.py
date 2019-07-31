def main():

    string = readFiles()

    result = findShortestPolymer(string)

    print(result)

def findShortestPolymer(string):
    minLength = len(string)
    for letter in range(0, 26):
        refinedString = removeLetters(string, letter)
        stringLength = len(reducePolymer(refinedString))
        if stringLength < minLength:
            minLength = stringLength

    return minLength

def removeLetters(string, letter):
    lowercase = chr(ord('a') + letter)
    uppercase = chr(ord('A') + letter)
    refinedString = ""
    for l in string:
        if l != lowercase and l != uppercase:
            refinedString += l
    return refinedString

def reducePolymer(string):
    idx = 0
    while idx != len(string) - 1:
        if canReact(string[idx], string[idx + 1]):
            string = string[:idx] + string[idx + 2:]  
            if idx != 0:
                idx -= 1
        else:
            idx += 1
    return string

def canReact(char1, char2):
    if char1.islower():
        if char2 == char1.upper():
            return True
        else:
            return False
    else:
        if char2 == char1.lower():
            return True
        else:
            return False

def readFiles():
    file = open("input.txt", "r")
    data = file.readline().strip()
    return data

if __name__ == "__main__":
    main()
