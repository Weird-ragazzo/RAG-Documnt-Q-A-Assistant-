# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot with a web interface. Upload documents and ask questions - the AI retrieves relevant content and generates accurate answers.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- **Document Upload**: Support for PDF, DOCX, TXT, and Markdown files
- **Semantic Search**: FAISS-powered vector search with sentence embeddings
- **AI Responses**: NVIDIA API integration for intelligent answers
- **Web Interface**: Clean Streamlit UI with dark theme
- **Source Tracking**: See which documents were used for each answer
- **Persistent Index**: Saves embeddings to disk for fast reload

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/rag-chatbot.git
cd rag-chatbot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Create your .env file from the example
cp .env.example .env

# Edit with your NVIDIA API credentials
nano .env  # or use any text editor
```



### 3. Run the Application

**Web Interface (Recommended):**
```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

**Command Line:**
```bash
python main.py
```

## Usage

1. **Upload Documents**: Use the sidebar to upload PDF, DOCX, TXT, or MD files
2. **Process**: Click "Upload & Process" to index the documents
3. **Ask Questions**: Type your question in the chat input
4. **View Sources**: Expand "View Sources" to see which documents were used

## Project Structure

```
rag-chatbot/
├── app.py                 # Streamlit web interface
├── main.py                # CLI interface
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── config/
│   └── config.yaml        # Configuration settings
├── src/
│   ├── rag_chatbot.py     # Main RAG logic
│   ├── document_loader.py # Document parsing
│   ├── embeddings.py      # Embedding generation
│   └── chunking.py        # Text chunking
├── data/
│   └── raw/               # Upload documents here
├── indices/               # Saved vector indices
└── logs/                  # Application logs
```

## Configuration

Edit `.env` or `config/config.yaml`:

| Variable | Description | Default |
|----------|-------------|---------|
| `NVIDIA_API_KEY` | Your NVIDIA API key | Required |
| `NVIDIA_API_URL` | API endpoint | NVIDIA chat completions |
| `NVIDIA_MODEL` | Model to use | openai/gpt-oss-20b |
| `CHUNK_SIZE` | Tokens per chunk | 500 |
| `CHUNK_OVERLAP` | Overlap between chunks | 50 |
| `TOP_K` | Number of results to retrieve | 3 |

## Tech Stack

- **Frontend**: Streamlit
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS
- **LLM**: NVIDIA API
- **Document Parsing**: PyPDF2, python-docx

## API Usage

```python
from src.rag_chatbot import RAGChatbot

# Initialize
chatbot = RAGChatbot(
    nvidia_api_key="your-key",
    nvidia_api_url="https://integrate.api.nvidia.com/v1/chat/completions",
    model_name="openai/gpt-oss-20b"
)

# Load documents
from src.document_loader import DocumentLoader
loader = DocumentLoader(data_dir="data/raw")
documents = loader.load_directory()
chatbot.add_documents(documents)

# Chat
result = chatbot.chat("What is this document about?")
print(result['response'])
```

## License

MIT
