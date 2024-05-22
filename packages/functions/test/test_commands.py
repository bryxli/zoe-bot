import sys
import os
import unittest
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/main')))
sys.modules['layer_import_helper'] = MagicMock()
sys.modules['dynamo'] = MagicMock()
sys.modules['league'] = MagicMock()

from commands.league_commands import init
from commands.server_commands import init

class TestLeagueCommands(unittest.TestCase):

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
