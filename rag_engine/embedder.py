# from InstructorEmbedding import INSTRUCTOR

# # Don't load at top-level
# _model = None

# def get_embedding(text: str):
#     global _model
#     if _model is None:
#         print("Loading INSTRUCTOR model...")
#         _model = INSTRUCTOR("hkunlp/instructor-base")
#     instruction = "Represent the news article for retrieval:"
#     return _model.encode([[instruction, text]])[0].tolist()



# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("intfloat/e5-small-v2")

# def get_embedding(text: str):
#     return model.encode(text).tolist()


# from sentence_transformers import SentenceTransformer

# _model = None

# def get_embedding(text: str):
#     global _model
#     if _model is None:
#         _model = SentenceTransformer("all-MiniLM-L6-v2")
#     return _model.encode(text).tolist()

import requests
from dotenv import load_dotenv
import datetime
load_dotenv()

JINA_API_URL = "https://api.jina.ai/v1/embeddings"
JINA_API_KEY = "jina_212b4a608f594063b5690eac1863f340UjUso8LTOqPdpglC4hXaSJqZGD0n"  # Replace with your actual key

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
