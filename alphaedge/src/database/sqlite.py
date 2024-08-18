# module imports
import sqlite3
from typing import Dict, List, Any

# project imports
from .sqlite_base import SqliteBase
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
                                broker_client_id TEXT,
                                broker_name TEXT,
                                api_key TEXT,
                                api_secret TEXT,
                                access_token TEXT,
                                is_admin INTEGER,
                                updated_at DATETIME,
                                created_at DATETIME)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                broker_client_id TEXT,
                                broker_name TXT,
                                symbol TEXT,
                                position_id INTEGER,
                                holding_id INTEGER,
                                quantity INTEGER,
                                price REAL,
                                order_type TEXT,
                                product_type TEXT,
                                status TEXT,
                                updated_at DATETIME,
                                created_at DATETIME,
                                FOREIGN KEY (user_id) REFERENCES users(id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS positions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                broker_client_id TEXT,
                                broker_name TXT,
                                symbol TEXT,
                                quantity INTEGER,
                                average_price REAL,
                                product_type TEXT,
                                created_at DATETIME,
                                updated_at DATETIME,
                                FOREIGN KEY (user_id) REFERENCES users(id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS holdings (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                broker_client_id TEXT,
                                broker_name TXT,
                                symbol TEXT,
                                quantity INTEGER,
                                average_price REAL,
                                updated_at DATETIME,
                                created_at DATETIME,
                                FOREIGN KEY (user_id) REFERENCES users(id))''')
        self.conn.commit()

    def create_user(self, broker_client_id: str, broker_name: str, api_key: str, api_secret: str, is_admin: int = 0):
        self.cursor.execute(
            '''SELECT COUNT(*) FROM users WHERE broker_client_id = ? AND broker_name = ?''', (broker_client_id, broker_name))

        user_exists = self.cursor.fetchone()[0]

        if user_exists:
            return {
                'error': True,
                'message': 'User already exists'
            }

        created_at = get_local_datetime()
        self.cursor.execute('''
                            INSERT INTO users (broker_client_id, broker_name, api_key, api_secret, is_admin, created_at) 
                            VALUES (?, ?, ?, ?, ?, ?)
                            ''',
                            (broker_client_id, broker_name, api_key, api_secret, is_admin, created_at))
        self.conn.commit()
        return {
            'error': False,
            'message': 'New user created'
        }

    def get_user(self, broker_client_id: str, broker_name: str):
        self.cursor.execute(
            '''SELECT * FROM users WHERE broker_client_id = ? AND broker_name = ?''', (broker_client_id, broker_name))

        user = self.cursor.fetchone()

        if user:
            columns = [column[0] for column in self.cursor.description]
            user_dict = dict(zip(columns, user))
            return {
                'error': False,
                'message': '',
                'data': user_dict
            }
        else:
            return {
                'error': True,
                'message': 'User does not exist',
                'data': {}
            }

    def get_all_users(self):
        self.cursor.execute('''SELECT * FROM users''')
        users = self.cursor.fetchall()

        if users:
            columns = [column[0] for column in self.cursor.description]
            users_list = [dict(zip(columns, user)) for user in users]
            return {
                'error': False,
                'message': '',
                'data': users_list
            }
        else:
            return {
                'error': True,
                'message': 'No users found',
                'data': []
            }

    def delete_user(self, broker_client_id: str, broker_name: str):
        self.cursor.execute('''
            SELECT COUNT(*) FROM users WHERE broker_client_id = ? AND broker_name = ?
        ''', (broker_client_id, broker_name))

        user_exists = self.cursor.fetchone()[0]

        if user_exists > 0:
            self.cursor.execute('''
                DELETE FROM users
                WHERE broker_client_id = ? AND broker_name = ?
            ''', (broker_client_id, broker_name))
            self.conn.commit()
            return {
                'error': False,
                'message': 'User deleted successfully.'
            }
        else:
            return {
                'error': True,
                'message': 'User with the given clientId and broker does not exist.'
            }

    def update_user_token(self, broker_client_id: str, broker_name: str, access_token: str):
        self.cursor.execute('''
          SELECT COUNT(*) FROM users WHERE broker_client_id = ? AND broker_name = ?
      ''', (broker_client_id, broker_name))

        user_exists = self.cursor.fetchone()[0]

        if user_exists > 0:
            time = get_local_datetime()
            self.cursor.execute('''
              UPDATE users
              SET access_token = ?, updated_at = ?             
              WHERE broker_client_id = ? AND broker_name = ?
          ''', (access_token, time, broker_client_id, broker_name))
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

    def create_order(self, user_id: int, symbol: str, quantity: int, price: float, order_type: str) -> Dict[str, Any]:
        created_at = get_local_datetime()
        self.cursor.execute('''
            INSERT INTO orders (user_id, symbol, quantity, price, order_type, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, symbol, quantity, price, order_type, 'open', created_at))
        self.conn.commit()
        return {'error': False, 'message': 'Order created successfully', 'order_id': self.cursor.lastrowid}

    def get_orders(self, user_id: int) -> Dict[str, Any]:
        self.cursor.execute(
            'SELECT * FROM orders WHERE user_id = ?', (user_id,))
        orders = self.cursor.fetchall()
        if orders:
            columns = [column[0] for column in self.cursor.description]
            orders_list = [dict(zip(columns, order)) for order in orders]
            return {'error': False, 'data': orders_list}
        return {'error': True, 'message': 'No orders found', 'data': []}

    def get_order(self, order_id: int) -> Dict[str, Any]:
        self.cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = self.cursor.fetchone()
        if order:
            columns = [column[0] for column in self.cursor.description]
            order_dict = dict(zip(columns, order))
            return {'error': False, 'data': order_dict}
        return {'error': True, 'message': 'Order not found', 'data': {}}

    def update_order(self, order_id: int, status: str) -> Dict[str, Any]:
        self.cursor.execute(
            'UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return {'error': False, 'message': 'Order updated successfully'}
        return {'error': True, 'message': 'Order not found or not updated'}

    def create_position(self, user_id: int, symbol: str, quantity: int, average_price: float) -> Dict[str, Any]:
        created_at = get_local_datetime()
        self.cursor.execute('''
            INSERT INTO positions (user_id, symbol, quantity, average_price, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, symbol, quantity, average_price, created_at))
        self.conn.commit()
        return {'error': False, 'message': 'Position created successfully', 'position_id': self.cursor.lastrowid}

    def get_positions(self, user_id: int) -> Dict[str, Any]:
        self.cursor.execute(
            'SELECT * FROM positions WHERE user_id = ?', (user_id,))
        positions = self.cursor.fetchall()
        if positions:
            columns = [column[0] for column in self.cursor.description]
            positions_list = [dict(zip(columns, position))
                              for position in positions]
            return {'error': False, 'data': positions_list}
        return {'error': True, 'message': 'No positions found', 'data': []}

    def get_position(self, position_id: int) -> Dict[str, Any]:
        self.cursor.execute(
            'SELECT * FROM positions WHERE id = ?', (position_id,))
        position = self.cursor.fetchone()
        if position:
            columns = [column[0] for column in self.cursor.description]
            position_dict = dict(zip(columns, position))
            return {'error': False, 'data': position_dict}
        return {'error': True, 'message': 'Position not found', 'data': {}}

    def update_position(self, position_id: int, quantity: int, average_price: float) -> Dict[str, Any]:
        self.cursor.execute('UPDATE positions SET quantity = ?, average_price = ? WHERE id = ?',
                            (quantity, average_price, position_id))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return {'error': False, 'message': 'Position updated successfully'}
        return {'error': True, 'message': 'Position not found or not updated'}

    def get_holdings(self, user_id: int) -> Dict[str, Any]:
        self.cursor.execute(
            'SELECT * FROM holdings WHERE user_id = ?', (user_id,))
        holdings = self.cursor.fetchall()
        if holdings:
            columns = [column[0] for column in self.cursor.description]
            holdings_list = [dict(zip(columns, holding))
                             for holding in holdings]
            return {'error': False, 'data': holdings_list}
        return {'error': True, 'message': 'No holdings found', 'data': []}

    def get_holding(self, holding_id: int) -> Dict[str, Any]:
        self.cursor.execute(
            'SELECT * FROM holdings WHERE id = ?', (holding_id,))
        holding = self.cursor.fetchone()
        if holding:
            columns = [column[0] for column in self.cursor.description]
            holding_dict = dict(zip(columns, holding))
            return {'error': False, 'data': holding_dict}
        return {'error': True, 'message': 'Holding not found', 'data': {}}

    def close(self):
        self.conn.close()


sqlite_db = Sqlite()
