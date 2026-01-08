import numpy as np
import os
import faiss
import requests
import json
from typing import List, Dict, Tuple
from loguru import logger

from .chunking import TextChunker
from .embeddings import EmbeddingManager

class RAGChatbot:
    def __init__(self, nvidia_api_key: str, nvidia_api_url: str, 
                 model_name: str = "openai/gpt-oss-20b",
                 chunk_size: int = 500, chunk_overlap: int = 50):
        """Initialize RAG Chatbot"""
        self.nvidia_api_key = nvidia_api_key
        self.nvidia_api_url = nvidia_api_url
        self.model_name = model_name
        
        # Initialize components
        logger.info("Initializing RAG components...")
        self.chunker = TextChunker(chunk_size, chunk_overlap)
        self.embedder = EmbeddingManager()
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(self.embedder.embedding_dim)
        
        # Storage
        self.chunks = []
        self.metadata = []
        
        logger.info("RAG Chatbot initialized successfully!")
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """Add documents to the knowledge base"""
        logger.info(f"Processing {len(documents)} documents...")
        
        all_chunks = []
        all_metadata = []
        
        for doc_idx, doc in enumerate(documents):
            text = doc['text']
            source = doc.get('source', f'document_{doc_idx}')
            
            # Chunk the document
            chunks = self.chunker.chunk_by_tokens(text)
            logger.info(f"  {source}: {len(chunks)} chunks")
            
            # Store chunks and metadata
            for chunk_idx, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadata.append({
                    'source': source,
                    'chunk_id': chunk_idx,
                    'doc_id': doc_idx
                })
        
        # Generate embeddings in batch
        logger.info("Generating embeddings...")
        embeddings = self.embedder.embed_texts(all_chunks)
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store
        self.chunks.extend(all_chunks)
        self.metadata.extend(all_metadata)
        
        logger.info(f"Total chunks in knowledge base: {len(self.chunks)}")
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, Dict, float]]:
        """Retrieve most relevant chunks"""
        if len(self.chunks) == 0:
            logger.warning("No documents in knowledge base")
            return []
        
        # Embed query
        query_embedding = self.embedder.embed_query(query)
        
        # Search
        distances, indices = self.index.search(query_embedding, min(top_k, len(self.chunks)))
        
        # Collect results
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.chunks):
                results.append((
                    self.chunks[idx],
                    self.metadata[idx],
                    float(distance)
                ))
        
        return results
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate response using NVIDIA API"""
        prompt = f"""You are a helpful assistant. Answer the user's question based on the provided context.

Context:
{context}

Question: {query}

Answer the question based on the context above. If the context doesn't contain relevant information, say so."""

        headers = {
            "Authorization": f"Bearer {self.nvidia_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        try:
            response = requests.post(
                self.nvidia_api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            logger.error(f"NVIDIA API error: {e}")
            return f"Error calling NVIDIA API: {str(e)}"
    
    def chat(self, query: str, top_k: int = 3, show_sources: bool = True) -> Dict:
        """Main chat function"""
        # Retrieve
        retrieved = self.retrieve(query, top_k)
        
        if not retrieved:
            return {
                'response': "I don't have any relevant information to answer that.",
                'sources': []
            }
        
        # Build context
        context = "\n\n".join([chunk for chunk, _, _ in retrieved])
        
        # Generate
        response = self.generate_response(query, context)
        
        result = {'response': response}
        
        if show_sources:
            sources = []
            for chunk, meta, distance in retrieved:
                sources.append({
                    'source': meta['source'],
                    'chunk_id': meta['chunk_id'],
                    'relevance_score': float(distance),
                    'preview': chunk[:200] + '...' if len(chunk) > 200 else chunk
                })
            result['sources'] = sources
        
        return result
    
    def save_index(self, filepath: str):
        if len(self.chunks) == 0:
            logger.warning("No chunks to save. Skipping index save.")
            return
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
            
            faiss.write_index(self.index, f"{filepath}.index")
            
            with open(f"{filepath}.meta", 'w', encoding='utf-8') as f:
                json.dump({
                    'chunks': self.chunks,
                    'metadata': self.metadata
                }, f)
            
            logger.info(f"Index saved to {filepath} ({len(self.chunks)} chunks)")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
            raise
    
    def load_index(self, filepath: str):
        """Load FAISS index and metadata"""
        try:
            self.index = faiss.read_index(f"{filepath}.index")
            
            with open(f"{filepath}.meta", 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.chunks = data['chunks']
                self.metadata = data['metadata']
            
            logger.info(f"Index loaded from {filepath} ({len(self.chunks)} chunks)")
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            raise