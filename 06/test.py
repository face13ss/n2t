import sys

symbol = {
    "R0" : "0",
    "R1" : "1",
    "R2" : "2",
    "R3" : "3",
    "R4" : "4",
    "R5" : "5",
    "R6" : "6",
    "R7" : "7",
    "R8" : "8",
    "R9" : "9",
    "R10" : "10",
    "R11" : "11",
    "R12" : "12",
    "R13" : "13",
    "R14" : "14",
    "R15" : "15",
}

labelSymbols = {}
def isNum(s):
    try:
        int(s)
        return True
    except:
        return False
    

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
nonLabelOpcodes = []
machineCodes = []
label = ""
for s in listA:
    stringLength = len(s)
    if (stringLength > 0 and s[0] == "/") or stringLength == 0:
        continue
    if s[0] == "(":
        label = s
        continue
    opcode = s.replace(" ","")
    end = opcode.find("/")
    final = end > 1 and opcode[0: opcode.find("/")] or opcode
    if len(label) > 0:
        final += label
        label=""
    filterList.append(final)
#_______________________________________________________________________

for idx, s in enumerate(filterList):
    label = ""
    if s.__contains__("("):
        label = s[s.find("("):]
        labelSymbols[label.replace("(","").replace(")","")] = idx
    nonLabelOpcodes.append (s.replace(label, ""))

print(labelSymbols)
for s in nonLabelOpcodes:
    print(s)
# for s in filterList:
#     if s[0] == "@":
#         opcode = s.replace("@", "")
#         if isNum(opcode):
#             print(s)
#         elif symbol.__contains__(opcode):
#             print("@" + symbol.get(opcode))adsad
#         elif labelSymbol.__contains__(opcode):
#             print("@" + str(labelSymbol.get(opcode)))
#         else:
#             print(s)
#     else:
#         print(s)
# some = [1,2,3,4,5,6]
# for idx, i in enumerate(some):
#     print(str(idx) + " - " + str(i))