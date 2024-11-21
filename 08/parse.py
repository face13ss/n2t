
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

# call function
def functionCall(funcName, call_count):
    callLabel = f"{funcName}.RET_{call_count}"
    ret = f"@{callLabel}\nD=A\n@R0\nA=M\nM=D\n@R0\nM=M+1"
    for address in ["@R1", "@R2", "@R3", "@R4"]:
        ret += f"\n{address}\nD=M\n@R0\nA=M\nM=D\n@R0\nM=M+1"

    ret += f"\n@R0\nD=M\n@R1\nM=D"
    ret += f"\n@{int(call_count)+ 5}\nD=D-A\n@R2\nM=D"
    ret += f"\n@{funcName}\n0;JMP"
    ret += f"\n({callLabel})"
    return ret

def functionReturn():
    #FRAME = R14
    #RET = R15
    ret = f"@R1\nD=M\n@R14\nM=D\n" #FRAME = LCL
    ret+= f"@5\nA=D-A\nD=M\n@R15\nM=D\n" # RET=*(FRAME-5)
    ret+= f"@R2\nD=M\n@0\nD=D+A\n@R13\nM=D\n@R0\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n" # *ARG = pop()
    ret+= f"@R2\nD=M\n@R0\nM=D+1\n" # SP = ARG + 1

    for addr in ["@R4", "@R3", "@R2", "@R1"]:
        ret+= f"@R14\nAMD=M-1\nD=M\n{addr}\nM=D\n"
    ret+= f"@R15\nA=M\n0;JMP"
    return ret

# function define
def functionDefine(funcName, nArgs):
    ret = f"({funcName})"
    for _ in range(int(nArgs)):
        ret += "\n@0\nD=A\n@R0\nA=M\nM=D\n@R0\nM=M+1"
    return ret

def end():
    end = "(END)\n@END\n0;JMP\n"
    return end

# Branch
# Conditional JUMP
def conditionJump(label):
    jump = f"@R0\nM=M-1\nA=M\nD=M\n@{label}\nD;JNE"
    return jump
# Unconditional JUMP
def unconditionalJump(label):
    jump = f"@{label}\n0;JMP"
    return jump

# push segment index -> push the value of segment[index] onto stack
# pop  segment index -> pops the top stack value and store it in segment[index]

def parseCode(rawVMCode:list, fileName: str)->list:
    asmCode = []
    for idx,s in enumerate(rawVMCode):
        
        opcode = s.split(" ")
        if len(opcode) >= 3:
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
                    asmCode.append(s +"debug push 3")
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
                    asmCode.append(s +"debug pop 3")
            elif opcode[0] == "function":
                asmCode.append(functionDefine(opcode[1], opcode[2]))
            elif opcode[0] == "call":
                asmCode.append(functionCall(opcode[1], idx))
            else:
                asmCode.append(s)
        elif len(opcode) == 2:
            if opcode[0] == "label":
                asmCode.append(f'({opcode[1]})')
            elif opcode[0] == "if-goto":
                asmCode.append(conditionJump(opcode[1]))
            elif opcode[0] == "goto":
                asmCode.append(unconditionalJump(opcode[1]))
            else:
                asmCode.append(s +"debug 2")
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
            elif opcode[0] == "return":
                asmCode.append(functionReturn())
            else:
                asmCode.append(s)
        
    # asmCode.append(end())
    return asmCode

