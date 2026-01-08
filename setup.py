from setuptools import setup, find_packages

setup(
    name="rag-chatbot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "faiss-cpu>=1.7.4",
        "sentence-transformers>=2.2.2",
        "tiktoken>=0.5.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "PyPDF2>=3.0.0",
        "python-docx>=1.1.0",
        "pyyaml>=6.0",
        "loguru>=0.7.0",
    ],
    python_requires=">=3.8",
)