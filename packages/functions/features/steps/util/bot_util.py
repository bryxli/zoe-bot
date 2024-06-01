import sys
import os
from unittest.mock import patch
from functools import wraps

class BotUtil:
    def __init__(self):
        dynamo_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src/layers/dynamo/python'))
        league_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src/layers/league/python'))
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src/main'))

        sys.path.append(dynamo_directory)
        sys.path.append(league_directory)
        sys.path.append(directory)

        def mock_verify_key_decorator(client_public_key):
            def _decorator(f):
                @wraps(f)
                def __decorator(*args, **kwargs):
                    return f(*args, **kwargs)
                return __decorator
            return _decorator
            
        with patch('discord_interactions.verify_key_decorator', mock_verify_key_decorator):
            from main import app
            self.app = app.test_client()

        sys.path.remove(dynamo_directory)
        sys.path.remove(league_directory)
        sys.path.remove(directory)

    def send_command(self, data):
        res = str(self.app.post('/', json=data).get_json())

        if '/setup - create guild instance' in res:
            return 'command information'
        elif data['data']['name'] == 'speak':
            return 'a random voice line'

        return res