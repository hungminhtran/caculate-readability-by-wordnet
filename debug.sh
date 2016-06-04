# for debug
echo "just debugging"
python3 main.py 3 data/testDataTEI output/test_output.csv input/wn-nouns/all-wn-BLW.txt input/wn-nouns/all-wn-SORTED-nouns.txt 0 1
python3 main.py 3 data/testDataNM output/test_NMoutput.csv input/wn-nouns/all-wn-BLW.txt input/wn-nouns/all-wn-SORTED-nouns.txt 0 0
python3 main.py 3 data/testDataVietnamese/normalTest output/test_Vietnamese_output.csv input/vietnamesewn-nouns/all-vietnamesewn-BLW.txt input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt 0 0
