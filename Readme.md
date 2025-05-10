# 🧠 RAG News Chatbot – Backend

This is the backend service for the RAG-powered news chatbot built using **FastAPI**. It handles chat sessions, query answering using Retrieval-Augmented Generation (RAG), and session management with **Redis**.

---

## 🧱 Tech Stack

* **Python 3.10.11**
* **FastAPI** – For API server
* **Redis** – For in-memory session history caching
* **Jina Embeddings API** – For semantic vector generation
* **Qdrant** – Vector database to store and search embeddings
* **Google Gemini API** – Final answer generation
* **Deployed on Render**

---

## ✨ Features

* RAG pipeline to combine document context with LLMs
* REST APIs to handle:

  * Chat (`POST /chat`)
  * Session creation (`GET /session`)
  * History retrieval (`GET /history/:session_id`)
  * Reset session (`POST /reset/:session_id`)
* Redis-based caching of session chat history
* Embedding + chunking of \~50 news articles
* Qdrant for fast top-k document retrieval

---
## 💤 Cold Start Notice (Render Free Tier)

This backend is hosted on the **free tier of Render**, which puts the server to sleep after periods of inactivity.

> 🕒 On your **first request**, you may notice a delay of **2–3 minutes** while the server “wakes up.”

You can check the loading status or pre-warm the backend by visiting:

👉 [https://rag-chatbot-backend-j4hg.onrender.com/](https://rag-chatbot-backend-j4hg.onrender.com/)

Once active, the chatbot will respond normally to queries via the frontend.

---
## ⚙️ Environment Variables

Make sure to define the following environment variables:

```bash
QDRANT_API_KEY=<your_qdrant_key>
JINA_API_KEY=<your_jina_api_key>
GOOGLE_GEMINI_API_KEY=<your_gemini_api_key>
REDIS_URL=redis://localhost:6379  # or your Render Redis instance
JINA_API_URL=https://api.jina.ai/v1/embeddings
QDRANT_URL=<your qdrant database>
```

---

## 🧪 Endpoints

| Endpoint                | Method | Description                          |
| ----------------------- | ------ | ------------------------------------ |
| `/session`              | GET    | Creates and returns a new session ID |
| `/chat`                 | POST   | Sends a query and returns a response |
| `/history/{session_id}` | GET    | Retrieves session history            |
| `/reset/{session_id}`   | POST   | Clears session chat                  |

---

## 🔌 How It Works

1. User sends query → `/chat`
2. Query is embedded using Jina API
3. Top-K similar document chunks retrieved from Qdrant
4. Gemini API is prompted with retrieved context + query
5. Response is stored in Redis (keyed by `session_id`)

---

## 🧠 Embeddings

* Using [`jina-embeddings-v2-base-en`](https://jina.ai/embeddings)
* Each news article is split into 500-character chunks with overlap
* Stored in Qdrant vector store with 768-dimensional embeddings

---

## 🔁 Caching & TTL Setup

Redis is used to cache session chat history for fast retrieval.

* Key format: `chat:{session_id}`
* TTL (Time-to-Live) for session history: **24 hours**

### How to configure TTLs:

```python
# Example TTL config during storage
redis.set(f"chat:{session_id}", json.dumps(data), ex=86400)  # 24 hours
```

### Optional Cache Warming:

* On startup, preload embeddings or hot articles to Qdrant (if needed)
* Could also prime Redis with FAQs or trending queries

---

## 📦 Setup Instructions

```bash
# Clone and install dependencies
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Set environment variables (or use .env file)

# Run the app
uvicorn main:app --reload
```

---

## 🌐 Deployment

Deployed using [Render](https://render.com/) free plan. Make sure to:

* Set environment variables under Render settings
* Add Redis and Qdrant services if needed

---

## 📬 Contact

For queries: [agarg1107@gmail.com](mailto:agarg1107@gmail.com)
