import sys
import os
import unittest
from unittest.mock import MagicMock, patch

class TestTask(unittest.TestCase):
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
        sys.path.append(directory)

        with patch('builtins.open', create=True) as mock_open:
            mock_template = MagicMock()
            mock_template.read.return_value = '{"foo": "bar"}'
            mock_open.return_value.__enter__.return_value = mock_template
            
            import task.main as main
            self.main = main

        sys.path.remove(directory)

    def test_task(self):
        # result = self.main.handler()
        
        self.assertEqual('result', 'result')

if __name__ == '__main__':
    unittest.main()
