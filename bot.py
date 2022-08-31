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
        with open("database/createServer.sql", "r") as f:
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
    try:
        cursor = bot.db.cursor()
        cursor.execute("SELECT * FROM serverlist")
        serverlist = cursor.fetchall()
        for server in serverlist:
            guild = bot.get_guild(int(server[0]))
            channel = guild.get_channel(int(server[1]))
            cursor.execute("SELECT * FROM '" + server[0] + "'")
            userlist = cursor.fetchall()
            for user in userlist:
                try:
                    player = lol_watcher.summoner.by_name(my_region, user[0])
                    match_id = lol_watcher.match.matchlist_by_puuid(my_region, player["puuid"], count = 1)[0]
                    if match_id != user[1]:
                        cursor.execute("UPDATE '" + server[0] + "' SET previous = '" + match_id + "'")
                        participants = lol_watcher.match.by_id(my_region, match_id)["info"]["participants"]
                        player_user = list(filter(lambda participant: participant["puuid"] == str(player["puuid"]), participants))[0]
                        kda = (float(player_user["kills"]) + float(player_user["assists"])) / float(player_user["deaths"])
                        if player_user["win"]:
                            await channel.send("my guy " + player_user["summonerName"] + " got a " + str(kda) + " kda on " + player_user["championName"] + " peepoClap")
                        else:
                            await channel.send("i believe in u " + player_user["summonerName"] + " you will do better next time")
                except ApiError as error:
                    print("Riot API Error:",error)
        bot.db.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to retrieve data from sqlite table.", error)

@bot.command()
async def setup(ctx):
    guild_id = ctx.guild.id
    channel_id = ctx.channel.id
    try:
        cursor = bot.db.cursor()
        cursor.execute("INSERT INTO serverlist (guild_id,channel_id) VALUES ('" + str(guild_id) + "','" + str(channel_id) + "')")
        cursor.execute("CREATE TABLE IF NOT EXISTS '" + str(guild_id) + "' ('user_id' varchar(255) NOT NULL, 'previous' varchar(255) NOT NULL DEFAULT 'NA', 'created_at' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
        bot.db.commit()
        cursor.close()
        print("Successfully inserted " + str(guild_id) + " into serverlist. Messages will be printed in channel: " + str(channel_id))
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table.", error)

@bot.command()
async def reset(ctx):
    guild_id = ctx.guild.id
    try:
        cursor = bot.db.cursor()
        cursor.execute("DELETE FROM serverlist WHERE guild_id='" + str(guild_id) + "'")
        cursor.execute("DROP TABLE '" + str(guild_id) + "'")
        bot.db.commit()
        cursor.close()
        print("Successfully deleted " + str(guild_id) + " from database.")
    except sqlite3.Error as error:
        print("Failed to reset:",error)

@bot.command()
async def adduser(ctx, arg):
    guild_id = ctx.guild.id
    user_id = arg
    try:
        cursor = bot.db.cursor()
        cursor.execute("INSERT INTO '" + str(guild_id) + "' (user_id) VALUES ('" + str(user_id) + "')")
        bot.db.commit()
        cursor.close()
        print(("Successfully inserted " + user_id + " into userlist."))
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table.", error)

@bot.command()
async def deluser(ctx, arg):
    guild_id = ctx.guild.id
    user_id = arg
    try:
        cursor = bot.db.cursor()
        cursor.execute("DELETE FROM '" + str(guild_id) + "' WHERE user_id = '" + str(user_id) + "'")
        bot.db.commit()
        cursor.close()
        print(("Successfully deleted " + user_id + " from userlist."))
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