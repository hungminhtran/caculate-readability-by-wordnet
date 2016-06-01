import importlib
extractText = importlib.import_module("ExtractText")
mod1 = importlib.import_module("module-1")
import sys

def testFunc(PATH, debug=0):
    print('')
    for f in mod1.listAllFile(PATH, 1):
        temp = extractText.extractTextTEI(f, 1)
        print('[OK]', f)
        if (debug != 0):
            print(temp)
if __name__ == "__main__":
    if (len(sys.argv) > 1):
        PATH = sys.argv[1]
    if (len(sys.argv) > 2):
        DEBUG = int(sys.argv[2])
    else:
        PATH = 'data/testDataTEI'
        DEBUG = 0
    testFunc(PATH, DEBUG)
else:
    print("import test_ExtractText module sucessfully")
