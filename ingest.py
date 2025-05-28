# ingest.py

from dotenv import load_dotenv
load_dotenv()

import json
from pathlib import Path
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
import os

# --- Config ---
DATA_PATH = Path("data/your_docs.json")
CHROMA_DIR = "db"

# --- Set your API key ---
os.environ["OPENAI_API_KEY"] = "your-key-here"  # Or set via environment

# --- Load data ---
with open(DATA_PATH, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# --- Convert to LangChain Documents ---
documents = [Document(page_content=entry["content"], metadata={"id": entry["id"]}) for entry in raw_data]

# --- Embed and store ---
embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents, embedding=embeddings, persist_directory=CHROMA_DIR)

vectordb.persist()
print(f"Ingested {len(documents)} documents into {CHROMA_DIR}")
