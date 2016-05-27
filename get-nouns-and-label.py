import importlib
import sys
import re
#run command
#python get-nouns-and-label.py 'input/POS-nouns' 'output/POS-output.txt'

mod1 = importlib.import_module("module-1")
outputFile = open(sys.argv[2], 'w+')
for f in mod1.listAllFile(sys.argv[1], 1):
    print 'process file ', f
    inputData = open(f, 'r').read()
    temp = re.findall("[a-zA-Z1-9]+/[A-Z]+", inputData)
    outputFile.write("\n".join(temp) + "\n")
    print ''
outputFile.close()
