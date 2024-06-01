import boto3

class ZoeBotTable:
    def __init__(self, region, stage):
        self.region = region
        self.client = boto3.client('dynamodb', region_name=self.region)
        self.table_name = f'{stage}-zoe-bot-db'

    def get_all(self):
        return self.client.scan(TableName=self.table_name)

    def guild_exists(self, guild_id):
        response = []
        try:
            response = self.client.get_item(
                TableName=self.table_name,
                Key={'guild_id': {'N': guild_id}}
            )
        except Exception as e:
            import logging
            logging.basicConfig(level=logging.WARNING)
            logging.warning(f"guild_exists exception: {e}")
            pass
        return 'Item' in response

    def get_guild(self, guild_id):
        response = self.client.get_item(
            TableName=self.table_name,
            Key={'guild_id': {'N': guild_id}}
        )
        return response.get('Item', {})

    def create_guild(self, guild_id, webhook_id, webhook_url):
        item = {
            'guild_id': {'N': guild_id},
            'webhook_id': {'S': webhook_id},
            'webhook_url': {'S': webhook_url},
            'region': {'S': 'NA'},
            'userlist': {'L': []},
            'acknowledgment' : {'BOOL': False}
        }
        self.client.put_item(
            TableName=self.table_name,
            Item=item
        )
        return True

    def destroy_guild(self, guild_id):
        self.client.delete_item(
            TableName=self.table_name,
            Key={'guild_id': {'N': guild_id}}
        )
        return True

    def update_guild(self, guild_id, updates):  
        self.client.update_item(
            TableName=self.table_name,
            Key={'guild_id': {'N': guild_id}},
            AttributeUpdates=updates
        )
        return True

    def get_all_users(self, guild_id):
        response = self.client.get_item(
            TableName=self.table_name,
            Key={'guild_id': {'N': guild_id}}
        ).get('Item', {}).get('userlist', {}).get('L', [])
        userlist = []
        for user in response:
            puuid = list(user.get('M', {}).keys())
            userlist.extend(puuid)
        return userlist

    def user_exists(self, guild_id, puuid):
        users = self.get_all_users(guild_id)
        return puuid in users

    def add_user(self, guild_id, puuid, gameId=''):
        expression_values = {
            ':user': {'L': [{'M': {puuid: {'S': gameId}}}]}
        }
        self.client.update_item(
            TableName=self.table_name,
            Key={'guild_id': {'N': guild_id}},
            UpdateExpression='SET userlist = list_append(userlist, :user)',
            ExpressionAttributeValues=expression_values
        )
        return True

    def delete_user(self, guild_id, puuid): # TODO: rather than using index, remove by querying the puuid key
        userlist = self.get_all_users(guild_id)
        index = userlist.index(puuid)
        self.client.update_item(
            TableName=self.table_name,
            Key={'guild_id': {'N': guild_id}},
            UpdateExpression=f'REMOVE userlist[{index}]',
        )
        return True

    def update_user(self, guild_id, puuid, gameId):
        self.delete_user(guild_id, puuid)
        self.add_user(guild_id, puuid, gameId)
        return True

    def check_acknowledgment(self, guild_id):
        return self.get_guild(guild_id)['acknowledgment']['BOOL']
    
    def get_webhook(self, guild_id):
        return self.get_guild(guild_id)['webhook_id']['S']
