import sys

segment = {
    "local" : "R1",
    "argument" : "R2",
    "this" : "R3",
    "that" : "R4",
}
TEMP = {
    "0" : "R5",
    "1" : "R6",
    "2" : "R7",
    "3" : "R8",
    "4" : "R9",
    "5" : "R10",
    "6" : "R11",
    "7" : "R12",
}

def pushConstant(value):
    return "@" + value + "\nD=A\n@R0\nA=M\nM=D\n@R0\nM=M+1"

# push segment
# Local, argument, this, that:
def pushSegment(seg, i):
    return "@"+ i + "\nD=A\n@" + segment[seg]+ "\nA=D+M\nD=M\n@R0\nA=M\nM=D\n@R0\nM=M+1"

# pop segment
# Local, argument, this, that:
def popSegment(seg, i):
    return "@R0\nM=M-1\n@"+ i + "\nD=A\n@" + segment[seg] + "\nD=D+M\n@R13\nM=D\n@R0\n\nA=M\nD=M\n@R13\nA=M\nM=D"

def pushPointer(i):
    pointer = ""
    if i == "0":
        pointer = "R3"
    else:
        pointer = "R4"
    return "\n@"+pointer + "\nD=M\n@R0\nA=M\nM=D\n@R0\nM=M+1"

def popPointer(i):
    pointer = ""
    if i == "0":
        pointer = "R3"
    else:
        pointer = "R4"
    return "@R0\nM=M-1\nA=M\nD=M\n@" + pointer + "\nM=D"

def pushTemp(value):
    result = "@" + TEMP[value] + "\nD=M" + "\n@" + "R0\nA=M\nM=D"
    result += "\n@R0\nM=M+1"
    return result

def popTemp(value):
    result = "@R0\nM=M-1\nA=M\nD=M"
    result += "\n@" + TEMP[value] + "\nM=D"
    return result

def pushStatic(fileName, i):
    return "@"+fileName + "." + i +"\nD=M\n@R0\nA=M\nM=D\n@R0\nM=M+1"

def popStatic(fileName, i):
    return "@R0\nM=M-1\nA=M\nD=M\n@"+fileName + "." + i+"\nM=D"

# ADD ----------------------------------------------------
# @--SP
# D=M
# @--SP
# M=D+M
# SP++
def add():
    # @--SP
    add = "\n@R0\nM=M-1"
    add += "\n@"+ "R0" + "\nA=M\nD=M"
    # @--SP
    add += "\n@R0\nM=M-1"

    add += "\n@"+ "R0" + "\nA=M\nM=D+M"

    add += "\n@R0\nM=M+1"
    return add

# SUB ----------------------------------------------------
# @--SP
# D=M
# @--SP
# M=M-D
# SP++
def sub():
    # @--SP
    sub = "\n@R0\nM=M-1"
    sub += "\n@"+ "R0" + "\nA=M\nD=M"
    # @--SP
    sub += "\n@R0\nM=M-1"

    sub += "\n@"+ "R0" + "\nA=M\nM=M-D"

    sub += "\n@R0\nM=M+1"
    return sub

def neg():
    asm = "@R0\nA=M-1\nM=-M"
    return asm

def eq(label):
    # save y to D
    asm = "@R0\nM=M-1\n@R0\nA=M\nD=M"
    # save y to R14
    asm+= "\n@R14\nM=D"
    # save x to D
    asm+= "\n@R0\nM=M-1\n@R0\nA=M\nD=M"
    asm+= "\n@R14\nD=D-M\n@TRUE"+ label +"\nD;JEQ\n@R0\nA=M\nM=0\n@END"+label+"\n0;JMP"
    asm+= "\n(TRUE" + label +")\n@R0\nA=M\nM=-1"
    asm+= "\n(END" + label + ")\n@R0\nM=M+1"
    return asm

def gt(label):
    # save y to D
    asm = "@R0\nM=M-1\n@R0\nA=M\nD=M"
    # save y to R14
    asm+= "\n@R14\nM=D"
    # save x to D
    asm+= "\n@R0\nM=M-1\n@R0\nA=M\nD=M"
    asm+= "\n@R14\nD=D-M\n@TRUE"+ label +"\nD;JGT\n@R0\nA=M\nM=0\n@END"+label+"\n0;JMP"
    asm+= "\n(TRUE" + label +")\n@R0\nA=M\nM=-1"
    asm+= "\n(END" + label + ")\n@R0\nM=M+1"
    return asm

