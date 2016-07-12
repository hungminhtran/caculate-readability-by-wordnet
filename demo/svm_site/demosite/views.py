from . import module_2
mod2 = module_2
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
_tempfile = open('statics/input/vietnamesewn-nouns/all-vietnamesewn-BLW.txt', 'r')
BLWnounsArray = _tempfile.read()
_tempfile.close()
_tempfile = open('statics/input/vietnamesewn-nouns/all-vietnamesewn-SORTED-nouns.txt', 'r')
NounsArray = _tempfile.read()
_tempfile.close()

def index(request):
    # try:
    # _file = str(request.POST['textData'])
    _file = 'what the hell'
    # import pdb; pdb.set_trace()
    ratio, blwN, allN = mod2.calculateReabilityByWordnetForEnglish(_file, BLWnounsArray, NounsArray, 0, 0)
    output = 'result' + ","+str(ratio) + "," + " | ".join(blwN) + ","  + " | ".join(allN) + "\n"
    return render(request, 'demosite/demosite.html', {'output': output})
    # except:
    #     return render(request, 'demosite/demosite.html', {'output': 'click submit to get output', })
