import pandas as pd
from mongo_conn import MongoConnection
import pymongo 

def get_coll_data(db_conn, coll_name):
    db = db_conn.get_mongo_client_db()
    coll = db[coll_name]
    customer_coll_doc_cursor = coll.find()

    df = pd.json_normalize(customer_coll_doc_cursor)
    df.drop(columns=["_id"], inplace= True)
    df.drop_duplicates(inplace=True)
    return df

"""
mydb_con = MongoConnection()
print(get_coll_data(mydb_con, "customer_data"))
"""