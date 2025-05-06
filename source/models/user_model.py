from pymongo import MongoClient
import os
from flask import current_app

class MongoDB:
    def __init__(self, uri=None, db_name=None):
        self.uri = uri or current_app.config['MONGO_URI']
        self.db_name = db_name or current_app.config["MONGO_DB_NAME"]
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]

        self.users = self.db["users"]
        self.csv_data = self.db['csv_data']

    def close(self):
        if self.client:
            self.client.close()