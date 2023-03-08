import json

import cassiopeia as cass

with open('config.json') as file:
    config = json.load(file)

cass.set_riot_api_key(config['riot_key'])

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

def find_most_recent_match(summoner):
    match_history = summoner.match_history
    if (match_history.count > 0):
        return match_history[0]
    return None

def find_participant_id(summoner, match):
    for participant in match.participants:
        if participant.summoner == summoner:
            return participant.id

me = find_player_by_name('bryxli', 'NA')