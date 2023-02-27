# imports important for Airflow
import pendulum
from airflow.decorators import dag, task

# Import Modules for code
import json
import pandas as pd
import datetime as dt
import psycopg2 
import pymongo 
import datetime

# import custom code for extract and transform
from mongo_conn import MongoConnection
from postgres_conn import PostgresConnection
from extract_mongo_data import get_coll_data
from extract_oltp_data import get_oltp_data
# [START instantiate_dag]
@dag(
    schedule_interval= '0 0 * * *',                             
    start_date=pendulum.datetime(2023, 2, 27, tz="UTC"), 
    catchup=False,               
    tags=['BankayaTest']
)
def ETLOdsBankayaPurchases():
    """
    This is a simple data pipeline to load OLTP data to BankayaTest Data
    Warehouse, orchestrated with Airflow 
    """

    # EXTRACT: Query the data from OLTP and MongoDB
    @task()
    def extract():
        oltp_conn = PostgresConnection('oltp').create_postgres_engine()
        oltp_conn.connect()
        mongo_conn = MongoConnection()

        dw_conn = PostgresConnection('dw').create_postgres_engine()
        dw_conn.connect()

        #Extract Mongo DB data
        customer_mongo_data = get_coll_data(mongo_conn, "customer_data")
        item_mongo_data = get_coll_data(mongo_conn, "items_data")

        # Extract OLTP data (postgres)
        customer_oltp_data = get_oltp_data(oltp_conn= oltp_conn, table_name="customer")
        items_oltp_data = get_oltp_data(oltp_conn= oltp_conn, table_name="item")
        purchase_oltp_data = get_oltp_data(oltp_conn= oltp_conn, table_name="item_bought")

        # Load to TMP Mongo
        customer_mongo_data.to_sql(name= "customer_mongo", 
                                   con= dw_conn,
                                   schema= "tmp",
                                   if_exists= "replace",
                                   index= False)
        item_mongo_data.to_sql(name= "item_mongo", 
                                   con= dw_conn,
                                   schema= "tmp",
                                   if_exists= "replace",
                                   index= False)
        
        # Load to TMP OLTP
        customer_oltp_data.to_sql(name= "customer_oltp", 
                                   con= dw_conn,
                                   schema= "tmp",
                                   if_exists= "replace",
                                   index= False)
        items_oltp_data.to_sql(name= "item_oltp", 
                                   con= dw_conn,
                                   schema= "tmp",
                                   if_exists= "replace",
                                   index= False)
        purchase_oltp_data.to_sql(name= "purchase_oltp", 
                                   con= dw_conn,
                                   schema= "tmp",
                                   if_exists= "replace",
                                   index= False)                        
        return {"task_id": "extract", "status": "completed", "message": "Data loaded in DW TMP schema"}
    
    @task
    def transform_mongo_data(payload_extract):
        dw_conn = PostgresConnection('dw').create_postgres_engine()
        dw_conn.connect()

        # Read data from TMP customer mongo and perform some cleaning before loading to stg
        tmp_customer_df = pd.read_sql("SELECT * FROM tmp.customer_mongo", dw_conn)
        tmp_customer_df["firstname"] = tmp_customer_df["firstname"].str.upper()
        tmp_customer_df["lastname"] = tmp_customer_df["lastname"].str.upper()

        tmp_customer_df.to_sql(name= "customer_mongo", 
                                   con= dw_conn,
                                   schema= "stg",
                                   if_exists= "replace",
                                   index= False) 
        # Read data from TMP customer mongo and perform some cleaning before loading to stg
        tmp_item_df = pd.read_sql("SELECT * FROM tmp.item_mongo", dw_conn)
        tmp_item_df["title"] = tmp_item_df["title"].str.upper()
        tmp_item_df["price"] = tmp_item_df["price"] * 20.0 # get price in pesos (dummy exchange value)

        tmp_item_df.to_sql(name= "item_mongo", 
                                   con= dw_conn,
                                   schema= "stg",
                                   if_exists= "replace",
                                   index= False)  
        return {"task_id": "transform_mongo_data", "status": "completed", "message": "Mongo Cleaned Data loaded in DW ODS schema"}

    @task
    def transform_oltp_data(payload_extract):
        dw_conn = PostgresConnection('dw').create_postgres_engine()
        dw_conn.connect()

        # Read data from TMP customer mongo and perform some cleaning before loading to stg
        tmp_customer_df = pd.read_sql("SELECT * FROM tmp.customer_oltp", dw_conn)
        tmp_customer_df["first_name"] = tmp_customer_df["first_name"].str.strip().str.upper()
        tmp_customer_df["last_name"] = tmp_customer_df["last_name"].str.strip().str.upper()
        tmp_customer_df["curp"] = tmp_customer_df["curp"].str.strip().str.upper()
        tmp_customer_df["rfc"] = tmp_customer_df["rfc"].str.strip().str.upper()

        tmp_customer_df.to_sql(name= "customer_oltp", 
                                   con= dw_conn,
                                   schema= "stg",
                                   if_exists= "replace",
                                   index= False) 
        # Read data from TMP customer mongo and perform some cleaning before loading to stg
        tmp_item_df = pd.read_sql("SELECT * FROM tmp.item_oltp", dw_conn)
        tmp_item_df["name_description"] = tmp_item_df["name_description"].str.upper()

        tmp_item_df.to_sql(name= "item_oltp", 
                                   con= dw_conn,
                                   schema= "stg",
                                   if_exists= "replace",
                                   index= False)
        # Read data from TMP purchase mongo and perform some cleaning before loading to stg
        tmp_purc_df = pd.read_sql("SELECT * FROM tmp.purchase_oltp", dw_conn)
        tmp_purc_df["total_amount"] = tmp_purc_df["total_amount"] * 20.0 

        tmp_purc_df.to_sql(name= "purchase_oltp", 
                                   con= dw_conn,
                                   schema= "stg",
                                   if_exists= "replace",
                                   index= False)  
        return {"task_id": "transform_mongo_data", "status": "completed", "message": "OLTP Cleaned Data loaded in DW ODS schema"}
    
    @task
    def load_oltp_data(payload_transform):
        dw_conn = PostgresConnection('dw').create_postgres_engine()
        dw_conn.connect()

        now = datetime.datetime.now().date()
        date_replication = now.strftime("%Y-%m-%d")

        stg_customer_df = pd.read_sql("SELECT * FROM stg.customer_oltp", dw_conn)
        ods_customer_ids_df = pd.read_sql("SELECT * FROM ods.customer_oltp", dw_conn)["id_oltp"]

        stg_customer_df = stg_customer_df[~stg_customer_df["id"].isin(ods_customer_ids_df)] # Load only new customers data
        stg_customer_df["replication_date"] = pd.to_datetime(date_replication)
        stg_customer_df = stg_customer_df.rename(columns={"id": "id_oltp"})

        stg_item_df = pd.read_sql("SELECT * FROM stg.item_oltp", dw_conn)
        ods_item_ids_df = pd.read_sql("SELECT * FROM ods.item_oltp", dw_conn)["id_oltp"]

        stg_item_df = stg_item_df[~stg_item_df["id"].isin(ods_item_ids_df)] # Load only new items data
        stg_item_df["replication_date"] = pd.to_datetime(date_replication)
        stg_item_df = stg_item_df.rename(columns={"id": "id_oltp"})

        stg_purc_df = pd.read_sql("SELECT * FROM stg.purchase_oltp", dw_conn)
        ods_purc_ids_df = pd.read_sql("SELECT * FROM ods.purchase_oltp", dw_conn)["order_id"]

        stg_purc_df = stg_purc_df[~stg_purc_df["order_id"].isin(ods_purc_ids_df)] # Load only new items data
        stg_purc_df["replication_date"] = pd.to_datetime(date_replication)

        stg_customer_df.to_sql(name="customer_oltp",
                               con= dw_conn,
                               schema= "ods",
                               if_exists= "append",
                               index= False)
        stg_item_df.to_sql(name="item_oltp",
                               con= dw_conn,
                               schema= "ods",
                               if_exists= "append",
                               index= False)
        stg_purc_df.to_sql(name="purchase_oltp",
                               con= dw_conn,
                               schema= "ods",
                               if_exists= "append",
                               index= False)
        
    @task
    def load_mongo_data(payload_transform):
        dw_conn = PostgresConnection('dw').create_postgres_engine()
        dw_conn.connect()

        now = datetime.datetime.now().date()
        date_replication = now.strftime("%Y-%m-%d")

        stg_customer_df = pd.read_sql("SELECT * FROM stg.customer_mongo", dw_conn)
        ods_customer_ids_df = pd.read_sql("SELECT * FROM ods.customer_mongo", dw_conn)["cust_id_mongo"]

        stg_customer_df = stg_customer_df[~stg_customer_df["cut_id"].isin(ods_customer_ids_df)] # Load only new customers data
        stg_customer_df = stg_customer_df.rename(columns={"cut_id": "cust_id_mongo"})

        stg_item_df = pd.read_sql("SELECT * FROM stg.item_mongo", dw_conn)
        ods_item_ids_df = pd.read_sql("SELECT * FROM ods.item_mongo", dw_conn)["item_id_mongo"]

        stg_item_df = stg_item_df[~stg_item_df["item_id"].isin(ods_item_ids_df)] # Load only new items data
        stg_item_df = stg_item_df.rename(columns={"item_id": "item_id_mongo"})
        stg_customer_df.to_sql(name="customer_mongo",
                               con= dw_conn,
                               schema= "ods",
                               if_exists= "append",
                               index= False)
        stg_item_df.to_sql(name="item_mongo",
                               con= dw_conn,
                               schema= "ods",
                               if_exists= "append",
                               index= False)


    bankaya_data = extract()
    mongo_bankaya_data = transform_mongo_data(bankaya_data)
    oltp_bankaya_data = transform_oltp_data(bankaya_data)
    load_mongo_data(mongo_bankaya_data)
    load_oltp_data(oltp_bankaya_data)

bankaya_puschases_dag = ETLOdsBankayaPurchases()
