import sys

existingResult = open(sys.argv[1], 'r').read().split('\n')
print('existing result ', sys.argv[1])
BLWnounsArray = open(sys.argv[2], 'r').read().split('\n')
print('blw  ', sys.argv[2])
outputFile = open(sys.argv[3], 'w+')
print('output  ', sys.argv[3])
outputFile.write("file,ratio,all blw,all nouns")
print('')
for element in existingResult:
    temp = element.split(',')
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
            ratio = len(nounsBLWInput)/len(allNouns)
        outputFile.write(temp[0] + ',' +  str(ratio) +',' + " | ".join(nounsBLWInput) + ',' + " | ".join(allNouns) + '\n')

outputFile.close()
