import os
import re
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyMuPDFLoader

def load_documents(data_directory: str):
    """
    Scans a directory recursively for files, loads them, and extracts the text.
    Currently configured to load all PDFs using PyMuPDFLoader.
    """
    if not os.path.exists(data_directory):
        raise FileNotFoundError(f"The directory {data_directory} does not exist.")
        
    print(f"Scanning '{data_directory}' for documents...")
    
    # 1. Initialize the DirectoryLoader
    # glob="**/*.pdf" ensures it searches recursively inside any subfolders too.
    loader = DirectoryLoader(
        path=data_directory,
        glob="**/*.pdf", 
        loader_cls=PyMuPDFLoader,
        show_progress=True 
    )
    
    # 2. Load all documents at once
    docs = loader.load()
    
    # 3. Apply the post-processing fix to remove awkward line breaks
    for doc in docs:
        doc.page_content = re.sub(r'(?<!\n)\n(?!\n)', ' ', doc.page_content)
            
    print(f"Successfully loaded {len(docs)} total document pages.")
    return docs

