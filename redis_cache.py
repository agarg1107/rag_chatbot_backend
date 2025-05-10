import redis
import json
import os
from dotenv import load_dotenv
import datetime
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def save_message(session_id, sender, message):
    key = f"chat:{session_id}"
    entry = json.dumps({
    "sender": sender,
    "message": message,
     "time": datetime.datetime.utcnow().isoformat()
    })
    redis_client.rpush(key, entry)
    redis_client.expire(key, 86400) 


def get_history(session_id):
    key = f"chat:{session_id}"
    entries = redis_client.lrange(key, 0, -1)
    return [json.loads(entry) for entry in entries]


def clear_history(session_id):
    key = f"chat:{session_id}"
    redis_client.delete(key)
