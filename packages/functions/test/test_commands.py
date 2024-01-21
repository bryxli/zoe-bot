import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main.commands.league_commands import init
#from src.main.commands.server_commands import init

class TestLeagueCommands(unittest.TestCase):
    

    def setUp(self):
        # TODO: create data for universal mocks
        pass


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
