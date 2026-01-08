#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from loguru import logger
import sys

from src.rag_chatbot import RAGChatbot
from src.document_loader import DocumentLoader

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/chatbot.log", rotation="500 MB", level="DEBUG")

def setup_chatbot():
    """Initialize and setup the chatbot"""
    # Load environment variables
    load_dotenv()
    
    # Get API credentials
    api_key = os.getenv('NVIDIA_API_KEY')
    api_url = os.getenv('NVIDIA_API_URL')
    model_name = os.getenv('NVIDIA_MODEL', 'openai/gpt-oss-20b')
    
    if not api_key or not api_url:
        logger.error("Missing NVIDIA API credentials in .env file")
        sys.exit(1)
    
    # Initialize chatbot
    chatbot = RAGChatbot(
        nvidia_api_key=api_key,
        nvidia_api_url=api_url,
        model_name=model_name
    )
    
    return chatbot

def load_documents(chatbot):
    """Load documents into the chatbot"""
    loader = DocumentLoader(data_dir="data/raw")
    
    # Load all documents from data/raw
    documents = loader.load_directory()
    
    if not documents:
        logger.warning("No documents found in data/raw/")
        return False
    
    # Add to chatbot
    chatbot.add_documents(documents)
    
    # Save index
    chatbot.save_index("indices/chatbot_index")
    
    return True

def interactive_chat(chatbot):
    """Run interactive chat session"""
    logger.info("Starting interactive chat. Type 'quit' to exit.")
    print("\n🤖 RAG Chatbot Ready! Ask me anything.\n")
    
    while True:
        try:
            query = input("You: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not query:
                continue
            
            # Get response
            result = chatbot.chat(query)
            
            print(f"\n🤖 Bot: {result['response']}\n")
            
            # Show sources
            if result.get('sources'):
                print("📚 Sources:")
                for src in result['sources']:
                    print(f"  • {src['source']}")
                print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}\n")

def main():
    """Main entry point"""
    chatbot = setup_chatbot()
    
    # Check if index exists
    if os.path.exists("indices/chatbot_index.index"):
        logger.info("Loading existing index...")
        try:
            chatbot.load_index("indices/chatbot_index")
        except Exception as e:
            logger.warning(f"Failed to load index: {e}")
            logger.info("Creating new index from documents...")
            if not load_documents(chatbot):
                logger.error("Failed to load documents. Add files to data/raw/")
                sys.exit(1)
    else:
        logger.info("No existing index found. Loading documents...")
        if not load_documents(chatbot):
            logger.error("Failed to load documents. Add files to data/raw/")
            sys.exit(1)
    
    # Start interactive chat
    interactive_chat(chatbot)

if __name__ == "__main__":
    main()