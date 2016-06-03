from nltk.corpus import wordnet as wn
from operator import add
import nltk
import re
import pickle
import datetime

MAX_LEVEL = 6
EMPTY_TABLE2_LINE = ",,,,,,,,,\n"

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

#input: noun
#output: standardized noun
def standanizeNoun(noun):
    tnoun = noun.replace(' ', '_')
    # tnoun = wn.morphy(tnoun, wn.NOUN) # disable for vietnet
    return tnoun

def deStandanizeNoun(noun):
    # tnoun = wn.morphy(noun, wn.NOUN)
    tnoun = noun.replace('_', ' ')
    return tnoun

#make . mean \.
def standandlizeNounsForInputRegex(noun):
    #puctuation = ['\!', '"', '\#', '\$', '\%', '\&', '\(', '\)', '\*', '\+', ',', '-', '\.', '/', ':', ';', '<', '=', '>', '\?', '\@', '\[', '\\', '\]', '\^', '_', '`', '\{', '\|', '\}', '\~']
    tnoun = re.sub("'", "'__", noun)
    tnoun = tnoun.lower()
    return tnoun

def standanlizeNounsForSearchRegex(noun):
    tnoun = noun
    tnoun = re.sub(r'\.', '\.', noun)
    tnoun = tnoun.lower()
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
        return [cpd, hyponym, total_lens, cpdByLvls]

    allHyponyms = SynsetNoun.hyponyms()
    if (allHyponyms == []):
        return [cpd, hyponym, total_lens, cpdByLvls]
    for synset in allHyponyms:
        for lemma in synset.lemmas():
            hyponym = hyponym + 1
            #use sandalizeNounsForRegex to avoid . in some nouns like a.e can be understand '.' in regex
            if re.search(standanlizeNounsForSearchRegex(hypernymName), lemma.name()): #noun in cpd hyponym, don't care whole word???
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
            cpdByLvls = list(map(add, cpdByLvls, tmp4))
    #return result
    return [cpd, hyponym, total_lens, cpdByLvls]

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
        print('Error isABacsicWord: standanizeNoun failed:', noun)
        return -1
    # print('synset is being process: ',wn.synsets(noun))
    try:
        cpd, hyponym, total_lens, cpdByLvls = cpdRatio(wn.synsets(noun)[0],1, noun)
        # cpd, hyponym, total_lens, cpdByLvls = cpdRatio(wn.synsets('guitar')[0],1, 'guitar')
        if hyponym > 0:
            t0 = int(round(float(cpd)*100/hyponym + 0.5)) #floor, not round
            t1 = int(round(float(total_lens)/hyponym + 0.5))
            t2 = abs(-len(noun) + t1)
        else:
            t0 = t1 = t2 = 'N/A'
        if hyponym and t0 >= 25 and t2 >= 4:
            return [True, cpd, hyponym, t0, cpdByLvls, len(noun), t1, t2]
        else:
            return [False, cpd, hyponym, t0, cpdByLvls, len(noun), t1, t2]
    except:
        print('Error isABacsicWord: noun is not found when get synset:', noun)
        return -1

#input: string a, b
#output: return true if a has more space (#32 in ASCII) than b, else return false
def compareFunc(a, b):
    result =  a.count(" ") - b.count(" ")
    if (result == 0):
        if (a.find("-") >= 0 or a.find("/") >= 0 or a.find(".") >= 0):
            if (b.find("-") >= 0 or b.find("/") >= 0 or b.find(".") >= 0):
                result = len(a) - len(b)
            else:
                result = 1
        else:
            if (b.find("-") >= 0 or b.find("/") >= 0 or b.find(".") >= 0):
                result = -1
            else:
                result = len(a) - len(b)
    return result

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

