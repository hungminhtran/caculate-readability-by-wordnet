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
# which each nouns, get all hypernym/hyponyms (6 levels max)
#     --> given a word, calculate number of compounds in full_hypornym -> get all hypernym/hypornym -> calculate again
# select all word which ratio compounds > 25%
# direct hyponyms - len(target word) >=4
for noun in nounsInput:
    noun = mod1.standanizeNoun(noun)
    cpd, hyponym, total_lens = mod1.cpdRatio(wn.synsets(noun)[0],1, noun)
    if hyponym and (int(round(float(cpd)*100/hyponym)) >= 25 and int(round(float(total_lens)/hyponym))>= 4):
        #multiple form of noun
        print noun, int(round(float(cpd)*100/hyponym)), len(noun), int(round(float(total_lens)/hyponym))
    # if hyponym:
    #     print noun, int(round(float(cpd)*100/hyponym)), len(noun), int(round(float(total_lens)/hyponym))
# calculate this ratio
