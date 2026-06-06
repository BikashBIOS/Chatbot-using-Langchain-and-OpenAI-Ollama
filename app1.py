from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"] = os.getenv("LANGSMITH_TRACING")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


## Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user's question without any bullshit."),
    ("user", "Question: {question}")
])

## Generate response function
def generate_response(question, engine, temperature, max_tokens):
    llm = Ollama(model=engine)   
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({'question': question})
    return answer


## Title of the app
st.title("Chatbot with Langchain and Ollama")

## Dropdown to select the model
engine = st.sidebar.selectbox("Select Ollama Model", ["gemma3:270m"])

## Adjust response parameters
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)

## User input
st.write("Ask a question to the Ollama:")
user_question = st.text_input("Ask a question:")

if user_question:
    response = generate_response(user_question, engine, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please enter a question to get a response.")