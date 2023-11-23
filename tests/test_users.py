import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import users

class UsersTests(unittest.TestCase):
    def setUp(self):
        self.user_dict = {}
        self.users_json_path = r"tests\test_users.json"
        self.response_added_user = "The user has been added!"
    
    def test_create_user_with_admin_permissions(self):
        msg = "user create TestingUser asd123qwe Yes"
        self.assertEqual(users.create_user(msg, self.user_dict, self.users_json_path), self.response_added_user)
        
    def test_create_user_with_no_admin_permissions(self):
        msg = "user create TestingUserNoAdmin asd123qwe No"
        self.assertEqual(users.create_user(msg, self.user_dict, self.users_json_path), self.response_added_user)
        
    def test_create_user_with_incorrect_admin_permissions(self):
        msg = "user create TestingUser asd123qwe Rights"
        response = "Incorrect value for admin rights"
        self.assertEqual(users.create_user(msg, self.user_dict, self.users_json_path), response)
        
    def test_create_user_if_the_name_of_user_exists_in_database(self):
        msg = "user create TestingUser asd123qwe Yes"
        self.assertEqual(users.create_user(msg, self.user_dict, self.users_json_path), self.response_added_user)
        responseExistUser = "The user exists"
        self.assertEqual(users.create_user(msg, self.user_dict, self.users_json_path), responseExistUser)
    
    def test_create_a_few_users_and_check_if_they_added_to_the_database(self):
        msgFirstUser = "user create FirstUser 123 No"
        msgSecondUser = "user create SecondUser 123 Yes"
        msgThirdUser = "user create ThirdUser 123 No"
        users.create_user(msgFirstUser, self.user_dict, self.users_json_path)
        users.create_user(msgSecondUser, self.user_dict, self.users_json_path)
        users.create_user(msgThirdUser, self.user_dict, self.users_json_path)
        self.assertEqual(len(self.user_dict), 3)
        
    def test_create_user_with_too_much_data_in_message(self):#nie działa
        msg = "user create TestingUser asd123qwe Yes Yes"
        with self.assertRaises(ValueError) as ctx:
            users.create_user(msg, self.user_dict, self.users_json_path)
        self.assertEqual("The wrong amount of data was entered or the format was incorrect", str(ctx.exception))
        
if __name__ == "__main__":
    unittest.main()
        