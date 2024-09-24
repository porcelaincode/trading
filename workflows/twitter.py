import os
import requests
import requests_oauthlib
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("X_API_KEY")
api_secret_key = os.getenv("X_API_SECRET")
access_token = os.getenv("X_ACCESS_TOKEN")
access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("X_BEARER_TOKEN")

mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')

auth = requests_oauthlib.OAuth1(
    api_key,
    api_secret_key,
    access_token,
    access_token_secret
)

client = MongoClient(mongo_connection_string)
db = client['your_database_name']
collection = db['engine_performance']

latest_data = collection.find_one(sort=[('timestamp', -1)])

days_pl = (latest_data['net_profit'] / latest_data['initial_capital']) * 100
best_win = max(latest_data['trade_wins'], default=0)
total_trades = latest_data['total_trades']
peak_gpu_load = latest_data['peak_gpu_load']
avg_gpu_load = latest_data['avg_gpu_load']
computation_time = latest_data['total_computation_time']
signal_gen_time = latest_data['signal_generation_time']
success_rate = (latest_data['successful_trades'] / total_trades) * 100

tweet_text = (
    f"Days P&L: {days_pl:.2f}%\n"
    f"Best Win: {best_win}%\n"
    f"Total Trades: {total_trades}\n\n"
    f"Peak GPU Load: {peak_gpu_load:.2f}%\n"
    f"Average GPU Load: {avg_gpu_load:.2f}%\n"
    f"Total Computation Time: {computation_time:.2f}ms/tick\n"
    f"Trade Signal Generation: {signal_gen_time:.2f}ms\n"
    f"Success Rate: {success_rate:.2f}%"
)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {bearer_token}"
}

payload = {
    "text": tweet_text
}

response = requests.post(
    "https://api.twitter.com/2/tweets",
    headers=headers,
    json=payload,
    auth=auth
)

print(response.text)