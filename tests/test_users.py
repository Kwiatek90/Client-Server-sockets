import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import users

class UsersTests(unittest.TestCase):
    def setUp(self):
        self.user_dict_empty = {}
        self.users_json_path = r"tests\test_users.json"
        self.response_added_user = "The user has been added!"
        self.create_user_msg = "create new TestUser 123 Yes"
        self.delete_user_msg = "delete user TestUser"
        self.user_dict_to_check = {
                                        "FirstUser": {
                                            "password": "123",
                                            "admin": False
                                        },
                                        "SecondUser": {
                                            "password": "123",
                                            "admin": True
                                        },
                                        "ThirdUser": {
                                            "password": "123",
                                            "admin": False
                                        }
                                    }
    
    def test_create_user_with_admin_permissions(self):
        testMsg = "user create TestingUser asd123qwe Yes"
        self.assertEqual(users.create_user(testMsg, self.user_dict_empty, self.users_json_path), self.response_added_user)
        
    def test_create_user_with_no_admin_permissions(self):
        testMsg = "user create TestingUserNoAdmin asd123qwe No"
        self.assertEqual(users.create_user(testMsg, self.user_dict_empty, self.users_json_path), self.response_added_user)
        
    def test_create_user_with_incorrect_admin_permissions(self):
        testMsg = "user create TestingUser asd123qwe Rights"
        response = "Incorrect value for admin rights"
        self.assertEqual(users.create_user(testMsg, self.user_dict_empty, self.users_json_path), response)
        
    def test_create_user_if_the_name_of_user_exists_in_database(self):
        self.assertEqual(users.create_user(self.create_user_msg, self.user_dict_empty, self.users_json_path), self.response_added_user)
        responseExistUser = "The user exists"
        self.assertEqual(users.create_user(self.create_user_msg, self.user_dict_empty, self.users_json_path), responseExistUser)
    
    def test_create_a_few_users_and_check_if_they_added_to_the_database(self):
        msgFirstUser = "user create FirstUser 123 No"
        msgSecondUser = "user create SecondUser 123 Yes"
        msgThirdUser = "user create ThirdUser 123 No"
        users.create_user(msgFirstUser, self.user_dict_empty, self.users_json_path)
        users.create_user(msgSecondUser, self.user_dict_empty, self.users_json_path)
        users.create_user(msgThirdUser, self.user_dict_empty, self.users_json_path)
        self.assertEqual(len(self.user_dict_empty), 3)
        
    def test_create_user_with_too_much_data_in_message(self):#nie działa
        testMsg = "user create TestingUser asd123qwe Yes Yes"
        self.assertEqual(users.create_user(testMsg, self.user_dict_empty, self.users_json_path), "The wrong amount of data was entered or the format was incorrect")
        
    def test_delete_user(self):
        users.create_user(self.create_user_msg, self.user_dict_empty, self.users_json_path)
        self.assertEqual(users.delete_user(self.delete_user_msg, self.user_dict_empty, self.users_json_path), "The user has been deleted")
        
    def test_delete_user_if_the_user_not_exist(self):
        self.assertEqual(users.delete_user(self.delete_user_msg, self.user_dict_empty, self.users_json_path), "User does not exist!")
        
    def test_delete_user_with_too_much_data_in_message(self):
        testMsg = "delete user TestUser User"
        self.assertEqual(users.delete_user(testMsg, self.user_dict_empty, self.users_json_path), "The wrong amount of data was entered or the format was incorrect")

    def test_user_log_in_check_the_user_is_logged(self):
        testMsg = "user log in FirstUser 123"
        self.assertEqual(users.user_log_in(testMsg, self.user_dict_to_check, None, False), ("FirstUser", False , "The user has been logged in!"))
   
    def test_user_log_in_with_incorrect_data(self):
        testMsg = "user log in FirstUser 123incorrect"
        self.assertEqual(users.user_log_in(testMsg, self.user_dict_to_check, None, False), (None , False , "The login details are incorrect"))
   
    def test_user_log_in_with_too_much_data_in_messages(self):
        testMsg = "user log in FirstUser 123 Admin"
        self.assertEqual(users.user_log_in(testMsg, self.user_dict_to_check, None, False), (None , False , "The wrong amount of data was entered or the format was incorrect"))

    def test_user_log_out(self):
        self.assertEqual(users.user_log_out("FirstUser"), (None, False, "[SERVER] The user has been logged out"))
        
    def test_user_log_out_if_no_one_is_log_in(self):
        self.assertEqual(users.user_log_out(None), (None, False, "[SERVER] No one is currently logged in"))
        
    def test_user_info(self):
        user_logged = "FirstUser"
        self.assertEqual(users.user_info(user_logged), f"You are logged in as {user_logged}" )
        
    def test_user_info_if_no_one_is_log_in(self):
        self.assertEqual(users.user_info(None), "You need to log in!")
        
    def test_save_load_user_json(self):
        users.save_users_json(self.user_dict_to_check, self.users_json_path)
        self.assertEqual(self.user_dict_to_check, users.load_users_json(self.users_json_path))
        
if __name__ == "__main__":
    unittest.main()
        