import sys
import os

arg = sys.argv[1]
vmCode = []
if arg.__contains__(".vm"):
    fileName = sys.argv[1].split("/")[1].split(".")[0]
    f = open(sys.argv[1], "r")
    vmCode = f.read().splitlines()
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

    for name in listVMFile:
        f = open(f"{path}/{name}", "r")
        vmCode.extend(f.read().splitlines())
        f.close()

for s in vmCode:
    print(s)