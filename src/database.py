import psycopg2
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import config
from src.connectionDb_pool import ConnectionPool

class DatabasePsql:
    def __init__(self, database_config_path):
        self.database_config_path = database_config_path
        self.connPool = ConnectionPool("tests\database_test.ini")
    
    def load_data_from_database(self, query):
        
        conn_db= self.connPool.get_conn()
        try:
            with conn_db.cursor() as cur:
                cur.execute(query)
                data =  cur.fetchall()
                self.connPool.release_conn(conn_db)
                return data
        except Exception as e:
            print(f"Error during database operation: {e}")
            self.connPool.release_conn(conn_db)
            return None
        
    def write_data_to_database(self, query):
        try:  
            conn_db = self.connPool.get_conn()
            cur = conn_db.cursor()
            cur.execute(query)
            conn_db.commit()
            self.connPool.release_conn(conn_db)
            return True
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            conn_db.rollback()
            self.connPool.release_conn(conn_db)
            return False
            

    
    
        
    
        
