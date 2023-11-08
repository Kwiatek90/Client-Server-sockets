import json

def messages_new(msg, user_dict, user_logged):
    messages_text, new, receiver, message = str(msg).split(" ")\
    if receiver in user_dict:
        #pobiera aktualne wiadomości uzytkownika
        #sprawdza czy nie przekracza 5 wiadomości
        #potem sprawdza czy wiadomość nie przekracza 255 znaków
        #wysyła
    else:
        #nie ma takiego uzytkownika
    
    
    
    
def load_message_user_json(user):
    with open(f'{user}.json', 'r') as file:
        users_json = json.load(file)
    return users_json   
    
    
def save_message_user_json(user):
    with open(f'{user}.json', 'w') as file:
        json.dump(users_dict, file, indent=3)