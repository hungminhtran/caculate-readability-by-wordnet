import importlib
mod1 = importlib.import_module("module-1")
from nltk.corpus import wordnet as wn
import nltk
import re

def findAllItemFromArray(inputData, searchData):
	result = []
	for noun in searchData:
	    # if re.search(r'\b' + noun + r'\b', inputData):
	    #     result.append(noun)
	    #     re.sub(r'\b' + noun + r'\b', '', inputData)
	    if re.search(r''+noun, inputData):
	        result.append(noun)
	        re.sub(r''+noun, '', inputData)
	return result

INPUT = 'data/easy.txt'
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
