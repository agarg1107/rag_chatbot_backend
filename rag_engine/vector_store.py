import os
import uuid
import requests
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "rag_vectors_db"


JINA_API_KEY = os.getenv("JINA_API_KEY") 
JINA_MODEL = "jina-embeddings-v2-base-en"  
JINA_ENDPOINT = "https://api.jina.ai/v1/embeddings"

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# Ensure collection exists
if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )

def get_embedding(text: str):
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": JINA_MODEL,
        "input": [{"text": text}]
    }
    try:
        response = requests.post(JINA_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]
    except Exception as e:
        print(f"[ERROR] Embedding failed: {e}")
        return [0.0] * 768  # fallback vector to avoid crash

def retrieve_similar_docs(query: str, k: int = 5):
    embedding = get_embedding(query)
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=k
    )
    return [hit.payload["content"] for hit in hits], [hit.payload for hit in hits]

def add_documents(documents_with_metadata):
    points = []
    for doc in documents_with_metadata:
        vector = get_embedding(doc["content"])
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "content": doc["content"],
                    **doc["metadata"]
                }
            )
        )
    print("Embedding shape (sample):", len(points[0].vector))
    client.upsert(collection_name=COLLECTION_NAME, points=points)

def search(query: str, top_k=3):
    embedding = get_embedding(query)
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=top_k
    )
    return [hit.payload["content"] for hit in hits]

