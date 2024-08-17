# module imports
import sqlite3

# project imports
from .sqlite_db import SqliteBase
from config import env
from utils import get_local_datetime


class Sqlite(SqliteBase):
    def __init__(self, db_name=env.DATABASE_URL):
        super().__init__()
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                brokerClientId TEXT,
                                brokerName TEXT,
                                apiKey TEXT,
                                apiSecret TEXT,
                                accessToken TEXT,
                                isAdmin INTEGER,
                                updated_at DATETIME,
                                created_at DATETIME)''')

        self.conn.commit()

    def create_user(self, brokerClientId: str, brokerName: str, apiKey: str, apiSecret: str, isAdmin: int = 0):
        self.cursor.execute(
            '''SELECT COUNT(*) FROM users WHERE brokerClientId = ? AND brokerName = ?''', (brokerClientId, brokerName))

        user_exists = self.cursor.fetchone()[0]

        if user_exists:
            return {
                'error': True,
                'message': 'User already exists'
            }

        created_at = get_local_datetime()
        self.cursor.execute('''
                            INSERT INTO users (brokerClientId, brokerName, apiKey, apiSecret, isAdmin, created_at) 
                            VALUES (?, ?, ?, ?, ?, ?)
                            ''',
                            (brokerClientId, brokerName, apiKey, apiSecret, isAdmin, created_at))
        self.conn.commit()
        return {
            'error': False,
            'message': 'New user created'
        }

    def update_user_token(self, brokerClientId: str, brokerName: str, accessToken: str):
        self.cursor.execute('''
          SELECT COUNT(*) FROM users WHERE brokerClientId = ? AND brokerName = ?
      ''', (brokerClientId, brokerName))

        user_exists = self.cursor.fetchone()[0]

        if user_exists > 0:
            time = get_local_datetime()
            self.cursor.execute('''
              UPDATE users
              SET accessToken = ?, updated_at = ?             
              WHERE brokerClientId = ? AND brokerName = ?
          ''', (accessToken, time, brokerClientId, brokerName))
            self.conn.commit()
            return {
                'error': False,
                'message': 'User record updated.'
            }
        else:
            return {
                'error': True,
                'message': 'User with the given clientId and broker does not exist.'
            }

    def close(self):
        self.conn.close()

sqlite_db = Sqlite()