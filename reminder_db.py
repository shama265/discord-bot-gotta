from datetime import date
import psycopg2
import psycopg2.extras
from os import environ

class ReminderDb:
  def __init__(self):
    self.__con = psycopg2.connect(environ['DATABASE_URL'])
    self.__con.cursor_factory = psycopg2.extras.DictCursor

    # CREATE TABLE
    with self.__con as con:
      with con.cursor() as cur:
        cur.execute('''CREATE TABLE IF NOT EXISTS events (
          id serial PRIMARY KEY,
          remark varchar NOT NULL,
          event_date date NOT NULL,
          channel_id bigint NOT NULL
        )''')

  def insertEvent(self, remark : str, event_date : date, channel_id : int):
    '''Add a event info'''
    with self.__con as con:
      with con.cursor() as cur:
        cur.execute('INSERT INTO events (remark, event_date, channel_id) values (%s, %s, %s)',
          (remark, event_date.isoformat(), channel_id))

  def selectAllEvents(self):
    '''Return events as a list of rows'''
    with self.__con as con:
      with con.cursor() as cur:
        cur.execute('SELECT id, remark, event_date, channel_id FROM events')
        return list(map(dict, cur.fetchall()))

  def deleteById(self, id : int):
    '''Delete a event by id'''
    with self.__con as con:
      with con.cursor() as cur:
        cur.execute('DELETE FROM events WHERE id = ?', (id,))

  def __enter__(self):
    return self
  
  def __exit__(self):
    self.close()

  def __del__(self):
    self.close()

  def close(self):
    self.__con.close()
