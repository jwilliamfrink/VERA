import faiss
import pickle
import os
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# === Clients ===

# OpenAI client
openai_client = OpenAI()  # uses OPENAI_API_KEY from environment

# MongoDB client
mongo_client = MongoClient("mongodb://localhost:27017")
collection = mongo_client["vera"]["ethics_documents"]

# Load FAISS index and ID map
index = faiss.read_index("vera_index.faiss")
with open("vera_id_map.pkl", "rb") as f:
    ids = pickle.load(f)

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# === Utility Functions ===

def build_context(docs):
    """Format context from contentBlocks for LLM input"""
    context_chunks = []
    for doc in docs:
        content_blocks = doc.get("contentBlocks", [])
        for block in content_blocks:
            excerpt = block.get("excerpt", "")
            rationale = block.get("rationale", "")
            notes = block.get("notes", "")
            combined = f"{excerpt} {rationale} {notes}".strip()
            if combined:
                context_chunks.append(combined)
    return "\n\n".join(context_chunks)

def ask_openai(context, question):
    """Send formatted context + question to OpenAI"""
    messages = [
        {"role": "system", "content": "You are a helpful assistant grounded in ethical principles."},
        {"role": "user", "content": f"Given the following context:\n\n{context}\n\nAnswer the question:\n{question}"}
    ]
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

# === Query Loop ===

while True:
    query = input("\nAsk a question (or 'exit'): ").strip()
    if query.lower() == "exit":
        break

    query_embedding = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_embedding, k=3)

    matched_docs = []
    for i in I[0]:
        doc_id = ids[i]
        doc = collection.find_one({"id": doc_id})
        if doc:
            matched_docs.append(doc)

    if matched_docs:
        context = build_context(matched_docs)
        answer = ask_openai(context, query)

        sources = []
        for doc in matched_docs:
            doc_id = doc.get("id", "unknown")
            title = doc.get("title", "Untitled")
            sources.append(f'{doc_id}, "{title}"')

        print("\n🧠 GPT Response:\n", answer)
        print("\n*Sources:", "; ".join(sources))
    else:
        print("No matching documents found.")
