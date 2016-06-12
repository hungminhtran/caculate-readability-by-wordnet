import sys
inputFile = open('input/POS-nouns/POS.txt', 'r');
data = inputFile.read()
inputFile.close()

data = data.split('\n')
hashmap = {}
for noun in data:
    hashmap[noun] = 0
for noun in data:
    hashmap[noun] = hashmap[noun] + 1
outputFile = open('input/POS-nouns/POS-statictis.txt', 'w+')
sortNouns = ((k, hashmap[k]) for k in sorted(hashmap, key=hashmap.get, reverse=True))
for k, v in sortNouns:
     outputFile.write(k +  '\t' + str(v) + '\n')
outputFile.close()
