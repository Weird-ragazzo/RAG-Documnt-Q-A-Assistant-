#!/usr/bin/env python3
"""
Streamlit Web Interface for RAG Chatbot
"""
import os
import streamlit as st
from dotenv import load_dotenv
from loguru import logger
import sys

from src.rag_chatbot import RAGChatbot
from src.document_loader import DocumentLoader

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO")

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot - AI Document Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Area */
    .main {
        background-color: #1a1a1a;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }
    
    /* Typography Hierarchy */
    h1 {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 2rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
    }
    
    h3 {
        color: #000000 !important;
        font-weight: 500 !important;
        font-size: 1.25rem !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #dee2e6;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2 {
        color: #212529 !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #212529 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #495057 !important;
        font-size: 0.875rem !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: #dee2e6 !important;
        margin: 1rem 0 !important;
    }
    
    /* Sidebar Buttons */
    [data-testid="stSidebar"] .stButton button {
        background-color: #0d6efd;
        color: white !important;
        border: none;
        border-radius: 4px;
        font-weight: 500;
        font-size: 0.875rem;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #0b5ed7;
    }
    
    [data-testid="stSidebar"] .stButton button p {
        color: white !important;
        margin: 0 !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border: 1px dashed #ced4da;
        border-radius: 4px;
        padding: 1rem;
    }
    
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small {
        color: #495057 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background-color: #2a2a2a;
        border: 1px dashed #555;
    }
    
    [data-testid="stSidebar"] [data-testid="stFileUploader"] label,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] p,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] span,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] small,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] button {
        color: #ffffff !important;
    }
    
    /* Alerts in Sidebar */
    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background-color: #d1e7dd !important;
        border: 1px solid #badbcc !important;
        border-radius: 4px;
        padding: 0.75rem !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stAlert"] p {
        color: #0f5132 !important;
        font-size: 0.875rem !important;
        margin: 0 !important;
    }
    
    /* Warning in Sidebar */
    [data-testid="stSidebar"] [data-testid="stNotification"][kind="warning"] {
        background-color: #fff3cd !important;
        border: 1px solid #ffecb5 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stNotification"][kind="warning"] p {
        color: #664d03 !important;
    }
    
    /* Expander in Sidebar */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 4px;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary p {
        color: #495057 !important;
        font-size: 0.875rem !important;
    }
    
    /* Slider */
    [data-testid="stSidebar"] .stSlider label {
        color: #495057 !important;
        font-size: 0.875rem !important;
    }
    
    /* Checkbox */
    [data-testid="stSidebar"] .stCheckbox label {
        color: #495057 !important;
        font-size: 0.875rem !important;
    }
    
    /* Chat Messages - Dark Backgrounds */
    [data-testid="stChatMessage"] {
        border-radius: 8px;
        padding: 1.25rem;
        margin: 0.75rem 0;
    }
    
    /* User Messages - Dark Blue */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #2d3748 !important;
        border: 1px solid #4a5568;
    }
    
    /* Assistant Messages - Dark */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background-color: #1e2530 !important;
        border: 1px solid #3a4556;
    }
    
    /* All text in chat white */
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] code {
        color: #ffffff !important;
    }
    
    [data-testid="stChatMessage"] strong {
        color: #ffffff !important;
    }
    
    [data-testid="stChatMessage"] a {
        color: #60a5fa !important;
    }
    
    /* Chat Input */
    [data-testid="stChatInput"] {
        border-radius: 8px;
    }
    
    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        background-color: #2d3748 !important;
        border: 1px solid #4a5568 !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: #9ca3af !important;
    }
    
    /* Source Box */
    .source-box {
        background-color: #374151;
        padding: 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
        border-left: 3px solid #fbbf24;
    }
    
    .source-box,
    .source-box p,
    .source-box span,
    .source-box strong,
    .source-box small {
        color: #ffffff !important;
    }
    
    /* Main Content Expander */
    .main [data-testid="stExpander"] {
        background-color: #2d3748;
        border: 1px solid #4a5568;
        border-radius: 4px;
        margin-top: 0.5rem;
    }
    
    .main [data-testid="stExpander"] summary p {
        color: #ffffff !important;
        font-weight: 500;
        font-size: 0.875rem;
    }
    
    /* Alerts in Main */
    .main [data-testid="stAlert"] {
        border-radius: 4px;
        padding: 1rem;
    }
    
    /* Caption */
    .stCaption {
        color: #e0e0e0 !important;
        font-size: 0.875rem !important;
    }
    
    .main .stCaption {
        color: #b0b0b0 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a1a1a1;
    }
    
    /* Sidebar collapse button fix */
    [data-testid="collapsedControl"] {
        top: 1rem;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def initialize_chatbot():
    """Initialize chatbot (cached to avoid reloading)"""
    load_dotenv()
    
    api_key = os.getenv('NVIDIA_API_KEY')
    api_url = os.getenv('NVIDIA_API_URL')
    model_name = os.getenv('NVIDIA_MODEL', 'openai/gpt-oss-20b')
    
    if not api_key or not api_url:
        st.error("❌ Missing NVIDIA API credentials in .env file")
        st.stop()
    
    try:
        chatbot = RAGChatbot(
            nvidia_api_key=api_key,
            nvidia_api_url=api_url,
            model_name=model_name
        )
        
        # Try to load existing index
        if os.path.exists("indices/chatbot_index.index"):
            logger.info("Loading existing index...")
            chatbot.load_index("indices/chatbot_index")
            return chatbot, True
        else:
            return chatbot, False
            
    except Exception as e:
        st.error(f"❌ Error initializing chatbot: {e}")
        st.stop()

def load_documents_into_chatbot(chatbot):
    """Load documents from data/raw into chatbot"""
    loader = DocumentLoader(data_dir="data/raw")
    documents = loader.load_directory()
    
    if not documents:
        return False, "No documents found in data/raw/"
    
    chatbot.add_documents(documents)
    chatbot.save_index("indices/chatbot_index")
    
    return True, f"Loaded {len(documents)} document(s)"

def main():
    # Header
    st.title("RAG Chatbot")
    st.caption("Ask questions about your documents")
    
    # Initialize chatbot
    with st.spinner("🔄 Initializing chatbot..."):
        chatbot, index_loaded = initialize_chatbot()
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # Status
        if index_loaded:
            st.success(f"Index loaded: {len(chatbot.chunks)} chunks")
        else:
            st.warning("No documents indexed")
        
        st.divider()
        
        # Documents
        st.subheader("Documents")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload documents",
            type=['txt', 'pdf', 'docx', 'md'],
            accept_multiple_files=True,
            help="Upload PDF, DOCX, TXT, or MD files"
        )
        
        if uploaded_files:
            if st.button("Upload & Process", use_container_width=True):
                with st.spinner("Uploading and processing files..."):
                    try:
                        # Create data/raw directory if it doesn't exist
                        os.makedirs("data/raw", exist_ok=True)
                        
                        uploaded_count = 0
                        for uploaded_file in uploaded_files:
                            # Save file to data/raw
                            file_path = os.path.join("data/raw", uploaded_file.name)
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            uploaded_count += 1
                        
                        # Reload documents
                        success, message = load_documents_into_chatbot(chatbot)
                        if success:
                            st.success(f"✅ Uploaded {uploaded_count} file(s). {message}")
                            st.rerun()
                        else:
                            st.error(message)
                    except Exception as e:
                        st.error(f"❌ Error uploading files: {e}")
        
        if st.button("Reload Documents", use_container_width=True):
            with st.spinner("Loading documents..."):
                success, message = load_documents_into_chatbot(chatbot)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        if st.button("Clear All Documents", use_container_width=True, type="secondary"):
            if st.session_state.get('confirm_clear', False):
                # Delete all files in data/raw
                import shutil
                if os.path.exists("data/raw"):
                    for file in os.listdir("data/raw"):
                        if file != ".gitkeep":
                            os.remove(os.path.join("data/raw", file))
                
                # Delete index files
                if os.path.exists("indices/chatbot_index.index"):
                    os.remove("indices/chatbot_index.index")
                if os.path.exists("indices/chatbot_index.meta"):
                    os.remove("indices/chatbot_index.meta")
                
                # Clear the cached chatbot
                st.cache_resource.clear()
                
                st.session_state.confirm_clear = False
                st.success("All documents cleared!")
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm deletion")
        
        # Document info
        if hasattr(chatbot, 'metadata') and chatbot.metadata:
            sources = list(set([m['source'] for m in chatbot.metadata]))
            st.caption(f"{len(sources)} document(s) loaded")
            with st.expander("View documents"):
                for source in sources:
                    st.text(f"{source}")
        
        st.divider()
        
        # Settings
        st.subheader("Retrieval")
        top_k = st.slider("Number of relevant chunks", 1, 10, 3)
        show_sources = st.checkbox("Show sources", value=True)
        
        st.divider()
        
        # Clear chat button
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        
        # Tips
        st.caption("Supported: PDF, DOCX, TXT, MD")
    
    # Check if documents are loaded
    if not hasattr(chatbot, 'chunks') or len(chatbot.chunks) == 0:
        st.info("Upload documents using the sidebar to get started.")
        return
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display sources if available
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("View Sources"):
                    for idx, source in enumerate(message["sources"], 1):
                        st.markdown(f"**{idx}.** {source['source']}")
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    result = chatbot.chat(prompt, top_k=top_k, show_sources=show_sources)
                    response = result['response']
                    
                    # Display response
                    st.markdown(response)
                    
                    # Display sources
                    if show_sources and result.get('sources'):
                        with st.expander("View Sources"):
                            for idx, source in enumerate(result['sources'], 1):
                                st.markdown(f"**{idx}.** {source['source']}")
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "sources": result.get('sources', [])
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    logger.error(f"Error in chat: {e}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

if __name__ == "__main__":
    main()
