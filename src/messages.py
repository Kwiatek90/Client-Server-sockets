import json
from datetime import datetime
from users import check_if_the_user_exists

def message_new(msg, conn_db, user_logged):
    try:
        command, message = str(msg).split(">")
        message_text, new_text, receiver = str(command.rstrip()).split(" ")
        message = message.lstrip()
        user_exists = check_if_the_user_exists(receiver, conn_db)
        
        if user_exists:
            unread = check_unread_msg(receiver, conn_db)
       
            if unread < 5:
                if len(message) <= 255:
                    #dodowanie wiadomosci
                    #BŁĄD:  wartość zbyt długa dla typu znakowego zmiennego (255) to podaje baza jak wiadomosc jest zbyt długa
                    user_msg_json.append({"Message from": user_logged, "Message": message, "Read": False, "Time of receiving the message": send_time})
                    save_message_user_json(receiver, user_msg_json, msg_path)
                    response = "The message has been sent"
                else:
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
    query = f"select count(unread) from messages where name = {receiver};"
    unread = int(conn_db.load_data_from_database(query)[0][0])
    return unread
            
    
def message_delete(msg, user_logged, msg_path):
    try:
        user_msg_json = load_message_user_json(user_logged, msg_path)
        message_text, delete_text , messages_num = str(msg).split(" ")
        messages_num = int(messages_num)
        del user_msg_json[messages_num]
        save_message_user_json(user_logged, user_msg_json, msg_path)
        response = "The message has been deleted"
        return response
    except ValueError:
        response = "The wrong amount of data was entered or the format was incorrect"
        return response

def message_read(user_logged, msg_path):
    user_msg_json = load_message_user_json(user_logged, msg_path)
    
    messages = []
    for message in user_msg_json:
        messages.append({"Message from:": message['Message from'], "Read": message["Read"]})
    
    messages_read_json = json.dumps(messages, indent=2)
    return messages_read_json
                
def message_read_from(msg, user_logged, msg_path):
    try:
        user_msg_json = load_message_user_json(user_logged, msg_path)
        message_text, read_text ,from_text, messages_num = str(msg).split(" ")
        messages_num = int(messages_num)
        
        user_msg_json[messages_num]["Read"] = True
        user_msg = user_msg_json[messages_num]
        response = json.dumps(user_msg, indent=1)
        
        save_message_user_json(user_logged, user_msg_json, msg_path)
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
        
