# Mini GenAI Projects

## Installation
1. Create virtual env -> python -m venv 'virtual env name'
2. Create requirements.txt -> Install all required libraries -> by 'pip install -r requirements.txt'
3. Create .env -> Mention all your API keys (OpenAI, Langchain, Groq)
4. Create .github file -> write '.env' there -> to avoid .env file to get uploaded in github.
5. NOTE : In Langchain, create new project, inside that project -> Create API key -> Copy that in your .env file and then also mention the LANGCHAIN_PROJECT = "project_name"

## Deploy your Apps using Streamlit:
1. After successfully running any of the below .py files, you can deploy this by below steps:
2. Create a Github repo.
3. Upload your .py and requirements.txt in the repo. Commit.
4. Now open streamlit.io (Streamlit cloud website) -> Create app -> Provide your app.py (name of your py file) and click Deploy.
5. Once you click deploy, it will open your website that anyone can access. And you can use that to showcase your projects.

## Deploy your Apps with Huggingface Spaces:
1. After successfully running any of the below .py files, you can deploy this by below steps:
2. Create a Github repo.
3. Upload your .py and requirements.txt in the repo. Commit.
4. Open Huggingface Spaces -> Create space -> give a name -> add the required info and create. 
5. Search 'github actions huggingface' -> Copy the yaml code.
6. Create .github/workflows/main.yaml file in your github repo. 
7. Paste that code -> In last line run: -> Replace HF_USERNAME and SPACE_NAME with your huggingface username and Space repo name respectively. 
8. Ensure to add '--force' at the last of that last line of code. 
9. Go to Settings of Github Repo -> Secrets and Variables -> Actions -> Add secret key -> Name - HF_TOKEN and give the HF access key in there and save. 
10. Then commit all of your codes and then in Actions tab of Github repo -> CI-CD pipeline will start executing. 
11. If it's successful, then go to your HF repo, and you will find an error for Readme file. 
12. Go to that Readme file and edit -> Enter the correct details as per the fields provided there and commit your HF repo. 
13. Copy that edited README code and copy paste in your Github Readme file. 
14. Then when the CI CD pipeline runs again, then your HF repo App will start running your .py website.
NOTE : Ensure you main .py file name is app.py. 


# Projects :

## Using OpenAI -> app.py:
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

## Using Ollama -> app1.py :
1. gemma3:270m -> model I installed in my local machine for running ollama (As ollama is a local llm)
2. Create app1.py
3. Use the above same code for Ollama also -> Just replace the OpenAI model with Ollama model.
4. To run -> streamlit app1.py


## RagBot -> Upload PDF and ask questions -> ragbot.py
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


## Youtube Summarizer -> youtube_sum.py 
This script builds a Streamlit application that extracts text content from either a **YouTube video transcript** or a **standard website URL**, then uses LangChain and a **Groq-hosted Llama 3.3 model** to generate a concise summary.

1. Streamlit Page Configuration & Headers
* `st.set_page_config(page_title="...", page_icon="🦜")`: Configures the browser tab's title and favicon icon.
* `st.title("🦜 LangChain: Summarize Text From YT or Website")`: Displays the main header title on the webpage.
* `st.subheader('Summarize URL')`: Adds a secondary sub-heading right below the title.

2. User Input Elements
* `with st.sidebar:`: Groups the following input widget inside the left-hand sidebar layout.
* `groq_api_key=st.text_input("Groq API Key", type="password")`: Creates a masked password field in the sidebar for the user to input their Groq API token securely.
* `generic_url=st.text_input("URL", label_visibility="collapsed")`: Renders a clean text input box on the main page for the user to paste the target URL, hiding its descriptive label for a cleaner UI.

3. LLM Setup & Prompt Engineering
* `llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)`: Initializes the Groq LLM client using the powerful `llama-3.3-70b-versatile` model.
* `prompt_template="... Content:{text}"`: Defines a raw string instructing the LLM to write a 300-word summary using `{text}` as a dynamic placeholder.
* `prompt=PromptTemplate(template=prompt_template, input_variables=["text"])`: Wraps the raw string into a formal LangChain `PromptTemplate` object that safely handles variable insertion.

4. Form Validation & Triggering
* `if st.button("Summarize the Content from YT or Website"):`: Creates a clickable button. The code block beneath it executes only when clicked.
* `if not groq_api_key.strip() or not generic_url.strip():`: Field validation to check if the user left either the API key or the URL input completely empty.
* `elif not validators.url(generic_url):`: Uses the `validators` library to confirm that the text entered by the user is actually formatted as a valid web link.

