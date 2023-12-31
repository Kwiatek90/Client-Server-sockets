import socket
class Client():
    def __init__(self, HOST, PORT) -> None:
        self.PORT = PORT
        self.HOST = HOST
        self.ADDR = (self.HOST, self.PORT)

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client.connect(self.ADDR)
        msg_connected = self.client.recv(1024).decode("utf-8")
        print(msg_connected)
        if msg_connected:
            self.send()
        else:
            self.client.close()
            

    def send(self):
        while True:
            msg = input(f"[CLIENT] Enter your message to the {self.HOST}\n")
            msg = msg.encode("utf-8")
            self.client.sendall(msg)
            
            msg_from_server = self.client.recv(1024).decode("utf-8")
            print(msg_from_server)
            
            if not msg_from_server:
                print("[SERVER] The server has been closed")
                print("[CLIENT] You are disconnected from the server")
                break
            
client = Client("127.0.0.1",65432)
client.connect_to_server()
