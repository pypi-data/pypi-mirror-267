from chaiverse.config import FEED_ENDPOINT
from chaiverse.http_client import SubmitterClient
from chaiverse.lib.now import utcnow

def get_feed(limit, end_time=None):
    if end_time is None:
        end_time = int(utcnow().timestamp())
    client = SubmitterClient()
    params = {"end_time": end_time, "limit": limit}
    feed = client.get(endpoint=FEED_ENDPOINT, params=params)
    return feed
