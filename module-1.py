from nltk.corpus import wordnet as wn
from operator import add
import nltk
import re
import pickle
import datetime
import random

MAX_LEVEL = 6

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
def standanizeNoun(noun, isTEI=0):
    tnoun = noun.lower()
    tnoun = noun.replace(' ', '_')
    if (isTEI == 1):
        tnoun = wn.morphy(tnoun, wn.NOUN) # disable for vietnet
    return tnoun

def deStandanizeNoun(noun):
    # tnoun = wn.morphy(noun, wn.NOUN)
    tnoun = noun.lower()
    tnoun = tnoun.replace('_', ' ')
    return tnoun

#make . mean \.
def standandlizeNounsForInputRegex(noun):
    #puctuation = ['\!', '"', '\#', '\$', '\%', '\&', '\(', '\)', '\*', '\+', ',', '-', '\.', '/', ':', ';', '<', '=', '>', '\?', '\@', '\[', '\\', '\]', '\^', '_', '`', '\{', '\|', '\}', '\~']
    tnoun = noun.lower()
    # tnoun = re.sub("'", "_", tnoun)
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
    cpdByLvls[0] = -11
        #maximum is recurse 6 level
    if (level > MAX_LEVEL or not SynsetNoun):
        return [cpd, hyponym, total_lens, cpdByLvls]
    try:
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
    except:
        print('wtf ', SynsetNoun)
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
#return synsets if can get synsets
#return -1 if not a noun
def checkIfNounNGetSynsets(noun):
    temp = standanizeNoun(noun)
    temp = wn.synsets(temp)
    if (temp == []):
        print('Error checkIfNounNGetSynsets: cannot find', noun, 'in wordnet', '__',temp,'__')
        return -1
    temp = temp[0]
    if (re.search('\.n\.', temp.name()) == None):
        print('Error', temp, " is not a noun")
        return -1
    return temp

#input: noun
#output: true if noun is bacsic word, %cpd in direct hyponym and average len direct hyponyms - len(target word)
#
# word which ratio compounds > 25%
# average len direct hyponyms - len(target word) >=4
def isABacsicWord(noun, ENGLISH=0):
    noun = standanizeNoun(noun, ENGLISH)
    if (noun == None):
        print('Error isABacsicWord: standanizeNoun failed:', noun)
        return -1
    # try:
    temp = checkIfNounNGetSynsets(noun)
    if (str(temp) == str(-1)):
        return -1;
    (cpd, hyponym, total_lens, cpdByLvls) = cpdRatio(temp ,1, noun)
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
    # except:
    #     print('Error isABacsicWord: Error when processing noun:', noun + '__')
    #     return -1

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
def getStatisticsWithAllNouns(NOUNS, ouputFile, ENGLISH=0):
    nouns = open(NOUNS, 'r').read()
    nouns = nouns.splitlines()
    outputAllnouns = open(ouputFile[0], 'w+')
    outputAllbacsicLvlWord = open(ouputFile[1], 'w+')
    outputABLW = open(ouputFile[2], "w+")
    #for hashmap when neccessery
    # outputHashMap = open('hashmapKey.txt', 'w+')
    for i in range(0, len(nouns)):
        nouns[i] = nouns[i].lower()
        if nouns[i]:
            t = isABacsicWord(nouns[i], ENGLISH)
            if (t != -1):
                #for hashmap when neccessery
                # outputHashMap.write(nouns[i] + '\n')
                stringOut = nouns[i] + "," + str(t[1]) + '/' + str(t[2]) + ',' + str(t[3]) + ','
                xxx = nouns[i]
                for i in range(1, MAX_LEVEL+1):
                    stringOut = stringOut + str(t[4][i]) + ','
                outputAllnouns.write(stringOut + str(t[7]) + "\n")
                if t[0]:
                    outputABLW.write(xxx + "\n")
                    outputAllbacsicLvlWord.write(stringOut+ str(t[7]) + "\n")
            else:
                print('Error getStatisticsWithAllNouns: cannot process word:', nouns[i])
    outputAllnouns.close()
    outputAllbacsicLvlWord.close()
    outputABLW.close()
    #for hashmap when neccessery
    # outputHashMap.close()

