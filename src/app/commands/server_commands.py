import wrappers.dynamo as db

COMMAND_SUCCESS = 'setup'
COMMAND_RESET = 'reset'
COMMAND_REGION = 'region'

SETUP_SUCCESS = 'guild initialized'
DELETE_SUCCESS = 'guild deleted'
REGION_SUCCESS = 'guild region changed'

GUILD_EXISTS = 'guild aready exists'
GUILD_DOES_NOT_EXIST = 'guild not registered'
REGION_DOES_NOT_EXIST = 'region not found'

REGION_LIST = ['BR', 'EUNE', 'EUW', 'JP', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'TR', 'RU']
ACKNOWLEDGMENT_PROMPT = 'this action can be harmful, running /reset or /region <region> will delete all registered users. acknowledge with /acknowledge'

guild_id = ''
channel_id = ''


def init(command, data):
    global guild_id, channel_id

    guild_id = data['guild_id']
    channel_id = data['channel_id']

    if command == COMMAND_SUCCESS:
        output = init_guild()
    elif command == COMMAND_RESET:
        output = delete_guild()
    elif command == COMMAND_REGION:
        output = change_region(data['data'])

    return output


def init_guild():
    if db.guild_exists(guild_id):
        return GUILD_EXISTS
    db.create_guild(guild_id, channel_id)
    return SETUP_SUCCESS


def delete_guild():
    if not check_acknowledgment():
        return ACKNOWLEDGMENT_PROMPT
    if not db.guild_exists(guild_id):
        return GUILD_DOES_NOT_EXIST
    db.destroy_guild(guild_id)
    return DELETE_SUCCESS


def change_region(data):
    if not check_acknowledgment():
        return ACKNOWLEDGMENT_PROMPT
    if not db.guild_exists(guild_id):
        return GUILD_DOES_NOT_EXIST
    try:
        arg = data["options"][0]["value"]   
    except KeyError:
        return ' '.join(REGION_LIST)
    current_region = arg.upper()
    if current_region not in REGION_LIST:
        return REGION_DOES_NOT_EXIST
    updates = {
        'region': {'Value': {'S': current_region}, 'Action': 'PUT'},
        'userlist': {'Value': {'L': []}, 'Action': 'PUT'},
    }
    db.update_guild(guild_id, updates)
    return REGION_SUCCESS


# TODO: before running delete_guild() and change_region(), check that user has aknowledged potential harm that those commands can cause
#       will involve creating a new function in dynamo.py, changing structure of the table, and creating a new slash command to acknowledge
def check_acknowledgment():
    return True
    