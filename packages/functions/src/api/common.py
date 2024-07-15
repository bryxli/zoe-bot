import json
import os

from dynamo import ZoeBotTable
from league import RiotAPI

if os.environ.get("API_KEY") is None:
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../configs/config.json'))
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    API_KEY = config.get("api_key")
    RIOT_KEY = config.get("riot_key")
    AWS_REGION = config.get("aws_region")
    TOKEN = config.get("token")
    STAGE = "dev"
else:
    API_KEY = os.environ.get("API_KEY")
    RIOT_KEY = os.environ.get("RIOT_KEY")
    AWS_REGION = os.environ.get("SET_AWS_REGION")
    TOKEN = os.environ.get("TOKEN")
    if os.environ.get("STAGE") == None:
        STAGE = "dev"
    else:
        STAGE = os.environ.get("STAGE")

db = ZoeBotTable(AWS_REGION, STAGE)
lol = RiotAPI(RIOT_KEY)

def auth(key):
    return key == API_KEY

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