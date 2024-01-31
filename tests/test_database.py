import unittest
import sys
import time
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src import database, connectionDb_pool


import threading

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.db = database.DatabasePsql("tests\database_test.ini")
        self.connPool = connectionDb_pool.ConnectionPool("tests\database_test.ini")

        
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
            try:
                response = self.db.load_data_from_database("SELECT * FROM users;")
                print(f'Thread number: {i}, response: {response}')
            except Exception as e:
                print(f"Thread not executed: {i}, error: {e}")
                
        start = time.perf_counter()
        
        threads = []
        for i in range(5000):
            thread = threading.Thread(target=db_read, args=(i,))
            thread.start()
            threads.append(thread)
            
        for thread in threads:
            thread.join()

        finish = time.perf_counter()
        print(f"Finished in {round(finish-start,2)} second(s)")
        
    def test_acquire_and_release_connection(self):
        conn = self.connPool.get_conn()
        self.assertIsNotNone(conn)
        self.connPool.release_conn(conn)
        self.assertEqual(self.connPool.active_conn, 0)
        self.assertEqual(self.connPool.queue.qsize(), 10)
    



        