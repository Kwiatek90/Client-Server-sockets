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
        
        self.active_conn = 0 #aktynwe thready uzyte do zapytan
        self.queue = queue.Queue(self.max_conn) #kolejka threadów
        self.all_conn_quantity = self.active_conn + self.queue.qsize()
        
        self.lock = threading.Lock() #watek zablokowany
        self.open_threads_connections() #startowe połączenia
        self.err = 0
    
    def connect_db(self):
        """Connect to the PostgreSQL database server"""
        try:
            params = config.config_params(self.database_config_path)
            conn = psycopg2.connect(**params)
            return conn
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            conn.close()
            
    def open_threads_connections(self):
        '''Na start tworzy 10 połączeń'''
        with self.lock:
            for _ in range(self.min_conn):
                self.queue.put(self.connect_db())
        
    def put_conn_db(self, conn_db):
        '''Odklada od queue uzyte połączenie'''
        with self.lock:
            self.queue.put(conn_db) 
            self.active_conn -= 1  
            
    def get_conn_db(self):
        '''Pobiera połączenie z queue i uzywa je do zapytania, jezli kolejka jest pusta tworzy kolejne'''
        with self.lock:
            if self.queue.empty():
                if self.active_conn < self.max_conn:
                    try:
                        self.active_conn += 1
                        self.queue.put(self.connect_db())
                        return self.queue.get()
                    except:
                        self.err +=1
                        print("błąd")
                else:
                    self.err +=1
                    raise ValueError("Za duzo połączeń") 
            else:
                self.active_conn += 1
                return self.queue.get()
                # to returnuje conn_cb gdzie mozemy juz pobierac dane
                
    def check_queue_pool(self):
        pass
    
    
    #### teraz chuj wie tak naprawde sprawdzic zalecenie, pobieranie i wrzucanie con n dziala, 
    # zobaczyc u kogos na filmiku jak to dziala
    ### jeszcze trzeba jakic conn check zrobic co sprawdza co minute ile jest poloaczen i jest usuwa
        
            
                