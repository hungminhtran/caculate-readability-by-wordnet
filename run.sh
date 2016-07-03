# command: python (number_process_to_use) (output_file) (input_data) (blw_data) (nouns_data)

#run command
echo "program running"
# python3 module-1.py # generate necessary file
python3 main.py 4 'data/testDataTEI/' 'output/testDataTEI_output.csv' 'input/wn-nouns/all-wn-BLW.txt' 'input/wn-nouns/all-wn-SORTED-nouns.txt' 0 1
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

# python3 classifier_get_feature.py 'output/test_data.txt' 'output/test_Vietnamese_output_classifier.csv' -1 
# python3 classifier_get_feature.py 'output/ShallowFt_Difficult_data.txt' 'output/vietnamesewn_Difficult_output2.csv' 3 
# python3 classifier_get_feature.py 'output/ShallowFt_Easy_data.txt' 'output/vietnamesewn_Easy_output2.csv' 1 
# python3 classifier_get_feature.py 'output/ShallowFt_Normal_data.txt' 'output/vietnamesewn_Normal_output2.csv' 2 

# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Difficult_output2.csv' 'input/vietnamese-freq-nouns/3000vietnamese-freq-BLW.txt' 'output/vietnamese3000freq_Difficult_output2.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Normal_output2.csv' 'input/vietnamese-freq-nouns/3000vietnamese-freq-BLW.txt' 'output/vietnamese3000freq_Normal_output2.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Easy_output2.csv' 'input/vietnamese-freq-nouns/3000vietnamese-freq-BLW.txt' 'output/vietnamese3000freq_Easy_output2.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Difficult_output2.csv' 'input/vietnamesePOS-nouns/3000-vietnamesePOS-BLW.txt' 'output/vietnamese3000POS_Difficult_output2.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Normal_output2.csv' 'input/vietnamesePOS-nouns/3000-vietnamesePOS-BLW.txt' 'output/vietnamese3000POS_Normal_output2.csv'
# python3 calculate-using-wn-by-exist-data.py 'output/vietnamesewn_Easy_output2.csv' 'input/vietnamesePOS-nouns/3000-vietnamesePOS-BLW.txt' 'output/vietnamese3000freq_Easy_output2.csv'

python3 vietnamese-formula-module.py data/ppVietnamese_by_catalog/ output/vietnameseFomula.csv 
echo "end"