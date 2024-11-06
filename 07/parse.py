import sys

# RAM address     Usage
# 0-15            sixteen virtual register
# 16-255          Static variable
# 256-2047        Stack
#
# local     256 - 383
# arg       384 - 512
# this      513 - 641
# that      642 - 769
# constant  770 - 898 
# Stack     899 - 2047
# 
# POINT 0 -> THIS
# POINT 1 -> THAT

Register = {
    "SP"    : 899,
    "LCL"   : 256,
    "ARG"   : 384,
    "THIS"  : 513,
    "THAT"  : 642,
    "TEMP0" : 0,
    "TEMP1" : 0,
    "TEMP2" : 0,
    "TEMP3" : 0,
    "TEMP4" : 0,
    "TEMP5" : 0,
    "TEMP6" : 0,
    "TEMP7" : 0,
    "R13"   : 0,
    "R14"   : 0,
    "R15"   : 0
}

RegisterPos = {
    "SP"    : "0",
    "LCL"   : "1",
    "ARG"   : "2",
    "THIS"  : "3",
    "THAT"  : "4",
    "TEMP0" : "5",
    "TEMP1" : "6",
    "TEMP2" : "7",
    "TEMP3" : "8",
    "TEMP4" : "9",
    "TEMP5" : "10",
    "TEMP6" : "11",
    "TEMP7" : "12",
    "R13"   : "13",
    "R14"   : "14",
    "R15"   : "15"
}

TEMP = {
    "0" : 5,
    "1" : 6,
    "2" : 7,
    "3" : 8,
    "4" : 9,
    "5" : 10,
    "6" : 11,
    "7" : 12,
}

RAMSegmentBase = {
    "LCL"       : 256,
    "ARG"       : 384,
    "THIS"      : 513,
    "THAT"      : 642,
    "STACK"     : 770
}

RAMSegmentP = {
    "LCL"       : 256,
    "ARG"       : 384,
    "THIS"      : 513,
    "THAT"      : 642,
    "STACK"     : 770
}

stackBase = 513
# SP   RAM[0]
# LCL  RAM[1]
# ARG  RAM[2]
# THIS RAM[3]
# THAT RAM[4]
# TEMP RAM[5-12]
# R13
# R14  RAM[13-15]
# R15

const = ["C_ARITHMETIC",
         "C_POP",
         "C_LABEL",
         "C_GOTO",
         "C_IF",
         "C_FUNCTION",
         "C_RETURN",
         "C_CALL"]

# STACK
def increaseStack():
    Register["SP"] += 1

def decreaseStack():
    Register["SP"] -= 1


# Constant -----------------------------------------------
def pushConstant(value):
    result = "@" + value + "\nD=A" + "\n@" + str(Register["SP"]) + "\nM=D"
    Register["SP"] +=1
    return result
    
# --------------------------------------------------------

# Local --------------------------------------------------
# pop Local
# @SP
# D=M
# @local + i
# M=D
def popLocal(value):
    result = "@"+ str(Register["SP"]) + "\nD=M" + "\n@" + str((RAMSegmentP["LCL"] + int(value))) + "\nM=D"
    Register["SP"] -=1
    return result

# push local
# @local + i
# D=M
# @SP
# M=D
def pushLocal(value):
    result = "@" + str((RAMSegmentP["LCL"] + int(value))) + "\nD=M" + "\n@" + str(Register["SP"]) + "\nM=D"
    Register["SP"] +=1
    return result

# --------------------------------------------------------

# Argument -----------------------------------------------
# pop Argument i
# @SP
# D=M
# @ARG + i
# M=D
def popArgument(value):
    result = "@"+ str(Register["SP"]) + "\nD=M" + "\n@" + str((RAMSegmentP["ARG"] + int(value))) + "\nM=D"
    Register["SP"] -=1
    return result

# push argument i
# @ARG + i
# D=M
# @SP
# M=D
def pushArgument(value):
    result = "@" + str((RAMSegmentP["ARG"] + int(value))) + "\nD=M" + "\n@" + str(Register["SP"]) + "\nM=D"
    Register["SP"] +=1
    return result


