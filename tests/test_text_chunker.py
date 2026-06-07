import os
import sys

# Add the src directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.document_processing.text_chunker import TextChunker

def test_semantic_chunking():
    print("========================================")
    print("  SEMANTIC TEXT CHUNKER TESTING  ")
    print("========================================\n")
    
    # 1. Create a massive fake document without newlines to force mid-paragraph splitting
    long_text = "The killer of the story is the butler. Wait, let me start over. This is a story about a very long document that needs to be chunked. Artificial Intelligence is a massive field that includes subfields like Machine Learning, Deep Learning, and Natural Language Processing. When we build an application like NotebookLM, we have to process thousands of words at once. However, Language Models have a strict memory limit known as the Context Window. If we pass a book that is one hundred thousand words long, the model will forget the beginning by the time it reaches the end. This is why we must use semantic chunking. Chunking is the process of slicing a document into smaller, bite-sized pieces. But we can't just slice it anywhere. If we slice it in the middle of a sentence, we lose the context. That is why we use an overlapping strategy, where the end of Chunk A overlaps with the beginning of Chunk B. LangChain provides a RecursiveCharacterTextSplitter that handles this beautifully. It tries to split by paragraphs first. If a paragraph is too long, it splits by sentences. If a sentence is too long, it splits by words. This ensures our semantic meaning is perfectly preserved!"
    
    # Simulate the output from Phase 1 (Data Ingestion)
    phase_1_output = [{
        "text": long_text.strip(),
        "metadata": {
            "source": "fake_ai_essay.txt",
            "page": 1,
            "type": "text"
        }
    }]
    
    print("Original Document Length:", len(long_text.strip()), "characters")
    print("Original Number of Documents: 1\n")
    
    # 2. Initialize the Chunker
    # We will use a very small chunk size to force it to split our short test text
    chunker = TextChunker(chunk_size=250, chunk_overlap=50)
    
    # 3. Process the documents
    chunked_docs = chunker.chunk_documents(phase_1_output)
    
    print("========================================")
    print(f" Chunking Complete! Sliced into {len(chunked_docs)} chunks.")
    print("========================================")
    
    # 4. Print the results to verify overlap and metadata
    for doc in chunked_docs:
        print(f"\n[ CHUNK {doc['metadata']['chunk_index'] + 1} / {doc['metadata']['total_chunks']} ]")
        print(f"Source: {doc['metadata']['source']}")
        print(f"Length: {len(doc['text'])} characters")
        print("-" * 40)
        print(doc['text'])
        print("-" * 40)

if __name__ == "__main__":
    test_semantic_chunking()
