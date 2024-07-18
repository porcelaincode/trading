# module imports
from fastapi import logger
from datetime import datetime, timedelta

# project imports
from database import MongoDb

if __name__ == '__main__':
    backup_db = MongoDb()

    # Transfer data from SQLite to MongoDB
    backup_db.transfer_data_from_sqlite()

    start_date = datetime.now() - timedelta(days=1)
    end_date = datetime.now()

    logger.info("Trade PnL:", backup_db.get_trade_pnl_between_dates(
        start_date, end_date))
    logger.info("Options Data:", backup_db.get_options_data_between_dates(
        start_date, end_date))
    logger.info("Closed Positions:", backup_db.get_closed_positions_between_dates(
        start_date, end_date))
    logger.info("Orders:", backup_db.get_orders_between_dates(
        start_date, end_date))

    backup_db.close()
