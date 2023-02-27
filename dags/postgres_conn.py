from sqlalchemy import create_engine
import json

class PostgresConnection:
    def __init__(self, db_type: str) -> None:
        with open("dags/creds.json") as creds:
            values = json.load(creds)
            creds.close()
        if db_type == 'oltp':
            self.database = values['db-oltp']
        else:
            self.database = values["db-dw"]
        self.user = values['user-postgres']
        self.password = values['pss-postgres']
        self.host = values['host-postgres']
        self.port = values['port-postgres']

    def create_postgres_engine(self):
        parms = "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
            self.user,
            self.password,
            self.host,
            self.port,
            self.database
        )
        engine_sql = create_engine(parms, echo= False)
        
        return engine_sql
    

    
