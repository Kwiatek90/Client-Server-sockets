from server import Server
from datetime import datetime
import time


server = Server("127.0.0.1", 65432, "v0.1.0")
server.start_server()


