# -*- coding: utf-8 -*-
from . import module_2
mod2 = module_2
from sklearn import svm, cross_validation, datasets
from sklearn.externals import joblib    
import hashlib
import time
import subprocess
import numpy
from .classifier_get_feature import getShallowFeatureForFile
from django.http import HttpResponseRedirect
from django.shortcuts import render

_tempfile = open('static/input/vietnamesewn-nouns/all-vietnamesewn-BLW.txt', 'r')
BLWnounsArray = _tempfile.read().splitlines()
_tempfile.close()
_tempfile = open('static/input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt', 'r')
NounsArray = _tempfile.read().splitlines()
_tempfile.close()

clf2 = joblib.load('static/svm_pkl_4ft' + '/' +  'rbf' + '.pkl')


def upload_file(request):
    output = ""
    if request.method == 'POST':
        START_TIME = time.time()
        if ('myfile' in request.FILES != None):
            m = hashlib.md5()
            m.update(str(request.FILES['myfile']).encode('utf-8'))
            hashName = m.hexdigest()
            filename ='static/tmp/' +  hashName
            with open(filename, 'wb+') as destination:
                # print('request file', str(request.FILES['myfile']))
                for chunk in request.FILES['myfile'].chunks():
                    destination.write(chunk)
            subprocess.check_call("dos2unix " + filename, shell=True)
            ratio, blwN, allN = mod2.calculateReabilityByWordnetForEnglish(filename, BLWnounsArray, NounsArray, 0, 0)
            subprocess.check_call("java -jar static/vn.hus.nlp.tokenizer-4.1.1-bin/vn.hus.nlp.tokenizer-4.1.1.jar -i " + filename + " -o " + filename + ".tok", shell=True)
            filename = filename + ".tok"
            _tempfile = open(filename, 'r')
            inputData = _tempfile.read()
            _tempfile.close()
            row = filename + ","+str(ratio) + "," + " | ".join(blwN) + ","  + " | ".join(allN) + "\n"
            # print(row)
            _shallowFt = getShallowFeatureForFile(inputData, row.split(','), [-1,0])
            shallowFt = numpy.asarray([float(_shallowFt[3]), float(_shallowFt[4])])
            # print(shallowFt)
            # print('shallow ft', _shallowFt)
            predictLable = clf2.predict(shallowFt.reshape((1,-1)))
            allN_highlight = []
            for i in range(len(allN)):
                allN_highlight.append(allN[i])
                for j in range(len(blwN)):
                    if (allN[i] == blwN[j]):
                        allN_highlight[i] = '<b>' + allN_highlight[i] + '</b>'
                        # print('aaaaaaaaa', allN_highlight[i], blwN[j])

            output = [' <font size ="4">NỘI DUNG TẬP TIN: </font> <br><br>' + inputData, ' <font size ="4">TỈ LỆ TỪ CƠ BẢN:    ' +str(ratio) + " %</font>", ' <font size ="4">CÁC DANH TỪ TÌM ĐƯỢC (CÁC TỪ CƠ BẢN ĐƯỢC <b>IN ĐẬM</b>): </font><br><br>' + "; ".join(allN_highlight), ' <font size ="4">CẤP ĐỘ DỄ ĐỌC (CÓ 3 CẤP ĐỘ: 1, 2, 3; CÀNG THẤP CÀNG DỄ ĐỌC):    ' +  str(int(predictLable[0])) + '</font>']
            # output = "upload file complete"
        else:
            output = ['<font size ="4">TẢI LÊN KHÔNG THÀNH CÔNG!</font>']
        # print(output)
        timecost = '<font size ="4"><b>TỔNG THỜI GIAN TÍNH TOÁN CẦN THIẾT:      </b>' + str(int((time.time() - START_TIME))) + ' GIÂY</font>'
        return render(request, 'demosite/demosite.html', {'output': output, 'time': timecost})
    else:
        return render(request, 'demosite/demosite.html')
