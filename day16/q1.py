import re




def main():

    inputData = readFiles()

    data = formatData(inputData)

    result = getResult(data) 
    print(result)


def getResult(data):
    ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, \
            gtir, gtri, gtrr, eqir, eqri, eqrr]
    
    testOp = lambda op, d: d['regEnd'] == op(list(d['regStart']), d['instr'])
    opsMatched = lambda d: map(lambda op: testOp(op, d), ops)
    getNumOpsMatched = lambda d: len(list(filter(lambda x: x, opsMatched(d))))
    numOpsMatched = map(getNumOpsMatched, data)

    return len(list(filter(lambda d: d >= 3, numOpsMatched)))


"""
Instruction operation functions
"""

def addr(reg, instr):
    reg[instr['C']] = reg[instr['A']] + reg[instr['B']]
    return reg


def addi(reg, instr):
    reg[instr['C']] = reg[instr['A']] + instr['B']
    return reg


def mulr(reg, instr):
    reg[instr['C']] = reg[instr['A']] * reg[instr['B']]
    return reg
    

def muli(reg, instr):
    reg[instr['C']] = reg[instr['A']] * instr['B']
    return reg


def banr(reg, instr):
    reg[instr['C']] = reg[instr['A']] & reg[instr['B']]
    return reg
    

def bani(reg, instr):
    reg[instr['C']] = reg[instr['A']] & instr['B']
    return reg


def borr(reg, instr):
    reg[instr['C']] = reg[instr['A']] | reg[instr['B']]
    return reg
    

def bori(reg, instr):
    reg[instr['C']] = reg[instr['A']] | instr['B']
    return reg


def setr(reg, instr):
    reg[instr['C']] = reg[instr['A']]
    return reg
    

def seti(reg, instr):
    reg[instr['C']] = instr['A']
    return reg


def gtir(reg, instr):
    reg[instr['C']] = 1 if instr['A'] > reg[instr['B']] else 0
    return reg


def gtri(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] > instr['B'] else 0
    return reg


def gtrr(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] > reg[instr['B']] else 0
    return reg


def eqir(reg, instr):
    reg[instr['C']] = 1 if instr['A'] == reg[instr['B']] else 0
    return reg


def eqri(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] == instr['B'] else 0
    return reg


def eqrr(reg, instr):
    reg[instr['C']] = 1 if reg[instr['A']] == reg[instr['B']] else 0
    return reg


def formatData(inputData):
    data = []
    numCases = len(inputData) // 3

    for i in range(numCases):

        case = {}

        # Get the 
        beforeText = inputData[i * 3]
        instrText = inputData[i * 3 + 1]
        afterText = inputData[i * 3 + 2]

        # Extract before register data
        regStartPattern = re.compile(r'Before: \[(.*)\]')
        regStart = regStartPattern.match(beforeText).groups()[0]
        regStart = regStart.strip(' ').split(',')

        # Extract instruction data
        instrText = instrText.split(' ')

        # Extract after register data
        regEndPattern = re.compile(r'After:  \[(.*)\]')
        regEnd = regEndPattern.match(afterText).groups()[0]
        regEnd = regEnd.strip(' ').split(',')

        # Convert all strings to integers
        regStart = list(map(lambda x: int(x), regStart))
        instrText = list(map(lambda x: int(x), instrText))
        regEnd = list(map(lambda x: int(x), regEnd))

        # Map instrText to {op, A, B, C}
        instr = {}
        instr['op'] = instrText[0] 
        instr['A'] = instrText[1] 
        instr['B'] = instrText[2] 
        instr['C'] = instrText[3] 
        
        case['regStart'] = regStart
        case['instr'] = instr
        case['regEnd'] = regEnd

        data.append(case)

    return data



def readFiles():
    data = None

    with open ('input1.txt') as f:
        data = f.read()

    data = data.split('\n')
    data = [d for d in data if d]

    return data


if __name__ == '__main__':
    main()
