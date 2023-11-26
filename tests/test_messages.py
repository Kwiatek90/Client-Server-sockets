import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from messages import *

def big_msg_open():
        with open("tests\msg_with_above_225_char.txt", "r") as f:
            text = f.read()
            
        return text
class MessagesTests(unittest.TestCase):
    def setUp(self):
        self.msg_path = r"tests\\"
        self.user_dict = {
                                        "FirstUser": {
                                            "password": "123",
                                            "admin": False
                                        },
                                        "SecondUser": {
                                            "password": "123",
                                            "admin": True
                                        },
                                        "UserMsgTest_full": {
                                            "password": "123",
                                            "admin": False
                                        },
                                        
                                    }
        self.full_message_inbox = load_message_user_json("UserMsgTest_full", self.msg_path)
        self.message_user = {
                                "Message from": "FirstUser",
                                "Message": "This is a message",
                                "Read": False,
                                "Time of receiving the message": "2023-11-26 10:55:50"
                            }
        
    def test_message_new_with_incorrect_command(self):
        test_msg = "message new FirstUser admin > This is the message"
        self.assertEqual(message_new(test_msg, self.user_dict, "SecondUser", self.msg_path), "The wrong amount of data was entered or the format was incorrect" )
        
    def test_message_new_if_the_receiver_is_in_user_database(self):
        test_msg = "message new FourthUser > This is the message"
        self.assertEqual(message_new(test_msg, self.user_dict, "FirstUser", self.msg_path), "User does not exist!")
        
    def test_message_new_if_the_inbox_is_full_with_more_than_5_messages(self):
        test_msg = "message new UserMsgTest_full > This is the message"
        self.assertEqual(message_new(test_msg, self.user_dict, "FirstUser", self.msg_path), "This user's inbox is full" )
     
    def test_message_new_when_the_message_exceeds_255_characters(self):
        test_msg = f"message new SecondUser > {big_msg_open()}"
        self.assertEqual(message_new(test_msg, self.user_dict, "FirstUser", self.msg_path) , "Message exceeds 255 characters!")
        
    def test_message_new_when_have_been_sent_and_have_been_deleted(self):
        test_msg = "message new SecondUser > This is a message"
        self.assertEqual(message_new(test_msg, self.user_dict, "FirstUser", self.msg_path), "The message has been sent")
        test_msg = "message delete 1"
        self.assertEqual(message_delete(test_msg, "SecondUser", self.msg_path), "The message has been deleted")
        
    def test_message_delete_with_incorrect_command(self):
        test_msg = "message delete 1 delete"
        self.assertEqual(message_delete(test_msg, "SecondUser", self.msg_path), "The wrong amount of data was entered or the format was incorrect")
        
    
        
    
    
    
    