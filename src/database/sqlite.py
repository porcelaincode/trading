# module imports
import sqlite3
import requests
from datetime import datetime

# project imports
from database.sqlite_base import SqliteBase
from database.mongo_base import MongoBase
from config import env


class Sqlite(SqliteBase):
    def __init__(self, db_name=env.DATABASE_URL):
        super().__init__()
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS instruments (
                                instrument_token INTEGER PRIMARY KEY,
                                exchange TEXT,
                                tradingsymbol TEXT,
                                name TEXT,
                                expiry DATE,
                                strike REAL,
                                tick_size REAL,
                                lot_size INTEGER,
                                instrument_type TEXT,
                                segment TEXT,
                                exchange_token TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                order_id TEXT PRIMARY KEY,
                                order_params TEXT,
                                consumer_key TEXT
                                status TEXT,
                                placed_at TIMESTAMP)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS active_positions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                client_id TEXT,
                                broker TXT,
                                symbol TEXT,
                                qty REAL,
                                entry_price REAL,
                                exit_price REAL,
                                status TEXT,
                                created_at TEXT,
                                closed_at TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS closed_positions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                position_id INTEGER,
                                client_id TEXT,
                                broker TXT,
                                symbol TEXT,
                                qty REAL,
                                entry_price REAL,
                                exit_price REAL,
                                status TEXT,
                                created_at TEXT,
                                closed_at TEXT
                                closed_at TIMESTAMP)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS options_greeks (
                                id INTEGER PRIMARY KEY,
                                tradingsymbol TEXT,
                                ltp REAL,
                                delta REAL,
                                gamma REAL,
                                theta REAL,
                                vega REAL,
                                rho REAL,
                                timestamp TIMESTAMP)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS subscriptions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                tradingsymbol TEXT,
                                subscribed_at TIMESTAMP,
                                broker TEXT,
                                status TEXT,
                                ltp_subscribed REAL,
                                ltp_unsubscribed REAL)''')

        self.conn.commit()

    def store_instruments(self):
        response = requests.get("http://api.kite.trade/instruments")
        instruments = response.text.split('\n')
        headers = instruments[0].split(',')
        for instrument in instruments[1:]:
            if instrument.strip():
                instrument_data = dict(zip(headers, instrument.split(',')))
                self.cursor.execute('''INSERT OR REPLACE INTO instruments VALUES (
                                        :instrument_token, :exchange, :tradingsymbol, :name, :expiry, :strike, 
                                        :tick_size, :lot_size, :instrument_type, :segment, :exchange_token)''',
                                    instrument_data)
        self.conn.commit()

    def store_order(self, order_id, order_params, status):
        self.cursor.execute('''INSERT INTO orders (order_id, order_params, status, placed_at)
                               VALUES (?, ?, ?, ?)''',
                            (order_id, str(order_params), status, datetime.now()))
        self.conn.commit()

    def today_stats(self):
        """
          abs_percentage: Absolute percentage (total profit/total capital invested) * 100 
          best_win: Best pnl % of trades executed today 
          total_trades: Total trades executed today
          peak_gpu_load: Peak GPU load during trading hours
          avg_gpu_load: Average GPU load during trading hours
          total_comp_time: Total computational time
          trade_sig_gen: Trades signal generation time
          scs_rate: Total Success Rate of Trades

          All values are rounded to 2 digits
        """

        data = {
            "abs_percentage": 0,
            "best_win": 0,
            "total_trades": 0,
            "peak_gpu_load": 0,
            "avg_gpu_load": 0,
            "total_comp_time": 0,
            "trade_sig_gen": 0,
            "scs_rate": 0
        }
        return data

    def create_backup(self, mongo: MongoBase):
        positions_data = []
        self.cursor.execute("SELECT * FROM closed_positions")
        closed_positions = self.cursor.fetchall()
        for position in closed_positions:
            position_data = {
                "id": position[0],
                "position_data": position[1],
                "closed_at": position[2]
            }
            positions_data.append(position_data)
        mongo.store_closed_position(positions_data)

        greeks_data = []
        self.cursor.execute("SELECT * FROM options_greeks")
        options_greeks = self.cursor.fetchall()
        for greek in options_greeks:
            greek_data = {
                "id": greek[0],
                "tradingsymbol": greek[1],
                "ltp": greek[2],
                "delta": greek[3],
                "gamma": greek[4],
                "theta": greek[5],
                "vega": greek[6],
                "rho": greek[7],
                "timestamp": greek[8]
            }
            greeks_data.append(greek_data)
        mongo.store_options_data(positions_data)

        orders_data = []
        self.cursor.execute("SELECT * FROM orders")
        orders = self.cursor.fetchall()
        for order in orders:
            order_data = {
                "order_id": order[0],
                "order_params": order[1],
                "status": order[2],
                "placed_at": order[3]
            }
            orders_data.append(order_data)
        mongo.store_orders(orders_data)

        self.cursor.execute("DELETE FROM closed_positions")
        self.cursor.execute("DELETE FROM options_greeks")
        self.cursor.execute("DELETE FROM orders")
        self.cursor.commit()

        self.close()

    def close(self):
        self.conn.close()

    def shutdown_cleanup(self):
        self.cursor.execute(f"DELETE FROM instruments")
        self.cursor.execute(f"DELETE FROM clients")
        self.cursor.commit()
