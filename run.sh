# command: python (number_process_to_use) (output_file) (input_data) (blw_data) (nouns_data)

#run command
echo "program running"
# python3 module-1.py # generate necessary file
# python3 main.py 1 'data/testDataTEI/' 'output/testDataTEI_output.csv' 'input/wn-nouns/all-wn-BLW.txt' 'input/wn-nouns/all-wn-SORTED-nouns.txt' 1 1
# python3 main.py 4 'data/English Textbook 4 Readability Level' output/ET4RL-outputBlw.csv input/blw-nouns/all-blw-BLW.txt input/wn-nouns/all-wn-SORTED-nouns.txt  0 1
# python3 main.py 4 'data/English Textbook 4 Readability Level' output/ET4RL-outputWN.csv input/wn-nouns/all-wn-BLW.txt input/wn-nouns/all-wn-SORTED-nouns.txt  0 1
# python3 main.py 4 'data/English Textbook 4 Readability Level' output/ET4RL-outputFreq.csv input/freq-nouns/3000-freq-BLW.txt input/wn-nouns/all-wn-SORTED-nouns.txt  0 1

# python3 main.py 4 data/ppVietnamese_by_catalog/Easy/ output/vietnamesewn_Easy_output2.csv input/vietnamesewn-nouns/all-vietnamesewn-BLW.txt input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt 0 0
# python3 main.py 4 data/ppVietnamese_by_catalog/Normal output/vietnamesewn_Normal_output2.csv input/vietnamesewn-nouns/all-vietnamesewn-BLW.txt input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt 0 0
# python3 main.py 4 data/ppVietnamese_by_catalog/Difficult output/vietnamesewn_Difficult_output2.csv input/vietnamesewn-nouns/all-vietnamesewn-BLW.txt input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt 0 0
# python3 main.py 4 data/testDataVietnamese/pp output/testDataVietnamese_output.csv input/vietnamesewn-nouns/all-vietnamesewn-BLW.txt input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt 0 0

# python3 classifier_get_feature.py 'output/test_data.txt' 'output/test_Vietnamese_output_classifier.csv' -1 'data/test_TanSoTu.txt'
# python3 classifier_get_feature.py 'Difficult_data.txt' 'output/vietnamesewn_Difficult_output.csv' 3 'data/TanSoTu.txt'
# python3 classifier_get_feature.py 'Easy_data.txt' 'output/vietnamesewn_Easy_output.csv' 1 'data/TanSoTu.txt'
# python3 classifier_get_feature.py 'Normal_data.txt' 'output/vietnamesewn_Normal_output.csv' 2 'data/TanSoTu.txt'


# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Difficult_output2.csv' 'input/vietnamese-freq-nouns/3000vietnamese-freq-BLW.txt' 'output/vietnamese3000freq_Difficult_output2.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Normal_output2.csv' 'input/vietnamese-freq-nouns/3000vietnamese-freq-BLW.txt' 'output/vietnamese3000freq_Normal_output2.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Easy_output2.csv' 'input/vietnamese-freq-nouns/3000vietnamese-freq-BLW.txt' 'output/vietnamese3000freq_Easy_output2.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Difficult_output2.csv' 'input/vietnamesePOS-nouns/3000-vietnamesePOS-BLW.txt' 'output/vietnamese3000POS_Difficult_output2.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Normal_output2.csv' 'input/vietnamesePOS-nouns/3000-vietnamesePOS-BLW.txt' 'output/vietnamese3000POS_Normal_output2.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Easy_output2.csv' 'input/vietnamesePOS-nouns/3000-vietnamesePOS-BLW.txt' 'output/vietnamese3000freq_Easy_output2.csv'

# python3 calculate-using-wn-by-exist-data.py 'output/ET4RL-outputWN.csv' 'input/20-nouns/all-20-BLW.txt' 'output/ET4RL-output20nouns.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/ET4RL-outputWN.csv' 'input/POS-nouns/all-3kPOS-BLW.txt' 'output/ET4RL-output3kPOS.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/ET4RL-outputWN.csv' 'input/blw-nouns/all-blw-BLW.txt' 'output/ET4RL-outputBlw.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/ET4RL-outputWN.csv' 'input/freq-nouns/3000-freq-BLW.txt' 'output/ET4RL-outputFreq.csv'

# python3 vietnamese-formula-module.py data/ppVietnamese_by_catalog/ output/vietnameseFomula.csv 

# caculate how many word in 3000word appear in document
# python3 main.py 4 data/testDataVietnamese/pp/ output/testDataVietnamese_output3kFreqInDoc.csv input/vietnamesewn-nouns/empty.txt input/vietnamese-freq-nouns/3000vietnamese-freq-SORTED-nouns.txt 0 0
# python3 main.py 4 data/Vietnamese_by_catalog/Easy/ output/vietnamese3kFreqInDoc_Easy_output2.csv input/vietnamesewn-nouns/empty.txt input/vietnamese-freq-nouns/3000vietnamese-freq-SORTED-nouns.txt 0 0
# python3 main.py 4 data/Vietnamese_by_catalog/Normal output/vietnamese3kFreqInDoc_Normal_output2.csv input/vietnamesewn-nouns/empty.txt input/vietnamese-freq-nouns/3000vietnamese-freq-SORTED-nouns.txt 0 0
# python3 main.py 4 data/Vietnamese_by_catalog/Difficult output/vietnamese3kFreqInDoc_Difficult_output2.csv input/vietnamesewn-nouns/empty.txt input/vietnamese-freq-nouns/3000vietnamese-freq-SORTED-nouns.txt 0 0
# get feature
python3 classifier_get_feature.py 'output/test_data.txt' 'output/testDataVietnamese_output.csv' -1 'output/testDataVietnamese_output3kFreqInDoc.csv' '' ''
python3 classifier_get_feature.py 'data/ppVietnameseShallowFt/ShallowFt_Difficult_data.txt' 'output/vietnamesewn_Difficult_output.csv' 3 'output/vietnamese3kFreqInDoc_Difficult_output2.csv' 'Vietnamese_by_catalog' 'ppVietnamese_by_catalog'
python3 classifier_get_feature.py 'data/ppVietnameseShallowFt/ShallowFt_Easy_data.txt' 'output/vietnamesewn_Easy_output.csv' 1 'output/vietnamese3kFreqInDoc_Easy_output2.csv' 'Vietnamese_by_catalog' 'ppVietnamese_by_catalog'
python3 classifier_get_feature.py 'data/ppVietnameseShallowFt/ShallowFt_Normal_data.txt' 'output/vietnamesewn_Normal_output.csv' 2  'output/vietnamese3kFreqInDoc_Normal_output2.csv' 'Vietnamese_by_catalog' 'ppVietnamese_by_catalog'
echo "end"