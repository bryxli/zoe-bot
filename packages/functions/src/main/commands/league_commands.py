import logging

from dynamo import ZoeBotTable
from league import RiotAPI

from constants.env import AWS_REGION, RIOT_KEY, STAGE
from constants.league import *

db = ZoeBotTable(AWS_REGION, STAGE)
lol = RiotAPI(RIOT_KEY)
guild_id = ''

logger = logging.getLogger("function-main")
logger.setLevel(logging.ERROR)

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
    gameName = data["options"][0]["value"] 
    tagLine = data["options"][1]["value"]
    try:
        puuid = lol.get_puuid_by_riot_id(gameName, tagLine, db.get_guild(guild_id)['region']['S'])
    except:
        return INVALID_USERNAME
    db.add_user(guild_id, puuid)
    return ADDUSER_SUCCESS

def delete_user(data):
    if not db.guild_exists(guild_id):
        return GUILD_DOES_NOT_EXIST
    gameName = data["options"][0]["value"] 
    tagLine = data["options"][1]["value"]  
    try:
        puuid = lol.get_puuid_by_riot_id(gameName, tagLine, db.get_guild(guild_id)['region']['S'])
    except:
        return INVALID_USERNAME
    # TODO: db.user_exists and db.delete_user both call get_all_users, consolidate to avoid unecessary calls
    if not db.user_exists(guild_id, puuid):
        return PLAYER_DOES_NOT_EXIST
    db.delete_user(guild_id, puuid)
    return DELUSER_SUCCESS

def userlist():
    if not db.guild_exists(guild_id):
        return GUILD_DOES_NOT_EXIST
    accountlist = db.get_all_users(guild_id)
    users = []
    for puuid in accountlist:
        try:
            account_name = lol.get_name_by_puuid(puuid, db.get_guild(guild_id)['region']['S'])
            users.append(account_name)
        except Exception as e:
            logger.error(e)
    if len(users) == 0:
        return NO_USERS_IN_USERLIST
    return ' '.join(users)
