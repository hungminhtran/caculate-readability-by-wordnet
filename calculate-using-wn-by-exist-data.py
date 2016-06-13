# python3 calculate-using-wn-by-exist-data.py [existing output file] [blw input] [new output file]
# python3 calculate-using-wn-by-exist-data.py output/ET4RL-outputFreq.csv input/freq-nouns/3000-freq-BLW.txt output/ET4RL-outputFreq_gen.csv
import sys

existingResult = open(sys.argv[1], 'r').read().split('\n')
print('existing result ', sys.argv[1])
BLWnounsArray = open(sys.argv[2], 'r').read().split('\n')
print('blw  ', sys.argv[2])
outputFile = open(sys.argv[3], 'w+')
print('output  ', sys.argv[3])
outputFile.write("file,ratio,blw,allNoun\n")
print('')
for i in range(1, len(existingResult)):
    temp = existingResult[i].split(',')
    if (temp != ['']):
        # print('')
        # print('temp is asdf', temp)
        # print('')
        allNouns = temp[3].split(' | ')
        nounsSet = set(allNouns)
        blwSet = set(BLWnounsArray)
        nounsBLWInput = list(nounsSet.intersection(blwSet))
        nounsBLWInput.sort()
        ratio = 0
        if len(nounsBLWInput) > 0:
            ratio = len(nounsBLWInput)/float(len(allNouns))*100.0
        outputFile.write(temp[0] + ',' +  str(ratio) +',' + " | ".join(nounsBLWInput) + ',' + " | ".join(allNouns) + '\n')

outputFile.close()
