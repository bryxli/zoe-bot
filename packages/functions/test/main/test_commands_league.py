import sys
import os
import unittest
from unittest.mock import patch

class TestCommandsLeague(unittest.TestCase):
    
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/main'))
        sys.path.append(directory)

        from commands.league_commands import init
        self.init = init

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

        self.patcher_user_exists = patch('dynamo.ZoeBotTable.user_exists')
        self.mock_user_exists = self.patcher_user_exists.start()
        self.mock_user_exists.return_value = True

        self.patcher_delete_user = patch('dynamo.ZoeBotTable.delete_user')
        self.mock_delete_user = self.patcher_delete_user.start()

        self.patcher_get_all_users = patch('dynamo.ZoeBotTable.get_all_users')
        self.mock_get_all_users = self.patcher_get_all_users.start()
        self.mock_get_all_users.return_value = ['']

        self.patcher_get_puuid_by_riot_id = patch('league.RiotAPI.get_puuid_by_riot_id')
        self.mock_get_puuid_by_riot_id = self.patcher_get_puuid_by_riot_id.start()
        self.mock_get_puuid_by_riot_id.return_value = ''

        self.patcher_get_name_by_puuid = patch('league.RiotAPI.get_name_by_puuid')
        self.mock_get_name_by_puuid = self.patcher_get_name_by_puuid.start()
        self.mock_get_name_by_puuid.return_value = ''

    def tearDown(self):
        self.patcher_guild_exists.stop()
        self.patcher_get_guild.stop()
        self.patcher_add_user.stop()
        self.patcher_user_exists.stop()
        self.patcher_delete_user.stop()
        self.patcher_get_all_users.stop()
        self.patcher_get_puuid_by_riot_id.stop()
        self.patcher_get_name_by_puuid.stop()       

    def test_add_user_guild_dne(self):
        self.mock_guild_exists.return_value = False
        res = self.init('adduser', self.data)
        self.assertEqual(res, 'guild not registered')

    def test_add_user_invalid_username(self):
        self.mock_get_puuid_by_riot_id.side_effect = Exception()
        res = self.init('adduser', self.data)
        self.assertEqual(res, 'please enter a valid username')

    def test_add_user(self):
        res = self.init('adduser', self.data)
        self.assertEqual(res, 'player registered')

    def test_delete_user_guild_dne(self):
        self.mock_guild_exists.return_value = False
        res = self.init('deluser', self.data)
        self.assertEqual(res, 'guild not registered')

    def test_delete_user_invalid_username(self):
        self.mock_get_puuid_by_riot_id.side_effect = Exception()
        res = self.init('deluser', self.data)
        self.assertEqual(res, 'please enter a valid username')

    def test_delete_user_dne(self):
        self.mock_user_exists.return_value = False
        res = self.init('deluser', self.data)
        self.assertEqual(res, 'player not registered')
    
    def test_delete_user(self):
        res = self.init('deluser', self.data)
        self.assertEqual(res, 'player deleted')

    def test_userlist_guild_dne(self):
        self.mock_guild_exists.return_value = False
        res = self.init('userlist', self.data)
        self.assertEqual(res, 'guild not registered')

    def test_userlist_error(self):
        self.mock_get_name_by_puuid.side_effect = Exception()
        res = self.init('userlist', self.data)
        self.assertEqual(res, 'no users are registered')

    def test_userlist_zero(self):
        self.mock_get_all_users.return_value = []
        res = self.init('userlist', self.data)
        self.assertEqual(res, 'no users are registered')

    def test_userlist(self):
        res = self.init('userlist', self.data)
        self.assertEqual(res, '')

if __name__ == '__main__':
    unittest.main()
