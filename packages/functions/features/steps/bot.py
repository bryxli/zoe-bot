import logging
import json
from behave import *

from util.bot_util import BotUtil

client = BotUtil()
logging.basicConfig(level=logging.INFO)

GUILD_ID = '1'

def request(context, raw_request):
    res = client.send_command(raw_request)
    data = json.loads(res)
    context.response = data['data']['content']
    logging.info(f"Bot returned: {context.response}")

@then('bot sends {output}')
def step_bot_return(context, output):
    assert(context.response == output)

@when('setup')
def step_setup(context):
    raw_request = {
        'type': 0,
        'data': {
            'name': 'setup'
        },
        'guild_id': GUILD_ID,
        'channel_id': 1
    }
    request(context, raw_request)

@when('reset')
def step_reset(context):
    raw_request = {
        'type': 0,
        'data': {
            'name': 'reset'
        },
        'guild_id': GUILD_ID
    }
    request(context, raw_request)

@when('region {region}')
def step_region(context, region):
    opts = { 'value': region } if region != '""' else {}

    raw_request = {
        'type': 0,
        'data': {
            'name': 'region',
            'options': [opts]
        },
        'guild_id': GUILD_ID
    }
    request(context, raw_request)

@when('acknowledge')
def step_acknowledge(context):
    raw_request = {
        'type': 0,
        'data': {
            'name': 'acknowledge'
        },
        'guild_id': GUILD_ID
    }
    request(context, raw_request)

@when('adduser {gameName}:{tag}')
def step_adduser(context, gameName, tag):
    raw_request = {
        'type': 0,
        'data': {
            'name': 'adduser',
            'options': [
                { 'value': gameName },
                { 'value': tag }
            ]
        },
        'guild_id': GUILD_ID
    }
    request(context, raw_request)

@when('deluser {gameName}:{tag}')
def step_deluser(context, gameName, tag):
    raw_request = {
        'type': 0,
        'data': {
            'name': 'deluser',
            'options': [
                { 'value': gameName },
                { 'value': tag }
            ]
        },
        'guild_id': GUILD_ID
    }
    request(context, raw_request)

@when('userlist')
def step_userlist(context):
    raw_request = {
        'type': 0,
        'data': { 'name': 'userlist' },
        'guild_id': GUILD_ID
    }
    request(context, raw_request)

@when('help')
def step_help(context):
    raw_request = {
        'type': 0,
        'data': { 'name': 'help' }
    }
    res = client.send_command(raw_request)
    context.response = res

@when('speak')
def step_speak(context):
    raw_request = {
        'type': 0,
        'data': { 'name': 'speak' }
    }
    res = client.send_command(raw_request)
    context.response = res

@given('a set of added players')
def step_add_player_set(context):
    for row in context.table:
        step_adduser(context, row['gameName'], row['tag'])
