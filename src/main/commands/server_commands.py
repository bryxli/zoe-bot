import json
import os
import requests

from dynamo import ZoeBotTable

AWS_REGION = os.environ.get("SET_AWS_REGION")
TOKEN = os.environ.get("TOKEN")

COMMAND_SETUP = 'setup'
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

db = ZoeBotTable(AWS_REGION)
guild_id = ''


def init(command, data):
    global guild_id

    guild_id = data['guild_id']

    if command == COMMAND_SETUP:
        output = init_guild(data)
    elif command == COMMAND_RESET:
        output = delete_guild()
    elif command == COMMAND_REGION:
        output = change_region(data['data'])

    return output


def init_guild(data):
    if db.guild_exists(guild_id):
        return GUILD_EXISTS
    
    channel_id = data["channel_id"]
    
    headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}
    body = {
        'name': 'zœ',
    }
    create_webhook_url = f"https://discordapp.com/api/channels/{channel_id}/webhooks"

    webhook = requests.post(create_webhook_url, headers=headers, data=json.dumps(body))
    arg = webhook.json()["url"]

    db.create_guild(guild_id, arg)
    return SETUP_SUCCESS


def delete_guild():
    if not db.guild_exists(guild_id):
        return GUILD_DOES_NOT_EXIST
    if not check_acknowledgment():
        return ACKNOWLEDGMENT_PROMPT
    db.destroy_guild(guild_id)
    return DELETE_SUCCESS


def change_region(data):
    if not db.guild_exists(guild_id):
        return GUILD_DOES_NOT_EXIST
    if not check_acknowledgment():
        return ACKNOWLEDGMENT_PROMPT
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


def check_acknowledgment():
    return db.check_acknowledgment(guild_id)
    