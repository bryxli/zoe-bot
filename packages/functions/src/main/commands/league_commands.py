from dynamo import ZoeBotTable
from league import RiotAPI

from constants.env import AWS_REGION, RIOT_KEY, STAGE
from constants.league import *

db = ZoeBotTable(AWS_REGION, STAGE)
lol = RiotAPI(RIOT_KEY)
guild_id = ''


def init(command, data):
    global guild_id

    guild_id = data['guild_id']

    if command == COMMAND_ADDUSER:
        output = add_user(data['data'])
    elif command == COMMAND_DELUSER:
        output = delete_user(data['data'])
    elif command == COMMAND_USERLIST:
        output = userlist()

    return output


def add_user(data):
    if not db.guild_exists(guild_id):
        return GUILD_DOES_NOT_EXIST
    arg = data["options"][0]["value"]   
    player = lol.find_player_by_name(arg, db.get_guild(guild_id)['region']['S'])
    if player is None:
        return INVALID_USERNAME
    if db.user_exists(guild_id, player.account_id):
        return PLAYER_EXISTS
    db.add_user(guild_id, player.account_id)
    return ADDUSER_SUCCESS


def delete_user(data):
    if not db.guild_exists(guild_id):
        return GUILD_DOES_NOT_EXIST
    arg = data["options"][0]["value"]   
    player = lol.find_player_by_name(arg, db.get_guild(guild_id)['region']['S'])
    if player is None:
        return INVALID_USERNAME
    # TODO: db.user_exists and db.delete_user both call get_all_users, consolidate to avoid unecessary calls
    if not db.user_exists(guild_id, player.account_id):
        return PLAYER_DOES_NOT_EXIST
    db.delete_user(guild_id, player.account_id)
    return DELUSER_SUCCESS


def userlist():
    if not db.guild_exists(guild_id):
        return GUILD_DOES_NOT_EXIST
    accountlist = db.get_all_users(guild_id)
    users = []
    for account in accountlist:
        users.append(lol.find_player_by_accountid(account, db.get_guild(guild_id)['region']['S']).name)
    if len(users) == 0:
        return NO_USERS_IN_USERLIST
    return ' '.join(users)
    