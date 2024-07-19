from datetime import datetime, timedelta, timezone

# Define IST timezone
IST = timezone(timedelta(hours=5, minutes=30))


def get_local_datetime():
    return datetime.now(IST)
