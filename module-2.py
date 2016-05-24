import importlib
mod1 = importlib.import_module("module-1")
extractText = importlib.import_module("ExtractText")
from nltk.corpus import wordnet as wn
import nltk
import re
import time
import sys
from multiprocessing import Process, Lock, Array

def findAllItemFromArray(inputData, searchData, printForDeBug = 0):
    result = []
    inputData = mod1.standandlizeNounsForInputRegex(inputData)
    for i  in range(len(searchData)):
        #for plural nouns
        tempT = [r"\b" + mod1.standanlizeNounsForSearchRegex(searchData[i]) + 's' + r"\b", r"\b" + mod1.standanlizeNounsForSearchRegex(searchData[i]) + r"\b"]
        for j in range(len(tempT)):
            inputData, isFinOut = re.subn(tempT[j], ' ', inputData) #avoid concat string can be created new noun
            if (isFinOut > 0):
                result.append(searchData[i])
                if (printForDeBug == 1):
                    print tempT[j]
                    print inputData
    result = set(result)
    if (printForDeBug):
        print "doc after re.sub all things:"
        print inputData
        print result
    return result

def calculateReabilityByWordnetForEnglish(INPUT, BLW_NOUNS, NOUNS, printForDeBug=0, isTEI=0):
    # get input
    inputData = extractText.extractTextTEI(INPUT, isTEI)
    inputData = inputData.lower()

    #get all BLW
    inputFile= open(BLW_NOUNS, 'r')
    BLWnounsArray = inputFile.read()
    inputFile.close()

    #get all nouns
    inputFile= open(NOUNS, 'r')
    NounsArray = inputFile.read()
    inputFile.close()

    tmp = inputData
    nounsBLWInput = findAllItemFromArray(tmp, BLWnounsArray.splitlines(), printForDeBug)
    # tmp = inputData
    nounsInput = findAllItemFromArray(tmp, NounsArray.splitlines(), printForDeBug)

    if (len(nounsInput) == 0):
        if (printForDeBug):
            print "no BLW"
        return None
    else:
        if (printForDeBug):
            print "ratio: ", float(len(nounsBLWInput))/len(nounsInput)*100, "%"
            print "blw:"
            print nounsBLWInput
            print "all nouns:"
            print nounsInput
        return float(len(nounsBLWInput))/len(nounsInput)*100, nounsBLWInput, nounsInput
#a.e. bug
# calculateReabilityByWordnetForEnglish('data/_testData.txt','all-BLW.txt','all-SORTED-wordnet-nouns.txt', 1)

#add a tuple of filepath [file1, file2, file3...]
def generateOutput(processID, filesPath, output, PROCESS_LOCK, TOTAL_TIME, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, isDebug = 0, isTEI = 0):
    for file in filesPath:
        startTime = time.time();
        ratio, blwN, allN = calculateReabilityByWordnetForEnglish(file, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, isDebug, isTEI)
        endTime = time.time();
        PROCESS_LOCK.acquire()
        TOTAL_TIME[0] = TOTAL_TIME[0] + 1
        TOTAL_TIME[1] = TOTAL_TIME[1] + endTime - startTime
        print TOTAL_TIME[0], ". process ", processID, " ", file, " time cost: ", time.time() - startTime, " time total currently: ", TOTAL_TIME[1]
        output.write(file + ";"+str(ratio) + ";" + " | ".join(blwN) + ";"  + " | ".join(allN) + "\n")
        PROCESS_LOCK.release()

mainStartTime = time.time();
MAX_PROCESS = int(sys.argv[1])
FILEPATH = sys.argv[2]
outputPath = sys.argv[3]
INPUT_BLW_NOUNS = sys.argv[4]
INPUT_ALL_NOUNS = sys.argv[5]
print 'number of process:', MAX_PROCESS, ' working on ', FILEPATH, 'save as ', outputPath
output = open(outputPath, 'w')
output.write("file;ratio;blw;allNoun\n")
#FILEPATH = "data/testDataNM"
#FILEPATH = "data/testDataTEI"
# FILEPATH = "data/English Textbook 4 Readability Level"
files = mod1.listAllFile(FILEPATH, 1)
partFiles = len(files)/MAX_PROCESS
myProcess = []
lock = Lock()
TOTAL_TIME = Array('f', [0, 0])
for processID in range(MAX_PROCESS-1):
    tmp = files[processID * partFiles:(processID+1)*partFiles]
    tmp = Process(target=generateOutput, args=(processID, tmp, output, lock, TOTAL_TIME, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, 0, 1, ))
    myProcess.append(tmp)
myProcess.append(Process(target=generateOutput, args=(MAX_PROCESS-1, files[(MAX_PROCESS - 1) * partFiles:], output, lock, TOTAL_TIME, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, 0, 1, )))
for _process in myProcess:
    _process.start()
for _process in myProcess:
    _process.join()
mainEndTime = time.time();
print "average time if do in one thread for one file: ", float(TOTAL_TIME[1])/TOTAL_TIME[0]
print "average time if do in", MAX_PROCESS, "process for one file: ", (mainEndTime - mainStartTime)/TOTAL_TIME[0]
print "program time cost (1 process): ", TOTAL_TIME[1]
print "program time cost: ", (mainEndTime - mainStartTime)
output.closed