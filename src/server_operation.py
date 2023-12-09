from users import *
from messages import *
from server import Server

def operations(self, msg, conn, conn_db):
    if msg == 'uptime':
        self.uptime(conn)
    elif msg == "info":
        self.info(conn)
    elif msg == "help":
        self.help_command(conn)
    elif msg == "stop":
        self.stop(conn)
    elif str(msg).startswith("user create") and self.is_admin == True:#wrzucic sprawdzanie admina do funkcji
        response = create_user(msg, self.user_dict, self.users_json_path)
        self.response_load_users(response, conn)
    elif str(msg).startswith("user delete") and self.is_admin == True:
        response = delete_user(msg, self.user_dict, self.users_json_path)
        self.response_load_users(response, conn)
    elif str(msg).startswith("users show") and self.is_admin == True:# z wysyłaniem za pomocą jsona nie będzie problemu tworzy sie ładnie
        users_list = users_show(self.user_dict)
        msg_json = json.dumps(users_list, indent=2)
        conn.sendall(f"[SERVER] Users on server\n{msg_json}".encode("utf-8"))  
    elif str(msg).startswith("user log in"):
        self.user_logged, self.is_admin, response = user_log_in(msg, self.user_dict, self.user_logged, self.is_admin)
        conn.sendall(f"[SERVER] {response}".encode("utf-8"))  
    elif msg == "user log out":
        self.user_logged, self.is_admin, response = user_log_out(self.user_logged)
        conn.sendall(f"{response}".encode("utf-8")) 
    elif msg =="user info":
        response = user_info(self.user_logged)
        conn.sendall(f"[SERVER] {response}".encode("utf-8"))
    elif str(msg).startswith("message new"):
        response = message_new(msg, self.user_dict, self.user_logged, self.messages_path)  
        conn.sendall(f"[SERVER] {response}".encode("utf-8"))    
    elif str(msg).startswith("message delete"):
        response = message_delete(msg, self.user_logged, self.messages_path)
        conn.sendall(f"[SERVER] {response}".encode("utf-8"))  
    elif msg == "messages read":
        response = message_read(self.user_logged, self.messages_path)
        conn.sendall(f"[SERVER] You have messages from:\n{response}".encode("utf-8")) 
    elif str(msg).startswith("message read from"):
        response, messages_num = message_read_from(msg, self.user_logged, self.messages_path)
        conn.sendall(f"[SERVER] Information about the message from the list with number {messages_num}\n{response}".encode("utf-8"))
    else:
        conn.sendall(f"[SERVER] You entered the wrong command or you don't have access to it".encode("utf-8"))