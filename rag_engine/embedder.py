from InstructorEmbedding import INSTRUCTOR

# Don't load at top-level
_model = None

def get_embedding(text: str):
    global _model
    if _model is None:
        _model = INSTRUCTOR("hkunlp/instructor-base")  # Load only once when first used
    instruction = "Represent the news article for retrieval:"
    return _model.encode([[instruction, text]])[0].tolist()
