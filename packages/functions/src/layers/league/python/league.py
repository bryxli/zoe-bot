import requests
from enum import Enum

class Continent(Enum):
    americas = "americas"
    asia = "asia"
    europe = "europe"
    sea = "sea"

class Region(Enum):
    brazil = "BR"
    europe_north_east = "EUNE"
    europe_west = "EUW"
    japan = "JP"
    korea = "KR"
    latin_america_north = "LAN"
    latin_america_south = "LAS"
    north_america = "NA"
    oceania = "OCE"
    turkey = "TR"
    russia = "RU"
    philippines = "PH"
    singapore = "SG"
    thailand = "TH"
    taiwan = "TW"
    vietnam = "VN"

class RiotAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.region_map = {
            Region.brazil: Continent.americas,
            Region.europe_north_east: Continent.europe,
            Region.europe_west: Continent.europe,
            Region.japan: Continent.asia,
            Region.korea: Continent.asia,
            Region.latin_america_north: Continent.americas,
            Region.latin_america_south: Continent.americas,
            Region.north_america: Continent.americas,
            Region.oceania: Continent.sea,
            Region.turkey: Continent.europe,
            Region.russia: Continent.europe,
            Region.philippines: Continent.sea,
            Region.singapore: Continent.sea,
            Region.thailand: Continent.sea,
            Region.taiwan: Continent.sea,
            Region.vietnam: Continent.sea
        }
    
    def get_AccountDto_by_riot_id(self, riot_id, region): # TODO
        pass

    def get_AccountDto_by_puuid(self, puuid, region):
        continent = self.region_map[region]
        url = f"https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def get_matchId_by_puuid(self, puuid, region):
        continent = self.region_map[region]
        print(region + " " + continent)
        url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count=1"
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response[0]
        else:
            return None
        
    def get_MatchDto_by_matchId(self, matchId, region):
        continent = self.region_map[region]
        url = f"https://{continent}.api.riotgames.com/lol/match/v5/matches/{matchId}"
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def get_puuid_by_riot_id(self, riot_id, region):
        AccountDto = self.get_AccountDto_by_riot_id(riot_id, region)
        return AccountDto["puuid"]

    def get_name_by_puuid(self, puuid, region):
        AccountDto = self.get_AccountDto_by_puuid(puuid, region)
        return AccountDto["gameName"]

    def get_match_by_puuid(self, puuid, region):
        matchId = self.get_matchId_by_puuid(puuid, region)
        MatchDto = self.get_MatchDto_by_matchId(matchId, region)
        return MatchDto
