import json
from datetime import datetime
from src import users
import psycopg2

def message_new(msg, conn_db, user_logged):
    try:
        command, message = str(msg).split(">")
        message_text, new_text, receiver = str(command.rstrip()).split(" ")
        message = message.lstrip()
        user_exists = users.check_if_the_user_exists(receiver, conn_db)
        
        if user_exists:
            unread = check_unread_msg(receiver, conn_db)
       
            if unread < 5:
                #dodowanie wiadomosci
                #BŁĄD:  wartość zbyt długa dla typu znakowego zmiennego (255) to podaje baza jak wiadomosc jest zbyt długa
                query_add_message = f"INSERT INTO messages (msg_from, msg_for, msg) VALUES ('{user_logged}','{receiver}','{message}')"
                response = conn_db.write_data_to_database(query_add_message)
                if response == True: 
                    response = "The message has been sent"
                elif response == False: 
                    response = "Message exceeds 255 characters!"
            else:
                response = "This user's inbox is full"
        else:
            response = "User does not exist!"

        return response

    except ValueError:
        response = "The wrong amount of data was entered or the format was incorrect"
        return response
    
def check_unread_msg(receiver, conn_db):
    query = f"select count(unread) from messages where msg_for = '{receiver}';"
    unread = int(conn_db.load_data_from_database(query)[0][0])
    return unread
            
    
def message_delete(msg, conn_db, user_logged):
    try:
        message_text, delete_text , messages_num = str(msg).split(" ")
        messages_exists = check_if_the_messages_exists(conn_db, user_logged, messages_num)
        if messages_exists:
            query_msg_delete = f"DELETE FROM messages WHERE msg_for = '{user_logged}' and msg_id = {messages_num};"
            response = conn_db.write_data_to_database(query_msg_delete)
            if response == True: response = "The message has been deleted"
            else: response = "Error in database query"
        else:
            response = "The message does not exist"    
        return response
    except ValueError:
        response = "The wrong amount of data was entered or the format was incorrect"
        return response

def check_if_the_messages_exists(conn_db, user_logged, messages_num):
    query = f"select exists(SELECT * FROM messages WHERE msg_for = '{user_logged}' and msg_id = {messages_num});"
    response = conn_db.load_data_from_database(query)[0][0]
    return response
    
def message_read(user_logged, conn_db):
    query_msg = f"SELECT msg_id, msg_from, unread FROM messages WHERE msg_for = '{user_logged}';"
    msg_list_from_db = conn_db.load_data_from_database(query_msg)

    messages = []
    for message in msg_list_from_db:
        messages.append({"Message_number:": message[0], "Message_from": message[1], "Read": message[2]})
    
    messages_read_json = json.dumps(messages, indent=2)
    return messages_read_json
                
def message_read_from(msg, conn_db, user_logged):
    try:
        message_text, read_text ,from_text, messages_num = str(msg).split(" ")
        messages_num = int(messages_num)
        message_exists = check_if_the_messages_exists(conn_db, user_logged, messages_num)
        
        if message_exists:
            query_msg_read = f"UPDATE messages SET unread = true WHERE msg_for = '{user_logged}' and msg_id = {messages_num};"
            query_msg = f"SELECT msg_id, msg_from, unread, time_msg_recv, msg FROM messages WHERE msg_for = '{user_logged}' and msg_id = {messages_num};"
            
            response_unread = conn_db.write_data_to_database(query_msg_read)
            if response_unread == True: print("The messages change unread to True") 
            else: print("Something goes wrong and messages not change to True") 
            msg_list = conn_db.load_data_from_database(query_msg)
            
            messages = []
            for message in msg_list:
                messages.append({"Message_number:": message[0], "Message_from": message[1], "Read": message[2], "Time_message": f"{message[3]}", "Message_text": message[4]})
        
            response = json.dumps(messages, indent=1)
        else:
            response = "The messages does not exist"
        
        return response, messages_num   
    except ValueError:
        response = "The wrong amount of data was entered or the format was incorrect"
        return response, messages_num
    
def load_message_user_json(user, msg_path):
    try:
        with open(f'{msg_path}\{user}.json', 'r') as file:
            users_json = json.load(file)
            return users_json   
        
    except FileNotFoundError:
        print("[FILES] File not exist, creating one")
        user_msg_json = []
        save_message_user_json(user, user_msg_json, msg_path)
        users_json = load_message_user_json(user, msg_path)
        return users_json
    
def save_message_user_json(user, user_msg_json, msg_path):
    with open(f'{msg_path}\{user}.json', 'w') as file:
        json.dump(user_msg_json, file, indent=2)
        
