import sys
import os
import unittest

class TestDynamoLayer(unittest.TestCase):
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/layers/dynamo/python'))
        sys.path.append(directory)

        from dynamo import ZoeBotTable

        self.region = os.environ.get("SET_AWS_REGION")
        self.stage = "dev"
        self.db = ZoeBotTable(self.region, self.stage)

        sys.path.remove(directory)

    def test_get_all(self):
        res = self.db.get_all()
        self.assertIn("{'Items': ", str(res))

    def test_guild_actions(self):
        def test_create_guild(self):
            self.assertTrue(True)

        def test_guild_exists(self):
            self.assertTrue(True)

        def test_get_guild(self):
            self.assertTrue(False)

        def test_update_guild(self):
            self.assertTrue(False)

        test_create_guild(self)
        test_guild_exists(self)
        test_get_guild(self)
        test_update_guild(self)
        #add_user
        #get_all_users
        #user_exists
        #update_user
        #delete_user
        #check_aknowledgment
        #get_webhook
        #destroy_guild

if __name__ == '__main__':
    unittest.main()
