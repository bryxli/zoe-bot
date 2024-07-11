from ..auth import auth
from dynamo import ZoeBotTable

db = ZoeBotTable('us-east-1', 'dev')

def handler(event, context):
    if not auth(event['apiKey']):
        return {
            'statusCode': 401,
            'body': 'unauthorized'
        }

    guild = db.get_guild(event['guildId'])
    if not guild:
        return {
            'statusCode': 404,
            'body': 'guild not found'
        }

    return {
        'statusCode': 200,
        'body': guild
    }
