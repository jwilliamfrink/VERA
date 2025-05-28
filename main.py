# main.py

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