import sys
import os
import unittest

class TestLeagueLayer(unittest.TestCase):
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/layers/league/python'))
        sys.path.append(directory)

        from league import RiotAPI
        self.RiotAPI = RiotAPI

        sys.path.remove(directory)

    def test_league(self):
        res = 'test'
        self.assertEqual(res, 'test')   

if __name__ == '__main__':
    unittest.main()
