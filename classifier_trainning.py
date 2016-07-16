 #!/usr/bin/env python -W ignore::DeprecationWarning
import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"
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
            # clf_List.append(svm.LinearSVC())            
        else:
            clf_List.append(svm.SVC(kernel=_kernel))
            # clf_List.append(svm.SVC(kernel=_kernel))
        # clf_name.append(_kernel + 'noblw')
        # clf_name.append(_kernel + 'blw')
        clf_name.append(_kernel)

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
        # temp2 = len(temp[0]) - 1 - (j+1) % 2
        # print(X[:temp1,:temp2], X[:temp1, -1])
        # clf_List[j].fit(X[:temp1,:temp2], X[:temp1, -1])
        # print(X[:temp1,1:temp2].shape,  X[:temp1,1:temp2][1])
        # print(temp.shape,  temp[:temp1,:temp2][1])
        # print('temp',temp[1,:temp2])
        # scores = cross_validation.cross_val_score(clf_List[j], temp[:,:temp2], temp[:, -1], cv=9)
        # print(j, temp[:temp1,:temp2].shape, clf_name[j], 'done', 'time', time.time() - TRAIN_TIME)
        # print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        # print('')
        colum_whiteList = [0, 2, 3]
        header = ['filename','words_sentences','wrong','letters_words','blw']
        for p in colum_whiteList:
            for q in colum_whiteList:
                X_train = 0
                X_score = 0
                if p == 3 and q == 3:
                    print(temp[:temp1,0:1].shape, temp[:temp1,2:4].shape)
                    X_train = temp[:temp1,0:4]
                    X_score = temp[temp1:,0:4]
                    trainCV = temp[:,0:4]
                elif ( p < q):
                    X_train = numpy.append(temp[:temp1,p:p+1], temp[:temp1,q:q+1], 1)
                    X_score = numpy.append(temp[temp1:,p:p+1], temp[temp1:,q:q+1], 1)
                    trainCV = numpy.append(temp[:,p:p+1], temp[:,q:q+1], 1)
                if (p < q or p == 3 and q == 3):
                    print('train X_train', clf_name[j], p, q, X_train[1])
                    if (p == 2 and q == 3):
                        clf_List[j].fit(X_train, temp[:temp1, -1])
                        score = clf_List[j].score(X_score, temp[temp1:, -1])
                        print(clf_name[j], p, q, "Accuracy: %0.2f " % (score))
                        joblib.dump(clf_List[j],  directory + '/' + clf_name[j] + '.pkl')
                        clf = joblib.load(directory + '/' +  clf_name[j] + '.pkl')
                        print(X_score.shape, 'clf load test score', clf_name[j], clf.score(X_score, temp[temp1:,-1]), 'train score', clf.score(X_train, temp[:temp1,-1]))
                    
                    # scores = cross_validation.cross_val_score(clf_List[j], trainCV, temp[:, -1], cv=9, n_jobs=-1)
                    # print(clf_name[j], p, q, trainCV.shape, "Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
                    # # title = ''

                        if (p == 3 and q == 3):
                            title = header[1]+ ',' + header[3] + ','+ header[4]
                            _tempfile = open('output/svm_result_'  + title + '_' + clf_name[j] + '_score=' + str(score) + '_.csv', 'w+')
                            _tempfile.write(header[0] + ',' + title + ',lable,predict\n')
                            _tempfile.write('traindata,traindata,traindata,traindata,traindata,traindata\n')
                        else:
                            title  = header[p+1] + ',' + header[q+1]
                            _tempfile = open('output/svm_result_'  + title + '_' + clf_name[j] + '_score=' + str(score) + '_.csv', 'w+')
                            _tempfile.write('filename,' + title +  ',lable,predict\n')
                            _tempfile.write('traindata,traindata,traindata,traindata,traindata\n')
                        # print('X', X.shape, X[1])
                        # _prediction = clf.predict(temp[1][:temp2])
                        # print('predict', str(_prediction[0]))
                        _prediction = clf.predict(X_train)
                        for i in range(temp1):
                            xxx = ''
                            for _temp in X_train[i]:
                                xxx = xxx + ',%.9f' % _temp

                            xx2 = ', %s' % X[i][-1]
                            xx3 = '%s,' % X[i][0]
                            _output = xx3 +  xxx + xx2
                            _output = _output + ',' + str(_prediction[i]) + '\n'
                            _tempfile.write(_output)
                        if (p == 3 and q == 3):
                            _tempfile.write('testdata,testdata,testdata,testdata,testdata,testdata\n')
                        else:
                            _tempfile.write('testdata,testdata,testdata,testdata,testdata\n')
                        _prediction = clf.predict(X_score)
                        for i in range(X_score.shape[0]):
                            xxx = ''
                            for _temp in X_score[i]:
                                xxx = xxx + ',%.9f' % _temp
                            xx2 = ', %s' % X[i][-1]
                            xx3 = '%s,' % X[i][0]
                            _output = xx3 +  xxx + xx2
                            _output = _output + ',' + str(_prediction[i]) + '\n'
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