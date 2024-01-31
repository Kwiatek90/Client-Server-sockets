import psycopg2
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import config
import threading
from queue import Queue
import time  
class ConnectionPool():
    def __init__(self, database_config_path):
        self.database_config_path = database_config_path
        self.min_queue_conn = 10
        self.max_conn = 50
        self.queue = Queue()
        self.active_conn = 0
        self.release_conn_quant = 0   
        self.start_time = time.time()
        self.semaphore = threading.Semaphore()
        self.open_threads_connections()
        self.cleanup_thread = threading.Thread(target=self.cleanup_connections, daemon=True)
        self.cleanup_thread.start()
    
    def open_threads_connections(self):
        '''At the beginning create a 10 locked connections in queue'''
        
        with self.semaphore:
            for _ in range(self.min_queue_conn):
                self.queue.put(self.connect_db())
    
    def connect_db(self):
        """Connect to the PostgreSQL database server"""
        
        try:
            params = config.config_params(self.database_config_path)
            conn = psycopg2.connect(**params)
            return conn
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise
        
    def get_conn(self):
        '''Take the connection from queue, if queue is empty, create one'''
        
        with self.semaphore:
            if self.queue.empty():
                if ( self.queue.qsize() + self.active_conn ) < self.max_conn:
                    self.active_conn +=1
                    return self.connect_db()
                
                else:
                    raise ValueError("Too much connections!")
                        
            else:
                self.active_conn += 1
                return self.queue.get()
                   
    def release_conn(self, conn_db_obj):
        '''Release connection to the queue'''
        
        with self.semaphore:
            self.queue.put(conn_db_obj) 
            self.release_conn_quant += 1
            self.active_conn -= 1
        
    def cleanup_connections(self):
        '''Every 60 seconds function check connections'''
        
        while True:
            time.sleep(60)
            with self.semaphore:
                print(f"Time: {round(time.time() - self.start_time, 2)}\nActive connections: {self.active_conn}\nQueue size: {self.queue.qsize()}\nRelease: {self.release_conn_quant}")
                while not self.queue.empty():
                    if self.queue.qsize() > self.min_queue_conn:
                        conn_db_obj = self.queue.get()
                        conn_db_obj.close()
                        self.active_conn -= 1
              