#generate table 1
def generate_statistic_blw_with_hypernym_hyponym_table1(blwFile, outputFileT1, DEBUG=0):
    # open output file
    outputT1 = open(outputFileT1, 'w+')

    # read input data
    blwF = open(blwFile, 'r')
    blwArr = blwF.read().split('\n')
    blwF.close()

    def counterAndwrite(allHyp):
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
        # with hypernym
        tNoun = checkIfNounNGetSynsets(noun);
        if (str(tNoun) != str(-1)):
            allHypernyms = tNoun.hypernyms()
            if (DEBUG == 1):
                print('all hypernyms\n', allHypernyms)
            (wlHyper, nwlHyper, mcHyper) = counterAndwrite(allHypernyms)
            # with hyponym
            allHyponyms = tNoun.hyponyms()
            (wlHypo, nwlHypo, mcHypo) = counterAndwrite(allHyponyms)
            if (DEBUG == 1):
                print('all hyponyms\n', allHyponyms)

            # table 1 write down
            awlHypo = 0
            if (nwlHypo != 0):
                awlHypo = wlHypo/nwlHypo
            awlHyper = 0
            if (nwlHyper != 0):
                awlHyper = wlHyper/nwlHyper
            outputT1.write(deStandanizeNoun(noun) + ',' + str(len(noun)) + ',' + mcNoun + ',' + str(awlHyper) + ',' + str(len(allHypernyms)) + ','
            + " ".join(mcHyper) + ',' + str(awlHypo) + ',' + str(len(allHyponyms)) + ',' + " ".join(mcHypo) + '\n')
    outputT1.close()

def isInhashmapGENTABLE(hashmap, key):
    key = key.lower()
    if key in hashmap:
        return hashmap[key].split(',')
    else:
        print('Warning:',key,'not in hashmap')
        return (key + ',N/A,' + 'N/A,'*7 + 'N/A').split(',')
#generate table 2 in paper from data source
def generate_statistic_table2(inputFile, outputFile, allWNSTATIC="input/wn-nouns/all-wn-nouns-STATISTIC.txt", KeyHashFile = "input/wn-nouns/hashmapKey.txt", DEBUG=0):


    print('input file', inputFile)
    print('output file', outputFile)
    # create hashmap
    allWNSTATICArr = open(allWNSTATIC, 'r').read().split('\n')
    KeyHashArr = open(KeyHashFile, 'r').read().split('\n')
    hashmap = {}
    for i in range(len(allWNSTATICArr)):
        hashmap[KeyHashArr[i]] = allWNSTATICArr[i]
    print('total hashmap len: ', len(allWNSTATICArr))
    # read inputfile and writedown to outputfile
    inputArr = open(inputFile, 'r').read().split('\n')
    print('total input len:', len(inputArr))
    outputFp = open(outputFile, 'w+')
    for noun in inputArr:
        noun = noun.lower()
        nounOut = hyponymOut = hypernymOut = ("N/A,"*9 + "N/A").split(',')
        tNoun = checkIfNounNGetSynsets(noun);
        if (str(tNoun) != str(-1)):
            temp = tNoun.hypernyms()
            if (temp != []):
                hyperT = deStandanizeNoun(temp[0].lemmas()[0].name())
                hypernymOut = isInhashmapGENTABLE(hashmap, hyperT)
            else:
                print('Error generate_statistic_table2: : retrive hypernyms failure', noun + '__', temp)
            temp =  tNoun.hyponyms()
            if (temp != []):
                hypoT = deStandanizeNoun(temp[0].lemmas()[0].name())
                hyponymOut = isInhashmapGENTABLE(hashmap, hypoT)
            else:
                print('Error generate_statistic_table2: : retrive hyponyms failure', noun + '__', temp)
            # temp = deStandanizeNoun(tNoun.lemmas()[0].name())
            nounOut = isInhashmapGENTABLE(hashmap, noun)
            outputFp.write(",".join(hypernymOut[:9]) + "\n")
            outputFp.write(",".join(nounOut[:9]) + "\n")
            outputFp.write(",".join(hyponymOut[:9]) + "\n")
        else:
            print('Error: generate_statistic_table2 retrive from wordnet failure', noun, '__')
    outputFp.close()

