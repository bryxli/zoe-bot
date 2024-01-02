import unittest

#from src.main.commands.league_commands import add_user
#from src.main.commands.server_commands import server_commands

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
