from disnake.ext import commands
import db_wrapper as db

class ServerSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='create server instance')
    async def setup(self, ctx):  # create new item in table
        if not db.guild_exists(str(ctx.guild.id)):
            db.create_guild(str(ctx.guild.id), str(ctx.channel.id))
            await ctx.send(f'zoe will post game updates here (reminder: zoe only speaks once every five minutes!)\nunlocked commands: ?reset ?region ?adduser ?deluser ?userlist')
        else:
            await ctx.send('guild already exists')

    @commands.command(description='reset instance')
    async def reset(self, ctx):  # delete item from table
        if db.guild_exists(str(ctx.guild.id)):
            db.destroy_guild(str(ctx.guild.id))
            await ctx.message.add_reaction(u"\U0001F44D")
        else:
            await ctx.send('guild has not been setup')

    @commands.command(description='change server region')
    async def region(self, ctx, arg=None):  # set new region of item in table
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
                    response = await self.bot.wait_for('message', check=check, timeout=10.0)
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