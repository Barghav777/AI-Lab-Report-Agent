"""
RAG Components Package for the Lab Report Agent.

This package contains modules for the Retrieval-Augmented Generation (RAG) pipeline:
- extractor: Handles extracting raw text from uploaded documents (PDF, DOCX, etc.).
- vector_store: Handles text chunking, embedding, and retrieving relevant context.
"""

# Import the main functions from the modules to make them directly accessible
# from the package, which simplifies import statements in other files.
from .extractor import extract_text_from_file
from .vector_store import get_relevant_context

# The __all__ variable defines the public API of this package.
# When a user writes 'from rag_components import *', only these names will be imported.
__all__ = [
    'extract_text_from_file',
    'get_relevant_context'
]