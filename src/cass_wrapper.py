import json

import cassiopeia as cass

with open('config.json') as file:
    config = json.load(file)

settings = {
    'global': {'version_from_match': 'patch'},
    'plugins': {},
    'pipeline': {'Cache': {}, 'DDragon': {}, 'RiotAPI': {'api_key': config['riot_key']}},
    'logging': {'print_calls': False, 'print_riot_api_key': False, 'default': 'WARNING', 'core': 'WARNING'}
}
cass.apply_settings(settings)

def find_player_by_name(name, region):
    summoner = cass.get_summoner(name=name, region=region)
    if (summoner.exists):
        return summoner
    return None

def find_player_by_accountid(accountid, region):
    summoner = cass.get_summoner(account_id=accountid, region=region)
    if(summoner.exists):
        return summoner
    return None

# me = find_player_by_name('bryxli', 'NA')