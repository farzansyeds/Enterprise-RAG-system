import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load the GOOGLE_API_KEY from .env
load_dotenv()

def get_llm():
    """
    Initializes the Google Gemini LLM.
    We use gemini-2.5-flash as it is highly capable and heavily featured in the free tier.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0.3 
    )
    return llm

def generate_rag_response(query: str, retrieved_docs: list):
    """
    Constructs a prompt using the retrieved context and generates an answer.
    """
    context_text = "\n\n---\n\n".join([doc.page_content for doc, score in retrieved_docs])
    
    template = """
    You are an expert technical assistant. Answer the question based ONLY on the provided context. 
    If the answer is not contained in the context, say "I cannot answer this based on the provided documents."
    Do not use outside knowledge.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    llm = get_llm()
    chain = prompt | llm
    
    print("Generating answer using Gemini...")
    response = chain.invoke({"context": context_text, "question": query})
    
    return response.content