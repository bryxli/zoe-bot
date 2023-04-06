import disnake
from disnake.ext import commands

class HelpCommand(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = disnake.Embed(title="Help", color=disnake.Color.orange())

        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_command_signature(c) for c in filtered]

           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Other")
                if cog_name == 'ServerSetup':
                    command_signatures = command_signatures[::-1]
                    cog_name = 'Server'
                elif cog_name == 'LeagueSetup':
                    cog_name = 'League'
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = disnake.Embed(title=self.get_command_signature(command), color=disnake.Color.random())
        if command.description:
            embed.description = command.description
        if alias := command.aliases:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)