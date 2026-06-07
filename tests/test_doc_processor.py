import os
import sys
import fitz  # PyMuPDF

# Add the src directory to the python path so we can import our module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.document_processing.doc_processor import DocumentProcessor

def create_dummy_pdf(filename="dummy.pdf"):
    """Create a simple 2-page PDF for testing."""
    doc = fitz.open()
    
    # Page 1
    page1 = doc.new_page()
    page1.insert_text((50, 50), "This is page 1 of the dummy PDF.")
    page1.insert_text((50, 70), "We are testing the NotebookLM Clone document parser.")
    
    # Page 2
    page2 = doc.new_page()
    page2.insert_text((50, 50), "This is page 2.")
    page2.insert_text((50, 70), "It should have different metadata.")
    
    doc.save(filename)
    doc.close()
    return filename

def test_document_processor():
    print("--- Testing DocumentProcessor ---")
    processor = DocumentProcessor()
    
    # 1. Test Text Processing
    print("\n1. Testing raw text processing...")
    txt_content = "This is a simple text document. It doesn't have pages."
    txt_docs = processor.process_text(txt_content, source_name="sample.txt")
    print(f"Extracted docs: {len(txt_docs)}")
    print(f"Doc 1 Text: {txt_docs[0]['text']}")
    print(f"Doc 1 Metadata: {txt_docs[0]['metadata']}")
    assert len(txt_docs) == 1
    assert txt_docs[0]['metadata']['source'] == "sample.txt"
    assert txt_docs[0]['metadata']['page'] == 1
    
    # 2. Test PDF Processing
    print("\n2. Testing PDF processing...")
    pdf_file = create_dummy_pdf("test_dummy.pdf")
    
    pdf_docs = processor.process_pdf(pdf_file, source_name="test_dummy.pdf")
    print(f"Extracted docs: {len(pdf_docs)}")
    
    for i, doc in enumerate(pdf_docs):
        print(f"\n--- Page {i+1} ---")
        print(f"Text: {doc['text']}")
        print(f"Metadata: {doc['metadata']}")
        
    assert len(pdf_docs) == 2
    assert "page 1" in pdf_docs[0]['text']
    assert pdf_docs[0]['metadata']['page'] == 1
    assert "page 2" in pdf_docs[1]['text']
    assert pdf_docs[1]['metadata']['page'] == 2
    
    # Cleanup
    os.remove(pdf_file)
    print("\n✅ All tests passed successfully!")

if __name__ == "__main__":
    test_document_processor()
