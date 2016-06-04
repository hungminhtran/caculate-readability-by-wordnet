import importlib
extractText = importlib.import_module("ExtractText")
mod1 = importlib.import_module("module-1")
import sys

def testFunc(PATH, debug=0, TEI = 1):
    print('')
    for f in mod1.listAllFile(PATH, 1):
        temp = extractText.extractTextTEI(f, TEI)
        print('[OK]', f)
        if (debug != 0):
            print(temp)
if __name__ == "__main__":
    if (len(sys.argv) > 1):
        PATH = sys.argv[1]
    if (len(sys.argv) > 2):
        DEBUG = int(sys.argv[2])
    if (len(sys.argv) > 3):
        ISTEI = int(sys.argv[3])
    else:
        PATH = 'data/testDataTEI'
        DEBUG = 0
        ISTEI = 1
    testFunc(PATH, DEBUG, ISTEI)
else:
    print("import test_ExtractText module sucessfully")
