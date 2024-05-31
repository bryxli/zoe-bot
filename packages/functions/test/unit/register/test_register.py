import sys
import os
import unittest
from unittest.mock import MagicMock, patch

class TestRegister(unittest.TestCase):
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src'))
        sys.path.append(directory)

        with patch('builtins.open', create=True) as mock_open:
            mock_yaml = MagicMock()
            mock_yaml.read.return_value = '[{ "name": "" }]'
            mock_open.return_value.__enter__.return_value = mock_yaml
            
            from register.main import handler
            self.handler = handler

        sys.path.remove(directory)

    def setUp(self):
        self.patcher_requests_post = patch('requests.post')
        self.mock_requests_post = self.patcher_requests_post.start()
        self.mock_requests_post_res = MagicMock()
        self.mock_requests_post_res.status_code = 201
        self.mock_requests_post.return_value = self.mock_requests_post_res

    def tearDown(self):
        self.patcher_requests_post.stop()

    def test_register(self):
        self.handler(None, None)

    # TODO: test_register_429 creates infinite loop due to status never getting past 429
    # def test_register_429(self):
    #     self.mock_requests_post_res.status_code = 429
    #     self.handler(None, None)

    def test_register_error(self):
        self.mock_requests_post_res.status_code = 1
        self.handler(None, None)

if __name__ == '__main__':
    unittest.main()
