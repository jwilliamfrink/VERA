"""
SETUP INSTRUCTIONS

1. Install Requirements:
    Run the following from your project root (preferably in a virtual environment):
        pip install -r requirements.txt

2. OpenAI API Access:
    - You'll need an OpenAI account with API access enabled.
    - A **Pay-as-you-go** account is sufficient. Free-tier API keys are not supported.
    - As of 2025, GPT-4-turbo or GPT-3.5-turbo are the recommended models. GPT-4-turbo is faster and supports longer context.
    - Billing info is required to activate the API: https://platform.openai.com/account/billing/overview

3. Environment Variables:
    Create a `.env` file in the project root with your OpenAI API key:
        OPENAI_API_KEY=sk-...
    ⚠️ Never commit your `.env` file to version control. Add it to `.gitignore`.

4. Running the App:
    You can launch the FastAPI server like this:
        nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
    Then open your browser at: http://localhost:8000


This script handles:
    - Web routing and templating
    - Receiving user queries
    - Passing those queries to the RAG pipeline
    - Returning value-grounded AI responses
"""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
api_key = os.getenv("OPENAI_API_KEY")

# --- Setup ---
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- RAG Chain Setup ---
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory="db", embedding_function=embeddings)
retriever = vectordb.as_retriever()
llm = ChatOpenAI(temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ask")
async def ask(query: str):
    response = qa_chain.run(query)
    if response.strip().lower() in ["i don't know.", "i don't know", ""]:
        response = llm.predict(query)
    return {"answer": response}