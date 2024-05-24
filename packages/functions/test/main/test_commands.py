import sys
import os
import unittest
from unittest.mock import patch, MagicMock

class TestCommands(unittest.TestCase):
    
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/main'))
        sys.path.append(directory)

        from commands.league_commands import init as league_init
        from commands.server_commands import init as server_init
        self.league_init = league_init
        self.server_init = server_init

        self.data = {
            'guild_id': '1',
            'data': {
                'options': [
                    {'value': ''}, 
                    {'value': ''}
                ]
            }
        }

        sys.path.remove(directory)

    def setUp(self):
        self.patcher_guild_exists = patch('dynamo.ZoeBotTable.guild_exists')
        self.mock_guild_exists = self.patcher_guild_exists.start()
        self.mock_guild_exists.return_value = True

        self.patcher_get_guild = patch('dynamo.ZoeBotTable.get_guild')
        self.mock_get_guild = self.patcher_get_guild.start()
        self.mock_get_guild.return_value = {'region': {'S': ''}}

        self.patcher_add_user = patch('dynamo.ZoeBotTable.add_user')
        self.mock_add_user = self.patcher_add_user.start()

        self.patcher_get_puuid_by_riot_id = patch('league.RiotAPI.get_puuid_by_riot_id')
        self.mock_get_puuid_by_riot_id = self.patcher_get_puuid_by_riot_id.start()
        self.mock_get_puuid_by_riot_id.return_value = ''

    def tearDown(self):
        self.patcher_guild_exists.stop()
        self.patcher_get_guild.stop()
        self.patcher_get_puuid_by_riot_id.stop()
        self.patcher_add_user.stop()

    # TODO: tests not fully refined, does not test exceptions, conditions, etc

    def test_add_user_guild_dne(self):
        self.mock_guild_exists.return_value = False
        res = self.league_init('adduser', self.data)
        self.assertEqual(res, 'guild not registered')

    def test_add_user_invalid_username(self):
        self.mock_get_puuid_by_riot_id.side_effect = Exception()
        res = self.league_init('adduser', self.data)
        self.assertEqual(res, 'please enter a valid username')

    def test_add_user(self):
        res = self.league_init('adduser', self.data)
        self.assertEqual(res, 'player registered')
    
    # def test_delete_user(self):
    #     res = self.league_init('deluser', self.data)
    #     self.assertEqual(res, 'player deleted')

    # def test_userlist(self):
    #     res = self.league_init('userlist', self.data)
    #     self.assertEqual(res, 'no users are registered')

    # def test_init_guild(self):
    #     res = self.server_init('setup', self.data)
    #     self.assertEqual(res, 'guild already exists')

    # def test_delete_guild(self):
    #     res = self.server_init('reset', self.data)
    #     self.assertEqual(res, 'guild deleted')            

    # def test_change_region(self):
    #     res = self.server_init('region', self.data)
    #     self.assertEqual(res, 'region not found') 

    # def test_acknowledge(self):
    #     res = self.server_init('acknowledge', self.data)
    #     self.assertEqual(res, 'successfully acknowledged')  

if __name__ == '__main__':
    unittest.main()
