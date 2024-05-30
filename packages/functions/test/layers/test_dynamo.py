import sys
import os
import json
import unittest

class TestDynamoLayer(unittest.TestCase):
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/layers/dynamo/python'))
        sys.path.append(directory)

        from dynamo import ZoeBotTable

        self.region = os.environ.get("SET_AWS_REGION")
        if self.region is None:
            config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../configs/config.json'))
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
            self.region = config.get("aws_region")
        self.stage = "dev"
        self.db = ZoeBotTable(self.region, self.stage)

        sys.path.remove(directory)

    def test_get_all(self):
        res = self.db.get_all()
        self.assertIn("{'Items': ", str(res))

    def test_dynamo_actions(self):
        GUILD_ID = '1'

        mock_guild = {'webhook_url': {'S': ''}, 'region': {'S': 'NA'}, 'guild_id': {'N': '1'}, 'acknowledgment': {'BOOL': False}, 'userlist': {'L': []}, 'webhook_id': {'S': 'foo'}}

        def test_guild_mock():
            res = self.db.get_guild(GUILD_ID)
            return res == mock_guild

        def test_create_guild():
            WEBHOOK_ID = 'foo'
            WEBHOOK_URL = ''

            res = self.db.create_guild(GUILD_ID, WEBHOOK_ID, WEBHOOK_URL)
            self.assertTrue(res)

            res = self.db.get_all()
            self.assertIn("guild_id': {'N': '1'}", str(res))

        def test_guild_exists():
            res = self.db.guild_exists(GUILD_ID)
            self.assertTrue(res)

        def test_get_guild():
            self.assertTrue(test_guild_mock())

        def test_update_guild():
            UPDATED_WEBHOOK_URL = 'bar'
            updates = {'webhook_url' : {'Value': {'S': UPDATED_WEBHOOK_URL}, 'Action': 'PUT'}}

            res = self.db.update_guild(GUILD_ID, updates)
            self.assertTrue(res)

            mock_guild['webhook_url'] = {'S': UPDATED_WEBHOOK_URL}
            self.assertTrue(test_guild_mock())

        def test_add_user():
            res = self.db.add_user(GUILD_ID, 'user_1')
            self.assertTrue(res)

            mock_guild['userlist']['L'].append({
                'M': { 'user_1': { 'S': '' }}
            })
            self.assertTrue(test_guild_mock())

        def test_user_exists():
            res = self.db.user_exists(GUILD_ID, 'user_1')
            self.assertTrue(res)

        def test_get_all_users():
            self.db.add_user(GUILD_ID, 'user_2')

            res = self.db.get_all_users(GUILD_ID)
            self.assertEqual(res, ['user_1', 'user_2'])

        def test_delete_user():
            res = self.db.delete_user(GUILD_ID, 'user_2')
            self.assertTrue(res)

            self.assertTrue(test_guild_mock())

        def test_update_user():
            res = self.db.update_user(GUILD_ID, 'user_1', 'foo')
            self.assertTrue(res)

            mock_guild['userlist']['L'][0]['M']['user_1']['S'] = 'foo'
            self.assertTrue(test_guild_mock())

        def test_check_acknowledgment():
            res = self.db.check_acknowledgment(GUILD_ID)
            self.assertFalse(res)

        def test_get_webhook():
            res = self.db.get_webhook(GUILD_ID)
            self.assertEqual(res, 'foo')

        def test_destroy_guild():
            res = self.db.destroy_guild(GUILD_ID)
            self.assertTrue(res)

            destroyed_guild = self.db.get_guild(GUILD_ID)
            self.assertEqual(destroyed_guild, {})

        test_create_guild()
        test_guild_exists()
        test_get_guild()
        test_update_guild()
        test_add_user()
        test_user_exists()
        test_get_all_users()
        test_delete_user()
        test_update_user()
        test_check_acknowledgment()
        test_get_webhook()
        test_destroy_guild()

if __name__ == '__main__':
    unittest.main()
