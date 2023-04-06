import json
import random
from string import Template

from discord.ext import tasks
import interactions

import cass_wrapper as cass
import db_wrapper as db

with open('config.json') as file:
    config = json.load(file)

with open("template.json") as file:
    template = json.load(file)

bot = interactions.Client(token=config['token'], default_scope=1016953904644247632)


def lambda__handler(event, context):
    bot.start()


@bot.event
async def on_ready() -> None:
    # await bot.change_presence(activity=discord.Game("?help"))
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


@bot.command(name='setup', description='create new item in table')
async def setup(ctx: interactions.CommandContext):
    if not db.guild_exists(str(ctx.guild.id)):
        db.create_guild(str(ctx.guild.id), str(ctx.channel.id))
        await ctx.send(f'zoe will post game updates here (reminder: zoe only speaks once every five minutes!)\nunlocked commands: ?reset ?region ?adduser ?deluser ?userlist')
    else:
        await ctx.send('guild already exists')


@bot.command(name='reset', description='delete item from table')
async def reset(ctx: interactions.CommandContext): 
    if db.guild_exists(str(ctx.guild.id)):
        db.destroy_guild(str(ctx.guild.id))
        await ctx.message.add_reaction(u"\U0001F44D")
    else:
        await ctx.send('guild has not been setup')


@bot.command(name='region', description='set new region of item in table', options= [
    interactions.Option(
        name='region',
        description='region',
        type=interactions.OptionType.STRING,
        required=False,
    ),
    interactions.Option(
        name='confirmation',
        description='confirmation',
        type=interactions.OptionType.STRING,
        required=False,
    )
])
async def region(ctx: interactions.CommandContext, region: str = '', confirmation: str = ''):  
    if db.guild_exists(str(ctx.guild.id)):
        regionlist = ['BR', 'EUNE', 'EUW', 'JP', 'KR',
                      'LAN', 'LAS', 'NA', 'OCE', 'TR', 'RU']
        if region == '':
            await ctx.send(str(regionlist))
            return
        current_region = region.upper()
        if current_region in regionlist:
            if confirmation.upper() == 'Y':
                updates = {
                        'region': {'Value': {'S': current_region}, 'Action': 'PUT'},
                        'userlist': {'Value': {'L': []}, 'Action': 'PUT'},
                }
                db.update_guild(str(ctx.guild.id), updates)
                await ctx.message.add_reaction(u"\U0001F44D")
            else:
                await ctx.send('changing server region will clear all users, please enter "Y" for confirmation field Ex: /region [region:na, confirmation:Y]')
        else:
            await ctx.send('region not found')
    else:
        await ctx.send('guild has not been setup')


@bot.command(name='adduser', description='add accountid to item in table', options= [
    interactions.Option(
        name='username',
        description='username',
        type=interactions.OptionType.STRING,
        required=True,
    )
])
async def adduser(ctx: interactions.CommandContext, username: str = ''): 
    if db.guild_exists(str(ctx.guild.id)):
        if username == '':
            await ctx.send('please enter a username')
            return
        player = cass.find_player_by_name(username, db.get_guild(str(ctx.guild.id))['region']['S'])
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


@bot.command(name='deluser', description='delete accountid from item in table', options= [
    interactions.Option(
        name='username',
        description='username',
        type=interactions.OptionType.STRING,
        required=True,
    )
])
async def deluser(ctx: interactions.CommandContext, username: str = ''):  
    if db.guild_exists(str(ctx.guild.id)):
        if username == '':
            await ctx.send('please enter a username')
            return
        player = cass.find_player_by_name(username, db.get_guild(str(ctx.guild.id))['region']['S'])
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


@bot.command(name='userlist', description='display list of users from item in table')
async def userlist(ctx: interactions.CommandContext):  
    if db.guild_exists(str(ctx.guild.id)):
        accountlist = db.get_all_users(str(ctx.guild.id))
        users = []
        for account in accountlist:
            users.append(cass.find_player_by_accountid(
                account, db.get_guild(str(ctx.guild.id))['region']['S']).name)
        if len(users) > 0:
            await ctx.send(str(users))
        else:
            await ctx.send('no users')
    else:
        await ctx.send('guild has not been setup')


@bot.command(name='speak', description='blah blah blah')
async def speak(ctx: interactions.CommandContext):
    response = template['response']
    await ctx.send(random.choice(response))


@bot.command(name='help', description='display help menu')
async def help(ctx: interactions.CommandContext):
    post_setup = ''
    if db.guild_exists(str(ctx.guild.id)):
        post_setup = '?reset - reset instance\n?region <region> - change server region\n?adduser <league username> - add user to server\n?deluser <league username> - delete user from server\n?userlist - show server userlist\n'
    await ctx.send(f'Commands\n?setup - create server instance\n{post_setup}?speak - zoe will talk to you')


if __name__ == '__main__':
    bot.start()