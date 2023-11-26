import json
from datetime import datetime

def message_new(msg, user_dict, user_logged, msg_path):
    try:
        command, message = str(msg).split(">")
        message_text, new_text, receiver = str(command.rstrip()).split(" ")
        message = message.lstrip()
        if receiver in user_dict:
            user_msg_json = load_message_user_json(receiver, msg_path)
            unread = check_unread_msg(user_msg_json)
            send_time = str(datetime.now().replace(microsecond=0))
       
            if unread < 5:
                if len(message) <= 255:
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
                
def message_read_from(conn, msg, user_logged):
    try:
        user_msg_json = load_message_user_json(user_logged)
        message_text, read_text ,from_text, messages_num = str(msg).split(" ")
        messages_num = int(messages_num)
        
        user_msg_json[messages_num]["Read"] = True
        user_msg = user_msg_json[messages_num]
        response = json.dumps(user_msg, indent=1)
        
        save_message_user_json(user_logged, user_msg_json)
        conn.sendall(f"[SERVER] Information about the message from the list with number {messages_num}\n{response}".encode("utf-8"))   
    except ValueError:
        response = "The wrong amount of data was entered or the format was incorrect"
        conn.sendall(f"[SERVER] {response}".encode("utf-8"))   
    
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
        
def check_unread_msg(user_msg_json):
    unread = 0
    for msg in user_msg_json:
        msg["Read"] == False
        unread += 1
    return unread
        