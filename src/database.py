import psycopg2
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import config
from src.connectionDb_pool import ConnectionPool

class DatabasePsql:
    def __init__(self, database_config_path):
        self.database_config_path = database_config_path
        self.conn_db = self.connect_db() #old connection
        self.connPool = ConnectionPool("tests\database_test.ini")
    
    def connect_db(self):
        """Connect to the PostgreSQL database server"""
        try:
            params = config.config_params(self.database_config_path)
            conn = psycopg2.connect(**params)
            return conn
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            conn.close()
                 
    def load_data_from_database(self, query):
        conn_db_obj = self.connPool.get_conn()
        conn_db = conn_db_obj["Connection"]
        with conn_db.cursor() as cur:
            cur.execute(query)
            data =  cur.fetchall()
            self.connPool.release_conn(conn_db_obj)
            cur.close()
            return data
        
    def write_data_to_database(self, query):
        try:  
            conn_db = self.connPool.get_conn_db()
            cur = conn_db.cursor()
            cur.execute(query)
            self.conn_db.commit()
            return True
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            self.conn_db.rollback()
            return False
            

    
    
        
    
        
