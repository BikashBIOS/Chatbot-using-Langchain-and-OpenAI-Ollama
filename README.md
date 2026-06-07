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


## RagBot -> Upload PDF and ask questions
1. Defining the Prompt Template
What it does: Instructs the LLM on how to behave. It mandates strict reliance on the custom data provided inside the <context> blocks.

Document Ingestion and Vectorization :
2. This block runs only when a user clicks the ingestion button. It prepares the data for searching.
What it does: Declares an ingestion function. Streamlit reruns the whole script from top to bottom every time a user interacts with the UI. The if "vectors" not in st.session_state: condition ensures that expensive document parsing and vector calculations only happen once, saving memory and time by caching them inside Streamlit's state storage.
3. Initializes an Ollama embedding engine running on your local machine to calculate the mathematical representations of text.
4. Targets a local folder named pdfs and loads every single page of text contained within those files into an array of objects.
5. Configures a text-splitting rule. It will chop pages into sections of up to 1000 characters each. If a paragraph splits awkwardly, it uses an overlap of 200 characters to preserve context across the boundary.
6. Executes the chunking rule, taking the raw full-length PDF pages and chopping them down into hundreds of shorter documents.
7. Passes the text chunks to the embedding model, calculates their mathematical coordinates, and loads them into a fast-searching FAISS Vector Database stored in RAM.

The Streamlit UI Control Elements :
8. Renders an interactive input box on the webpage allowing users to type questions.
9. Renders a button. Clicking it executes the create_vector_embeddings() process outlined above, and prints a green success alert banner on screen when finished.

Execution and RAG Processing :
10. Combines your Groq LLM brain and your structured instructions template together. This chain knows exactly how to format context texts and questions into a unified string.
11. Converts the raw FAISS database into a functional Retriever object, enabling it to accept search strings and return the top matching text snippets.
12. Assembles the full operational pipeline. It coordinates capturing the query, pulling the context documents using the retriever, sending everything to the prompt, and piping it directly to the model.
13. Captures the starting timestamp, fires the query to the execution chain via .invoke(), tracks the end timestamp, and logs the generation time directly into your development terminal log.
14. Extracts the generated text from the JSON output payload and presents it neatly to the user on the screen.
15. Creates a collapsible accordion UI component. Clicking it opens up a list view showing the exact document fragments pulled from your local PDFs that were passed to the LLM to formulate the final response.

## Search Engine GenAI app (search your context based on Third parties using Tools & Agents) -> tools_search.py
This application builds an interactive chatbot using **Streamlit** for the frontend UI, **LangChain** for agent and tool management, and **Groq (Llama 3)** as the Large Language Model.
* To run this file -> streamlit tools_search.py -> Enter groq api key -> Then enter your query and search.

1. Tool Initialization (ArXiv, Wikipedia, & DuckDuckGo)
* `arxiv_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)`: Configures the ArXiv API tool to fetch only the top 1 result and limit the text content to 200 characters.
* `arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)`: Creates the executable ArXiv tool for the LangChain agent.
* `api_wrapper=WikipediaAPIWrapper(...)` & `wiki=...`: Configures and initializes the Wikipedia search tool with the same constraints (1 result, 200 characters max).
* `search=DuckDuckGoSearchRun(name="Search")`: Initializes a DuckDuckGo search tool to allow the agent to fetch live data from the web.

2. Streamlit UI & Sidebar Setup
* `st.title("🔎 LangChain - Chat with search")`: Sets the main heading of the web application.
* `st.sidebar.title("Settings")`: Adds a sidebar header named "Settings".
* `api_key=st.sidebar.text_input("...", type="password")`: Creates a secure password-style input field in the sidebar for the user to safely provide their Groq API key.

3. Session State & Chat History Management
* `if "messages" not in st.session_state:`: Checks if a chat history exists in the current browser session.
* `st.session_state["messages"] = [...]`: If no history exists, initializes it with a default greeting from the assistant.
* `for msg in st.session_state.messages:`: Loops through all previous messages stored in the session state.
* `st.chat_message(msg["role"]).write(msg['content'])`: Dynamically renders past messages on the screen, matching them to the correct UI bubble (user or assistant).

4. User Input Handling
* `if prompt:=st.chat_input(placeholder="..."):`: Displays a chat input box. If the user types a message and hits enter, it assigns that text to the variable `prompt`.
* `st.session_state.messages.append(...)`: Appends the new user message to the session state history to maintain context.
* `st.chat_message("user").write(prompt)`: Instantly renders the user's message in the chat UI.

5. LLM and Agent Initialization
* `llm=ChatGroq(..., model_name="Llama3-8b-8192", streaming=True)`: Initializes the Groq LLM client using the provided API key, selecting the Llama 3 (8B) model with streaming enabled.
* `tools=[search, arxiv, wiki]`: Bundles the search, ArXiv, and Wikipedia tools into a list for the agent to access.
* `search_agent=initialize_agent(...)`: Combines the tools and LLM into a LangChain agent. It uses `ZERO_SHOT_REACT_DESCRIPTION` (allowing the agent to decide which tool to use based solely on the tool's description) and enables error parsing handling.

6. Executing the Agent & Rendering Output
* `with st.chat_message("assistant"):`: Opens a UI container block designated for the chatbot's response.
* `st_cb=StreamlitCallbackHandler(...)`: Creates a callback handler that intercepts the agent's internal "Thought/Action/Observation" loop and prints it live in the UI.
* `response=search_agent.run(..., callbacks=[st_cb])`: Runs the agent by passing the entire conversation history, passing the callback handler to show the agent's live reasoning.
* `st.session_state.messages.append(...)`: Appends the final answer generated by the agent into the session state history.
* `st.write(response)`: Prints the final polished answer inside the assistant's chat bubble.