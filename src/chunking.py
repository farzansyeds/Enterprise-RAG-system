from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

def chunk_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Splits large documents into smaller chunks for the Vector Database.
    """
    print(f"Splitting documents into chunks of {chunk_size} characters...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        # This tells the splitter to try splitting by paragraphs first, then sentences, then words
        separators=["\n\n", "\n", " ", ""] 
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    return chunks