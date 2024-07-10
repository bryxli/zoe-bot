from behave import *

from util.guild_util import GuildUtil
client = GuildUtil()

@given('guild has not been initialized')
def step_guild_not_init(context):
    client.delete_guild()

@given('guild has been initialized')
def step_guild_init(context):
    client.create_guild()

@given('guild has been acknowledged')
def step_guild_acknowledged(context):
    client.acknowledge()
