import json

def create_user(msg, user_dict, users_json_path):
    try:
        user_str, create_str,  name, password, admin = str(msg).split(" ")
        
        if admin == "Yes" or admin == "yes":
            admin = True
        elif admin == "No" or admin == "no": 
            admin = False
        else:
            response = "Incorrect value for admin rights"
            return response
        
        if name in user_dict:
            response = "The user exists"
        else:   
            user_dict[name] = {'password': password, 'admin': admin}
            save_users_json(user_dict, users_json_path)
            response = "The user has been added!"
        return response
    except ValueError:
        print("[FAIL] Wrong data")
        response = "The wrong amount of data was entered or the format was incorrect"
        return response
    finally:
        pass
        #zamyka tworzenie query
    
def delete_user(msg, user_dict, users_json_path):
    try:
        user, delete,  name = str(msg) .split(" ")
        
        if name in user_dict:
            user_dict.pop(name)
            save_users_json(user_dict, users_json_path)
            response = "The user has been deleted"
            print(f"[DELETE] The {name} has been deleted")
        else:
            response = "User does not exist!"
            
        return response
    except ValueError:
        print("[FAIL] Wrong data")
        response = "The wrong amount of data was entered or the format was incorrect"
        return response
    
def users_show(user_dict):
    users = []
    for user in user_dict:
        users.append(user)
    return users
        
def user_log_in(msg, user_dict, user_logged , is_admin):
    try:
        if not user_logged:
            user, log, inn, name, password = str(msg).split(" ")
            
            if name in user_dict and user_dict[name]['password'] == password:
                response, user_logged, is_admin = "The user has been logged in!", name, user_dict[name]['admin']
            else:
                response = "The login details are incorrect"
                print("[FAIL] The client provided wrong data")
                
        else:
            response = user_info(user_logged)
        
        return user_logged, is_admin, response
    except ValueError:
        print("[FAIL] Wrong data")
        response = "The wrong amount of data was entered or the format was incorrect"
        
        return user_logged, is_admin, response

def user_log_out(user_logged):
    is_admin = False
    
    if user_logged:
        user_logged = None
        response = "[SERVER] The user has been logged out"
    else:
        response = "[SERVER] No one is currently logged in"
    return user_logged, is_admin, response

def user_info(user_logged):
    if not user_logged:
        respone = "You need to log in!"
    else:
        respone = f"You are logged in as {user_logged}"
    return respone

def save_users_json(users_dict, users_json_path):### save juz nie trzeba robic, tylko za kazdym razem po utworzenie usunieciu trzeba bedzie ładować dane na nowo
    with open(users_json_path, 'w') as file:
        json.dump(users_dict, file, indent=3)
        
def load_users_json(users_json_path):
    with open(users_json_path, 'r') as file:
        users_json = json.load(file)
    return users_json

    
  


