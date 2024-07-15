import json
import os

from ..util import get_common_guild_params, validate_params
from dynamo import ZoeBotTable
from league import RiotAPI

RIOT_KEY = os.environ.get("RIOT_KEY") # TODO: local build logic

db = ZoeBotTable('us-east-1', 'dev')
lol = RiotAPI(RIOT_KEY)

def handler(event, context):
    params, missing_params = get_common_guild_params(event)

    validation_response = validate_params(params, missing_params)
    if validation_response:
        return validation_response

    accountlist = db.get_all_users(params['guildId'])
    users = []
    for puuid in accountlist:
        try:
            account_name = lol.get_name_by_puuid(puuid, db.get_guild(params['guildId'])['region']['S'])
            users.append(account_name)
        except Exception as e:
            return {
                'statusCode': 400,
                'body': f'failed to retrieve summoner name: {e}'
            }

    return {
        'statusCode': 200,
        'body': json.dumps(users)
    }
