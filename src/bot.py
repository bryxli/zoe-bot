import json
import os
import platform
import sqlite3
import sys
import random
import functools
import typing
import asyncio
import logging

from contextlib import closing
from string import Template
from riotwatcher import LolWatcher, ApiError

import discord
from discord.ext import tasks, commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

if not os.path.isfile("templates/custom.json"):
    print("'templates/custom.json' not found! Using default responses.")
    custom = None
else:
    with open("templates/custom.json") as file:
        custom = json.load(file)

if not os.path.isfile("logs/log.log"):
    f = open("logs/log.log", "x")
    f.close()
        
intents = discord.Intents.all()

bot = Bot(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents, help_command=None)
lol_watcher = LolWatcher(config["league_token"])
default_region = "na1"
regionlist = ['br1', 'eun1', 'euw1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'tr1', 'ru']

def init_db():
    with closing(connect_db()) as db:
        with open("../database/createServer.sql", "r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    return sqlite3.connect("../database/database.db")

bot.config = config
bot.db = connect_db()

@bot.event
async def on_ready() -> None:
    logging.basicConfig(filename='logs/log.log', filemode='w', format='%(message)s', level="WARN")
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    await bot.change_presence(activity=discord.Game("?help"))
    status_task.start()

@tasks.loop(minutes = 5.0)
async def status_task() -> None:
    try:
        cursor = bot.db.cursor()
        cursor.execute("SELECT * FROM serverlist")
        serverlist = cursor.fetchall()
        for server in serverlist:
            guild = bot.get_guild(int(server[0]))
            try:
                channel = guild.get_channel(int(server[1]))
                cursor.execute(f"SELECT * FROM '{server[0]}' ORDER BY RANDOM()")
                userlist = cursor.fetchall()
                for user in userlist:
                    try:
                        region = server[3]
                        player = await find_player(region, user[0])
                        try:
                            match_id = await find_match(region, player["puuid"])
                        except IndexError as error:
                            continue
                        if match_id != user[1]:
                            participants = await find_participants(region, match_id)
                            player_user = list(filter(lambda participant: participant["puuid"] == str(player["puuid"]), participants))[0]
                            try:
                                kda = str(round((float(player_user["kills"]) + float(player_user["assists"])) / float(player_user["deaths"]),2))
                            except ZeroDivisionError as error:
                                kda = "perfect"
                            if custom is not None:
                                if player_user["win"]:
                                    if len(custom["win"]) > 0:
                                        t = Template(random.choice(custom["win"]))
                                        answer = t.substitute(summonername=player_user["summonerName"], kda=kda, championname = player_user["championName"])
                                    else:
                                        answer = f"{player_user['summonerName']}: Win || {player_user['championName']} KDA: {kda}"
                                else:
                                    if len(custom["lose"]) > 0:
                                        t = Template(random.choice(custom["lose"]))
                                        answer = t.substitute(summonername=player_user["summonerName"], kda=kda, championname = player_user["championName"])
                                    else:
                                        answer = f"{player_user['summonerName']}: Loss || {player_user['championName']} KDA: {kda}"
                            else:
                                win_loss = "Win" if player_user["win"] else "Loss"
                                answer = f"{player_user['summonerName']}: {win_loss} || {player_user['championName']} KDA: {kda}"
                            await channel.send(answer)
                            cursor.execute(f"INSERT INTO recent (message) VALUES ('{answer}')")
                            cursor.execute(f"UPDATE '{server[0]}' SET previous = '{match_id}' WHERE user_id = '{player_user['summonerName']}'")
                    except ApiError as error:
                        print("Riot API Error:",error)
            except AttributeError as error:
                pass
        bot.db.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to retrieve data from sqlite table.", error)

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

@to_thread
def find_player(region, id):
    return lol_watcher.summoner.by_name(region, id)

@to_thread
def find_match(region, puuid):
    return lol_watcher.match.matchlist_by_puuid(region, puuid)[0]

@to_thread
def find_participants(region, match_id):
    return lol_watcher.match.by_id(region, match_id)["info"]["participants"]

@bot.command()
async def setup(ctx):
    guild_id = str(ctx.guild.id)
    channel_id = str(ctx.channel.id)
    try:
        cursor = bot.db.cursor()
        cursor.execute(f"INSERT INTO serverlist (guild_id,channel_id,region) VALUES ('{guild_id }','{channel_id}','{default_region}')")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS '{guild_id}' ('user_id' varchar(255) NOT NULL, 'previous' varchar(255) NOT NULL DEFAULT 'NA', 'created_at' timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
        bot.db.commit()
        cursor.close()
        print(f"Successfully inserted {guild_id} into serverlist. Messages will be printed in channel: {channel_id}")
        await ctx.send("i will send messages here (reminder: zoe only speaks once every five minutes!)\nunlocked commands: ?reset ?region ?setregion ?adduser ?deluser ?userlist")
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table.", error)

@bot.command()
async def reset(ctx):
    guild_id = str(ctx.guild.id)
    try:
        cursor = bot.db.cursor()
        cursor.execute(f"DELETE FROM serverlist WHERE guild_id='{guild_id}'")
        cursor.execute(f"DROP TABLE '{guild_id}'")
        bot.db.commit()
        cursor.close()
        print(f"Successfully deleted {guild_id} from serverlist.")
        await ctx.message.add_reaction(u"\U0001F44D")
    except sqlite3.Error as error:
        print("Failed to reset:",error)

@bot.command()
async def region(ctx):
    guild_id = str(ctx.guild.id)
    try:
        cursor = bot.db.cursor()
        cursor.execute(f"SELECT region FROM serverlist WHERE guild_id='{guild_id}'")
        region = cursor.fetchall()[0][0]
        await ctx.send(f"region is currently set to {region}\nregion values: {str(regionlist)}")
    except sqlite3.Error as error:
        print("Failed to find region column:",error)

@bot.command()
async def setregion(ctx, arg):
    guild_id = str(ctx.guild.id)
    region = str(arg)
    if region not in regionlist:
        await ctx.send("region not found")
    else:
        try:
            cursor = bot.db.cursor()
            cursor.execute(f"UPDATE serverlist SET region = '{region}' WHERE guild_id='{guild_id}'")
            bot.db.commit()
            cursor.close()
            print(f"Successfully changed region in {guild_id}")
            await ctx.message.add_reaction(u"\U0001F44D")
        except sqlite3.Error as error:
            print("Failed to update region column:",error)

@bot.command()
async def adduser(ctx, arg):
    guild_id = str(ctx.guild.id)
    user_id = str(arg)
    try:
        cursor = bot.db.cursor()
        cursor.execute(f"SELECT region FROM serverlist WHERE guild_id='{guild_id}'")
        region = cursor.fetchall()[0][0]
        player = await find_player(region, arg)
        user_id = player["name"]
        cursor.execute(f"SELECT * FROM '{guild_id}'")
        userlist = cursor.fetchall()
        for i in range(len(userlist)):
            if user_id == userlist[i][0]:
                raise EnvironmentError(user_id)
        cursor.execute(f"INSERT INTO '{guild_id}' (user_id) VALUES ('{user_id}')")
        bot.db.commit()
        cursor.close()
        print(f"Successfully inserted {user_id} into {guild_id}")
        await ctx.message.add_reaction(u"\U0001F44D")
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table.", error)
    except ApiError as error:
        await ctx.send("name not found")
    except EnvironmentError as error: 
        await ctx.send(f"{user_id} has already been added")

@bot.command()
async def deluser(ctx, arg):
    guild_id = str(ctx.guild.id)
    user_id = str(arg)
    try:
        cursor = bot.db.cursor()
        cursor.execute("DELETE FROM '{guild_id}' WHERE user_id = '{user_id}' COLLATE NOCASE")
        bot.db.commit()
        cursor.close()
        print(f"Successfully deleted {user_id} from {guild_id}")
        await ctx.message.add_reaction(u"\U0001F44D")
    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table.", error)  

@bot.command()
async def userlist(ctx):
    guild_id = str(ctx.guild.id)
    try:
        cursor = bot.db.cursor()
        cursor.execute(f"SELECT * FROM '{guild_id}'")
        userlist = cursor.fetchall()
        users = ""
        for user in userlist:
            users += str(user[0]) + "\n"
        if users == "":
            users = "userlist empty!"
        cursor.close()
        print("Successfully printed userlist:\n" + users)
        await ctx.send(users)
    except sqlite3.Error as error:
        print("Failed to retrieve data from sqlite table.")

@bot.command()
async def speak(ctx):
    if custom is not None and len(custom["speak"]) > 0:
        await ctx.send(random.choice(custom["speak"]))
    else:
        first_move = ["Hey guys, so, cosmic change time, possible armageddon, twilight of the gods, blah blah blah. You've been heralded.","There are so many weirdos here... It's awesome!","I bring a message for you all: a warning, a sigil. But first, I wanna see the sparkle flies.","Hello? Hey, I'm over here if you want to aim a high-velocity attack against me! Maybe you'll hit me this time!","Anyone wanna go into that ankle-deep liquid? Hello? Hellooooo!!","Here we go on an adventure, through this place! Even though we don't know the name of it! It doesn't matter!","The sky is billions of explosions burning far away! How could you not wanna see them?? I did. They were pretty cool.","This will be fine! Don't worry about it Zoe, things break all the time. Like reality, planets... y'know, stuff.","The sun and moon rise in time, to ash and mirth. The mountain takes... all. Change comes.","When the beings here look up, do they think we're looking back?! We really aren't.","Heyyyy! I'm gonna have new friends, new friends here, and it's gonna be awesome 'cause they are awesome and we'll have an awesome party with cake and stuff! Should I make chocolate mooncake or strawberry mooncake? CHOCOLATE STRAWBERRY CAKE!!","There's this illusion of the reality, but it's not really really real, like it's beside and inside and inside and beside, but never on top... Nevermind, just kidding, but not really..","Ohh! I like how the atmospheric refraction is favoring intense short waves today!","The sky called to me. So I went! It was pretty cool. I like this too, though.","Psst! Hey! Can you tell me your secrets? I promise not to tell them to... everyone!","There are holes in reality. And... in donuts.","We don't try to understand the sense it doesn't make, so we're trying to share that with you. You're welcome.","There is a day we must all fulfill our destiny. ...That day is taco day!!","So, there's these, like, yinger and yangerons, and they spin in this projected pattern which intersects fourth-dimensionally. But it isn't a measurable function. It's got a whoosh, whoom, whoooooooooh!"]
        await ctx.send(random.choice(first_move))

@bot.command()
async def help(ctx):
    guild_id = str(ctx.guild.id)
    post_setup = "?reset - wipe server from database\n?region - list current region and region codes\n?setregion <region> - set server region\n?adduser <league username> - add to server database\n?deluser <league username> - delete from server database\n?userlist - show server userlist\n"
    try:
        cursor = bot.db.cursor()
        cursor.execute(f"SELECT * FROM '{guild_id}'")
        cursor.close()
    except sqlite3.Error as error:
        post_setup = ""
    await ctx.send(f"Commands\n?setup - zoe will speak in this channel\n{post_setup}?speak - zoe will talk to you")

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