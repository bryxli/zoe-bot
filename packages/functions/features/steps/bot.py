from behave import *

from util.bot_util import BotUtil
client = BotUtil()

GUILD_ID = '1'

@then('bot sends {output}')
def step_bot_return(context, output):
    assert(context.response == output)

@when('setup') # TODO: webhook creation returns {'message': '401: Unauthorized', 'code': 0}
def step_setup(context):
    raw_request = {
        'type': 0,
        'data': {
            'name': 'setup'
        },
        'guild_id': GUILD_ID,
        'channel_id': 1016953904644247632
    }
    res = client.send_command(raw_request)
    context.response = res

@when('reset')
def step_reset(context):
    context.response = ''

@when('region {region}')
def step_region(context, region):
    context.response = ''

@when('acknowledge')
def step_acknowledge(context):
    context.response = ''

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