#2 output file: all nouns with statistic, all basic level word
def getStatisticsWithAllNouns(NOUNS, ouputFile):
    nouns = open(NOUNS, 'r').read()
    nouns = nouns.splitlines()
    outputAllnouns = open(ouputFile[0], 'w+')
    outputAllbacsicLvlWord = open(ouputFile[1], 'w+')
    outputABLW = open(ouputFile[2], "w+")
    for i in range(0, len(nouns)):
        nouns[i] = nouns[i].lower()
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
            else:
                print('Error getStatisticsWithAllNouns: cannot process noun:', nouns[i])
    outputAllnouns.close()
    outputAllbacsicLvlWord.close()
    outputABLW.close()

#generate table 1, 2
def generate_statistic_blw_with_hypernym_hyponym(blwFile, allNounsStatisticfile, outputFileT1, outputFileT2, DEBUG=0):
    # open output file
    outputT1 = open(outputFileT1, 'w+')
    outputT2 = open(outputFileT2, 'w+')

    # read input data
    blwF = open(blwFile, 'r')
    blwArr = blwF.read().split('\n')
    blwF.close()

    allNounsStatisticF = open(allNounsStatisticfile, 'r')
    allNounsStatisticStream = allNounsStatisticF.read()
    allNounsStatisticF.close()

    def searchDatT2(temp):
        temp = deStandanizeNoun(temp)
        nounbak = temp
        if (DEBUG == 1):
            print('search ', temp)
        temp = re.search(r"^" + temp.lower() + ",.*\n", allNounsStatisticStream, re.M)
        if (temp == None):
            print("****", datetime.datetime.now().time(), "Error: None type when search ", nounbak)
            return 'N/A\n'
        return temp.group()

    def counterAndwrite(allHyp, outputT2):
        wlHyp = 0
        nwlHyp = 0
        mcHyp = ['', '']
        for synset in allHyp:
            wlHyp = wlHyp + synset.name().find('.') - synset.name().count('_') #table 1
            nwlHyp = nwlHyp + 1 #table 1
            if (synset.name().find('_') > -1):
                mcHyp[1] = 'B'
            else:
                mcHyp[0] = 'A'
            for lemma in synset.lemmas():
                if (lemma.name() != None):
                    outputT2.write(searchDatT2(lemma.name()))
        return [wlHyp, nwlHyp, mcHyp]

    # process
    if (DEBUG == 1):
        blwArr = ['guitar', 'apple', 'bus']
    for noun in blwArr[:]:
        noun = noun.lower()
        noun = standanizeNoun(noun)
        if (noun == None):
            return -1

        mcNoun = 'A'
        if (noun.find('_') > -1):
            mcNoun = 'B'
        if (DEBUG == 1):
            print('noun is ', noun)
        outputT2.write(EMPTY_TABLE2_LINE)
        outputT2.write(EMPTY_TABLE2_LINE)
        # with hypernym
        #table 2
        try:
            allHypernyms = wn.synsets(noun)[0].hypernyms()
        except:
            print('Error generate_statistic_blw_with_hypernym_hyponym: can not get hyppernyms: ', noun)
            allHypernyms = []
        if (DEBUG == 1):
            print('all hypernyms\n', allHypernyms)
        (wlHyper, nwlHyper, mcHyper) = counterAndwrite(allHypernyms, outputT2)
        #write noun down
        outputT2.write(EMPTY_TABLE2_LINE)
        outputT2.write(searchDatT2(noun))
        outputT2.write(EMPTY_TABLE2_LINE)
        # with hyponym
        #table 2
        try:
            allHyponyms = wn.synsets(noun)[0].hyponyms()
        except:
            print('Error generate_statistic_blw_with_hypernym_hyponym: can not get hypponyms: ', noun)
            allHyponyms = []
        (wlHypo, nwlHypo, mcHypo) = counterAndwrite(allHyponyms, outputT2)
        if (DEBUG == 1):
            print('all hyponyms\n', allHyponyms)

        # table 1 write down
        awlHypo = 0
        if (nwlHypo != 0):
            awlHypo = wlHypo/nwlHypo
        awlHyper = 0
        if (nwlHyper != 0):
            awlHyper = wlHyper/nwlHyper
        outputT1.write(str(len(noun)) + ',' + mcNoun + ',' + str(awlHyper) + ',' + str(len(allHypernyms)) + ','
        + " ".join(mcHyper) + ',' + str(awlHypo) + ',' + str(len(allHyponyms)) + ',' + " ".join(mcHypo) + '\n')

    outputT1.close()
    outputT2.close()

