# database.py (updated)
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        """Initialize database connection"""
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/user_db')
        try:
            self.client = MongoClient(mongo_uri)
            db_name = mongo_uri.split('/')[-1]
            self.db = self.client[db_name]
            print(f"Connected to MongoDB: {mongo_uri}")
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise

    def get_collection(self, collection_name):
        """Get collection by name"""
        return self.db[collection_name]

    def close(self):
        """Close the database connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

# Initialize the database instance
db = Database()







# import os
# from pymongo import MongoClient
# from pymongo.errors import ConnectionFailure

# class Database:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(Database, cls).__new__(cls)
#             cls._instance.client = None
#             cls._instance.db = None
#             cls._instance.initialize()
#         return cls._instance

#     def initialize(self):
#         """Initialize database connection"""
#         mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/user_db')
#         try:
#             self.client = MongoClient(mongo_uri)
#             # Extract database name from the URI
#             db_name = mongo_uri.split('/')[-1]
#             self.db = self.client[db_name]
#             print(f"Connected to MongoDB: {mongo_uri}")
#         except ConnectionFailure as e:
#             print(f"Failed to connect to MongoDB: {e}")
#             raise

#     def get_collection(self, collection_name):
#         """Get collection by name"""
#         return self.db[collection_name]

#     def close(self):
#         """Close the database connection"""
#         if self.client:
#             self.client.close()
#             print("MongoDB connection closed")