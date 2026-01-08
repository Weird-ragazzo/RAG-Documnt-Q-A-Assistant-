from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
from loguru import logger

class EmbeddingManager:
    """Manage text embeddings"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(f"Embedding dimension: {self.embedding_dim}")
    
    def embed_texts(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Generate embeddings for multiple texts"""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        return embeddings.astype('float32')
    
    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for a single query"""
        embedding = self.model.encode([query], convert_to_numpy=True)
        return embedding.astype('float32')