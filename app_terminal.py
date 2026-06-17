import os
import sys
import time
import shutil
import threading
from typing import List, Dict, Any

from src.document_processing.doc_processor import DocumentProcessor
from src.document_processing.text_chunker import TextChunker
from src.embeddings.token_batcher import TokenBatcher
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.database.vector_db import VectorDB
from src.generation.rag import RAGEngine

# A global thread-safe event flag to control the state machine.
# When it is SET, it means the background thread is actively embedding math,
# so the chat interface MUST wait.
is_embedding = threading.Event()

# To keep track of how many buckets have been processed
progress_lock = threading.Lock()
total_chunks = 0
processed_chunks_count = 0

def run_background_ingestion(test_file: str, collection_name: str = "notebook_documents"):
    """
    The background worker that safely reads the PDF, chunks it, and ingests
    in token-aware buckets.
    """
    global total_chunks
    global processed_chunks_count

    try:
        # STEP 1: Extraction
        processor = DocumentProcessor()
        
        if test_file.lower().endswith(".pdf"):
            raw_documents = processor.process_pdf(test_file, source_name=os.path.basename(test_file))
        else:
            with open(test_file, "r", encoding="utf-8") as f:
                text_content = f.read()
            raw_documents = processor.process_text(text_content=text_content, source_name=os.path.basename(test_file))
        
        # STEP 2: Chunking
        chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
        chunked_documents = chunker.chunk_documents(raw_documents)
        
        with progress_lock:
            total_chunks = len(chunked_documents)
            
        # STEP 3: Token-Aware Batching
        batcher = TokenBatcher(token_limit=90000)
        buckets = batcher.batch_documents(chunked_documents)
        total_buckets = len(buckets)
        
        print(f"\n[BACKGROUND] Document split into {total_chunks} chunks.")
        print(f"[BACKGROUND] Safely grouped into {total_buckets} token-aware buckets (<90k tokens each).")

        # Drop the old database to avoid Windows FileLock issues
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "notebook_lm.db"))
        if os.path.exists(db_path):
            if os.path.isdir(db_path):
                shutil.rmtree(db_path, ignore_errors=True)
            else:
                os.remove(db_path)

        db = VectorDB()
        db.create_collection(collection_name=collection_name, dimension=1536)
        embedder = EmbeddingGenerator()

        # STEP 4: State Machine Incremental Processing
        for i, bucket in enumerate(buckets):
            # LOCK THE CHAT: We are actively embedding!
            is_embedding.set()
            
            # Embed
            processed_bucket = embedder.generate_embeddings(bucket)
            
            # Insert
            db.insert_documents(collection_name=collection_name, chunked_documents=processed_bucket)
            
            with progress_lock:
                processed_chunks_count += len(bucket)
                percent = int((processed_chunks_count / total_chunks) * 100)
                
            # UNLOCK THE CHAT: Embedding is done for this bucket!
            is_embedding.clear()
            
            print(f"\n[BACKGROUND] Bucket {i+1}/{total_buckets} completed. Ingestion {percent}% complete.")
            
            # Cooldown logic for Cohere Rate Limits
            if i < len(buckets) - 1:
                print(f"[BACKGROUND] Sleeping for 60 seconds to let Cohere token quota reset...")
                # We sleep while the lock is OPEN, so the user can chat freely!
                time.sleep(60)

        print("\n[BACKGROUND] 100% of the document has been successfully ingested!")
        
    except Exception as e:
        print(f"\n[BACKGROUND ERROR] The ingestion pipeline crashed: {e}")
        is_embedding.clear()

def run_chat_interface():
    """
    The main thread interface for the user.
    """
    print("========================================")
    print("  NOTEBOOK LM - UNIFIED TERMINAL APP  ")
    print("========================================\n")
    
    print("Starting background ingestion...")
    # Start the ingestion in a background thread
    test_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "AI_FreeBook.pdf"))
    
    # Wait until the background thread starts and sets the lock before initializing RAGEngine
    # to avoid a race condition trying to initialize VectorDB while it's being deleted.
    time.sleep(2) 
    
    # Actually wait until at least the first bucket is done or it's sleeping, so we don't 
    # try to query a completely empty VectorDB or hit Milvus while it's creating collections.
    while is_embedding.is_set():
        time.sleep(0.5)

    print("[SYSTEM] Initializing RAG Chat Engine...")
    engine = RAGEngine()
    
    print("\n[SYSTEM] Ready! Type 'exit' to quit.")
    print("[SYSTEM] You can ask questions while the background ingestion processes the remaining book!\n")

    while True:
        try:
            # Let the user type
            user_input = input("\nYou: ")
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            if not user_input.strip():
                continue

            # ** STATE MACHINE CHECK **
            if is_embedding.is_set():
                print("...Hold on, the AI is actively ingesting the next batch. Your question is queued...")
                # Wait until the background thread finishes its math
                is_embedding.wait()

            print("\nAI is thinking...")
            answer = engine.ask(user_input)
            
            print("\n--- AI RESPONSE ---")
            print(answer)
            print("-------------------\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)

if __name__ == "__main__":
    import os
    test_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "AI_FreeBook.pdf"))
    
    # Launch background thread
    ingest_thread = threading.Thread(target=run_background_ingestion, args=(test_file,), daemon=True)
    ingest_thread.start()
    
    # Launch main chat loop
    run_chat_interface()
