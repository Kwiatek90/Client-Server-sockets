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
        self.user_dict = users.load_users_json()
        self.is_admin = False
        self.user_logged = ""
    
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
                response = users.create_user(msg, self.user_dict)
                self.response_load_users(response, conn)
            elif str(msg).startswith("user delete") and self.is_admin == True:
                response = users.delete_user(msg, self.user_dict)
                self.response_load_users(response, conn)
            elif str(msg).startswith("users show") and self.is_admin == True:
                users_list = users.users_show(self.user_dict)
                msg_json = json.dumps(users_list, indent=2)
                conn.sendall(f"[SERVER] Users on server {msg_json}".encode("utf-8"))  
            elif str(msg).startswith("user log in"):
                self.user_logged, self.is_admin = users.user_log_in(conn , msg, self.user_dict, self.user_logged, self.is_admin)
            elif msg == "user log out":
                self.user_logged, self.is_admin = users.user_log_out(conn, self.user_logged, self.is_admin)
            elif str(msg).startswith("user info"):
                response = users.user_info(self.user_logged)
                conn.sendall(f"[SERVER] {response}".encode("utf-8"))    
            elif str(msg).startswith("messages read"):
                #wyświeltania wiadomości od uztkowników
                pass
            elif str(msg).startswith("message read from"):
                #wyswietla wiadomosci od konkretnych uztkownkow
                pass
            elif str(msg).startswith("message new"):
                resposne = messages.message_new(msg, self.user_logged)
                pass
            elif str(msg).startswith("message delete"):
                #usuwa wiadomosc
                pass
            else:
                conn.sendall(f"[SERVER] You entered the wrong command or you don't have access to it".encode("utf-8"))
     
        conn.close()
        
    def response_load_users(self, response, conn):
        conn.sendall(f"[SERVER] {response}".encode("utf-8"))
        self.user_dict = users.load_users_json()
    
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
        self.send_json(time, conn)
    
    def info(self,conn):
        info_dict = { "Version of the server":self.VERSION, "Creation date": self.server_start_time.strftime('%a %d %b %Y, %I:%M%p')} 
        self.send_json(info_dict, conn)
    
    def help_command(self, conn):############zrobic pobieranie z jsona
        if not self.user_logged:
            commands_info = {
                "uptime": "server live time",
                "info": "returns the version number of the server, its creation date",
                "help": "returns a list of available commands with a short description",
                "stop": "stops the server and client at the same time",
                "user log in [NAME] [PASSWORD]": "Log in to the server by entering Name and Password"
            }
        elif self.is_admin == False:
            commands_info ={
                "uptime": "server live time",
                "info": "returns the version number of the server, its creation date",
                "help": "returns a list of available commands with a short description",
                "stop": "stops the server and client at the same time",
                "user log in [NAME] [PASSWORD]": "Log in to the server by entering Name and Password",
                "user info": "Shows who is currently logged in",
                "user log out": "Logs the user out"
                #messsage
                }
        elif self.is_admin == True:
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
                "users show": "Shows all server users"
            }
        
        self.send_json(commands_info, conn)

    def stop(self, conn):
        print("[CLOSING] Server has been closed")
        self.connected = False
        self.server_live = False
        conn.close()
       