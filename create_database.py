import os
from dotenv import load_dotenv
#from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
#import torch
from src.document_loader import load_documents
from src.chunking import chunk_documents

# Load the environment variables from your .env file
load_dotenv()

# Define where our data is and where we want to save the database
DATA_PATH = "data"
CHROMA_PATH = "vector_store"

def generate_data_store():
    """
    Executes the data ingestion pipeline: Load -> Chunk -> Embed -> Store.
    """
    # 1. Load the raw documents
    documents = load_documents(DATA_PATH)
    
    # 2. Split into chunks
    chunks = chunk_documents(documents)
    
    # 3. Initialize the Embedding Model
    # We use OpenAI's cost-effective and highly capable text-embedding-3-small model
    #device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("Initializing embedding model...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        #model_kwargs={'device': device}
    )
    
    # 4. Create and save the Vector Database
    print(f"Creating Chroma vector database at '{CHROMA_PATH}'...")
    
    # This function automatically creates embeddings for all chunks and saves them to disk
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print(f"✅ Success! Saved {len(chunks)} vectorized chunks to the '{CHROMA_PATH}' folder.")

if __name__ == "__main__":
    generate_data_store()