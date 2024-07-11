from ..auth import auth
from dynamo import ZoeBotTable

db = ZoeBotTable('us-east-1', 'dev')

def handler(event, context):
    if not auth(event['apiKey']):
        return {
            'statusCode': 401,
            'body': 'unauthorized'
        }
    if not db.guild_exists(event['guildId']):
        return {
            'statusCode': 404,
            'body': 'guild not found'
        }
    if not db.check_acknowledgment(event['guildId']):
        return {
            'statusCode': 403,
            'body': 'not acknowledged'
        }
    
    REGION_LIST = ['BR', 'EUNE', 'EUW', 'JP', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'TR', 'RU', 'PH', 'SG', 'TH', 'TW', 'VN']
    region = event['leagueRegion'].upper()

    if region not in REGION_LIST:
        return {
            'statusCode': 400,
            'body': 'invalid region'
        }
    updates = {
        'region': {'Value': {'S': region}, 'Action': 'PUT'},
        'userlist': {'Value': {'L': []}, 'Action': 'PUT'},
    }

    db.update_guild(event['guildId'], updates)

    return {
        'statusCode': 200
    }