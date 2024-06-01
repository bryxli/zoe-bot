import sys
import os
import json

GUILD_ID = '1'
WEBHOOK_ID = ''
WEBHOOK_URL = ''

class GuildUtil:
    def __init__(self):
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src/layers/dynamo/python'))
        sys.path.append(directory)

        from dynamo import ZoeBotTable

        self.region = os.environ.get("SET_AWS_REGION")
        if self.region is None:
            config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../configs/config.json'))
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
            self.region = config.get("aws_region")
        self.stage = "dev"
        self.db = ZoeBotTable(self.region, self.stage)

        sys.path.remove(directory)

    def delete_guild(self):
        self.db.destroy_guild(GUILD_ID)

    def create_guild(self):
        self.db.create_guild(GUILD_ID, WEBHOOK_ID, WEBHOOK_URL)

    def acknowledge(self):
        UPDATES = {
            'acknowledgment' : {'Value': {'BOOL': True}, 'Action': 'PUT'}
        }
        self.db.update_guild(GUILD_ID, UPDATES)

    def add_users(self):
        pass # TODO

        