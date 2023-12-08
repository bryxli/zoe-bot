import json
import requests

from dynamo import ZoeBotTable

from constants.env import AWS_REGION, TOKEN, STAGE
from constants.server import *

db = ZoeBotTable(AWS_REGION, STAGE)
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
    elif command == COMMAND_ACKNOWLEDGE:
        output = acknowledge()

    return output


def init_guild(data):
    print('test command runs')
    if db.guild_exists(guild_id):
        return GUILD_EXISTS
    
    channel_id = data["channel_id"]
    
    headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}
    body = {
        'name': 'zœ',
    }
    create_webhook_url = f"https://discordapp.com/api/channels/{channel_id}/webhooks"

    webhook = requests.post(create_webhook_url, headers=headers, data=json.dumps(body))
    webhook_id = webhook.json()["id"]
    webhook_url = webhook.json()["url"]

    db.create_guild(guild_id, webhook_id, webhook_url)
    return SETUP_SUCCESS


def delete_guild():
    if not db.guild_exists(guild_id):
        return GUILD_DOES_NOT_EXIST
    if not db.check_acknowledgment(guild_id):
        return ACKNOWLEDGMENT_PROMPT

    webhook_id = db.get_webhook(guild_id)

    headers = {"Authorization": f"Bot {TOKEN}"}
    delete_webhook_url = f"https://discordapp.com/api/webhooks/{webhook_id}"

    db.destroy_guild(guild_id)
    requests.delete(delete_webhook_url, headers=headers)

    return DELETE_SUCCESS


def change_region(data):
    if not db.guild_exists(guild_id):
        return GUILD_DOES_NOT_EXIST
    if not db.check_acknowledgment(guild_id):
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

def acknowledge():
    updates = {
        'acknowledgment' : {'Value': {'BOOL': True}, 'Action': 'PUT'}
    }
    db.update_guild(guild_id, updates)
    return ACKNOWLEDGE_SUCCESS