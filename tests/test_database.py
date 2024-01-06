import unittest
import sys
import time
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src import users
from src import database

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.db = database.DatabasePsql("tests\database_test.ini")
        
    def test_crash_with_5000_query_to_database(self):
        start = time.perf_counter()
        
        querys = ["SELECT * FROM users;" for _ in range(5000)]
        
        for query in querys:
            response = self.db.load_data_from_database(query)
        
        finish = time.perf_counter()
        print(f"Finished in {round(finish-start,2)} second(s)")