import importlib
mod1 = importlib.import_module("module-1")
extractText = importlib.import_module("ExtractText")
from nltk.corpus import wordnet as wn
import nltk
import re
import threading
import time
import sys
TOTAL_TIME = [0, 0]
MAX_THREAD = 2
# TOTAL_THREAD =  threading.BoundedSemaphore(MAX_THREAD)
THREAD_LOCK = threading.Lock()

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
class myThread(threading.Thread):
    def __init__(self, threadID, filesPath, output, isDebug = 0, isTEI = 0):
        # TOTAL_THREAD.acquire() # decrements the counter
        super(myThread, self).__init__()
        self.threadID = threadID
        self.filesPath = filesPath
        self.output = output
        self.isDebug = isDebug
        self.isTEI = isTEI

    def run(self):
        for file in self.filesPath:
            startTime = time.time();
            ratio, blwN, allN = calculateReabilityByWordnetForEnglish(file,'all-BLW.txt','all-SORTED-wordnet-nouns.txt', self.isDebug, self.isTEI)
            endTime = time.time();
            with THREAD_LOCK:
                TOTAL_TIME[0] = TOTAL_TIME[0] + 1
                TOTAL_TIME[1] = TOTAL_TIME[1] + endTime - startTime
                print TOTAL_TIME[0], ". thread ", str(self.threadID), " ", file, " time cost: ", time.time() - startTime, " time total currently: ", TOTAL_TIME[1]
                self.output.write(file + ";"+str(ratio) + ";" + " | ".join(blwN) + ";"  + " | ".join(allN) + "\n")
        # TOTAL_THREAD.release() # increments the counter

mainStartTime = time.time();
FILEPATH = sys.argv[1]
outputPath = sys.argv[2]
print 'number of thread:', MAX_THREAD, ' working on ', FILEPATH, 'save as ', outputPath
output = open(outputPath  + 'output.csv', 'w')
output.write("file;ratio;blw;allNoun\n")
#FILEPATH = "data/testDataNM"
#FILEPATH = "data/testDataTEI"
# FILEPATH = "data/English Textbook 4 Readability Level"
#0, 1, 2, 3
# FILEPATH = "data/testMultithread_1"
files = mod1.listAllFile(FILEPATH, 1)
quaterFiles = len(files)/4
myThreadArr = []
for threadID in range(MAX_THREAD-1):
    tmp = files[threadID * quaterFiles:(threadID+1)*quaterFiles]
    tmpT = myThread(threadID, tmp, output, 0, 1)
    tmpT.start()
    myThreadArr.append(tmpT)
tmpT = myThread(MAX_THREAD-1, files[(MAX_THREAD-1) * quaterFiles:], output, 0, 1)
tmpT.start()
myThreadArr.append(tmpT)

for _myThread in myThreadArr:
    _myThread.join()
mainEndTime = time.time();
print "average time if do in one thread for one file: ", float(TOTAL_TIME[1])/TOTAL_TIME[0]
print "time of program: ", (mainEndTime - mainStartTime)
output.closed