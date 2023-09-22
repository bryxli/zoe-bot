import os
import cassiopeia as cass

RIOT_KEY = os.environ.get("RIOT_KEY")

settings = {
    'global': {'version_from_match': 'patch'},
    'plugins': {},
    'pipeline': {'Cache': {}, 'DDragon': {}, 'RiotAPI': {'api_key': RIOT_KEY}},
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
    if (summoner.exists):
        return summoner
    return None
