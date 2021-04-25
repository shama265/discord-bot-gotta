from discord.ext import tasks, commands
from datetime import datetime, date, timedelta
from reminder_db import ReminderDb
import sys

class Reminder(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = ReminderDb()
    self.date_delta = timedelta(days=1)
  
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
      self.db.insertEvent(remark, set_date)
      await ctx.message.add_reaction('👍')
    except ValueError:
      print(f'Invalid date string: {date_string}')
      await ctx.message.add_reaction('🆖')
    except:
      print(f'Uncaught exception: {sys.exc_info()[0]}')
      print(sys.exc_info()[2])
      await ctx.message.add_reaction('😩')

  async def remind(self):
    target_date = date.today() + self.date_delta
    # fetch events from db

    # remind events started tomorrow

  def __del__(self):
    self.db.close()
