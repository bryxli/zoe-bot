import json
import random

import disnake
from disnake.ext import commands

from commands.help_command import HelpCommand
from commands.server_commands import Server
from commands.league_commands import League

with open('config.json') as file:
    config = json.load(file)

with open("template.json") as file:
    template = json.load(file)

client = commands.InteractionBot(test_guilds=[1016953904644247632])

client.add_cog(Server(client))
client.add_cog(League(client))

@client.event
async def on_ready() -> None:
    print('client loaded')

@client.slash_command(description='zoe will talk to you')
async def speak(ctx):
    response = template['response']
    await ctx.send(random.choice(response))

client.run(config['token'])
