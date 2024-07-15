import json

from ..auth import auth
from dynamo import ZoeBotTable

db = ZoeBotTable('us-east-1', 'dev')

def handler(event, context):
    params = json.loads(event['body'])
    missing_params = [param for param in ['apiKey', 'guildId'] if param not in params]

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

    guild = db.get_guild(params['guildId'])
    print(guild)
    print(type(guild))
    print(str(guild))
    if not guild:
        return {
            'statusCode': 404,
            'body': 'guild not found'
        }

    return {
        'statusCode': 200,
        'body': json.dumps(guild)
    }
