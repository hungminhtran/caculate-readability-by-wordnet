import importlib
mod1 = importlib.import_module("module-1")
from nltk.corpus import wordnet as wn
import nltk
import re

#result to compare: Are their true?
#
#easy text:   ratio:  39.1304347826 % ['can', 'cold', 'hold', 'orange', 'plain', 'potato', 's', 'vinegar', 'well']
#medium text: ratio:  28.0          % ['course', 'culture', 'mean', 'right', 's', 'technology', 'trade']
#hard text:   ratio:  24.2424242424 % ['barometer', 'call', 'office', 'out', 'perfect', 'street', 'system', 'well']

def standandlizeNounsForSearch(noun):
    tnoun = noun.replace('.', '\.')
    return tnoun

def findAllItemFromArray(inputData, searchData):
    result = []
    # complile first to make runtime faster when using too many time
    # prog = re.compile(pattern)
    # result = prog.match(string)
    for noun in searchData:
        temp = r"\b" + standandlizeNounsForSearch(noun) + r"\b"
        inputData, isFinOut = re.subn(temp, ' ', inputData) #avoid concat string can be created new noun
        if (isFinOut > 0):
            result.append(noun)
            print temp
            print inputData
    print "doc after re.sub all things:"
    print inputData
    return result

def calculateReabilityByWordnet(INPUT, BLW_NOUNS, NOUNS):
    import time;
    startTime = time.time();

    # get input
    inputFile = open(INPUT, 'r')
    inputData = inputFile.read()
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
    nounsBLWInput = findAllItemFromArray(tmp, BLWnounsArray.splitlines())
    # tmp = inputData
    nounsInput = findAllItemFromArray(tmp, NounsArray.splitlines())
    if (len(nounsInput) == 0):
        print "no BLW"
    else:
        print "ratio: ", float(len(nounsBLWInput))/len(nounsInput)*100, "%"
    print "blw:"
    print nounsBLWInput
    print "all nouns:"
    print nounsInput
    print "time cost: ", time.time() - startTime

calculateReabilityByWordnet('data/medium.txt','all-BLW.txt','all-SORTED-wordnet-nouns.txt')