import feedparser
import requests
import uuid
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag_engine.vector_store import add_documents

def fetch_rss_articles(rss_url, limit=50):
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries[:limit]:
        link = entry.link
        content = fetch_article_text(link)
        if content:
            articles.append({"title": entry.title, "text": content})
    return articles

def fetch_article_text(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join(p.get_text() for p in paragraphs)
        return content[:5000] 
    except Exception as e:
        print(f"Failed to fetch article: {url} ({e})")
        return None

def chunk_with_splitter(text, chunk_size=500, overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)

def run_ingestion():
    rss_urls = [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.cnn.com/rss/edition.rss",
        "https://feeds.reuters.com/reuters/topNews",
        "https://www.aljazeera.com/xml/rss/all.xml"
    ]
    
    all_documents = []
    for rss_url in rss_urls:
        print(f"Ingesting from: {rss_url}")
        articles = fetch_rss_articles(rss_url)
        for article in articles:
            chunks = chunk_with_splitter(article["text"])
            for chunk in chunks:
                all_documents.append({
                    "content": chunk,
                    "metadata": {
                        "title": article["title"],
                        "id": str(uuid.uuid4())
                    }
                })

    print(f"Adding {len(all_documents)} chunks to Qdrant")
    add_documents(all_documents)


if __name__ == "__main__":
    run_ingestion()
