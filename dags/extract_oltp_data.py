import pandas as pd
from postgres_conn import PostgresConnection
import sqlalchemy
from sqlalchemy import text

def get_oltp_data(oltp_conn, table_name: str) -> pd.DataFrame:
    q = f"SELECT * FROM bankaya.{table_name}"
    print(q)
    return pd.read_sql(q, oltp_conn)
