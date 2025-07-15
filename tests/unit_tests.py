import unittest
from core.socket_without_powers import ParentSocket

class TestParentSocket(unittest.TestCase):
    def setUp(self):
        self.parent_socket = ParentSocket()
        super().setUp()
    
    def tearDown(self):
        self.parent_socket.close()

    def test_constants(self):
        self.assertEqual(self.parent_socket.KB, 1024)

if __name__ == '__main__':
    unittest.main()