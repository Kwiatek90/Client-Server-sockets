import json

def message_new(conn, msg, user_dict, user_logged):
    try:
        command, message = str(msg).split(">")
        message_text, new_text, receiver = str(command.rstrip()).split(" ")
        message = message.lstrip()
        if receiver in user_dict:
            user_msg_json = load_message_user_json(receiver)
            if len(user_msg_json) < 5:
                if len(message) <= 255:
                    user_msg_json.append({"Message from": user_logged, "Message": message})
                    save_message_user_json(receiver, user_msg_json)
                    response = "The message has been sent"
                else:
                    response = "Message exceeds 255 characters!"
            else:
                response = "This user's inbox is full"
        else:
            response = "User does not exist!"

        conn.sendall(f"[SERVER] {response}".encode("utf-8"))  
        
    except ValueError:
        response = "The wrong amount of data was entered or the format was incorrect"
        conn.sendall(f"[SERVER] {response}".encode("utf-8"))  
    
def message_delete(conn, user):
    #usuwanie
    pass

def message_read(conn, user_logged):
    user_msg_json = load_message_user_json(user_logged)
    conn.sendall(f"[SERVER] You have messages from:".encode("utf-8")) 
    for message_from in user_msg_json:
        response = message_from['Message from']#stworzyc plik json jakis bo sie slabo wysyła
        conn.sendall(f"{response}".encode("utf-8")) 

            
def message_read_from(conn, user_logged, message_from):
    pass

    
def load_message_user_json(user):
    try:
        with open(f'{user}.json', 'r') as file:
            users_json = json.load(file)
            return users_json   
        
    except FileNotFoundError:
        user_msg_json = []
        save_message_user_json(user, user_msg_json)
        users_json = load_message_user_json(user)
        return users_json
    
def save_message_user_json(user, user_msg_json):
    with open(f'{user}.json', 'w') as file:
        json.dump(user_msg_json, file, indent=2)
        