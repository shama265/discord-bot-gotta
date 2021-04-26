from discord.ext import tasks, commands
from datetime import datetime, date, timedelta
from reminder_db import ReminderDb
import sys

class Reminder(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = ReminderDb()
    self.date_delta = timedelta(days=1)
    self.remind.start()
  
  def cog_unload(self):
    self.remind.cancel()
  
  @commands.command()
  async def rmd(self, ctx, date_string:str, remark:str):
    '''Set reminder from date'''
    try:
      now_date = datetime.today()
      month, day = map(int, date_string.split('/'))
      year = now_date.year
      if(month < now_date.month
        or month == now_date.month and day <= now_date.day):
        year += 1
      
      set_date = date(year, month, day)
      print(set_date)
      self.db.insertEvent(remark, set_date, ctx.channel.id)
      await ctx.message.add_reaction('👍')
    except ValueError:
      print(f'Invalid date string: {date_string}')
      await ctx.message.add_reaction('🆖')
    except:
      print(f'Uncaught exception: {sys.exc_info()[0]}')
      print(sys.exc_info()[2])
      await ctx.message.add_reaction('😩')

  @tasks.loop(hours=24.0)
  async def remind(self):
    '''Remind approaching events'''
    await self.bot.wait_until_ready()
    try:
      target_date = date.today() + self.date_delta
      events = self.db.selectAllEvents()
      for e in filter(lambda e: e['event_date'] >= target_date, events):
        await self.bot.get_channel(e['channel_id']).send(f'Reminder: {e["remark"]} at {e["event_date"]}')
        self.db.deleteById(e['id'])
    except Exception as e:
      print(f'Uncaught exception: {sys.exc_info()[0]}')

  def __del__(self):
    self.db.close()
