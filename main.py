from server import Server

server = Server("127.0.0.1", 65432, "v0.2.0", "config\database.ini")
server.start_server()