5. Smart Data Loading (YouTube vs. Web Scraping)
* `with st.spinner("Waiting..."):`: Displays an animated loading wheel while the background extraction and LLM tasks are running.
* `if "youtube.com" in generic_url:`: Checks if the URL points to a YouTube video.
* `loader=YoutubeLoader.from_youtube_url(...)`: If it is a YouTube link, LangChain fetches and parses the video's automated or manual transcript/subtitles.
* `else: loader=UnstructuredURLLoader(...)`: If it is a normal webpage, it leverages an unstructured scraper (mimicking a realistic Mac Chrome browser agent header to prevent getting blocked by basic anti-bot scripts).
* `docs=loader.load()`: Executes the selected loader and converts the raw extracted text into clean LangChain Document objects.

6. Executing the Summarization Chain
* `chain=load_summarize_chain(llm, chain_type="stuff", prompt=prompt)`: Instantiates a pre-built LangChain summarization workflow. The `"stuff"` type means it takes all the fetched document text and feeds it into the prompt at once.
* `output_summary=chain.run(docs)`: Passes the loaded documents through the model to execute the summary request.
* `st.success(output_summary)`: Displays the resulting text in a green success banner on the UI.
* `except Exception as e: st.exception(f"Exception:{e}")`: A fail-safe block that catches any runtime breakdown (e.g., restricted video transcripts, network timeouts) and safely prints the error stack trace on screen.


## Math Gen AI app -> math_gpt.py 
This script builds a Streamlit-based math and reasoning chatbot. It uses a LangChain agent to dynamically switch between three tools: a **Wikipedia Searcher**, an **LLM-backed Calculator**, and a custom **Logical Reasoning Chain**, all powered by the **Groq Llama 3.3 model**.

1. App Configuration & API Key Guardrails
* `st.set_page_config(page_title="...", page_icon="🧮")`: Sets the application's browser tab title and favicon.
* `st.title("Text To Math Problem Solver Using Google Gemma 2")`: Displays the primary heading on the UI.
* `groq_api_key=st.sidebar.text_input(label="Groq API Key", type="password")`: Securely grabs the Groq API key via a password-style sidebar input.
* `if not groq_api_key:`: Check if the key field is empty.
* `st.info(...)` & `st.stop()`: Displays an informational banner asking for the key and halts further execution of the script to prevent code crashes.

2. LLM Initialization
* `llm=ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)`: Connects to the Groq API using the high-performing `llama-3.3-70b-versatile` model instance.

3. Tool Setup (Wikipedia & Calculator)
* `wikipedia_wrapper=WikipediaAPIWrapper()`: Connects to the Wikipedia API framework.
* `wikipedia_tool=Tool(...)`: Packages the Wikipedia wrapper into a standard LangChain tool with a clear description so the agent knows when to use it for data queries.
* `math_chain=LLMMathChain.from_llm(llm=llm)`: Sets up a specialized LangChain utility that translates natural language math questions into exact mathematical expressions.
* `calculator = StructuredTool.from_function(...)`: Converts the math chain into an agent tool named `"Calculator"`, explicitly telling the agent to only pass standard math equations to it.

4. Custom Reasoning Tool Setup
* `prompt="..."`: Defines a structured template instructing the LLM to logically break down and solve math problems step-by-step.
* `prompt_template=PromptTemplate(...)`: Converts the raw string into a LangChain `PromptTemplate` parsing object.
* `chain=LLMChain(llm=llm, prompt=prompt_template)`: Pairs the LLM with the custom logical prompt template.
* `reasoning_tool = StructuredTool.from_function(...)`: Wraps this logic chain into a tool named `"Reasoning Tool"`, giving the agent a fallback strategy for deep word-problem parsing.

5. Multi-Tool Agent Config & Chat History
* `assistant_agent=initialize_agent(...)`: Binds the three tools (`Wikipedia`, `Calculator`, `Reasoning Tool`) to the LLM. It relies on the `ZERO_SHOT_REACT_DESCRIPTION` loop mechanism to choose the best tool per step.
* `if "messages" not in st.session_state:`: Verifies if a conversation log is already initialized for this browser session.
* `st.session_state["messages"]=[...]`: Initializes history with a greeting from the chatbot if it's a brand new session.
* `for msg in st.session_state.messages:`: Iterates over the running history array.
* `st.chat_message(msg["role"]).write(msg['content'])`: Loops and draws previous user/assistant chats out on screen to keep the UI persistent.

