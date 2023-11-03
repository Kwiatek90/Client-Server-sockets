import json
import socket
import time
from datetime import datetime

class Server:
    def __init__(self, HOST, PORT, VERSION) -> None:
        self.HOST = HOST
        self.PORT = PORT
        self.VERSION = VERSION
        self.ADDR = (self.HOST, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_start_time = datetime.now().replace(microsecond=0)
    
    def start_server(self):
        print("[STARTING] Server is starting ...")
        self.server.bind(self.ADDR)
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.HOST}")
        
        self.server_live = True
        while self.server_live:
            conn, adrr = self.server.accept()
            self.client_connection(conn, adrr)
            
        self.server.close()
            
    def client_connection(self, conn, adrr):
        print(f"[NEW CONNECTION] {adrr} connected.")
        conn.sendall(f"[SERVER] You are connected to the {self.HOST}".encode("utf-8"))
    
        connected = True
        while connected:
            msg = conn.recv(1024).decode("utf-8")
            if msg == 'uptime':
                self.uptime(conn)
            elif msg == "info":
                self.info(conn)
            elif msg == "help":
                self.help_command(conn)
            elif msg == "stop":
                connected = False
                self.server_live = False
        
        conn.close()
    
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
    
    def help_command(self, conn):
        commands_info = {
            "uptime": "server live time",
            "info": "returns the version number of the server, its creation date",
            "help": "returns a list of available commands with a short description",
            "stop": "stops the server and client at the same time"
        }
        self.send_json(commands_info, conn)

    def stop(self):
        pass
