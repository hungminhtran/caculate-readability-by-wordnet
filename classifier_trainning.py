import sys
if sys.version_info[0] > 2:
    raise "Must be using Python 2"
from sklearn import svm, cross_validation, datasets
from sklearn.externals import joblib    
from sklearn.utils import shuffle
import numpy
import time, os
from multiprocessing import Pool
MAX_PROCESS = 4
CF = 0.9

def smv_freq(inputFile, directory = 'svm_pkl/', mykernel=['linear', 'poly', 'rbf'], isuseDict = 0, dictPath = 'data/TanSoTu.txt'):
    START_TIME = time.time()
    if (isuseDict):
        dictFreq = []
        _tempfile = open(dictPath, 'r') 
        dictData = _tempfile.read().splitlines()
        _tempfile.close()
        for i in range(len(dictData)):
            dictFreq.append(float(dictData[i].split('\t')[1]))
        dictFreq = numpy.asarray(dictFreq)
    # inputFile = ['data/ppVietnameseLocalWordsFreq/test_data1.txt', 'data/ppVietnameseLocalWordsFreq/test_data2.txt']
        # clf_List = [clf_poly_noblw, clf_poly_blw, clf_linear_noblw, clf_linear_blw]
        # clf_name = ['poly_noblw', 'poly_blw', 'linear_noblw', 'linear_blw']
    clf_List = []
    clf_name = []
    for _kernel in mykernel:
        if _kernel == 'linear':
            clf_List.append(svm.LinearSVC())
            clf_List.append(svm.LinearSVC())            
        else:
            clf_List.append(svm.SVC(kernel=_kernel))
            clf_List.append(svm.SVC(kernel=_kernel))
        clf_name.append(_kernel + 'noblw')
        clf_name.append(_kernel + 'blw')

    X = numpy.loadtxt(inputFile[0])
    for _file in range(1, len(inputFile)):
        X = numpy.concatenate((X, numpy.loadtxt(inputFile[_file])), axis=0)

    # data = datasets.load_digits().data
    # target = datasets.load_digits().target
    # target = target.reshape((target.shape[0], 1))
    # X = numpy.append(data, target, 1)
    # X = numpy.asarray(X)
    # X = numpy.repeat(X, 10, 0)

    X = shuffle(X, random_state=0)
    print(X[1])
    X[:,-2] = X[:,-2] / 100
    if (isuseDict):
        dictFreq = numpy.power(10.0, -dictFreq)
        X[:,:-2] = X[:,:-2] - dictFreq
        X = numpy.fabs(X)
    print(X[1])
    # for _kernel in mykernel:
    print('input data shape', X.shape)
    print('train and dump clf')  
    if not os.path.exists(directory):
        os.makedirs(directory)
    for j in range(len(clf_List)):
        TRAIN_TIME = time.time()
        temp1 = int(CF*len(X)) - 1
        temp2 = len(X[0]) - 1 - (j+1) % 2
        # print(X[:temp1,:temp2], X[:temp1, -1])
        clf_List[j].fit(X[:temp1,:temp2], X[:temp1, -1])
        print(X[:temp1,:temp2].shape, temp1, temp2, j, 'clf done', 'time', time.time() - TRAIN_TIME)
        DUMP_TIME = time.time()
        joblib.dump(clf_List[j],  directory + '/' + clf_name[j] + '.pkl')
        print(clf_name[j], 'dump time total: ', time.time() - DUMP_TIME)

    print('test')
    for j in range(len(clf_List)):
        TRAIN_TIME = time.time()
        temp1 = int(CF*len(X))
        temp2 = X.shape[1] - 1 - (j+1) % 2
        print(X[temp1:,:temp2].shape, j, 'clf test score', clf_name[j], clf_List[j].score(X[temp1:,:temp2], X[temp1:, -1]), 'time', time.time() - TRAIN_TIME)
    # X = []
    print('load dump')
    for i in range(len(clf_List)):
        TRAIN_TIME = time.time()
        clf2 = joblib.load(directory + clf_name[i] + '.pkl')
        temp1 = int(CF*len(X))
        temp2 = X.shape[1] - 1 - (i+1) % 2
        print(X[temp1:,:temp2].shape, i, 'clf load test score', clf_name[i], clf2.score(X[temp1:,:temp2], X[temp1:, -1]), 'time', time.time() - TRAIN_TIME)
    print('end at ', time.time() - START_TIME)

if __name__ == '__main__':
    # inputFile_1 = ['data/ppVietnameseLocalWordsFreq/Difficult_data.large.txt', 'data/ppVietnameseLocalWordsFreq/Easy_data.large.txt', 'data/ppVietnameseLocalWordsFreq/Normal_data.large.txt']
    # smv_freq(inputFile_1, directory = 'svm_pkl/', mykernel=['linear'], isuseDict = 1, dictPath = 'data/TanSoTu.txt')
    inputFile_2 = ['data/ppVietnameseShallowFt/ShallowFt_Difficult_data.txt', 'data/ppVietnameseShallowFt/ShallowFt_Normal_data.txt', 'data/ppVietnameseShallowFt/ShallowFt_Easy_data.txt']
    # smv_freq(inputFile_2, 'svm_pkl_4ft/', mykernel=['linear', 'linear', 'linear'])
    smv_freq(inputFile_2, 'svm_pkl_4ft/')