def getKeyWithNoHNA(outputFile, allWNSTATIC="input/wn-nouns/all-wn-nouns-STATISTIC.txt", KeyHashFile = "input/wn-nouns/hashmapKey.txt", sourceNouns = "input/wn-nouns/hashmapKey.txt"):
    allWNSTATICArr = open(allWNSTATIC, 'r').read().split('\n')
    KeyHashArr = open(KeyHashFile, 'r').read().split('\n')
    hashmap = {}
    for i in range(len(allWNSTATICArr)):
        hashmap[KeyHashArr[i]] = allWNSTATICArr[i]
    sourceNounArr = open(sourceNouns, 'r').read().splitlines()
    output = open(outputFile, 'w+')
    for noun in sourceNounArr:
        noun = noun.lower()
        nounOut = hyponymOut = hypernymOut = ("N/A,"*9 + "N/A").split(',')
        tNoun = checkIfNounNGetSynsets(noun);
        if (str(tNoun) != str(-1)):
            temp = tNoun.hypernyms()
            if (temp != []):
                hyperT = deStandanizeNoun(temp[0].lemmas()[0].name())
                hypernymOut = isInhashmapGENTABLE(hashmap, hyperT)
                temp =  tNoun.hyponyms()
                if (temp != []):
                    hypoT = deStandanizeNoun(temp[0].lemmas()[0].name())
                    hyponymOut = isInhashmapGENTABLE(hashmap, hypoT)
                    nounOut = isInhashmapGENTABLE(hashmap, noun)
                    _tempNum = 0
                    _tempStr = ",".join(hypernymOut[:9])
                    _tempNum = _tempNum + _tempStr.find('N/A')
                    _tempStr = ",".join(nounOut[:9])
                    _tempNum = _tempNum + _tempStr.find('N/A')
                    _tempStr = ",".join(hyponymOut[:9])
                    _tempNum = _tempNum + _tempStr.find('N/A')                    
                    if (_tempNum < 0):
                        output.write(noun + '\n')
    output.close()

def generateList_K_sample(k, inputFile, outputFile):
    inputData = open(inputFile, 'r').read().splitlines()
    sample = random.sample(range(len(inputData)), k)
    sample.sort()
    output = open(outputFile, 'w+')
    for item in sample:
        output.write(inputData[item] + '\n')
    output.close()

def getWordInWordnet(table1File, outputFile):
    inputData = open(table1File).read().splitlines()
    output = open(outputFile, 'w+')
    for i in range(len(inputData)):
        output.write(inputData[i].split(',')[0] + '\n')
    output.close()