if __name__ == '__main__':
    import sys
    if sys.version_info[0] < 3:
        raise "Must be using Python 3"
    print("start run at ", datetime.datetime.now().time())
    print('gen blw')
    getListOfNounsWithCompoundNounsFirst('input/blw-nouns/blw-nouns.txt', "input/blw-nouns/blw-SORTED-nouns.txt")
    getStatisticsWithAllNouns("input/blw-nouns/blw-SORTED-nouns.txt", ["input/blw-nouns/all-blw-nouns-STATISTIC.txt",
    "input/blw-nouns/all-blw-BLW-statistic.txt", "input/blw-nouns/all-blw-BLW.txt"])
    print('gen wn')
    getListOfNounsWithCompoundNounsFirst('input/wn-nouns/all-wn-nouns.txt', "input/wn-nouns/all-wn-SORTED-nouns.txt")
    getStatisticsWithAllNouns('input/wn-nouns/all-wn-SORTED-nouns.txt', ["input/wn-nouns/all-wn-nouns-STATISTIC.txt",
    "input/wn-nouns/all-wn-BLW-statistic.txt", "input/wn-nouns/all-wn-BLW.txt"])
    print('gen 3000-freq')
    getStatisticsWithAllNouns('input/freq-nouns/3000-freq-word-SORTED.txt', ["input/freq-nouns/3000-freq-nouns-STATISTIC.txt",
    "input/freq-nouns/3000-freq-BLW-statistic.txt", "input/freq-nouns/3000-freq-BLW.txt"])
    print('t1, t2 blw')
    generate_statistic_blw_with_hypernym_hyponym('input/blw-nouns/all-blw-BLW.txt', 'input/wn-nouns/all-wn-nouns-STATISTIC.txt',
    'output/blw-table-1.csv', 'output/blw-table-2.csv', DEBUG=0)
    print('t1, t2 wn')
    generate_statistic_blw_with_hypernym_hyponym('input/wn-nouns/all-wn-BLW.txt', 'input/wn-nouns/all-wn-nouns-STATISTIC.txt',
    'output/wn-table-1.csv', 'output/wn-table-2.csv', DEBUG=0)
    print('t1, t2 3000-freq')
    generate_statistic_blw_with_hypernym_hyponym('input/freq-nouns/3000-freq-BLW.txt', 'input/wn-nouns/all-wn-nouns-STATISTIC.txt',
    'output/300-freq-table-1.csv', 'output/300-freq-table-2.csv', DEBUG=0)
    print("gen vietnamesewn")
    from nltk.corpus import vietnet as wn
    getListOfNounsWithCompoundNounsFirst('input/vietnamesewn-nouns/all-vietnamesewn-nouns.txt'
    , "input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt")
    getStatisticsWithAllNouns('input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt'
    , ["input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt"
    , "input/vietnamesewn-nouns/all-vietnamesewn-BLW-statistic.txt", "input/vietnamesewn-nouns/all-vietnamesewn-BLW.txt"])
    generate_statistic_blw_with_hypernym_hyponym('input/vietnamesewn-nouns/all-vietnamesewn-BLW.txt'
    , 'input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt','output/vietnamesewn-table-1.csv'
    , 'output/vietnamesewn-table-2.csv', DEBUG=0)
    print("end run at ", datetime.datetime.now().time())
else:
    print('import module-1 sucessfully')
