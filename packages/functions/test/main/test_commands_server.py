import copy
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

class TestCommands(unittest.TestCase):
    
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/main'))
        sys.path.append(directory)

        from commands.server_commands import init
        self.init = init

        self.data = {
            'guild_id': '1',
            'channel_id': 1,
            'data': {
                'options': [
                    {'value': 'NA'}
                ]
            }
        }

        sys.path.remove(directory)

    def setUp(self):
        self.patcher_guild_exists = patch('dynamo.ZoeBotTable.guild_exists')
        self.mock_guild_exists = self.patcher_guild_exists.start()
        self.mock_guild_exists.return_value = True

        self.patcher_create_guild = patch('dynamo.ZoeBotTable.create_guild')
        self.mock_create_guild = self.patcher_create_guild.start()

        self.patcher_check_acknowledgment = patch('dynamo.ZoeBotTable.check_acknowledgment')
        self.mock_check_acknowledgment = self.patcher_check_acknowledgment.start()
        self.mock_check_acknowledgment.return_value = True

        self.patcher_get_webhook = patch('dynamo.ZoeBotTable.get_webhook')
        self.mock_get_webhook = self.patcher_get_webhook.start()
        self.mock_get_webhook.return_value = ''

        self.patcher_destroy_guild = patch('dynamo.ZoeBotTable.destroy_guild')
        self.mock_destroy_guild = self.patcher_destroy_guild.start()

        self.patcher_update_guild = patch('dynamo.ZoeBotTable.update_guild')
        self.mock_update_guild = self.patcher_update_guild.start()

        self.patcher_requests_post = patch('requests.post')
        self.mock_requests_post = self.patcher_requests_post.start()
        self.mock_requests_post_res = MagicMock()
        self.mock_requests_post_res.return_value = { 'id': '', 'url': '' }
        self.mock_requests_post.return_value = self.mock_requests_post_res

        self.patcher_requests_delete = patch('requests.delete')
        self.mock_requests_delete = self.patcher_requests_delete.start()

    def tearDown(self):
        self.patcher_guild_exists.stop()   
        self.patcher_create_guild.stop() 
        self.patcher_check_acknowledgment.stop() 
        self.patcher_get_webhook.stop() 
        self.patcher_destroy_guild.stop() 
        self.patcher_update_guild.stop()
        self.patcher_requests_post.stop()

    def test_init_guild_exists(self):
        res = self.init('setup', self.data)
        self.assertEqual(res, 'guild already exists')

    def test_init_guild(self):
        self.mock_guild_exists.return_value = False
        res = self.init('setup', self.data)
        self.assertEqual(res, 'guild initialized')

    def test_delete_guild_dne(self):
        self.mock_guild_exists.return_value = False
        res = self.init('reset', self.data)
        self.assertEqual(res, 'guild not registered')

    def test_delete_guild_acknowledgment(self):
        self.mock_check_acknowledgment.return_value = False
        res = self.init('reset', self.data)
        self.assertEqual(res, 'this action can be harmful, running /reset or /region <region> will delete all registered users. acknowledge with /acknowledge')

    def test_delete_guild(self):
        res = self.init('reset', self.data)
        self.assertEqual(res, 'guild deleted')

    def test_change_region_dne(self):
        self.mock_guild_exists.return_value = False
        res = self.init('region', self.data)
        self.assertEqual(res, 'guild not registered')

    def test_change_region_acknowledgment(self):
        self.mock_check_acknowledgment.return_value = False
        res = self.init('region', self.data)
        self.assertEqual(res, 'this action can be harmful, running /reset or /region <region> will delete all registered users. acknowledge with /acknowledge')

    def test_change_region_empty(self):
        invalid_data = copy.deepcopy(self.data)
        invalid_data['data'].pop('options')
        res = self.init('region', invalid_data)
        self.assertEqual(res, 'BR EUNE EUW JP KR LAN LAS NA OCE TR RU PH SG TH TW VN')

    def test_change_region_invalid_region(self):
        invalid_data = copy.deepcopy(self.data)
        invalid_data['data']['options'][0]['value'] = ''
        res = self.init('region', invalid_data)
        self.assertEqual(res, 'region not found')

    def test_change_region(self):
        res = self.init('region', self.data)
        self.assertEqual(res, 'guild region changed')

    def test_change_region(self):
        res = self.init('region', self.data)
        self.assertEqual(res, 'guild region changed')

    def test_acknowledge_dne(self):
        self.mock_guild_exists.return_value = False
        res = self.init('acknowledge', self.data)
        self.assertEqual(res, 'guild not registered')

    def test_acknowledge(self):
        res = self.init('acknowledge', self.data)
        self.assertEqual(res, 'successfully acknowledged')

if __name__ == '__main__':
    unittest.main()
