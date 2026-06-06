import streamlit as st
from dotenv import load_dotenv
import os
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

## Langsmith Tracking

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

## Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user's question without any bullshit."),
    ("user", "Question: {question}")
])

def generate_response(question, api_key, llm, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({'question': question})
    return answer


## Title of the app
st.title("Chatbot with Langchain and OpenAI")

## Sidebar
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

## Dropdown to select the model
llm = st.sidebar.selectbox("Select OpenAI Model", ["gpt-3.5-turbo", "gpt-4"])

## Adjust response parameters
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)

## User input
st.write("Ask a question to the OpenAI:")
user_question = st.text_input("Ask a question:")

if user_question:
    response = generate_response(user_question, api_key, llm, temperature, max_tokens)
    st.write(response)
elif user_question:
    st.warning("Please enter your OpenAI API key in the sidebar to get a response.")
else:
    st.write("Please enter a question to get a response.")