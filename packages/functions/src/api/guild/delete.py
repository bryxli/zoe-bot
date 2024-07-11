import json
import os
import requests

from ..auth import auth
from dynamo import ZoeBotTable

TOKEN = os.environ.get("TOKEN") # TODO: local build logic

db = ZoeBotTable('us-east-1', 'dev')

def handler(event, context):
    params = json.loads(event['body'])
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

    webhook_id = db.get_webhook(params['guildId'])
    headers = {"Authorization": f"Bot {TOKEN}"}
    delete_webhook_url = f"https://discordapp.com/api/webhooks/{webhook_id}"

    try:
        requests.delete(delete_webhook_url, headers=headers)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'error deleting webhook: {e}'
        }

    db.destroy_guild(params['guildId'])

    return {
        'statusCode': 200
    }
