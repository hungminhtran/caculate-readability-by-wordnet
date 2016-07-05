import sys
if sys.version_info[0] > 2:
    raise "Must be using Python 2"
from sklearn import svm, cross_validation, datasets
from sklearn.externals import joblib    
from sklearn.utils import shuffle
import numpy
import time, os
from multiprocessing import Pool, Process, Lock, Array, Queue
MAX_PROCESS = 4
CF = 0.9

def smv_freq(inputFile, directory = 'svm_pkl/', mykernel=['linear'], isuseDict = 0, dictPath = 'data/TanSoTu.txt'):
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

    # X = numpy.loadtxt(inputFile[0])
    # for _file in range(1, len(inputFile)):
    #     X = numpy.concatenate((X, numpy.loadtxt(inputFile[_file])), axis=0)
    X = []
    for i in range(len(inputFile)):
        _tempfile = open(inputFile[i], 'r')
        temp = _tempfile.read()
        _tempfile.close()
        X = X + temp.splitlines()
    for i in range(len(X)):
        X[i] = X[i].split(',')
    X = numpy.asarray(X)


    # data = datasets.load_digits().data
    # target = datasets.load_digits().target
    # target = target.reshape((target.shape[0], 1))
    # X = numpy.append(data, target, 1)
    # X = numpy.asarray(X)
    # X = numpy.repeat(X, 10, 0)

    if (isuseDict):
        dictFreq = numpy.power(10.0, -dictFreq)
        X[:,:-2] = X[:,:-2] - dictFreq
        X = numpy.fabs(X)
    X = shuffle(X, random_state=0)
    print('X',X[1])
    # for _kernel in mykernel:
    print('input data shape', X.shape)
    print('train and dump clf')  
    if not os.path.exists(directory):
        os.makedirs(directory)
    temp = X[:,1:].astype(numpy.float)
    # X[:,-2] = X[:,-2] / 100
    print('temp',temp[1])
    for j in range(len(clf_List)):
        TRAIN_TIME = time.time()
        temp1 = int(CF*len(temp)) - 1
        temp2 = len(temp[0]) - 1 - (j+1) % 2
        # print(X[:temp1,:temp2], X[:temp1, -1])
        # clf_List[j].fit(X[:temp1,:temp2], X[:temp1, -1])
        # print(X[:temp1,1:temp2].shape,  X[:temp1,1:temp2][1])
        # print(temp.shape,  temp[:temp1,:temp2][1])
        # print('temp',temp[1,:temp2])
        # scores = cross_validation.cross_val_score(clf_List[j], temp[:,:temp2], temp[:, -1], cv=9)
        # print(j, temp[:temp1,:temp2].shape, clf_name[j], 'done', 'time', time.time() - TRAIN_TIME)
        # print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        # print('')
        print('train', temp[:temp1,:temp2][1])
        clf = clf_List[j].fit(temp[:temp1,:temp2], temp[:temp1, -1])
        score = clf.score(temp[temp1:,:temp2], temp[temp1:, -1])
        _tempfile = open('output/svm_result_'  + '_' + clf_name[j] + '_score=' + str(score) + '_.csv', 'w+')
        if (j % 2 == 1):
            _tempfile.write('filename,words/sentences,letters/senetences,letters/words,blw,lable,predict\n')
            _tempfile.write('traindata,traindata,traindata,traindata,traindata,traindata,traindata\n')
        else:
            _tempfile.write('filename,words/sentences,letters/senetences,letters/words,lable,predict\n')
            _tempfile.write('traindata,traindata,traindata,traindata,traindata,traindata\n')
        # print('X', X.shape, X[1])
        # _prediction = clf.predict(temp[1][:temp2])
        # print('predict', str(_prediction[0]))
        for i in range(temp1):
            _prediction = clf.predict(temp[i][:temp2])
            _output = ','.join(X[i][:temp2+1]) + ',' + X[i][-1].tostring()
            _output = _output + ',' + str(_prediction[0]) + '\n'
            _tempfile.write(_output)
        if (j % 2 == 1):
            _tempfile.write('testdata,testdata,testdata,testdata,testdata,testdata,testdata\n')
        else:
            _tempfile.write('testdata,testdata,testdata,testdata,testdata,testdata\n')
        for i in range(temp1+1, X.shape[0]):
            _prediction = clf.predict(temp[i][:temp2])            
            _output = ','.join(X[i][:temp2+1]) + ',' + X[i][-1].tostring()
            _output = _output + ',' + str(_prediction[0]) + '\n'
            _tempfile.write(_output)                
        _tempfile.close()
    #     DUMP_TIME = time.time()
    #     joblib.dump(clf_List[j],  directory + '/' + clf_name[j] + '.pkl')
    #     print(clf_name[j], 'dump time total: ', time.time() - DUMP_TIME)
    # print('test')
    # for j in range(len(clf_List)):
    #     TRAIN_TIME = time.time()
    #     temp1 = int(CF*len(X))
    #     temp2 = X.shape[1] - 1 - (j+1) % 2
    #     print(X[temp1:,:temp2].shape, j, 'clf test score', clf_name[j], clf_List[j].score(X[temp1:,:temp2], X[temp1:, -1]), 'time', time.time() - TRAIN_TIME)
    # # X = []
    # print('load dump')
    # for i in range(len(clf_List)):
    #     TRAIN_TIME = time.time()
    #     clf2 = joblib.load(directory + clf_name[i] + '.pkl')
    #     temp1 = int(CF*len(X))
    #     temp2 = X.shape[1] - 1 - (i+1) % 2
    #     print(X[temp1:,:temp2].shape, i, 'clf load test score', clf_name[i], clf2.score(X[temp1:,:temp2], X[temp1:, -1]), 'time', time.time() - TRAIN_TIME)
    print('end at ', time.time() - START_TIME)

if __name__ == '__main__':
    # inputFile_1 = ['data/ppVietnameseLocalWordsFreq/Difficult_data.large.txt', 'data/ppVietnameseLocalWordsFreq/Easy_data.large.txt', 'data/ppVietnameseLocalWordsFreq/Normal_data.large.txt']
    # smv_freq(inputFile_1, directory = 'svm_pkl/', mykernel=['linear'], isuseDict = 1, dictPath = 'data/TanSoTu.txt')
    inputFile_2 = ['data/ppVietnameseShallowFt/ShallowFt_Difficult_data.txt', 'data/ppVietnameseShallowFt/ShallowFt_Normal_data.txt', 'data/ppVietnameseShallowFt/ShallowFt_Easy_data.txt']
    # smv_freq(inputFile_2, 'svm_pkl_4ft/', mykernel=['linear', 'linear', 'linear'])
    smv_freq(inputFile_2, 'svm_pkl_4ft/', mykernel=['linear', 'rbf'])