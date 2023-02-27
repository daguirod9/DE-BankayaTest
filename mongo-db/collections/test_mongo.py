import pymongo 

# Connect to mongodb
myclient = pymongo.MongoClient("mongodb://localhost:27017/",username='root',password='example')
print("connected")
# List the DBs and Collections to create
db_name = 'bankaya-nosql'
coll_customer_name = "customer"
coll_item_name = "items"
coll_to_create_list = [coll_customer_name, coll_item_name]


#Retrieve databases on MongoDB server an try to create if not exists
dblist = myclient.list_database_names()

print(dblist)