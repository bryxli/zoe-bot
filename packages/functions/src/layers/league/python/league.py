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

    def get_continent(self, region):
        if region is Region.brazil:
            return Continent.americas
        if region is Region.europe_north_east:
            return Continent.europe
        if region is Region.europe_west:
            return Continent.europe
        if region is Region.japan:
            return Continent.asia
        if region is Region.korea:
            return Continent.asia
        if region is Region.latin_america_north:
            return Continent.americas
        if region is Region.latin_america_south:
            return Continent.americas
        if region is Region.north_america:
            return Continent.americas
        if region is Region.oceania:
            return Continent.sea
        if region is Region.turkey:
            return Continent.europe
        if region is Region.russia:
            return Continent.europe
        if region is Region.philippines:
            return Continent.sea
        if region is Region.singapore:
            return Continent.sea
        if region is Region.thailand:
            return Continent.sea
        if region is Region.taiwan:
            return Continent.sea
        if region is Region.vietnam:
            return Continent.sea
    
    def get_AccountDto_by_riot_id(self, riot_id, region): # TODO
        pass

    def get_AccountDto_by_puuid(self, puuid, region):
        continent = self.get_continent(region)
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
        continent = self.get_continent(region)
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
        continent = self.get_continent(region)
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
