# backend/redis_cache.py
# import redis
# import json

# r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# def save_message(session_id: str, role: str, message: str):
#     key = f"chat:{session_id}"
#     chat = r.get(key)
#     messages = json.loads(chat) if chat else []
#     messages.append({"role": role, "text": message})
#     r.setex(key, 3600, json.dumps(messages))  # 1 hour TTL

# def get_history(session_id: str):
#     key = f"chat:{session_id}"
#     chat = r.get(key)
#     return json.loads(chat) if chat else []

# def clear_history(session_id: str):
#     r.delete(f"chat:{session_id}")


import redis
import json
import os
from dotenv import load_dotenv
import datetime
load_dotenv()
# Load from environment or paste directly for now
REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Save a message
def save_message(session_id, sender, message):
    key = f"chat:{session_id}"
    entry = json.dumps({
    "sender": sender,
    "message": message,
     "time": datetime.datetime.utcnow().isoformat()
    })
    redis_client.rpush(key, entry)
    redis_client.expire(key, 86400)  # TTL: 1 day

# Get full chat history
def get_history(session_id):
    key = f"chat:{session_id}"
    entries = redis_client.lrange(key, 0, -1)
    return [json.loads(entry) for entry in entries]

# Clear chat history
def clear_history(session_id):
    key = f"chat:{session_id}"
    redis_client.delete(key)
