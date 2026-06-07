import os
import time

from src.document_processing.doc_processor import DocumentProcessor
from src.document_processing.text_chunker import TextChunker
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.database.vector_db import VectorDB

def run_ingestion(file_path: str, collection_name: str = "notebook_documents"):
    print("\n========================================")
    print("  MASTER INGESTION PIPELINE STARTING  ")
    print("========================================\n")
    
    start_time = time.time()

    # 1. PHASE 1: The Reader (Document Processor)
    print(f"[STEP 1] Reading file: {file_path}")
    processor = DocumentProcessor()
    
    with open(file_path, "r", encoding="utf-8") as f:
        text_content = f.read()
        
    documents = processor.process_text(text_content=text_content, source_name=os.path.basename(file_path))
    
    if not documents:
        print("Error: Could not read document.")
        return
        
    print(f"         Successfully extracted text from {len(documents)} document(s).")

    # 2. MODULE 2.1: The Slicer (Semantic Chunking)
    print("\n[STEP 2] Slicing text into chunks...")
    chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
    chunked_documents = chunker.chunk_documents(documents)
    print(f"         Created {len(chunked_documents)} semantic chunks.")

    # 3. MODULE 2.2: The Translator (Vector Embeddings via Google Gemini)
    print("\n[STEP 3] Translating chunks into 768-dimensional math (Google Gemini)...")
    generator = EmbeddingGenerator()
    # This will modify the 'chunked_documents' list in place by adding an 'embedding' key
    processed_chunks = generator.generate_embeddings(chunked_documents)
    print(f"         Successfully generated {len(processed_chunks)} mathematical coordinates.")

    # 4. MODULE 2.3: The Vault (Milvus Lite Vector DB)
    print("\n[STEP 4] Saving data permanently into the Vector Vault...")
    db = VectorDB()
    
    # Ensure collection exists
    db.create_collection(collection_name=collection_name, dimension=768)
    
    # Insert the fully processed chunks
    db.insert_documents(collection_name=collection_name, chunked_documents=processed_chunks)
    
    end_time = time.time()
    
    print("\n========================================")
    print(f"  PIPELINE COMPLETE IN {end_time - start_time:.2f} SECONDS!  ")
    print("========================================\n")

if __name__ == "__main__":
    # For testing, let's run it automatically on our fake AI essay
    test_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "sample_data", "fake_ai_essay.txt"))
    run_ingestion(test_file, collection_name="notebook_documents")
