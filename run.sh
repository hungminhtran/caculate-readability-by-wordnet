# command: python (number_process_to_use) (output_file) (input_data) (blw_data) (nouns_data)

# for debug
echo "just debugging"
python3 module-1.py # generate necessary file
python3 main.py 4 data/testDataTEI output/test_output.csv input/wn-nouns/all-wn-BLW.txt input/wn-nouns/all-wn-SORTED-nouns.txt 0 1

#run command
# echo "program running"
# python3 module-1.py # generate necessary file
# python3 main.py 4 'data/English Textbook 4 Readability Level' output/ET4RL-outputBlw.csv input/blw-nouns/all-blw-BLW.txt input/wn-nouns/all-wn-SORTED-nouns.txt  0 1
# python3 main.py 4 'data/English Textbook 4 Readability Level' output/ET4RL-outputWN.csv input/wn-nouns/all-wn-BLW.txt input/wn-nouns/all-wn-SORTED-nouns.txt  0 1
# python3 main.py 4 'data/English Textbook 4 Readability Level' output/ET4RL-outputFreq.csv input/freq-nouns/3000-freq-BLW.txt input/wn-nouns/all-wn-SORTED-nouns.txt  0 1
