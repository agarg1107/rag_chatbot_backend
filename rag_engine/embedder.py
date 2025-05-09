# backend/rag_engine/embedder.py
from InstructorEmbedding import INSTRUCTOR

model = INSTRUCTOR("hkunlp/instructor-base")

def get_embedding(text: str):
    instruction = "Represent the news article for retrieval:"
    return model.encode([[instruction, text]])[0].tolist()
