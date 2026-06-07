import os
import sys
from dotenv import load_dotenv

# Add the src directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load the environment variables to get GEMINI_API_KEY
load_dotenv()

from src.embeddings.embedding_generator import EmbeddingGenerator

def test_embedding_generator():
    print("========================================")
    print("  GEMINI EMBEDDING GENERATOR TEST  ")
    print("========================================\n")
    
    # 1. Create a few fake chunked documents (like what TextChunker outputs)
    fake_chunks = [
        {
            "text": "Artificial Intelligence is a massive field.",
            "metadata": {"chunk_index": 0, "source": "fake_doc.txt"}
        },
        {
            "text": "NotebookLM allows you to interact with your documents.",
            "metadata": {"chunk_index": 1, "source": "fake_doc.txt"}
        }
    ]
    
    print("Initializing Gemini API Client...")
    generator = EmbeddingGenerator()
    
    print(f"\nSending {len(fake_chunks)} chunks to Google Gemini...")
    embedded_chunks = generator.generate_embeddings(fake_chunks)
    
    print("\n========================================")
    print("  EMBEDDING GENERATION COMPLETE!  ")
    print("========================================\n")
    
    for doc in embedded_chunks:
        text = doc['text']
        embedding = doc.get('embedding', [])
        
        print(f"[ CHUNK {doc['metadata']['chunk_index']} ]")
        print(f"Text: '{text}'")
        print(f"Embedding Array Length: {len(embedding)} dimensions")
        
        if len(embedding) > 0:
            # Print the first 5 dimensions just to show what it looks like
            preview = [round(num, 4) for num in embedding[:5]]
            print(f"First 5 dimensions: {preview} ...")
        
        print("-" * 40 + "\n")

if __name__ == "__main__":
    test_embedding_generator()
