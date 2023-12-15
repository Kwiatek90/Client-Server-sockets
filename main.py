from src import server

server = server.Server("127.0.0.1", 65432, "v0.3.0", "config\database.ini")
server.start_server()

