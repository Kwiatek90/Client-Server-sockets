import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src import database
from src import users

class ServerTests(unittest.TestCase):
    def setUp(self):
        self.db = database.DatabasePsql("tests\database_test.ini")
        self.users_list_from_db = [('admin', 'admin', True), ('user', 'user', False)]
        
    def test_load_users_from_database(self):
        data = self.db.load_data_from_database("SELECT name, password, is_admin FROM users_test;")
        self.assertEqual(data, self.users_list_from_db)
        
    def test_user_from_db_list_to_dict(self):
        user_list_out = [{'name': 'admin', 'password': 'admin', 'is_admin': True}, {'name': 'user', 'password': 'user', 'is_admin': False}]
        data = users.users_to_dict(self.users_list_from_db)
        name = "admin"
        if name in user_list_out:
            print(True)
        else:
            print(False)
        self.assertEqual(data, user_list_out)
        
    def test(self):
        query =  "select exists(select name from users_test where name='admin')"
        user_exists = self.db.load_data_from_database(query)[0][0]
        print(user_exists)
        
        
        

    