6. Main Interaction UI & Execution
* `question=st.text_area("Enter your question:", "...")`: Renders a multiline text box pre-loaded with a complex word problem involving fruits as a placeholder example.
* `if st.button("Find my Answer"):`: Watches for a user click to trigger calculations.
* `if question:`: Validates that the input text area isn't blank.
* `st.session_state.messages.append(...)` & `st.chat_message("user").write(question)`: Adds the user's question to the session state log and prints it onto the active UI screen.
* `st_cb=StreamlitCallbackHandler(...)`: Hooks directly into Streamlit to print an expandable box showing the agent's real-time inner thoughts and tool lookups.
* `response=assistant_agent.run(...)`: Dispatches the full conversation history to the agent to extract the solution.
* `st.session_state.messages.append(...)`: Saves the agent's final generated calculation text into the history log.
* `st.write('### Response:')` & `st.success(response)`: Prints a formatted markdown header and presents the final answer in a neat green response banner.
* `else: st.warning("Please enter the question")`: Throws a warning message alert if the user clicked the button on an empty input field.


## HuggingFace Integration -> huggingface_int.py
* Same Youtube summarizer using Huggingface Endpoint instead of Groq -> only the llm is changed to HF. 
* It's currently not supporting for HF models for direct text-generation. So, output you will not get.


## PDF Q&A using AstraDB -> pdfquery.ipynb
1. Login to Astra.Datastax -> Create database (whichever free) -> Generate token and Copy endpoint -> Paste those in ASTRA_TOKEN & ASTRA_EP in .env file.
2. Follow below code summary:
* Loading PDF:
PdfReader('pdfs/confident.pdf'): Initializes the PDF reader object by pointing it to the local file path (pdfs/confident.pdf) and preparing it for text extraction.
* Raw Text Extraction Loop:
from typing_extensions import Concatenate: Imports a typing utility (not strictly required for the execution logic here).
raw_text = '': Initializes an empty string variable to serve as the master accumulator for the entire document's text content.
for i, page in enumerate(pdfreader.pages):: Iterates through every individual page structure stored within the loaded PDF file sequentially.
content = page.extract_text(): Triggers the text extraction method on the current page to parse out structural characters into a standard Python string.
if content: raw_text += content: Performs a safety check to ensure text characters were successfully returned, then appends the extracted page content to the raw_text variable.
* LLM and Embedding Model Initialization:
llm = Ollama(model = "llama3.2:1b"): Instructs the local Ollama service to instantiate the lightweight, 1-billion-parameter Llama 3.2 generative language model for text synthesis.
embedding = OllamaEmbeddings(model="llama3.2:1b"): Instantiates the vector embedding factory from the same Llama 3.2 model backend to map textual words into numerical vector spaces.
* Connecting to AstraDB Vector Store
from langchain_astradb import AstraDBVectorStore: Imports the official integration class to connect LangChain structures directly to DataStax AstraDB.
load_dotenv(): Scans the project directory for a hidden .env file and safely populates its content into the system's active environment variables.
import os: Imports Python's built-in OS module to read environment strings.
astra_vector_store = AstraDBVectorStore(...): Connects to your cloud database instance. It provisions or binds to a table named my_chat_tablee1, passing along your model credentials (API Endpoint and Token) and declaring the local Ollama configuration as its vector conversion engine.
* Splitting Text into Chunk Components:
from langchain_classic.text_splitter import CharacterTextSplitter: Imports the structural token control framework to subdivide massive continuous documents.
text_splitter = CharacterTextSplitter(...): Configures a rule-based text splitter object. It breaks text wherever a newline character (\n) occurs, aiming for structural windows of roughly 800 characters per block while intentionally overlapping neighboring chunks by 200 characters to preserve contextual transitions.
texts = text_splitter.split_text(raw_text): Converts the singular, long raw_text string into an indexed Python list containing multiple smaller text chunks.
* Vector Database Upsertion :
astra_vector_store.add_texts(texts[:50]): Takes up to the first 50 sliced text chunks, streams them through the local Ollama embedding mechanism to generate high-dimensional vector representations, and pushes those vector records to AstraDB.
astra_vector_index = VectorStoreIndexWrapper(...): Packs the raw cloud vector database pipeline inside an optimized LangChain query wrapper class, making automated semantic search and context retrieval seamless.
* Conversational RAG Loop (Interactive Querying):
while True:: Enters a persistent, looping terminal prompt state to allow uninterrupted questioning.
query_text = input(...).strip(): Grabs user inputs from the interactive prompt line and safely trims off empty padding spaces.
if query_text.lower() == "quit": break: Evaluates terminal exits cleanly when the user explicitly requests to close the session.
answer = astra_vector_index.query(query_text, llm=llm): Executes the actual RAG operation under the hood:
Vectorizes the user's string query using your local embedding settings.
Runs a semantic similarity calculation over the database contents to extract relevant matching context chunks.
Composes an instructional prompt combining the user's question with those relevant context chunks.
Feeds that combined text payload into your local Llama 3.2 instance to generate an accurate, verified textual answer.
astra_vector_store.similarity_search_with_score(query_text, k=4): Performs a direct semantic lookup across the vector indices to return the top 4 matching document chunks (k=4) alongside their relative mathematical distance/similarity coefficients.


