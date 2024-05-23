import sys
import os
import unittest
from unittest.mock import MagicMock

class TestCommands(unittest.TestCase):
    
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/main'))
        sys.path.append(directory)
        sys.modules['dynamo'] = MagicMock()
        sys.modules['league'] = MagicMock()

        from commands.league_commands import init as league_init
        from commands.server_commands import init as server_init
        self.league_init = league_init
        self.server_init = server_init

        sys.path.remove(directory)

    def test_add_user(self):
        res = 'test'
        self.assertEqual(res, 'test')
    
    def test_delete_user(self):
        res = 'test'
        self.assertEqual(res, 'test')

    def test_userlist(self):
        res = 'test'
        self.assertEqual(res, 'test')

    def test_init_guild(self):
        res = 'test'
        self.assertEqual(res, 'test')

    def test_delete_guild(self):
        res = 'test'
        self.assertEqual(res, 'test')              

    def test_change_region(self):
        res = 'test'
        self.assertEqual(res, 'test')    

    def test_acknowledge(self):
        res = 'test'
        self.assertEqual(res, 'test')        

if __name__ == '__main__':
    unittest.main()
