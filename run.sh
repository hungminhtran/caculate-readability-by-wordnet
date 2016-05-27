#test if some TEI file wrong
python test_ExtractText.py
# command: python (number_process_to_use) (output_file) (input_data) (blw_data) (nouns_data)

# for debug
# python module-2.py 4 data/testDataTEI data/output.csv input/wn-nouns/all-BLW.txt input/wn-nouns/all-SORTED-wordnet-nouns.txt

#run command
python module-2.py 4 'data/English Textbook 4 Readability Level' output/ET4RL-outputWN.csv input/wn-nouns/all-BLW.txt input/wn-nouns/all-SORTED-wordnet-nouns.txt
python module-2.py 4 'data/English Textbook 4 Readability Level' output/ET4RL-outputFreq.csv input/freq-nouns/all-BLW.txt input/freq-nouns/words_freq_SORTED.txt
