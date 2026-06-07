"""
Embedding Generator Module
Handles generation of vector embeddings from text chunks using Google Gemini.
"""

import os
from typing import List, Dict, Any
from google import genai

class EmbeddingGenerator:
    def __init__(self):
        """
        Initializes the Gemini API client.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        self.client = genai.Client(api_key=api_key)
        # The recommended embedding model for Gemini
        self.model_name = "gemini-embedding-2"

    def generate_embeddings(self, chunked_documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes a list of chunked documents and generates embeddings in batches.
        Adds the 'embedding' array to each document.
        """
        if not chunked_documents:
            return []

        # Extract all text chunks into a list for batch processing
        texts = [doc.get("text", "") for doc in chunked_documents]

        try:
            embeddings = []
            for text in texts:
                result = self.client.models.embed_content(
                    model=self.model_name,
                    contents=text,
                    config={
                        "task_type": "RETRIEVAL_DOCUMENT",
                        "output_dimensionality": 768
                    }
                )
                # The API returns a result object with embeddings. Each has a 'values' list.
                embeddings.append(result.embeddings[0].values)

            # Attach the generated embeddings back to our original document dictionaries
            for i, doc in enumerate(chunked_documents):
                doc["embedding"] = embeddings[i]

            return chunked_documents

        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            return chunked_documents

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Takes a single search query string and generates its embedding.
        Crucially, uses task_type='RETRIEVAL_QUERY' which tells Gemini
        to optimize this math coordinate to attract matching documents.
        """
        try:
            result = self.client.models.embed_content(
                model=self.model_name,
                contents=query,
                config={
                    "task_type": "RETRIEVAL_QUERY",
                    "output_dimensionality": 768
                }
            )
            return result.embeddings[0].values
        except Exception as e:
            print(f"Error generating query embedding: {str(e)}")
            return []
