# coding=UTF-8
import importlib
mod1 = importlib.import_module("module-1")
import re
import time
import datetime
from multiprocessing import Process, Lock, Array, Queue
MAX_PROCESS = 4

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
        #     print(temp[0], len(temp))
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
            X.append(temp)
        except:
            PROCESS_LOCK.acquire()
            print("ERROR: " + row[0] + " can not open!")
            PROCESS_LOCK.release()
    PROCESS_LOCK.acquire()
    RESULT_QUEUE.put(X)
    PROCESS_LOCK.release()

if __name__ == '__main__':
    START_TIME = time.time()
    import sys
    if not sys.version_info[0] < 4:
        raise "Must be using Python 2"
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
        #                                   getDataNFeatureFromFile(PROCESS_LOCK, RESULT_QUEUE, filesQueue, outputFile, labelKWs, dictFile='data/TanSoTu.txt', keyword=['Vietnamese_by_catalog', 'ppVietnamese_by_catalog']):
        myProcess.append(Process(target=getDataNFeatureFromFile, args=(PROCESS_LOCK, RESULT_QUEUE, filesQueue, sys.argv[3], sys.argv[4])))
    result = []
    for _process in myProcess:
        _process.start()
    for _process in myProcess:
        _process.join()
    result = []
    while (not RESULT_QUEUE.empty()):
        result = result + RESULT_QUEUE.get()
    _tempfile = open(sys.argv[1], 'w+')
    for i in range(len(result)):
        _tempfile.write(' '.join(map(lambda x: str(x), result[i])) + '\n')
    _tempfile.close()
    print('total runtime:', time.time() - START_TIME)