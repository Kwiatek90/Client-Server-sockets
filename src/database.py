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
        finally:#spradzic czy to sie wyoknuje
            if self.conn_db is not None:
                self.conn_db.close()
                print('Database connection closed.')
                
    def load_users_from_database(self):
        query = "SELECT name, password, is_admin FROM users;"
        cur = self.conn_db.cursor()
        cur.execute(query)
        data =  cur.fetchone()
        cur.close()
        return data
        
    
        
