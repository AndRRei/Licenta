import threading
import time

from django.forms.models import modelform_factory
from django.forms import ModelForm
from MongoTests.models import TestConfiguration
from django.http import HttpResponse
from django import forms
from django.shortcuts import render
from MongoTests.CreateTables import TableGenerator
from MongoTests.DatabaseTester import DatabaseTester

class TestConfigurationForm(ModelForm):
    class Meta:
        model =TestConfiguration
        fields =['readState','readPercentage','readKeys','readSize',
                    'writeState','writePercentage','writeKeys','writeSize',
                    'updateState','updatePercentage','updateKeys','updateSize']
        
class myThread (threading.Thread):
    flagTablesCreated=0
    tablesCreated="Tables were created"
    totalNumOfOperations=0
    currentNumOfOperations=0
    status=1
    
    def __init__(self, totalNumOfOperations):
        threading.Thread.__init__(self)
        self.totalNumOfOperations=totalNumOfOperations
    def run(self):
        time.sleep(1)
        self.status="Tables created"
        time.sleep(1)
        self.currentNumOfOperations=self.totalNumOfOperations/5
        self.status=self.currentNumOfOperations 
        time.sleep(1)
        self.currentNumOfOperations=self.totalNumOfOperations/4
        self.status=self.currentNumOfOperations 
        time.sleep(1)
        self.currentNumOfOperations=self.totalNumOfOperations/3
        self.status=self.currentNumOfOperations 
        time.sleep(1)
        self.currentNumOfOperations=self.totalNumOfOperations/2
        self.status=+self.currentNumOfOperations 
        time.sleep(1)
        self.currentNumOfOperations=self.totalNumOfOperations
        self.status=+self.currentNumOfOperations
        time.sleep(1)
        self.status=0
        
        
       

        
       
                
       
t1 =myThread(0) 
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
    print (configuration)
    return HttpResponse("succes");
def testMongoDB(request):
    cr=TableGenerator(request.session["test_configuration"],request.POST.get('NumberOfOperations',False))
    cr.createTables()
    tester = DatabaseTester(request.session["test_configuration"],request.POST.get('NumberOfOperations',False))
    time_interval=tester.test()
    return HttpResponse("succes from test Mongo with : " + str(time_interval));


    
