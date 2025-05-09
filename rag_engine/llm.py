import os
import httpx
import json
from rag_engine.vector_store import retrieve_similar_docs
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": GEMINI_API_KEY
}

async def query_gemini(user_query: str) -> str:
    context_docs, _ = retrieve_similar_docs(user_query, k=5)
    context = "\n".join(context_docs)

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"""You are a helpful assistant. You may use the following context if it is relevant.
If the context doesn't contain enough details, answer based on your general knowledge

Context:
{context}

Question: {user_query}
Answer in clear and concise language. If the answer is not in the context, say "I don’t know."""
                    }
                ]
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_URL, headers=headers, json=payload)
        data = response.json()
        print("GEMINI RAW RESPONSE:", data)

        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            raise ValueError(f"Gemini error: {data}")
