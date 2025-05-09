# backend/rag_engine/vector_store.py

from .embedder import get_embedding
import uuid
import chromadb
from chromadb.config import Settings

from InstructorEmbedding import INSTRUCTOR



client = chromadb.PersistentClient(path="./chroma_store")

collection = client.get_or_create_collection(name="news_articles")
def retrieve_similar_docs(query: str, k: int = 5):
    embedding = get_embedding(query)  # Returns 768-dim
    results = collection.query(
        query_embeddings=[embedding],  # ✅ Use embedding, not query_texts
        n_results=k,
        include=["documents", "metadatas"]
    )
    return results["documents"][0], results["metadatas"][0]
from .embedder import get_embedding

def add_documents(documents_with_metadata):
    documents = [doc["content"] for doc in documents_with_metadata]
    metadatas = [doc["metadata"] for doc in documents_with_metadata]
    ids = [doc["metadata"]["id"] for doc in documents_with_metadata]
    embeddings = [get_embedding(doc["content"]) for doc in documents_with_metadata]
    print("Embedding shape (sample):", len(embeddings[0]))

    collection = client.get_or_create_collection("news_articles")
    collection.add(
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
        ids=ids
    )



# def add_documents(docs: list[str], metadatas: list[dict]):
#     embeddings = [get_embedding(doc) for doc in docs]
#     ids = [str(i) for i in range(len(docs))]
#     collection.add(documents=docs, metadatas=metadatas, embeddings=embeddings, ids=ids)

# def search(query: str, top_k=3):
#     from .embedder import get_embedding
#     embedder = INSTRUCTOR("hkunlp/instructor-base")
#     embedding = embedder.encode([[ "Represent the news query for retrieval:", query ]])[0]
#     # embedding = get_embedding(query)
#     results = collection.query(query_embeddings=[embedding], n_results=top_k)
#     return results["documents"][0]
def search(query: str, top_k=3):
    from .embedder import get_embedding
    embedding = get_embedding(query)
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    return results["documents"][0]
