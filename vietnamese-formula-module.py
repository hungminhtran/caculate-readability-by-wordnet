import importlib
mod1 = importlib.import_module("module-1")
import sys
from multiprocessing import Queue, Pool
import time
if (sys.version_info[0] < 3):
    raise "Must be using Python 3"
TOTAL_WORKER = 4
def vietnameseFormual(inputFile):
    vietnameseChar = ["a", "à", "ả", "ã", "á", "ạ", "ă", "ằ", "ẳ", "ẵ", "ắ", "ặ", "â", "ầ", "ẩ", "ẫ", "ấ", "ậ", "b", "c", "d",
    "đ", "e", "è", "ẻ", "ẽ", "é", "ẹ", "ê", "ề", "ể", "ễ", "ế", "ệ", "f", "g", "h", "i", "ì", "ỉ", "ĩ", "í", "ị", "j", "k", "l",
    "m", "n", "o", "ò", "ỏ", "õ", "ó", "ọ", "ô", "ồ", "ổ", "ỗ", "ố", "ộ", "ơ", "ờ", "ở", "ỡ", "ớ", "ợ", "p", "q", "r", "s", "t",
    "u", "ù", "ủ", "ũ", "ú", "ụ", "ư", "ừ", "ử", "ữ", "ứ", "ự", "v", "w", "x", "y", "ỳ", "ỷ", "ỹ", "ý", "ỵ", "z", "-"]
    vietnameseCountChar = [1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3,
    1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2,
    2, 2, 3, 3, 3, 3, 3, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1]
    hashmapVietnameseCharCount = {}
    for i in range(len(vietnameseCountChar)):
        hashmapVietnameseCharCount[vietnameseChar[i]] = vietnameseCountChar[i]
    paragrah = open(inputFile, 'r').read().lower().split('\n')
    totalLetter = 0
    totalWord = 0
    totalSentence = 0
    # each sentence in a line
    for sentence in paragrah:
        if (len(sentence) > 0):
            for c in sentence:
                if (c in hashmapVietnameseCharCount):
                    totalLetter = totalLetter + hashmapVietnameseCharCount[c]
            totalWord = totalWord + sentence.count(" ") + 1
            totalSentence = totalSentence + 1
    WL = float(totalLetter)/totalWord
    SL = float(totalWord)/totalSentence
    RL = 2*WL + 0.2*SL - 6
    return (inputFile, totalLetter, totalWord, totalSentence, RL)
if __name__ == "__main__":
    FILEPATH = sys.argv[1]
    OUTPUTFILE = sys.argv[2]
    startTime = time.time()
    files = mod1.listAllFile(FILEPATH, 1)
    with Pool(TOTAL_WORKER) as p:
        result = p.map(vietnameseFormual, files)
    outputFile = open(OUTPUTFILE, 'w+')
    outputFile.write('file, totalLetter, totalWord, totalSentence, vietnamese formula result\n')
    for item in result:
        outputFile.write(item[0] + ',' + str(item[1]) + ',' + str(item[2]) + ',' + str(item[3]) + ',' + str(item[4]) + '\n')
    outputFile.close()
    print('total worker: ', TOTAL_WORKER, 'cost: ', time.time() - startTime)