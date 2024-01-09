import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src import users
from src import database

class UsersTests(unittest.TestCase):
    def setUp(self):
        self.user_dict_empty = {}
        self.response_added_user = "The user has been added!"
        self.create_user_msg = "create new TestUser 123 Yes"
        self.delete_user_msg = "delete user TestUser"
        self.db = database.DatabasePsql("tests\database_test.ini")
        self.users_list_from_db = [('admin', True), ('user', False)]
    
    def test_create_user_with_admin_permissions(self):
        testMsg = "user create TestingUser asd123qwe Yes"
        self.assertEqual(users.create_user(testMsg, self.db), self.response_added_user)
        msg = "user delete TestingUser"
        users.delete_user(msg, self.db)
 
    def test_create_user_with_no_admin_permissions(self):
        testMsg = "user create TestingUserNoAdmin asd123qwe No"
        self.assertEqual(users.create_user(testMsg, self.db), self.response_added_user)
        msg = "user delete TestingUserNoAdmin"
        users.delete_user(msg, self.db)
      
    def test_create_user_with_incorrect_admin_permissions(self):
        testMsg = "user create TestingUser asd123qwe Rights"
        response = "Incorrect value for admin rights"
        self.assertEqual(users.create_user(testMsg, self.db), response)
           
    def test_create_user_if_the_name_of_user_exists_in_database(self):
        testMsg = "user create admin asd123qwe Yes"
        self.assertEqual(users.create_user(testMsg, self.db), "The user exists")

    def test_create_user_with_too_much_data_in_message(self):#nie działa
        testMsg = "user create TestingUser asd123qwe Yes Yes"
        self.assertEqual(users.create_user(testMsg, self.db), "The wrong amount of data was entered or the format was incorrect")
            
    def test_delete_user(self):
        msg = "user create TestingUser asd123qwe Yes"
        users.create_user(msg, self.db)
        testMsg = "user delete TestingUser"
        self.assertEqual(users.delete_user(testMsg, self.db), "The user has been deleted")
   
    def test_delete_user_if_the_user_not_exist(self):
        testMsg = "delete user TestUserWhooseNotExist"
        self.assertEqual(users.delete_user(self.delete_user_msg, self.db), "User does not exist!")
      
    def test_delete_user_with_too_much_data_in_message(self):
        testMsg = "delete user TestUser User"
        self.assertEqual(users.delete_user(testMsg, self.db), "The wrong amount of data was entered or the format was incorrect")

    def test_user_log_in_check_the_user_is_logged(self):
        testMsg = "user log in user user"
        self.assertEqual(users.user_log_in(testMsg, self.db, None, False), ("user", False , "The user has been logged in!"))
   
    def test_user_log_in_with_incorrect_data(self):
        testMsg = "user log in FirstUser 123incorrect"
        self.assertEqual(users.user_log_in(testMsg, self.db, None, False), (None , False , "The login details are incorrect"))
        
    def test_user_log_in_with_too_much_data_in_messages(self):
        testMsg = "user log in FirstUser 123 Admin"
        self.assertEqual(users.user_log_in(testMsg, self.db, None, False), (None , False , "The wrong amount of data was entered or the format was incorrect"))

    def test_user_log_out(self):
        self.assertEqual(users.user_log_out("FirstUser"), (None, False, "[SERVER] The user has been logged out"))
       
    def test_user_log_out_if_no_one_is_log_in(self):
        self.assertEqual(users.user_log_out(None), (None, False, "[SERVER] No one is currently logged in"))
         
    def test_user_info(self):
        user_logged = "FirstUser"
        self.assertEqual(users.user_info(user_logged), f"You are logged in as {user_logged}" )
        
    def test_user_info_if_no_one_is_log_in(self):
        self.assertEqual(users.user_info(None), "You need to log in!")
   
    def test_user_from_db_list_to_dict(self):
        user_list_out = [{'name': 'admin', 'is_admin': True}, {'name': 'user', 'is_admin': False}, {'is_admin': True, 'name': 'john_doe'}, {'is_admin': False, 'name': 'alice_smith'}]
        data = users.users_show(self.db)
        self.assertEqual(data, user_list_out)
        
if __name__ == "__main__":
    unittest.main()
        