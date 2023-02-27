import pymongo 


def insert_multiple_docs_in_coll(collection, list_of_rows):
    # write the documents to the collection
    docs_inserted = collection.insert_many(list_of_rows)
    print("Docs inserted with ids: \n", docs_inserted.inserted_ids) 

# Connect to mongodb
myclient = pymongo.MongoClient("mongodb://localhost:27017/",username='root',password='example')
print("connected")

# List the DBs and Collections to create
db_name = 'bankaya-nosql'
coll_customer_name = "customer_data"
coll_item_name = "items_data"
coll_orders_name = "orders_name"

# Create db, collections and insert data
mydb = myclient[db_name]
my_customer_coll = mydb[coll_customer_name]

list_customers_docs = [
    {"cut_id": 1,"firstname": 'Bruce', "lastname": 'Wayne'},
    {"cut_id": 2,"firstname": 'Clark', "lastname": 'Kent'},
    {"cut_id": 3,"firstname": 'Tony', "lastname": 'Stark'}]

insert_multiple_docs_in_coll(my_customer_coll, list_customers_docs)

# Create db, collections and insert data
my_item_coll = mydb[coll_item_name]

list_item_docs = [
    {"item_id": 1,"title": 'USM', "price": 10.2},
    {"item_id": 2,"title": 'Mouse', "price": 12.23},
    {"item_id": 3,"title": 'Monitor', "price": 199.99}]

insert_multiple_docs_in_coll(my_item_coll, list_item_docs)

# Create db, collections and insert data
my_orders_coll = mydb[coll_orders_name]

list_orders_docs = [
    { 
        "order_id": 101203,
        "created_ts": '2023-02-24 19:05:32.000',
        "customer_id": 1,
        "items": [
            {"item_id": 1, "quantity": 1},
            {"item_id": 2, "quantity": 1}
        ],
        "amount_total": 22.43
    },
        { 
        "order_id": 101203,
        "created_ts": '2023-02-24 20:05:32.000',
        "customer_id": 3,
        "items": [
            {"item_id": 3, "quantity": 1}
        ],
        "amount_total": 199.99
    }
    ]

insert_multiple_docs_in_coll(my_orders_coll, list_orders_docs)



