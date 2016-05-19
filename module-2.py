import importlib
mod1 = importlib.import_module("module-1")
from nltk.corpus import wordnet as wn
import nltk
import re

def findAllItemFromArray(inputData, searchData, printForDeBug = 0):
    result = []
    inputData = mod1.standandlizeNounsForInputRegex(inputData)
    for i  in range(len(searchData)):
        #for plural nouns
        tempT = [r"\b" + mod1.standanlizeNounsForSearchRegex(searchData[i]) + 's' + r"\b", r"\b" + mod1.standanlizeNounsForSearchRegex(searchData[i]) + r"\b"]
        for j in range(len(tempT)):
            inputData, isFinOut = re.subn(tempT[j], ' ', inputData) #avoid concat string can be created new noun
            if (isFinOut > 0):
                result.append(searchData[i])
                if (printForDeBug == 1):
                    print tempT[j]
                    print inputData
    result = set(result)
    if (printForDeBug):
        print "doc after re.sub all things:"
        print inputData
        print result
    return result

def calculateReabilityByWordnetForEnglish(INPUT, BLW_NOUNS, NOUNS, printForDeBug=0):
    import time;
    startTime = time.time();

    # get input
    inputFile = open(INPUT, 'r')
    inputData = inputFile.read()
    inputData = inputData.lower()
    print inputData
    inputFile.close()

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
        print "no BLW"
    else:
        print "ratio: ", float(len(nounsBLWInput))/len(nounsInput)*100, "%"
    print "blw:"
    print nounsBLWInput
    print "all nouns:"
    print nounsInput
    print "time cost: ", time.time() - startTime

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

# calculateReabilityByWordnetForEnglish('data/_testData.txt','all-BLW.txt','all-SORTED-wordnet-nouns.txt', 1)
for f in listAllFile('data', 1):
    print f
    calculateReabilityByWordnetForEnglish(f,'all-BLW.txt','all-SORTED-wordnet-nouns.txt')
    print ''
