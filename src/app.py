import json

import discord
from discord.ext import commands
from discord.ext.commands import Bot

with open('config.json') as file:
    config = json.load(file)

intents = discord.Intents.all()
bot = Bot(command_prefix=commands.when_mentioned_or(config['prefix']), intents=intents, help_command=None)
bot.config = config

@bot.event
async def on_ready() -> None:
    await bot.change_presence(activity=discord.Game("#help"))

@bot.command()
async def help(ctx):
    await ctx.send('help')

bot.run(config['token'])