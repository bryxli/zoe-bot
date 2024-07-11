import json
import os
import requests # TODO: needs to be added to a requirements.txt for api, currently relies on layer for dependency

from ..auth import auth
from dynamo import ZoeBotTable

TOKEN = os.environ.get("TOKEN") # TODO: local build logic

db = ZoeBotTable('us-east-1', 'dev')

def handler(event, context):
    if not auth(event['apiKey']):
        return {
            'statusCode': 401,
            'body': 'unauthorized'
        }
    if db.guild_exists(event['guildId']):
        return {
            'statusCode': 409,
            'body': 'guild already exists'
        }

    headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}
    body = {
        'name': 'zœ',
    }
    create_webhook_url = f"https://discordapp.com/api/channels/{event['channelId']}/webhooks"
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

    db.create_guild(event['guildId'], webhook_id, webhook_url)

    return {
        'statusCode': 201
    }