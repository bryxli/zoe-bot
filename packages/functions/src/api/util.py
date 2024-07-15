import json
import os

from .auth import auth
from dynamo import ZoeBotTable
from league import RiotAPI

RIOT_KEY = os.environ.get("RIOT_KEY")  # TODO: local build logic

db = ZoeBotTable('us-east-1', 'dev')
lol = RiotAPI(RIOT_KEY)

def get_common_params(event, required):
    params = json.loads(event['body'])
    missing_params = [param for param in required if param not in params]
    return params, missing_params

def get_common_league_params(event):
    return get_common_params(event, ['apiKey', 'guildId', 'gameName', 'tagLine'])

def get_common_guild_params(event):
    return get_common_params(event, ['apiKey', 'guildId'])

def validate_params(params, missing_params):
    if missing_params:
        return {
            'statusCode': 400,
            'body': f'missing parameters: {", ".join(missing_params)}'
        }
    if not auth(params['apiKey']):
        return {
            'statusCode': 401,
            'body': 'unauthorized'
        }
    if not db.guild_exists(params['guildId']):
        return {
            'statusCode': 404,
            'body': 'guild not found'
        }
    return None

def get_puuid(gameName, tagLine, guild_id):
    try:
        puuid = lol.get_puuid_by_riot_id(gameName, tagLine, db.get_guild(guild_id)['region']['S'])
    except:
        return None
    return puuid
