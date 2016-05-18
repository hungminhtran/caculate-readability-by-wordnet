import importlib
mod1 = importlib.import_module("module-1")
from nltk.corpus import wordnet as wn
import nltk
import re

#need filter for 've, 't, ? ~ -, _

def findAllItemFromArray(inputData, searchData):
    result = []
    inputData = " " + inputData
    inputData = mod1.standandlizeNounsForInputRegex(inputData)
    print inputData
    for noun in searchData:
        if (noun not in "".join(result)): #remove some conflit data
            temp = " " + mod1.standanlizeNounsForSearchRegex(noun) + "[ 's]"
            if (re.search(temp, inputData)):
                result.append(noun)
    return result

# #return position data in array
# def binarySearchForArray(data, array, compareFunc):
#     if (len(array) == 0):
#         return -1;
#     mid = len(array)/2
#     if (compareFunc(data, array[n]) == 0):
#         return mid
#     if (compareFunc(data, array[n]) == 1):
#         binarySearchForArray(data, array[n+1:len(array)], compareFunc)
#     else:
#         binarySearchForArray(data, array[0:n-1], compareFunc)

# def findItemFromArrayUserBS(inputData, searchData, printForDeBug=0, compareFunc=None):
#     result = []
#     temp = inputData.split(" ")
#     for j in range(11):
#         for i in range(len(temp) - j):
#             if (binarySearchForArray(temp[i:i+j], searchData, compareFunc) > -1):
#                 result.append(temp[i:i+j])

# findItemFromArrayUserBS("what the hell are you doing What do you want from me", ["what", "the", "fuck"])

def calculateReabilityByWordnetForEnglish(INPUT, BLW_NOUNS, NOUNS):
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
calculateReabilityByWordnetForEnglish('./data/_testData.txt','all-BLW.txt','all-SORTED-wordnet-nouns.txt')
# for f in listAllFile('data', 1):
#     print f
#     calculateReabilityByWordnetForEnglish(f,'all-BLW.txt','all-SORTED-wordnet-nouns.txt')
#     print ''
