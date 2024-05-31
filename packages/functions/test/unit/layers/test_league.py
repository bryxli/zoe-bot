import sys
import os
import json
import unittest

class TestLeagueLayer(unittest.TestCase):
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName)

        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src/layers/league/python'))
        sys.path.append(directory)

        from league import RiotAPI

        self.api_key = os.environ.get("RIOT_KEY")
        if self.api_key is None:
            config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../configs/config.json'))
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
            self.api_key = config.get("riot_key")
        self.RiotAPI = RiotAPI(self.api_key)

        sys.path.remove(directory)

    def test_league_actions(self):
        def test_get_AccountDto_by_riot_id():
            res = self.RiotAPI.get_AccountDto_by_riot_id('bryxli', 'NA1', 'NA')
            self.assertIn("'gameName': 'bryxli', 'tagLine': 'NA1'}", str(res))
            return res

        def test_get_AccountDto_by_puuid(puuid):
            res = self.RiotAPI.get_AccountDto_by_puuid(puuid, 'NA')
            self.assertIn("'gameName': 'bryxli', 'tagLine': 'NA1'}", str(res))

        def test_get_matchId_by_puuid(puuid):
            res = self.RiotAPI.get_matchId_by_puuid(puuid, 'NA')
            if not res.startswith('NA1_'):
                self.assertTrue(False)
            return res

        def test_get_MatchDto_by_matchId(matchId):
            res = self.RiotAPI.get_MatchDto_by_matchId(matchId, 'NA')
            self.assertIn(f"'matchId': '{matchId}'", str(res))

        def test_get_AccountDto_by_riot_id_error():
            try:
                self.RiotAPI.get_AccountDto_by_riot_id('GN', 'NA1', 'NA')
            except:
                pass
            else:
                self.assertTrue(False)

        def test_get_AccountDto_by_puuid_error():
            try:
                self.RiotAPI.get_AccountDto_by_puuid('foo', 'NA')
            except:
                pass
            else:
                self.assertTrue(False)

        def test_get_matchId_by_puuid_error():
            try:
                self.RiotAPI.get_matchId_by_puuid('foo', 'NA')
            except:
                pass
            else:
                self.assertTrue(False)

        def test_get_MatchDto_by_matchId_error():
            try:
                self.RiotAPI.get_MatchDto_by_matchId('foo', 'NA')
            except:
                pass
            else:
                self.assertTrue(False)

        def test_get_puuid_by_riot_id():
            try:
                puuid = self.RiotAPI.get_puuid_by_riot_id('bryxli', 'NA1', 'NA')
            except:
                self.assertTrue(False)
            return puuid

        def test_get_name_by_puuid(puuid):
            try:
                self.RiotAPI.get_name_by_puuid(puuid, 'NA')
            except:
                self.assertTrue(False)

        def test_get_match_by_puuid(puuid):
            try:
                self.RiotAPI.get_match_by_puuid(puuid, 'NA')
            except:
                self.assertTrue(False)

        test_get_AccountDto_by_riot_id()['puuid']
        puuid = test_get_puuid_by_riot_id()

        matchId = test_get_matchId_by_puuid(puuid)
        test_get_MatchDto_by_matchId(matchId)

        test_get_AccountDto_by_puuid(puuid)
        test_get_name_by_puuid(puuid)
        test_get_match_by_puuid(puuid)

        test_get_AccountDto_by_riot_id_error()
        test_get_AccountDto_by_puuid_error()
        test_get_matchId_by_puuid_error()
        test_get_MatchDto_by_matchId_error()

if __name__ == '__main__':
    unittest.main()
