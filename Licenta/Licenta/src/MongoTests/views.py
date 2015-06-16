import threading
import time
import json
import psutil
import os
import collections

from django.forms.models import modelform_factory
from django.forms import ModelForm
from MongoTests.models import TestConfiguration
from django.http import HttpResponse
from django import forms
from django.shortcuts import render
from MongoTests.TableGenerator import TableGenerator
from MongoTests.DatabaseTester import DatabaseTester


class TestConfigurationForm(ModelForm):
    class Meta:
        model =TestConfiguration
        fields =['readState','readPercentage','readKeys','readSize',
                    'writeState','writePercentage','writeKeys','writeSize',
                    'updateState','updatePercentage','updateKeys','updateSize']
        
class myThread (threading.Thread):
    currentNumberOfOps=0
    
    def __init__(self,tester):
        threading.Thread.__init__(self)
        self.tester=tester
    def run(self):
        self.tester.test()
    def getCurrentNumberOfOps(self):
        self.currentNumberOfOps=self.tester.status
        return self.currentNumberOfOps
    def getThreadId(self):
        return threading.get_ident()
        
        
        
       

        
       
                
       
t1=myThread(0)
isThreadStarted=False;
# def base(request):
#     return render(request , 'base.html')
# def tests(request):
#     return render(request, 'tests.html', {'form': NameForm})
def dashboard(request):
    Form = modelform_factory(TestConfiguration,form=TestConfigurationForm)
    return render(request,'dashboard.html',{'form':Form})
def saveTestConfiguration(request):
    configuration = TestConfiguration()
    configuration = request.POST
    request.session["test_configuration"]=configuration
    return HttpResponse(json.dumps(configuration),content_type = "application/json");
def testMongoDB(request):
    cr=TableGenerator(request.session["test_configuration"],request.POST.get('NumberOfOperations',False))
    cr.createTables()
    tester = DatabaseTester(request.session["test_configuration"],request.POST.get('NumberOfOperations',False))
    #time_interval=tester.test()
    #global status
    #status=tester.status;
    global t1
    t1=myThread(tester)
    t1.start()
    global isThreadStarted
    isThreadStarted=True
    
    return HttpResponse("Thread for test was started");
def getTestStatus(request):
    global isThreadStarted
    isFinished=0;
    currentNumberOfOps=0;
    if(isThreadStarted==True):
        
        currentNumberOfOps=t1.getCurrentNumberOfOps()
        if not t1.isAlive():
            isFinished=1;
            isThreadStarted=False
        data={}
        data['currentNumberOfOperation']=currentNumberOfOps;
        data['isFinished']=isFinished;
        data['isTableCreated']=1
        return HttpResponse(json.dumps(data),content_type = "application/json");
    else:
        data={}
        data['isTableCreated']=0
        return HttpResponse(json.dumps(data),content_type = "application/json");
def getCPUUsage(request):
    data={}
    global isThreadStarted
    global t1
    proc = psutil.Process()
    c=collections.Counter(proc.threads())
    if(t1.isAlive()):
        for thread in c.elements():
            if(thread.id==t1.getThreadId()):
                data['CPUUsage']=proc.cpu_percent(interval=1)
    else:
        data['CPUUsage']=0
    
    data['totalCPUUsage']=psutil.cpu_percent()             
    data['memoryUsage']=psutil.virtual_memory().percent
    return HttpResponse(json.dumps(data),content_type = "application/json");
    

    
