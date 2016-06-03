import importlib
mod1 = importlib.import_module("module-1")
extractText = importlib.import_module("ExtractText")
from nltk.corpus import wordnet as wn
import nltk
import re

def findAllItemFromArray(inputData, searchData, printForDeBug = 0):
    result = []
    inputData = mod1.standandlizeNounsForInputRegex(inputData)
    for i  in range(len(searchData)):
        #for plural nouns
        #re.search("[ ^ ]{0,1}we[ s]", 'we ')
        tempT = [r"\b" + mod1.standanlizeNounsForSearchRegex(searchData[i]) + '[s]{0,1}' + r"\b"]
        for j in range(len(tempT)):
            inputData, isFinOut = re.subn(tempT[j], ' ', inputData) #avoid concat string can be created new noun
            if (isFinOut > 0):
                result.append(searchData[i])
                if (printForDeBug == 1):
                    print(tempT[j])
                    print(inputData)
    result.sort()
    result = set(result)
    if (printForDeBug):
        print("doc after re.sub all things:")
        print(inputData)
        print(result)
    return result

def calculateReabilityByWordnetForEnglish(INPUT, BLW_NOUNS, NOUNS, printForDeBug=0, isTEI=0):
    # get input
    inputData = extractText.extractTextTEI(INPUT, isTEI)
    inputData = inputData.lower()

    #get all BLW
    inputFile= open(BLW_NOUNS, 'r')
    BLWnounsArray = inputFile.read()
    inputFile.close()

    #get all nouns
    inputFile= open(NOUNS, 'r')
    NounsArray = inputFile.read()
    inputFile.close()

    tmp = inputData
    nounsBLWInput = findAllItemFromArray(tmp, BLWnounsArray.splitlines(), printForDeBug)
    # tmp = inputData
    nounsInput = findAllItemFromArray(tmp, NounsArray.splitlines(), printForDeBug)

    if (len(nounsInput) == 0):
        if (printForDeBug):
            print("no BLW")
        return None
    else:
        if (printForDeBug):
            print("ratio: ", float(len(nounsBLWInput))/len(nounsInput)*100, "%")
            print("blw:")
            print(nounsBLWInput)
            print("all nouns:")
            print(nounsInput)
        return float(len(nounsBLWInput))/len(nounsInput)*100, nounsBLWInput, nounsInput
if __name__ == '__main__':
    import sys
    if sys.version_info[0] < 3:
        raise "Must be using Python 3"
    #a.e. bug
    FILEPATH = 'data/testDataNM'
    files = mod1.listAllFile(FILEPATH, 1)
    for f in files:
        print(calculateReabilityByWordnetForEnglish(f,'input/wn-nouns/all-wn-BLW.txt','input/wn-nouns/all-wn-SORTED-nouns.txt', 0, 0))
else:
    print('import module-2 sucessfully')
