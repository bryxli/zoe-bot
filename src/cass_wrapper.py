import json

import cassiopeia as cass

with open('config.json') as file:
    config = json.load(file)

cass.set_riot_api_key(config['riot_key'])

def find_player_by_name(name, region):
    try:
        summoner = cass.get_summoner(name=name, region=region)
        summoner.puuid
        return summoner
    except Exception as e:
        return e