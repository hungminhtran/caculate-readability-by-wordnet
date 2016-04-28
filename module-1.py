from nltk.corpus import wordnet as wn
import nltk
import re
import pickle

def standanizeNoun(noun):
    #standardize noun
    tnoun = noun.replace(' ', '_')
    tnoun = wn.morphy(tnoun, wn.NOUN)
    return tnoun

#compound ration of a word / hyponym
#input: noun
#output: (cpd, hyponym, total_hyponym_len)
def cpdRatio(SynsetNoun, level, hypernymName):
    #maximum is recurse 6 level
    if (level > 6):
        return 0, 0, 0
    if (not SynsetNoun):
        return 0, 0, 0
#    print level,SynsetNoun.name()
    cpd = 0
    hyponym = 0
    total_lens = 0
    allHyponyms = SynsetNoun.hyponyms() #why we choose this?
    if (allHyponyms == []):
        return 0, 0, 0
    for synset in allHyponyms:
        for lemma in synset.lemmas():
            hyponym = hyponym + 1
            if re.search(hypernymName, lemma.name()): #noun in cpd hyponym, don't care whole word???
                cpd = cpd + 1
            total_lens = total_lens + len(lemma.name())
#            print level, SynsetNoun.hyponyms()[0].name(), lemma.name()
            if synset.name().find('_'):
                total_lens = total_lens -1 #remove space from len counter
        if synset.lemmas()[0]:
            tmp1, tmp2, tmp3 = cpdRatio(synset, level+1, hypernymName)
            cpd = cpd + tmp1
            hyponym = hyponym + tmp2
            total_lens = total_lens + tmp3
    #return result
    return cpd, hyponym, total_lens

#testNoun = ['guitar', 'apples', 'piano', 'drum', 'peach', 'grape', 'hammer', 'saw', 'screwdriver', 'pants', 'paper']
# for noun in testNoun:
#     noun = standanizeNoun(noun)
#     print noun, cpdRatio(wn.synsets(noun)[0],1, noun)

#input: array and compare function
#output: a sorted array
def quickSort(arr, compareFunc):
    if (len(arr)<=1):
        return arr
    pivot = arr[0]
    left, right, equal = [], [], []
    for i in arr:
        if compareFunc(i, pivot) > 0:
            left.append(i)
        elif compareFunc(i, pivot) == 0:
            equal.append(i)
        else:
            right.append(i)
    return quickSort(left, compareFunc) + equal + quickSort(right, compareFunc)

#input: string a, b
#output: return true if a has more space (#32 in ASCII) than b, else return false
def compareFunc(a, b):
    return a.count(" ") - b.count(" ")

###should pick up by pickle
#input: nouns file path, nouns file path after sorted
#output: nouns file after sort
def getListOfNounsWithCompoundNounsFirst(NOUNS, SORTED_NOUNS):
    nounsArray = open(NOUNS, 'r').read()
    # testNoun = ['g ui tar', 'ap ples', 'piano', 'd r u m', 'p e a c h ', 'gra pe', 'h a mmer', 'sa       w', 'screw d river', 'pants', 'pap er']
    # result = quickSort(testNoun, compareFunc)
    # print result
    result = quickSort(nounsArray.splitlines(), compareFunc)
    output = open(SORTED_NOUNS, 'w+')
    pickle.dump(result, output)
    output.close()

getListOfNounsWithCompoundNounsFirst('all-wordnet-nouns.txt', "all-wordnet-nouns-SORTED.txt")

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
