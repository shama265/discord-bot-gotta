import sqlite3
from datetime import date

db_file = 'gottani.db'

class ReminderDb:
  def __init__(self):
    self.__con = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    self.__con.row_factory = sqlite3.Row

    # CREATE TABLE
    self.__con.execute('''CREATE TABLE IF NOT EXISTS events (
      id INTEGER PRIMARY KEY,
      remark TEXT NOT NULL,
      event_date DATE NOT NULL,
      channel_id INTEGER NOT NULL
    )''')

  def insertEvent(self, remark : str, event_date : date, channel_id : int):
    '''Add a event info'''
    with self.__con as con:
      return con.execute('INSERT INTO events (remark, event_date, channel_id) values (?, ?, ?)',
        (remark, event_date.isoformat(), channel_id))

  def selectAllEvents(self):
    '''Return events as a list of rows'''
    with self.__con as con:
      return list(map(dict, con.execute('SELECT id, remark, event_date, channel_id FROM events').fetchall()))

  def deleteById(self, id : int):
    '''Delete a event by id'''
    with self.__con as con:
      return con.execute('DELETE FROM events WHERE id = ?', (id,))

  def __enter__(self):
    return self
  
  def __exit__(self):
    self.close()

  def __del__(self):
    self.close()

  def close(self):
    self.__con.close()
