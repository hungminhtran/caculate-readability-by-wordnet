import sys
import re
import importlib
mod1 = importlib.import_module("module-1")
#run command
#python get-nouns-and-label.py 'input/POS-nouns' 'output/POS-output.txt'

print('can only find *.POS file')
print('')
outputFile = open(sys.argv[2], 'w+')
for f in mod1.listAllFile(sys.argv[1], 1):
    if (re.search("\.POS$", f) != None):
        print('process file ', f)
        inputData = open(f, 'r').read()
        temp = re.findall("[a-zA-Z1-9]+/[A-Z]+", inputData)
        outputFile.write("\n".join(temp) + "\n")
    else:
        print("no pos file in ", f)
outputFile.close()
