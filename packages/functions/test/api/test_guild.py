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

        self.event_data = {
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
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/api'))
        sys.path.append(directory)
        
        if params == 'test_guild_dne':
            self.dynamo_mock.ZoeBotTable.return_value.guild_exists = MagicMock(return_value=False)
        elif params == 'test_not_acknowledged':
            self.dynamo_mock.ZoeBotTable.return_value.guild_exists = MagicMock(return_value=True)
            self.dynamo_mock.ZoeBotTable.return_value.check_acknowledgment = MagicMock(return_value=False)
        else:
            self.dynamo_mock.ZoeBotTable.return_value.guild_exists = MagicMock(return_value=True)
            self.dynamo_mock.ZoeBotTable.return_value.check_acknowledgment = MagicMock(return_value=True)

        with patch.dict(sys.modules, {'dynamo': self.dynamo_mock, 'league': MagicMock()}):
            from guild.delete import handler
            sys.path.remove(directory)

            return handler(event, None)

    def get(self, event, params=None): # todo
        pass

    def region(self, event, params=None): # todo
        pass

    def acknowledge(self, event, params=None): # todo
        pass

    def test_setup_missing_params(self):
        event_missing_params = {
            'body': {}
        }
        res = self.setup(json.dumps(event_missing_params))
        self.assertEqual(res['statusCode'], 400)

    def test_setup_api_key(self):
        self.mock_auth.return_value = False
        res = self.setup(json.dumps(self.event_data))
        self.assertEqual(res['statusCode'], 401)

    def test_setup_guild_exists(self):
        res = self.setup(json.dumps(self.event_data), 'test_guild_exists')
        self.assertEqual(res['statusCode'], 409)

    def test_setup_webhook_error(self):
        self.mock_requests_post.side_effect = Exception()
        res = self.setup(json.dumps(self.event_data))
        self.assertEqual(res['statusCode'], 500)

    def test_setup_success(self):
        res = self.setup(json.dumps(self.event_data))
        self.assertEqual(res['statusCode'], 201)

    def test_delete_missing_params(self):
        event_missing_params = {
            'body': {}
        }
        res = self.delete(json.dumps(event_missing_params))
        self.assertEqual(res['statusCode'], 400)

    def test_delete_api_key(self):
        self.mock_auth.return_value = False
        res = self.delete(json.dumps(self.event_data))
        self.assertEqual(res['statusCode'], 401)

    def test_delete_guild_dne(self):
        res = self.delete(json.dumps(self.event_data), 'test_guild_dne')
        self.assertEqual(res['statusCode'], 404)

    # def test_delete_not_acknowledged(self):
    #     res = self.delete(json.dumps(self.event_data), 'test_not_acknowledged')
    #     self.assertEqual(res['statusCode'], 403)

    # def test_delete_success(self):
    #     res = self.delete(json.dumps(self.event_data))
    #     self.assertEqual(res['statusCode'], 200)

    def test_get_missing_params(self): # todo
        pass

    def test_get_api_key(self): # todo
        pass

    def test_get_guild_dne(self): # todo
        pass

    def test_get_success(self): # todo
        pass

    # TODO: create region and acknowledge tests

if __name__ == '__main__':
    unittest.main()
