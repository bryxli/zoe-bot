import logging
import json
from behave import *

from util.bot_util import BotUtil

client = BotUtil()
logging.basicConfig(level=logging.INFO)

GUILD_ID = '1'

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
    res = client.send_command(raw_request)
    data = json.loads(res)
    context.response = data['data']['content']

@when('reset')
def step_reset(context):
    raw_request = {
        'type': 0,
        'data': {
            'name': 'reset'
        },
        'guild_id': GUILD_ID
    }
    res = client.send_command(raw_request)
    data = json.loads(res)
    context.response = data['data']['content']

@when('region {region}')
def step_region(context, region):
    raw_request = {
        'type': 0,
        'data': {
            'name': 'region',
            'options': [{ 'value': region }]
        },
        'guild_id': GUILD_ID
    }
    res = client.send_command(raw_request)
    data = json.loads(res)
    context.response = data['data']['content']

@when('acknowledge')
def step_acknowledge(context):
    raw_request = {
        'type': 0,
        'data': {
            'name': 'acknowledge'
        },
        'guild_id': GUILD_ID
    }
    res = client.send_command(raw_request)
    data = json.loads(res)
    context.response = data['data']['content']

@when('adduser {gameName}:{tag}')
def step_adduser(context, gameName, tag):
    context.response = ''

@when('deluser {gameName}:{tag}')
def step_deluser(context, gameName, tag):
    context.response = ''

@when('userlist')
def step_userlist(context):
    context.response = ''

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
