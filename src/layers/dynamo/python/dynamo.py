import boto3
import os

REGION = os.environ.get("SET_AWS_REGION") # TODO: pass in REGION from lambda function, layer not able to access

client = boto3.client('dynamodb', region_name=REGION)
table_name = 'ZoeBotTable'


def get_all():
    return client.scan(TableName=table_name)


def guild_exists(guild_id):
    response = client.get_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}}
    )
    return 'Item' in response


def get_guild(guild_id):
    response = client.get_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}}
    )
    return response['Item']


def create_guild(guild_id, webhook_url):
    item = {
        'guild_id': {'N': guild_id},
        'webhook_url': {'S': webhook_url},
        'region': {'S': 'NA'},
        'userlist': {'L': []},
    }
    client.put_item(
        TableName=table_name,
        Item=item
    )


def destroy_guild(guild_id):
    client.delete_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}}
    )


def update_guild(guild_id, updates):  # adds/updates any attribute in respective item
    client.update_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}},
        AttributeUpdates=updates
    )


def get_all_users(guild_id):
    response = client.get_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}}
    )['Item']['userlist']['L']
    userlist = []
    for user in response:
        account_id = list(user['M'].keys())
        userlist.extend(account_id)
    return userlist


def user_exists(guild_id, account_id):
    users = get_all_users(guild_id)
    return account_id in users


def add_user(guild_id, account_id, last_created=''):
    expression_values = {
        ':user': {'L': [{'M': {account_id: {'S': last_created}}}]}
    }
    client.update_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}},
        UpdateExpression='SET userlist = list_append(userlist, :user)',
        ExpressionAttributeValues=expression_values
    )


def delete_user(guild_id, account_id):
    userlist = get_all_users(guild_id)
    index = userlist.index(account_id)
    client.update_item(
        TableName=table_name,
        Key={'guild_id': {'N': guild_id}},
        UpdateExpression=f'REMOVE userlist[{index}]',
    )


def update_user(guild_id, account_id, last_created):
    delete_user(guild_id, account_id)
    add_user(guild_id, account_id, last_created)
    