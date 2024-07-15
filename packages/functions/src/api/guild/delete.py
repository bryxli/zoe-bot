import os
import requests

from ..util import get_common_guild_params, validate_params
from dynamo import ZoeBotTable

TOKEN = os.environ.get("TOKEN") # TODO: local build logic

db = ZoeBotTable('us-east-1', 'dev')

def handler(event, context):
    params, missing_params = get_common_guild_params(event)

    validation_response = validate_params(params, missing_params)
    if validation_response:
        return validation_response
    
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
