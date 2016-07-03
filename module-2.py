import importlib
mod1 = importlib.import_module("module-1")
extractText = importlib.import_module("ExtractText")
import nltk
from nltk.tokenize import word_tokenize
import re

def findAllItemFromArray(inputData, searchData, printForDeBug = 0, isTEI = 1):
    if (isTEI == 1):
        result = []
        inputData = mod1.standandlizeNounsForInputRegex(inputData)
        tokenInputData = word_tokenize(inputData)
        for i in range(len(tokenInputData)):
            tokenInputData[i] =  mod1.standanizeNoun(tokenInputData[i])
        tokenInputDataSet = set(tokenInputData)
        searchDataSet = set(searchData)
        result = list(tokenInputDataSet.intersection(searchDataSet))
        result.sort()
        return result
    else:
        result = []
        inputData = mod1.standandlizeNounsForInputRegex(inputData)
        for searchPattern  in searchData:
            tempT = r"\b" + mod1.standanlizeNounsForSearchRegex(mod1.standanizeNoun(searchPattern)) + r"\b"
            isFindOut = re.search(tempT, inputData)
            if (isFindOut != None):
                result.append(searchPattern)
        result = list(set(result))
        result.sort()
        return result

def calculateReabilityByWordnetForEnglish(INPUT, BLWnounsArray, NounsArray, printForDeBug=0, isTEI=0):
    # get input
    inputData = extractText.extractTextTEI(INPUT, isTEI)
    inputData = inputData.lower()
    #get all nouns
    nounsInput = findAllItemFromArray(inputData[:], NounsArray, printForDeBug, isTEI)
    #get all blw
    nounsSet = set(nounsInput)
    blwSet = set(BLWnounsArray)
    nounsBLWInput = list(nounsSet.intersection(blwSet))
    nounsBLWInput.sort()
    if (len(nounsInput) == 0):
        # if (printForDeBug):
        #     print("no BLW")
        return 0, nounsInput, nounsInput
    else:
        # if (printForDeBug):
        #     print("ratio: ", float(len(nounsBLWInput))/len(nounsInput)*100, "%")
        #     print("blw:")
        #     print(nounsBLWInput)
        #     print("all nouns:")
        #     print(nounsInput)
        return float(len(nounsBLWInput))/len(nounsInput)*100, nounsBLWInput, nounsInput
        
if __name__ == '__main__':
    import sys
    if sys.version_info[0] < 3:
        raise "Must be using Python 3"
    #a.e. bug
    FILEPATH = 'data/testDataNM'
    files = mod1.listAllFile(FILEPATH, 1)
    #get all BLW
    inputFile= open('input/wn-nouns/all-wn-BLW.txt', 'r')
    BLWnounsArray = inputFile.read()
    BLWnounsArray = BLWnounsArray.splitlines()
    inputFile.close()

    #get all nouns
    inputFile= open('input/wn-nouns/all-wn-SORTED-nouns.txt', 'r')
    NounsArray = inputFile.read()
    NounsArray = NounsArray.splitlines()
    inputFile.close()
    for f in files:
        print(calculateReabilityByWordnetForEnglish(f, BLWnounsArray, NounsArray, 0, 0))
else:
    print('import module-2 sucessfully')
