#run command
#python3 get-nouns-and-label.py 'input/POS-nouns' 'output/POS-output.txt'

import sys
import re

def listAllFile(fullPath, listSubDir = 0):
    from os import listdir
    from os.path import isfile, join, isdir

    onlyfiles = []
    for f in listdir(fullPath):
        tf = join(fullPath, f)
        if isfile(tf):
            onlyfiles.append(tf)
        elif (listSubDir):
            temp = listAllFile(tf, listSubDir)
            onlyfiles = onlyfiles + temp
    return onlyfiles


print('can only find *.POS file')
print('')
outputFile = open(sys.argv[2], 'w+')
for f in listAllFile(sys.argv[1], 1):
    if (re.search("\.POS$", f) != None or re.search("\.pos$", f) != None):
        print('process file ', f)
        inputData = open(f, 'r').read()
        temp = re.findall("[a-zA-Z1-9][a-zA-Z1-9-]+/[A-Z]+", inputData)
        outputFile.write("\n".join(temp) + "\n")
    else:
        print("no pos file in ", f)
outputFile.close()
