import json
import os

from ..auth import auth
from dynamo import ZoeBotTable
from league import RiotAPI

RIOT_KEY = os.environ.get("RIOT_KEY") # TODO: local build logic

db = ZoeBotTable('us-east-1', 'dev')
lol = RiotAPI(RIOT_KEY)

def handler(event, context):
    params = json.loads(event['body'])
    missing_params = [param for param in ['apiKey', 'guildId', 'gameName', 'tagLine'] if param not in params]

    if missing_params:
        return {
            'statusCode': 400,
            'body': f'missing parameters: {", ".join(missing_params)}'
        }
    if 'apiKey' not in params or not auth(params['apiKey']):
        return {
            'statusCode': 401,
            'body': 'unauthorized'
        }
    if not db.guild_exists(params['guildId']):
        return {
            'statusCode': 404,
            'body': 'guild not found'
        }

    gameName = params['gameName']
    tagLine = params['tagLine']

    try:
        puuid = lol.get_puuid_by_riot_id(gameName, tagLine, db.get_guild(params['guildId'])['region']['S'])
    except:
        return {
            'statusCode': 400,
            'body': 'invalid username'
        }

    if db.user_exists(params['guildId'], puuid):
        return {
            'statusCode': 409,
            'body': 'user already exists'
        }
    
    db.add_user(params['guildId'], puuid)

    return {
        'statusCode': 200
    }
