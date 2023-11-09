import json

def message_new(conn, msg, user_dict, user_logged):
    try:
        messages_text, new, receiver, message = str(msg).split(" ")#rozkmin jak przyjac wieksza ilosc wiadomosci
        if receiver in user_dict:
            user_msg_json = load_message_user_json(receiver)
            if len(user_msg_json) <= 5:#nie moze okreslic ilosci 
                if len(message) <= 255:
                    user_msg_json.append({"Message from": user_logged, "Message": message})#znowu blad po dadaniu append
                    print(user_msg_json)
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
    
    
    
    
def load_message_user_json(user):
    try:
        with open(f'{user}.json', 'r') as file:
            users_json = json.load(file)
        return users_json   
    except FileNotFoundError:
        user_msg_json = []
        save_message_user_json(user, user_msg_json)
        load_message_user_json(user)
    
def save_message_user_json(user, user_msg_json):
    with open(f'{user}.json', 'w') as file:
        json.dump(user_msg_json, file, indent=2)