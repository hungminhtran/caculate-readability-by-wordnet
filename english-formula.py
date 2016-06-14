# command line
# python english-formula.py data/English\ Textbook\ 4\ Readability\ Level output/ET4RL-formula.csv
from __future__ import print_function
import sys
print('work on python 2 only')
if (sys.version_info[0] > 2):
    raise "Must be using Python 2"
from textstat.textstat import textstat
import importlib
mod1 = importlib.import_module("module-1")
extractText = importlib.import_module("ExtractText")
from multiprocessing import Queue, Pool
import time
TOTAL_WORKER = 1

def calculate2FormulaFromFile(inputFile, isTEI=1):
    inputData = extractText.extractTextTEI(inputFile, isTEI)
    try:
        r1 = textstat.flesch_kincaid_grade(inputData)
    except:
        print('ERROR: cannot calculate flesch_kincaid_grade for ', inputFile)
        r1 = -1
    try:
        r2 = textstat.dale_chall_readability_score(inputData)
    except:
        print('ERROR: cannot calculate dale_chall_readability_score for ', inputFile)
        r2 = -1
    return (inputFile, r1, r2)

if (__name__ == '__main__'):
    FILEPATH = sys.argv[1]
    OUTPUTFILE = sys.argv[2]
    startTime = time.time()
    files = mod1.listAllFile(FILEPATH, 1)
    result = []
    # with Pool(TOTAL_WORKER) as p:
        # result = p.map(calculate2FormulaFromFile, files)
    for file in files:
        result.append(calculate2FormulaFromFile(file))
    outputFile = open(OUTPUTFILE, 'w+')
    outputFile.write('file, flesch_kincaid_grade, dale_chall_readability_score\n')
    for item in result:
        outputFile.write(item[0] + ',' + str(item[1]) + ',' + str(item[2]) + '\n')
    outputFile.close()
    print('total worker: ', TOTAL_WORKER, 'cost: ', time.time() - startTime)