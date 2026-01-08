import tiktoken
from typing import List

class TextChunker:
    """Handle text chunking with various strategies"""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def chunk_by_tokens(self, text: str) -> List[str]:
        """Chunk text by token count with overlap"""
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), self.chunk_size - self.overlap):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            if i + self.chunk_size >= len(tokens):
                break
        
        return chunks
    
    def chunk_by_sentences(self, text: str, max_chunk_size: int = None) -> List[str]:
        """Chunk text by sentences, respecting max size"""
        if max_chunk_size is None:
            max_chunk_size = self.chunk_size
        
        # Simple sentence splitting (can be improved with spaCy/nltk)
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() + '.' for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_tokens = len(self.tokenizer.encode(sentence))
            
            if current_size + sentence_tokens > max_chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_size = sentence_tokens
            else:
                current_chunk.append(sentence)
                current_size += sentence_tokens
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks