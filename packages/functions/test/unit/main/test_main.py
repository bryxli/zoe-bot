import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from functools import wraps

class TestMain(unittest.TestCase):
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src'))
        sys.path.append(directory)

        with patch('builtins.open', create=True) as mock_open:
            mock_template = MagicMock()
            mock_template.read.return_value = '{"response": ["speak"]}'
            mock_open.return_value.__enter__.return_value = mock_template

            def mock_verify_key_decorator(client_public_key):
                def _decorator(f):
                    @wraps(f)
                    def __decorator(*args, **kwargs):
                        return f(*args, **kwargs)
                    return __decorator
                return _decorator
            
            with patch('discord_interactions.verify_key_decorator', mock_verify_key_decorator):
                from main.main import app
                self.app = app.test_client()

        sys.path.remove(directory)

    def test_ping(self):
        raw_request = { 'type': 1 }
        res = self.app.post('/', json=raw_request)
        self.assertIn('{"type":1}', str(res.data))

    def test_help(self):
        raw_request = {
            'type': 0,
            'data': { 'name': 'help' }
        }
        res = self.app.post('/', json=raw_request)
        self.assertIn('/setup - create guild instance', str(res.data))

    def test_speak(self):
        raw_request = {
            'type': 0,
            'data': { 'name': 'speak' }
        }
        res = self.app.post('/', json=raw_request)
        self.assertIn('speak', str(res.data))

    def test_server(self):
        with patch('commands.server_commands.init', MagicMock(return_value = 'server command initialized')):
            raw_request = {
                'type': 0,
                'data': { 'name': 'setup' }
            }
            res = self.app.post('/', json=raw_request)
            self.assertIn('server command initialized', str(res.data))

    def test_league(self):
        with patch('commands.league_commands.init', MagicMock(return_value = 'league command initialized')):
            raw_request = {
                'type': 0,
                'data': { 'name': 'adduser' }
            }
            res = self.app.post('/', json=raw_request)
            self.assertIn('league command initialized', str(res.data))

if __name__ == '__main__':
    unittest.main()
