from langchain_chroma import Chroma
#from langchain_huggingface import HuggingFaceEmbeddings
import torch
from langchain_google_genai import GoogleGenerativeAIEmbeddings

CHROMA_PATH = "vector_store"

def get_vector_store():
    """
    Loads the persisted Chroma vector database from disk using GPU if available.
    """
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        model_kwargs={'device': device}  # Runs similarity encoding on GPU
    )
    
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    return db

def retrieve_relevant_chunks(query: str, top_k: int = 3):
    """
    Performs cosine similarity search against stored embeddings.
    Returns the top_k most relevant chunks.
    """
    db = get_vector_store()
    
    # similarity_search_with_relevance_scores returns both the document and similarity score
    results = db.similarity_search_with_relevance_scores(query, k=top_k)
    return results

if __name__ == "__main__":
    # Test query against your circular linked list PDF
    test_query = "What is a circular linked list?"
    print(f"Testing retrieval for: '{test_query}'\n")
    
    results = retrieve_relevant_chunks(test_query, top_k=2)
    for i, (doc, score) in enumerate(results):
        print(f"--- Result {i+1} (Score: {score:.4f}) ---")
        print(doc.page_content[:300] + "...\n")