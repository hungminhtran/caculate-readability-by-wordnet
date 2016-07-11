from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def index(request):
    try:
        return render(request, 'demosite/demosite.html', {'output': str(request.POST['textData']), })
    except:
        return render(request, 'demosite/demosite.html', {'output': 'click submit to get output', })
