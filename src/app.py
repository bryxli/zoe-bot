import json
import random

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

import cass_wrapper as cass
import db_wrapper as db

with open('config.json') as file:
    config = json.load(file)

intents = discord.Intents.all()
bot = Bot(command_prefix=commands.when_mentioned_or(config['prefix']), intents=intents, help_command=None)
bot.config = config

@bot.event
async def on_ready() -> None:
    await bot.change_presence(activity=discord.Game("#help"))
    loop.start()

@tasks.loop(minutes = 5.0)
async def loop():
    data = db.get_all()['Items']
    for guild in data:
        guild_id = guild['guild_id']['N']
        channel_id = guild['channel_id']['N']
        
        discord_guild = bot.get_guild(int(guild_id))
        discord_channel = discord_guild.get_channel(int(channel_id))

        for user_data in guild['userlist']['L']: # [{'M':{account_id:{'S':last_created}}}...]
            account_id = list(user_data['M'].keys())[0]

            summoner = cass.find_player_by_accountid(account_id, guild['region']['S'])

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

                    player = match.participants[id]
                    champion_name = player.champion.name
                    kda = str(round(player.stats.kda,2))
                    win = str(player.stats.win)

                    db.update_user(guild_id, account_id, last_created)
          
                    await discord_channel.send(f'{champion_name}  {kda}  {win}')

@bot.command()
async def setup(ctx): # create new item in table
    if not db.guild_exists(str(ctx.guild.id)):
        db.create_guild(str(ctx.guild.id), str(ctx.channel.id))
        await ctx.send(f'zoe will post game updates here (reminder: zoe only speaks once every five minutes!)\nunlocked commands: ?reset ?region ?adduser ?deluser ?userlist')
    else:
        await ctx.send('guild already exists')

@bot.command()
async def reset(ctx): # delete item from table
    if db.guild_exists(str(ctx.guild.id)):
        db.destroy_guild(str(ctx.guild.id))
        await ctx.message.add_reaction(u"\U0001F44D")
    else:
        await ctx.send('guild has not been setup')   

@bot.command()
async def region(ctx, arg=None): # view current region / set new region of item in table
    if db.guild_exists(str(ctx.guild.id)):
        regionlist = ['BR','EUNE','EUW','JP','KR','LAN','LAS','NA','OCE','TR','RU']
        if arg is None:
            await ctx.send(regionlist)
            return
        if arg.upper() in regionlist:
            updates = {
                'region': {'Value': {'S': arg}, 'Action': 'PUT'}, 
            }
            db.update_guild(str(ctx.guild.id), updates)
            await ctx.message.add_reaction(u"\U0001F44D")
        else:
            await ctx.send('region not found')   
    else:
        await ctx.send('guild has not been setup')

@bot.command()
async def adduser(ctx, arg=None): # add accountid to item in table
    if db.guild_exists(str(ctx.guild.id)):
        if arg is None:
            await ctx.send('please enter a username')
            return
        player = cass.find_player_by_name(arg,db.get_guild(str(ctx.guild.id))['region']['S'])
        if player is None:
            await ctx.send('please enter a valid username')
            return
        if db.user_exists(str(ctx.guild.id),player.account_id):
            await ctx.send('user already exists')
            return
        db.add_user(str(ctx.guild.id), player.account_id)
        await ctx.message.add_reaction(u"\U0001F44D")
    else:
        await ctx.send('guild has not been setup')

@bot.command()
async def deluser(ctx, arg=None): # delete accountid from item in table
    if db.guild_exists(str(ctx.guild.id)):
        if arg is None:
            await ctx.send('please enter a username')
            return
        player = cass.find_player_by_name(arg,db.get_guild(str(ctx.guild.id))['region']['S'])
        if player is None:
            await ctx.send('please enter a valid username')
            return
        if not db.user_exists(str(ctx.guild.id),player.account_id): # TODO: db.user_exists and db.delete_user both call get_all_users, consolidate to avoid unecessary calls
            await ctx.send('user does not exist')
            return
        db.delete_user(str(ctx.guild.id), player.account_id)
        await ctx.message.add_reaction(u"\U0001F44D")
    else:
        await ctx.send('guild has not been setup')


@bot.command()
async def userlist(ctx): # display list of users from item in table
    if db.guild_exists(str(ctx.guild.id)):
        accountlist = db.get_all_users(str(ctx.guild.id))
        users = []
        for account in accountlist:
            users.append(cass.find_player_by_accountid(account,db.get_guild(str(ctx.guild.id))['region']['S']).name)
        await ctx.send(users)
    else:
        await ctx.send('guild has not been setup')

@bot.command()
async def speak(ctx):
    first_move = ["Hey guys, so, cosmic change time, possible armageddon, twilight of the gods, blah blah blah. You've been heralded.","There are so many weirdos here... It's awesome!","I bring a message for you all: a warning, a sigil. But first, I wanna see the sparkle flies.","Hello? Hey, I'm over here if you want to aim a high-velocity attack against me! Maybe you'll hit me this time!","Anyone wanna go into that ankle-deep liquid? Hello? Hellooooo!!","Here we go on an adventure, through this place! Even though we don't know the name of it! It doesn't matter!","The sky is billions of explosions burning far away! How could you not wanna see them?? I did. They were pretty cool.","This will be fine! Don't worry about it Zoe, things break all the time. Like reality, planets... y'know, stuff.","The sun and moon rise in time, to ash and mirth. The mountain takes... all. Change comes.","When the beings here look up, do they think we're looking back?! We really aren't.","Heyyyy! I'm gonna have new friends, new friends here, and it's gonna be awesome 'cause they are awesome and we'll have an awesome party with cake and stuff! Should I make chocolate mooncake or strawberry mooncake? CHOCOLATE STRAWBERRY CAKE!!","There's this illusion of the reality, but it's not really really real, like it's beside and inside and inside and beside, but never on top... Nevermind, just kidding, but not really..","Ohh! I like how the atmospheric refraction is favoring intense short waves today!","The sky called to me. So I went! It was pretty cool. I like this too, though.","Psst! Hey! Can you tell me your secrets? I promise not to tell them to... everyone!","There are holes in reality. And... in donuts.","We don't try to understand the sense it doesn't make, so we're trying to share that with you. You're welcome.","There is a day we must all fulfill our destiny. ...That day is taco day!!","So, there's these, like, yinger and yangerons, and they spin in this projected pattern which intersects fourth-dimensionally. But it isn't a measurable function. It's got a whoosh, whoom, whoooooooooh!"]
    await ctx.send(random.choice(first_move))

@bot.command()
async def help(ctx):
    post_setup = ''
    if db.guild_exists(str(ctx.guild.id)):
        post_setup = '?reset - reset instance\n?region <region> - change server region\n?adduser <league username> - add user to server\n?deluser <league username> - delete user from server\n?userlist - show server userlist\n'
    await ctx.send(f'Commands\n?setup - create server instance\n{post_setup}?speak - zoe will talk to you')

bot.run(config['token'])