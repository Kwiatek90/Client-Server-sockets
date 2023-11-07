
def create_user(msg):
    user = {}
    create_str, user_str, name, password, admin = str(msg).split(" ")
    if admin == "Yes" or admin == "yes":
        admin = True
    else:
        admin = False
    user = {'name': name, 'password' : password, 'admin' : admin }
    
    #zapisywanie w json
    return user