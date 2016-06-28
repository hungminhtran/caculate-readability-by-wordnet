# coding=UTF-8
import importlib
mod1 = importlib.import_module("module-1")
import re
import time
import datetime
from multiprocessing import Process, Lock, Array, Queue
MAX_PROCESS = 1

'''
file: filepath, ratio, blw, all nouns
dict: word - log(freq)
'''
def getFreqWordsForFileFromDict(inputDataFromFileInRow, row, dictData, dictFreq, labelKWs):
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

'''
file: output file when calc blw/ all nouns
outputFile: write down result
keyword: change path to preprocessing data
label: label of this dataset
'''
def getDataNFeatureFromFile(PROCESS_LOCK, RESULT_QUEUE, filesQueue, labelKWs, dictFile='data/TanSoTu.txt', keyword=['Vietnamese_by_catalog', 'ppVietnamese_by_catalog']):
    PROCESS_LOCK.acquire()
    dictFreq = []
    _tempfile = open(dictFile, 'r') 
    dictData = _tempfile.read().splitlines()
    _tempfile.close()
    PROCESS_LOCK.release()
    for i in range(len(dictData)):
        dictFreq.append(float(dictData[i].split('\t')[1]))
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
            row = row.split(',')
            row[0] = re.sub(keyword[0], keyword[1], row[0])
            PROCESS_LOCK.acquire()
            print(filesQueue.qsize(), 'processing', row[0], 'at', datetime.datetime.now().time())
            PROCESS_LOCK.release()
            _tempfile = open(row[0], 'r', )
            inputDataFromFileInRow = _tempfile.read().lower()
            _tempfile.close()
            temp = getFreqWordsForFileFromDict(inputDataFromFileInRow, row, dictData, dictFreq, labelKWs)
            RESULT_QUEUE.put(temp)
            #print(row[0], temp)
        except:
            PROCESS_LOCK.acquire()
            print("ERROR: " + row[0] + " can not open!")
            PROCESS_LOCK.release()
    RESULT_QUEUE.put('EOP')

def writeOutResult(RESULT_QUEUE, outputFile):
    print('output file', outputFile)
    isEndWriteOut = MAX_PROCESS
    _tempfile = open(sys.argv[1], 'w+')
    while (isEndWriteOut):
        time.sleep(2)   
        temp = RESULT_QUEUE.get()
        if (temp == 'EOP'):
            isEndWriteOut = isEndWriteOut - 1
        else:
            _tempfile.write(' '.join(map(lambda x: str(x), temp)) + '\n')
    _tempfile.close()

if __name__ == '__main__':
    START_TIME = time.time()
    import sys
    if not sys.version_info[0] > 2:
        raise "Must be using Python 3"
    # getFreqWordsForFileFromDict(['data/ppVietnamese_by_catalog/Easy/ct24/ct24 (100).txt',12.35,3, 4], 'data/TanSoTu.txt')
    # getDataNFeatureFromFile('test_data.txt', 'output/test_Vietnamese_output_classifier.csv', 'test')
    # X3 = getDataNFeatureFromFile('Difficult_data.txt', 'output/vietnamesewn_Difficult_output.csv', 3)
    # X1 = getDataNFeatureFromFile('Easy_data.txt','output/vietnamesewn_Easy_output.csv', 1)
    # X2 = getDataNFeatureFromFile('Normal_data.txt','output/vietnamesewn_Normal_output.csv', 2)
    _tempfile = open(sys.argv[2], 'r')
    temp = _tempfile.read().splitlines()
    _tempfile.close()
    filesQueue = Queue()
    RESULT_QUEUE = Queue()
    for i in range(1, len(temp)):
            filesQueue.put(temp[i])
    PROCESS_LOCK = Lock()
    myProcess = []
    for processID in range(MAX_PROCESS):
        myProcess.append(Process(target=getDataNFeatureFromFile, args=(PROCESS_LOCK, RESULT_QUEUE, filesQueue, sys.argv[3], sys.argv[4])))
    myProcess.append(Process(target=writeOutResult, args=(RESULT_QUEUE, sys.argv[1])))

    for _process in myProcess:
        _process.start()
    for _process in myProcess:
        _process.join()
    print('total runtime:', time.time() - START_TIME)
