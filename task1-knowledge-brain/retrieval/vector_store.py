import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STORAGE_FILE = "documents_store.json"

def chunk_text(text, chunk_size=400, overlap=40):
    lines = text.split("\n")
    chunks = []
    current_chunk = []
    current_length = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        current_chunk.append(line)
        current_length += len(line)
        if current_length >= chunk_size:
            chunks.append("\n".join(current_chunk))
            current_chunk = current_chunk[-1:]
            current_length = len(current_chunk[0])
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    return chunks

def index_articles(articles):
    all_chunks = []
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                all_chunks = json.load(f)
        except Exception:
            all_chunks = []

    for art in articles:
        chunks = chunk_text(art["content"])
        img_info = art["images"][0]["url"] if art.get("images") else ""
        for idx, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{art['url']}#chunk_{idx}",
                "content": chunk,
                "title": art["title"],
                "url": art["url"],
                "image_url": img_info
            })

    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

def search_knowledge(query_text, n_results=3):
    if not os.path.exists(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data:
        return []

    corpus = [item["content"] for item in data]
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
        query_vec = vectorizer.transform([query_text])
        scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    except Exception:
        return []

    top_indices = scores.argsort()[-n_results:][::-1]
    results = []
    for idx in top_indices:
        if scores[idx] > 0.05:
            results.append({
                "content": data[idx]["content"],
                "title": data[idx]["title"],
                "url": data[idx]["url"],
                "image_url": data[idx].get("image_url", ""),
                "score": float(scores[idx])
            })
    return results