def lt(label):
    # save y to D
    asm = "@R0\nM=M-1\n@R0\nA=M\nD=M"
    # save y to R14
    asm+= "\n@R14\nM=D"
    # save x to D
    asm+= "\n@R0\nM=M-1\n@R0\nA=M\nD=M"
    asm+= "\n@R14\nD=D-M\n@TRUE"+ label +"\nD;JLT\n@R0\nA=M\nM=0\n@END"+label+"\n0;JMP"
    asm+= "\n(TRUE" + label +")\n@R0\nA=M\nM=-1"
    asm+= "\n(END" + label + ")\n@R0\nM=M+1"
    return asm

def andWise():
    # save y to D
    asm = "@R0\nM=M-1\n@R0\nA=M\nD=M"
    # save y to R14
    asm+= "\n@R14\nM=D"
    # save x to D
    asm+= "\n@R0\nM=M-1\n@R0\nA=M\nD=M"
    asm+= "\n@R14\nD=D&M\n@R0\nA=M\nM=D"
    asm+= "\n@R0\nM=M+1"
    return asm

def orWise():
    # save y to D
    asm = "@R0\nM=M-1\n@R0\nA=M\nD=M"
    # save y to R14
    asm+= "\n@R14\nM=D"
    # save x to D
    asm+= "\n@R0\nM=M-1\n@R0\nA=M\nD=M"
    asm+= "\n@R14\nD=D|M\n@R0\nA=M\nM=D"
    asm+= "\n@R0\nM=M+1"
    return asm

def notWise():
    asm = "@R0\nA=M-1\nM=!M"
    return asm


def end():
    end = "(END)\n@END\n0;JMP\n"
    return end

# push segment index -> push the value of segment[index] onto stack
# pop  segment index -> pops the top stack value and store it in segment[index]
fileName = sys.argv[1].split("/")[1].split(".")[0]
f = open(sys.argv[1], "r")
listA = f.read().splitlines()
f.close()
rawVMCode = []
for s in listA:
    if len(s) == 0 or s[0] == "/":
        continue
    rawVMCode.append(s)

asmCode = []
for idx,s in enumerate(rawVMCode):
    opcode = s.split(" ")
    if len(opcode) > 1:
        # push
        if opcode[0] == "push":
            if opcode[1] == "constant":
                asmCode.append(pushConstant(opcode[2]))
            elif opcode[1] == "local" or opcode[1] == "argument" or opcode[1] == "this" or opcode[1] == "that":
                asmCode.append(pushSegment(opcode[1], opcode[2]))
            elif opcode[1] == "pointer":
                asmCode.append(pushPointer(opcode[2]))
            elif opcode[1] == "temp":
                asmCode.append(pushTemp(opcode[2]))
            elif opcode[1] == "static":
                asmCode.append(pushStatic(fileName, opcode[2]))
            else:
                asmCode.append(s)
        # pop -------------------------------------------
        elif opcode[0] == "pop":
            if opcode[1] == "local" or opcode[1] == "argument" or opcode[1] == "this" or opcode[1] == "that":
                asmCode.append(popSegment(opcode[1], opcode[2]))
            elif opcode[1] == "pointer":
                asmCode.append(popPointer(opcode[2]))
            elif opcode[1] == "temp":
                asmCode.append(popTemp(opcode[2]))
            elif opcode[1] == "static":
                asmCode.append(popStatic(fileName, opcode[2]))
            else:
                asmCode.append(s)
        else:
            asmCode.append(s)
    else:
        if opcode[0] == "add":
            asmCode.append(add())
        elif opcode[0] == "sub":
            asmCode.append(sub())
        elif opcode[0] == "neg":
            asmCode.append(neg())
        elif opcode[0] == "eq":
            asmCode.append(eq(str(idx)))
        elif opcode[0] == "gt":
            asmCode.append(gt(str(idx)))
        elif opcode[0] == "lt":
            asmCode.append(lt(str(idx)))
        elif opcode[0] == "and":
            asmCode.append(andWise())
        elif opcode[0] == "or":
            asmCode.append(orWise())
        elif opcode[0] == "not":
            asmCode.append(notWise())
        else:
            asmCode.append(opcode[0])
    
asmCode.append(end())

writeFileName = sys.argv[1].split(".")[0] + ".asm"
f = open(writeFileName, "w+")
for s in asmCode:
    print(s)
    f.write(s+"\n")

f.close()
