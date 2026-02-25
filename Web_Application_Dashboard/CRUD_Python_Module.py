# Example Python Code to Insert a Document 

from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    """def __init__(self): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = 'aacuser' 
        PASS = 'SNHU1234' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)]
        self.counters = self.database["counters"]"""
    
    def __init__(self, username="aacuser", password="SNHU1234"):
        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'

        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (username, password, HOST, PORT))
        self.database = self.client[DB]
        self.collection = self.database[COL]
        self.counters = self.database["counters"]


    

    # Create a method to return the next available record number for use in the create method
    
    def get_next_record_number(self, counter_name="animals_record_id"):
        
        
        doc = self.counters.find_one_and_update(
            {"_id": counter_name},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return doc["seq"]
            
        
        
        
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        """ if-statement that rejects empty and non-dictionary documents """
        if data is None or not isinstance(data, dict) or len(data) == 0:
            return False

        """ checks if data has a record id. If not, the get_next_record_number function will assign the next available id record number """
        try:
            if "record_id" not in data:
                data["record_id"] = self.get_next_record_number()
        
        #inserts the data into the  mongoDB collection and returns True if successful, else False.
            result = self.collection.insert_one(data)
            return result.acknowledged is True
        
        #Crash / exception handling
        except PyMongoError:
            return False
        except Exception:
            return False

            
            
            
    # Create method to implement the R in CRUD.
    
    def read(self, query=None):
        """ if there is no specific query provided, return all documents """
        if query is None:
            query = {}

        """ if there is no existing document per the assigned query, the read method will return """
        if not isinstance(query, dict):
            return []

        """ utilizes the find function, then assigns it to cursor. Cursor is then returned """
        try:
            cursor = self.collection.find(query) 
            return list(cursor)
        except PyMongoError:
            return []
        except Exception:
            return []
        
    # An Update method that queries for and changes document(s) from a specified MongoDB database and specified collection
    def update(self, query, update_data):
        """if query data does not exist or update_data is not presented in dictionary format, return the value 0"""
        if not isinstance(query, dict) or not isinstance(update_data, dict):
            return 0
        """if either query or update_data is empty, return the value 0"""
        if len(query) == 0 or len(update_data) == 0:
            return 0
        
        """using the update_many statement on the query data to update it to the update_data, then returning the number of modified values"""
        try:
            result = self.collection.update_many(query,{"$set": update_data})
            return result.modified_count
        except PyMongoError:
            return 0
        except Exception:
            return 0
        
        
    #A Delete method that queries for and removes document(s) from a specified MongoDB database and specified collection
    def delete(self, query):
        """if query is empty or not in dictionary format or if the query is empty, return the value 0"""
        if query is None or not isinstance(query, dict) or len(query) == 0:
            return 0
        
        """Delete a single document matching query and return number removed."""
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        
        except PyMongoError:
            return 0
        except Exception:
            return 0
        