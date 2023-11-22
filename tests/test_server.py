import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from server import Server

class UsersTests(unittest.TestCase):
    def test(self):
        server = Server()
        
    