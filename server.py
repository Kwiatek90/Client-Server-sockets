import socket

HEADER = 64 #Określenie ilości bytes
PORT = 65432
HOST = "127.0.0.1"
ADDR = (HOST, PORT)
CONNECTIONS = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(ADDR)

def client_connection(conn, adrr):
    print(f"[NEW CONNECTION] {adrr} connected.")
    
    connected = True
    if connected:
        msg = conn.recv(HEADER)    
        

def start_server():
    s.listen()
    while True:
        conn, adrr = s.accept()
        client_connection(conn, adrr)
        CONNECTIONS += 1
        print(f"[ACTIVE CONNECTIONS] {CONNECTIONS}")
        

print("[STARTING] Server is starting ...")
start_server()