import os
from typing import List, Dict, Any
from pymilvus import MilvusClient

class VectorDB:
    def __init__(self, db_path: str = "./notebook_lm.db"):
        """
        Initializes the Vector Database.
        By providing a local file path, Milvus Lite automatically creates
        a serverless, local vector database!
        """
        self.db_path = db_path
        self.client = MilvusClient(uri=self.db_path)

    def create_collection(self, collection_name: str, dimension: int = 768):
        """
        Creates a collection (like a SQL table) if it doesn't already exist.
        The dimension MUST perfectly match the output of our EmbeddingGenerator (768).
        """
        if self.client.has_collection(collection_name):
            print(f"Collection '{collection_name}' already exists.")
            return

        print(f"Creating collection '{collection_name}' with {dimension} dimensions...")
        
        # This simplified API automatically sets up an 'id' primary key
        # and enables dynamic fields so we can throw any metadata into it!
        self.client.create_collection(
            collection_name=collection_name,
            dimension=dimension,
            metric_type="COSINE", # Cosine similarity is the industry standard for text embeddings
            auto_id=True # Tells Milvus to automatically generate unique IDs for each chunk
        )
        print("Collection created successfully!")

    def insert_documents(self, collection_name: str, chunked_documents: List[Dict[str, Any]]):
        """
        Takes the fully processed chunks (with text, metadata, and embeddings)
        and formats them for Milvus insertion.
        """
        data_to_insert = []
        for i, doc in enumerate(chunked_documents):
            # We must provide the exact mathematical array to the 'vector' field
            if "embedding" not in doc:
                continue

            record = {
                "vector": doc["embedding"],
                "text": doc.get("text", ""),
                "source": doc.get("metadata", {}).get("source", "unknown"),
                "chunk_index": doc.get("metadata", {}).get("chunk_index", -1)
            }
            data_to_insert.append(record)

        if not data_to_insert:
            print("No valid documents with embeddings found to insert.")
            return

        print(f"Inserting {len(data_to_insert)} vectors into '{collection_name}'...")
        res = self.client.insert(
            collection_name=collection_name,
            data=data_to_insert
        )
        print("Insertion complete!")
        return res

    def search(self, collection_name: str, query_vector: list, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Performs an Approximate Nearest Neighbor (ANN) search.
        Finds the top chunks mathematically closest to the query_vector.
        """
        print(f"Searching for the top {limit} closest matches...")
        
        results = self.client.search(
            collection_name=collection_name,
            data=[query_vector],
            limit=limit,
            search_params={"metric_type": "COSINE"},
            output_fields=["text", "source", "chunk_index"] # We tell Milvus to return the original text!
        )
        
        # Clean up the output to make it easy to read
        formatted_results = []
        # results is a list of lists (one list per query vector)
        for hit in results[0]:
            formatted_results.append({
                "score": hit["distance"], # How close was the match mathematically?
                "text": hit["entity"]["text"],
                "source": hit["entity"]["source"],
                "chunk_index": hit["entity"]["chunk_index"]
            })
            
        return formatted_results
