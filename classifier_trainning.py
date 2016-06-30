import sys
if sys.version_info[0] > 2:
    raise "Must be using Python 2"
from sklearn import svm, cross_validation, datasets
from sklearn.externals import joblib    
from sklearn.utils import shuffle
import numpy
import time, os
CF = 0.9
BIAS = 4
if __name__ == '__main__':
    START_TIME = time.time()
    # inputFile = ['data/ppVietnameseLocalWordsFreq/Difficult_data.txt', 'data/ppVietnameseLocalWordsFreq/Easy_data.txt', 'data/ppVietnameseLocalWordsFreq/Normal_data.txt']
    inputFile = ['data/ppVietnameseLocalWordsFreq/test_data1.txt', 'data/ppVietnameseLocalWordsFreq/test_data2.txt']
    k = 0;
    clf_linear_blw = svm.SVC(kernel='linear')
    clf_linear_noblw = svm.SVC(kernel='linear')
    clf_poly_blw = svm.SVC(kernel='poly')
    clf_poly_noblw = svm.SVC(kernel='poly')
    clf_List = [clf_poly_noblw, clf_poly_blw, clf_linear_noblw, clf_linear_blw]
    clf_name = ['poly_noblw', 'poly_blw', 'linear_noblw', 'linear_blw']
    X = []
    for file in inputFile:
        _tempFile = open(file, 'r')
        lines = _tempFile.readlines();
        _tempFile.close()
        for line in lines:
            X = X + [map(float, line.split())] #add line 0 first for svm to get all class
    data = datasets.load_digits().data
    target = datasets.load_digits().target
    target = target.reshape((target.shape[0], 1))
    X = numpy.append(data, target, 1)

    X = numpy.asarray(X)
    X = numpy.repeat(X, 1000, 0)
    X = shuffle(X, random_state=0)
    for j in range(len(clf_List)):
        TRAIN_TIME = time.time()
        temp1 = int(CF*len(X)) - 1
        temp2 = len(X[0]) - 1 - (j+1) % 2
        # print(X[:temp1,:temp2], X[:temp1, -1])
        clf_List[j].fit(X[:temp1,:temp2], X[:temp1, -1])
        print(X[:temp1,:temp2].shape, temp1, temp2, j, 'clf done', 'time', time.time() - TRAIN_TIME)
    print('test')
    for j in range(len(clf_List)):
        TRAIN_TIME = time.time()
        temp1 = int(CF*len(X))
        temp2 = X.shape[1] - 1 - (j+1) % 2
        print(X[temp1:,:temp2].shape, j, 'clf test score', clf_name[j], clf_List[j].score(X[temp1:,:temp2], X[temp1:, -1]), 'time', time.time() - TRAIN_TIME)
    # X = []
    print('train done, dump clf')  
    directory = 'svm_pkl/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i in range(len(clf_List)):
        DUMP_TIME = time.time()
        joblib.dump(clf_List[i],  directory + clf_name[i] + '.pkl')
        print(clf_name[i], 'dump time total: ', time.time() - DUMP_TIME)
    print('load dump')

    for i in range(len(clf_List)):
        TRAIN_TIME = time.time()
        clf2 = joblib.load(directory + clf_name[i] + '.pkl')
        temp1 = int(CF*len(X))
        temp2 = X.shape[1] - 1 - (i+1) % 2
        print(X[temp1:,:temp2].shape, i, 'clf load test score', clf_name[i], clf2.score(X[temp1:,:temp2], X[temp1:, -1]), 'time', time.time() - TRAIN_TIME)

    print('end at ', time.time() - START_TIME)