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