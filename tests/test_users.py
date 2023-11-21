import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import users

class UsersTests(unittest.TestCase):
    def setUp(self):
        self.user_dict = {}
        
        
    def test_create_user(self):
        msg = "creater user TestingUser asd123qwe Yes"
        response = "The user has been added!"
        self.assertEqual(users.create_user(msg, self.user_dict), response)#sprawdzic zapisywanie do jsona
        
if __name__ == "__main__":
    unittest.main()
        