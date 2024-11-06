import sys

# Symbol Table
symbolTableCom0 = {
    "0" : "101010",
    "1" : "111111",
    "-1" : "111010",
    "D" : "001100",
    "A" : "110000",
    "!D" : "001101",
    "!A" : "110001",
    "-D" : "001111",
    "-A" : "110011",
    "D+1" : "011111",
    "A+1" : "110111",
    "D-1" : "001110",
    "A-1" : "110010",
    "D+A" : "000010",
    "D-A" : "010011",
    "A-D" : "000111",
    "D&A" : "000000",
    "D|A" : "010101",
}

symbolTableCom1 = {
    "M" : "110000",
    "!M" : "110001",
    "-M" : "110011",
    "M+1" : "110111",
    "M-1" : "110010",
    "D+M" : "000010",
    "D-M" : "010011",
    "M-D" : "000111",
    "D&M" : "000000",
    "D|M" : "010101",
}

destTable = {
    "null" : "000",
    "M" : "001",
    "D" : "010",
    "DM" : "011",
    "MD" : "011",
    "A" : "100",
    "AM" : "101",
    "AD" : "110",
    "ADM" : "111",
}

jumpTable = {
    "null":"000",
    "JGT" : "001",
    "JEQ" : "010",
    "JGE" : "011",
    "JLT" : "100",
    "JNE" : "101",
    "JLE" : "110",
    "JMP" : "111",
}

#Check file exit
a = len(sys.argv)
if a < 2:
    print("Where your file??????")
    exit()
# read file
f = open(sys.argv[1], "r")
listA = f.read().splitlines()
f.close()
# pure assembly
filterList = []
machineCodes = []
for s in listA:
    stringLength = len(s)
    if (stringLength > 0 and s[0] == "/") or stringLength == 0:
        continue
    opcode = s.replace(" ","")
    end = opcode.find("/")
    filterList.append(end > 1 and opcode[0: opcode.find("/")] or opcode)

##########################################################################
# FOR helper function
def DecimalToBinary(num):
    return bin(num).replace("0b", "")

def paddingBinaryTo15bit(binStr):
    strlen = len(binStr)
    requireLen = 15
    string0 = ""
    if requireLen - strlen == 0:
        return binStr
    if requireLen - strlen < 0:
        print("exception paddingBinaryTo15bit")
        exit()
    for i in range(requireLen - strlen):
        string0 = string0 + "0"
    return string0 + binStr

def assignData(opcode):
    print("assignData: " + opcode)
    header = "111"
    opcodeList = opcode.split("=")
    comp = symbolTableCom0.__contains__(opcodeList[1]) and "0" or "1"
    compStr = comp == "0" and symbolTableCom0.get(opcodeList[1]) or symbolTableCom1.get(opcodeList[1])

    result = header + comp + compStr + destTable.get(opcodeList[0]) + jumpTable.get("null")
    print("assignData: " + result)
    return result

def jump(opcode):
    print("jump: " + opcode)
    header = "111"
    opcodeList = opcode.split(";")
    comp = symbolTableCom0.__contains__(opcodeList[0]) and "0" or "1"
    compStr = comp == "0" and symbolTableCom0.get(opcodeList[0]) or symbolTableCom0.get(opcodeList[0])
    
    result = header + comp + compStr + destTable.get("null") + jumpTable.get(opcodeList[1])
    print("jump: " + result)
    return result

##########################################################################

##########################################################################
# LOGIC HERE
for s in filterList:
    if s[0] == "@":
        number = int(s.replace("@",""))
        machineCodes.append("0" + paddingBinaryTo15bit(DecimalToBinary(number)))
    else:
        if s.__contains__("="):
            machineCodes.append(assignData(s))
        elif s.__contains__(";"):
            machineCodes.append(jump(s))
##########################################################################


#----------------Write file-----------------------------
fileName = sys.argv[1].split("/")[1].split(".")[0] + ".hack"

f = open(sys.argv[1].split("/")[0] + "/" + fileName,"w+")
for s in machineCodes:
    f.write(s + "\n")
    

f.close()
print(len(filterList))
