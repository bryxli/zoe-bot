import requests
import cassiopeia as cass

class RiotAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.settings = {
            'global': {'version_from_match': 'patch'},
            'plugins': {},
            'pipeline': {'Cache': {}, 'DDragon': {}, 'RiotAPI': {'api_key': self.api_key}},
            'logging': {'print_calls': False, 'print_riot_api_key': False, 'default': 'WARNING', 'core': 'WARNING'}
        }
        cass.apply_settings(self.settings)

    def find_player_by_name(self, name, region):
        summoner = cass.get_summoner(name=name, region=region)
        if summoner.exists:
            return summoner
        return None

    def find_player_by_accountid(self, account_id, region):
        summoner = cass.get_summoner(account_id=account_id, region=region)
        if summoner.exists:
            return summoner
        return None
    
    def get_AccountDto_by_puuid(self, puuid):
        url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}" # TODO: url changes based on region
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def get_matchId_by_puuid(self, puuid):
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count=1" # TODO: url changes based on region
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response[0]
        else:
            return None
        
    def get_MatchDto_by_matchId(self, matchId):
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}" # TODO: url changes based on region
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None