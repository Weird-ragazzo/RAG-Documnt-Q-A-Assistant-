import os
from typing import List, Dict
import PyPDF2
import docx
from pathlib import Path
from loguru import logger

class DocumentLoader:
    """Load documents from various file formats"""
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = Path(data_dir)
        self.supported_formats = {'.txt', '.pdf', '.docx', '.md'}
    
    def load_txt(self, filepath: Path) -> str:
        """Load text file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_pdf(self, filepath: Path) -> str:
        """Load PDF file"""
        text = []
        with open(filepath, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text.append(page.extract_text())
        return '\n'.join(text)
    
    def load_docx(self, filepath: Path) -> str:
        """Load DOCX file"""
        doc = docx.Document(filepath)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    
    def load_file(self, filepath: Path) -> Dict[str, str]:
        """Load a single file"""
        ext = filepath.suffix.lower()
        
        try:
            if ext == '.txt' or ext == '.md':
                text = self.load_txt(filepath)
            elif ext == '.pdf':
                text = self.load_pdf(filepath)
            elif ext == '.docx':
                text = self.load_docx(filepath)
            else:
                logger.warning(f"Unsupported format: {ext}")
                return None
            
            logger.info(f"Loaded: {filepath.name} ({len(text)} chars)")
            
            return {
                'text': text,
                'source': filepath.name,
                'path': str(filepath)
            }
        except Exception as e:
            logger.error(f"Error loading {filepath}: {e}")
            return None
    
    def load_directory(self, directory: str = None) -> List[Dict[str, str]]:
        """Load all supported documents from directory"""
        if directory is None:
            directory = self.data_dir
        else:
            directory = Path(directory)
        
        documents = []
        
        for filepath in directory.rglob('*'):
            if filepath.is_file() and filepath.suffix.lower() in self.supported_formats:
                doc = self.load_file(filepath)
                if doc:
                    documents.append(doc)
        
        logger.info(f"Loaded {len(documents)} documents from {directory}")
        return documents