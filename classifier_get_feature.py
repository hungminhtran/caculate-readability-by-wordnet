# coding=UTF-8
import importlib
mod1 = importlib.import_module("module-1")
vfm = importlib.import_module("vietnamese-formula-module")
import re
import time
import datetime
from multiprocessing import Process, Lock, Array, Queue
MAX_PROCESS = 4

def getFreqWordsForFileFromDict(inputDataFromFileInRow, row, funcArgs):
    dictData = funcArgs[0]
    dictFreq = funcArgs[1]
    labelKWs = funcArgs[2]
    totalWords = 0
    result = []
    for i in range(len(dictData)):
        word = dictData[i].split('\t')[0]
        temp = r"\b" + word + r"\b"
        temp = re.findall(temp, inputDataFromFileInRow)
        # if (len(temp) > 0):
        #     print(row[0], temp[0], len(temp))
        result.append(len(temp))
        totalWords = totalWords + len(temp)
    if (totalWords > 0):
        for i in range(len(result)):
            result[i] = result[i] / float(totalWords)
    result = result + [float(row[1])]
    # return dictFreq + result + [labelKWs]
    return result + [labelKWs]

def getShallowFeatureForFile(inputDataFromFileInRow, row, funcArgs):
    labelKWs = funcArgs[0]
    hashMapFileCount3kWords = funcArgs[1]
    paragraph = inputDataFromFileInRow.splitlines()
    totalSentences = 0
    totalSentences =len(paragraph)
    totalWords = inputDataFromFileInRow.count(' ') 
    punctuations = '“”‘’!()-[]{};:\'\"\\,<>./?@#$^&*~'
    # punctuations = [',', '.', '?']
    for p in punctuations:
        totalWords = totalWords - inputDataFromFileInRow.count(p)
    hashmapVietnameseCharCount = {}
    for i in range(len(vfm.vietnameseCountChar)):
        hashmapVietnameseCharCount[vfm.vietnameseChar[i]] = vfm.vietnameseCountChar[i]
    totalLetter = 0
    for sentence in paragraph:
        if (len(sentence) > 0):
            for c in sentence:
                if (c in hashmapVietnameseCharCount):
                    totalLetter = totalLetter + hashmapVietnameseCharCount[c]
            # totalSentences = totalSentences + 1
    if (totalSentences > 0 and totalWords > 0):
        # return [float(totalWords)/totalSentences, totalSentences, totalWords, totalLetter, row[0], float(totalLetter)/totalSentences, float(totalLetter)/totalWords, float(row[1]), labelKWs]
        return [float(hashMapFileCount3kWords[row[0]])/totalWords, float(totalWords)/totalSentences, float(totalLetter)/totalSentences, float(totalLetter)/totalWords, float(row[1]), labelKWs]
    # else:
    #     return [-1, -1, -1, float(row[1]), labelKWs]

def getDataNFeatureFromFileForAProc(PROCESS_LOCK, RESULT_QUEUE, filesQueue, subProcFunc, funcArgs):
    X = []
    while (1):
        PROCESS_LOCK.acquire()
        #check if queue is empty
        if filesQueue.empty():
            PROCESS_LOCK.release()
            break
        else:
            row = filesQueue.get()
            PROCESS_LOCK.release()
        try:
        # if (1):
            PROCESS_LOCK.acquire()
            print(filesQueue.qsize(), 'processing', row[0], 'at', datetime.datetime.now().time())
            PROCESS_LOCK.release()
            _tempfile = open(row[0], 'r', )
            inputDataFromFileInRow = _tempfile.read().lower()
            _tempfile.close()
            # temp = getFreqWordsForFileFromDict(inputDataFromFileInRow, row, funcArgs[0], funcArgs[1], funcArgs[2])
            temp = subProcFunc(inputDataFromFileInRow, row, funcArgs)
            RESULT_QUEUE.put(temp)
            #print(row[0], temp)
        except:
            PROCESS_LOCK.acquire()
            print("ERROR: " + row[0] + " can not process file. File not found or bug in code!")
            PROCESS_LOCK.release()
    RESULT_QUEUE.put('EOP')

