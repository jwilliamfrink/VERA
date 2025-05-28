# ingest.py

import json
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document

# Load .env file
load_dotenv()

# --- Config ---
DATA_PATH = Path("data/veraSampleContext.json")
CHROMA_DIR = "db"

# --- Load data ---
with open(DATA_PATH, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# --- Build Documents from contentBlocks ---
documents = []
for entry in raw_data:
    for block in entry.get("contentBlocks", []):
        documents.append(
            Document(
                page_content=block["excerpt"],
                metadata={
                    "doc_id": entry["id"],
                    "block_id": block["id"],
                    "title": entry.get("title", ""),
                    "tags": ", ".join(entry.get("tags", [])),  # Flatten tag list
                    "type": entry.get("type", "")
                }
            )
        )

# --- Ingest into ChromaDB ---
embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents, embedding=embeddings, persist_directory=CHROMA_DIR)
vectordb.persist()

print(f"Ingested {len(documents)} blocks into {CHROMA_DIR}")