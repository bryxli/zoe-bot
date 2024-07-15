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
    if not db.guild_exists(params['guildId']):
        return {
            'statusCode': 404,
            'body': 'guild not found'
        }

    updates = {
        'acknowledgment' : {'Value': {'BOOL': True}, 'Action': 'PUT'}
    }

    db.update_guild(params['guildId'], updates)

    return {
        'statusCode': 200
    }
