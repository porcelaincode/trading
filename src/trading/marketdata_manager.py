# market_data_manager.py
from database import sqlite
from broker import ZerodhaKite, IciciBreeze, KotakNeo


class MarketDataManager:
    def __init__(self):
        self.broker_clients = {
            'zerodha': ZerodhaKite(),
            'icici_direct': IciciBreeze(),
            'kotak_neo': KotakNeo()
        }
        self.active_broker = None
        self.db = sqlite
        self.create_tables()

    def create_tables(self):
        with self.db:
            self.db.execute('''CREATE TABLE IF NOT EXISTS subscribed_instruments (
                tradingSymbol TEXT PRIMARY KEY,
                instrumentToken TEXT,
                segment TEXT
            )''')

    def switch_broker(self, broker_name):
        self.active_broker = self.broker_clients[broker_name]

    def subscribe_instrument(self, instrument):
        with self.db:
            self.db.execute('''INSERT OR REPLACE INTO subscribed_instruments (tradingSymbol, instrumentToken, segment)
                               VALUES (?, ?, ?)''', (instrument['tradingSymbol'], instrument['instrumentToken'], instrument['segment']))
        if self.active_broker:
            self.active_broker.subscribe([instrument])

    def unsubscribe_instrument(self, instrument):
        with self.db:
            self.db.execute(
                '''DELETE FROM subscribed_instruments WHERE tradingSymbol = ?''', (instrument['tradingSymbol'],))
        if self.active_broker:
            self.active_broker.unsubscribe([instrument])

    def get_subscribed_instruments(self):
        with self.db:
            return self.db.execute('SELECT tradingSymbol, instrumentToken, segment FROM subscribed_instruments').fetchall()

    async def get_market_data(self):
        if self.active_broker:
            return await self.active_broker.get_market_data()
