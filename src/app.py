import json
import random
from string import Template

import disnake
from disnake.ext import commands, tasks

from commands.help_command import HelpCommand
from commands.server_commands import Server
from commands.league_commands import League

import wrappers.cassiopeia as cass
import wrappers.dynamo as db

with open('config.json') as file:
    config = json.load(file)

with open("template.json") as file:
    template = json.load(file)

bot = commands.Bot(command_prefix=commands.when_mentioned_or(config['prefix']), intents=disnake.Intents.all(), help_command=HelpCommand())
bot.add_cog(Server(bot))
bot.add_cog(League(bot))

@bot.event
async def on_ready() -> None:
    await bot.change_presence(activity=disnake.Game("?help"))
    loop.start()


@tasks.loop(minutes=5.0)
async def loop():
    data = db.get_all()['Items']
    for guild in data:
        guild_id = guild['guild_id']['N']
        channel_id = guild['channel_id']['N']
        print(f'checking in {guild_id}:{channel_id}')

        try:
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
        except Exception as e:
            print(e)


@bot.command(description='zoe will talk to you')
async def speak(ctx):
    response = template['response']
    await ctx.send(random.choice(response))

bot.run(config['token'])
