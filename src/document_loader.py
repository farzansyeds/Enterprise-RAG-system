import os
from langchain_community.document_loaders import PyPDFLoader

def load_documents(data_directory: str):
    """
    Scans a directory for PDF files, loads them, and extracts the text.
    """
    documents = []
    
    # Check if the directory exists
    if not os.path.exists(data_directory):
        raise FileNotFoundError(f"The directory {data_directory} does not exist.")
        
    print(f"Scanning '{data_directory}' for PDFs...")
    
    # Loop through all files in the directory
    for filename in os.listdir(data_directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(data_directory, filename)
            print(f"Loading: {filename}")
            
            # PyPDFLoader extracts the text page by page
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
            
    print(f"Successfully loaded {len(documents)} total pages.")
    return documents

# Quick test (Will only run if you execute this specific file)
if __name__ == "__main__":
    # Create a 'data' folder in your root directory and put a test PDF in it
    docs = load_documents("../data")