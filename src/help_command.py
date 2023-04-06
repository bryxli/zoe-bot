import disnake
from disnake.ext import commands

class HelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
                emby = disnake.Embed(description=page)
                await destination.send(embed=emby)