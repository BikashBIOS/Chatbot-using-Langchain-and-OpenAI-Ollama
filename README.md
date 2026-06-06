## Installation
1. Create virtual env -> python -m venv chatenv
2. Create requirements.txt -> Install all required libraries
3. Create .env -> Mention all your API keys (OpenAI, Langchain, Groq)
4. NOTE : In Langchain, create new project, inside that project -> Create API key -> Copy that in your .env file and then also mention the LANGCHAIN_PROJECT = "project_name"


## Using OpenAI :
1. Create app.py -> Write your code there
2. Prompt Template :
Uses LangChain’s ChatPromptTemplate to structure the conversation.
Defines a System Message to control the AI's persona/behavior and a User Message containing a dynamic placeholder {question}
3. The LLM Chain Logic (generate_response)
ChatOpenAI(model=llm): Initializes the connection to the chosen OpenAI model.
StrOutputParser(): A LangChain utility that extracts the clean, raw string response from the AI's raw message object.
LCEL (LangChain Expression Language): The code chain = prompt | llm | output_parser pipes the components together sequentially.
chain.invoke(): Triggers the execution of the pipeline by passing the user's question.
4. Streamlit UI Elements
The frontend UI is constructed cleanly using Streamlit's native components:
st.title(): Adds the main header to the webpage.
st.sidebar: Moves configuration inputs to a collapsable left panel.
text_input(..., type="password"): Securely masks the API key input.
selectbox(): Creates a dropdown menu for selecting between gpt-3.5-turbo and gpt-4.
slider(): Provides interactive sliders to adjust hyperparameters (temperature and max_tokens).
st.text_input(): Captures the user's textual query.
5. Application Control Flow (Logic Gate)
Checks if the user has typed a question and presses enter. If true, it invokes the backend logic and renders the final text response via st.write().
6. [User Input] ➔ [Prompt Template] ➔ [OpenAI Chat Model] ➔ [String Output Parser] ➔ [UI Screen Display]
                                              │
                                              └───> [Logs Sent to LangSmith Dashboard]
7. To run the app.py -> streamlit run app.py

## Using Ollama :
1. gemma3:270m -> model I installed in my local machine for running ollama (As ollama is a local llm)
2. Create app1.py
3. Use the above same code for Ollama also -> Just replace the OpenAI model with Ollama model.
4. To run -> streamlit app1.py
