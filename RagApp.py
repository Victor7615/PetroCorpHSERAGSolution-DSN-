import streamlit as st
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# --- Page Configuration ---
st.set_page_config(
    page_title="Global PetroCorp Compliance Assistant",
    page_icon="⛽",
    layout="wide"
)

# --- Load Environment Variables & Secrets ---
load_dotenv()

def get_secret(key):
    """Fetches a secret from environment variables or Streamlit's secrets manager."""
    val = os.getenv(key)
    if val:
        return val
    try:
        return st.secrets[key]
    except (FileNotFoundError, KeyError):
        return None

# --- Azure Service Configuration ---
AZURE_OPENAI_ENDPOINT = get_secret("OPEN_AI_ENDPOINT")
AZURE_OPENAI_KEY = get_secret("OPEN_AI_KEY")
AZURE_OPENAI_CHAT_DEPLOYMENT = get_secret("CHAT_MODEL")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = get_secret("EMBEDDING_MODEL")

AZURE_SEARCH_ENDPOINT = get_secret("SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = get_secret("SEARCH_KEY")
AZURE_SEARCH_INDEX = get_secret("INDEX_NAME")

# --- Verify Configuration ---
missing_keys = [k for k, v in locals().items() if k.startswith("AZURE_") and v is None]
if missing_keys:
    st.error(f"🚨 Critical Error: The following configurations are missing: {', '.join(missing_keys)}. Please set them in your .env file or Streamlit secrets.")
    st.stop()

# --- Initialize Azure Clients (Cached for performance) ---
@st.cache_resource
def get_azure_clients():
    """Initializes and returns the Azure OpenAI and AI Search clients."""
    try:
        openai_client = AzureOpenAI(
            api_version="2024-02-01",
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY
        )
        search_credential = AzureKeyCredential(AZURE_SEARCH_KEY)
        search_client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=AZURE_SEARCH_INDEX,
            credential=search_credential
        )
        return openai_client, search_client
    except Exception as e:
        st.error(f"🚨 Failed to initialize Azure clients: {e}")
        st.stop()

openai_client, search_client = get_azure_clients()

# --- RAG Orchestration Function ---
def get_rag_response(question):
    """Orchestrates the RAG process: embed, search, and generate."""
    try:
        # 1. Embed the user's question using the OpenAI client
        embedding = openai_client.embeddings.create(
            model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
            input=question
        )
        query_vector = embedding.data[0].embedding

        # 2. Search Azure AI Search for relevant documents
        # NEW CODE
        search_results = search_client.search(
        search_text="",
        vector_queries=[{"kind": "vector", "vector": query_vector, "k": 3, "fields": "contentVector"}],
        select=["content"]
        )
        #search_results = search_client.search(
           # search_text="",  # Use vector search primarily
           # vector_queries=[{"vector": query_vector, "k": 3, "fields": "contentVector"}],
           # select=["content"] # Select the field containing the text chunk
        #)

        # 3. Combine search results into a single context string
        context = " ".join([result["content"] for result in search_results])

        if not context:
            return "I couldn't find any relevant information in the knowledge base to answer your question."

        # 4. Build the prompt for the chat model
        system_prompt = f"""
        You are "HSE Assist," a specialized AI assistant for PetroSafe Global Holdings. Your primary purpose is to help all employees and contractors understand and comply with the company's Health, Safety, and Environment (HSE) policies and procedures. You are a supportive and knowledgeable resource designed to make safety information accessible and clear.

        1. Core Knowledge Base:
        Your primary source of truth is the PetroSafe Global Holdings HSE Policy, Document ID: PSG-HSE-POL-001. All your answers must be grounded in and consistent with the context provided below. If the context doesn't cover a topic, state that the specific information is not available in the policy and recommend contacting a human HSE supervisor.

        2. Interaction Style & Tone:
        Your tone must be supportive, clear, patient, and professional. Always prioritize safety. Reinforce the company's commitment to "zero harm." Base your answers directly on the text of the policy document provided in the context.

        3. Crucial Guardrails & Limitations:
        You do not approve permits, authorize work, or conduct risk assessments. Your role is to inform, not to authorize. If a user asks for permission, you must refuse and direct them to the proper human authority. If a query is unclear or describes a complex situation not explicitly covered in the policy, do not invent an answer; instead, direct the user to their supervisor. You are aware that the current date is August 16, 2025.

        CONTEXT:
        ---
        {context}
        ---
        """
        
        # 5. Generate the final answer using the chat model
        chat_completion = openai_client.chat.completions.create(
            model=AZURE_OPENAI_CHAT_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.1
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        st.error(f"An error occurred during the RAG process: {e}")
        return "Sorry, I encountered an error while processing your request."

# --- Streamlit Chat UI ---
st.title("Global PetroCorp Compliance Assistant ⚖️")
st.markdown("This assistant provides answers grounded in official corporate policy documents.")
# NEW UI initialization with disclaimer
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add the initial disclaimer message from the assistant
    disclaimer = "I am HSE Assist, your AI guide to the PetroSafe Global Holdings HSE Policy. My purpose is to provide information from this policy. I am not a substitute for professional judgment, on-site risk assessment, or your supervisor's direction. In any emergency, follow the established Emergency Response Plan and contact your supervisor immediately."
    st.session_state.messages.append({"role": "assistant", "content": disclaimer})


#if "messages" not in st.session_state:
    #st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a compliance question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            response = get_rag_response(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})