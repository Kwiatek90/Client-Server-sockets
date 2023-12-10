import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src import Server, database

class ServerTests(unittest.TestCase):
    def setUp(self):
        self.server = Server("127.0.0.1", 65432, "test", database_config_path)
        database_config_path = "tests\database_test.ini"
    
    def test_load_users_from_database(self):
        print(self.server.user_dict)
        
    