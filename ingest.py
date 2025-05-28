"""
SETUP INSTRUCTIONS

1. Install Requirements:
    Run from your project root (ideally inside a virtual environment):
        pip install -r requirements.txt

2. OpenAI API Access:
    - Requires an OpenAI account with API access enabled.
    - Pay-as-you-go billing is required (free-tier keys will not work).
    - Sign up and find your key at: https://platform.openai.com/account/api-keys

3. Store Your API Key:
    Create a `.env` file in the project root and add:
        OPENAI_API_KEY=sk-...
    ⚠️ Be sure `.env` is listed in your `.gitignore` so your key isn't exposed.

4. Source Document Format:
    - This script expects a JSON file (default: `data/veraSampleContext.json`) structured like:
        [
            {
                "id": "doc-001",
                "content": "Full text of the value statement or policy.",
                "tags": ["equity", "inclusion"]
            },
            ...
        ]

        - You can also refer to the example YAML data structure at: reference/veraContext.yaml

5. ▶Run Ingestion:
    From the project root:
        python3 ingest.py

    The script will:
    - ingest a structured set of values-aligned documents
    - Generate vector embeddings
    - Store results in ChromaDB (default path: `db/`)
"""

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