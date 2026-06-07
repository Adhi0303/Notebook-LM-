import os
import sys

# Add the src directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.vector_db import VectorDB

def test_vector_db():
    print("========================================")
    print("  MILVUS LITE VECTOR DB TEST  ")
    print("========================================\n")

    # 1. Initialize the Database
    # We will use a separate test database file so we don't mess up the real one
    db_path = "./test_milvus.db"
    import uuid
    db = VectorDB(db_path=db_path)
    
    # On Windows, Milvus Lite can have file-locking issues if we try to drop and recreate
    # the exact same collection repeatedly in a quick test. 
    # To bypass this, we will just use a uniquely named collection for every test run!
    collection_name = f"test_collection_{uuid.uuid4().hex[:8]}"

    # 2. Create the Collection (Dimensions MUST be exactly 3 for this test to keep it simple)
    # Note: In real life, this will be 768. But for a visual test, 3 is easier.
    db.create_collection(collection_name=collection_name, dimension=3)

    # 3. Create some fake embeddings (3-dimensional math for Dogs, Cars, Apples)
    fake_documents = [
        {
            "text": "A golden retriever is a great family dog.",
            "metadata": {"source": "dog_book.txt", "chunk_index": 0},
            "embedding": [0.9, 0.1, 0.0]  # High in 'animal' dimension
        },
        {
            "text": "The new sports car goes from 0 to 60 in 3 seconds.",
            "metadata": {"source": "car_magazine.txt", "chunk_index": 1},
            "embedding": [0.0, 0.9, 0.1]  # High in 'vehicle' dimension
        },
        {
            "text": "Granny Smith apples are incredibly crisp and tart.",
            "metadata": {"source": "fruit_guide.txt", "chunk_index": 2},
            "embedding": [0.1, 0.0, 0.9]  # High in 'food' dimension
        }
    ]

    # 4. Insert into Database
    db.insert_documents(collection_name, fake_documents)

    # 5. Perform an Approximate Nearest Neighbor Search
    print("\n--- SEARCHING THE DATABASE ---")
    print("User Search Query: 'Tell me about fast vehicles.'")
    
    # We pretend the EmbeddingGenerator gave us this vector for the search query:
    search_vector = [0.0, 0.85, 0.15] # Highly aligned with the 'vehicle' dimension

    print(f"Generated Math for Query: {search_vector}")
    
    # Find the top 1 closest match
    results = db.search(collection_name, search_vector, limit=1)

    print("\n========================================")
    print("  SEARCH RESULTS  ")
    print("========================================\n")
    
    for hit in results:
        print(f"Math Score (Cosine Similarity): {hit['score']:.4f}")
        print(f"Source Document: {hit['source']}")
        print(f"Matched Text: '{hit['text']}'")
        print("-" * 40)

if __name__ == "__main__":
    test_vector_db()
