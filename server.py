import json
import socket
from datetime import datetime
import users
import messages
class Server:
    def __init__(self, HOST, PORT, VERSION) -> None:
        self.HOST = HOST
        self.PORT = PORT
        self.VERSION = VERSION
        self.ADDR = (self.HOST, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_start_time = datetime.now().replace(microsecond=0)
        self.is_admin = False
        self.user_logged = None
        self.users_json_path = r'D:\Programowanie\EgzaminyZeroToJunior\DATABASE\CS_socket\users.json'
        self.user_dict = users.load_users_json(self.users_json_path)
        
    
    def start_server(self):
        print("[STARTING] Server is starting ...")
        self.server.bind(self.ADDR)
        self.server.listen()
      
        print(f"[LISTENING] Server is listening on {self.HOST}")
        
        self.server_live = True
        while self.server_live:
            conn, addr = self.server.accept()
            self.client_connection(conn, addr)
            
        self.server.close()
            
    def client_connection(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        conn.sendall(f"[SERVER] You are connected to the {self.HOST}".encode("utf-8"))

        
        self.connected = True
        while self.connected:
            msg = conn.recv(1024).decode("utf-8")
            if msg == 'uptime':
                self.uptime(conn)
            elif msg == "info":
                self.info(conn)
            elif msg == "help":
                self.help_command(conn)
            elif msg == "stop":
                self.stop(conn)
            elif str(msg).startswith("user create") and self.is_admin == True:
                response = users.create_user(msg, self.user_dict, self.users_json_path)
                self.response_load_users(response, conn)
            elif str(msg).startswith("user delete") and self.is_admin == True:
                response = users.delete_user(msg, self.user_dict, self.users_json_path)
                self.response_load_users(response, conn)
            elif str(msg).startswith("users show") and self.is_admin == True:
                users_list = users.users_show(self.user_dict)
                msg_json = json.dumps(users_list, indent=2)
                conn.sendall(f"[SERVER] Users on server\n{msg_json}".encode("utf-8"))  
            elif str(msg).startswith("user log in"):
                self.user_logged, self.is_admin = users.user_log_in(conn , msg, self.user_dict, self.user_logged, self.is_admin)
            elif msg == "user log out":
                self.user_logged, self.is_admin = users.user_log_out(conn, self.user_logged, self.is_admin)
            elif str(msg).startswith("user info"):
                response = users.user_info(self.user_logged)
                conn.sendall(f"[SERVER] {response}".encode("utf-8"))
            elif str(msg).startswith("message new"):
                messages.message_new(conn, msg, self.user_dict, self.user_logged)    
            elif str(msg).startswith("message delete"):
                messages.message_delete(conn, msg, self.user_logged)
            elif msg == "messages read":
                messages.message_read(conn, self.user_logged)
            elif str(msg).startswith("message read from"):
                messages.message_read_from(conn, msg, self.user_logged)
            else:
                conn.sendall(f"[SERVER] You entered the wrong command or you don't have access to it".encode("utf-8"))
     
        conn.close()
        
    def response_load_users(self, response, conn):
        conn.sendall(f"[SERVER] {response}".encode("utf-8"))
        self.user_dict = users.load_users_json(self.users_json_path)
    
    def send_json(self, msg, conn):
        msg_json = json.dumps(msg, indent=2)
        conn.send(msg_json.encode("utf-8"))   
            
    def uptime(self, conn):
        server_now_time = datetime.now().replace(microsecond=0)
        diff_time = str(server_now_time - self.server_start_time).split(":") 
        date_dict = {}
        date_dict["Hours"] = diff_time[0]
        date_dict["Minuts"] = diff_time[1]
        date_dict["Seconds"] = diff_time[2]
        time = {"Live of server": date_dict}
        print("[SENDING] Live of server")
        self.send_json(time, conn)
    
    def info(self,conn):
        info_dict = { "Version of the server":self.VERSION, "Creation date": self.server_start_time.strftime('%a %d %b %Y, %I:%M%p')} 
        print("[SENDING] Info about server")
        self.send_json(info_dict, conn)
    
    def help_command(self, conn):
        commands_info = {
            "uptime": "server live time",
            "info": "returns the version number of the server, its creation date",
            "help": "returns a list of available commands with a short description",
            "stop": "stops the server and client at the same time",
            "user log in [NAME] [PASSWORD]": "Log in to the server by entering Name and Password",
            "user info": "Shows who is currently logged in",
            "user log out": "Logs the user out",
            "user create [NAME] [PASSWORD] [IS_ADMIN(Yes/No)]": "Creating a user",
            "user delete [NAME]": "Deleting a user",
            "users show": "Shows all server users",
            "message new [NAME] > [MESSAGE]": "Will send a message to the user with a maximum capacity of 255 characters",
            "message delete [MESSAGE NUMBER STARTING FROM 0]": "Deleting a message",
            "messages read": "Shows all messages, who they are from and whether they have been read",
            "message read from [MESSAGE NUMBER STARTING FROM 0]": "Show message from the sender"
        }
        print("[SENDING] Help command")
        self.send_json(commands_info, conn)

    def stop(self, conn):
        print("[CLOSING] Server has been closed")
        self.connected = False
        self.server_live = False
        conn.close()
       