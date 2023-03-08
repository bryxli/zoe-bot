import json

import cassiopeia as cass

with open('config.json') as file:
    config = json.load(file)

cass.set_riot_api_key(config['riot_key'])

def find_player(name, region):
    try:
        summoner_id = cass.get_summoner(name=name, region=region).puuid
        return summoner_id
    except Exception as e:
        print(e)