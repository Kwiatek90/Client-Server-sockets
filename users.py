import json

def create_user(msg, user_dict):
    create_str, user_str, name, password, admin = str(msg).split(" ")#############################zrobic try jak bedzie zla ilosc komenda podaba
    
    if admin == "Yes" or admin == "yes":
        admin = True
    else:
        admin = False
    
    if name in user_dict:
        msg = "Użytkownik istnieje!"
        return msg
    else:   
        user_dict[name] = {'password': password, 'admin': admin}
        save_users_json(user_dict)
        response = "Użytkownik został dodany!"
        return response
    
def delete_user(msg, user_dict):
    delete, user, name = str(msg) .split(" ")
      
    if name in user_dict:
        user_dict.pop(name)
        save_users_json(user_dict)
        response = "Użytkownik został usunięty"
    else:
        response = "Użytkownik nie istnieje!"
        
    return response

def user_log_in(msg, user_dict):
    user, log, inn, name, password = str(msg).split(" ")
    
    if name in user_dict and user_dict[name]['password'] == password:
            response, name, is_admin = "Użytkownik został zalogowany!", name, user_dict[name]['admin']
    else:
        response = "Dane logowania są nieprawidłowe"
        name = ""
        is_admin = False
        
    return response, name, is_admin

def user_info(user_logged):
    respone = f"Jesteś zalogowany jako {user_logged}"
    
    return respone

def save_users_json(users_dict):
    with open('users.json', 'w') as file:
        json.dump(users_dict, file, indent=3)
        
def load_users_json():
    with open('users.json', 'r') as file:
        users_json = json.load(file)
    return users_json

  


