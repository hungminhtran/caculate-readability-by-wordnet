import time
import sys
from multiprocessing import Process, Lock, Array, SimpleQueue
import importlib
from datetime import datetime
END_PROCESS_SIGNAL = 'END_PROCESS_SIGNAL'
mod2 = importlib.import_module("module-2")
mod1 = importlib.import_module("module-1")
testDataTEIMod = importlib.import_module("test_ExtractText")

#add a tuple of filepath [file1, file2, file3...]
def generateOutput(processID, filesQueue, outQueue, PROCESS_LOCK, TOTAL_TIME, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, isDebug = 0
, isTEI = 0):
    #loop till out of file
    PROCESS_LOCK.acquire()
    print('='*5, 'proc', processID, 'start at', datetime.now().time(), '='*5)
    PROCESS_LOCK.release()
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
            beginTime = datetime.now().time()
            ratio, blwN, allN = mod2.calculateReabilityByWordnetForEnglish(_file, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, isDebug
            , isTEI)
            endTime = time.time();
            #write down\
            PROCESS_LOCK.acquire()
            TOTAL_TIME[1] = TOTAL_TIME[1] + endTime - startTime
            print(int(TOTAL_TIME[0]), "-proc", processID, 'start time', beginTime, 'end process time', datetime.now().time(),
            "-time cost:", int(time.time() - startTime), _file)
            TOTAL_TIME[0] = TOTAL_TIME[0] + 1
            outQueue.put(_file + ","+str(ratio) + "," + " | ".join(blwN) + ","  + " | ".join(allN) + "\n")
            PROCESS_LOCK.release()

    PROCESS_LOCK.acquire()
    print('='*5, '-proc', processID, 'exit at', datetime.now().time(), '='*5)
    outQueue.put(END_PROCESS_SIGNAL)
    PROCESS_LOCK.release()

def writeOUt(outQueue, fileName, PROCESS_LOCK):
    PROCESS_LOCK.acquire()
    print('='*5, 'proc writeOut', 'start at', datetime.now().time(), '='*5)
    PROCESS_LOCK.release()
    EOP = 0
    outFile = open(fileName, 'w+')
    outFile.write("file,ratio,blw,allNoun\n")
    while (1):
        time.sleep(10)
        temp = ""
        if (EOP == MAX_PROCESS):
            break;
        PROCESS_LOCK.acquire()
        while not outQueue.empty():
            temp = outQueue.get()
            if (temp == END_PROCESS_SIGNAL):
                EOP = EOP + 1
            else:
                outFile.write(temp)
        PROCESS_LOCK.release()
    # not need to use mutex here because all process are close
    print('='*5, 'proc writeOut', 'exit at', datetime.now().time(), '='*5)
    outFile.close()

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
    # write output process
    myProcess.append(Process(target=writeOUt, args=(outQueue, outputPath, lock)))
    #start and wait all process finish their job
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
else:
    print('module won"t run if not main()')
