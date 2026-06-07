"""
Document Processor Module
Handles parsing of PDFs, TXT, and Markdown files into raw text with metadata.
"""

import fitz  # PyMuPDF
from typing import List, Dict, Any, Union
import io

class DocumentProcessor:
    def __init__(self):
        pass

    def process_pdf(self, file_data: Union[str, bytes, io.BytesIO], source_name: str) -> List[Dict[str, Any]]:
        """
        Extracts text from a PDF, returning a list of dictionaries where each
        dictionary represents a single page with its associated metadata.
        """
        documents = []
        
        try:
            # Handle both file paths and byte streams (for Streamlit uploads)
            if isinstance(file_data, str):
                pdf_document = fitz.open(file_data)
            elif isinstance(file_data, bytes):
                pdf_document = fitz.open(stream=file_data, filetype="pdf")
            elif hasattr(file_data, "read"):
                # Handle BytesIO or similar file-like objects
                pdf_document = fitz.open(stream=file_data.read(), filetype="pdf")
            else:
                raise ValueError("file_data must be a path, bytes, or file-like object")

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text = page.get_text("text").strip()
                
                # Only add pages that actually have text
                if text:
                    documents.append({
                        "text": text,
                        "metadata": {
                            "source": source_name,
                            "page": page_num + 1,  # 1-indexed for human readability
                            "type": "pdf"
                        }
                    })
                    
            pdf_document.close()
            return documents
            
        except Exception as e:
            print(f"Error processing PDF {source_name}: {str(e)}")
            return []

    def process_text(self, text_content: str, source_name: str, file_type: str = "text") -> List[Dict[str, Any]]:
        """
        Processes plain text or markdown files. 
        Treats the entire text as a single 'page' for metadata purposes.
        """
        if not text_content.strip():
            return []
            
        return [{
            "text": text_content.strip(),
            "metadata": {
                "source": source_name,
                "page": 1,
                "type": file_type
            }
        }]
