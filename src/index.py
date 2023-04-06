from discord.ext import tasks
import interactions

TOKEN = 'MTA4Mjg0NjIyODY3MDMyNDc4Ng.G8UJBj.QoOILEHr72atVA9GFOtB9wRwAe0CXOc4_ClQU8' # DEV 

bot = interactions.Client(token=TOKEN, default_scope=1016953904644247632)

@bot.event
async def on_ready():
    task.start()

@tasks.loop(seconds=5)
async def task():
    print('test')

@bot.command(name='my_first_command', description='description')
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")

def handler(event, context):
    bot.start(TOKEN)