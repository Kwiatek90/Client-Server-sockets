import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import users

class UsersTests(unittest.TestCase):
    def setUp(self):
        self.user_dict = {}
    
    def create_user_with_admin_permissions(self):
        msg = "creater user TestingUser asd123qwe Yes"
        response = "The user has been added!"
        users_json_path = r"tests\test_users.json"
        self.assertEqual(users.create_user(msg, self.user_dict, users_json_path), response)
        
    def create_user_with_no_admin_permissions(self):
        msg = "creater user TestingUserNoAdmin asd123qwe No"
        response = "The user has been added!"
        users_json_path = r"tests\test_users.json"
        self.assertEqual(users.create_user(msg, self.user_dict, users_json_path), response)
        
    def create_user_with_incorrect_admin_permissions(self):
        pass
        
        
if __name__ == "__main__":
    unittest.main()
        