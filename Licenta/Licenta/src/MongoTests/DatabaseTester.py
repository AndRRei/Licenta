'''
Created on Jun 4, 2015

@author: aclosca
'''
import pymongo
import datetime 
import json
from pymongo import MongoClient

class DatabaseTester():
    '''
    classdocs
    '''


    def __init__(self, TestConfiguration,NumberOfOperations):
        '''
        Constructor
        '''
        self.NumberOfOperations=NumberOfOperations
        self.TestConfiguration = TestConfiguration
        
    def test(self):
        configuration=self.TestConfiguration
        client = MongoClient()
        db=client.database
        print (db.collection_names());
        if 'write_collection' in db.collection_names():
            s=self.createKeyContentBySize(configuration)
            documents =[]
            for i in range (1,int(self.NumberOfOperations)):
                document=self.createDocument(configuration,s)
                documents.append(document)
            print(documents)    
            a = datetime.datetime.now()
            db.write_collection.insert_many(documents)
            b = datetime.datetime.now()
            c=b-a
            return c.microseconds
        db.insert_collection.drop()
        db.update_collection.drop()
        db.write_collection.drop()
    def createDocument(self,TestConfiguration,s):
        document = {}
        key=""
        for i in range (1,int(self.TestConfiguration['writeKeys'])):
            key ="key" + str(i)
            document.update({key : s})
        return document    
        
    def createKeyContentBySize(self,TestConfiguration):
        s=""
        for i in range(1,int(self.TestConfiguration['writeSize'])):
            s+="a"
        return s    
        
        
        
        
        
        
            
            
        
        
        