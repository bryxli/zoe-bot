import json
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

class TestApiGuild(unittest.TestCase):
    
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        self.dynamo_mock = MagicMock()
        self.dynamo_mock.ZoeBotTable = MagicMock()
        self.dynamo_mock.ZoeBotTable.return_value.create_guild = MagicMock(return_value=True)

        self.event_setup = {
            'body': {
                'apiKey':'foo',
                'guildId': 'bar',
                'channelId': 'foobar'
            }
        }

    def setUp(self):
        self.patcher_auth = patch('src.api.common.auth')
        self.mock_auth = self.patcher_auth.start()
        self.mock_auth.return_value = True

        self.patcher_requests_post = patch('requests.post')
        self.mock_requests_post = self.patcher_requests_post.start()

    def tearDown(self):
        self.patcher_auth.stop()
        self.patcher_requests_post.stop()

    def setup(self, event, params=None):
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/api'))
        sys.path.append(directory)
        
        if params == 'test_guild_exists':
            self.dynamo_mock.ZoeBotTable.return_value.guild_exists = MagicMock(return_value=True)
        else:
            self.dynamo_mock.ZoeBotTable.return_value.guild_exists = MagicMock(return_value=False)

        with patch.dict(sys.modules, {'dynamo': self.dynamo_mock, 'league': MagicMock()}):
            from guild.setup import handler
            sys.path.remove(directory)

            return handler(event, None)
        
    def delete(self, event, params=None):
        pass

    def get(self, event, params=None):
        pass

    def region(self, event, params=None):
        pass

    def acknowledge(self, event, params=None):
        pass

    def test_missing_params(self):
        event_missing_params = {
            'body': {}
        }
        res = self.setup(json.dumps(event_missing_params))
        self.assertEqual(res['statusCode'], 400)

    def test_api_key(self):
        self.mock_auth.return_value = False
        res = self.setup(json.dumps(self.event_setup))
        self.assertEqual(res['statusCode'], 401)

    def test_guild_exists(self):
        res = self.setup(json.dumps(self.event_setup), 'test_guild_exists')
        self.assertEqual(res['statusCode'], 409)

    def test_webhook_error(self):
        self.mock_requests_post.side_effect = Exception()
        res = self.setup(json.dumps(self.event_setup))
        self.assertEqual(res['statusCode'], 500)

    def test_success(self):
        res = self.setup(json.dumps(self.event_setup))
        self.assertEqual(res['statusCode'], 201)

if __name__ == '__main__':
    unittest.main()
