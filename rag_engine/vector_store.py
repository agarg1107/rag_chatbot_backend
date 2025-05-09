# # backend/rag_engine/vector_store.py

# from .embedder import get_embedding
# import uuid
# import chromadb
# from chromadb.config import Settings

# from InstructorEmbedding import INSTRUCTOR



# client = chromadb.PersistentClient(path="./chroma_store")

# collection = client.get_or_create_collection(name="news_articles")
# def retrieve_similar_docs(query: str, k: int = 5):
#     embedding = get_embedding(query)  # Returns 768-dim
#     results = collection.query(
#         query_embeddings=[embedding],  # ✅ Use embedding, not query_texts
#         n_results=k,
#         include=["documents", "metadatas"]
#     )
#     return results["documents"][0], results["metadatas"][0]
# from .embedder import get_embedding

# def add_documents(documents_with_metadata):
#     documents = [doc["content"] for doc in documents_with_metadata]
#     metadatas = [doc["metadata"] for doc in documents_with_metadata]
#     ids = [doc["metadata"]["id"] for doc in documents_with_metadata]
#     embeddings = [get_embedding(doc["content"]) for doc in documents_with_metadata]
#     print("Embedding shape (sample):", len(embeddings[0]))

#     collection = client.get_or_create_collection("news_articles")
#     collection.add(
#         documents=documents,
#         metadatas=metadatas,
#         embeddings=embeddings,
#         ids=ids
#     )



# # def add_documents(docs: list[str], metadatas: list[dict]):
# #     embeddings = [get_embedding(doc) for doc in docs]
# #     ids = [str(i) for i in range(len(docs))]
# #     collection.add(documents=docs, metadatas=metadatas, embeddings=embeddings, ids=ids)

# # def search(query: str, top_k=3):
# #     from .embedder import get_embedding
# #     embedder = INSTRUCTOR("hkunlp/instructor-base")
# #     embedding = embedder.encode([[ "Represent the news query for retrieval:", query ]])[0]
# #     # embedding = get_embedding(query)
# #     results = collection.query(query_embeddings=[embedding], n_results=top_k)
# #     return results["documents"][0]
# def search(query: str, top_k=3):
#     from .embedder import get_embedding
#     embedding = get_embedding(query)
#     results = collection.query(query_embeddings=[embedding], n_results=top_k)
#     return results["documents"][0]


# backend/rag_engine/vector_store.py

import os
import uuid
from .embedder import get_embedding
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = "https://aaaff63f-5803-400f-95d6-7b687d5f0d6e.us-west-2-0.aws.cloud.qdrant.io:6333"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "rag_vectors_db"

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# Ensure collection exists
if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

def retrieve_similar_docs(query: str, k: int = 5):
    embedding = get_embedding(query)  # Returns 384-dim vector
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



# from qdrant_client import QdrantClient

# qdrant_client = QdrantClient(
#     url="https://aaaff63f-5803-400f-95d6-7b687d5f0d6e.us-west-2-0.aws.cloud.qdrant.io:6333", 
#     api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ysbvBq8YyN88qsnpkrG4LqBputn-k98rGG48pMhvLPs",
# )

# print(qdrant_client.get_collections())