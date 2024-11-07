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
    "SP"    : 256,
    "LCL"   : 300,
    "ARG"   : 400,
    "THIS"  : 3000,
    "THAT"  : 3010,
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
    return "\n@R0\nM=M+1"
  

def decreaseStack():
    return "@R0\nM=M-1\n"


# Constant -----------------------------------------------
# push constant value
# @value
# D=A
# @R0
# A=M
# M=S
def pushConstant(value):
    result = "@" + value + "\nD=A" + "\n@R0" + "\nA=M\nM=D"
    result += increaseStack()
    return result
    
# --------------------------------------------------------

# Local --------------------------------------------------
# pop Local
# @--SP
# D=M
# @local + i
# M=D
def popLocal(value):
    result = decreaseStack()
    result += "@"+ "R0" + "\nD=M" 
    result += "\n@R1" + "\nD=M"+ "\n@"+value + "\nD=D+A\nA=D\nM=D"
    return result

# push local i
# @local
# D=M
# @i
# D=D+A
# D=M
# @SP
# A=M
# M=D
def pushLocal(value):
    result = "@R1" + "\nD=M"+ "\n@"+value + "\nD=D+A\nA=D\nD=M" + "\n@" + "R0" + "\nA=M\nM=D"
    result += increaseStack()
    return result

# --------------------------------------------------------

# Argument -----------------------------------------------
# pop Argument i
# @SP
# D=M
# @ARG
# D=M
# @i
# D=D+A
# A=D
# M=D
def popArgument(value):
    result = decreaseStack()
    result += "@"+ "R0" + "\nD=M" + "\n@R2" + "\nD=M" + "\n@"+value + "\nD=D+A\nA=D\nM=D"
    return result

# push argument i
# @ARG + i
# D=M
# @SP
# M=D
def pushArgument(value):
    result = "@R1" + "\nD=M" +"\n@"+ value + "\nD=D+A\nA=D\nD=M" + "\n@" + "R0" + "\nM=D"
    result += increaseStack()
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
    result = decreaseStack()
    result += "@"+ "R0" + "\nD=M\n@R3" + "\nD=M"+ "\n@" + value + "\nD=D+A\nA=D\nM=D"
    return result

# push this i
# @THIS + i
# D=M
# @SP
# M=D
def pushThis(value):
    result = "@R3" + "\nD=M"+ "\n@" + value + "\nD=D+A\nA=D\nD=M" + "\n@" + "R0" + "\nM=D"
    result += increaseStack()
    return result
# --------------------------------------------------------

# THAT ---------------------------------------------------
# pop that i
# @SP
# D=M
# @THAT + i
# M=D
def popThat(value):
    result = decreaseStack()
    result += "@"+ "R0" + "\nD=M" + "\n@R4" + "\nD=M" + "\n@" + value + "\nD=D+A\nA=D\nM=D"
    return result

# push that i
# @THAT + i
# M=D
# @SP
# D=M
def pushThat(value):
    result = "@R4" + "\nD=M" + "\n@" + value + "\nD=D+A\nA=D\nD=M" + "\n@" + "R0" + "\nM=D"
    result += increaseStack()
    return result
# --------------------------------------------------------

# TEMP ---------------------------------------------------
# pop temp i
# @SP
# D=M
# @temp[i]
# M=D
def popTemp(value):
    result = decreaseStack()
    result += "@"+ "R0" + "\nD=M" + "\n@R" + str(TEMP[value]) + "\nM=D"
    return result

# push temp i
# @temp[i]
# D=M
# @SP
# M=D
def pushTemp(value):
    result = "@R" + str(TEMP[value]) + "\nD=M" + "\n@" + "R0" + "\nM=D"
    result += increaseStack()
    return result
# --------------------------------------------------------

# POINTER ------------------------------------------------
# 0 = THIS (R3) or 1 = THAT (R4)

# push pointer 0
# @R3
# D=M
# @R0
# A=M
# M=D

def pushPointer(value):
    pointer = ""
    if value == 0:
        pointer = "R3"
    else:
        pointer = "R4"
    
    result = "@" + pointer + "\nD=M" + "\n@R0\nA=M\nM=D"
    result += increaseStack()
    return result

# pop pointer 0
# @--R0
# D=M
# @R3
# M=D
def popPointer(value):
    pointer = ""
    if value == 0:
        pointer = "R3"
    else:
        pointer = "R4"
    result = decreaseStack()
    result += "@R0\nD=M\n@"+pointer+"\nM=D"
# --------------------------------------------------------

# ADD ----------------------------------------------------
# @--SP
# D=M
# @--SP
# M=D+M
# SP++
def add():
    add = decreaseStack()
    add += "@"+ "R0" + "\nD=M"
    # 
    Register["SP"] -=1
    add += "\n@"+ "R0" + "\nM=D+M"
    add += increaseStack()
    return add

# SUB ----------------------------------------------------
# @--SP
# D=M
# @--SP
# M=D-M
# SP++
def sub():
    sub = decreaseStack()
    sub += "@"+ "R0" + "\nD=M"
    # 
    Register["SP"] -=1
    sub += "\n@"+ "R0" + "\nM=D-M"
    sub += increaseStack()
    return sub

def end():
    end = "(END)\n@END\n0;JMP\n"
    return end

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
                print(pushConstant(opcode[2]) + "   // " + s)
                
            elif opcode[1] == "local":
                print(pushLocal(opcode[2]) + "   // " + s)
                
            elif opcode[1] == "that":
                print(pushThat(opcode[2]) + "   // " + s)
                
            elif opcode[1] == "argument":
                print(pushArgument(opcode[2]) + "   // " + s)
                
            elif opcode[1] == "this":
                print(pushThis(opcode[2]) + "   // " + s)
                
            elif opcode[1] == "temp":
                print(pushThis(opcode[2]) + "   // " + s)
            elif opcode[1] == "pointer":
                print(pushPointer(opcode[2]) + "   // " + s)
            else:
                print(s)
        # pop -------------------------------------------
        elif opcode[0] == "pop":
            if opcode[1] == "local":
                print(popLocal(opcode[2])+  "   // " + s)
                
            elif opcode[1] == "argument":
                print(popArgument(opcode[2])+  "   // " + s)

            elif opcode[1] == "this":
                print(popThis(opcode[2])+  "   // " + s)

            elif opcode[1] == "that":
                
                print(popThat(opcode[2])+  "   // " + s)
            elif opcode[1] == "temp":
                
                print(popTemp(opcode[2])+  "   // " + s)
            else:
                print(s)
        
        # else:
        #     print(s)
    else:
        if opcode[0] == "add":
            print(add())
        elif opcode[0] == "sub":
            print(sub())  
        else:
            print(opcode[0])
    
print(end())