segment = {
    "local" : "R1",
    "argument" : "R2",
    "this" : "R3",
    "that" : "R4",
}

def pushConstant(value):
    return "@" + value + "\nD=A\n@R0\nA=M\nM=D@R\nM=M+1"

# push segment
# Local, argument, this, that:
def pushSegment(seg, i):
    return "@"+ i + "\nD=A\n@" + segment[seg]+ "\nA=D+M\nD=M\n@R0\nA=M\nM=D\n@R0\nM=M+1"

# pop segment
# Local, argument, this, that:
def popSegment(seg, i):
    return "@R0\nM=M-1\n@"+ i + "\nD=A\n@" + segment[seg] + "\nD=D+M\n@R13\nM=D\n@R0\nD=M\n@R13\nA=M\nM=D"

def pushPointer(i):
    pointer = ""
    if i == "0":
        pointer = "R3"
    else:
        pointer = "R4"
    return "@R0\nM=M-1\nA=M\nD=M\n@" + pointer + "\nM=D"

def popPointer(i):
    pointer = ""
    if i == "0":
        pointer = "R3"
    else:
        pointer = "R4"
    return "@R0\nM=M-1\nA=M\nD=M\n@" + pointer + "\nM=D"