from dynamo import ZoeBotTable

db = ZoeBotTable('us-east-1', 'dev')

def get_guild(event, context):
    guild = db.get_guild(event['guildId'])
    if not guild:
        return {
            'statusCode': 404,
            'body': 'Guild not found'
        }
    return {
        'statusCode': 200,
        'body': guild
    }

def setup_guild(event, context): # guild_id, webhook_id, webhook_url
    print('api/guild.setup')

def change_region(event, context): # guild_id, updates
    print('api/guild.change_region')

def delete_guild(event, context): # guild_id
    print('api/guild.delete_guild')

def acknowledge(event, context): # guild_id, updates
    print('api/guild.acknowledge')
