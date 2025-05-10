import requests
from dotenv import load_dotenv
import datetime
import os
load_dotenv()

JINA_API_URL = os.getenv("JINA_API_URL")
JINA_API_KEY = os.getenv("JINA_API_KEY")

def get_embedding(text: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JINA_API_KEY}"
    }
    data = {
        "model": "jina-embeddings-v2-base-en",  
        "input": [{"text": text}]
    }
    
    try:
        response = requests.post(JINA_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["data"][0]["embedding"]
    except Exception as e:
        print(f"Embedding error: {e}")
        return None
