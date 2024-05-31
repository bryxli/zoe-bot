import sys
import os
import unittest
from unittest.mock import MagicMock, patch

class TestTask(unittest.TestCase):
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src'))
        sys.path.append(directory)

        with patch('builtins.open', create=True) as mock_open:
            mock_template = MagicMock()
            mock_template.read.return_value = '{"win": [""], "lose": [""]}'
            mock_open.return_value.__enter__.return_value = mock_template

            from task.main import handler
            self.handler = handler

        sys.path.remove(directory)

    def setUp(self):
        self.patcher_get_all = patch('dynamo.ZoeBotTable.get_all')
        self.mock_get_all = self.patcher_get_all.start()
        self.mock_get_all.return_value = {
            'Items': [{
                'guild_id': { 'N': '1' },
                'region': { 'S': '' },
                'webhook_url': { 'S': '' },
                'userlist': { 'L': [{ 'M': {
                    'foo': { 'S': 'bar' }
                } }] }
            }]
        }

        self.patcher_guild_exists = patch('dynamo.ZoeBotTable.guild_exists')
        self.mock_guild_exists = self.patcher_guild_exists.start()
        self.mock_guild_exists.return_value = True

        self.patcher_get_match_by_puuid = patch('league.RiotAPI.get_match_by_puuid')
        self.mock_get_match_by_puuid = self.patcher_get_match_by_puuid.start()
        self.mock_get_match_by_puuid.return_value = {'info': {
            'gameId': '',
            'participants': [{
                'puuid': 'foo',
                'summonerName': '',
                'championName': '',
                'challenges': { 'kda': 1 },
                'win': True
            }]
        }}

        self.patcher_update_user = patch('dynamo.ZoeBotTable.update_user')
        self.mock_update_user = self.patcher_update_user.start()

        self.patcher_requests_post = patch('requests.post')
        self.mock_requests_post = self.patcher_requests_post.start()

    def tearDown(self):
        self.patcher_guild_exists.stop()
        self.patcher_get_match_by_puuid.stop()
        self.patcher_get_all.stop()
        self.patcher_update_user.stop()
        self.patcher_requests_post.stop()

    def test_process_guild_win(self):
        self.handler(None, None)

    def test_process_guild_lose(self):
        self.mock_get_match_by_puuid.return_value['info']['participants'][0]['win'] = False
        self.handler(None, None)

    def test_process_guild_exception(self):
        self.mock_get_match_by_puuid.side_effect = Exception()
        self.handler(None, None)

    def test_process_user_data_exception(self):
        self.mock_update_user.side_effect = Exception()
        self.handler(None, None)

if __name__ == '__main__':
    unittest.main()
