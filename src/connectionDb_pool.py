import psycopg2
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import config

import threading
import queue
import time  
class ConnectionPool():
    def __init__(self, database_config_path):
        self.database_config_path = database_config_path
        self.min_conn = 10
        self.max_conn = 100
        
        self.queue = queue.Queue(self.max_conn)
        
        self.lock = threading.Lock()
        self.open_threads_connections()
        
        self.cleanup_thread = threading.Thread(target=self.cleanup_connections, daemon=True)
        self.cleanup_thread.start()
    
    def open_threads_connections(self):
        '''At the beginning we create a 10 locked connections in queue'''
        with self.lock:
            for _ in range(self.min_conn):
                self.queue.put(self.connect_db())
    
    def connect_db(self):
        """Connect to the PostgreSQL database server"""
        params = config.config_params(self.database_config_path)
        conn = psycopg2.connect(**params) # Wait for the thread to finish      
        return {"Connection": conn, "created_at": time.time()}
            
    def get_conn(self):
        '''Take the connection from queue, if queue is empty, create one. When the connection raise an exception, function create antoher '''
        conn_db_obj = None
        
        
        #teraz jest oki, trylko ze jak przychodzi queue do 0 to jest błąd
        with self.lock:
            try:
                if not self.queue.empty():
                    if self.queue.qsize() < self.max_conn:
                        conn_db_obj = self.queue.get()
                    else:
                        print("Connection limit reached 100!") 
                else:###tutjta trzeba sprawdzic te odkładanie połączeń
                    conn_db_obj = self.connect_db()
               
            except Exception as e:
                print(f"Error during work: {e}")
                if conn_db_obj:
                    conn_db_obj["Connection"].close()
                conn_db_obj = self.connect_db()
            finally:    
                return conn_db_obj
        
    def release_conn(self, conn_db_obj):
        '''Release connection to the queue'''
        with self.lock:
            self.queue.put(conn_db_obj) 
            print(f"Queue size {self.queue.qsize()}")
              
    def cleanup_connections(self):
        '''Every 60 seconds function check connections'''
        while True:
            time.sleep(60)
            while not self.queue.empty():
                print(self.queue.qsize())
                if self.queue.qsize() > self.min_conn:
                    conn_db_obj = self.queue.get()
                    if time.time() - conn_db_obj["created_at"] < 60:
                        self.queue.put(conn_db_obj)
                    else:
                        conn_db_obj["Connection"].close()
              