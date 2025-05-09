from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag_engine.vector_store import search  # assumes this returns a list of relevant texts
from rag_engine.llm import query_gemini     # your Gemini query function
from schema import ChatRequest, ChatResponse
import uuid
from redis_cache import save_message, get_history, clear_history
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/chat", response_model=ChatResponse)
# async def chat(req: ChatRequest):
#     # Step 1: Try to retrieve context
#     context_docs = search(req.message)  # this should return a list of strings (content chunks)

#     if context_docs:
#         context = "\n\n".join(context_docs)
#         prompt = f"""You are a helpful AI assistant. Try to answer using the following context from news articles.
# If the context doesn't help, you can still answer using your general knowledge.

# Context:
# {context}

# Question: {req.message}
# Answer:"""
#     else:
#         prompt = f"""You are a smart assistant. Answer the following question based on your knowledge.

# Question: {req.message}
# Answer:"""

#     # Step 4: Get response from Gemini
#     print("Prompt sent to Gemini:\n", prompt)

#     reply = await query_gemini(prompt)
#     return ChatResponse(reply=reply)

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    context_docs = search(req.message)

    if context_docs:
        context = "\n\n".join(context_docs)
        prompt = f"""You are a helpful AI assistant. Try to answer using the following context from news articles.
If the context doesn't help, you can still answer using your general knowledge.

Context:
{context}

Question: {req.message}
Answer:"""
    else:
        prompt = f"""You are a smart assistant. Answer the following question based on your knowledge.

Question: {req.message}
Answer:"""

    print("Prompt sent to Gemini:\n", prompt)

    reply = await query_gemini(prompt)

    # Save user + bot messages to Redis
    save_message(req.session_id, "user", req.message)
    save_message(req.session_id, "bot", reply)

    return ChatResponse(reply=reply)
@app.get("/history/{session_id}")
def history(session_id: str):
    return get_history(session_id)

@app.post("/reset/{session_id}")
def reset(session_id: str):
    clear_history(session_id)
    return {"message": "Session reset."}


@app.get("/session")
def new_session():
    return {"session_id": str(uuid.uuid4())}
@app.get("/ping")
def ping():
    return {"status": "ok"}
