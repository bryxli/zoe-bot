import sys
import os
import json
import unittest

class TestLeagueLayer(unittest.TestCase):
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/layers/league/python'))
        sys.path.append(directory)

        from league import RiotAPI

        self.api_key = os.environ.get("RIOT_KEY")
        if self.api_key is None:
            config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../configs/config.json'))
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
            self.api_key = config.get("riot_key")
        self.RiotAPI = RiotAPI(self.api_key)

        sys.path.remove(directory)

    def test_get_AccountDto_by_riot_id():
        pass

    def test_get_AccountDto_by_puuid():
        pass

    def test_get_matchId_by_puuid():
        pass

    def test_get_MatchDto_by_matchId():
        pass

    def test_get_puuid_by_riot_id():
        pass

    def test_get_name_by_puuid():
        pass

    def test_get_match_by_puuid():
        pass

if __name__ == '__main__':
    unittest.main()
