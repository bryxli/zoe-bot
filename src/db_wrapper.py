import boto3

client = boto3.client('dynamodb')
table_name = 'zoe_db'

def get_all():
    return client.scan(TableName=table_name)

def guild_exists(guild_id):
    response = client.get_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}}
    )
    return 'Item' in response

def create_guild(guild_id, channel_id):
    item = {
        'guild_id': {'N': guild_id},
        'channel_id': {'N': channel_id},
        'region': {'S': 'NA'},
        'userlist': {'L': []},
    }
    response = client.put_item(
        TableName=table_name,
        Item=item
    )
    return response

def destroy_guild(guild_id):
    response = client.delete_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}}
    )
    return response

def update_guild(guild_id, updates): # adds/updates any attribute in respective item
    response = client.update_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}},
        AttributeUpdates = updates
    )
    return response

def get_all_users(guild_id):
    response = client.get_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}}
    )['Item']['userlist']['L'] # [{'S',account_id},{'S',account_id}...,]
    userlist = []
    for user in response:
        userlist.append(user['S'])
    return userlist


def user_exists(guild_id, account_id):
    users = get_all_users(guild_id)
    return account_id in users

def add_user(guild_id, account_id):
    expression_values = {
        ':user':{'L':[{'S':account_id}]}
    }
    response = client.update_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}},
        UpdateExpression = 'SET userlist = list_append(userlist, :user)',
        ExpressionAttributeValues = expression_values
    )
    return response

def delete_user(guild_id, account_id):
    userlist = get_all_users(guild_id)
    index = userlist.index(account_id)
    response = client.update_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}},

        UpdateExpression = f'REMOVE userlist[{index}]',
    )
    return response

# create_guild('test_gid','test_cid')

# updates = {
#     'new_attribute': {'Value': {'S': 'test'}, 'Action': 'PUT'}, 
# }
# update_guild('test_gid', updates)

print(get_all())
# detroy_guild('test_gid')