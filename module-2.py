import importlib
mod1 = importlib.import_module("module-1")
from nltk.corpus import wordnet as wn
import nltk
import re

INPUT = 'data/easy.txt'
NOUNS = 'all-wordnet-nouns.txt'
# get input
inputData = open(INPUT, 'r').read()

# scan all nouns in text -> textNounsArray
#get all nouns to array
#check if noun in input: add space to first of input  to check (example -> ample)
nounsInput = []
nounsArray = open(NOUNS, 'r').read()
for noun in nounsArray.splitlines():
    if re.search(r'\b' + noun + r'\b', inputData):
        nounsInput.append(noun)
        re.sub(r'\b' + noun + r'\b', '', inputData)