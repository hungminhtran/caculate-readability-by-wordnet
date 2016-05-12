import importlib
mod1 = importlib.import_module("module-1")
from nltk.corpus import wordnet as wn
import nltk
import re

#result to compare:
#easy text:   ratio:  39.1304347826 % ['can', 'cold', 'hold', 'orange', 'plain', 'potato', 's', 'vinegar', 'well']
#medium text: ratio:  28.0          % ['course', 'culture', 'mean', 'right', 's', 'technology', 'trade']
#hard text:   ratio:  24.2424242424 % ['barometer', 'call', 'office', 'out', 'perfect', 'street', 'system', 'well']
def findAllItemFromArray(inputData, searchData):
    result = []
    # complile first to make runtime faster when using too many time
    # prog = re.compile(pattern)
    # result = prog.match(string)
    for noun in searchData:
        temp = r'\b' + noun + r'\b'
        if (re.search(temp, inputData) != None):
            result.append(noun)
            print temp
            # re.sub(r'\b' + noun + r'\b', ' ', inputData) #avoid concat string can be created new noun
        # if inputData.find(noun) > -1: # faster
    return result

INPUT = 'data/medium.txt'
BLW_NOUNS = 'all-BLW.txt'
NOUNS = 'all-SORTED-wordnet-nouns.txt'
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
# print nounsBLWInput
# print nounsInput
print "ratio: ", float(len(nounsBLWInput))/len(nounsInput)*100, "%"
print "blw:"
print nounsBLWInput
print "all nouns:"
print nounsInput
print inputData
print re.search(inputData, '/bre/b')