# import streamlit as st
# from src.retriever import retrieve_relevant_chunks
# from src.generator import generate_rag_response

# st.set_page_config(page_title="Enterprise RAG System", page_icon="📚")
# st.title("📚 Enterprise RAG Assistant")
# st.markdown("Upload PDFs to the `data/` folder, run `python create_database.py`, and ask questions below.")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# if user_query := st.chat_input("Ask a question about your documents..."):
#     st.chat_message("user").markdown(user_query)
#     st.session_state.messages.append({"role": "user", "content": user_query})
    
#     with st.chat_message("assistant"):
#         with st.spinner("Searching documents and generating response..."):
#             try:
#                 relevant_docs = retrieve_relevant_chunks(user_query, top_k=3)
                
#                 if not relevant_docs:
#                     st.error("No relevant documents found in the database.")
#                 else:
#                     final_answer = generate_rag_response(user_query, relevant_docs)
#                     st.markdown(final_answer)
                    
#                     with st.expander("View Source Documents"):
#                         for i, (doc, score) in enumerate(relevant_docs):
#                             st.markdown(f"**Source {i+1} (Relevance: {score:.2f})**")
#                             st.info(doc.page_content)
                    
#                     st.session_state.messages.append({"role": "assistant", "content": final_answer})
#             except Exception as e:
#                 st.error(f"An error occurred: {e}")