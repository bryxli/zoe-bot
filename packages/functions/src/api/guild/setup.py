import json
import requests

from src.api.common import auth, AWS_REGION, STAGE, TOKEN
from dynamo import ZoeBotTable

db = ZoeBotTable(AWS_REGION, STAGE)

def handler(event, context):
    params = json.loads(event)['body']
    missing_params = [param for param in ['apiKey', 'guildId', 'channelId'] if param not in params]

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
    if db.guild_exists(params['guildId']):
        return {
            'statusCode': 409,
            'body': 'guild already exists'
        }

    headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}
    body = {
        'name': 'zœ',
    }
    create_webhook_url = f"https://discordapp.com/api/channels/{params['channelId']}/webhooks"
    webhook_id = ''
    webhook_url = ''

    try:
        webhook = requests.post(create_webhook_url, headers=headers, data=json.dumps(body))
        webhook_id = webhook.json()["id"]
        webhook_url = webhook.json()["url"]
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'error creating webhook: {e}'
        }

    db.create_guild(params['guildId'], webhook_id, webhook_url)

    return {
        'statusCode': 201
    }
