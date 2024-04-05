from flask import Flask, request
from redis import Redis
from dotenv import load_dotenv

import time
import os

app = Flask(__name__)

load_dotenv()

redis_client = Redis(host=os.environ["HOST"],
                     port=os.environ["PORT"],
                     db=os.environ["DB"],
                     password=os.environ["PASSWORD"])

# We allow 2 requests per minute
MAX_REQUESTS = 2
WINDOW_SIZE = 60


@app.post("/api/tweets")
def create_tweet():
    data = request.get_json()
    user_id = data["user_id"]
    timestamp = int(time.time())
    request_id = f"{request.method} {request.url} {timestamp}"

    with redis_client.pipeline() as pipeline:
        pipeline.zremrangebyscore(user_id, 0, timestamp - WINDOW_SIZE)
        pipeline.zadd(user_id, {request_id: timestamp})
        pipeline.zcard(user_id)
        res = pipeline.execute()
    set_size = res[2]
    if set_size <= MAX_REQUESTS:
        return "REQUEST ACCEPTED!"
    return "REQUEST REFUSED!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
