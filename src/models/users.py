from pymongo import IndexModel, ASCENDING, DESCENDING
from ..database import mongo_db as db

# Define the schemas for the collections

# accounts collection schema
db.accounts.create_index([("user_id", ASCENDING)], unique=True)
# Schema: { "user_id": ObjectId, "name": string, "balance": float, "account_type": string }

# agents collection schema (configuration of an agent that can trade with anti-bias settings)
db.agents.create_index([("agent_id", ASCENDING)], unique=True)
# Schema: { "agent_id": ObjectId, "strategy": string, "anti_bias": boolean, "parameters": dict }

# broadcasts collection schema (trading signal broadcasts, possibly empty as per the image)
db.broadcasts.create_index([("signal_id", ASCENDING)], unique=True)
# Schema: { "signal_id": ObjectId, "timestamp": datetime, "message": string, "users_notified": list }

# engine_performance collection schema (tracks performance data of trading algorithms)
db.engine_performance.create_index([("engine_id", ASCENDING)])
# Schema: { "engine_id": ObjectId, "timestamp": datetime, "performance_metrics": dict }

# instruments collection schema (tracks available financial instruments)
db.instruments.create_index([("instrument_id", ASCENDING)], unique=True)
# Schema: { "instrument_id": ObjectId, "symbol": string, "type": string, "price": float }

# margin_ledger collection schema (tracks margin balances for each user)
db.margin_ledger.create_index([("ledger_id", ASCENDING)], unique=True)
# Schema: { "ledger_id": ObjectId, "user_id": ObjectId, "balance": float, "timestamp": datetime }

# orders collection schema (tracks buy/sell orders placed by users)
db.orders.create_index([("order_id", ASCENDING)], unique=True)
# Schema: { "order_id": ObjectId, "user_id": ObjectId, "instrument_id": ObjectId, "quantity": int, "price": float, "status": string, "timestamp": datetime }

# positions collection schema (tracks current positions of users)
db.positions.create_index([("position_id", ASCENDING)], unique=True)
# Schema: { "position_id": ObjectId, "user_id": ObjectId, "instrument_id": ObjectId, "quantity": int, "avg_price": float, "timestamp": datetime }

# signals collection schema (stores trading signals)
db.signals.create_index([("signal_id", ASCENDING)], unique=True)
# Schema: { "signal_id": ObjectId, "type": string, "data": dict, "timestamp": datetime }

# ticks collection schema (stores market tick data for instruments)
db.ticks.create_index([("tick_id", ASCENDING)], unique=True)
# Schema: { "tick_id": ObjectId, "instrument_id": ObjectId, "price": float, "volume": int, "timestamp": datetime }

# users collection schema (tracks user data)
db.users.create_index([("user_id", ASCENDING)], unique=True)
# Schema: { "user_id": ObjectId, "name": string, "email": string, "password_hash": string, "created_at": datetime }

