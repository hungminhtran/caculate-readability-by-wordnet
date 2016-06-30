import sys
if sys.version_info[0] > 2:
    raise "Must be using Python 2"
from sklearn import svm, cross_validation
from sklearn.externals import joblib    
import numpy
import time;
CF = 1
BIAS = 4
if __name__ == '__main__':
    START_TIME = time.time()
    # inputFile = ['data/ppVietnameseLocalWordsFreq/Difficult_data.txt', 'data/ppVietnameseLocalWordsFreq/Easy_data.txt', 'data/ppVietnameseLocalWordsFreq/Normal_data.txt']
    inputFile = ['data/ppVietnameseLocalWordsFreq/test_data.txt', 'data/ppVietnameseLocalWordsFreq/test_data2.txt']
    k = 0;
    clf_poly_blw = svm.SVC(kernel='poly')
    clf_linear_blw = svm.SVC(kernel='linear')
    clf_poly_noblw = svm.SVC(kernel='poly')
    clf_linear_noblw = svm.SVC(kernel='linear')
    clf_List = [clf_linear_noblw, clf_linear_blw, clf_poly_noblw, clf_poly_blw]
    clf_name = ['linear_noblw', 'linear_blw', 'poly_noblw', 'poly_blw']
    X = []
    for file in inputFile:
        _tempFile = open(file, 'r')
        X = X + [map(float, _tempFile.readline().split())] #add line 0 first for svm to get all class
        _tempFile.close()

    for _file in range(len(inputFile)):
        _tempFile = open(inputFile[_file], 'r')
        fileData = _tempFile.readlines()
        _tempFile.close()
        for i in range(1, int(len(fileData) * CF - 1)): #line 0 was added above
            k = k + 1;
            X = X + [map(float, fileData[i].split())]
            if k % BIAS == 0 or _file == len(inputFile) - 1 and i == len(fileData) - 1:
                X = numpy.asarray(X)
                TRAIN_TIME = time.time()
                for j in range(len(clf_List)):
                    temp1 = len(X) - 1
                    temp2 = len(X[0]) - 1 - (j+1) % 2
                    print(i, 'asdf', j, temp2, X[:temp1,:temp2])
                    print(i, 'asdf', j, temp2, X[:temp1,-1])
                    clf_List[i].fit(X[:temp1,:temp2], X[:temp1, -1])
                print(len(X), 'lines complete', time.time() - TRAIN_TIME)
                X = []
    print('train done, dump clf')    
    for i in range(len(clf_List)):
        DUMP_TIME = time.time()
        joblib.dump(clf_List[i],  'data/ppVietnameseLocalWordsFreq/svm_pkl/' + clf_name[i] + '.pkl')
        print('dump time total: ', time.time() - DUMP_TIME)
    print('end at ', time.time() - START_TIME)