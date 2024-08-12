# module imports
from pymongo import MongoClient

# project imports
from database.mongo_base import MongoBase

from app_config import env


class MongoDb(MongoBase):
    def __init__(self, db_name=env.MONGODB_DATABASE, uri=env.MONGODB_URL):
        super().__init__()
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.create_collections()

    def create_collections(self):
        self.db.create_collection(
            "users", capped=True, size=5242880, max=5000, check_exists=True)
        self.db.create_collection(
            "trades", capped=True, size=5242880, max=5000, check_exists=True)
        self.db.create_collection(
            "options_data", capped=True, size=5242880, max=5000, check_exists=True)
        self.db.create_collection(
            "closed_positions", capped=True, size=5242880, max=5000, check_exists=True)
        self.db.create_collection(
            "orders", capped=True, size=5242880, max=5000, check_exists=True)

    def store_trade(self, trade_data):
        self.db.trades.insert_many(trade_data)

    def store_users(self, users_data):
        self.db.users.insert_many(users_data)

    def store_options_data(self, options_data):
        self.db.options_data.insert_many(options_data)

    def store_closed_position(self, position_data):
        self.db.closed_positions.insert_many(position_data)

    def store_orders(self, order_data):
        self.db.orders.insert_many(order_data)

    def get_trade_pnl_between_dates(self, start_date, end_date):
        trades = self.db.trades.find(
            {"closed_at": {"$gte": start_date, "$lte": end_date}})
        total_pnl = 0.0
        total_percentage_pnl = 0.0
        for trade in trades:
            total_pnl += trade["pnl"]
            total_percentage_pnl += trade["percentage_pnl"]
        return total_pnl, total_percentage_pnl

    def get_options_data_between_dates(self, start_date, end_date):
        options_data = self.db.options_data.find(
            {"timestamp": {"$gte": start_date, "$lte": end_date}})
        return list(options_data)

    def get_closed_positions_between_dates(self, start_date, end_date):
        closed_positions = self.db.closed_positions.find(
            {"closed_at": {"$gte": start_date, "$lte": end_date}})
        return list(closed_positions)

    def get_orders_between_dates(self, start_date, end_date):
        orders = self.db.orders.find(
            {"placed_at": {"$gte": start_date, "$lte": end_date}})
        return list(orders)

    def transfer_data_from_sqlite(self):
        # sqlite_db = Sqlite()
        # sqlite_db.create_backup(mongo=self)
        pass

    def close(self):
        self.client.close()
