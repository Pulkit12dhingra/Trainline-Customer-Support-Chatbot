import streamlit as st
import time
import json
import ollama
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

# Load intents from intents.json
def load_intents():
    """Load intents.json and convert them into retrievable text format."""
    try:
        with open("data/intents.json", "r") as file:
            data = json.load(file)
        
        intents_text = []
        intent_lookup = {}  # Dictionary for quick lookup

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                response = intent["responses"][0]  # Use the first response for now
                intents_text.append(Document(page_content=f"Pattern: {pattern}\nResponse: {response}"))
                intent_lookup[pattern.lower()] = response  # Store for direct lookup

        return intents_text, intent_lookup
    except Exception as e:
        st.error(f"Error loading intents.json: {e}")
        return [], {}

# Load intents
intent_docs, intent_lookup = load_intents()

# Load train-related intents from train_Data.json
def load_train_intents():
    """Load train_Data.json and convert them into retrievable text format."""
    try:
        with open("data/train_Data.json", "r") as file:
            data = json.load(file)
        
        train_intents_text = []
        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                response = intent["responses"][0]  # Use the first response
                train_intents_text.append(Document(page_content=f"Pattern: {pattern}\nResponse: {response}"))
        
        return train_intents_text
    except Exception as e:
        st.error(f"Error loading train_Data.json: {e}")
        return []

# Load and process both content.txt, intents.json, and train_Data.json into FAISS
@st.cache_resource
def load_faiss_index():
    """Loads text data from content.txt, intents.json, and train_Data.json, chunks it, embeds it, and stores it in FAISS."""
    try:
        # Load content.txt
        loader = TextLoader("data/content.txt")
        documents = loader.load()

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)

        # Load train-related intents
        train_intents_docs = load_train_intents()

        # Combine all sources
        all_docs = docs + intent_docs + train_intents_docs

        # Create embeddings using Hugging Face
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Store in FAISS for retrieval
        vectorstore = FAISS.from_documents(all_docs, embeddings)

        return vectorstore.as_retriever()
    except Exception as e:
        st.error(f"Error loading FAISS index: {e}")
        return None

# Load the FAISS retriever (runs once to cache)
retriever = load_faiss_index()

# Stream text output
def stream_Data(text, delay: float = 0.05):
    """Yields words with a delay for smooth streaming."""
    for word in text.split():
        yield word + " "
        time.sleep(delay)

# Function to check for direct intent matches
def check_intents(user_input):
    """Checks if the user's query matches any predefined intents and returns a response."""
    user_input_lower = user_input.lower()
    for pattern, response in intent_lookup.items():
        if pattern in user_input_lower:
            return response
    return None

# Streamlit UI
st.title("🔍 RAG Chatbot (General Chat + Train Queries)")

# Initial bot message
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False

if not st.session_state.conversation_started:
    with st.chat_message("assistant"):
        st.write("Hi... how can I help you today?")
    st.session_state.conversation_started = True

# User input
prompt = st.chat_input("Chat with the bot...")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    # Check for predefined intent matches first
    intent_response = check_intents(prompt)

    if intent_response:
        # Respond using predefined intents
        with st.chat_message("assistant"):
            st.write(stream_Data(intent_response))
    else:
        # Retrieve relevant documents for train-related queries
        if retriever:
            relevant_docs = retriever.get_relevant_documents(prompt)
            context = "\n\n".join([doc.page_content for doc in relevant_docs])

            # Construct query with retrieved context
            full_prompt = f"Context: {context}\n\nUser: {prompt}\n\nAnswer:"

            # Send query to TinyLlama in Ollama
            with st.spinner("Processing..."):
                result = ollama.chat(model="tinyllama", messages=[{"role": "user", "content": full_prompt}])
                response = result["message"]["content"]

                # Display response
                with st.chat_message("assistant"):
                    st.write(stream_Data(response))