def writeOutResult(RESULT_QUEUE, outputFile):
    print('output file', outputFile)
    isEndWriteOut = MAX_PROCESS
    _tempfile = open(outputFile, 'w+')
    while (isEndWriteOut > 0):
        temp = RESULT_QUEUE.get()
        if (temp == 'EOP'):
            isEndWriteOut = isEndWriteOut - 1
        else:
            _tempfile.write(' '.join(map(lambda x: str(x), temp)) + '\n')
        while (RESULT_QUEUE.empty() and isEndWriteOut > 0):
            time.sleep(1)
    _tempfile.close()

def getFeatureMultiprocessing(subProcFunc, blwFile, outputFile, funcArgs, keyword=['Vietnamese_by_catalog', 'ppVietnamese_by_catalog']):
    START_TIME = time.time()
    # getFreqWordsForFileFromDict(['data/ppVietnamese_by_catalog/Easy/ct24/ct24 (100).txt',12.35,3, 4], 'data/TanSoTu.txt')
    # getDataNFeatureFromFile('test_data.txt', 'output/test_Vietnamese_output_classifier.csv', 'test')
    # X3 = getDataNFeatureFromFile('Difficult_data.txt', 'output/vietnamesewn_Difficult_output.csv', 3)
    # X1 = getDataNFeatureFromFile('Easy_data.txt','output/vietnamesewn_Easy_output.csv', 1)
    # X2 = getDataNFeatureFromFile('Normal_data.txt','output/vietnamesewn_Normal_output.csv', 2)
    _tempfile = open(blwFile, 'r')
    temp = _tempfile.read().splitlines()
    _tempfile.close()
    filesQueue = Queue()
    RESULT_QUEUE = Queue()
    for i in range(1, len(temp)):
            temp[i] = temp[i].split(',')
            temp[i][0] = re.sub(keyword[0], keyword[1], temp[i][0])
            if not keyword[0] == '' and (not temp[i][0].find(keyword[-1]) > 0):
                print('[ERROR] processing ', temp[i][0])
                print('sub', keyword[0], keyword[-1], re.sub(keyword[0], keyword[-1], temp[i][0]))
                return
            filesQueue.put(temp[i])
    PROCESS_LOCK = Lock()
    myProcess = []
    for processID in range(MAX_PROCESS):
        myProcess.append(Process(target=getDataNFeatureFromFileForAProc, args=(PROCESS_LOCK, RESULT_QUEUE, filesQueue, subProcFunc, funcArgs)))
    myProcess.append(Process(target=writeOutResult, args=(RESULT_QUEUE, outputFile)))

    for _process in myProcess:
        _process.start()
    for _process in myProcess:
        _process.join()
    print('total runtime:', time.time() - START_TIME)

def getFreqFeatureFromFile(outputFile, blwFile, labelKWs, dictFile='data/TanSoTu.txt'):
    dictFreq = []
    _tempfile = open(dictFile, 'r')
    dictData = _tempfile.read().splitlines()
    _tempfile.close()
    for i in range(len(dictData)):
        dictFreq.append(float(dictData[i].split('\t')[1]))
    funcArgs = [dictData, dictFreq, labelKWs]
    getFeatureMultiprocessing(getFreqWordsForFileFromDict, blwFile, outputFile, funcArgs)

def getShallowFeatureFromFile(outputFile, blwFile, labelKWs, _3kFreqInDoc, _kw):
    hashMapFileCount3kWords = {}
    _tempfile = open(_3kFreqInDoc, 'r')
    _3kFreqInDoc = _tempfile.read().splitlines()
    _tempfile.close()
    for i in range(1,len(_3kFreqInDoc)):
        temp = _3kFreqInDoc[i].split(',')
        hashMapFileCount3kWords[re.sub(_kw[0], _kw[1], temp[0])] = float(temp[-1].split(' | ')[-1])
    # print(hashMapFileCount3kWords)
    funcArgs = [labelKWs, hashMapFileCount3kWords]
    getFeatureMultiprocessing(getShallowFeatureForFile, blwFile, outputFile, funcArgs, _kw)

if __name__ == '__main__':
    import sys
    if not sys.version_info[0] > 2:
        raise "Must be using Python 3"
    # getFreqFeatureFromFile(sys.argv[1],sys.argv[2], sys.argv[3], sys.argv[4])
    getShallowFeatureFromFile(sys.argv[1],sys.argv[2], sys.argv[3], sys.argv[4], [sys.argv[5], sys.argv[6]])