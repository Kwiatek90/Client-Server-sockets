import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src import messages
from src import database

def big_msg_open():
        with open("tests\msg_with_above_225_char.txt", "r") as f:
            text = f.read()
            
        return text
class MessagesTests(unittest.TestCase):
    def setUp(self):
        self.db = database.DatabasePsql("tests\database_test.ini")
        
    #aktualny test    
    def test_message_new_with_incorrect_command(self):
        test_msg = "message new FirstUser admin > This is the message"
        self.assertEqual(messages.message_new(test_msg, self.db, "admin"), "The wrong amount of data was entered or the format was incorrect" )
    #aktualny test    
    def test_message_new_if_the_receiver_is_not_in_user_database(self):
        test_msg = "message new UserNotExist > This is the message"
        self.assertEqual(messages.message_new(test_msg, self.db, "admin"), "User does not exist!")
    #aktualny test   
    def test_message_new_if_the_inbox_is_full_with_more_than_5_messages(self):
        test_msg = "message new user > This is the message"
        self.assertEqual(messages.message_new(test_msg, self.db, "admin"), "This user's inbox is full" )
    #aktualny test    
    def test_message_new_when_the_message_exceeds_255_characters(self):
        test_msg = f"message new admin > {big_msg_open()}"
        self.assertEqual(messages.message_new(test_msg, self.db, "user") , "Message exceeds 255 characters!")
    
    #akutalny test    
    def test_message_new_when_have_been_sent_and_have_been_deleted(self):
        test_msg = "message new admin > This is a message which will be deleted"
        self.assertEqual(messages.message_new(test_msg, self.db, "user"), "The message has been sent")
        query_to_find_id_msg = "select msg_id from messages where msg_from = 'user' and msg_for = 'admin' and msg = 'This is a message which will be deleted';"
        msg_id = self.db.load_data_from_database(query_to_find_id_msg)[0][0]
        test_msg = f"message delete {msg_id}"
        self.assertEqual(messages.message_delete(test_msg, self.db, 'admin'), "The message has been deleted")
    
    #aktaulny test  
    def test_messages_delete_when_the_number_of_messages_is_incorrect(self):
        test_msg = f"messages delete 99"
        self.assertEqual(messages.message_delete(test_msg, self.db, 'admin'), "The message does not exist")
     
    #aktualny test    
    def test_message_delete_with_incorrect_command(self):
        test_msg = "message delete 1 delete"
        self.assertEqual(messages.message_delete(test_msg, self.db, ""), "The wrong amount of data was entered or the format was incorrect")
        
        
    
if __name__ == "__main__":
    unittest.main()
        
        
    
    
    
    