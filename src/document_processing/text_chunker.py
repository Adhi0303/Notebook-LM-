"""
Text Chunker Module
Splits large text documents into smaller semantic chunks with overlap.
"""

from typing import List, Dict, Any
import copy
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initializes the RecursiveCharacterTextSplitter.
        Defaults: 1000 characters per chunk, 200 characters overlap.
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes a list of standard document dictionaries.
        Returns a new list of chunked document dictionaries, preserving metadata.
        """
        chunked_docs = []
        
        for doc in documents:
            text = doc.get("text", "")
            metadata = doc.get("metadata", {})
            
            # Use LangChain to split the text
            text_chunks = self.splitter.split_text(text)
            
            # Create a new document object for each chunk
            for i, chunk in enumerate(text_chunks):
                # We do a deep copy of metadata so each chunk gets its own unique dictionary
                chunk_metadata = copy.deepcopy(metadata)
                
                # Add chunk indexing so we know the order of the pieces
                chunk_metadata["chunk_index"] = i
                chunk_metadata["total_chunks"] = len(text_chunks)
                
                chunked_docs.append({
                    "text": chunk,
                    "metadata": chunk_metadata
                })
                
        return chunked_docs