if __name__ == '__main__':
    import sys
    if sys.version_info[0] < 3:
        raise "Must be using Python 3"
    startTimeGlobal = datetime.datetime.now().time()
    print("start run at ", datetime.datetime.now().time())
    # print('gen blw')
    # getListOfNounsWithCompoundNounsFirst('input/blw-nouns/blw-nouns.txt', "input/blw-nouns/blw-SORTED-nouns.txt")
    # getStatisticsWithAllNouns("input/blw-nouns/blw-SORTED-nouns.txt", ["input/blw-nouns/all-blw-nouns-STATISTIC.txt",
    # "input/blw-nouns/all-blw-BLW-statistic.txt", "input/blw-nouns/all-blw-BLW.txt"], ENGLISH=1)
    # print('gen 3000-freq')
    # getListOfNounsWithCompoundNounsFirst('input/freq-nouns/3000-freq-word.txt', "input/freq-nouns/3000-freq-word-SORTED-nouns.txt")
    # getStatisticsWithAllNouns("input/freq-nouns/3000-freq-word-SORTED-nouns.txt", ["input/freq-nouns/3000-freq-nouns-STATISTIC.txt",
    # "input/freq-nouns/3000-freq-BLW-statistic.txt", "input/freq-nouns/3000-freq-BLW.txt"], ENGLISH=1)
    # print('pos ')
    # getListOfNounsWithCompoundNounsFirst('input/POS-nouns/all-3kPOS-nouns.txt', "input/POS-nouns/all-3kPOS-SORTED-nouns.txt")
    # getStatisticsWithAllNouns('input/POS-nouns/all-3kPOS-SORTED-nouns.txt', ["input/POS-nouns/all-3kPOS-nouns-STATISTIC.txt",
    # "input/POS-nouns/all-3kPOS-BLW-statistic.txt", "input/POS-nouns/all-3kPOS-BLW.txt"], ENGLISH=1)
    # print('gen wn')
    # getListOfNounsWithCompoundNounsFirst('input/wn-nouns/all-wn-nouns.txt', "input/wn-nouns/all-wn-SORTED-nouns.txt")
    # getStatisticsWithAllNouns('input/wn-nouns/all-wn-SORTED-nouns.txt', ["input/wn-nouns/all-wn-nouns-STATISTIC.txt",
    # "input/wn-nouns/all-wn-BLW-statistic.txt", "input/wn-nouns/all-wn-BLW.txt"], ENGLISH=1)

    # print('20 nouns')
    # getListOfNounsWithCompoundNounsFirst('input/20-nouns/20-nouns.txt', "input/20-nouns/all-20-SORTED-nouns.txt")
    # getStatisticsWithAllNouns('input/20-nouns/all-20-SORTED-nouns.txt', ["input/20-nouns/all-20-nouns-STATISTIC.txt",
    # "input/20-nouns/all-20-BLW-statistic.txt", "input/20-nouns/all-20-BLW.txt"], ENGLISH=1)

    # print("test table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/blw-nouns/blw-SORTED-nouns.txt',
    # 'output/test-3kPOS-table-1.csv', DEBUG=0)
    # print("blw table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/blw-nouns/blw-SORTED-nouns.txt',
    # 'output/blw-table-1.csv', DEBUG=0)
    # print("freq-nouns table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/freq-nouns/3000-freq-word-SORTED-nouns.txt', 'output/3kfreq-table-1.csv', DEBUG=0)
    # print("POS table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/POS-nouns/all-3kPOS-SORTED-nouns.txt', 'output/3kPOS-table-1.csv', DEBUG=0)
    # print("wn table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/wn-nouns/all-wn-SORTED-nouns.txt', 'output/wn-table-1.csv', DEBUG=0)
    # print("20 nouns table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/20-nouns/all-20-SORTED-nouns.txt', 'output/20-table-1.csv', DEBUG=0)
    
    # print('input/generator-20 table 1')
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/generator-20/3000-freq-word-SORTED-nouns-20.txt',
    # 'output/generate-20/3000-freq-word-SORTED-nouns-20-table-1.csv', DEBUG=0)
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/generator-20/all-3kPOS-SORTED-nouns-20.txt',
    # 'output/generate-20/all-3kPOS-SORTED-nouns-20-table-1.csv', DEBUG=0)
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/generator-20/blw-SORTED-nouns-20.txt',
    # 'output/generate-20/blw-SORTED-nouns-20-table-1.csv', DEBUG=0)
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/generator-20/wn-20-nouns.txt',
    # 'output/generate-20/wn-20-nouns-table-1.csv', DEBUG=0)

    # # print("test table 2")
    # # generate_statistic_table2('input/POS-nouns/all-3kPOS-SORTED-nouns.txt', 'output/test-3kPOS-table-2.csv', DEBUG=0)
    # print("blw table 2")
    # generate_statistic_table2('input/blw-nouns/blw-SORTED-nouns.txt', 'output/blw-table-2.csv', DEBUG=0)
    # print("freq table 2")
    # generate_statistic_table2('input/freq-nouns/3000-freq-word-SORTED-nouns.txt', 'output/3k-freq-table-2.csv', DEBUG=0)
    # print("3kPOS table 2")
    # generate_statistic_table2('input/POS-nouns/all-3kPOS-SORTED-nouns.txt', 'output/3kPOS-table-2.csv', DEBUG=0)
    # print("wn table 2")
    # generate_statistic_table2('input/wn-nouns/all-wn-SORTED-nouns.txt', 'output/wn-table-2.csv', DEBUG=0)
    # print("20 table 2")
    # generate_statistic_table2('input/20-nouns/all-20-SORTED-nouns.txt', 'output/20-table-2.csv', DEBUG=0)

    # print('input/generator-20 table 2')
    # generate_statistic_table2('input/generator-20/blw-SORTED-nouns-20.txt', 
    #     'output/generate-20/blw-SORTED-nouns-20-table-2.csv', DEBUG=0)
    # generate_statistic_table2('input/generator-20/all-3kPOS-SORTED-nouns-20.txt', 
    #     'output/generate-20/all-3kPOS-SORTED-nouns-20-table-2.csv', DEBUG=0)
    # generate_statistic_table2('input/generator-20/3000-freq-word-SORTED-nouns-20.txt', 
    #     'output/generate-20/3000-freq-word-SORTED-nouns-20-table-2.csv', DEBUG=0)
    # generate_statistic_table2('input/generator-20/wn-20-nouns.txt', 
    #     'output/generate-20/wn-20-nouns-table-2.csv', DEBUG=0)

    # getWordInWordnet('output/3kPOS-table-1.csv', 'input/POS-nouns/hashmapKey.txt')
    # getWordInWordnet('output/3kfreq-table-1.csv', 'input/freq-nouns/hashmapKey.txt')
    # getWordInWordnet('output/blw-table-1.csv', 'input/blw-nouns/hashmapKey.txt')

    # generateList_K_sample(30, 'input/POS-nouns/hashmapKey.txt', 'input/POS-nouns/(30)-all-3kPOS-SORTED-nouns.txt')
    # generateList_K_sample(30, 'input/blw-nouns/hashmapKey.txt', 'input/blw-nouns/(30)-blw-SORTED-nouns.txt')
    # generateList_K_sample(30, 'input/freq-nouns/hashmapKey.txt', 'input/freq-nouns/(30)-3000-freq-word-SORTED-nouns.txt')
    # generateList_K_sample(3000, 'input/wn-nouns/hashmapKey.txt', 'input/wn-nouns/(3000)-all-wn-SORTED-nouns.txt')
    # generateList_K_sample(30, 'input/wn-nouns/(3000)-all-wn-SORTED-nouns.txt', 'input/wn-nouns/(30)-all-wn-SORTED-nouns.txt')

    # print("30-blw table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/blw-nouns/(30)-blw-SORTED-nouns.txt',
    # 'output/generate-30-3k/(30)-blw-table-1.csv', DEBUG=0)
    # print("30-freq-nouns table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/freq-nouns/(30)-3000-freq-word-SORTED-nouns.txt',
    # 'output/generate-30-3k/(30)-3kfreq-table-1.csv', DEBUG=0)
    # print("30-POS table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/POS-nouns/(30)-all-3kPOS-SORTED-nouns.txt',
    # 'output/generate-30-3k/(30)-3kPOS-table-1.csv', DEBUG=0)
    # print("30-wn table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/wn-nouns/(30)-all-wn-SORTED-nouns.txt',
    # 'output/generate-30-3k/(30)-wn-table-1.csv', DEBUG=0)
    # print("3000-wn table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/wn-nouns/(3000)-all-wn-SORTED-nouns.txt',
    # 'output/generate-30-3k/(3000)-wn-table-1.csv', DEBUG=0)

    # print("30-blw table 2")
    # generate_statistic_table2('input/blw-nouns/(30)-blw-SORTED-nouns.txt', 'output/generate-30-3k/(30)-blw-table-2.csv', DEBUG=0)
    # print("30-freq table 2")
    # generate_statistic_table2('input/freq-nouns/(30)-3000-freq-word-SORTED-nouns.txt', 'output/generate-30-3k/(30)-3k-freq-table-2.csv', DEBUG=0)
    # print("30-3kPOS table 2")
    # generate_statistic_table2('input/POS-nouns/(30)-all-3kPOS-SORTED-nouns.txt', 'output/generate-30-3k/(30)-3kPOS-table-2.csv', DEBUG=0)
    # print("30-wn table 2")
    # generate_statistic_table2('input/wn-nouns/(30)-all-wn-SORTED-nouns.txt', 'output/generate-30-3k/(30)-wn-table-2.csv', DEBUG=0)
    # print("3000-wn table 2")
    # generate_statistic_table2('input/wn-nouns/(3000)-all-wn-SORTED-nouns.txt', 'output/generate-30-3k/(3000)-wn-table-2.csv', DEBUG=0)

    # getKeyWithNoHNA('input/wn-nouns/hashKeyNotNA.txt')
    # getKeyWithNoHNA('input/POS-nouns/hashKeyNotNA.txt', sourceNouns = 'input/POS-nouns/hashmapKey.txt')
    # getKeyWithNoHNA('input/blw-nouns/hashKeyNotNA.txt', sourceNouns = 'input/blw-nouns/hashmapKey.txt')
    # getKeyWithNoHNA('input/freq-nouns/hashKeyNotNA.txt', sourceNouns = 'input/freq-nouns/hashmapKey.txt')

    # generateList_K_sample(100, 'input/POS-nouns/hashKeyNotNA.txt', 'input/POS-nouns/(100)-all-3kPOS-SORTED-nouns.txt')
    # # generateList_K_sample(100, 'input/blw-nouns/hashKeyNotNA.txt', 'input/blw-nouns/(100)-blw-SORTED-nouns.txt')
    # generateList_K_sample(100, 'input/freq-nouns/hashKeyNotNA.txt', 'input/freq-nouns/(100)-3000-freq-word-SORTED-nouns.txt')
    # generateList_K_sample(100, 'input/wn-nouns/hashKeyNotNA.txt', 'input/wn-nouns/(100)-all-wn-SORTED-nouns.txt')


    # print("100-blw table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/blw-nouns/(100)-blw-SORTED-nouns.txt','output/generate-30-3k-60/(100)-blw-table-1.csv', DEBUG=0)
    # print("100-freq-nouns table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/freq-nouns/(100)-3000-freq-word-SORTED-nouns.txt',
    # 'output/generate-30-3k-60/(100)-3kfreq-table-1.csv', DEBUG=0)
    # print("100-POS table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/POS-nouns/(100)-all-3kPOS-SORTED-nouns.txt',
    # 'output/generate-30-3k-60/(100)-3kPOS-table-1.csv', DEBUG=0)
    # print("100-wn table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/wn-nouns/(100)-all-wn-SORTED-nouns.txt',
    # 'output/generate-30-3k-60/(100)-wn-table-1.csv', DEBUG=0)

    # # print("100-blw table 2")
    # # generate_statistic_table2('input/blw-nouns/(100)-blw-SORTED-nouns.txt', 'output/generate-30-3k-60/(100)-blw-table-2.csv', DEBUG=0)
    # print("100-freq table 2")
    # generate_statistic_table2('input/freq-nouns/(100)-3000-freq-word-SORTED-nouns.txt', 'output/generate-30-3k-60/(100)-3k-freq-table-2.csv', DEBUG=0)
    # print("100-3kPOS table 2")
    # generate_statistic_table2('input/POS-nouns/(100)-all-3kPOS-SORTED-nouns.txt', 'output/generate-30-3k-60/(100)-3kPOS-table-2.csv', DEBUG=0)
    # print("100-wn table 2")
    # generate_statistic_table2('input/wn-nouns/(100)-all-wn-SORTED-nouns.txt', 'output/generate-30-3k-60/(100)-wn-table-2.csv', DEBUG=0)

    print("gen vietnamesewn")
    from nltk.corpus import vietnet as wn

    # print('vietnamese wn')
    # getListOfNounsWithCompoundNounsFirst('input/vietnamesewn-nouns/all-vietnamesewn-nouns.txt'
    # , "input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt")
    # getStatisticsWithAllNouns('input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt'
    # , ["input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt"
    # , "input/vietnamesewn-nouns/all-vietnamesewn-BLW-statistic.txt", "input/vietnamesewn-nouns/all-vietnamesewn-BLW.txt"])
    
    # print('freq vietnamese')
    # getListOfNounsWithCompoundNounsFirst('input/vietnamese-freq-nouns/3000vietnamese-nouns.txt', "input/vietnamese-freq-nouns/3000vietnamese-freq-SORTED-nouns.txt")
    # getStatisticsWithAllNouns('input/vietnamese-freq-nouns/3000vietnamese-freq-SORTED-nouns.txt',
    # ["input/vietnamese-freq-nouns/3000vietnamese-freq-nouns-STATISTIC.txt",
    # "input/vietnamese-freq-nouns/3000vietnamese-freq-BLW-statistic.txt",
    # "input/vietnamese-freq-nouns/3000vietnamese-freq-BLW.txt"])
    # print('vietnamesePOS')
    # getListOfNounsWithCompoundNounsFirst('input/vietnamesePOS-nouns/3000-vietnamesePOS-nouns.txt'
    # , "input/vietnamesePOS-nouns/3000-vietnamesePOS-SORTED-nouns.txt")
    # getStatisticsWithAllNouns('input/vietnamesePOS-nouns/3000-vietnamesePOS-SORTED-nouns.txt',
    # ["input/vietnamesePOS-nouns/3000-vietnamesePOS-nouns-STATISTIC.txt",
    # "input/vietnamesePOS-nouns/3000-vietnamesePOS-BLW-statistic.txt",
    # "input/vietnamesePOS-nouns/3000-vietnamesePOS-BLW.txt"])

    # print("vietnamesewn nouns table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt',
    # 'output/vietnamesewn-table-1.csv', DEBUG=0)
    # print("3000vietnamese-freq nouns table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/vietnamese-freq-nouns/3000vietnamese-freq-SORTED-nouns.txt',
    # 'output/3000vietnamese-freq-table-1.csv', DEBUG=0)
    # print("3000vietnamesePOS nouns table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/vietnamesePOS-nouns/3000-vietnamesePOS-SORTED-nouns.txt',
    # 'output/3000-vietnamesePOS-table-1.csv', DEBUG=0)

    # print("vietnamesewn table 2")
    # generate_statistic_table2('input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt', 'output/vietnamesewn-table-2.csv',
    # allWNSTATIC='input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt',
    # KeyHashFile='input/vietnamesewn-nouns/hashmapKey.txt', DEBUG=0)
    # print("3000vietnamese-freq table 2")
    # generate_statistic_table2('input/vietnamese-freq-nouns/3000vietnamese-freq-SORTED-nouns.txt',
    # 'output/3000vietnamese-freq-table-2.csv', allWNSTATIC='input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt',
    # KeyHashFile='input/vietnamesewn-nouns/hashmapKey.txt', DEBUG=0)
    # print("3000vietnamese-POS table 2")
    # generate_statistic_table2('input/vietnamesePOS-nouns/3000-vietnamesePOS-SORTED-nouns.txt',
    # 'output/3000-vietnamesePOS-table-2.csv', allWNSTATIC='input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt',
    # KeyHashFile='input/vietnamesewn-nouns/hashmapKey.txt', DEBUG=0)

    # getWordInWordnet('output/3000-vietnamesePOS-table-1.csv', 'input/vietnamesePOS-nouns/hashmapKey.txt')
    # getWordInWordnet('output/3000vietnamese-freq-table-1.csv', 'input/vietnamese-freq-nouns/hashmapKey.txt')

    # generateList_K_sample(30, 'input/vietnamese-freq-nouns/hashmapKey.txt', 'input/vietnamese-freq-nouns/(30)-3000vietnamese-freq-SORTED-nouns.txt')
    # generateList_K_sample(30, 'input/vietnamesePOS-nouns/hashmapKey.txt', 'input/vietnamesePOS-nouns/(30)-3000-vietnamesePOS-SORTED-nouns.txt')
    # generateList_K_sample(3000, 'input/vietnamesewn-nouns/hashmapKey.txt', 'input/vietnamesewn-nouns/(3000)-all-vietnamesewn-SORTED-nouns.txt')
    # generateList_K_sample(30, 'input/vietnamesewn-nouns/(3000)-all-vietnamesewn-SORTED-nouns.txt', 'input/vietnamesewn-nouns/(30)-all-vietnamesewn-SORTED-nouns.txt')

    # print("(30)-3000vietnamese-freq nouns table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/vietnamese-freq-nouns/(30)-3000vietnamese-freq-SORTED-nouns.txt',
    # 'output/generate-30-3k/(30)-3000vietnamese-freq-table-1.csv', DEBUG=0)
    # print("(30)-3000vietnamesePOS nouns table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/vietnamesePOS-nouns/(30)-3000-vietnamesePOS-SORTED-nouns.txt',
    # 'output/generate-30-3k/(30)-3000-vietnamesePOS-table-1.csv', DEBUG=0)
    # print("(3000)-vietnamesewn nouns table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/vietnamesewn-nouns/(3000)-all-vietnamesewn-SORTED-nouns.txt',
    # 'output/generate-30-3k/(3000)-vietnamesewn-table-1.csv', DEBUG=0)
    # print("(30)-vietnamesewn nouns table 1")
    # generate_statistic_blw_with_hypernym_hyponym_table1('input/vietnamesewn-nouns/(30)-all-vietnamesewn-SORTED-nouns.txt',
    # 'output/generate-30-3k/(30)-vietnamesewn-table-1.csv', DEBUG=0)

    # print("(30)-3000vietnamese-freq table 2")
    # generate_statistic_table2('input/vietnamese-freq-nouns/(30)-3000vietnamese-freq-SORTED-nouns.txt',
    # 'output/generate-30-3k/(30)-3000vietnamese-freq-table-2.csv', allWNSTATIC='input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt',
    # KeyHashFile='input/vietnamesewn-nouns/hashmapKey.txt', DEBUG=0)
    # print("(30)-3000vietnamese-POS table 2")
    # generate_statistic_table2('input/vietnamesePOS-nouns/(30)-3000-vietnamesePOS-SORTED-nouns.txt',
    # 'output/generate-30-3k/(30)-3000-vietnamesePOS-table-2.csv', allWNSTATIC='input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt',
    # KeyHashFile='input/vietnamesewn-nouns/hashmapKey.txt', DEBUG=0)
    # print("(30)-vietnamesewn table 2")
    # generate_statistic_table2('input/vietnamesewn-nouns/(30)-all-vietnamesewn-SORTED-nouns.txt', 'output/generate-30-3k/(30)-vietnamesewn-table-2.csv',
    # allWNSTATIC='input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt',
    # KeyHashFile='input/vietnamesewn-nouns/hashmapKey.txt', DEBUG=0)
    # print("(3000)-vietnamesewn table 2")
    # generate_statistic_table2('input/vietnamesewn-nouns/(3000)-all-vietnamesewn-SORTED-nouns.txt', 'output/generate-30-3k/(3000)-vietnamesewn-table-2.csv',
    # allWNSTATIC='input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt',
    # KeyHashFile='input/vietnamesewn-nouns/hashmapKey.txt', DEBUG=0)

    getKeyWithNoHNA('input/vietnamese-freq-nouns/hashKeyNotNA.txt', allWNSTATIC="input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt", KeyHashFile = "input/vietnamesewn-nouns/hashmapKey.txt", sourceNouns = 'input/vietnamese-freq-nouns/hashmapKey.txt')
    getKeyWithNoHNA('input/vietnamesePOS-nouns/hashKeyNotNA.txt', allWNSTATIC="input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt", KeyHashFile = "input/vietnamesewn-nouns/hashmapKey.txt", sourceNouns = 'input/vietnamesePOS-nouns/hashmapKey.txt')
    getKeyWithNoHNA('input/vietnamesewn-nouns/hashKeyNotNA.txt', allWNSTATIC="input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt", KeyHashFile = "input/vietnamesewn-nouns/hashmapKey.txt", sourceNouns = 'input/vietnamesewn-nouns/hashmapKey.txt')

    print('generate ramdom 100')
    generateList_K_sample(100, 'input/vietnamese-freq-nouns/hashKeyNotNA.txt', 'input/vietnamese-freq-nouns/(100)-3000vietnamese-freq-SORTED-nouns.txt')
    generateList_K_sample(100, 'input/vietnamesePOS-nouns/hashKeyNotNA.txt', 'input/vietnamesePOS-nouns/(100)-3000-vietnamesePOS-SORTED-nouns.txt')
    generateList_K_sample(100, 'input/vietnamesewn-nouns/hashKeyNotNA.txt', 'input/vietnamesewn-nouns/(100)-all-vietnamesewn-SORTED-nouns.txt')

    print('generate ramdom 1-0 table 1')
    generate_statistic_blw_with_hypernym_hyponym_table1('input/vietnamese-freq-nouns/(100)-3000vietnamese-freq-SORTED-nouns.txt',
    'output/generate-30-3k-60/(100)-3000vietnamese-freq-table-1.csv', DEBUG=0)
    print("(30)-3000vietnamesePOS nouns table 1")
    generate_statistic_blw_with_hypernym_hyponym_table1('input/vietnamesePOS-nouns/(100)-3000-vietnamesePOS-SORTED-nouns.txt',
    'output/generate-30-3k-60/(100)-3000-vietnamesePOS-table-1.csv', DEBUG=0)
    print("(3000)-vietnamesewn nouns table 1")
    generate_statistic_blw_with_hypernym_hyponym_table1('input/vietnamesewn-nouns/(100)-all-vietnamesewn-SORTED-nouns.txt',
    'output/generate-30-3k-60/(100)-vietnamesewn-table-1.csv', DEBUG=0)    

    print('generate ramdom 100 table 2')
    generate_statistic_table2('input/vietnamese-freq-nouns/(100)-3000vietnamese-freq-SORTED-nouns.txt',
    'output/generate-30-3k-60/(100)-3000vietnamese-freq-table-2.csv', allWNSTATIC='input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt',
    KeyHashFile='input/vietnamesewn-nouns/hashmapKey.txt', DEBUG=0)
    print("(30)-3000vietnamese-POS table 2")
    generate_statistic_table2('input/vietnamesePOS-nouns/(100)-3000-vietnamesePOS-SORTED-nouns.txt',
    'output/generate-30-3k-60/(100)-3000-vietnamesePOS-table-2.csv', allWNSTATIC='input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt',
    KeyHashFile='input/vietnamesewn-nouns/hashmapKey.txt', DEBUG=0)
    print("(30)-vietnamesewn table 2")
    generate_statistic_table2('input/vietnamesewn-nouns/(100)-all-vietnamesewn-SORTED-nouns.txt', 'output/generate-30-3k-60/(100)-vietnamesewn-table-2.csv',allWNSTATIC='input/vietnamesewn-nouns/all-vietnamesewn-nouns-STATISTIC.txt',KeyHashFile='input/vietnamesewn-nouns/hashmapKey.txt', DEBUG=0)

    print("end run time: ", datetime.datetime.now().time())
else:
    print('import module-1 sucessfully')
