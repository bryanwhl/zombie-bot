import sqlite3
import threading

'''
CONSTANTS
'''
EVENT_MESSAGE = 6
USER_NAME = 0
START_DATE = 1
END_DATE = 2
COLLECTION_DATE = 3
LOCK = threading.Lock()

class Database:
    '''
    Initializing database.db file and connecting to the file
    '''
    def __init__(self):
        self.con = sqlite3.connect(
            'database.db', check_same_thread=False)
        self.cur = self.con.cursor()

    '''
    Initializing commit function
    '''
    def commit(self):
      self.con.commit()

    '''
    Initializing tables which only needs to be called once at the start of the program
    '''
    def create_tables(self):
        try:
            self.cur.execute(
                '''CREATE TABLE users(username text, nusnet_id text, house text, telegram_id text, type text, id text)''')
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            return e
            