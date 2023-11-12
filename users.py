import json

def create_user(msg, user_dict):
    try:
        user_str, create_str,  name, password, admin = str(msg).split(" ")
        
        if admin == "Yes" or admin == "yes":
            admin = True
        elif admin == "No" or "no": 
            admin = False
        else:
            response = "Incorrect value for admin rights"
            return response
        
        if name in user_dict:
            response = "The user exists"
        else:   
            user_dict[name] = {'password': password, 'admin': admin}
            save_users_json(user_dict)
            response = "The user has been added!"
        return response
    except ValueError:
        print("[FAIL] Wrong data")
        response = "The wrong amount of data was entered or the format was incorrect"
        return response
    
def delete_user(msg, user_dict):
    try:
        user, delete,  name = str(msg) .split(" ")
        
        if name in user_dict:
            user_dict.pop(name)
            save_users_json(user_dict)
            response = "The user has been deleted"
            print(f"[DELETE] The {name} has been delted")
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
        
def user_log_in(conn , msg, user_dict, user_logged , is_admin):
    try:
        if not user_logged:
            user, log, inn, name, password = str(msg).split(" ")
            
            if name in user_dict and user_dict[name]['password'] == password:
                    response, user_logged, is_admin = "The user has been logged in!", name, user_dict[name]['admin']
            else:
                response = "The login details are incorrect"
                print("[FAIL] The client provided wrong data")
                user_logged = ""
                is_admin = False
            
            conn.sendall(f"[SERVER] {response}".encode("utf-8"))  
            return user_logged, is_admin
        else:
            response = user_info(user_logged)
            conn.sendall(f"[SERVER] {response}".encode("utf-8"))  
        
            return user_logged, is_admin
    except ValueError:
        print("[FAIL] Wrong data")
        response = "The wrong amount of data was entered or the format was incorrect"
        user_logged = ""
        is_admin = False
        conn.sendall(f"[SERVER] {response}".encode("utf-8"))  
        
        return user_logged, is_admin

def user_log_out(conn, user_logged, is_admin):
    if user_logged:
        user_logged = None
        is_admin = False
        conn.sendall(f"[SERVER] The user has been logged out".encode("utf-8")) 
    else:
        conn.sendall(f"[SERVER] No one is currently logged in".encode("utf-8")) 
    return user_logged, is_admin

def user_info(user_logged):
    if not user_logged:
        respone = "You need to log in!"
    else:
        respone = f"You are logged in as {user_logged}"
    return respone

def save_users_json(users_dict):
    with open(r'D:\Programowanie\EgzaminyZeroToJunior\DATABASE\CS_socket\users.json', 'w') as file:
        json.dump(users_dict, file, indent=3)
        
def load_users_json():
    with open(r'D:\Programowanie\EgzaminyZeroToJunior\DATABASE\CS_socket\users.json', 'r') as file:
        users_json = json.load(file)
    return users_json

    
  


