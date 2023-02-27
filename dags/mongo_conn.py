import pymongo 
import json

class MongoConnection:
    def __init__(self) -> None:
        with open("dags/creds.json") as creds:
            values = json.load(creds)
            creds.close()
        self.database = values['db-mongo']
        self.user = values['user-mongo']
        self.password = values['pss-mongo']
        self.host = values['host-mongo']

    def get_mongo_client_db(self):
        mongo_client = pymongo.MongoClient('mongodb://root:example@mongodb-dev:27017/', directConnection=True)
        print("connected to mongo")
        print(mongo_client.list_database_names())
        return mongo_client[self.database]
    