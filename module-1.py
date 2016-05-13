from nltk.corpus import wordnet as wn
from operator import add
import nltk
import re
import pickle

MAX_LEVEL = 6

#input: noun
#output: standardized noun
def standanizeNoun(noun):
    tnoun = noun.replace(' ', '_')
    tnoun = wn.morphy(tnoun, wn.NOUN)
    return tnoun
def standandlizeNounsForRegex(noun):
    tnoun = noun.replace('.', '\.')
    return tnoun

#compound ration of a word / hyponym
#input: noun
#output: (cpd, hyponym, total_hyponym_len)
#
# which each nouns, get all hypernym/hyponyms (6 levels max)
#     --> given a word, calculate number of compounds in full_hypornym
def cpdRatio(SynsetNoun, level, hypernymName):
#    print level,SynsetNoun.name()
    cpd = 0
    hyponym = 0
    total_lens = 0
    cpdByLvls = [0] * (MAX_LEVEL + 1)
        #maximum is recurse 6 level
    if (level > MAX_LEVEL or not SynsetNoun):
        return cpd, hyponym, total_lens, cpdByLvls

    allHyponyms = SynsetNoun.hyponyms() #why we choose this?
    if (allHyponyms == []):
        return cpd, hyponym, total_lens, cpdByLvls
    for synset in allHyponyms:
        for lemma in synset.lemmas():
            hyponym = hyponym + 1
            #use sandalizeNounsForRegex to avoid . in some nouns like a.e can be understand '.' in regex
            if re.search(standandlizeNounsForRegex(hypernymName), lemma.name()): #noun in cpd hyponym, don't care whole word???
                cpd = cpd + 1
                cpdByLvls[level] = cpdByLvls[level] + 1 #count cpd in current level
            total_lens = total_lens + len(lemma.name())
#            print level, SynsetNoun.hyponyms()[0].name(), lemma.name()
            # total_lens = total_lens - synset.name().count('_') #remove space from len counter
        if synset.lemmas()[0]:
            # print cpdRatio(synset, level+1, hypernymName)
            tmp1, tmp2, tmp3, tmp4 = cpdRatio(synset, level+1, hypernymName)
            cpd = cpd + tmp1
            hyponym = hyponym + tmp2
            total_lens = total_lens + tmp3
            cpdByLvls = map(add, cpdByLvls, tmp4)
    #return result
    return cpd, hyponym, total_lens, cpdByLvls

# testNoun = ['guitar', 'apples', 'piano', 'drum', 'peach', 'grape', 'hammer', 'saw', 'screwdriver', 'pants', 'paper']
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


#input: noun
#output: true if noun is bacsic word, %cpd in direct hyponym and average len direct hyponyms - len(target word)
#
# word which ratio compounds > 25%
# average len direct hyponyms - len(target word) >=4
def isABacsicWord(noun):
    noun = standanizeNoun(noun)
    if (noun == None):
        return -1
    cpd, hyponym, total_lens, cpdByLvls = cpdRatio(wn.synsets(noun)[0],1, noun)
    # cpd, hyponym, total_lens, cpdByLvls = cpdRatio(wn.synsets('guitar')[0],1, 'guitar')
    if hyponym > 0:
        t0 = int(round(float(cpd)*100/hyponym + 0.5)) #floor, not round
        t1 = int(round(float(total_lens)/hyponym + 0.5))
        t2 = abs(-len(noun) + t1)
    else:
        t0 = t1 = t2 = 'N/A'
    if hyponym and t0 >= 25 and t2 >= 4:
        return True, cpd, hyponym, t0, cpdByLvls, len(noun), t1, t2
    else:
        return False, cpd, hyponym, t0, cpdByLvls, len(noun), t1, t2

#input: string a, b
#output: return true if a has more space (#32 in ASCII) than b, else return false
def compareFunc(a, b):
    return a.count(" ") - b.count(" ")

#input: nouns file path, nouns file path after sorted
#output: nouns file after sort
def getListOfNounsWithCompoundNounsFirst(NOUNS, SORTED_NOUNS):
    nounsArray = open(NOUNS, 'r').read()
    # testNoun = ['g uitar', 'piano', 'd r u m', 'p e a c h', 'gra pe', 'h a mmer', 'sa    w', 'screw d river', 'pants', 'paper']
    # result = quickSort(testNoun, compareFunc)
    # print result
    result = quickSort(nounsArray.splitlines(), compareFunc)
    output = open(SORTED_NOUNS, 'w+')
    for i in range(0, len(result)):
        output.write(result[i] + "\n")
    output.close()
# getListOfNounsWithCompoundNounsFirst('all-wordnet-nouns.txt', "all-SORTED-wordnet-nouns.txt")

#2 output file: all nouns with statistic, all basic level word
def getStatisticsWithAllNouns(NOUNS, ouputFile):
    nouns = open(NOUNS, 'r').read()
    nouns = nouns.splitlines()
    outputAllnouns = open(ouputFile[0], 'w+')
    outputAllbacsicLvlWord = open(ouputFile[1], 'w+')
    outputABLW = open(ouputFile[2], "w+")
    for i in range(0, len(nouns)):
        if nouns[i]:
            t = isABacsicWord(nouns[i])
            if (t != -1):
                stringOut = nouns[i] + "," + str(t[1]) + '/' + str(t[2]) + ',' + str(t[3]) + ','
                xxx = nouns[i]
                for i in range(0, MAX_LEVEL):
                    stringOut = stringOut + str(t[4][i]) + ','
                outputAllnouns.write(stringOut + str(t[7]) + "\n")
                if t[0]:
                    outputABLW.write(xxx + "\n")
                    outputAllbacsicLvlWord.write(stringOut+ str(t[7]) + "\n")
    outputAllnouns.close()
    outputAllbacsicLvlWord.close()
    outputABLW.close()

getStatisticsWithAllNouns('all-SORTED-wordnet-nouns.txt', ["all-nouns-STATISTIC.txt", "all-BLW-statistic.txt", "all-BLW.txt"])