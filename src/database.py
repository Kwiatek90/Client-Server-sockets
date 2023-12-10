import psycopg2
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import config

class DatabasePsql:
    def __init__(self, database_config_path):
        self.database_config_path = database_config_path
        self.conn_db = self.connect_db()
        
    
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
        cur = self.conn_db.cursor()
        cur.execute(query)
        data =  cur.fetchall()
        cur.close()
        self.conn_db.close()
        return data
    
    def write_data_to_database(self, query):
        try:  
            cur = self.conn_db.cursor()
            cur.execute(query)
            self.conn_db.commit()
            return True
        except (Exception, psycopg2.Error) as error:
            response = ("Error while connecting to PostgreSQL", error)
            self.conn_db.rollback()
            return response
            

    
    
        
    
        
