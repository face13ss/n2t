import parse
import os
import sys


def clearComment(vmCode:list)->list[str]:
    rawVMCode = []
    for s in vmCode:
        finalString = ""
        if len(s) == 0 or s[0] == "/":
            continue
        if s.__contains__("//"):
            finalString = s[0:s.index("//")].strip()
        else:
            finalString = s
        rawVMCode.append(finalString)
    return rawVMCode

def writeFile(asmCode:list, filename):
    f = open(filename, "w+")
    for s in asmCode:
        print(s)
        f.write(s+"\n")
    f.close()
# ------------------------------------------------------------
arg = sys.argv[1]


vmSourceCode = []
if arg.__contains__(".vm"):
    fileName = sys.argv[1].split("/")[1].split(".")[0]
    f = open(sys.argv[1], "r")
    vmSourceCode = f.read().splitlines()
    f.close()
else:

    path = os.path.realpath(arg)
    listAllFile = os.listdir(path)
    listVMFile =[]
    for f in listAllFile:
        if f.endswith(".vm"):
            if f.__contains__("Sys"):
                listVMFile.insert(0,f)
            else:
                listVMFile.append(f)

for filename in listVMFile:
    f = open(f"{path}/{filename}", "r")
    fileParseCode = parse.parseCode(clearComment(f.read().splitlines()), filename)
    vmSourceCode.extend(fileParseCode)
    f.close()



# asmCode = parse.parseCode()
writeFileName = ""
if arg.__contains__(".vm"):
    writeFileName = sys.argv[1].split(".")[0] + ".asm"  
else:
    writeFileName = arg + "/run.asm"

writeFile(vmSourceCode, writeFileName)