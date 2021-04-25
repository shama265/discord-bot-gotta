import sqlite3
from datetime import date

db_file = 'gottani.db'

class ReminderDb:
  def __init__(self):
    self.__con = sqlite3.connect(db_file)

    # CREATE TABLE
    self.__con.execute('''CREATE TABLE IF NOT EXISTS events (
      id INTEGER PRIMARY KEY,
      remark TEXT,
      date TEXT
    )''')

  def insertEvent(self, remark : str, event_date : date):
    with self.__con as con:
      con.execute('INSERT INTO events (remark, date) values (?, ?)',
        (remark, event_date.isoformat()))

  def selectAllEvents(self):
    with self.__con as con:
      return con.execute('SELECT * FROM events').fetchall()

  def __enter__(self):
    return self
  
  def __exit__(self):
    self.close()

  def __del__(self):
    self.close()

  def close(self):
    self.__con.close()
