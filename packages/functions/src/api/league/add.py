from dynamo import ZoeBotTable
from ..util import get_common_league_params, validate_params, get_puuid

db = ZoeBotTable('us-east-1', 'dev')

def handler(event, context):
    params, missing_params = get_common_league_params(event)
    validation_response = validate_params(params, missing_params)
    if validation_response:
        return validation_response
    
    gameName = params['gameName']
    tagLine = params['tagLine']
    guild_id = params['guildId']

    puuid = get_puuid(gameName, tagLine, guild_id)
    if not puuid:
        return {
            'statusCode': 400,
            'body': 'invalid username'
        }

    if db.user_exists(guild_id, puuid):
        return {
            'statusCode': 409,
            'body': 'user already exists'
        }
    
    db.add_user(guild_id, puuid)

    return {
        'statusCode': 200
    }
