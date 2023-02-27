# DE-BankayaTest
Repo project for Bankaya Data Engineering Test

Project uses the next technologies:
-Airflow
-Python
-Pandas
-PostgreSQL
-MongoDB

This project creates an Data Pipeline to extract data from a PostgreSQL oltp database
and MongoDB and load it to a PostgreSQL olap database. 

Both OLTP and OLAP data lives in the same postgres server (localhost).

All services are set up with an docker compose file, based on an airflow modified image
to be able of connect with MongoDB

## Airflow auth
U y P: airflow

## Adminer (SQL Client) auth
U y P: airflow
H: postgres:5432

The Data Pipeline code is in dags/BankayaTestETL.py



