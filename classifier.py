# coding=UTF-8
import importlib
mod1 = importlib.import_module("module-1")
import re
import time
import datetime
from multiprocessing import Process, Lock, Array, Queue
'''
file: filepath, ratio, blw, all nouns
dict: word - log(freq)
'''
def getFreqWordsForFileFromDict(inputDataFromFileInRow, row, dictData, dictFreq, labelKWs):
    totalWords = 0
    result = []
    for i in range(len(dictData)):
        word = dictData[i].split('\t')[0]
        # temp = r"\b" + word + r"\b"
        # temp = re.findall(temp, inputDataFromFileInRow)
        # result.append(len(temp))
        # totalWords = totalWords + len(temp)
        temp = float(inputDataFromFileInRow.count(word))
        result.append(temp)
        totalWords = totalWords + temp
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
def getDataNFeatureFromFile(outputFile, file, labelKWs, dictFile='data/TanSoTu.txt', keyword=['Vietnamese_by_catalog', 'ppVietnamese_by_catalog']):
    inputData = open(file, 'r').read().splitlines()
    dictFreq = []
    dictData = open(dictFile, 'r').read().splitlines()
    for i in range(len(dictData)):
        dictFreq.append(float(dictData[i].split('\t')[1]))
    X = []
    TOTAL_FILE = len(inputData)
    for i in range(1, len(inputData)):
        try:
            row = inputData[i]
            row = row.split(',')
            row[0] = re.sub(keyword[0], keyword[1], row[0])
            print(i*100.0/TOTAL_FILE, 'processing ', row[0], 'at', datetime.datetime.now().time())
            inputDataFromFileInRow = open(row[0], 'r', ).read().lower()
            temp = getFreqWordsForFileFromDict(inputDataFromFileInRow, row, dictData, dictFreq, labelKWs)
            X.append(temp)
        except:
            print("ERROR: " + row[0] + " can not open!")
    fileX = open(outputFile, 'w+')
    for i in range(len(X)):
        fileX.write(' '.join(map(lambda x: str(x), X[i])) + '\n')
    fileX.close()
    return X

if __name__ == '__main__':
    START_TIME = time.time()
    import sys
    if not sys.version_info[0] < 3:
        raise "Must be using Python 2"
    # getFreqWordsForFileFromDict(['data/ppVietnamese_by_catalog/Easy/ct24/ct24 (100).txt',12.35,3, 4], 'data/TanSoTu.txt')
    # getDataNFeatureFromFile('test_data.txt', 'output/test_Vietnamese_output_classifier.csv', 'test')
    # X3 = getDataNFeatureFromFile('Difficult_data.txt', 'output/vietnamesewn_Difficult_output.csv', 3)
    # X1 = getDataNFeatureFromFile('Easy_data.txt','output/vietnamesewn_Easy_output.csv', 1)
    # X2 = getDataNFeatureFromFile('Normal_data.txt','output/vietnamesewn_Normal_output.csv', 2)
    getDataNFeatureFromFile(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])