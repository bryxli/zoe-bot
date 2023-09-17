import wrappers.league as lol
import wrappers.dynamo as db

guild_id = ''


def init(command, data):
    global guild_id

    guild_id = data['guild_id']

    if command == 'adduser':
        output = add_user(data['data'])
    elif command == 'deluser':
        output = delete_user(data['data'])
    elif command == 'userlist':
        output = userlist()

    return output


def add_user(data):
    if not db.guild_exists(guild_id):
        return 'guild has not been setup'
    arg = data["options"][0]["value"]   
    player = lol.find_player_by_name(arg, db.get_guild(guild_id)['region']['S'])
    if player is None:
        return 'please enter a valid username'
    if db.user_exists(guild_id, player.account_id):
        return 'user already exists'
    db.add_user(guild_id, player.account_id)
    return 'user successfully added to guild'


def delete_user(data):
    if not db.guild_exists(guild_id):
        return 'guild has not been setup'
    arg = data["options"][0]["value"]   
    player = lol.find_player_by_name(arg, db.get_guild(guild_id)['region']['S'])
    if player is None:
        return 'please enter a valid username'
    # TODO: db.user_exists and db.delete_user both call get_all_users, consolidate to avoid unecessary calls
    if not db.user_exists(guild_id, player.account_id):
        return 'user does not exist'
    db.delete_user(guild_id, player.account_id)
    return 'user successfully deleted from guild'


def userlist():
    if not db.guild_exists(guild_id):
        return 'guild has not been setup'
    accountlist = db.get_all_users(guild_id)
    users = []
    for account in accountlist:
        users.append(lol.find_player_by_accountid(account, db.get_guild(guild_id)['region']['S']).name)
    if len(users) == 0:
        return 'no users have been added'
    return ' '.join(users)
    