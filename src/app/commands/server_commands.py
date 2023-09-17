import wrappers.dynamo as db

REGION_LIST = ['BR', 'EUNE', 'EUW', 'JP', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'TR', 'RU']

guild_id = ''
channel_id = ''


def init(command, data):
    global guild_id, channel_id

    guild_id = data['guild_id']
    channel_id = data['channel_id']

    if command == 'setup':
        output = init_guild()
    elif command == 'reset':
        output = delete_guild()
    elif command == 'region':
        output = change_region(data['data'])

    return output


def init_guild():
    if db.guild_exists(guild_id):
        return 'guild aready exists'
    db.create_guild(guild_id, channel_id)
    return f'guild initialized'


def delete_guild():
    if not check_acknowledgment():
        return 'this action can be harmful, running /reset or /region <region> will delete all registered users. acknowledge with /acknowledge'
    if not db.guild_exists(guild_id):
        return 'guild not registered'
    db.destroy_guild(guild_id)
    return 'guild deleted'


def change_region(data):
    if not check_acknowledgment():
        return 'this action can be harmful, running /reset or /region <region> will delete all registered users. acknowledge with /acknowledge'
    if not db.guild_exists(guild_id):
        return 'guild has not been setup'
    try:
        arg = data["options"][0]["value"]   
    except KeyError:
        return REGION_LIST
    current_region = arg.upper()
    if current_region not in REGION_LIST:
        return 'region not found'
    updates = {
        'region': {'Value': {'S': current_region}, 'Action': 'PUT'},
        'userlist': {'Value': {'L': []}, 'Action': 'PUT'},
    }
    db.update_guild(guild_id, updates)
    return 'guild region changed'


# TODO: before running delete_guild() and change_region(), check that user has aknowledged potential harm that those commands can cause
#       will involve creating a new function in dynamo.py, changing structure of the table, and creating a new slash command to acknowledge
def check_acknowledgment():
    return True
    