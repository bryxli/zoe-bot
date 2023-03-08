import json
import random

import discord
from discord.ext import commands
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

@bot.command()
async def setup(ctx): # create new item in table
    response = db.create_guild(str(ctx.guild.id), str(ctx.channel.id)) # do not run this if guild.id exists
    await ctx.send(response)

@bot.command()
async def reset(ctx): # delete item from table
    response = db.delete_guild(str(ctx.guild.id)) # do not run this if guild.id does not exist
    await ctx.send(response)   

@bot.command()
async def region(ctx, arg=None): # view current region / set new region of item in table
    regionlist = ['BR','EUNE','EUW','JP','KR','LAN','LAS','NA','OCE','TR','RU']
    if arg is None:
        await ctx.send(regionlist)
        return
    response = 'region not found'
    if arg.upper() in regionlist:
        updates = {
            'region': {'Value': {'S': arg}, 'Action': 'PUT'}, 
        }
        response = db.update_guild(str(ctx.guild.id), updates)
    await ctx.send(response)   

@bot.command()
async def adduser(ctx, arg): # add user to item in table
    player = cass.find_player_by_name(arg,'NA')
    await ctx.send(player)

@bot.command()
async def deluser(ctx): # delete user from item in table
    await ctx.send('deluser')

@bot.command()
async def userlist(ctx): # display list of users from item in table
    await ctx.send('userlist')

@bot.command()
async def speak(ctx):
    first_move = ["Hey guys, so, cosmic change time, possible armageddon, twilight of the gods, blah blah blah. You've been heralded.","There are so many weirdos here... It's awesome!","I bring a message for you all: a warning, a sigil. But first, I wanna see the sparkle flies.","Hello? Hey, I'm over here if you want to aim a high-velocity attack against me! Maybe you'll hit me this time!","Anyone wanna go into that ankle-deep liquid? Hello? Hellooooo!!","Here we go on an adventure, through this place! Even though we don't know the name of it! It doesn't matter!","The sky is billions of explosions burning far away! How could you not wanna see them?? I did. They were pretty cool.","This will be fine! Don't worry about it Zoe, things break all the time. Like reality, planets... y'know, stuff.","The sun and moon rise in time, to ash and mirth. The mountain takes... all. Change comes.","When the beings here look up, do they think we're looking back?! We really aren't.","Heyyyy! I'm gonna have new friends, new friends here, and it's gonna be awesome 'cause they are awesome and we'll have an awesome party with cake and stuff! Should I make chocolate mooncake or strawberry mooncake? CHOCOLATE STRAWBERRY CAKE!!","There's this illusion of the reality, but it's not really really real, like it's beside and inside and inside and beside, but never on top... Nevermind, just kidding, but not really..","Ohh! I like how the atmospheric refraction is favoring intense short waves today!","The sky called to me. So I went! It was pretty cool. I like this too, though.","Psst! Hey! Can you tell me your secrets? I promise not to tell them to... everyone!","There are holes in reality. And... in donuts.","We don't try to understand the sense it doesn't make, so we're trying to share that with you. You're welcome.","There is a day we must all fulfill our destiny. ...That day is taco day!!","So, there's these, like, yinger and yangerons, and they spin in this projected pattern which intersects fourth-dimensionally. But it isn't a measurable function. It's got a whoosh, whoom, whoooooooooh!"]
    await ctx.send(random.choice(first_move))

@bot.command()
async def help(ctx):
    await ctx.send('help')

bot.run(config['token'])