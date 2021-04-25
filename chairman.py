import discord
from discord.ext import commands
from asyncio import sleep
from reminder import Reminder
from os import environ

bot = commands.Bot(command_prefix='$')

client = discord.Client()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def hello(ctx, delay:float = 0):
  if(delay > 0):
    print(f'send hello after {delay} sec(s)')
    await sleep(delay)
  await ctx.send('Hello!')

@bot.command()
async def look(ctx):
  await ctx.message.add_reaction('👀')

bot.add_cog(Reminder(bot))

bot.run(environ['BOT_TOKEN'])
