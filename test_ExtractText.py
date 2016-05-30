import importlib
def testFunc(PATH):
    extractText = importlib.import_module("ExtractText")
    mod1 = importlib.import_module("module-1")
    for f in mod1.listAllFile(PATH, 1):
        print(f)
        extractText.extractTextTEI(f, 1)
        print('')
if __name__ == "__main__":
    PATH = 'data/testDataTEI'
    testFunc(PATH)
else:
    print("import test_ExtractText module sucessfully")
