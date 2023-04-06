from disnake.ext import commands
import cass_wrapper as cass
import db_wrapper as db

class LeagueSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['au'], description='add user to server, user must be a valid League of Legends username')
    async def adduser(self, ctx, arg=None):  # add accountid to item in table
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

    @commands.command(aliases=['du'], description='add user to server, user must be a valid League of Legends username and exist')
    async def deluser(self, ctx, arg=None):  # delete accountid from item in table
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

    @commands.command(aliases=['ul'], description='show server userlist')
    async def userlist(self, ctx):  # display list of users from item in table
        if db.guild_exists(str(ctx.guild.id)):
            accountlist = db.get_all_users(str(ctx.guild.id))
            users = []
            for account in accountlist:
                users.append(cass.find_player_by_accountid(
                    account, db.get_guild(str(ctx.guild.id))['region']['S']).name)
            await ctx.send(users)
        else:
            await ctx.send('guild has not been setup')