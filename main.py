import time
import sys
from multiprocessing import Process, Lock, Array, Queue
import importlib
mod2 = importlib.import_module("module-2")
mod1 = importlib.import_module("module-1")
testDataTEIMod = importlib.import_module("test_ExtractText")

#add a tuple of filepath [file1, file2, file3...]
def generateOutput(processID, filesPath, queue, PROCESS_LOCK, TOTAL_TIME, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, isDebug = 0, isTEI = 0):
    for file in filesPath:
        startTime = time.time();
        ratio, blwN, allN = mod2.calculateReabilityByWordnetForEnglish(file, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, isDebug, isTEI)
        endTime = time.time();
        PROCESS_LOCK.acquire()
        TOTAL_TIME[0] = TOTAL_TIME[0] + 1
        TOTAL_TIME[1] = TOTAL_TIME[1] + endTime - startTime
        print(int(TOTAL_TIME[0]), ". process ", processID, " ", file, " time cost: ", int(time.time() - startTime), " time total currently: ", int(TOTAL_TIME[1]))
        queue.put(file + ","+str(ratio) + "," + " | ".join(blwN) + ","  + " | ".join(allN) + "\n")
        PROCESS_LOCK.release()

mainStartTime = time.time();
MAX_PROCESS = int(sys.argv[1])
FILEPATH = sys.argv[2]
outputPath = sys.argv[3]
INPUT_BLW_NOUNS = sys.argv[4]
INPUT_ALL_NOUNS = sys.argv[5]

testDataTEIMod.testFunc(FILEPATH)

print('number of process:', MAX_PROCESS, ' working on ', FILEPATH, 'save as ', outputPath)
queue = Queue()
files = mod1.listAllFile(FILEPATH, 1)
partFiles = len(files)/MAX_PROCESS
myProcess = []
lock = Lock()
TOTAL_TIME = Array('f', [0, 0])
for processID in range(MAX_PROCESS-1):
    tmp = files[int(processID * partFiles):int((processID+1)*partFiles)]
    tmp = Process(target=generateOutput, args=(processID, tmp, queue, lock, TOTAL_TIME, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, 0, 1, ))
    myProcess.append(tmp)
myProcess.append(Process(target=generateOutput, args=(MAX_PROCESS-1, files[int((MAX_PROCESS - 1) * partFiles):], queue, lock, TOTAL_TIME, INPUT_BLW_NOUNS, INPUT_ALL_NOUNS, 0, 1, )))
for _process in myProcess:
    _process.start()
for _process in myProcess:
    _process.join()
mainEndTime = time.time();
print("average time if do in one thread for one file: ", float(TOTAL_TIME[1])/TOTAL_TIME[0])
print("average time if do in", MAX_PROCESS, "process for one file: ", (mainEndTime - mainStartTime)/TOTAL_TIME[0])
print("program time cost (1 process): ", TOTAL_TIME[1])
print("program time cost: ", (mainEndTime - mainStartTime))
output = open(outputPath, 'w')
output.write("file,ratio,blw,allNoun\n")
# output.write(queue)
while (not queue.empty()):
    output.write(queue.get())
output.close()
