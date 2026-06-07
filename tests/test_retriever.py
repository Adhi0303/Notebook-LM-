import os
import sys

# Add the src directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generation.retriever import SemanticRetriever

def test_retriever():
    print("========================================")
    print("  SEMANTIC RETRIEVER TEST  ")
    print("========================================\n")

    # The user asks a question in the chat interface
    user_query = "Why do we need to use semantic chunking?"
    print(f"User Question: '{user_query}'\n")

    print("[STEP 1] Initializing Semantic Retriever...")
    retriever = SemanticRetriever()

    print("\n[STEP 2] Searching the Vector Vault...")
    # Get the top 2 most relevant chunks from the database
    results = retriever.retrieve(query=user_query, top_k=2)

    print("\n========================================")
    print("  RETRIEVAL RESULTS  ")
    print("========================================\n")

    if not results:
        print("No results found. Did you run the ingestion pipeline first?")
        return

    for i, hit in enumerate(results):
        print(f"--- MATCH {i+1} ---")
        print(f"Score: {hit['score']:.4f}")
        print(f"Source: {hit['source']} (Chunk {hit['chunk_index']})")
        print(f"Text:\n{hit['text']}")
        print("-" * 40)
        print()

if __name__ == "__main__":
    test_retriever()
