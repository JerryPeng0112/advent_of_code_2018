import re


def main():

    inputData = readFiles()

    data = formatData(inputData)

    opsMatched = getOpsMatched(data) 

    opFuncMap = solveOpFuncs(opsMatched)

    testProgram = readTestProgram()

    result = runInstr(opFuncMap, testProgram)

    print(result)


def getOpsMatched(data):
    # All instruction operation functions
    ops = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', \
            'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']
    
    # Test if the instruction works on a case data
    testOp = lambda op, d: d['regEnd'] == op(list(d['regStart']), d['instr'])

    # Filter the instruction functions that work
    opFuncs = lambda d: filter(lambda op: testOp(globals()[op], d), ops)
    
    # Map instruction functions to op -> funcs dictionary:
    # { op: [funcs...] }
    opToFuncs = lambda d: [d['instr']['op'], list(opFuncs(d))]

    # Get the instruction functions that work on each piece of case data
    opsMatched = list(map(opToFuncs, data))

    return opsMatched


def solveOpFuncs(opsMatched):
    # Dictionary maps opcode to instruction function
    opFuncMap = {}

    # Find all 16 opcode functions
    while len(opFuncMap) != 16:
        
        addedOp = set()
        addedFunc = set()
        count = 0
        
        for case in opsMatched:
            
            op = case[0]
            funcs = case[1]

            # If there are only 1 corresponding instruction function, add to map
            if len(funcs) == 1:
                count += 1
                opFuncMap[op] = funcs[0]
                addedOp.add(op)
                addedFunc.add(funcs[0])

        # Filter out cases with added opcode
        opsMatched = list(filter(lambda d: d[0] not in addedOp, opsMatched))

        # Filter out funcs with added instruction function
        for idx, case in enumerate(opsMatched):
            opsMatched[idx][1] = list(filter(lambda d: d not in addedFunc, case[1]))

    return opFuncMap


def runInstr(opFuncMap, program):
    reg = [0, 0, 0, 0]
    
    for instr in program:
        func = opFuncMap[instr['op']]
        reg = globals()[func](reg, instr)

    return reg[0]
    


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


def readTestProgram():
    data = None

    with open('input2.txt') as f:
        data = f.read()

    data = data.split('\n')
    data = [d for d in data if d]

    # Map instruction string to dict format: {'op', 'A', 'B', 'C'}
    data = map(lambda d: d.split(' '), data)
    data = list(map(lambda d: list(map(lambda x: int(x), d)), data))

    instrDict = lambda d: {'op': d[0], 'A': d[1], 'B': d[2], 'C': d[3]}
    data = [instrDict(d) for d in data]
    
    return data


if __name__ == '__main__':
    main()
