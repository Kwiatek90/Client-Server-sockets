import json

def create_user(msg, conn_db):
    try:
        user_str, create_str,  name, password, admin = str(msg).split(" ")
        
        if admin == "Yes" or admin == "yes":
            admin = True
        elif admin == "No" or admin == "no": 
            admin = False
        else:
            response = "Incorrect value for admin rights"
            return response
        
        query =  f"select exists(select name from users_test where name='{name}')"
        user_exists = conn_db.load_data_from_database(query)[0][0]
        
        if user_exists:
            response = "The user exists"
        else: 
            query_add_user = f"INSERT INTO users_test (name, password, is_admin) VALUES ('{name}', '{password}', {admin});"
            response = conn_db.write_data_to_database(query_add_user)
            if response == True: response = "The user has been added!"
        return response
    except ValueError:
        print("[FAIL] Wrong data")
        response = "The wrong amount of data was entered or the format was incorrect"
        return response
    
def delete_user(msg, conn_db):
    try:
        user, delete,  name = str(msg) .split(" ")
        
        query =  f"select exists(select name from users_test where name='{name}')"
        user_exists = conn_db.load_data_from_database(query)[0][0]
        
        if user_exists:
            query_delete_user = f"DELETE FROM users_test WHERE name = '{name}';"
            response = conn_db.write_data_to_database(query_delete_user)
            if response:
                response = "The user has been deleted"
            print(f"[DELETE] The {name} has been deleted")
            return response
        else:
            response = "User does not exist!"
            
        return response
    except ValueError:
        print("[FAIL] Wrong data")
        response = "The wrong amount of data was entered or the format was incorrect"
        return response

#to do zrobienia przenisc funkcje z database do users lub funkjca users to dict tutaj    
def users_show(conn_db):
    query = "select name, is_admin from users_test;"
    users_list_from_db = conn_db.load_data_from_database(query)
    users = users_to_dict(users_list_from_db)
    return users
        
def user_log_in(msg, conn_db, user_logged , is_admin):
    try:
        if not user_logged:
            user, log, inn, name, password = str(msg).split(" ")
            
            query =  f"select exists(select name from users_test where name = '{name}');"
            user_exists = conn_db.load_data_from_database(query)[0][0]
            
            if user_exists: 
                query_password = f"select password, is_admin from users_test where name = '{name}';"
                user_password_from_db = conn_db.load_data_from_database(query_password)[0][0]
                user_is_admin_from_db = conn_db.load_data_from_database(query_password)[0][1]
                if user_password_from_db == password:
                    response, user_logged, is_admin = "The user has been logged in!", name, user_is_admin_from_db
                else:
                    response = "The password is incorrect"
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

def users_to_dict(users_from_db):
    user_list= []
    
    for row in users_from_db:
        user_dict = {}
        user_dict["name"] = row[0]
        user_dict["is_admin"] = row[1]
        user_list.append(user_dict)
        
    return user_list
        

    
  


