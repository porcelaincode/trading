# module imports
import requests
import requests_oauthlib
from app_config import env

# project imports
from database import Sqlite


def publish_tweet(text):
    auth = requests_oauthlib.OAuth1(
        env.TWITTER_API_KEY,
        env.TWITTER_API_SECRET_KEY,
        env.TWITTER_ACCESS_TOKEN,
        env.TWITTER_ACCESS_TOKEN_SECRET
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {env.TWITTER_BEARER_TOKEN}"
    }
    payload = {
        "text": text
    }

    response = requests.post(
        env.TWITTER_BASE_URL,
        headers=headers,
        json=payload,
        auth=auth
    )

    return response


if __name__ == '__main__':
    sqlite_db = Sqlite()
    stats = sqlite_db.today_stats()

    text = f"Days P&L: {stats['abs_percentage']}%\nBest Win: {stats['best_win']}%\nTotal Trades: {stats['total_trades']}\n\nPeak GPU Load: {stats['peak_gpu_load']}%\nAverage GPU Load: {stats['avg_gpu_load']}%\nTotal Computation Time: {stats['total_comp_time']}ms/tick\nTrade Signal Generation: {stats['trade_sig_gen']}ms\nSuccess Rate: {stats['scs_rate']}%"

    publish_tweet(text)
