import json
import os
import platform
import sqlite3
import sys

from contextlib import closing

import discord
from discord.ext import tasks, commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from riotwatcher import LolWatcher, ApiError

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents.default()

bot = Bot(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents, help_command=None)
lol_watcher = LolWatcher(config["league_token"])
my_region = "na1"

def init_db():
    with closing(connect_db()) as db:
        with open("database/schema.sql", "r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect("database/database.db")

bot.config = config
bot.db = connect_db()

@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()

@tasks.loop(seconds=10)
async def status_task() -> None:
    # print('do riot stuff here')
    pass

@bot.command()
async def adduser(ctx, arg):
    user_id = arg
    try:
        cursor = bot.db.cursor()
        sqlite_insert_query = "INSERT INTO userlist (user_id) VALUES ('" + user_id + "')"
        cursor.execute(sqlite_insert_query)
        bot.db.commit()
        cursor.close()
        await ctx.send("Successfully inserted " + user_id + " into userlist.")
        print(("Successfully inserted " + user_id + " into userlist."))
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table.", error)

@bot.command()
async def deluser(ctx, arg):
    user_id = arg
    try:
        cursor = bot.db.cursor()
        sqlite_insert_query = "DELETE FROM userlist WHERE user_id = '" + user_id + "'"
        cursor.execute(sqlite_insert_query)
        bot.db.commit()
        cursor.close()
        await ctx.send("Successfully deleted " + user_id + " from userlist.")
        print(("Successfully inserted " + user_id + " into userlist."))
    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table.", error)        

@bot.event
async def on_command_completion(context: Context) -> None:
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        print(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
    else:
        print(f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")

@bot.event
async def on_command_error(context: Context, error) -> None:
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error

init_db()
bot.run(config["token"])