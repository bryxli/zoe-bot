import json

from src.api.common import auth, AWS_REGION, STAGE
from dynamo import ZoeBotTable

db = ZoeBotTable(AWS_REGION, STAGE)

def handler(event, context):
    params = json.loads(event)['body']
    missing_params = [param for param in ['apiKey', 'guildId', 'leagueRegion'] if param not in params]

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
    if not db.check_acknowledgment(params['guildId']):
        return {
            'statusCode': 403,
            'body': 'not acknowledged'
        }
    
    REGION_LIST = ['BR', 'EUNE', 'EUW', 'JP', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'TR', 'RU', 'PH', 'SG', 'TH', 'TW', 'VN']
    region = params['leagueRegion'].upper()

    if region not in REGION_LIST:
        return {
            'statusCode': 400,
            'body': 'invalid region'
        }
    updates = {
        'region': {'Value': {'S': region}, 'Action': 'PUT'},
        'userlist': {'Value': {'L': []}, 'Action': 'PUT'},
    }

    db.update_guild(params['guildId'], updates)

    return {
        'statusCode': 200
    }
