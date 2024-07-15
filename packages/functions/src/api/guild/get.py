import json

from ..util import get_common_guild_params, validate_params
from dynamo import ZoeBotTable

db = ZoeBotTable('us-east-1', 'dev')

def handler(event, context):
    params, missing_params = get_common_guild_params(event)

    validation_response = validate_params(params, missing_params)
    if validation_response:
        return validation_response
    
    guild = db.get_guild(params['guildId'])

    return {
        'statusCode': 200,
        'body': json.dumps(guild)
    }
