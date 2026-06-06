import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_classic.vectorstores import FAISS
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
from langchain_community.document_loaders import PyPDFDirectoryLoader


from dotenv import load_dotenv
load_dotenv()

## load groq api key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.1-8b-instant", api_key=groq_api_key)

prompt= ChatPromptTemplate.from_messages({
    """
    Answer teh questions based on the provided context.
    Please provide the most accurate response based on the question.
    <context>
    {context}
    <context>
    Question: {input}
    """
})

def create_vector_embeddings():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = OllamaEmbeddings()   ## Use Ollama/OpenAI embeddings
        st.session_state.loader = PyPDFDirectoryLoader("pdfs")
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
    
user_prompt=st.text_input("Enter your question here")

if st.button("Document Embeddings"):
    create_vector_embeddings()
    st.success("Document embeddings created successfully!")

import time

if user_prompt:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    create_retrieval_chain(retriever, document_chain)
    
    start = time.process_time()
    response = document_chain.invoke({"input": user_prompt})
    print(f"Response time: {time.process_time() - start} seconds")

    st.write(response['answer'])

    ## Streamlit expander
    with st.expander("Document Similarity Search"):
        for i,doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write('----------------------')