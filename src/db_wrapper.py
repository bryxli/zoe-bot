import boto3

client = boto3.client('dynamodb')
table_name = 'zoe_db'

def get_all():
    return client.scan(TableName=table_name)

def create_guild(guild_id, channel_id):
    item = {
        'guild_id': {'S': guild_id},
        'channel_id': {'S': channel_id},
        'region': {'S': 'NA'},
    }
    response = client.put_item(
        TableName=table_name,
        Item=item
    )
    return response

def delete_guild(guild_id):
    response = client.delete_item(
        TableName=table_name,
        Key={'guild_id': {'S': guild_id}}
    )
    return response

updates = {
    'new_attribute': {'Value': {'S': 'test'}, 'Action': 'PUT'}, 
}

def update_guild(guild_id, updates):
    response = client.update_item(
        TableName=table_name,
        Key={'guild_id': {'S': guild_id}},
        AttributeUpdates = updates
    )
    return response

# create_guild('test_gid','test_cid')
# update_guild('test_gid', updates)
# print(get_all())
# delete_guild('test_gid')