import psycopg2
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import config

import threading
import queue
import time  
import random
class ConnectionPool():
    def __init__(self, database_config_path):
        self.database_config_path = database_config_path
        self.min_conn = 10
        self.max_conn = 100
        
        #self.active_conn = 0 #aktywne połączenia
        self.queue = queue.Queue(self.max_conn) #zalokowane połączenia
        
        self.lock = threading.Lock() #watek zablokowany
        self.open_threads_connections() #startowe połączeni
        
        self.cleanup_thread = threading.Thread(target=self.cleanup_connections, daemon=True)
        self.cleanup_thread.start()
        
        self.status_thread = threading.Thread(target=self.checking_status, daemon=True)
        self.status_thread.start()
    
    def open_threads_connections(self):
        '''Na start tworzymy 10 zalokowanych połączeń jako wartość minimalna'''
        with self.lock:
            for _ in range(self.min_conn):
                self.queue.put(self.connect_db())
    
    def connect_db(self):
        """Connect to the PostgreSQL database server"""
        params = config.config_params(self.database_config_path)
        conn = psycopg2.connect(**params) # Wait for the thread to finish      
        return {"Connection": conn, "created_at": time.time()}
            
    def get_conn(self):
        '''Pobiera połączenie z queue i uzywa je do zapytania, jezli kolejka jest pusta tworzy kolejne'''
        with self.lock:
            try:
                conn_db_obj = self.queue.get()
            except self.queue.empty():
                if self.queue.qsize() < self.max_conn:
                    conn_db_obj = self.connect_db()
                else:
                        raise ValueError("Connection limit reached 100!") 
            return conn_db_obj
        
    def release_conn(self, conn_db):
        '''Odklada do queue uzyte połączenie'''
        with self.lock:
            self.queue.put(conn_db) 
              
    def cleanup_connections(self):
        while True:
            time.sleep(60)
            while not self.queue.empty():
                conn_db_obj = self.queue.get()
                if time.time() - conn_db_obj["created_at"] < 60:  # Keep connections active for the last minute
                    self.queue.put(conn_db_obj)
                else:
                    conn_db_obj["Connection"].close()
              
    def checking_status(self):
        while True:
            time.sleep(5)
            return self.queue.qsize()
               
    #do wyrzucenia                
    def check_queue_pool(self):
        "Funkcja która zamyka nie potrzebne active conn"
        
        with self.lock:
            while True:
                if self.active_conn > self.min_conn:
                    conn_db = self.queue.get()
                    conn_db.close()
                    #self.active_conn -= 1
                    
                elif self.active_conn < self.min_conn:
                    self.queue.put(self.connect_db())
                    #self.active_conn += 1
                else:
                    return False
            