# --------------------------------------------------------

# THIS ---------------------------------------------------
# pop this i
#
# @SP
# D=M
# @THIS + i
# M=D
def popThis(value):
    result = "@"+ str(Register["SP"]) + "\nD=M" + str((RAMSegmentP["THIS"] + int(value))) + "\nM=D"
    Register["SP"] -=1
    return result

# push this i
# @THIS + i
# D=M
# @SP
# M=D
def pushThis(value):
    result = "@" + str((RAMSegmentP["THIS"] + int(value))) + "\nD=M" + "\n@" + str(Register["SP"]) + "\nM=D"
    Register["SP"] +=1
    return result
# --------------------------------------------------------

# THAT ---------------------------------------------------
# pop that i
# @SP
# D=M
# @THAT + i
# M=D
def popThat(value):
    result = "@"+ str(Register["SP"]) + "\nD=M" + "\n@" + str((RAMSegmentP["THAT"] + int(value))) + "\nM=D"
    Register["SP"] -=1
    return result

# push that i
# @THAT + i
# M=D
# @SP
# D=M
def pushThat(value):
    result = "@" + str((RAMSegmentP["THAT"] + int(value))) + "\nD=M" + "\n@" + str(Register["SP"]) + "\nM=D"
    Register["SP"] +=1
    return result
# --------------------------------------------------------

# TEMP ---------------------------------------------------
# pop temp i
# @SP
# D=M
# @temp[i]
# M=D
def popTemp(value):
    result = "@"+ str(Register["SP"]) + "\nD=M" + "\n@" + str(TEMP[value]) + "\nM=D"
    Register["SP"] -=1
    return result

# push temp i
# @temp[i]
# D=M
# @SP
# M=D
def pushTemp(value):
    result = "@" + str(TEMP[value]) + "\nD=M" + "\n@" + str(Register["SP"]) + "\nM=D"
    Register["SP"] +=1
    return result
# --------------------------------------------------------


def add(x, y):
    return x + y

def sub():
    return
def initializer():
    return

def hasMoreLines():
    return False

def commandType():
    return const[0]

def arg1():
    return ""

def arg2():
    return 1

# push segment index -> push the value of segment[index] onto stack
# pop  segment index -> pops the top stack value and store it in segment[index]

f = open(sys.argv[1], "r")
listA = f.read().splitlines()
f.close()
rawVMCode = []
for s in listA:
    if len(s) == 0 or s[0] == "/":
        continue
    rawVMCode.append(s)


for s in rawVMCode:
    opcode = s.split(" ")
    if len(opcode) > 1:
        # push
        if opcode[0] == "push":
            if opcode[1] == "constant":
                # print(pushConstant(opcode[2]) + "   // " + s)
                print()
            elif opcode[1] == "local":
                # print(pushLocal(opcode[2]) + "   // " + s)
                print()
            elif opcode[1] == "that":
                # print(pushThat(opcode[2]) + "   // " + s)
                print()
            elif opcode[1] == "argument":
                # print(pushArgument(opcode[2]) + "   // " + s)
                print()
            elif opcode[1] == "this":
                # print(pushThis(opcode[2]) + "   // " + s)
                print()
            elif opcode[1] == "temp":
                # print(pushThis(opcode[2]) + "   // " + s)
                print()
            else:
                print(s)
        # pop -------------------------------------------
        elif opcode[0] == "pop":
            if opcode[1] == "local":
                # print(popLocal(opcode[2])+  "   // " + s)
                print()
            elif opcode[1] == "argument":
                print()
                # print(popArgument(opcode[2])+  "   // " + s)
            elif opcode[1] == "this":
                print()
                # print(popThis(opcode[2])+  "   // " + s)
            elif opcode[1] == "that":
                print()
                # print(popThat(opcode[2])+  "   // " + s)
            elif opcode[1] == "temp":
                print()
                # print(popTemp(opcode[2])+  "   // " + s)
            else:
                print(s)
        
        # else:
        #     print(s)
    else:
        print(opcode[0])
