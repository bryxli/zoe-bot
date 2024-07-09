import logging

from constants.env import AWS_REGION, RIOT_KEY, STAGE
from constants.league import *

from commands.layer_import_helper import get_ZBT, get_RAPI

ZoeBotTable = get_ZBT()
RiotAPI = get_RAPI()

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
    if db.user_exists(guild_id, puuid):
        return PLAYER_EXISTS
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
