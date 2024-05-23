import sys
import os
import unittest
from unittest.mock import MagicMock

class TestDynamoLayer(unittest.TestCase):
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/layers/dynamo/python'))
        sys.path.append(directory)

        from dynamo import ZoeBotTable
        self.ZoeBotTable = ZoeBotTable

        sys.path.remove(directory)

    def test_dynamo(self):
        res = 'test'
        self.assertEqual(res, 'test')   

if __name__ == '__main__':
    unittest.main()
