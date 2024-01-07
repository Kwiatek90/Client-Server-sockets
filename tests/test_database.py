import unittest
import sys
import time
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src import users
from src import database
import threading

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.db = database.DatabasePsql("tests\database_test.ini")
        
        
    def test_crash_with_5000_query_to_database_when_over_each_iteration_db_connect(self):
        querys = ["SELECT * FROM users;" for _ in range(10)]
        
        for i, query in enumerate(querys):
            db = database.DatabasePsql("tests\database_test.ini")
            with db.conn_db.cursor() as cur:
                cur.execute(query)
                response =  cur.fetchall()
                print(f'Iteration {i}, response: {response}')
                cur.close()  
        
    def test_crash_with_5000_query_to_database(self):
        start = time.perf_counter()
        
        querys = ["SELECT * FROM users;" for _ in range(5000)]
        
        for i, query in enumerate(querys):
            response = self.db.load_data_from_database(query)
            print(f'Iteration {i}, response: {response}')
            
        finish = time.perf_counter()
        print(f"Finished in {round(finish-start,2)} second(s)")
        
    def test_crash_with_5000_query_to_databsae_using_threads(self):
        def db_read(i):
            response = self.db.load_data_from_database("SELECT * FROM users;")
            print(f'Numer wątku: {i}, response: {response}')
        
        start = time.perf_counter()
        
        threads = []
        for i in range(5000):
            thread = threading.Thread(target=db_read, args=(i,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
            
        while True:
            try: 
                print(f"Połączenia: {self.db.connPool.checking_status()}")
            except KeyboardInterrupt:
                return False
            
        finish = time.perf_counter()
        print(f"Finished in {round(finish-start,2)} second(s)")
    




        