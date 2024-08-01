import sys
import os
import unittest
from unittest.mock import MagicMock, patch

class TestApiGuild(unittest.TestCase):
    
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/api'))
        sys.path.append(directory)

        sys.modules['dynamo'] = MagicMock()
        sys.modules['league'] = MagicMock()

        from guild.setup import handler as handler_setup
        self.handler_setup = handler_setup

        self.event_setup = {
            'body': {
                'apiKey':'foo',
                'guildId': 'bar',
                'channelId': 'foobar'
            }
        } # happy path

        sys.path.remove(directory)

    def setUp(self):
        self.patcher_guild_exists = patch('dynamo.ZoeBotTable.guild_exists')
        self.mock_guild_exists = self.patcher_guild_exists.start()
        self.mock_guild_exists.return_value = True

        self.patcher_auth = patch('auth')
        self.mock_auth = self.patcher_auth.start()
        self.mock_auth.return_value = True

        self.patcher_requests_post = patch('requests.post')
        self.mock_requests_post = self.patcher_requests_post.start()
        self.mock_requests_post_res = MagicMock()
        self.mock_requests_post_res.return_value = { 'id': '', 'url': '' }
        self.mock_requests_post.return_value = self.mock_requests_post_res

        self.patcher_guild_exists = patch('dynamo.ZoeBotTable.create_guild')
        self.mock_guild_exists = self.patcher_guild_exists.start()

    def tearDown(self):
        self.patcher_guild_exists.stop()   
        self.patcher_auth.stop()
        self.patcher_requests_post.stop()

    def test_missing_params(self):
        event_missing_params = {
            'body': {}
        }
        res = self.handler_setup(event_missing_params, None)
        self.assertEqual(res['statusCode'], 400)

if __name__ == '__main__':
    unittest.main()
