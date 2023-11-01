import json
import socket
import time

class Server:
    def __init__(self, HOST, PORT) -> None:
        self.HOST = HOST
        self.PORT = PORT
        self.ADDR = (self.HOST, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_time = time.time()
    
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
            if msg == "stop":
                connected = False
                self.server_live = False
        
        conn.close()
            
    def uptime(self, conn):
        time = {"Live of server": f"{time.time() - self.server_time}"}
        time_json = json.dumps(time, indent=1)
        conn.send(time_json.encode("utf-8"))
    
    def help_command(self):
        self.commands_info = {
            "uptime": "zwraca czas życia serwera",
            "info": "zwraca numer wersji serwera, datę jego utworzenia",
            "help": "zwraca listę dostępnych komend z krótkim opisem",
            "stop": "zatrzymuje jednocześnie serwer i klienta"
        }
    
    def info(self):
        pass
    
    def stop(self):
        pass
