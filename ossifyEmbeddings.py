import faiss
import pickle
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

# Config
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "vera"
COLLECTION_NAME = "ethics_documents"
FAISS_INDEX_PATH = "vera_index.faiss"
ID_MAP_PATH = "vera_id_map.pkl"

# Initialize clients
client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]
model = SentenceTransformer("all-MiniLM-L6-v2")

# Fetch and process documents
docs = []
ids = []
texts = []

for doc in collection.find({}, {"_id": 0, "id": 1, "contentBlocks": 1}):
    content_blocks = doc.get("contentBlocks", [])
    block_texts = []

    for block in content_blocks:
        excerpt = block.get("excerpt", "")
        rationale = block.get("rationale", "")
        notes = block.get("notes", "")
        block_texts.append(f"{excerpt} {rationale} {notes}".strip())

    full_text = " ".join(block_texts).strip()
    if full_text:
        ids.append(doc["id"])
        texts.append(full_text)

# Generate embeddings
embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

# Build and save FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)
faiss.write_index(index, FAISS_INDEX_PATH)

# Save ID mapping
with open(ID_MAP_PATH, "wb") as f:
    pickle.dump(ids, f)

print(f"Ossified {len(ids)} embeddings to '{FAISS_INDEX_PATH}' and ID map to '{ID_MAP_PATH}'.")