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



from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    return model.encode(text).tolist()


# from sentence_transformers import SentenceTransformer

# _model = None

# def get_embedding(text: str):
#     global _model
#     if _model is None:
#         _model = SentenceTransformer("all-MiniLM-L6-v2")
#     return _model.encode(text).tolist()

