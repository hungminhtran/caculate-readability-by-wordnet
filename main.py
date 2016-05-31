import time
import sys
from multiprocessing import Process, Lock, Array, SimpleQueue
import importlib
from datetime import datetime
mod2 = importlib.import_module("module-2")
mod1 = importlib.import_module("module-1")
testDataTEIMod = importlib.import_module("test_ExtractText")

#add a tuple of filepath [file1, file2, file3...]
def generateOutput(processID, filesQueue, outQueue, PROCESS_LOCK, TOTAL_TIME, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, isDebug = 0
, isTEI = 0):
    #loop till out of file
    startProTime = datetime.now().time()
    while (1):
        #get a file from queue
        PROCESS_LOCK.acquire()
        #check if queue is empty
        if filesQueue.empty():
            PROCESS_LOCK.release()
            break
        else:
            _file = filesQueue.get()
            PROCESS_LOCK.release()
            #begin calculate
            startTime = time.time();
            ratio, blwN, allN = mod2.calculateReabilityByWordnetForEnglish(_file, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, isDebug
            , isTEI)
            endTime = time.time();
            #write down
            PROCESS_LOCK.acquire()
            TOTAL_TIME[0] = TOTAL_TIME[0] + 1
            TOTAL_TIME[1] = TOTAL_TIME[1] + endTime - startTime
            print(int(TOTAL_TIME[0]), "-proc", processID, 'startTime', startProTime,  "-time cost:",
            int(time.time() - startTime), "-time total", int(TOTAL_TIME[1]), _file)
            outQueue.put(_file + ","+str(ratio) + "," + " | ".join(blwN) + ","  + " | ".join(allN) + "\n")
            PROCESS_LOCK.release()

if (__name__ == '__main__'):
    mainStartTime = time.time();
    MAX_PROCESS = int(sys.argv[1])
    FILEPATH = sys.argv[2]
    outputPath = sys.argv[3]
    INPUT_BLW_NOUNS = sys.argv[4]
    INPUT_ALL_NOUNS = sys.argv[5]
    DEBUG = int(sys.argv[6])
    TEIFILE = int(sys.argv[7])
    testDataTEIMod.testFunc(FILEPATH)
    print('number of process:', MAX_PROCESS, ' working on ', FILEPATH, 'save as ', outputPath, 'debug', DEBUG, 'is tiefile'
    , TEIFILE)
    #queue use for handling file for each worker
    filesQueue = SimpleQueue()
    files = mod1.listAllFile(FILEPATH, 1)
    for f in files:
        filesQueue.put(f)
    myProcess = []
    lock = Lock()
    TOTAL_TIME = Array('f', [0, 0])
    outQueue = SimpleQueue()
    for processID in range(MAX_PROCESS):
        myProcess.append(Process(target=generateOutput, args=(processID, filesQueue, outQueue, lock, TOTAL_TIME,
        INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, DEBUG, TEIFILE)))
    for _process in myProcess:
        _process.start()
    for _process in myProcess:
        _process.join()
    mainEndTime = time.time();
    print("end time", datetime.now().time())
    print("average time if do in one thread for one file: ", float(TOTAL_TIME[1])/TOTAL_TIME[0])
    print("average time if do in", MAX_PROCESS, "process for one file: ", (mainEndTime - mainStartTime)/TOTAL_TIME[0])
    print("program time cost (1 process): ", TOTAL_TIME[1])
    print("program time cost: ", (mainEndTime - mainStartTime))
    output = open(outputPath, 'w')
    output.write("file,ratio,blw,allNoun\n")
    # output.write(queue)
    while (not outQueue.empty()):
        output.write(outQueue.get())
    output.close()
else:
    print('module won"t run if not main()')
