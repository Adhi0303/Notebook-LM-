"""
Embedding Generator Module
Handles generation of vector embeddings from text chunks using Cohere API v2.
"""

import os
from typing import List, Dict, Any
import time
import cohere

class EmbeddingGenerator:
    def __init__(self):
        """
        Initializes the Cohere API client.
        """
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not found in environment variables.")
        
        # Use ClientV2 as per Cohere's latest documentation
        self.client = cohere.ClientV2(api_key=api_key)
        self.model_name = "embed-v4.0"

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
            # Cohere API v2 allows up to 96 inputs per embed request
            batch_size = 90
            
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                
                # Retry loop for rate limits (Cohere gives 1000 calls per month, 100 RPM free)
                for attempt in range(5):
                    try:
                        res = self.client.embed(
                            model=self.model_name,
                            texts=batch_texts,
                            input_type="search_document",
                            embedding_types=["float"]
                        )
                        # ClientV2 returns embeddings inside .embeddings.float_
                        for emb in res.embeddings.float_:
                            embeddings.append(emb)
                        break
                    except Exception as e:
                        if "429" in str(e) or "503" in str(e):
                            wait_time = 2 ** attempt
                            print(f"API Error (possibly rate limit): {e}. Retrying in {wait_time}s...")
                            time.sleep(wait_time)
                        else:
                            raise e
                else:
                    print("Failed to embed batch after 5 attempts.")
                    break

            # Attach the generated embeddings back to our original document dictionaries
            for i, doc in enumerate(chunked_documents):
                if i < len(embeddings):
                    doc["embedding"] = embeddings[i]

            return chunked_documents

        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            return chunked_documents

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Takes a single search query string and generates its embedding.
        Crucially, uses input_type='search_query' which tells Cohere
        to optimize this math coordinate to attract matching search_documents.
        """
        try:
            res = self.client.embed(
                model=self.model_name,
                texts=[query],
                input_type="search_query",
                embedding_types=["float"]
            )
            return res.embeddings.float_[0]
        except Exception as e:
            print(f"Error generating query embedding: {str(e)}")
            return []
