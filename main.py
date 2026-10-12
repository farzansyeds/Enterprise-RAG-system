from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from fastapi.staticfiles import StaticFiles

# Import your existing logic
from src.document_loader import load_documents
from src.chunking import chunk_documents
from src.retriever import retrieve_relevant_chunks
from src.generator import generate_rag_response
from langchain_chroma import Chroma
#from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
#import torch

app = FastAPI()

# Allow React to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
CHROMA_PATH = "vector_store"
os.makedirs(DATA_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    question: str

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    # 1. Save file
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Process and Vectorize
    raw_docs = load_documents(DATA_DIR)
    chunks = chunk_documents(raw_docs)
    
    #device = 'cuda' if torch.cuda.is_available() else 'cpu'
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
       # model_kwargs={'device': device}
    )
    
    Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH)
    return {"message": f"Successfully indexed {file.filename}"}

@app.post("/api/chat")
def chat_with_document(request: QueryRequest):
    relevant_docs = retrieve_relevant_chunks(request.question, top_k=3)
    if not relevant_docs:
        return {"answer": "No relevant context found.", "sources": []}
    
    answer = generate_rag_response(request.question, relevant_docs)
    sources = [{"content": doc.page_content, "score": score} for doc, score in relevant_docs]
    
    return {"answer": answer, "sources": sources}

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")