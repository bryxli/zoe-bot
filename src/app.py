import json
import random
from string import Template

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

import cass_wrapper as cass
import db_wrapper as db

with open('config.json') as file:
    config = json.load(file)

with open("template.json") as file:
    template = json.load(file)

intents = discord.Intents.all()
bot = Bot(command_prefix=commands.when_mentioned_or(
    config['prefix']), intents=intents, help_command=None)
bot.config = config


@bot.event
async def on_ready() -> None:
    await bot.change_presence(activity=discord.Game("?help"))
    loop.start()


@tasks.loop(minutes=5.0)
async def loop():
    data = db.get_all()['Items']
    for guild in data:
        guild_id = guild['guild_id']['N']
        channel_id = guild['channel_id']['N']
        print(f'checking in {guild_id}:{channel_id}')

        discord_guild = bot.get_guild(int(guild_id))
        discord_channel = discord_guild.get_channel(int(channel_id))

        # [{'M':{account_id:{'S':last_created}}}...]
        for user_data in guild['userlist']['L']:
            account_id = list(user_data['M'].keys())[0]
            print(f'found user {account_id}')

            summoner = cass.find_player_by_accountid(
                account_id, guild['region']['S'])

            match_history = summoner.match_history
            if (match_history.count > 0):
                match = match_history[0]
                for participant in match.participants:
                    if participant.summoner.account_id == summoner.account_id:
                        id = match.participants.index(participant)
                        break

                last_created_old = user_data['M'][account_id]['S']
                last_created = str(match.creation)
                if last_created != last_created_old:
                    print('found new match')

                    player = match.participants[id]
                    summoner_name = summoner.name
                    champion_name = player.champion.name
                    kda = str(round(player.stats.kda, 2))
                    win = player.stats.win

                    if win:
                        t = Template(random.choice(template['win']))
                    else:
                        t = Template(random.choice(template['lose']))

                    db.update_user(guild_id, account_id, last_created)

                    await discord_channel.send(t.substitute(summoner_name=summoner_name, kda=kda, champion_name=champion_name))


@bot.command()
async def setup(ctx):  # create new item in table
    if not db.guild_exists(str(ctx.guild.id)):
        db.create_guild(str(ctx.guild.id), str(ctx.channel.id))
        await ctx.send(f'zoe will post game updates here (reminder: zoe only speaks once every five minutes!)\nunlocked commands: ?reset ?region ?adduser ?deluser ?userlist')
    else:
        await ctx.send('guild already exists')


@bot.command()
async def reset(ctx):  # delete item from table
    if db.guild_exists(str(ctx.guild.id)):
        db.destroy_guild(str(ctx.guild.id))
        await ctx.message.add_reaction(u"\U0001F44D")
    else:
        await ctx.send('guild has not been setup')


@bot.command()
async def region(ctx, arg=None):  # set new region of item in table
    if db.guild_exists(str(ctx.guild.id)):
        regionlist = ['BR', 'EUNE', 'EUW', 'JP', 'KR',
                      'LAN', 'LAS', 'NA', 'OCE', 'TR', 'RU']
        if arg is None:
            await ctx.send(regionlist)
            return
        current_region = arg.upper()
        if current_region in regionlist:
            await ctx.send('changing server region will clear all users, are you sure? y/n')

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                response = await bot.wait_for('message', check=check, timeout=10.0)
            except Exception:
                await ctx.send('timeout: server region not changed')
            else:
                if response.content.upper() == 'Y':
                    updates = {
                        'region': {'Value': {'S': current_region}, 'Action': 'PUT'},
                        'userlist': {'Value': {'L': []}, 'Action': 'PUT'},
                    }
                    db.update_guild(str(ctx.guild.id), updates)
                    await response.add_reaction(u"\U0001F44D")
                elif response.content.upper() == 'N':
                    await ctx.send('server region not changed')
        else:
            await ctx.send('region not found')
    else:
        await ctx.send('guild has not been setup')


@bot.command()
async def adduser(ctx, arg=None):  # add accountid to item in table
    if db.guild_exists(str(ctx.guild.id)):
        if arg is None:
            await ctx.send('please enter a username')
            return
        player = cass.find_player_by_name(
            arg, db.get_guild(str(ctx.guild.id))['region']['S'])
        if player is None:
            await ctx.send('please enter a valid username')
            return
        if db.user_exists(str(ctx.guild.id), player.account_id):
            await ctx.send('user already exists')
            return
        db.add_user(str(ctx.guild.id), player.account_id)
        await ctx.message.add_reaction(u"\U0001F44D")
    else:
        await ctx.send('guild has not been setup')


@bot.command()
async def deluser(ctx, arg=None):  # delete accountid from item in table
    if db.guild_exists(str(ctx.guild.id)):
        if arg is None:
            await ctx.send('please enter a username')
            return
        player = cass.find_player_by_name(
            arg, db.get_guild(str(ctx.guild.id))['region']['S'])
        if player is None:
            await ctx.send('please enter a valid username')
            return
        # TODO: db.user_exists and db.delete_user both call get_all_users, consolidate to avoid unecessary calls
        if not db.user_exists(str(ctx.guild.id), player.account_id):
            await ctx.send('user does not exist')
            return
        db.delete_user(str(ctx.guild.id), player.account_id)
        await ctx.message.add_reaction(u"\U0001F44D")
    else:
        await ctx.send('guild has not been setup')


@bot.command()
async def userlist(ctx):  # display list of users from item in table
    if db.guild_exists(str(ctx.guild.id)):
        accountlist = db.get_all_users(str(ctx.guild.id))
        users = []
        for account in accountlist:
            users.append(cass.find_player_by_accountid(
                account, db.get_guild(str(ctx.guild.id))['region']['S']).name)
        await ctx.send(users)
    else:
        await ctx.send('guild has not been setup')


@bot.command()
async def speak(ctx):
    response = template['response']
    await ctx.send(random.choice(response))


@bot.command()
async def help(ctx):
    post_setup = ''
    if db.guild_exists(str(ctx.guild.id)):
        post_setup = '?reset - reset instance\n?region <region> - change server region\n?adduser <league username> - add user to server\n?deluser <league username> - delete user from server\n?userlist - show server userlist\n'
    await ctx.send(f'Commands\n?setup - create server instance\n{post_setup}?speak - zoe will talk to you')

bot.run(config['token'])
