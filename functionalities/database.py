import psycopg2
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import config

class DatabasePsql:
    def __init__(self):
        self.conn_db = self.connect_db()
    
    def connect_db(self):
        """Connect to the PostgreSQL database server"""
        conn = None
        try:
            params = config.config_params()
            print(params)
            conn = psycopg2.connect(**params)
            
            return conn
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            conn.close()
        #finally:
        #    if conn_db is not None:
        #        conn_db.close()
        #        print('Database connection closed.')
        
        
