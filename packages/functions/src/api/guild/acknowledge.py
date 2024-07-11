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

    updates = {
        'acknowledgment' : {'Value': {'BOOL': True}, 'Action': 'PUT'}
    }

    db.update_guild(event['guildId'], updates)

    return {
        'statusCode': 200
    }
