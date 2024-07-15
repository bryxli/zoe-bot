from ..common import get_common_guild_params, validate_params, AWS_REGION, STAGE
from dynamo import ZoeBotTable

db = ZoeBotTable(AWS_REGION, STAGE)

def handler(event, context):
    params, missing_params = get_common_guild_params(event)

    validation_response = validate_params(params, missing_params)
    if validation_response:
        return validation_response

    updates = {
        'acknowledgment' : {'Value': {'BOOL': True}, 'Action': 'PUT'}
    }

    db.update_guild(params['guildId'], updates)

    return {
        'statusCode': 200
    }
