import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src import database
from src import users

class ServerTests(unittest.TestCase):
    def setUp(self):
        self.db = database.DatabasePsql("tests\database_test.ini")
          
    def test_load_data_from_database(self):
        data = self.db.load_data_from_database("SELECT name, password, is_admin FROM users_test;")
        self.assertEqual(data, self.users_list_from_db)
        
    def test_write_data_to_database(self):
        query = "INSERT INTO users_test (name, password, is_admin) VALUES ('TestUser', 'TestUser', True);"
        self.assertEqual(self.db.write_data_to_database(query), True)
        
        
        
        

    