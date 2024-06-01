import sys
import os
import json

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

        