'''
Created on Jun 3, 2015

@author: aclosca
'''
import pymongo

from pymongo import MongoClient

class TableGenerator():
    '''
    classdocs
    '''


    def __init__(self, TestConfiguration,NumberOfOperations):
        '''
        Constructor
        '''
        self.NumberOfOperations=NumberOfOperations
        self.TestConfiguration=TestConfiguration
    
    def createTables(self):
        configuration=self.TestConfiguration
        client = MongoClient()
        db=client.database
        if 'readState' in configuration:
            db.insert_collection.insert_one({"create":"insertCollection"})
        if 'writeState' in configuration:
            db.write_collection.insert_one({"create":"writeCollection"})
        if 'updateState' in configuration:
            db.update_collection.insert_one({"create":"updateCollection"})
                
            
        
    
        
        
            
    
        