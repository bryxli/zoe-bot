import sys
import os
import unittest
from unittest.mock import MagicMock, patch

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

        self.data = {
            "guild_id": 1,
            "data": {
                "options": [
                    {"value": "foo"}, 
                    {"value": "bar"}
                ]
            }
        }

        sys.path.remove(directory)

    # TODO: tests not fully refined, does not test exceptions, conditions, etc

    def test_add_user(self):
        res = self.league_init('adduser', self.data)
        self.assertEqual(res, 'player registered')
    
    def test_delete_user(self):
        res = self.league_init('deluser', self.data)
        self.assertEqual(res, 'player deleted')

    def test_userlist(self):
        res = self.league_init('userlist', self.data)
        self.assertEqual(res, 'no users are registered')

    def test_init_guild(self):
        res = self.server_init('setup', self.data)
        self.assertEqual(res, 'guild already exists')

    def test_delete_guild(self):
        res = self.server_init('reset', self.data)
        self.assertEqual(res, 'guild deleted')            

    def test_change_region(self):
        res = self.server_init('region', self.data)
        self.assertEqual(res, 'region not found') 

    def test_acknowledge(self):
        res = self.server_init('acknowledge', self.data)
        self.assertEqual(res, 'successfully acknowledged')  

if __name__ == '__main__':
    unittest.main()
