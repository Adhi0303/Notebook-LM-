from typing import List, Dict, Any
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.database.vector_db import VectorDB

class SemanticRetriever:
    def __init__(self, db_path: str = "./notebook_lm.db"):
        """
        Initializes the Semantic Retriever.
        It connects to the Google Gemini Embeddings API and our local Milvus Database.
        """
        self.embedding_generator = EmbeddingGenerator()
        self.vector_db = VectorDB(db_path=db_path)

    def retrieve(self, query: str, collection_name: str = "notebook_documents", top_k: int = 3) -> List[Dict[str, Any]]:
        """
        The core of Semantic Search.
        1. Translates the user's text query into a 768-dimensional coordinate.
        2. Searches the Vector Vault using Cosine Similarity.
        3. Returns the top_k most relevant chunks of text.
        """
        # Step 1: Translate the query into math using task_type='RETRIEVAL_QUERY'
        query_embedding = self.embedding_generator.generate_query_embedding(query)
        
        if not query_embedding:
            print("Failed to generate embedding for query.")
            return []

        # Step 2 & 3: Search the vault and return the top results
        results = self.vector_db.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=top_k
        )
        
        return results
